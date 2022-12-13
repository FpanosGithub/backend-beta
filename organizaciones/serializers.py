from dataclasses import fields
from rest_framework import serializers

from organizaciones.models import Organizacion, Diseñador, Fabricante, LicenciaFabricacion, EEM
from organizaciones.models import Keeper, Owner, Aprovador, Certificador
from ingenieria.models import TipoEje, TipoVehiculo, VersionCambiador
from ingenieria.serializers import TipoVehiculoMinimoSerializer, TipoEjeMinimoSerializer, VersionCambiadorMinimoSerializer
from red_ferroviaria.models import Cambiador
from red_ferroviaria.serializers import CambiadorSerializer

class DatosSeleccionActores ():
    def __init__(self):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #diseñadores = Diseñador.objects.all()
        query_fabricantes = Fabricante.objects.all()
        query_EEMs = EEM.objects.all()
        query_keepers = Keeper.objects.all()
        query_owners = Owner.objects.all()
        #aprovadores = Aprovador.objects.all()
        #certificadores = Certificador.objects.all()
        query_tipos_ejes = TipoEje.objects.all()
        query_tipos_vehiculos = TipoVehiculo.objects.all()
        query_versiones_cambiadores = VersionCambiador.objects.all()
        query_cambiadores = Cambiador.objects.all()

        owners = OwnerSerializer(query_owners, many= True)
        keepers = KeeperSerializer(query_keepers, many= True)
        fabricantes = FabricanteSerializer(query_fabricantes, many= True)
        EEMs = EEMSerializer(query_EEMs, many= True)
        tipos_ejes = TipoEjeMinimoSerializer(query_tipos_ejes, many= True)
        tipos_vehiculos = TipoVehiculoMinimoSerializer(query_tipos_vehiculos, many= True)
        versiones_cambiadores = VersionCambiadorMinimoSerializer(query_versiones_cambiadores, many= True)
        cambiadores = CambiadorSerializer(query_cambiadores, many= True)


        self.data = {   'owners':owners.data, 
                        'keepers':keepers.data,
                        'fabricantes':fabricantes.data,
                        'EEMs':EEMs.data,
                        'tipos_ejes':tipos_ejes.data,
                        'tipos_vehiculos':tipos_vehiculos.data,
                        'versiones_cambiadores':versiones_cambiadores.data,
                        'cambiadores':cambiadores.data,
        }

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Organizacion

class DiseñadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Diseñador

class FabricanteSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Fabricante

class LicenciaFabricacionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LicenciaFabricacion

class EEMSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = EEM

class KeeperSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Keeper

class OwnerSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Owner

class AprovadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Aprovador

class CertificadorSerializer(serializers.ModelSerializer):
    organizacion = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = Certificador