"""
index/urls.py — URLs públicas de la landing page.

  /                       → index
  /nosotros/              → nosotros
  /novedades/             → novedades
  /servicios/             → servicios (lista)
  /servicios/<pk>/        → servicio_detalle
  /contacto/              → contacto_publico
  /contacto/exito/        → contacto_exito
  /api/chat/              → chat_api (chatbot)
"""
from django.urls import path
from . import views
from .chatbot_views import chat_api

app_name = 'index'

urlpatterns = [
    path('',                        views.index,            name='index'),
    path('nosotros/',               views.nosotros,         name='nosotros'),
    path('nosotros/<int:pk>/<slug:slug>/',
         views.instructor_detalle, name='instructor_detalle'),
    path('novedades/',              views.novedades,        name='novedades'),
    path('novedades/<int:pk>/<slug:slug>/',
         views.novedad_detalle, name='novedad_detalle'),
    path('servicios/',              views.servicios,        name='servicios'),
    path('servicios/<int:pk>/',     views.servicio_detalle, name='servicio_detalle'),
    path('contacto/',               views.contacto_publico, name='contacto_publico'),
    path('contacto/exito/',         views.contacto_exito,   name='contacto_exito'),

    # Chatbot API
    path('api/chat/',               chat_api,               name='chat_api'),
]
