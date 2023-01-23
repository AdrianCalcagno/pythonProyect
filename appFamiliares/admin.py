from django.contrib import admin
from .models import Mensajes, Avatar, Newsletter
# Register your models here.

admin.site.register(Mensajes)
admin.site.register(Avatar)
admin.site.register(Newsletter)