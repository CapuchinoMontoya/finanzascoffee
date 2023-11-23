from django.forms import ModelForm
from .models import TblIngresos, TblGastos

class CreateIngresosForm(ModelForm):
    class Meta:
        model = TblIngresos
        fields = ['nombreIngreso', 'cantidadIngreso', 'fechaIngreso']

class CreateGastosForm(ModelForm):
    class Meta:
        model = TblGastos
        fields = ['nombreGasto', 'cantidadGasto', 'fechaGasto']