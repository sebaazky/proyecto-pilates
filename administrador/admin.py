"""
administrador/admin.py
Configuración del panel de administración de Django.
"""
from django.contrib import admin
from .models import Service, BlogPost, ContactMessage, Instructor


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    readonly_fields = ('created_at',)  # Solo created_at existe en Service


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_date', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-published_date', '-created_at')
    readonly_fields = ('created_at',)  # Solo created_at existe en BlogPost


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialties', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'specialties', 'bio')
    ordering = ('order', 'name')
    # Instructor SÍ tiene ambos campos
    readonly_fields = ('created_at', 'updated_at')
