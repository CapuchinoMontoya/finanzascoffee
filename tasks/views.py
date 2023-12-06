from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import activate
from django.contrib.auth import login, logout, authenticate
from .forms import CreateIngresosForm, CreateGastosForm, AddTargetForm
from .models import TblIngresos, TblGastos, TblTarjetas
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
import calendar
import json

# Create your views here.


def home(request):
    return render(request, 'home.html')

@login_required
def addTarget(request):
    if request.method == 'GET':
        return render(request, 'addTarget.html', {
            'form': AddTargetForm
        })      
    else:
        try: 
            form = AddTargetForm(request.POST)
            newTarget = form.save(commit=False)
            newTarget.usuario = request.user
            newTarget.save()
            return redirect('tasks')
        except:
            return render(request, 'addTarget.html', {
                'form': AddTargetForm,
                'error': 'Error Add Target'
            })  

@login_required
def calendario(request):
    ingresos = TblIngresos.objects.filter(usuario=request.user)
    gastos = TblGastos.objects.filter(usuario=request.user)

    eventos = []
    for ingreso in ingresos:
        fecha_str = ingreso.fechaIngreso.strftime('%Y-%m-%d')
        eventos.append({
            'title': ingreso.nombreIngreso,
            'date': fecha_str,
            'type': 'Ingreso'
        })
    for gasto in gastos:
        fecha_str = gasto.fechaGasto.strftime('%Y-%m-%d')
        eventos.append({
            'title': gasto.nombreGasto,
            'date': fecha_str,
            'type': 'Gasto'
        })
    eventos = sorted(eventos, key=lambda x: x['date'])
    eventos_json = json.dumps(eventos)

    return render(request, 'calendario.html', {
        'eventos_json': eventos_json
    })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })

@login_required
def tasks(request):
    pagoFinal = 0
    ingresos = TblIngresos.objects.filter(usuario=request.user)
    gastos = TblGastos.objects.filter(usuario=request.user)

    datos = []

    # Agregar ingresos a la lista
    for ingreso in ingresos:
        datos.append({
            'id': ingreso.id,
            'nombre': ingreso.nombreIngreso,
            'tipo': 'Ingreso',
            'cantidad': ingreso.cantidadIngreso,
            'fecha': ingreso.fechaIngreso,
        })

    # Agregar gastos a la lista
    for gasto in gastos:
        datos.append({
            'id': gasto.id,
            'nombre': gasto.nombreGasto,
            'tipo': 'Gasto',
            'cantidad': gasto.cantidadGasto,
            'fecha': gasto.fechaGasto,
        })

    datos = sorted(datos, key=lambda x: x['fecha'])
    
    pagos = []
    for dato in datos:
        if dato['tipo'] == 'Ingreso':
            pagoFinal +=  dato['cantidad']
            pagos.append({
                'id': dato['id'],
                'Total': pagoFinal,
                'FechaPago': dato['fecha'],
                'Nombre': dato['nombre'],
                'Cantidad': dato['cantidad'],
                'Tipo': 'Ingreso',
            })    
        else:
            pagoFinal -= dato['cantidad']
            pagos.append({
                'id': dato['id'],
                'Total': pagoFinal,
                'FechaPago': dato['fecha'],
                'Nombre': dato['nombre'],
                'Cantidad': dato['cantidad'],
                'Tipo': 'Gasto',
            })
    return render(request, 'tasks.html', {
        'pagos': pagos
    })

@login_required
def actualizar_ingreso(request, id):
    if request.method == 'GET':
        ingreso = get_object_or_404(TblIngresos, id=id, usuario = request.user)
        form = CreateIngresosForm(instance=ingreso)
        return render(request, 'actualizar_ingreso.html', {'form': form })
    else:
        try:
            ingreso = get_object_or_404(TblIngresos, id=id, usuario = request.user)
            form = CreateIngresosForm(request.POST, instance=ingreso)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'actualizar_ingreso.html', {'form': form, 'error': "Error updating Ingreso"})

@login_required
def eliminar_ingreso(request, id):
    try:
        ingreso = get_object_or_404(TblIngresos, id=id, usuario = request.user)
        ingreso.delete()
        return redirect('tasks')
    except ValueError:
        return redirect('tasks')

