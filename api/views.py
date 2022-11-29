from eventos.models import CambioEje
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Importaciones de distintas apps
# organizaciones
from organizaciones.serializers import DatosSeleccionActores
# material
from vehiculos.ejes import filtrar_ejes
from vehiculos.vehiculos import filtrar_vehiculos
from vehiculos.serializers import EjeSerializer, VehiculoSerializer
# eventos
from eventos.models import CambioEje, EventoEje, EventoVehiculo
from eventos.logicas import filtrar_cambios_eje, filtrar_circulaciones_eje, filtrar_operaciones_cambio 
from eventos.logicas import filtrar_circulaciones_vehiculo
from eventos.serializers import DatosSeleccionAlarmas
from eventos.serializers import EventoEjeSerializer, CirculacionEjeSerializer, CambioSerializer, OperacionCambioSerializer
from eventos.serializers import EventoVehiculoSerializer, CirculacionVehiculoSerializer
# mantenimientos
from mantenimiento.logicas import filtrar_intervenciones_eje, filtrar_intervenciones_vehiculo
from mantenimiento.serializers import DatosMantenimientoEje, DatosMantenimientoVehiculo

# ACCESOS API PARA ENTREGAR INFORMACIÓN DE MERCAVE AL FRONTEND (HECHO EN REACT)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ACTORES
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# api/actores
@api_view(['GET'])
@permission_classes([AllowAny])
def Actores(request): 
    serializer = DatosSeleccionActores()
    return Response(serializer.data)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ALARMAS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# api/alarmas
@api_view(['GET'])
@permission_classes([AllowAny])
def Alarmas(request): 
    serializer = DatosSeleccionAlarmas()
    return Response(serializer.data)




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJES
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# api/ejes
@api_view(['POST'])
@permission_classes([AllowAny])
def SeleccionEjes(request):
    filtro = request.data['filtro']
    ejes = filtrar_ejes(filtro)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EjeSerializer(ejes, many= True)
    return Response(serializer.data)

# api/circulaciones_eje
@api_view(['POST'])
@permission_classes([AllowAny])
def CirculacionesEje(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de eventos del eje seleccionado con un rango temporal
    rango = request.data['rango']
    id_eje = request.data['id_eje']
    circulaciones = filtrar_circulaciones_eje(rango, id_eje)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CirculacionEjeSerializer(circulaciones, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/eventos_circulacion_eje
@api_view(['POST'])
@permission_classes([AllowAny])
def EventosCirculacionEje(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de eventos del eje seleccionado con un rango temporal
    id_circulacion = request.data['id_circulacion']
    eventos = EventoEje.objects.filter(circulacion = id_circulacion).order_by('-dt')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EventoEjeSerializer(eventos, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/cambios_eje
@api_view(['POST'])
@permission_classes([AllowAny])
def CambiosEje(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de cambios del eje seleccionados con un rango temporal
    rango = request.data['rango']
    id_eje = request.data['id_eje']
    cambios_eje = filtrar_cambios_eje(rango, id_eje)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CambioSerializer(cambios_eje, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/mantenimientos_eje
@api_view(['POST'])
@permission_classes([AllowAny])
def MantenimientosEje(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer l ainformación de plan de mantenimiento , niveles, proximos_mantenimientos
    # y una lista de intervenciones del eje seleccionados con un rango temporal
    rango = request.data['rango']
    id_eje = request.data['id_eje']
    intervenciones_eje = filtrar_intervenciones_eje(rango, id_eje)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = DatosMantenimientoEje(id_eje, intervenciones_eje)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VEHÍCULOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# api/vehiculos
@api_view(['POST'])
@permission_classes([AllowAny])
def SeleccionVehiculos(request):
    filtro = request.data['filtro']
    vehiculos = filtrar_vehiculos(filtro)   
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# api/circulaciones_vagon
@api_view(['POST'])
@permission_classes([AllowAny])
def CirculacionesVehiculo(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de eventos del eje seleccionado con un rango temporal
    rango = request.data['rango']
    id_vehiculo = request.data['id_vagon']
    circulaciones = filtrar_circulaciones_vehiculo(rango, id_vehiculo)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CirculacionVehiculoSerializer(circulaciones, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/eventos_circulacion_vagon
@api_view(['POST'])
@permission_classes([AllowAny])
def EventosCirculacionVehiculo(request): 
    id_circulacion = request.data['id_circulacion']
    eventos = EventoVehiculo.objects.filter(circulacion = id_circulacion).order_by('-dt')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EventoVehiculoSerializer(eventos, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/mantenimientos_vagón
@api_view(['POST'])
@permission_classes([AllowAny])
def MantenimientosVehiculo(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    rango = request.data['rango']
    id_vehiculo = request.data['id_vehiculo']
    intervenciones_vehiculo = filtrar_intervenciones_vehiculo(rango, id_vehiculo)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = DatosMantenimientoVehiculo(id_vehiculo, intervenciones_vehiculo)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAMBIADORES
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# api/operaciones_de_cambio
@api_view(['POST'])
@permission_classes([AllowAny])
def OperacionesDeCambio(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de operaciones de cambio con un rango temporal
    rango = request.data['rango']
    operaciones_cambio = filtrar_operaciones_cambio(rango)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = OperacionCambioSerializer(operaciones_cambio, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)


# api/cambios_operacion
@api_view(['POST'])
@permission_classes([AllowAny])
def CambiosOperacion(request): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de cambios de la operacion seleccionada
    id_operacion = request.data['id_operacion']
    cambios_operacion = CambioEje.objects.filter(operacion = id_operacion)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CambioSerializer(cambios_operacion, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)