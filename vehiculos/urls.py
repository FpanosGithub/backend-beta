from django.urls import path

# Ejes
from vehiculos.views import SeleccionEjes,DetalleEje, Seleccion920, Seleccion760
# Vehiculos
from vehiculos.views import SeleccionVehiculos, DetalleVehiculo, SeleccionLocomotoras, SeleccionAuxiliares, SeleccionVagones

urlpatterns = [
    # EJES
    path('ejes', SeleccionEjes, name = 'ejes'),
    path('ejes/<int:id>/', DetalleEje, name = 'detalle_eje'),
    path('ejes920', Seleccion920, name = 'ejes920'),
    path('ejes760', Seleccion760, name = 'ejes760'),
    # VEHÍCULOS 
    path('', SeleccionVehiculos, name = 'vehiculos'),
    path('<int:id>/', DetalleVehiculo, name = 'detalle_vehiculo'),
    path('locomotoras', SeleccionLocomotoras, name = 'locomotoras'),
    path('auxiliares', SeleccionAuxiliares, name = 'auxiliares'),
    path('vagones', SeleccionVagones, name = 'vagones'),
]