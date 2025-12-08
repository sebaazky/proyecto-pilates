# index/forms.py
from django import forms
from .models import Contacto  # Usa el modelo Contacto de la app index
from .models import NewsPost
from django.utils import timezone


class ContactoPublicoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ["nombre", "correo", "telefono", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tu nombre"}
            ),
            "correo": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Tu correo"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tu teléfono"}
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe tu mensaje aquí",
                    "rows": 5,
                }
            ),
        }


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "tag", "image", "excerpt",
                  "body", "published", "featured"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Título",
            }),
            "tag": forms.Select(attrs={
                "class": "form-select",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "excerpt": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Resumen corto…",
            }),
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Contenido (HTML simple permitido)",
            }),
            "published": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "featured": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        # Si se marca “publicado” y no hay fecha, la seteamos
        if obj.published and not obj.published_at:
            obj.published_at = timezone.now()
        if commit:
            obj.save()
        return obj
