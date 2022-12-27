from django.contrib import admin

from red_ferroviaria.models import Linea, PuntoRed, Cambiador

# Register your models here.
admin.site.register(Linea)
admin.site.register(PuntoRed)
admin.site.register(Cambiador)