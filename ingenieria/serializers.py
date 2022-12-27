from dataclasses import fields
from rest_framework import serializers
from ingenieria.models import TipoVehiculo, TipoEje, VersionCambiador

class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TipoVehiculo

class TipoVehiculoMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = ['id', 'codigo', 'descripcion']

class TipoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TipoEje

class TipoEjeMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEje
        fields = ['id', 'codigo']

class VersionCambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = VersionCambiador

class VersionCambiadorMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'codigo']
        model = VersionCambiador