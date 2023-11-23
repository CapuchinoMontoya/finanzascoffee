from django.shortcuts import render, redirect
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
    ingresos = TblIngresos.objects.all()
    gastos = TblGastos.objects.all()

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
            'id': ingreso.id,
            'nombre': gasto.nombreGasto,
            'tipo': 'Gasto',
            'cantidad': gasto.cantidadGasto,
            'fecha': gasto.fechaGasto,
        })

    datos = sorted(datos, key=lambda x: x['fecha'])
    fechaActual = datetime.today().date()
    
    pagos = []
    pagoFinal = 0
    for dato in datos:
        if fechaActual > dato['fecha']:
            #datos.remove(dato)
            print(dato)
        else: 
            if dato['tipo'] == 'Ingreso':
                pagoFinal +=  dato['cantidad']
                pagos.append({
                    'id': '',
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