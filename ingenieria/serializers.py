from dataclasses import fields
from rest_framework import serializers
from ingenieria.models import TipoEje, VersionCambiador

class VersionEjeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TipoEje

class VersionCambiadorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = VersionCambiador