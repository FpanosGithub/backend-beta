from django.urls import path
# Generales
# Vehiculos
from eventos.views import CirculacionesVehiculo, EventosCirculacionVehiculo, CirculacionesVehiculoAmpliadas, CirculacionesEje
from eventos.views import CirculacionesEje, EventosCirculacionEje, CirculacionesEjeAmpliadas, CambiosEje

urlpatterns = [
    # VEHÍCULOS 
    path('circulaciones_vehiculo/<int:id>/', CirculacionesVehiculo, name = 'circulaciones_vehiculo'),
    path('eventos_circulacion_vehiculo/<int:id>/', EventosCirculacionVehiculo, name = 'eventos_circulacion_vehiculo'),
    path('circulaciones_vehiculo_ampliadas/<int:id>/', CirculacionesVehiculoAmpliadas, name = 'circulaciones_vehiculo_ampliadas'),
    # EJES 
    path('circulaciones_eje/<int:id>/', CirculacionesEje, name = 'circulaciones_eje'),
    path('eventos_circulacion_eje/<int:id>/', EventosCirculacionEje, name = 'eventos_circulacion_eje'),
    path('circulaciones_eje_ampliadas/<int:id>/', CirculacionesEjeAmpliadas, name = 'circulaciones_eje_ampliadas'),
    path('cambios_eje/<int:id>/', CambiosEje, name = 'cambios_eje'),
]