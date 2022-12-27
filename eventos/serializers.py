from dataclasses import fields
from rest_framework import serializers
from eventos.models import IntervencionEje, AlarmaEje, EventoEje, CirculacionEje, CambioEje, OperacionCambio
from eventos.models import IntervencionVehiculo, AlarmaVehiculo, EventoVehiculo, CirculacionVehiculo
from eventos.models import Noticia
from vehiculos.serializers import EjeMinimoSerializer, VehiculoMinimoSerializer
from red_ferroviaria.serializers import CambiadorMinimoSerializer

class OperacionMinimoSerializer(serializers.ModelSerializer):
    cambiador = CambiadorMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = ['id', 'cambiador']
        model = OperacionCambio

class CambioSerializer(serializers.ModelSerializer):
    eje = serializers.StringRelatedField(many=False)
    operacion = OperacionMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = CambioEje

class AlarmaEjeSerializer(serializers.ModelSerializer):
    eje = EjeMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = AlarmaEje

class AlarmaVehiculoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = AlarmaVehiculo

class EventoEjeSerializer(serializers.ModelSerializer):
    en_vehiculo = serializers.StringRelatedField(many=False)
    eje = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = EventoEje

class CirculacionEjeSerializer(serializers.ModelSerializer):
    en_vehiculo = serializers.StringRelatedField(many=False)
    eje = EjeMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = CirculacionEje

class CirculacionVehiculoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = CirculacionVehiculo

class EventoVehiculoSerializer(serializers.ModelSerializer):
    vehiculo = serializers.StringRelatedField(many=False)
    class Meta:
        fields = '__all__'
        model = EventoVehiculo

class OperacionCambioSerializer(serializers.ModelSerializer):
    cambiador = CambiadorMinimoSerializer(many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = OperacionCambio

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Noticia


class DatosCirculacion ():
    def __init__(self, cursor):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        velocidades = []
        temperaturasA = []
        temperaturasB =[]
        aax = []
        aay = []
        aaz = []
        abx = []
        aby = []
        abz = []

        for doc in cursor:
            velocidades.append(doc["vel"])
            temperaturasA.append(doc["tempa"])
            temperaturasB.append(doc["tempb"])
            aax.extend(doc["aax"])
            aay.extend(doc["aay"])
            aaz.extend(doc["aaz"])
            abx.extend(doc["abx"])
            aby.extend(doc["aby"])
            abz.extend(doc["abz"])
        
        self.data = {'vel':velocidades, 'tempa':temperaturasA, 'tempb':temperaturasB,'aax':aax,'aay':aay,'aaz':aaz,'abx':abx,'aby':aby,'abz':abz}

class DatosSeleccionAlarmas ():
    def __init__(self):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        query_alarmas_ejes_activas = AlarmaEje.objects.filter(activa= True)
        query_alarmas_ejes_resueltas = AlarmaEje.objects.filter(activa= False)
        query_alarmas_vehiculos_activas = AlarmaVehiculo.objects.filter(activa= True)
        query_alarmas_vehiculos_resueltas = AlarmaVehiculo.objects.filter(activa= False)

        alarmas_ejes_activas = AlarmaEjeSerializer(query_alarmas_ejes_activas, many= True)
        alarmas_ejes_resueltas = AlarmaEjeSerializer(query_alarmas_ejes_resueltas, many= True)
        alarmas_vehiculos_activas = AlarmaVehiculoSerializer(query_alarmas_vehiculos_activas, many= True)
        alarmas_vehiculos_resueltas = AlarmaVehiculoSerializer(query_alarmas_vehiculos_resueltas, many= True)
        
        self.data = {   'ejes': {'activas':alarmas_ejes_activas.data, 'resueltas':alarmas_ejes_resueltas.data,},
                        'vehiculos':{'activas':alarmas_vehiculos_activas.data,'resueltas':alarmas_vehiculos_resueltas.data,}
        }