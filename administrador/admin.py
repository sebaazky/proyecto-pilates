from django.contrib import admin
from .models import Service, BlogPost, ContactMessage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Servicios
    """
    list_display = ['name', 'price', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']

    fieldsets = (
        ('Información del Servicio', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Configuración', {
            'fields': ('is_active', 'order')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Blog/Novedades
    """
    list_display = ['title', 'is_published', 'published_date', 'created_at']
    list_filter = ['is_published', 'published_date', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'content', 'image')
        }),
        ('Publicación', {
            'fields': ('is_published', 'published_date')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Mensajes de Contacto.
    Los mensajes NO se pueden eliminar para mantener historial.
    """
    list_display = ['name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Mensaje', {
            'fields': ('message',)
        }),
        ('Gestión', {
            'fields': ('status', 'admin_notes')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']

    def has_delete_permission(self, request, obj=None):
        """
        Deshabilita la opción de eliminar mensajes.
        Mantiene el historial completo de contactos.
        """
        return False

    def has_add_permission(self, request):
        """
        Deshabilita la creación manual de mensajes desde el admin.
        Los mensajes solo se crean desde el formulario público.
        """
        return False
