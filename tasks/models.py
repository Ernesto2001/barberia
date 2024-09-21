from django.db import models

# Estado
class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Roles
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


# Usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=100)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# Tipo de servicio
class TipoServicio(models.Model):
    id_tiposervicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Servicio
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    id_tiposervicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(Usuario, related_name='creado_por', on_delete=models.CASCADE)
    asignado_a = models.ForeignKey(Usuario, related_name='asignado_a', on_delete=models.CASCADE)
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return f'Servicio {self.id_servicio} - {self.descripcion}'


# Comentarios
class Comentario(models.Model):
    id_comentarios = models.AutoField(primary_key=True)
    comentario = models.TextField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comentario {self.id_comentarios} por {self.id_usuario}'
