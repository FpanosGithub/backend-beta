from django.shortcuts import render
from rest_framework import generics, viewsets

from red_ferroviaria.models import Linea, PuntoRed
from red_ferroviaria.serializers import LineaSerializer, PuntoRedSerializer

# Create your views here.

class Lineas(viewsets.ModelViewSet):
    queryset = Linea.objects.all()
    serializer_class = LineaSerializer

class PuntosRed(viewsets.ModelViewSet):
    queryset = PuntoRed.objects.all()
    serializer_class = PuntoRedSerializer