from django.forms import ModelForm
from .models import TblIngresos, TblGastos
from django import forms

class CreateIngresosForm(ModelForm):
    class Meta:
        model = TblIngresos
        fields = ['nombreIngreso', 'cantidadIngreso', 'fechaIngreso']
        widgets = {
            'nombreIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder':"Nombre de tu Ingreso"}),
            'cantidadIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': "number", 'placeholder':"Cantidad de tu Ingreso"}),
            'fechaIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': "date", 'placeholder':"Fecha de tu Ingreso"}),
            }

class CreateGastosForm(ModelForm):
    class Meta:
        model = TblGastos
        fields = ['nombreGasto', 'cantidadGasto', 'fechaGasto']
        widgets = {
            'nombreGasto': forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder':"Nombre de tu Gasto"}),
            'cantidadGasto': forms.TextInput(attrs={'class': 'form-control', 'type': "number", 'placeholder':"Cantidad de tu Gasto"}),
            'fechaGasto': forms.TextInput(attrs={'class': 'form-control', 'type': "date", 'placeholder':"Fecha de pago"}),
            }