"""
URL configuration for finanzacoffee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('tasks/createIngreso/', views.createIngreso, name='createIngreso'),
    path('tasks/createGasto/', views.createGasto, name='createGasto'),
    path('actualizar_ingreso/<int:id>/', views.actualizar_ingreso, name='actualizar_ingreso'),
    path('actualizar_gasto/<int:id>/', views.actualizar_gasto, name='actualizar_gasto'),
    path('eliminar_ingreso/<int:id>/', views.eliminar_ingreso, name='eliminar_ingreso'),
    path('eliminar_gasto/<int:id>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('calendario/', views.calendario, name='calendario'),
    path('tarjetas/', views.myTargets, name='tarjetas'),
    path('tarjetas/addTarget/', views.addTarget, name='addTarget'),
    path('cuentasClaras/', views.cuentasClaras, name='cuentasClaras'),
]
