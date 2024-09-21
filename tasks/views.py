from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from tasks.models import Usuario, Rol

from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Usuario, Rol
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import logout

# Create your views here.


def cliente_view(request):
    return render(request, 'cliente.html')


def trabajador_view(request):
    return render(request, 'trabajador.html')


def admin_view(request):
    return render(request, 'mi-admin.html')

    citas_asignadas_count = Servicio.objects.filter(estado='asignado').count()  # Cambia el filtro según tu lógica
    citas_pendientes_count = Servicio.objects.filter(estado='pendiente').count()  # Cambia el filtro según tu lógica
    citas_cerradas_count = Servicio.objects.filter(estado='cerrado').count()  # Cambia el filtro según tu lógica
    citas_canceladas_count = Servicio.objects.filter(estado='cancelado').count()  # Cambia el filtro según tu lógica
    
    context = {
        'citas_asignadas_count': citas_asignadas_count,
        'citas_pendientes_count': citas_pendientes_count,
        'citas_cerradas_count': citas_cerradas_count,
        'citas_canceladas_count': citas_canceladas_count,
    }
    return render(request, 'admin.html', context)

def logout_view(request):
    return render(request,'menu_principal.html')

#@login_required
def agendar_cita(request):
    return render(request, 'agendar_cita.html')

#@login_required
def registro_citas(request):
    return render(request, 'registro_citas.html')

#@login_required
def reportes_citas(request):
    return render(request, 'reportes_citas.html')

def citas_asignadas(request):
    return render(request, 'citas_asignadas.html')

def signup(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        # Asumiendo que solo hay un rol de cliente
        rol = Rol.objects.get(nombre='Cliente')

        # Validaciones
        try:
            # Comprobar duplicados
            if Usuario.objects.filter(correo=correo).exists():
                raise ValidationError("El correo ya está en uso.")
            if Usuario.objects.filter(usuario=usuario).exists():
                raise ValidationError("El nombre de usuario ya está en uso.")
            if Usuario.objects.filter(telefono=telefono).exists():
                raise ValidationError("El teléfono ya está en uso.")

            # Crear el usuario con la contraseña encriptada
            nuevo_usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                usuario=usuario,
                contrasena=make_password(contrasena),  # Encriptar la contraseña
                id_rol=rol
            )
            nuevo_usuario.save()
            return redirect('login')  # Redirigir al login después de registrarse

        except ValidationError as e:
            return render(request, 'signup.html', {'error': str(e)})

        except IntegrityError:
            return render(request, 'signup.html', {'error': "Error al crear el usuario."})

    return render(request, 'signup.html')  # Renderizar el formulario de registro

def user_login(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contrasena']
        
        try:
            user = Usuario.objects.get(usuario=username)
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

        # Verificar la contraseña
        if check_password(password, user.contrasena):
            # Aquí deberías agregar la lógica para loguear al usuario
            # como establecer la sesión, etc. Esto depende de tu implementación
            request.session['user_id'] = user.id_usuario  # Guarda el ID del usuario en la sesión
            if user.id_rol.nombre == 'Cliente':
                return redirect('cliente')
            elif user.id_rol.nombre == 'Trabajador':
                return redirect('trabajador')
            elif user.id_rol.nombre == 'Admin':
                return redirect('mi-admin')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        rol_id = request.POST['rol']  # Suponiendo que el rol es enviado como un ID

        # Validar si el correo, usuario o teléfono ya existen
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('crear_usuario')

        if Usuario.objects.filter(usuario=usuario).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return redirect('crear_usuario')

        if Usuario.objects.filter(telefono=telefono).exists():
            messages.error(request, "El teléfono ya está registrado.")
            return redirect('crear_usuario')

        # Obtener el rol
        rol = Rol.objects.get(id_rol=rol_id)

        # Crear el usuario
        try:
            nuevo_usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                usuario=usuario,
                contrasena=make_password(contrasena),
                id_rol=rol
            )
            nuevo_usuario.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('mi-admin')  # Redirigir al admin después de crear el usuario
        except IntegrityError:
            messages.error(request, "Hubo un error al crear el usuario. Intente nuevamente.")

    # Obtener todos los roles para el formulario
    roles = Rol.objects.all()
    return render(request, 'crear_usuario.html', {'roles': roles})

def admin_dashboard_view(request):
    # Cualquier lógica adicional que necesites
    return render(request, 'admin_dashboard.html')


def menu_principal(request):
   
    return render(request, 'menu_principal.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('menu_principal')  # Redirige a la vista deseada