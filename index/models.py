# index/models.py
from django.conf import settings
from django.db import models
from administrador.models import ClasePilates  # <-- importamos la clase admin
from django.utils.text import slugify


class Reserva(models.Model):
    CLASES = [
        ("reformer", "Reformer"),
        ("mat", "Mat"),
        ("grupal", "Grupal"),
    ]
    ESTADOS = [
        ("Confirmada", "Confirmada"),
        ("Pendiente", "Pendiente"),
        ("Cancelada", "Cancelada"),
        ("Completada", "Completada"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas_index",
        related_query_name="reserva_index",
    )

    # --- NUEVO: vínculo (opcional por compatibilidad) ---
    clase = models.ForeignKey(
        ClasePilates,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservas_index",
    )

    # Campos existentes (se mantendrán para compatibilidad / reportes)
    tipo = models.CharField(max_length=20, choices=CLASES)
    fecha = models.DateField()
    inicio = models.TimeField()
    fin = models.TimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=12, choices=ESTADOS, default="Confirmada")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-inicio"]
        # Evita doble reserva del mismo usuario a misma clase
        constraints = [
            models.UniqueConstraint(
                fields=["user", "clase"], name="uniq_reserva_usuario_misma_clase"
            )
        ]

    def __str__(self):
        base = f"{self.user} - {self.tipo} - {self.fecha} {self.inicio}"
        if self.clase_id:
            base += f" (Clase: {self.clase.nombre_clase})"
        return base

    # --- Helpers de cupos ---
    @staticmethod
    def cupos_tomados(clase: ClasePilates) -> int:
        return Reserva.objects.filter(clase=clase).exclude(estado="Cancelada").count()

    @staticmethod
    def hay_cupo(clase: ClasePilates) -> bool:
        return Reserva.cupos_tomados(clase) < clase.capacidad_maxima

    from django.db import models


class Contacto(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True, null=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    # 👇 NUEVO: estado y comentario interno para el CRM
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("revisado", "Revisado"),
        ("respondido", "Respondido"),
    ]
    estado_mensaje = models.CharField(
        max_length=12, choices=ESTADOS, default="pendiente"
    )
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"


class NewsPost(models.Model):
    TAGS = [
        ("Consejos", "Consejo"),
        ("Eventos",  "Evento"),
        ("Promos",   "Promo"),
        ("MK",       "MK · Historia"),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    tag = models.CharField(max_length=16, choices=TAGS, default="Consejos")
    excerpt = models.TextField(max_length=300, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:170]
            slug = base
            i = 2
            while NewsPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"[:180]
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)
