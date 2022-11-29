from dataclasses import fields
from rest_framework import serializers
from red_ferroviaria.models import Linea, PuntoRed, Cambiador

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Linea

class PuntoRedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PuntoRed

class PuntoRedMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['codigo', 'lng', 'lat']
        model = PuntoRed

class CambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cambiador

class CambiadorMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['codigo', 'lng', 'lat']
        model = Cambiador