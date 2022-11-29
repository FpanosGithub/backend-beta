from django.contrib import admin
from organizaciones.models import Organizacion, Diseñador, Fabricante, LicenciaFabricacion, EEM, Keeper, Owner, Aprovador, Certificador

# Register your models here.
admin.site.register(Organizacion)
admin.site.register(Diseñador)
admin.site.register(Fabricante)
admin.site.register(LicenciaFabricacion)
admin.site.register(EEM)
admin.site.register(Keeper)
admin.site.register(Owner)
admin.site.register(Aprovador)
admin.site.register(Certificador)


