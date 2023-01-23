from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import *
from appFamiliares.models import Avatar
# from appFamiliares.views import obtenerAvatar
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormMixin
from .forms import FormMensajes
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user.id)
    if len(lista)!=0:
        avatar=lista[0].imagen.url
        print(avatar)
    else:
        avatar="/media/avatars/default.png"
    return avatar

@login_required
def buscarUsuario(request):
        username = request.GET["username"]
        usuario= User.objects.filter(username=username)
        if len(usuario)!=0:
            return render(request, "App2/resultadosBusquedaUsuarios.html", {"usuario":usuario, "avatar": obtenerAvatar(request)})
        else:
            messages.error(request, "No existe usuario con ese nombre")
            return render(request, "App2/inbox.html", {"avatar": obtenerAvatar(request)})

@login_required
def leerUsuarios(request):
    usuarios=User.objects.all()
    return render(request, "App2/leerUsuarios.html", {"usuarios":usuarios, "avatar": obtenerAvatar(request)})

class Inbox(View):
    def get(self,request):
        inbox = Canal.objects.filter(canalusuario__usuario__in=[request.user.id])

        return render(request, "App2/inbox.html", {"inbox": inbox, "avatar": obtenerAvatar(request)})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class CanalFormMixin(FormMixin):
    form_class =FormMensajes

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        form = self.get_form()
        if form.is_valid():
            canal = self.get_object()
            usuario = self.request.user
            mensaje = form.cleaned_data.get("mensaje")
            canal_obj = CanalMensaje.objects.create(canal=canal, usuario=usuario, texto=mensaje)

            if is_ajax(request=request):
                return JsonResponse({

                    "mensaje": canal_obj.texto,
                    'username': canal_obj.usuario.username

                    }, status=201)

            return super().form_valid(form)

        else:

            if is_ajax(request=request):
                return JsonResponse({"ERROR":form.errors}, status=400)

            return super().form_invalid(form)

class CanalDetailView(LoginRequiredMixin,CanalFormMixin,  DetailView):
    template_name = 'App2/canal_detail.html'
    queryset = Canal.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        print(obj)

        context['si_canal_mienbro'] = self.request.user in obj.usuarios.all()
        return context

class DetailMs(LoginRequiredMixin, CanalFormMixin, DetailView):
    template_name= 'App2/canal_detail.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        mi_username = self.request.user.username
        canal, _ = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

        if username == mi_username:
            mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)
            return mi_canal

        if canal == None:
            raise Http404
        else:
            return canal

def mensajes_privados(request,username,*args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse("No estas logueado")

    mi_username = request.user.username

    canal, created = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

    if created:
        print("Canal Creado")
    Usuarios_Canal = canal.canalusuario_set.all().values("usuario__username")
    print(Usuarios_Canal)
    mensaje_canal = canal.canalmensaje_set.all()
    print(mensaje_canal.values("texto"))

    return HttpResponse(f"Nuestro Canal - {canal.id}")


