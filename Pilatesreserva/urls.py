"""
Pilatesreserva/urls.py
URLs principales del proyecto.

Rutas públicas:
  /                    → landing page (index)
  /nosotros/
  /novedades/
  /servicios/
  /contacto/

Rutas privadas (no enlazadas en ningún lugar público):
  /login/pr-gestion-k7x/          → acceso administrador
  /login/pr-gestion-k7x/salir/    → logout

Panel CMS:
  /administrador/      → panel del administrador (requiere login + rol)

Django Admin (soporte técnico):
  /admin/              → Django admin nativo
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin (soporte técnico)
    path('admin/', admin.site.urls),

    # Landing pública
    path('', include('index.urls')),

    # Login privado — /login/ existe pero la subruta no es obvia
    path('login/', include('login.urls')),

    # Panel CMS del administrador
    path('administrador/', include('administrador.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
