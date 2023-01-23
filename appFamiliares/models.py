from django.db import models
from django.contrib.auth.models import User


class Mensajes(models.Model):
    nombre = models.CharField(max_length=50, default='', unique=True)
    email = models.EmailField(default='')
    asunto = models.CharField(max_length=200, default='')
    mensaje = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.email+" - "+self.asunto
class Newsletter(models.Model):
    email = models.EmailField(default='')

    def __str__(self):
        return self.email
class Avatar(models.Model):
    imagen= models.ImageField(upload_to="avatars")
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user