@login_required
def eliminar_gasto(request, id):
    try:
        gasto = get_object_or_404(TblGastos, id=id, usuario = request.user)
        gasto.delete()
        return redirect('tasks')
    except ValueError:
        return redirect('tasks')

@login_required
def actualizar_gasto(request, id):
    if request.method == 'GET':
            gasto = get_object_or_404(TblGastos, id=id)
            form = CreateGastosForm(instance=gasto)
            return render(request, 'actualizar_gasto.html', {'form': form})
    else:
        try:
            gasto = get_object_or_404(TblGastos, id=id, usuario = request.user)
            form = CreateGastosForm(request.POST, instance=gasto)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'actualizar_gasto.html', {'form': form, 'error': "Error updating Ingreso"})

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None: 
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or Pass is incorrect'
        })
        else:
            login(request, user)
            return redirect('tasks')
        
@login_required
def createIngreso(request):
    if request.method == 'GET':
        tarjetas= TblTarjetas.objects.filter(usuario=request.user) 
        return render(request, 'createIngreso.html', {
            'form': CreateIngresosForm,
            'tarjetas': tarjetas
        })      
    else:
        try:
            form = CreateIngresosForm(request.POST)
            newTask = form.save(commit=False)
            newTask.usuario = request.user
            idTarjeta = form.cleaned_data['tarjeta'].id
            today = timezone.now().date()
            if today >= newTask.fechaIngreso:
                tarjetas = TblTarjetas.objects.filter(usuario=request.user, id = idTarjeta)
                for tarjeta in tarjetas:
                    tarjeta.cantidadDisponible = tarjeta.cantidadDisponible + newTask.cantidadIngreso
                    tarjeta.save()
            newTask.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'createIngreso.html', {
                'form': CreateIngresosForm,
                'error': ValueError
            })  
        
@login_required
def createGasto(request):
    if request.method == 'GET':
        return render(request, 'createGasto.html', {
            'form': CreateGastosForm
        })      
    else:
        try: 
            form = CreateGastosForm(request.POST)
            newTask = form.save(commit=False)
            newTask.usuario = request.user
            newTask.save()
            return redirect('tasks')
        except:
            return render(request, 'createGasto.html', {
                'form': CreateGastosForm,
                'error': 'Plase provide valid data'
            }) 

@login_required     
def myTargets(request):
    activate('es') 
    today = timezone.now().date()
    tarjetas = TblTarjetas.objects.filter(usuario=request.user)
    ingresos = TblIngresos.objects.filter(usuario=request.user, fechaIngreso__lte = today)
    # for ingreso in ingresos:
    #     if ingreso.tarjeta:
    #         tarjetasActualizado = TblTarjetas.objects.filter(usuario=request.user, id = ingreso.tarjeta.id)
    #         for tarjeta in tarjetasActualizado:
    #             tarjeta.cantidadDisponible = tarjeta.cantidadDisponible + ingreso.cantidadIngreso
    #             tarjeta.save()
    for tarjeta in tarjetas:
        if today >= tarjeta.fechaPago:
            tarjeta.fechaPago = tarjeta.fechaPago.replace(
                month=tarjeta.fechaPago.month + 1 if tarjeta.fechaPago.month != 12 else 1,
                year=tarjeta.fechaPago.year + 1 if tarjeta.fechaPago.month == 12 else tarjeta.fechaPago.year,
                day=tarjeta.fechaPago.day
            )
            tarjeta.save()
    return render(request, 'myTargets.html', {
        'tarjetas': tarjetas
    })

