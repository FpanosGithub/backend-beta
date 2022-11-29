from django.db import models
from django.contrib.auth.models import AbstractUser
from organizaciones.models import Organizacion

# Create your models here.
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10, null= True, blank = True)
    puesto = models.CharField(max_length=40, null= True, blank = True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.RESTRICT,null= True, blank = True)
    pass