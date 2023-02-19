from django.urls import path
# Generales
# Vehiculos
from eventos.views import CirculacionesVehiculo, EventosCirculacionVehiculo, CirculacionesVehiculoAmpliadas


urlpatterns = [
    # VEHÍCULOS 
    path('circulaciones_vehiculo/<int:id>/', CirculacionesVehiculo, name = 'circulaciones_vehiculo'),
    path('eventos_circulacion_vehiculo/<int:id>/', EventosCirculacionVehiculo, name = 'eventos_circulacion_vehiculo'),
    path('circulaciones_vehiculo_ampliadas/<int:id>/', CirculacionesVehiculoAmpliadas, name = 'circulaciones_vehiculo_ampliadas'),
]