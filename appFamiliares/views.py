from django.shortcuts import render
from .models import Mensajes, Avatar, Newsletter
from appFamiliares.forms import MensajesForm, RegistroUsuarioForm, UserEditForm, AvatarForm, NewsletterForm, EditMensajeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user.id)
    if len(lista)!=0:
        avatar=lista[0].imagen.url
    else:
        avatar="/media/avatars/default.png"
    return avatar

#Vistas

def inicio(request):
    return render (request, "appFamiliares/padre.html",{"avatar": obtenerAvatar(request)})

def integrantes(request):
    return render (request, "appFamiliares/integrantes.html", {"avatar": obtenerAvatar(request)})

def aboutme(request):
    return render (request, "appFamiliares/aboutme.html", {"avatar": obtenerAvatar(request)})

@login_required
def contacto(request):
    if request.method == "POST":
        forms = MensajesForm(request.POST)
        if forms.is_valid():
            informacion = forms.cleaned_data
            nombre = informacion["nombre"]
            email = informacion["email"]
            asunto = informacion["asunto"]
            mensaje = informacion["mensaje"]
            final = Mensajes(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje)
            final.save()
            messages.success(request, "¡Mensaje enviado con éxito!")
            return render (request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Algo falló, revisá la información por favor")
            return render (request, "appFamiliares/contacto.html", {"forms":forms, "avatar": obtenerAvatar(request)})
    else:
        formulario = MensajesForm()
        return render (request, "appFamiliares/contacto.html", {"forms":formulario, "avatar": obtenerAvatar(request)})

def suscribirse(request):
    if request.method == "POST":
        forms = NewsletterForm(request.POST)
        if forms.is_valid():
            informacion = forms.cleaned_data
            email = informacion["email"]
            final = Newsletter(email=email)
            final.save()
            messages.success(request, "¡Te suscribiste con éxito!")
            return render (request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Algo falló")
            return render (request, "appFamiliares/padre.html", {"forms":forms, "avatar": obtenerAvatar(request)})
    else:
        formulario = NewsletterForm()
        return render (request, "appFamiliares/padre.html", {"forms":formulario, "avatar": obtenerAvatar(request)})

@login_required
def busquedaMensajes(request):
    return render (request, "appFamiliares/busquedaMensajes.html", {"avatar": obtenerAvatar(request)})

@login_required
def buscar(request):
        nombre = request.GET["username"]
        mensajes= Mensajes.objects.filter(nombre=nombre)
        if len(mensajes)!=0:
            return render(request, "appFamiliares/resultadosBusqueda.html", {"mensajes":mensajes, "avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "No existen mensajes con ese nombre de usuario")
            return render(request, "appFamiliares/busquedaMensajes.html", {"avatar": obtenerAvatar(request)})

@login_required
def leerMensajes(request):
    mensajes=Mensajes.objects.all()
    return render(request, "appFamiliares/leerMensajes.html", {"mensajes":mensajes, "avatar": obtenerAvatar(request)})

@login_required
def eliminarMensaje(request, id):
    mensaje=Mensajes.objects.get(id=id)
    mensaje.delete()
    mensajes=Mensajes.objects.all()
    messages.success(request, "¡Mensaje eliminado con éxito!")
    return render(request, "appFamiliares/leerMensajes.html", {"mensajes":mensajes, "avatar": obtenerAvatar(request)})

@login_required

def editarMensaje(request, id):
    mensaje=Mensajes.objects.get(id=id)
    if request.method=="POST":
        form=MensajesForm(request.POST)
        print(form)
        if form.is_valid():
            informacion=form.cleaned_data
            mensaje.mensaje=informacion["mensaje"]
            mensaje.asunto=informacion["asunto"]
            mensaje.save()
            mensajes=Mensajes.objects.all()
            messages.success(request, "¡Mensaje editado correctamente!")
            return render(request, "appFamiliares/leerMensajes.html", {"mensajes":mensajes, "avatar": obtenerAvatar(request)})
        pass
    else:
        formulario= MensajesForm(initial={"asunto":mensaje.asunto, "mensaje":mensaje.mensaje, "avatar": obtenerAvatar(request)})
        return render(request, "appFamiliares/editarMensaje.html", {"form":formulario, "mensaje":mensaje, "avatar": obtenerAvatar(request)})


def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Usuario creado con éxito!")
            return render(request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Error al crear el usuario")
            return render(request, "appFamiliares/register.html", {"form": form, "avatar": obtenerAvatar(request)})
    else:
        form= RegistroUsuarioForm()
        return render(request, "appFamiliares/register.html", {"form": form, "avatar": obtenerAvatar(request)})

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, "¡Hola, hemos podido loguearte!")
                return render(request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
                return render(request, "appFamiliares/login.html", {"form": form, "avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return render(request, "appFamiliares/login.html", {"form": form, "avatar": obtenerAvatar(request)})
    else:
        form=AuthenticationForm()
        return render(request, "appFamiliares/login.html", {"form": form, "avatar": obtenerAvatar(request)})

@login_required
def editarPerfil(request):
    usuario=request.user

    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.save()
            messages.success(request, "¡Usuario editado correctamente!")
            return render(request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Error al editar el usuario")
            return render(request, "appFamiliares/editarPerfil.html", {"form": form, "nombreusuario":usuario.username, "avatar": obtenerAvatar(request)})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "appFamiliares/editarPerfil.html", {"form": form, "nombreusuario":usuario.username, "avatar": obtenerAvatar(request)})

@login_required
def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            messages.success(request, "¡Avatar agregado correctamente!")
            return render(request, "appFamiliares/padre.html", {"avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "Error al agregar el avatar")
            return render(request, "appFamiliares/agregarAvatar.html", {"form": form, "usuario": request.user, "avatar": obtenerAvatar(request)})
    else:
        form=AvatarForm()
        return render(request, "appFamiliares/agregarAvatar.html", {"form": form, "usuario": request.user, "avatar": obtenerAvatar(request)})
