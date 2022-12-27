from django.contrib import admin
from eventos.models import OperacionCambio, CambioEje, CirculacionEje, EventoEje, EventoVehiculo, CirculacionVehiculo 
from eventos.models import AlarmaEje, AlarmaVehiculo, AlarmaCambiador, Noticia
from eventos.models import IntervencionEje, IntervencionVehiculo, RegistroIntervencionEje

# Register your models here.
# CAMBIOS
admin.site.register(OperacionCambio)
admin.site.register(CambioEje)
# CIRCULACIONES
admin.site.register(CirculacionEje)
admin.site.register(CirculacionVehiculo)
admin.site.register(EventoEje)
admin.site.register(EventoVehiculo)
# ALARMAS
admin.site.register(AlarmaEje)
admin.site.register(AlarmaVehiculo)
admin.site.register(AlarmaCambiador)
admin.site.register(Noticia)
# MANTENIMIENTO
admin.site.register(IntervencionEje)
admin.site.register(IntervencionVehiculo)
admin.site.register(RegistroIntervencionEje)