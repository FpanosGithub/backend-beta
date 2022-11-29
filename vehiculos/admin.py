from django.contrib import admin
from vehiculos.models import Vehiculo
from vehiculos.models import Eje, ConjuntoEje, ElementoEje
from vehiculos.models import Distribuidor, ConjuntoDistribuidor
from vehiculos.models import SistIntegradoVehiculo, ConjuntoSI, ElementoSI

# Register your models here.
admin.site.register(Vehiculo)

admin.site.register(Eje)
admin.site.register(ConjuntoEje)
admin.site.register(ElementoEje)

admin.site.register(Distribuidor)
admin.site.register(ConjuntoDistribuidor)

admin.site.register(SistIntegradoVehiculo)
admin.site.register(ConjuntoSI)
admin.site.register(ElementoSI)
