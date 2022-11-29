from django.db import models
from django.urls import reverse

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DEFINICIÓN DEL MANTENIMIENTO.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class PlanMantenimiento (models.Model):
    codigo = models.CharField(max_length=25, null= True, blank = True)
    material = models.CharField(max_length=25, null= True, blank = True)
    normativa = models.CharField(max_length=15, null= True, blank = True)
    revision = models.IntegerField(default=0)
    fecha_revisión = models.DateField(null=True, blank=True)
    elaborado_por = models.CharField(max_length=15, null= True, blank = True)
    revisado_por = models.CharField(max_length=15, null= True, blank = True)
    documento = models.CharField(max_length=15, null= True, blank = True)
    def __str__(self):
        return self.codigo

class NivelMantenimiento (models.Model):
    pm = models.ForeignKey(PlanMantenimiento, on_delete=models.CASCADE)
    nivel = models.IntegerField(default=1)
    codigo = models.CharField(max_length=5, null= True, blank = True)
    dias_siguiente_nivel = models.IntegerField(default=1000)
    km_siguiente_nivel = models.FloatField(default=100000)
    def __str__(self):
        return (self.pm.codigo + ' - ' + self.codigo)
