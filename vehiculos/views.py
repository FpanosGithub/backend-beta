from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Importaciones de distintas apps
# material
from vehiculos.models import Eje, Vehiculo
from vehiculos.serializers import EjeSerializer, VehiculoSerializer

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# EJES
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# vehiculos/ejes
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionEjes(request):
    ejes = Eje.objects.all().order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EjeSerializer(ejes, many= True)
    return Response(serializer.data)
# vehiculos/ejes/1/
@api_view(['GET'])
@permission_classes([AllowAny])
def DetalleEje(request, id=1):
    eje = Eje.objects.get(id=id)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EjeSerializer(eje, many= False)
    return Response(serializer.data)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VEHÍCULOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# vehiculos/
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionVehiculos(request):
    vehiculos = Vehiculo.objects.all().order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# vehiculos/1/
@api_view(['GET'])
@permission_classes([AllowAny])
def DetalleVehiculo(request, id=1):
    vehiculo = Vehiculo.objects.get(id=id)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculo, many= False)
    return Response(serializer.data)

# vehiculos/locomotoras
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionLocomotoras(request):
    vehiculos = Vehiculo.objects.filter(tipo__codigo = 'locomotora').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# vehiculos/auxiliares
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionAuxiliares(request):
    vehiculos = Vehiculo.objects.filter(tipo__codigo = 'auxiliares').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# vehiculos/vagones
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionVagones(request):
    vehiculos = Vehiculo.objects.filter(tipo__codigo = 'vagones').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)