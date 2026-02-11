"""
administrador/views.py
Panel CMS personalizado para el cliente administrador.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Service, BlogPost, ContactMessage
from .forms import ServiceForm, BlogPostForm, ContactMessageForm


def solo_admin(view_func):
    """Decorador: solo usuarios con rol administrador pueden acceder."""
    @login_required(login_url='login:login')
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or getattr(request.user, 'rol', '') == 'administrador'):
            messages.error(
                request, 'No tienes permiso para acceder a esta sección.')
            return redirect('index:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_sidebar_context():
    """Contexto global para el sidebar (badge de mensajes nuevos)."""
    return {
        'mensajes_nuevos': ContactMessage.objects.filter(status='new').count()
    }


# ─────────────────────────────────────────────
# DASHBOARD / HOME
# ─────────────────────────────────────────────

@solo_admin
def home(request):
    """Vista principal del panel de administración."""
    context = {
        'total_servicios': Service.objects.count(),
        'servicios_activos': Service.objects.filter(is_active=True).count(),
        'total_posts': BlogPost.objects.count(),
        'posts_publicados': BlogPost.objects.filter(is_published=True).count(),
        'total_mensajes': ContactMessage.objects.count(),
        'mensajes_nuevos': ContactMessage.objects.filter(status='new').count(),
        'mensajes_recientes': ContactMessage.objects.order_by('-created_at')[:5],
        'servicios_recientes': Service.objects.order_by('-created_at')[:3],
        'posts_recientes': BlogPost.objects.order_by('-published_date')[:3],
    }
    return render(request, 'administrador/admin_home.html', context)


# ─────────────────────────────────────────────
# SERVICIOS
# ─────────────────────────────────────────────

@solo_admin
def servicios_list(request):
    """Lista todos los servicios con búsqueda."""
    q = request.GET.get('q', '').strip()
    servicios = Service.objects.all()
    if q:
        servicios = servicios.filter(
            Q(name__icontains=q) | Q(description__icontains=q))
    context = {
        'servicios': servicios,
        'q': q,
        **get_sidebar_context()
    }
    return render(request, 'administrador/servicios/list.html', context)


@solo_admin
def servicio_crear(request):
    """Crea un nuevo servicio."""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servicio creado correctamente.')
            return redirect('administrador:servicios_list')
    else:
        form = ServiceForm()
    context = {'form': form, 'titulo': 'Crear Servicio',
               'accion': 'Crear', **get_sidebar_context()}
    return render(request, 'administrador/servicios/form.html', context)


@solo_admin
def servicio_editar(request, pk):
    """Edita un servicio existente."""
    servicio = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servicio actualizado correctamente.')
            return redirect('administrador:servicios_list')
    else:
        form = ServiceForm(instance=servicio)
    context = {'form': form, 'servicio': servicio, 'titulo': 'Editar Servicio',
               'accion': 'Guardar cambios', **get_sidebar_context()}
    return render(request, 'administrador/servicios/form.html', context)


@solo_admin
def servicio_eliminar(request, pk):
    """Elimina un servicio con confirmación."""
    servicio = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        nombre = servicio.name
        servicio.delete()
        messages.success(
            request, f'🗑️ Servicio "{nombre}" eliminado correctamente.')
        return redirect('administrador:servicios_list')
    context = {'servicio': servicio, **get_sidebar_context()}
    return render(request, 'administrador/servicios/confirmar_eliminar.html', context)


@solo_admin
def servicio_toggle_activo(request, pk):
    """Activa o desactiva un servicio rápidamente."""
    servicio = get_object_or_404(Service, pk=pk)
    servicio.is_active = not servicio.is_active
    servicio.save()
    estado = 'activado' if servicio.is_active else 'desactivado'
    messages.success(request, f'✅ Servicio "{servicio.name}" {estado}.')
    return redirect('administrador:servicios_list')


# ─────────────────────────────────────────────
# BLOG / NOVEDADES
# ─────────────────────────────────────────────

@solo_admin
def blog_list(request):
    """Lista todas las publicaciones con búsqueda."""
    q = request.GET.get('q', '').strip()
    posts = BlogPost.objects.all()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    context = {
        'posts': posts,
        'q': q,
        **get_sidebar_context()
    }
    return render(request, 'administrador/blog/list.html', context)


@solo_admin
def blog_crear(request):
    """Crea una nueva publicación."""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Publicación creada correctamente.')
            return redirect('administrador:blog_list')
    else:
        form = BlogPostForm()
    context = {'form': form, 'titulo': 'Nueva Publicación',
               'accion': 'Publicar', **get_sidebar_context()}
    return render(request, 'administrador/blog/form.html', context)


@solo_admin
def blog_editar(request, pk):
    """Edita una publicación existente."""
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(
                request, '✅ Publicación actualizada correctamente.')
            return redirect('administrador:blog_list')
    else:
        form = BlogPostForm(instance=post)
    context = {'form': form, 'post': post, 'titulo': 'Editar Publicación',
               'accion': 'Guardar cambios', **get_sidebar_context()}
    return render(request, 'administrador/blog/form.html', context)


@solo_admin
def blog_eliminar(request, pk):
    """Elimina una publicación con confirmación."""
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        titulo = post.title
        post.delete()
        messages.success(
            request, f'🗑️ Publicación "{titulo}" eliminada correctamente.')
        return redirect('administrador:blog_list')
    context = {'post': post, **get_sidebar_context()}
    return render(request, 'administrador/blog/confirmar_eliminar.html', context)


@solo_admin
def blog_toggle_publicado(request, pk):
    """Publica o despublica un post rápidamente."""
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save()
    estado = 'publicado' if post.is_published else 'despublicado'
    messages.success(request, f'✅ "{post.title}" {estado}.')
    return redirect('administrador:blog_list')


# ─────────────────────────────────────────────
# MENSAJES DE CONTACTO
# ─────────────────────────────────────────────

@solo_admin
def mensajes_list(request):
    """Lista mensajes de contacto con filtro por estado."""
    estado = request.GET.get('estado', '')
    mensajes = ContactMessage.objects.all()
    if estado:
        mensajes = mensajes.filter(status=estado)
    context = {
        'mensajes': mensajes,
        'estado_filtro': estado,
        'status_choices': ContactMessage.STATUS_CHOICES,
        **get_sidebar_context()
    }
    return render(request, 'administrador/contacto/list.html', context)


@solo_admin
def mensaje_detalle(request, pk):
    """Ver detalle de un mensaje y cambiar estado/notas."""
    mensaje = get_object_or_404(ContactMessage, pk=pk)
    # Marcar como leído automáticamente si está nuevo
    if mensaje.status == 'new':
        mensaje.status = 'read'
        mensaje.save()
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, instance=mensaje)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mensaje actualizado correctamente.')
            return redirect('administrador:mensajes_list')
    else:
        form = ContactMessageForm(instance=mensaje)
    context = {'mensaje': mensaje, 'form': form, **get_sidebar_context()}
    return render(request, 'administrador/contacto/detalle.html', context)
