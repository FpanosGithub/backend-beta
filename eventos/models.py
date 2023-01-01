from django.db import models
from django.urls import reverse
from vehiculos.models import Vehiculo, Eje
from red_ferroviaria.models import PuntoRed, Cambiador
from ingenieria.models import ConsistenciaEje, ConsistenciaSI

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAMBIO. Cada cambio registra sus valores y dispara un evento para el eje
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OperacionCambio(models.Model):
    dt = models.DateTimeField()
    cambiador = models.ForeignKey(Cambiador, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_sentido =  [('UICIB', 'UIC->IB'),
                         ('IBUIC', 'IB->UIC'),
                         ('UICRUS', 'UIC->RUS'),
                         ('RUSUIC', 'RUS->UIC')]
    sentido = models.CharField(max_length=8, choices = opciones_sentido, default = 'UICIB')
    alarma = models.BooleanField(default=False)
    alarma_activa = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.pk) + ' - Cambiador: ' + str(self.cambiador.codigo))

class CambioEje(models.Model):
    operacion = models.ForeignKey(OperacionCambio, on_delete=models.CASCADE, null= True, blank = True)
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    num_cambio_eje = models.IntegerField(default=0)
    cambiador = models.ForeignKey(Cambiador, on_delete=models.CASCADE, null= True, blank = True)
    alarma = models.BooleanField(default=False)
    inicio = models.DateTimeField()               
    V = models.FloatField(default = 2.77)       # Velocidad de entrada m/s
    FV = models.FloatField(default = 250)       # Fuerza Vertical (peso en eje) KN
    # VALORES RUEDA A
    tdaM = models.FloatField(default = 5000)  # tiempo (ms) desde inicio punto de F máxima en desencerrojamiento
    fdaM = models.FloatField(default = 30)    # fuerza (KN) máxima en desencerrojamiento
    ddaM = models.FloatField(default = 10)    # desplazamiento (mm) de disco en punto de f máxima en desencerrojamiento
    tcaM = models.FloatField(default = 10000)  # tiempo (ms) desde inicio punto de F máxima en cambio
    fcaM = models.FloatField(default = 20)    # fuerza (KN) máxima en desencerrojamiento
    dcaM = models.FloatField(default = 70)  # desplazamiento (mm) de rueda en punto de F máxima en cambio
    team = models.FloatField(default = 15000)  # tiempo (ms) desde inicio punto de F minima en encerrojamiento
    feam = models.FloatField(default = 10)    # fuerza (KN) mínima en encerrojamiento
    deam = models.FloatField(default = 20)  # desplazamiento (mm) de disco en punto de F mínima en encerrojamiento
    # VALORES RUEDA B 
    tdbM = models.FloatField(default = 25000)  # tiempo (ms) desde inicio punto de F máxima en desencerrojamiento
    fdbM = models.FloatField(default = 30)    # fuerza (KN) máxima en desencerrojamiento
    ddbM = models.FloatField(default = 10)    # desplazamiento (mm) de disco en punto de f máxima en desencerrojamiento
    tcbM = models.FloatField(default = 300000)  # tiempo (ms) desde inicio punto de F máxima en cambio
    fcbM = models.FloatField(default = 20)    # fuerza (KN) máxima en desencerrojamiento
    dcbM = models.FloatField(default = 70)  # desplazamiento (mm) de rueda en punto de F máxima en cambio
    tebm = models.FloatField(default = 35000)  # tiempo (ms) desde inicio punto de F minima en encerrojamiento
    febm = models.FloatField(default = 10)    # fuerza (KN) mínima en encerrojamiento
    debm = models.FloatField(default = 20)  # desplazamiento (mm) de disco en punto de F mínima en encerrojamiento
    def __str__(self):
        return (str(self.inicio) +  ' - Eje: ' + str(self.eje.codigo))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ALARMAS 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class AlarmaEje(models.Model):
    activa = models.BooleanField(default=False)
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE, null= True, blank = True)
    dt = models.DateTimeField(null=True, blank=True)
    opciones_alarma =  [('TEMPERATURA','TEMPERATURA'),
                        ('CIRCULACION','CIRCULACION'),
                        ('CAMBIO', 'CAMBIO'),
                        ('MANTENIMIENTO', 'MANTENIMIENTO'),
                        ]
    tipo = models.CharField(max_length=15, choices = opciones_alarma, default = 'CIRCULACION')
    mensaje = models.CharField(max_length=50, null= True, blank = True)
    informe_solucion = models.CharField(max_length=50, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - Eje: ' + str(self.eje.codigo))
    
class AlarmaVehiculo(models.Model):
    activa = models.BooleanField(default=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null= True, blank = True)
    dt = models.DateTimeField(null=True, blank=True)
    opciones_alarma =  [('TRANSMISION', 'TRANSMISION'),
                        ('CIRCULACION', 'CIRCULACION'),  
                        ('MANTENIMIENTO', 'MANTENIMIENTO'),
                        ]
    tipo = models.CharField(max_length=15, choices = opciones_alarma, default = 'CIRCULACION')
    mensaje = models.CharField(max_length=50, null= True, blank = True)
    informe_solucion = models.CharField(max_length=50, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - vehículo: ' + str(self.vehiculo.id))
    
class AlarmaCambiador(models.Model):
    activa = models.BooleanField(default=False)
    cambiador = models.ForeignKey(Cambiador, on_delete=models.CASCADE, null= True, blank = True)
    dt = models.DateTimeField(null=True, blank=True)
    opciones_alarma =  [('OPERACION', 'OPERACION'),
                        ('GENERAL', 'GENERAL'),
                        ('MANTENIMIENTO', 'MANTENIMIENTO'),
                        ]
    tipo = models.CharField(max_length=15, choices = opciones_alarma, default = 'OPERACION')
    mensaje = models.CharField(max_length=50, null= True, blank = True)
    informe_solucion = models.CharField(max_length=50, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - Cambiador: ' + str(self.cambiador.codigo))   

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CIRCULACIÓN
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# VEHÍCULO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class CirculacionVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null= True, blank = True)
    abierta = models.BooleanField(default=True)
    # Punto de arranque de la circulación => coincidirá con un evento START
    dt_inicial = models.DateTimeField()
    lat_inicial = models.FloatField(default=-3.9820)
    lng_inicial = models.FloatField(default=40.2951)
    punto_red_inicial = models.CharField(max_length=16, null= True, blank = True)
    # Punto de terminación de la circulación => coincidirá con siguiente evento STOP capturado
    dt_final = models.DateTimeField(null= True, blank = True)
    lat_final = models.FloatField(default=-3.9820)
    lng_final = models.FloatField(default=40.2951)
    punto_red_final = models.CharField(max_length=16, null= True, blank = True)
    # Alarma
    alarma = models.BooleanField(default=False, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - Vehículo: ' + str(self.vehiculo.id))
    
class EventoVehiculo(models.Model):
    dt = models.DateTimeField()
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_evento =  [('START', 'EMPIEZA'),
                        ('STOP', 'PARA'),
                        ('CIRC', 'CIRCULANDO'),
                        ('NUDO','NUDO'),
                        ]
    evento = models.CharField(max_length=12, choices = opciones_evento, default = 'CIRC', null= True, blank = True)
    vel = models.FloatField(default=0, null= True, blank = True)
    alarma = models.BooleanField(default=False, null= True, blank = True)
    circulacion = models.ForeignKey(CirculacionVehiculo, on_delete=models.CASCADE, null= True, blank = True)
    def __str__(self):  
        return (str(self.pk) + ' - Vehículo: ' + str(self.vehiculo.id))
    

# EJE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class CirculacionEje(models.Model):
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    abierta = models.BooleanField(default=True)
    en_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, null= True, blank = True)
    # Punto de arranque de la circulación => coincidirá con un evento START
    dt_inicial = models.DateTimeField()
    lat_inicial = models.FloatField(default=-3.9820)
    lng_inicial = models.FloatField(default=40.2951)
    punto_red_inicial = models.CharField(max_length=16, null= True, blank = True)
    # Punto de terminación de la circulación => coincidirá con siguiente evento STOP capturado
    dt_final = models.DateTimeField(null= True, blank = True)
    lat_final = models.FloatField(default=-3.9820)
    lng_final = models.FloatField(default=40.2951)
    punto_red_final = models.CharField(max_length=16, null= True, blank = True)
    # Alarma
    alarma = models.BooleanField(default=False, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - Eje: ' + str(self.eje.codigo))

class EventoEje(models.Model):
    dt = models.DateTimeField()
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    en_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.RESTRICT, null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    opciones_evento =  [('START', 'EMPIEZA'),
                        ('STOP', 'PARA'),
                        ('CIRC', 'CIRCULANDO'),
                        ('NUDO','NUDO'),
                        ('CAMBIO','CAMBIO'),
                        ]
    evento = models.CharField(max_length=12, choices = opciones_evento, default = 'CIRC', null= True, blank = True)
    vel = models.FloatField(default=0, null= True, blank = True)
    tempa = models.FloatField(default=25, null= True, blank = True)
    tempb = models.FloatField(default=25, null= True, blank = True)
    alarma = models.BooleanField(default=False, null= True, blank = True)
    circulacion = models.ForeignKey(CirculacionEje, on_delete=models.CASCADE, null= True, blank = True)   
    axMa = models.FloatField(default=2.5, null= True, blank = True)
    axMb = models.FloatField(default=2.5, null= True, blank = True)
    ayMa = models.FloatField(default=3.5, null= True, blank = True)
    ayMb = models.FloatField(default=3.5, null= True, blank = True)
    azMa = models.FloatField(default=4.5, null= True, blank = True)
    azMb = models.FloatField(default=4.5, null= True, blank = True)
    axmeda = models.FloatField(default=2.5, null= True, blank = True)
    axmedb = models.FloatField(default=2.5, null= True, blank = True)
    aymeda = models.FloatField(default=3.5, null= True, blank = True)
    aymedb = models.FloatField(default=3.5, null= True, blank = True)
    azmeda = models.FloatField(default=4.5, null= True, blank = True)
    azmedb = models.FloatField(default=4.5, null= True, blank = True)
    def __str__(self):
        return (str(self.pk) + ' - Eje: ' + str(self.eje.codigo))

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# REGISTROS DE MANTENIMIENTOS REALIZADOD
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class IntervencionVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null= True, blank = True)
    nivel = models.CharField(max_length=5, null= True, blank = True)
    # pm = models.ForeignKey(PlanMantenimiento, on_delete=models.CASCADE, null= True, blank = True)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    inicio = models.DateField(null=True, blank=True)
    fin = models.DateField(null=True, blank=True)
    km = models.FloatField(default=0)
    firmado_por = models.CharField(max_length=25, null= True, blank = True)
    supervisado_por = models.CharField(max_length=25, null= True, blank = True)
    NC = models.BooleanField(default=False)
    NoConformidad = models.CharField(max_length=15, null= True, blank = True)
    cerrada = models.BooleanField(default=True)
    apta = models.BooleanField(default=True)
    def __str__(self):
        return (str(self.pk) + ' - ' + str(self.nivel)+ ' - Vehículo: ' + str(self.vehiculo.matricula))

class IntervencionEje(models.Model):
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE, null= True, blank = True)
    nivel = models.CharField(max_length=5, null= True, blank = True)
    # pm = models.ForeignKey(PlanMantenimiento, on_delete=models.CASCADE, null= True, blank = True)
    punto_red = models.ForeignKey(PuntoRed, on_delete=models.RESTRICT, null= True, blank = True)
    inicio = models.DateField(null=True, blank=True)
    fin = models.DateField(null=True, blank=True)
    km = models.FloatField(default=0)
    firmado_por = models.CharField(max_length=25, null= True, blank = True)
    supervisado_por = models.CharField(max_length=25, null= True, blank = True)
    NC = models.BooleanField(default=False)
    NoConformidad = models.CharField(max_length=15, null= True, blank = True)
    cerrada = models.BooleanField(default=True)
    apta = models.BooleanField(default=True)
    def __str__(self):
        return (str(self.pk) + ' - ' + str(self.nivel)+ ' - Eje: ' + str(self.eje.codigo))

class RegistroIntervencionSI(models.Model):
    interv = models.ForeignKey(IntervencionVehiculo, on_delete=models.CASCADE, null= True, blank = True)   
    consistencia = models.ForeignKey(ConsistenciaSI, on_delete=models.RESTRICT, null= True, blank = True)   

class RegistroIntervencionEje(models.Model):
    interv = models.ForeignKey(IntervencionEje, on_delete=models.CASCADE, null= True, blank = True)   
    consistencia = models.ForeignKey(ConsistenciaEje, on_delete=models.RESTRICT, null= True, blank = True)   

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ACONTECIMIENTOS - NOTICIAS DEL PROYECTO MERCAVE
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Noticia(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length=50, null= True, blank = True)
    mensaje = models.CharField(max_length=250, null= True, blank = True)
    foto = models.CharField(max_length=16, null= True, blank = True)
    opciones_subproyecto =  [('Ejes', 'Ejes'),
                         ('Cambiador', 'Cambiador'),
                         ('Vagones', 'Vagones'),
                         ('Banco Tria', 'Banco Tria'),
                         ('Banco Córdoba', 'Banco Córdoba')]
    subproyecto = models.CharField(max_length=15, choices = opciones_subproyecto, default = 'Ejes')
    alerta = models.BooleanField(default=False)
    logro = models.BooleanField(default=False)
    def __str__(self):
        return (str(self.pk) + ' - ' + str(self.fecha))   



