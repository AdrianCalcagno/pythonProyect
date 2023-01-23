from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('integrantes/', integrantes, name="integrantes"),
    path('contacto/', contacto, name="contacto"),
    path('inicio/', inicio, name="inicio"),
    path('', inicio, name="inicio"),
    path('appFamiliares/', inicio, name="inicio"),
    path('busquedaMensajes/', busquedaMensajes, name="busquedaMensajes"),
    path("buscar/", buscar, name="buscar"),
    path("aboutme/", aboutme, name="aboutme"),
    path("leerMensajes/", leerMensajes, name="leerMensajes"),
    path("eliminarMensaje/<id>", eliminarMensaje, name="eliminarMensaje"),
    path("editarMensaje/<id>", editarMensaje, name="editarMensaje"),
    path("mensajeFormulario/", contacto, name="mensajeFormulario"),
    path("register/", register, name="register"),
    path("login/", login_request, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('editarPerfil/', editarPerfil, name='editarPerfil'),
    path('agregarAvatar/', agregarAvatar, name='agregarAvatar'),
    path('suscribirse/', suscribirse, name='suscribirse'),

]