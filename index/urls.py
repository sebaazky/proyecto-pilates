"""
index/urls.py — URLs públicas de la landing page.

  /                       → index
  /nosotros/              → nosotros
  /novedades/             → novedades
  /servicios/             → servicios (lista)
  /servicios/<pk>/        → servicio_detalle
  /contacto/              → contacto_publico
  /contacto/exito/        → contacto_exito
"""
from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('',                        views.index,            name='index'),
    path('nosotros/',               views.nosotros,         name='nosotros'),
    path('novedades/',              views.novedades,        name='novedades'),
    path('servicios/',              views.servicios,        name='servicios'),
    path('servicios/<int:pk>/',     views.servicio_detalle, name='servicio_detalle'),
    path('contacto/',               views.contacto_publico, name='contacto_publico'),
    path('contacto/exito/',         views.contacto_exito,   name='contacto_exito'),
]
