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

# vehiculos/ejes920
@api_view(['GET'])
@permission_classes([AllowAny])
def Seleccion920(request):
    ejes = Eje.objects.filter(tipo_eje__codigo__contains='920')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EjeSerializer(ejes, many= True)
    return Response(serializer.data)

# vehiculos/ejes760
@api_view(['GET'])
@permission_classes([AllowAny])
def Seleccion760(request):
    ejes = Eje.objects.filter(tipo_eje__codigo__contains='760')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = EjeSerializer(ejes, many= True)
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
    vehiculos = Vehiculo.objects.filter(clase = 'LOCOMOTORA').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# vehiculos/auxiliares
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionAuxiliares(request):
    vehiculos = Vehiculo.objects.filter(clase = 'AUXILIAR').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)

# vehiculos/vagones
@api_view(['GET'])
@permission_classes([AllowAny])
def SeleccionVagones(request):
    vehiculos = Vehiculo.objects.filter(clase = 'VAGON').order_by('-id')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    serializer = VehiculoSerializer(vehiculos, many= True)
    return Response(serializer.data)