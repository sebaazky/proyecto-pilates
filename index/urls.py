from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    # Landing principal
    path('', views.index, name='index'),

    # Contacto
    path('contacto/', views.contacto_publico, name='contacto_publico'),
    path('contacto/exito/', views.contacto_exito, name='contacto_exito'),

    # Páginas informativas
    path('nosotros/', views.nosotros, name='nosotros'),
    path('novedades/', views.novedades, name='novedades'),
]
