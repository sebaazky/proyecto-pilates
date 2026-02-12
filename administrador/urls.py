"""
administrador/urls.py
URLs del panel CMS.
"""
from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [

    # ── Dashboard ──────────────────────────────────────────
    path('', views.home, name='home'),

    # ── Servicios ──────────────────────────────────────────
    path('servicios/',                   views.servicios_list,
         name='servicios_list'),
    path('servicios/crear/',             views.servicio_crear,
         name='servicio_crear'),
    path('servicios/<int:pk>/editar/',
         views.servicio_editar,       name='servicio_editar'),
    path('servicios/<int:pk>/eliminar/',
         views.servicio_eliminar,     name='servicio_eliminar'),
    path('servicios/<int:pk>/toggle/',
         views.servicio_toggle_activo, name='servicio_toggle'),

    # ── Blog / Novedades ───────────────────────────────────
    path('blog/',                    views.blog_list,            name='blog_list'),
    path('blog/crear/',              views.blog_crear,           name='blog_crear'),
    path('blog/<int:pk>/editar/',    views.blog_editar,          name='blog_editar'),
    path('blog/<int:pk>/eliminar/',
         views.blog_eliminar,        name='blog_eliminar'),
    path('blog/<int:pk>/toggle/',
         views.blog_toggle_publicado, name='blog_toggle'),

    # ── Mensajes de Contacto ───────────────────────────────
    path('mensajes/',            views.mensajes_list,    name='mensajes_list'),
    path('mensajes/<int:pk>/',   views.mensaje_detalle,  name='mensaje_detalle'),

    # ── Usuarios (solo superadmin) ─────────────────────────
    path('usuarios/',                    views.usuarios_list,
         name='usuarios_list'),
    path('usuarios/crear/',
         views.usuario_crear,    name='usuario_crear'),
    path('usuarios/<int:pk>/editar/',
         views.usuario_editar,   name='usuario_editar'),
    path('usuarios/<int:pk>/eliminar/',
         views.usuario_eliminar, name='usuario_eliminar'),
]
