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


class DatosCirculacionesVehiculoAmpliadas ():
    def __init__(self, id_vehiculo):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Sacamos las últimas x (15) circulaciones de ese vehículo
        lista_circulaciones = CirculacionVehiculo.objects.filter(vehiculo = id_vehiculo).order_by('-id')[:15]
        circulaciones_ampliadas = []
        circulacion_ampliada = {}
        for circulacion in lista_circulaciones:
            circulacion_ampliada= {
                'id': circulacion.id,
                'abierta': circulacion.abierta,
                'alarma': circulacion.alarma,
                'dt_inicial': circulacion.dt_inicial,
                'lat_inicial': circulacion.lat_inicial,
                'lng_inicial': circulacion.lng_inicial,
                'punto_red_inicial': circulacion.punto_red_inicial,
                'dt_final': circulacion.dt_final,
                'lat_final': circulacion.lat_final,
                'lng_final': circulacion.lng_final,
                'punto_red_final': circulacion.punto_red_final,
                'eventos': self.DatosEventos(id_circulacion = circulacion.id)
            }
            circulaciones_ampliadas.append(circulacion_ampliada)

        self.data = circulaciones_ampliadas
    
    def DatosEventos (self, id_circulacion):        
        query_eventos = EventoVehiculo.objects.filter(circulacion = id_circulacion).order_by('-dt')
        lista_eventos = []
        evento = {}
        for item in query_eventos:
            evento = {
                'id': item.id,
                'dt': item.dt,
                'lng': item.lng,
                'lat': item.lat,
                'punto_red': item.punto_red,
                'evento': item.evento,
                'vel': item.vel,
                'alarma': item.alarma,
            }
            lista_eventos.append(evento)
            
        return lista_eventos

class DatosCirculacionesEjeAmpliadas ():
    def __init__(self, id_eje):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Sacamos las últimas x (15) circulaciones de ese vehículo
        lista_circulaciones = CirculacionEje.objects.filter(eje = id_eje).order_by('-id')[:15]
        circulaciones_ampliadas = []
        circulacion_ampliada = {}
        for circulacion in lista_circulaciones:
            circulacion_ampliada= {
                'id': circulacion.id,
                'abierta': circulacion.abierta,
                'alarma': circulacion.alarma,
                'en_vehiculo': circulacion.en_vehiculo.matricula,
                'dt_inicial': circulacion.dt_inicial,
                'lat_inicial': circulacion.lat_inicial,
                'lng_inicial': circulacion.lng_inicial,
                'punto_red_inicial': circulacion.punto_red_inicial,
                'dt_final': circulacion.dt_final,
                'lat_final': circulacion.lat_final,
                'lng_final': circulacion.lng_final,
                'punto_red_final': circulacion.punto_red_final,
                'eventos': self.DatosEventos(id_circulacion = circulacion.id)
            }
            circulaciones_ampliadas.append(circulacion_ampliada)

        self.data = circulaciones_ampliadas
    
    def DatosEventos (self, id_circulacion):        
        query_eventos = EventoEje.objects.filter(circulacion = id_circulacion).order_by('-dt')
        lista_eventos = []
        evento = {}
        for item in query_eventos:
            evento = {
                'id': item.id,
                'dt': item.dt,
                'lng': item.lng,
                'lat': item.lat,
                'punto_red': item.punto_red,
                'evento': item.evento,
                'alarma': item.alarma,
                'vel': item.vel,
                'tempa': item.tempa,
                'tempb': item.tempb,
                'axMa': item.axMa,
                'axMb': item.axMb,
                'ayMa': item.ayMa,
                'ayMb': item.ayMb,
                'azMa': item.azMa,
                'azMb': item.azMb,
                'axmeda': item.axmeda,
                'axmedb': item.axmedb,
                'aymeda': item.aymeda,
                'aymedb': item.aymedb,
                'azmeda': item.azmeda,
                'azmedb': item.azmedb,
            }
            lista_eventos.append(evento)
            
        return lista_eventos      

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