@login_required 
def cuentasClaras(request):
    if request.method == 'GET':
        dineroDisponible = 0;
        today = timezone.now().date()
        ingresos = TblIngresos.objects.filter(usuario=request.user, fechaIngreso__lte = today)
        ingresosActuales = TblIngresos.objects.filter(usuario=request.user, fechaIngreso__lte=today).select_related('tarjeta')
        gastos = TblGastos.objects.filter(usuario=request.user, fechaGasto__lte = today)
        gastosFuturos = TblGastos.objects.filter(usuario=request.user, fechaGasto__gt=today)
        filtroTarjetas = []
        filtroGastos = []
        tarjetas = TblTarjetas.objects.filter(usuario=request.user)

        for ingreso in ingresos:
            dineroDisponible += ingreso.cantidadIngreso
        for gasto in gastos:
            dineroDisponible -= gasto.cantidadGasto
            fecha_str = gasto.fechaGasto.strftime('%Y-%m-%d')
            filtroGastos.append({
                'ID': gasto.id,
                'DATE': fecha_str,
                'GASTO': gasto.cantidadGasto
            })
        eventos_json = json.dumps(filtroGastos)

        for tarjeta in tarjetas:
            filtroTarjetas.append({
                'nombreTarjeta': tarjeta.nombreTarjeta,
                'idTarjeta': tarjeta.id,
                'cantidadTarjeta': tarjeta.cantidadDisponible
            })
        tarjetas_json = json.dumps(filtroTarjetas)
        return render(request, 'cuentasClaras.html', {'eventos_json': eventos_json, 'tarjetas_json': tarjetas_json, 'ingresos': ingresosActuales, 'gastos': gastosFuturos, 'dineroDisponible': dineroDisponible})
    else:
        respuesta = request.POST.get('respuesta')
        idEliminar = request.POST.get('idEliminar')
        idTarjeta = request.POST.get('idTarjeta')
        dineroDisponible = 0;
        today = timezone.now().date()
        ingresos = TblIngresos.objects.filter(usuario=request.user, fechaIngreso__lte = today)
        ingresosActuales = TblIngresos.objects.filter(usuario=request.user, fechaIngreso__lte=today).select_related('tarjeta')
        gastos = TblGastos.objects.filter(usuario=request.user, fechaGasto__lte = today)
        gastosFuturos = TblGastos.objects.filter(usuario=request.user, fechaGasto__gt=today)
        filtroTarjetas = []
        filtroGastos = []
        tarjetas = TblTarjetas.objects.filter(usuario=request.user)

        for ingreso in ingresos:
            dineroDisponible += ingreso.cantidadIngreso
        for gasto in gastos:
            dineroDisponible -= gasto.cantidadGasto
            fecha_str = gasto.fechaGasto.strftime('%Y-%m-%d')
            filtroGastos.append({
                'ID': gasto.id,
                'DATE': fecha_str
            })
        eventos_json = json.dumps(filtroGastos)
        for tarjeta in tarjetas:
            filtroTarjetas.append({
                'nombreTarjeta': tarjeta.nombreTarjeta,
                'idTarjeta': tarjeta.id
            })
        tarjetas_json = json.dumps(filtroTarjetas)
        if respuesta == 'true':
            calcularSaldos(request, idTarjeta, idEliminar)
        else:
            gastos = TblGastos.objects.filter(usuario=request.user, fechaGasto__lte = today, id = idEliminar)
            for gasto in gastos:
                if today.month == 2:
                    # Si el mes es febrero, verificamos si es año bisiesto
                    if today.year % 4 == 0:
                        ultimoDiaMes = 29
                        if today.day == ultimoDiaMes:
                            gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month + 1, day=1)
                        else:
                            gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month, day=today.day+1)
                    else:
                        ultimoDiaMes = 28
                        if today.day == ultimoDiaMes:
                            gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month + 1, day=1)
                        else:
                            gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month, day=today.day+1)
                else:
                    ultimoDiaMes = calendar.monthrange(today.year, today.month)[1]
                    if today.day == ultimoDiaMes: # Si es el último día del mes
                        if today.month == 12: # Si es diciembre
                            gasto.fechaGasto = gasto.fechaGasto.replace(year=today.year + 1, month=1, day=1) # Aumentamos el año, el mes y seteamos el día a 1
                        else:
                            gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month + 1, day=1) # Aumentamos el mes y seteamos el día a 1
                    else: # Si no es el último día
                        gasto.fechaGasto = gasto.fechaGasto.replace(month=today.month, day=today.day + 1) # Aumentamos el día en 1
                gasto.save()
        return render(request, 'cuentasClaras.html', {'eventos_json': eventos_json, 'tarjetas_json': tarjetas_json, 'ingresos': ingresosActuales, 'gastos': gastosFuturos, 'dineroDisponible': dineroDisponible})
    
def calcularSaldos(request, idTarjeta, idEliminar):
    tarjeta = get_object_or_404(TblTarjetas, id=idTarjeta, usuario = request.user)
    gasto = get_object_or_404(TblGastos, id=idEliminar, usuario = request.user)
    tarjeta.cantidadDisponible = tarjeta.cantidadDisponible - gasto.cantidadGasto
    tarjeta.save()
    gasto.delete()
