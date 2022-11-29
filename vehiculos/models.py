from django.db import models
from django.urls import reverse
from organizaciones.models import Owner, Fabricante, EEM, Keeper
from ingenieria.models import TipoVehiculo, TipoEje, TipoConjuntoEje, TipoElementoEje

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 1. VEHICULOS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Vehiculo(models.Model):
    # Descripción del vehiculo
    codigo = models.CharField(max_length=16, unique= True)
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE, null=True, blank=True)
    matricula = models.CharField(max_length=100, default = ' ', null=True, blank=True)
    descripcion = models.CharField(max_length=100, default = ' ', null=True, blank=True)
    #!!!!!!!!
    km_origen = models.FloatField(default=0)                  # km que llevaba cuando la EEM lo asumió
    fecha_origen = models.DateField(default = "2022-01-01")   # cuando lo asumión la EEM
    #!!!!!!!!
    # Quien es quién
    owner= models.ForeignKey(Owner, on_delete=models.RESTRICT, null=True, blank=True)
    keeper= models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    EEM= models.ForeignKey(EEM, on_delete=models.RESTRICT, null=True, blank=True)
    fabricante= models.ForeignKey(Fabricante, on_delete=models.RESTRICT, null=True, blank=True)
    fecha_fab = models.DateField(null=True, blank=True)
    # Mantenimiento del Vehículo
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)    # cuando terminó el último mantenimiento
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)    # cuando será el proximo mantenimiento
    km_proximo_mant = models.FloatField(default=0, null=True, blank=True)
    nivel_proximo_mant = models.IntegerField(default=0)
    # Estado del Vehículo
    estado_servicio = models.CharField(max_length=15, choices = [('BAJA','BAJA'),('CIRCULANDO','CIRCULANDO'),('PARADO','PARADO'),('MANTENIMIENTO','MANTENIMIENTO')], default = 'PARADO')
    observaciones_servicio = models.CharField(max_length=80, default = 'sin observaciones')
    transmitiendo = models.BooleanField(default=False)
    alarma = models.BooleanField(default=False)
    ultimo_evento_dt = models.DateTimeField(null=True, blank=True)
    en_nudo = models.BooleanField(default=False)
    vel = models.FloatField(default=0, null=True, blank=True)
    lng = models.FloatField(default=-3.9820) # grados
    lat = models.FloatField(default=40.2951) # grados
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    km_totales = models.FloatField(default=0)           # km origen + km circulados
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_vehiculo", kwargs={'pk':self.pk})

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 2. SISTEMAS DE UN VEHÍCULO
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 2.1 EJE MONTADO
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Eje(models.Model):
    #Identificación
    codigo = models.CharField(max_length=16, unique= True)
    tipo_eje = models.ForeignKey(TipoEje, on_delete=models.RESTRICT, null=True, blank=True)
    #!!!!!!!!
    km_origen = models.FloatField(default=0)                    # km que llevaba cuando la EEM lo asumió
    fecha_origen = models.DateField(default = "2022-01-01")     # cuando lo asumión la EEM
    #!!!!!!!!
    #Quien es quién
    owner = models.ForeignKey(Owner, on_delete=models.RESTRICT, null=True, blank=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.RESTRICT, limit_choices_to={'de_ejes': True},null=True, blank=True)
    fecha_fab = models.DateField(null=True, blank=True)
    keeper = models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    EEM = models.ForeignKey(EEM, on_delete=models.RESTRICT, null=True, blank=True)
    # Situación de Mantenimiento
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True) 
    fecha_proximo_mantenimiento = models.DateField(null=True, blank=True)    # cuando será el proximo mantenimiento
    km_proximo_mant = models.FloatField(default=0)
    nivel_proximo_mant = models.IntegerField(default=0)
    #Situación operativa
    vehiculo = models.ForeignKey(Vehiculo, related_name='ejes', on_delete=models.RESTRICT, null=True, blank=True)
    estado_servicio = models.CharField(max_length=15, choices = [('BAJA','BAJA'),('CIRCULANDO','CIRCULANDO'),('PARADO','PARADO'),('MANTENIMIENTO','MANTENIMIENTO')], default = 'PARADO')
    observaciones_servicio = models.CharField(max_length=80, default = 'sin observaciones')
    alarma_temp = models.BooleanField(default=False)
    alarma_aceleraciones = models.BooleanField(default=False)
    alarma_cambio = models.BooleanField(null=True,default=False)
    alarma_mantenimiento = models.BooleanField(null=True,default=False)
    tempa = models.FloatField(default=25.0, null=True, blank=True)
    tempb = models.FloatField(default=25.0, null=True, blank=True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #Vida del eje
    num_cambios = models.IntegerField(default=0)
    km_totales = models.FloatField(default=0)           # km origen + km circulados
    coef_trabajo = models.FloatField(default=0)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_eje", kwargs={'pk':self.pk})

class ConjuntoEje(models.Model):
    eje = models.ForeignKey(Eje, related_name='conjuntos', on_delete=models.RESTRICT, null=True, blank=True)
    tipo = models.ForeignKey(TipoConjuntoEje, on_delete=models.RESTRICT, null=True, blank=True)
    codigo = models.CharField(max_length=16, unique= True)
    num_conjuntos = models.IntegerField(default=0)
    def __str__(self):
        return self.codigo

class ElementoEje(models.Model):
    conjunto = models.ForeignKey(ConjuntoEje, related_name='conjuntos', on_delete=models.RESTRICT, null=True, blank=True)
    tipo = models.ForeignKey(TipoElementoEje, on_delete=models.RESTRICT, null=True, blank=True)
    codigo = models.CharField(max_length=16, unique= True)
    num_elementos = models.IntegerField(default=0)
    def __str__(self):
        return self.codigo


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 2.2 DISTRIBUIDOR
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Distribuidor(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    marcado = models.CharField(max_length=20,default = ' ', null=True, blank=True)
    tipo = models.CharField(max_length=16, default = '', null=True, blank=True)
    documentacion_tecnica = models.CharField(max_length=30, default = ' ', null=True, blank=True)
    imagen = models.CharField(max_length=30,default = ' ', null=True, blank=True)
    # Quien es quién
    owner= models.ForeignKey(Owner, on_delete=models.RESTRICT, null=True, blank=True)
    keeper= models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    EEM= models.ForeignKey(EEM, on_delete=models.RESTRICT, limit_choices_to={'de_bogies': True},)
    # Situación
    vehiculo= models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, null=True, blank=True)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_bogie", kwargs={'pk':self.pk}) 

class ConjuntoDistribuidor(models.Model):
    nombre = models.CharField(max_length=16, default = '', null=True, blank=True)
    tipo = models.CharField(max_length=16, default = '', null=True, blank=True)
    num = models.IntegerField(default=0)
    documentacion_tecnica = models.CharField(max_length=30, default = ' ', null=True, blank=True)
    # Situación
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.codigo

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 2.3 OTROS SISTEMAS INTEGRADOS EN EL VEHÍCULO
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class SistIntegradoVehiculo(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    marcado = models.CharField(max_length=20,default = ' ', null=True, blank=True)
    tipo = models.CharField(max_length=16, default = '', null=True, blank=True)
    documentacion_tecnica = models.CharField(max_length=30, default = ' ', null=True, blank=True)
    imagen = models.CharField(max_length=30,default = ' ', null=True, blank=True)
    # Quien es quién
    owner= models.ForeignKey(Owner, on_delete=models.RESTRICT, null=True, blank=True)
    keeper= models.ForeignKey(Keeper, on_delete=models.RESTRICT, null=True, blank=True)
    EEM= models.ForeignKey(EEM, on_delete=models.RESTRICT, limit_choices_to={'de_bogies': True},)
    # Situación
    vehiculo= models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, null=True, blank=True)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_bogie", kwargs={'pk':self.pk}) 

class ConjuntoSI(models.Model):
    nombre = models.CharField(max_length=16, default = '', null=True, blank=True)
    tipo = models.CharField(max_length=16, default = '', null=True, blank=True)
    num = models.IntegerField(default=0)
    documentacion_tecnica = models.CharField(max_length=30, default = ' ', null=True, blank=True)
    # Situación
    sistema = models.ForeignKey(SistIntegradoVehiculo, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.codigo

class ElementoSI(models.Model):
    nombre = models.CharField(max_length=16, default = '', null=True, blank=True)
    tipo = models.CharField(max_length=16, default = '', null=True, blank=True)
    num = models.IntegerField(default=0)
    documentacion_tecnica = models.CharField(max_length=30, default = ' ', null=True, blank=True)
    # Situación
    conjunto = models.ForeignKey(ConjuntoSI, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.codigo