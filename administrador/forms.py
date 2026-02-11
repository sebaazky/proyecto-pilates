"""
administrador/forms.py
Formularios para el panel de administración CMS.
Todo se gestiona principalmente desde Django Admin.
"""
from django import forms
from .models import Service, BlogPost, ContactMessage


class ServiceForm(forms.ModelForm):
    """
    Formulario para gestionar servicios.
    (Opcional - Django Admin ya maneja esto)
    """
    class Meta:
        model = Service
        fields = ['name', 'description', 'price',
                  'image', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class BlogPostForm(forms.ModelForm):
    """
    Formulario para gestionar publicaciones del blog.
    (Opcional - Django Admin ya maneja esto)
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image',
                  'is_published', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class ContactMessageForm(forms.ModelForm):
    """
    Formulario para actualizar el estado de mensajes de contacto.
    (Opcional - Django Admin ya maneja esto)
    """
    class Meta:
        model = ContactMessage
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
