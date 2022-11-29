from dataclasses import fields
from rest_framework import serializers
from ingenieria.models import TipoVehiculo, TipoEje, VersionCambiador

class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TipoVehiculo

class TipoEjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TipoEje

class VersionCambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = VersionCambiador