"""
administrador/forms.py
Formularios para el panel de administración CMS.
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import Service, BlogPost, ContactMessage, Instructor

User = get_user_model()


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price',
                  'image', 'is_active', 'order']
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price':       forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'order':       forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        """Validar que el precio sea mayor a 0."""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('El precio debe ser mayor a $0.')
        return price


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        # ← CAMBIO: published_date eliminado de fields, se maneja automáticamente
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['status', 'admin_notes']
        widgets = {
            'status':      forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['name', 'photo', 'specialties', 'bio',
                  'certifications', 'order', 'is_active']
        widgets = {
            'name':           forms.TextInput(attrs={'class': 'form-control'}),
            'specialties':    forms.TextInput(attrs={'class': 'form-control'}),
            'bio':            forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order':          forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ─────────────────────────────────────────────────────────────
# FORMULARIOS DE USUARIO — solo para superadmin
# ─────────────────────────────────────────────────────────────

class UsuarioCrearForm(forms.ModelForm):
    """Crea un nuevo usuario administrador con contraseña hasheada."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres'
        }),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(
                {'password2': 'Las contraseñas no coinciden.'})
        if p1 and len(p1) < 8:
            raise forms.ValidationError(
                {'password1': 'La contraseña debe tener al menos 8 caracteres.'})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.rol = 'administrador'
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class UsuarioEditarForm(forms.ModelForm):
    """
    Edita un usuario existente.
    Contraseña opcional — si se deja vacía, no se cambia.
    """
    password1 = forms.CharField(
        label='Nueva contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar vacío para no cambiar',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite la nueva contraseña',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError(
                    {'password2': 'Las contraseñas no coinciden.'})
            if len(p1) < 8:
                raise forms.ValidationError(
                    {'password1': 'Mínimo 8 caracteres.'})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user
