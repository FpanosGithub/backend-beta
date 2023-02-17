from django.urls import path
# Generales
# Vehiculos
from eventos.views import CirculacionesVehiculo, EventosCirculacionVehiculo


urlpatterns = [
    # VEHÍCULOS 
    path('circulaciones_vehiculo/<int:id>/', CirculacionesVehiculo, name = 'circulaciones_vehiculo'),
    path('eventos_circulacion_vehiculo/<int:id>/', EventosCirculacionVehiculo, name = 'eventos_circulacion_vehiculo'),
]