from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CreateIngresosForm, CreateGastosForm
from .models import TblIngresos, TblGastos
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.


def home(request):
    return render(request, 'home.html')

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
        return render(request, 'createIngreso.html', {
            'form': CreateIngresosForm
        })      
    else:
        try: 
            form = CreateIngresosForm(request.POST)
            newTask = form.save(commit=False)
            newTask.usuario = request.user
            newTask.save()
            return redirect('tasks')
        except:
            return render(request, 'createIngreso.html', {
                'form': CreateIngresosForm,
                'error': 'Plase provide valid data'
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