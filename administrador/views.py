"""
administrador/views.py
Panel CMS personalizado.

ROLES:
  superusuario (is_superuser=True) → accede al panel + gestiona usuarios
  administrador (rol='administrador') → accede al panel, SIN gestión de usuarios
"""
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from .models import Service, BlogPost, ContactMessage
from .forms import (ServiceForm, BlogPostForm,
                    ContactMessageForm, UsuarioCrearForm, UsuarioEditarForm)

User = get_user_model()


# ─────────────────────────────────────────────────────────────
# DECORADORES
# ─────────────────────────────────────────────────────────────

def solo_admin(view_func):
    """
    Permite acceso a superusuarios Y usuarios con rol='administrador'.
    No autenticado → login secreto.
    Autenticado sin permiso → inicio.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('login:login')
            return redirect(f'{login_url}?next={request.path}')

        if request.user.is_superuser or getattr(request.user, 'rol', '') == 'administrador':
            return view_func(request, *args, **kwargs)

        messages.error(
            request, 'No tienes permiso para acceder a esta sección.')
        return redirect('index:index')

    return wrapper


def solo_superadmin(view_func):
    """
    Solo superusuarios pueden acceder (gestión de usuarios).
    Un administrador normal que intente entrar → redirige al dashboard con error.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('login:login')
            return redirect(f'{login_url}?next={request.path}')

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        messages.error(
            request, 'Esta sección es exclusiva del superadministrador.')
        return redirect('administrador:home')

    return wrapper


# ─────────────────────────────────────────────────────────────
# CONTEXTO GLOBAL (sidebar)
# ─────────────────────────────────────────────────────────────

def get_sidebar_context():
    return {
        'mensajes_nuevos': ContactMessage.objects.filter(status='new').count()
    }


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────

@solo_admin
def home(request):
    context = {
        'total_servicios':     Service.objects.count(),
        'servicios_activos':   Service.objects.filter(is_active=True).count(),
        'total_posts':         BlogPost.objects.count(),
        'posts_publicados':    BlogPost.objects.filter(is_published=True).count(),
        'total_mensajes':      ContactMessage.objects.count(),
        'mensajes_nuevos':     ContactMessage.objects.filter(status='new').count(),
        'mensajes_recientes':  ContactMessage.objects.order_by('-created_at')[:5],
        'servicios_recientes': Service.objects.order_by('-created_at')[:3],
        'posts_recientes':     BlogPost.objects.order_by('-published_date')[:3],
        # Para el sidebar
        'total_admins': User.objects.filter(rol='administrador').count(),
    }
    return render(request, 'administrador/admin_home.html', context)


# ─────────────────────────────────────────────────────────────
# SERVICIOS
# ─────────────────────────────────────────────────────────────

@solo_admin
def servicios_list(request):
    q = request.GET.get('q', '').strip()
    servicios = Service.objects.all()
    if q:
        servicios = servicios.filter(
            Q(name__icontains=q) | Q(description__icontains=q))
    return render(request, 'administrador/servicios/list.html', {
        'servicios': servicios, 'q': q, **get_sidebar_context()
    })


@solo_admin
def servicio_crear(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servicio creado correctamente.')
            return redirect('administrador:servicios_list')
    else:
        form = ServiceForm()
    return render(request, 'administrador/servicios/form.html', {
        'form': form, 'titulo': 'Crear Servicio',
        'accion': 'Crear', **get_sidebar_context()
    })


@solo_admin
def servicio_editar(request, pk):
    servicio = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servicio actualizado correctamente.')
            return redirect('administrador:servicios_list')
    else:
        form = ServiceForm(instance=servicio)
    return render(request, 'administrador/servicios/form.html', {
        'form': form, 'servicio': servicio,
        'titulo': 'Editar Servicio', 'accion': 'Guardar cambios',
        **get_sidebar_context()
    })


@solo_admin
def servicio_eliminar(request, pk):
    servicio = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        nombre = servicio.name
        servicio.delete()
        messages.success(request, f'🗑️ Servicio "{nombre}" eliminado.')
        return redirect('administrador:servicios_list')
    return render(request, 'administrador/servicios/confirmar_eliminar.html', {
        'servicio': servicio, **get_sidebar_context()
    })


@solo_admin
def servicio_toggle_activo(request, pk):
    servicio = get_object_or_404(Service, pk=pk)
    servicio.is_active = not servicio.is_active
    servicio.save()
    estado = 'activado' if servicio.is_active else 'desactivado'
    messages.success(request, f'✅ Servicio "{servicio.name}" {estado}.')
    return redirect('administrador:servicios_list')


# ─────────────────────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────────────────────

@solo_admin
def blog_list(request):
    q = request.GET.get('q', '').strip()
    posts = BlogPost.objects.all()
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'administrador/blog/list.html', {
        'posts': posts, 'q': q, **get_sidebar_context()
    })


