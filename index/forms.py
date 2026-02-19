# index/forms.py
from django import forms
from django.core.exceptions import ValidationError
import re


class ContactoPublicoForm(forms.Form):
    """
    Formulario de contacto público.
    No usa ModelForm porque el modelo ContactMessage está en la app administrador.
    """
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre',
            'pattern': '[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+',
            'title': 'Solo letras permitidas',
        })
    )

    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu correo',
        })
    )

    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu teléfono',
            'type': 'tel',
        })
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu mensaje aquí',
            'rows': 5,
        })
    )

    def clean_nombre(self):
        """Validar que el nombre solo contenga letras y espacios."""
        nombre = self.cleaned_data.get('nombre', '').strip()

        if not nombre:
            raise ValidationError('El nombre es obligatorio.')

        # Solo letras (incluyendo acentos), espacios y guiones
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras.')

        # Mínimo 2 caracteres
        if len(nombre) < 2:
            raise ValidationError(
                'El nombre debe tener al menos 2 caracteres.')

        return nombre

    def clean_telefono(self):
        """Validar formato de teléfono."""
        telefono = self.cleaned_data.get('telefono', '').strip()

        # Teléfono es opcional, si está vacío lo aceptamos
        if not telefono:
            return telefono

        # Remover espacios, guiones y paréntesis para validar
        telefono_limpio = re.sub(r'[\s\-\(\)\+]', '', telefono)

        # Verificar que solo contenga dígitos después de limpiar
        if not telefono_limpio.isdigit():
            raise ValidationError('El teléfono solo puede contener números.')

        # Verificar longitud (entre 8 y 15 dígitos es razonable)
        if len(telefono_limpio) < 8 or len(telefono_limpio) > 15:
            raise ValidationError(
                'El teléfono debe tener entre 8 y 15 dígitos.')

        return telefono
