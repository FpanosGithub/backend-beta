from rest_framework import serializers
from vehiculos.models import Vehiculo, Eje
from ingenieria.serializers import TipoVehiculoSerializer

class EjeMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eje
        fields = ['id', 'codigo']

class VehiculoMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'codigo']

class EjeSerializer(serializers.ModelSerializer):
    version = serializers.StringRelatedField(many=False)
    fabricante = serializers.StringRelatedField(many=False)
    keeper = serializers.StringRelatedField(many=False)
    owner = serializers.StringRelatedField(many=False)
    EEM = serializers.StringRelatedField(many=False)
    bogie = serializers.StringRelatedField(many=False)
    vehiculo = VehiculoMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = Eje

class VehiculoSerializer(serializers.ModelSerializer):
    tipo = TipoVehiculoSerializer(many=False, read_only=True)
    fabricante = serializers.StringRelatedField(many=False)
    keeper = serializers.StringRelatedField(many=False)
    owner = serializers.StringRelatedField(many=False)
    EEM = serializers.StringRelatedField(many=False)
    ejes = EjeMinimoSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Vehiculo

