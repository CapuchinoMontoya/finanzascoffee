from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TblIngresos(models.Model):
    nombreIngreso = models.TextField(blank=True)
    cantidadIngreso =  models.BigIntegerField(null=False)
    fechaIngreso = models.DateField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombreIngreso

class TblGastos(models.Model):
    nombreGasto = models.TextField(blank=True)
    cantidadGasto =  models.BigIntegerField(null=False)
    fechaGasto = models.DateField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreGasto
