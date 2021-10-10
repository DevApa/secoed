from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from conf.models import Rol, RolMoodle


class UsuarioManger(BaseUserManager):
    def create_user(self, email, username, nombres, apellidos, identificacion, telefono, password=None):
        if not email:
            raise ValueError
            {'El usuario debe tener un correo electrónico'}
        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos,
            identificacion=identificacion,
            telefono=telefono,
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, username, nombres, apellidos, identificacion, telefono, password):
        usuario = self.create_user(
            email=email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            identificacion=identificacion,
            telefono=telefono,
            password=password,
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True, max_length=50)
    email = models.CharField('Correo electrónico', unique=True, max_length=254)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    identificacion = models.CharField('Identificación', unique=True, max_length=10)
    direccion = models.CharField('Direccion domiciliaria', max_length=500)
    telefono = models.CharField('Teléfono', max_length=50)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    imagen = models.ImageField('Imagen de perfil', upload_to='user/', max_length=200, blank=False, null=True,
                               height_field=None)
    roles = models.ManyToManyField(Rol, blank=False, through='RolUser')
    rol_moodle = models.ForeignKey(RolMoodle, on_delete=models.SET_NULL, null=True)
    objects = UsuarioManger()
    moodle_user = models.IntegerField('Id del usuario de moodle', null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'identificacion', 'telefono']

    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador

    class Meta:
        db_table = 'conf_user'


class RolUser(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        db_table = 'conf_rol_user'