@solo_admin
def blog_crear(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Publicación creada correctamente.')
            return redirect('administrador:blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'administrador/blog/form.html', {
        'form': form, 'titulo': 'Nueva Publicación',
        'accion': 'Publicar', **get_sidebar_context()
    })


@solo_admin
def blog_editar(request, pk):
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
    return render(request, 'administrador/blog/form.html', {
        'form': form, 'post': post,
        'titulo': 'Editar Publicación', 'accion': 'Guardar cambios',
        **get_sidebar_context()
    })


@solo_admin
def blog_eliminar(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        titulo = post.title
        post.delete()
        messages.success(request, f'🗑️ Publicación "{titulo}" eliminada.')
        return redirect('administrador:blog_list')
    return render(request, 'administrador/blog/confirmar_eliminar.html', {
        'post': post, **get_sidebar_context()
    })


@solo_admin
def blog_toggle_publicado(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save()
    estado = 'publicado' if post.is_published else 'despublicado'
    messages.success(request, f'✅ "{post.title}" {estado}.')
    return redirect('administrador:blog_list')


# ─────────────────────────────────────────────────────────────
# MENSAJES
# ─────────────────────────────────────────────────────────────

@solo_admin
def mensajes_list(request):
    estado = request.GET.get('estado', '')
    mensajes = ContactMessage.objects.all()
    if estado:
        mensajes = mensajes.filter(status=estado)
    return render(request, 'administrador/contacto/list.html', {
        'mensajes': mensajes,
        'estado_filtro': estado,
        'status_choices': ContactMessage.STATUS_CHOICES,
        **get_sidebar_context()
    })


@solo_admin
def mensaje_detalle(request, pk):
    mensaje = get_object_or_404(ContactMessage, pk=pk)
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
    return render(request, 'administrador/contacto/detalle.html', {
        'mensaje': mensaje, 'form': form, **get_sidebar_context()
    })


# ─────────────────────────────────────────────────────────────
# USUARIOS — solo superadmin
# ─────────────────────────────────────────────────────────────

@solo_superadmin
def usuarios_list(request):
    """Lista todos los usuarios administradores."""
    usuarios = User.objects.filter(
        rol='administrador', is_superuser=False
    ).order_by('username')
    return render(request, 'administrador/usuarios/list.html', {
        'usuarios': usuarios,
        **get_sidebar_context()
    })


@solo_superadmin
def usuario_crear(request):
    """Crea un nuevo usuario administrador con contraseña hasheada."""
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f'✅ Usuario "{user.username}" creado correctamente.')
            return redirect('administrador:usuarios_list')
    else:
        form = UsuarioCrearForm()
    return render(request, 'administrador/usuarios/form.html', {
        'form': form,
        'titulo': 'Crear Usuario Administrador',
        'accion': 'Crear usuario',
        **get_sidebar_context()
    })


@solo_superadmin
def usuario_editar(request, pk):
    """Edita un usuario existente. Contraseña opcional."""
    usuario = get_object_or_404(User, pk=pk, is_superuser=False)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'✅ Usuario "{usuario.username}" actualizado.')
            return redirect('administrador:usuarios_list')
    else:
        form = UsuarioEditarForm(instance=usuario)
    return render(request, 'administrador/usuarios/form.html', {
        'form': form,
        'usuario': usuario,
        'titulo': f'Editar — {usuario.username}',
        'accion': 'Guardar cambios',
        **get_sidebar_context()
    })


@solo_superadmin
def usuario_eliminar(request, pk):
    """Elimina un usuario con confirmación. No puede eliminarse a sí mismo."""
    usuario = get_object_or_404(User, pk=pk, is_superuser=False)

    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('administrador:usuarios_list')

    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'🗑️ Usuario "{username}" eliminado.')
        return redirect('administrador:usuarios_list')

    return render(request, 'administrador/usuarios/confirmar_eliminar.html', {
        'usuario': usuario,
        **get_sidebar_context()
    })
