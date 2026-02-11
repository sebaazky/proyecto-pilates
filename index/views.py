"""
index/views.py
Vistas simplificadas para la landing page del proyecto PilatesReserva.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from administrador.models import Service, BlogPost, ContactMessage


def index(request):
    """
    Vista principal de la landing page.
    Muestra servicios activos y últimas publicaciones del blog.
    """
    # Obtener servicios activos ordenados
    services = Service.objects.filter(is_active=True).order_by('order', 'name')

    # Obtener últimas 3 publicaciones
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]

    context = {
        'services': services,
        'blog_posts': blog_posts,
    }

    return render(request, 'index/index.html', context)


def contacto_publico(request):
    """
    Procesa el formulario de contacto de la landing page.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        # Validación básica
        if not name or not email or not message:
            messages.error(
                request, 'Por favor completa todos los campos obligatorios.')
            return redirect('index:index')

        # Crear mensaje de contacto
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            status='new'
        )

        messages.success(
            request,
            '¡Gracias por contactarnos! Te responderemos pronto.'
        )
        return redirect('index:contacto_exito')

    # Si no es POST, mostrar página de contacto
    return render(request, 'index/contacto.html')


def contacto_exito(request):
    """
    Página de confirmación después de enviar el formulario de contacto.
    """
    return render(request, 'index/contacto_exito.html')


def nosotros(request):
    """
    Página "Sobre Nosotros" / "Quiénes Somos"
    """
    return render(request, 'index/nosotros.html')


def novedades(request):
    """
    Listado público de novedades/blog.
    """
    # Obtener todas las publicaciones publicadas
    posts = BlogPost.objects.filter(
        is_published=True).order_by('-published_date')

    context = {
        'posts': posts,
    }

    return render(request, 'index/novedades.html', context)
