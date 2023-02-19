from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Importaciones de distintas apps
# eventos
from eventos.models import CirculacionVehiculo, EventoVehiculo
from eventos.serializers import EventoVehiculoSerializer, CirculacionVehiculoSerializer, DatosCirculacionesAmpliadas


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VEHÍCULOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# eventos/circulaciones_vehiculo
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesVehiculo(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    circulaciones = CirculacionVehiculo.objects.filter(vehiculo = id).order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CirculacionVehiculoSerializer(circulaciones, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/eventos_circulacion_vehiculo
@api_view(['GET'])
@permission_classes([AllowAny])
def EventosCirculacionVehiculo(request, id=1): 
    eventos = EventoVehiculo.objects.filter(circulacion = id).order_by('-dt')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EventoVehiculoSerializer(eventos, many= True)
    print(serializer.data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# eventos/circulaciones_vehiculo_ampliadas
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesVehiculoAmpliadas(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = DatosCirculacionesAmpliadas(id_vehiculo = id)
    print(serializer.data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)