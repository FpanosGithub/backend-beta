from django.urls import path
# Generales
from api.views import Actores, Alarmas
# Ejes
from api.views import SeleccionEjes, CirculacionesEje, EventosCirculacionEje, CambiosEje, MantenimientosEje
# Vehiculos
from api.views import SeleccionVehiculos, CirculacionesVehiculo, EventosCirculacionVehiculo, MantenimientosVehiculo
# Cambiadores
from api.views import OperacionesDeCambio, CambiosOperacion

urlpatterns = [
    # ACTORES
    path('actores', Actores, name = 'actores'),
    # ALARMAS
    path('alarmas', Alarmas, name = 'alarmas'),
    # EJES
    path('ejes', SeleccionEjes, name = 'ejes'),
    path('circulaciones_eje', CirculacionesEje, name = 'circulaciones_eje'),
    path('eventos_circulacion_eje', EventosCirculacionEje, name = 'eventos_circulacion_eje'),
    path('cambios_eje', CambiosEje, name = 'cambios_eje'),
    path('mantenimientos_eje', MantenimientosEje, name = 'mantenimientos_eje'),
    # VEHÍCULOS 
    path('vehiculos', SeleccionVehiculos, name = 'vehiculos'),
    path('circulaciones_vehiculo', CirculacionesVehiculo, name = 'circulaciones_vehiculo'),
    path('eventos_circulacion_vehiculo', EventosCirculacionVehiculo, name = 'eventos_circulacion_vehiculo'),
    path('mantenimientos_vehiculo', MantenimientosVehiculo, name = 'mantenimientos_vehiculo'),
    # CAMBIADORES
    path('operaciones_de_cambio', OperacionesDeCambio, name = 'operaciones_de_cambio'),
    path('cambios_operacion', CambiosOperacion, name = 'cambios_operacion'),
]