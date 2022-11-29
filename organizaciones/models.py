from django.db import models
from django.urls import reverse

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Actores del sistema Mercave
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Organizacion(models.Model):
    ''' Corresponde a la tabla de la base de datos con los datos de las organizaciones
        que participan en el ecosistema Mercave'''
    codigo = models.CharField(max_length=16,unique= True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    cif = models.CharField(max_length=16, null=True, blank=True)
    logo = models.CharField(max_length=150, null=True, blank=True)
    color_corporativo = models.CharField(max_length=7, null=True, blank=True)
    def __str__(self):
        return self.codigo
    def get_absolute_url(self):
        return reverse("ficha_organizacion", kwargs={'pk':self.pk})

class Diseñador(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    de_ejes = models.BooleanField(default=False)
    de_cambiadores = models.BooleanField(default=False)
    de_material_rodante = models.BooleanField(default=False)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_diseñador", kwargs={'pk':self.pk})

class Fabricante(models.Model):
    ''' hay campos para determinar las especializaciones del fabricante'''
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    de_ejes = models.BooleanField(default=False)
    de_cambiadores = models.BooleanField(default=False)
    de_bogies = models.BooleanField(default=False)
    de_vagones = models.BooleanField(default=False)
    de_locomotoras = models.BooleanField(default=False)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_fabricante", kwargs={'pk':self.pk})

class LicenciaFabricacion(models.Model):
    '''Detalles de la licencia concedida por parte de ADIF al fabricante'''
    numero = models.CharField(max_length=16, unique= True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    contrato = models.FileField(upload_to='contratos/', null=True, blank = True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    alcance = models.CharField(max_length=150, null=True, blank=True)
    ambito = models.CharField(max_length=150, null=True, blank=True)
    restricciones = models.CharField(max_length=150, null=True, blank=True)

class EEM(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    de_ejes = models.BooleanField(default=False)
    de_cambiadores = models.BooleanField(default=False)
    de_bogies = models.BooleanField(default=False)
    de_vagones = models.BooleanField(default=False)
    de_locomotoras = models.BooleanField(default=False)
    funcion1 = models.BooleanField(default=True)
    funcion2 = models.BooleanField(default=True)
    funcion3 = models.BooleanField(default=True)
    funcion4 = models.BooleanField(default=True)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_mantenedor", kwargs={'pk':self.pk})

class Keeper(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_keeper", kwargs={'pk':self.pk})

class Owner(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_operador", kwargs={'pk':self.pk})

class Aprovador(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_aprovador", kwargs={'pk':self.pk})

class Certificador(models.Model):
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    def __str__(self):
        return self.organizacion.codigo
    def get_absolute_url(self):
        return reverse("ficha_certificador", kwargs={'pk':self.pk})


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!