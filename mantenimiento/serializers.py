from dataclasses import fields
from rest_framework import serializers
from red_ferroviaria.serializers import PuntoRedMinimoSerializer
from vehiculos.models import Eje, Vehiculo
from mantenimiento.models import PlanMantenimiento, NivelMantenimiento
from eventos.models import IntervencionEje, IntervencionVehiculo

class PMSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PlanMantenimiento

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = NivelMantenimiento

class IntervencionEjeSerializer(serializers.ModelSerializer):
    punto_red = PuntoRedMinimoSerializer (many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = IntervencionEje

class IntervencionVehiculoSerializer(serializers.ModelSerializer):
    punto_red = PuntoRedMinimoSerializer (many=False, read_only=True)
    class Meta:
        fields = '__all__'
        model = IntervencionVehiculo

class DatosMantenimientoEje ():
    def __init__(self, id_eje, intervenciones):
        eje = Eje.objects.get(pk = id_eje)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pm =  PMSerializer(eje.tipo_eje.plan_mantenimiento)
        query_niveles = NivelMantenimiento.objects.filter(pm__id = eje.tipo_eje.plan_mantenimiento.id)     
        niveles = NivelSerializer(query_niveles, many =True)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        lista = IntervencionEjeSerializer(intervenciones, many =True)

        self.data = {'pm':pm.data, 'niveles':niveles.data, 'lista': lista.data}

class DatosMantenimientoVehiculo ():
    def __init__(self, id_vehiculo, intervenciones): 
        vehiculo = Vehiculo.objects.get(pk = id_vehiculo)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pm =  PMSerializer(vehiculo.tipo.plan_mantenimiento)
        query_niveles = NivelMantenimiento.objects.filter(pm__id = vehiculo.tipo.plan_mantenimiento.id)     
        niveles = NivelSerializer(query_niveles, many =True)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        lista = IntervencionVehiculoSerializer(intervenciones, many =True)

        self.data = {'pm':pm.data, 'niveles':niveles.data, 'lista': lista.data}



