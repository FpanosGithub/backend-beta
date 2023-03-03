from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Importaciones de distintas apps
# eventos
from eventos.models import CirculacionVehiculo, EventoVehiculo, CirculacionEje, EventoEje, CambioEje
from eventos.serializers import EventoVehiculoSerializer, CirculacionVehiculoSerializer, DatosCirculacionesVehiculoAmpliadas
from eventos.serializers import CirculacionEjeSerializer, EventoEjeSerializer, DatosCirculacionesEjeAmpliadas, CambioSerializer


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VEHÍCULOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# eventos/circulaciones_vehiculo
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesVehiculo(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    circulaciones = CirculacionVehiculo.objects.filter(vehiculo = id).order_by('-id')[:15]
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
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# eventos/circulaciones_vehiculo_ampliadas
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesVehiculoAmpliadas(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = DatosCirculacionesVehiculoAmpliadas(id_vehiculo = id)
    print(serializer.data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJES
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# eventos/circulaciones_eje
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesEje(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    circulaciones = CirculacionEje.objects.filter(eje = id).order_by('-id')[:15]
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CirculacionEjeSerializer(circulaciones, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# api/eventos_circulacion_eje
@api_view(['GET'])
@permission_classes([AllowAny])
def EventosCirculacionEje(request, id=1): 
    eventos = EventoEje.objects.filter(circulacion = id).order_by('-dt')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EventoEjeSerializer(eventos, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# eventos/circulaciones_eje_ampliadas
@api_view(['GET'])
@permission_classes([AllowAny])
def CirculacionesEjeAmpliadas(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = DatosCirculacionesEjeAmpliadas(id_eje = id)
    print(serializer.data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)

# eventos/cambios_eje
@api_view(['GET'])
@permission_classes([AllowAny])
def CambiosEje(request, id=1): 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Vamos a componer una lista de cambios del eje solicitado
    cambios = CambioEje.objects.filter(eje = id).order_by('-inicio')[:20]
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = CambioSerializer(cambios, many= True)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return Response(serializer.data)