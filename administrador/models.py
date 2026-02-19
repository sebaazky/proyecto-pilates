from django.db import models
from django.utils import timezone


class Service(models.Model):
    """
    Modelo para gestionar los servicios ofrecidos por el centro de Pilates.
    Estos servicios se muestran dinámicamente en la landing page.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del servicio",
        help_text="Ej: Clases de Pilates, Kinesiología"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción completa del servicio"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Precio (CLP)",
        help_text="Precio en pesos chilenos (sin decimales)"
    )
    image = models.ImageField(
        upload_to='services/',
        verbose_name="Imagen",
        help_text="Imagen representativa del servicio"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, se muestra en la landing page"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número aparece primero)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    Modelo para gestionar publicaciones de blog/novedades.
    Se muestran en la sección de novedades de la landing page.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la publicación"
    )
    content = models.TextField(
        verbose_name="Contenido",
        help_text="Contenido completo de la publicación"
    )
    image = models.ImageField(
        upload_to='blog/',
        verbose_name="Imagen destacada",
        help_text="Imagen principal de la publicación (obligatoria)",
        blank=False,  # ← CAMBIO: ahora es obligatoria
        null=False    # ← CAMBIO: no puede ser NULL
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publicado",
        help_text="Si está publicado, se muestra en la landing page"
    )
    published_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de publicación",
        help_text="Se establece automáticamente al crear/editar"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_excerpt(self, words=30):
        """Retorna un extracto del contenido"""
        word_list = self.content.split()
        if len(word_list) > words:
            return ' '.join(word_list[:words]) + '...'
        return self.content


class ContactMessage(models.Model):
    """
    Modelo para gestionar mensajes de contacto recibidos desde la landing page.
    Los administradores pueden ver y gestionar estos mensajes.
    """
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('read', 'Leído'),
        ('replied', 'Respondido'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        blank=True
    )
    message = models.TextField(
        verbose_name="Mensaje"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Estado"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Notas internas",
        help_text="Notas privadas del administrador (no visibles para el cliente)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de recepción"
    )

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"


class Instructor(models.Model):
    """
    Modelo para gestionar instructores del centro.
    Se muestran en la sección 'El Equipo' de la landing page.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre completo",
        help_text="Nombre y apellido del instructor"
    )
    photo = models.ImageField(
        upload_to='instructors/',
        verbose_name="Foto",
        help_text="Foto profesional del instructor"
    )
    specialties = models.CharField(
        max_length=200,
        verbose_name="Especialidades",
        help_text="Ej: Mat & Reformer - Instructora Principal"
    )
    bio = models.TextField(
        verbose_name="Biografía",
        help_text="Descripción breve del instructor (experiencia, enfoque)"
    )
    certifications = models.TextField(
        blank=True,
        verbose_name="Certificaciones",
        help_text="Lista de certificaciones y formación (opcional)"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número aparece primero)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está activo, se muestra en la landing page"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
