from django.contrib import admin
from .models import TblIngresos, TblGastos, TblTarjetas

# Register your models here.
admin.site.register(TblIngresos)
admin.site.register(TblGastos)
admin.site.register(TblTarjetas)