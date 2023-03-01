from django.urls import path

# Ejes
from vehiculos.views import SeleccionEjes,DetalleEje
# Vehiculos
from vehiculos.views import SeleccionVehiculos, DetalleVehiculo, SeleccionLocomotoras, SeleccionAuxiliares, SeleccionVagones

urlpatterns = [
    # EJES
    path('ejes', SeleccionEjes, name = 'ejes'),
    path('ejes/<int:id>/', DetalleEje, name = 'detalle_eje'),
    path('ejes920', SeleccionEjes, name = 'ejes920'),
    path('ejes760', SeleccionEjes, name = 'ejes760'),
    # VEHÍCULOS 
    path('', SeleccionVehiculos, name = 'vehiculos'),
    path('<int:id>/', DetalleVehiculo, name = 'detalle_vehiculo'),
    path('locomotoras', SeleccionLocomotoras, name = 'locomotoras'),
    path('auxiliares', SeleccionAuxiliares, name = 'auxiliares'),
    path('vagones', SeleccionVagones, name = 'vagones'),
]