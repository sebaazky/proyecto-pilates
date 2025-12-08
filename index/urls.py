# index/urls.py
from django.urls import path
from . import views
from .views_chat import chat_api
from . import panel_news_views as pnl

app_name = "index"

urlpatterns = [
    # Landing
    path("", views.index, name="index"),

    # Página de Clases (la que extiende base_index y muestra tabs)
    path("clases/", views.clases, name="clases"),

    # Contacto público (form y confirmación)
    path("contacto/", views.contacto_publico, name="contacto_publico"),
    path("contacto/exito/", views.contacto_exito, name="contacto_exito"),

    # Catálogo de clases en tarjetas
    path("clases/disponibles/", views.clases_disponibles_cards,
         name="clases_disponibles_cards"),

    # Catálogo en grid
    path("catalogo/", views.clases_grid, name="clases_grid"),
    path("api/chat/", chat_api, name="chat_api"),
    path("faqs/", views.faqs, name="faqs"),
    path("novedades/", views.novedades, name="novedades"),
    path("panel/novedades/",                    pnl.news_list,
         name="panel_news_list"),
    path("panel/novedades/nuevo/",
         pnl.news_create,         name="panel_news_new"),
    path("panel/novedades/<int:pk>/editar/",
         pnl.news_edit,           name="panel_news_edit"),
    path("panel/novedades/<int:pk>/eliminar/",
         pnl.news_delete,         name="panel_news_del"),
    path("panel/novedades/<int:pk>/publicar/",
         pnl.news_toggle_publish, name="panel_news_pub"),
    path("panel/novedades/<int:pk>/destacar/",
         pnl.news_toggle_featured, name="panel_news_feat"),
    path("nosotros/", views.nosotros, name="nosotros"),

]
