"""
administrador/models.py
Modelos de la aplicación administrador.
"""
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image_field, max_width=1920, max_height=1080, quality=90):
    """
    Comprime una imagen usando Pillow.

    Args:
        image_field: Campo ImageField de Django
        max_width: Ancho máximo en píxeles
        max_height: Alto máximo en píxeles
        quality: Calidad JPEG (1-100)

    Returns:
        InMemoryUploadedFile: Imagen comprimida
    """
    img = Image.open(image_field)

    # Convertir a RGB
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[-1])
        else:
            background.paste(img)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Redimensionar si es necesario
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # Comprimir
    output = BytesIO()
    img.save(
        output,
        format='JPEG',
        quality=quality,
        optimize=True,
        progressive=True
    )
    output.seek(0)

    # Generar nombre
    filename = image_field.name.split('/')[-1]
    filename_without_ext = filename.rsplit('.', 1)[0]
    new_filename = f"{filename_without_ext}.jpg"

    return InMemoryUploadedFile(
        output,
        'ImageField',
        new_filename,
        'image/jpeg',
        sys.getsizeof(output),
        None
    )


class Service(models.Model):
    """Modelo para servicios ofrecidos."""
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre del servicio"
    )
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio (CLP)"
    )
    image = models.ImageField(
        upload_to='services/',
        verbose_name="Imagen"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Comprimir imagen antes de guardar"""
        if self.image:
            self.image = compress_image(
                self.image, max_width=1920, max_height=1080, quality=90)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Modelo para posts del blog/novedades."""
    title = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    content = models.TextField(verbose_name="Contenido")
    image = models.ImageField(
        upload_to='blog/',
        blank=False,
        null=False,
        verbose_name="Imagen"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Publicado"
    )
    published_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de publicación"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Post del blog"
        verbose_name_plural = "Posts del blog"
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def get_slug(self):
        """Genera slug SEO-friendly desde el título"""
        return slugify(self.title)

    def get_absolute_url(self):
        """URL canónica del post para SEO"""
        return reverse('index:novedad_detalle', kwargs={
            'pk': self.pk,
            'slug': self.get_slug()
        })

    def get_excerpt(self, length=150):
        """Extrae excerpt del contenido"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length].rsplit(' ', 1)[0] + '...'

    def get_reading_time(self):
        """Calcula tiempo de lectura en minutos (200 palabras/min)"""
        palabras = len(self.content.split())
        return max(1, round(palabras / 200))

    def save(self, *args, **kwargs):
        """Comprimir imagen antes de guardar"""
        if self.image:
            self.image = compress_image(
                self.image, max_width=1920, max_height=1080, quality=90)
        super().save(*args, **kwargs)


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

    def get_slug(self):
        """Genera slug SEO-friendly desde el nombre"""
        return slugify(self.name)

    def get_absolute_url(self):
        """URL canónica del instructor para SEO"""
        return reverse('index:instructor_detalle', kwargs={
            'pk': self.pk,
            'slug': self.get_slug()
        })

    def save(self, *args, **kwargs):
        """Comprimir foto antes de guardar"""
        if self.photo:
            self.photo = compress_image(
                self.photo, max_width=1200, max_height=1600, quality=90)
        super().save(*args, **kwargs)
