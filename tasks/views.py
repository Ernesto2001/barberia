from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from tasks.models import Usuario, Rol, Servicio, Estado
from .models import Servicio, TipoServicio

from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Usuario, Rol
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import logout

from django.db.models import Sum

# Create your views here.


def cliente_view(request):
    return render(request, 'cliente.html')


def trabajador_view(request):
    return render(request, 'trabajador.html')


def admin_view(request):
   return render(request, 'mi-admin.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')  # Asegúrate que redirige a 'login' 

def agendar_cita(request):
    return render(request, 'agendar_cita.html')


def registro_citas(request):
    return render(request, 'registro_citas.html')


def reportes_citas(request):
    return render(request, 'reportes_citas.html')


def citas_asignadas(request):
    # Filtrar citas por estado "Asignado", "Finalizado" y "Pendiente"
  
    citas_finalizadas = Servicio.objects.filter(id_estado__nombre="Finalizado")
    
    # Crear el contexto para pasar a la plantilla
    context = {
        'citas_finalizadas': citas_finalizadas,
    }

    return render(request, 'citas_asignadas.html', context)




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

        # Intenta obtener el usuario por el nombre de usuario
        try:
            user = Usuario.objects.get(usuario=username)
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

        # Verificar la contraseña usando check_password (si las contraseñas están hasheadas)
        if check_password(password, user.contrasena):
            # Establecer la sesión manualmente
            request.session['user_id'] = user.id_usuario  # Guarda el ID del usuario en la sesión
            request.session['nombre'] = user.nombre  # Guarda el nombre del usuario para mostrar en la plantilla

            # Redirigir según el rol del usuario
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
    estados = Estado.objects.all()

    # Contar las citas según su estado
    citas_asignadas_count = Servicio.objects.filter(id_estado__nombre='Asignado').count()
    citas_pendientes_count = Servicio.objects.filter(id_estado__nombre='Pendiente').count()
    citas_finalizadas_count = Servicio.objects.filter(id_estado__nombre='Finalizado').count()
    citas_canceladas_count = Servicio.objects.filter(id_estado__nombre='Cancelado').count()

    # Calcular el total de ingresos (suma de precios de servicios que están finalizados)
    total_ingresos = Servicio.objects.filter(id_estado__nombre='Finalizado').aggregate(Sum('precio'))['precio__sum'] or 0

    # Crear el contexto para pasar a la plantilla
    context = {
        'citas_asignadas_count': citas_asignadas_count,
        'citas_pendientes_count': citas_pendientes_count,
        'citas_canceladas_count': citas_canceladas_count,
        'citas_finalizadas_count': citas_finalizadas_count,
        'total_ingresos': total_ingresos,
    }
    
    # Renderizar la plantilla con el contexto
    return render(request, 'admin_dashboard.html', context)
    

def ver_registro_admin(request):
      # Obtener solo las citas con estado "Pendiente" (ajusta el id_estado según tu tabla)
    citas = Servicio.objects.filter(id_estado_id=1)  # Cambia 1 por el id del estado "Pendiente"

    # Crear el contexto para pasar a la plantilla
    context = {
        'citas': citas,
    }
    return render(request, 'ver_registro_admin.html', context)

def asignar_cita(request, cita_id):
    if request.method == 'POST':
        usuario_asignado_id = request.POST.get('usuario_asignado')
        
        # Obtén la cita y actualiza el usuario asignado
        cita = Servicio.objects.get(id=cita_id)
        cita.asignado_a_id = usuario_asignado_id
        cita.save()

        # Redirigir a la vista de registro admin después de la asignación
        return redirect('ver_registro_admin')


def menu_principal(request):
   
    return render(request, 'menu_principal.html')



def agendar(request):
    usuario = request.user  # Obtener el usuario autenticado
    tipos_servicio = TipoServicio.objects.all()  # Obtener los tipos de servicio disponibles

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tipo_servicio_id = request.POST.get('tipo_servicio')
        tipo_servicio = TipoServicio.objects.get(id_tiposervicio=tipo_servicio_id)

        # Aquí estamos asumiendo que al crear la cita estará en estado 'Pendiente' o cualquier otro estado inicial que tengas.
        estado_pendiente = Estado.objects.get(nombre="Pendiente")  # Asegúrate de tener este estado en la base de datos

        # Crear el servicio (la cita)
        nueva_cita = Servicio(
            precio=0,  # Puedes establecer un precio fijo o dinámico si lo prefieres
            id_tiposervicio=tipo_servicio,
            creado_por=usuario,  # Cliente que está creando la cita
            asignado_a=None,  # Esto lo puede asignar un admin o trabajador más tarde
            id_estado=estado_pendiente,  # Inicialmente, estado 'Pendiente'
            descripcion=f"Cita para {tipo_servicio.nombre}",
            fecha=fecha
        )
        nueva_cita.save()

        return redirect('ver_registro')  # Redirigir a la página de registro o lista de citas después de agendar

    return render(request, 'agendar.html', {
        'usuario': usuario,
        'tipos_servicio': tipos_servicio
    })
     

def ver_registro(request):
    # Aquí puedes obtener las citas desde la base de datos si es necesario 
   citas = Servicio.objects.all()  # Cambia 'Servicio' si es necesario.
   return render(request, 'ver_registro.html')
 