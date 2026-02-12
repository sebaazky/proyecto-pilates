"""
login/urls.py

URL privada del administrador — no enlazada en ningún template público.
El prefijo 'login/' viene de Pilatesreserva/urls.py y se mantiene
para no levantar sospechas. La ruta real queda:

  /login/pr-gestion-k7x/          → formulario de acceso
  /login/pr-gestion-k7x/salir/    → cierre de sesión

Nadie debería llegar aquí salvo el administrador que conoce la URL.
"""
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('pr-gestion-k7x/',        views.login_admin,  name='login'),
    path('pr-gestion-k7x/salir/',  views.logout_admin, name='logout'),
]
