"""
login/views.py

ARQUITECTURA:
  - Superusuario (tú/dev)  → accede por /admin/ de Django únicamente
  - Administrador (cliente) → accede por /login/pr-gestion-k7x/
                               cuenta creada por el dev desde /admin/
                               con rol = 'administrador'

El login secreto SOLO acepta usuarios con rol == 'administrador'.
Los superusuarios NO pueden entrar por aquí (son cuentas técnicas).
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache


@never_cache
@require_http_methods(["GET", "POST"])
def login_admin(request):
    """Acceso privado exclusivo para usuarios con rol = 'administrador'."""

    # Ya está logueado como administrador → directo al panel
    if request.user.is_authenticated:
        if _es_admin(request.user):
            return redirect('administrador:home')
        # Logueado pero sin rol admin (ej: superusuario perdido aquí)
        logout(request)
        return render(request, 'login/login_admin.html', {
            'error': 'Esta área es exclusiva para administradores del sistema.'
        })

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'login/login_admin.html', {
                'error': 'Completa todos los campos.',
                'username': username,
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if _es_admin(user):
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('administrador:home')
            else:
                # Credenciales válidas pero no tiene rol administrador
                # (puede ser el superusuario dev intentando entrar aquí)
                return render(request, 'login/login_admin.html', {
                    'error': 'Esta cuenta no tiene acceso al panel de administración.',
                    'username': username,
                })
        else:
            return render(request, 'login/login_admin.html', {
                'error': 'Usuario o contraseña incorrectos.',
                'username': username,
            })

    return render(request, 'login/login_admin.html', {
        'next': request.GET.get('next', ''),
    })


@never_cache
def logout_admin(request):
    """Cierra sesión y vuelve al login privado."""
    logout(request)
    return redirect('login:login')


# ── Helper ────────────────────────────────────────────────────
def _es_admin(user):
    """
    Devuelve True SOLO si el usuario tiene rol = 'administrador'.
    Los superusuarios (dev/técnicos) NO tienen acceso por aquí.
    """
    if not user or not user.is_active:
        return False
    return getattr(user, 'rol', None) == 'administrador'
