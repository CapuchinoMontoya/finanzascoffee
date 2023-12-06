from django.forms import ModelForm
from .models import TblIngresos, TblGastos, TblTarjetas
from django import forms

class CreateIngresosForm(ModelForm):
    class Meta:
        model = TblIngresos
        fields = ['nombreIngreso', 'cantidadIngreso', 'fechaIngreso', 'tarjeta']
        widgets = {
            'nombreIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Nombre de tu Ingreso'}),
            'cantidadIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Cantidad de tu Ingreso'}),
            'fechaIngreso': forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Fecha de tu Ingreso'}),
            'tarjeta': forms.Select(attrs={'class': 'form-control'}),
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

class AddTargetForm(ModelForm):
    class Meta:
        model = TblTarjetas
        fields = ['nombreTarjeta', 'numTarjeta', 'cantidadDisponible', 'tipoTarjeta', 'fechaPago']
        widgets = {
            'nombreTarjeta': forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder':"Nombre de tu Gasto"}),
            'numTarjeta': forms.TextInput(attrs={'class': 'form-control', 'type': "number", 'placeholder':"Ultimos 4 digitos de la tarjeta"}),
            'cantidadDisponible': forms.HiddenInput(attrs={'value': 0}),
            'tipoTarjeta' : forms.Select(attrs={'class': 'form-control', 'placeholder':"Tipo de Tarjeta"}, choices=(
                ("Credito", "Tarjeta de Crédito"),
                ("Debito", "Tarjeta de Débito"),
                ("Prestamo", "Préstamo"),
                ("Efectivo", "Efectivo"),
            )),
            'fechaPago': forms.TextInput(attrs={'class': 'form-control', 'type': "date", 'placeholder':"Fecha de corte"}),
            }