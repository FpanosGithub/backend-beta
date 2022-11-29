from django.db import models
from django.urls import reverse
from ingenieria.models import VersionCambiador
from organizaciones.models import Fabricante, EEM

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Modelos que identifican puntos singulares de la red ferroviaria
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Linea(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    nombre = models.CharField(max_length=100, null= True, blank = True)
    def __str__(self):
        return (str(self.codigo) + '-' + str(self.nombre))
    def get_absolute_url(self):
        return reverse("ficha_linea", kwargs={'pk':self.pk})

class PuntoRed(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    descripcion = models.CharField(max_length=100, null= True, blank = True)
    nudo = models.BooleanField(default=False)
    linea = models.ForeignKey(Linea, on_delete=models.RESTRICT, null= True, blank = True)
    pkilometrico = models.FloatField(null= True, blank = True)
    lng = models.FloatField(default=-3.9820)
    lat = models.FloatField(default=40.2951)
    def __str__(self):
        if self.codigo: return str(self.codigo)
        else: return 'Indeterminado'

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Elementos del sistema / Activos físicos
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Cambiador(models.Model):
    codigo = models.CharField(max_length=16, unique= True)
    nombre = models.CharField(max_length=100, default = 'Experimental-01')
    version= models.ForeignKey(VersionCambiador, on_delete=models.RESTRICT, null=True, blank=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True},null=True, blank=True)
    EEM = models.ForeignKey(EEM, on_delete=models.RESTRICT, limit_choices_to={'de_cambiadores': True},null=True, blank=True)
    fecha_fab = models.DateField(null=True, blank=True)
    num_cambios = models.IntegerField(default=0)
    mantenimiento = models.CharField(max_length=16, null=True, blank=True)
    lng = models.FloatField(default=-4.6920) # grados
    lat = models.FloatField(default=37.9246) # grados

    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_cambiador", kwargs={'pk':self.pk})
