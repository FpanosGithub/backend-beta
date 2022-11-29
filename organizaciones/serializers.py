from dataclasses import fields
from rest_framework import serializers

from organizaciones.models import Organizacion, Diseñador, Fabricante, LicenciaFabricacion, EEM
from organizaciones.models import Keeper, Owner, Aprovador, Certificador
from ingenieria.models import TipoEje, VersionCambiador
from red_ferroviaria.models import Cambiador
from ingenieria.serializers import VersionEjeSerializer, VersionCambiadorSerializer
from material.serializers import ModeloVagonSerializer, CambiadorSerializer

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
        query_versiones_ejes = VersionEje.objects.all()
        query_modelos_vagones = ModeloVagon.objects.all()
        query_versiones_cambiadores = VersionCambiador.objects.all()
        query_cambiadores = Cambiador.objects.all()


        owners = OwnerSerializer(query_owners, many= True)
        keepers = KeeperSerializer(query_keepers, many= True)
        fabricantes = FabricanteSerializer(query_fabricantes, many= True)
        EEMs = EEMSerializer(query_EEMs, many= True)
        versiones_ejes = VersionEjeSerializer(query_versiones_ejes, many= True)
        modelos_vagones = ModeloVagonSerializer(query_modelos_vagones, many= True)
        versiones_cambiadores = VersionCambiadorSerializer(query_versiones_cambiadores, many= True)
        cambiadores = CambiadorSerializer(query_cambiadores, many= True)


        self.data = {   'owners':owners.data, 
                        'keepers':keepers.data,
                        'fabricantes':fabricantes.data,
                        'EEMs':EEMs.data,
                        'versiones_ejes':versiones_ejes.data,
                        'modelos_vagones':modelos_vagones.data,
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