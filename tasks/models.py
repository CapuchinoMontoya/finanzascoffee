from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TblIngresos(models.Model):
    nombreIngreso = models.TextField(blank=True)
    cantidadIngreso =  models.BigIntegerField(null=False)
    fechaIngreso = models.DateField(null=False)
    tarjeta = models.ForeignKey('TblTarjetas', on_delete=models.SET_NULL, null=True, blank=True)
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

class TblTarjetas(models.Model):
    nombreTarjeta = models.TextField(blank=True)
    numTarjeta =  models.IntegerField(null=True)
    cantidadDisponible =  models.BigIntegerField(null=True)
    tipoTarjeta = models.CharField(max_length=20, choices=(
        ("Credito", "Tarjeta de Crédito"),
        ("Debito", "Tarjeta de Débito"),
        ("Prestamo", "Préstamo"),
        ("Efectivo", "Efectivo"),
    ), null=False)

    fechaPago = models.DateField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreTarjeta
