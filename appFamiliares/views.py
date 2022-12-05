from django.shortcuts import render
from .models import Familiar
from django.http import HttpResponse

def familiar(request):
    fami1 = Familiar(nombre="Juan", apellido="Perez", nacimiento="2001-02-03", edad=20)
    fami2= Familiar(nombre="Maria", apellido="Perez", nacimiento="1994-04-23", edad=27)
    fami3 = Familiar(nombre="Pedro", apellido="Gonzalez", nacimiento="1950-01-07", edad=71)
    fami1.save()
    fami2.save()
    fami3.save()
    texto = f"Los familiares son: {fami1.nombre} {fami1.apellido} nacido en {fami1.nacimiento}, {fami2.nombre} {fami2.apellido} nacida en {fami2.nacimiento}, {fami3.nombre} {fami3.apellido} nacido en {fami3.nacimiento}"
    return HttpResponse(texto)