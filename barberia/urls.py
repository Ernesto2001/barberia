"""
URL configuration for barberia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/', views.cliente_view, name='cliente'),
    path('trabajador/', views.trabajador_view, name='trabajador'),
    path('mi-admin/', views.admin_view, name='mi-admin'),
    path('logout/', views.logout_view, name='logout'), 
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
    path('registro_citas/', views.registro_citas, name='registro_citas'),
    path('reportes_citas/', views.reportes_citas, name='reportes_citas'),
    path('logout/', views.logout_view, name='logout'),
    path('citas_asignadas/', views.citas_asignadas, name='citas_asignadas'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('menu/', views.menu_principal, name='menu_principal'),
    path('', lambda request: redirect('menu_principal', permanent=False)), 
   
]
