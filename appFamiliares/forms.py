from django import forms
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User

class EditMensajeForm(forms.Form):
    asunto = forms.CharField(label="Asunto", max_length=200)
    mensaje = forms.CharField(label="Mensaje", max_length=200)
class MensajesForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50)
    email = forms.EmailField(label="Email", max_length=50)
    asunto = forms.CharField(label="Asunto", max_length=200)
    mensaje = forms.CharField(label="Mensaje", max_length=200)

class NewsletterForm(forms.Form):
    email = forms.EmailField(label="email")


class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email= forms.EmailField(label="Email")
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username","first_name", "last_name", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}



class UserEditForm(UserCreationForm):
    first_name=forms.CharField(label='Modificar Nombre')
    last_name=forms.CharField(label='Modificar Apellido')
    email= forms.EmailField(label="Email Usuario")
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["first_name", "last_name", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}



class AvatarForm(forms.Form):
    imagen=forms.ImageField(label="Subir imagen")