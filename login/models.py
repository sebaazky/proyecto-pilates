from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario personalizado del sistema.
    Solo permite usuarios administradores para gestionar el CMS.
    """
    ROLES = [
        ("administrador", "Administrador"),  # ✅ Solo este rol
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default="administrador",  # ✅ Default cambiado
        verbose_name="Rol",
        help_text="Rol del usuario en el sistema"
    )
