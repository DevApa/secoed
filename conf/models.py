from django.db import models


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'


class Modulo(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=1000)
    orden = models.IntegerField(default=0)
    icon = models.TextField(max_length=1000)
    key = models.TextField(max_length=1000)
    menus = []

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        ordering = ('orden',)


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=1000)
    orden = models.IntegerField(default=0)
    icon = models.TextField(max_length=1000, null=True)
    href = models.TextField(max_length=1000, null=True)
    url = models.TextField(max_length=1000, null=True)
    modulo_id = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    roles = models.ManyToManyField(Rol, blank=False, through='RolMenu')
    key = models.TextField(max_length=1000, null=True)
    items = []

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        ordering = ('orden',)


class Icono(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=1000, null=True)


class Universidad(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=1000, null=True)
    telefono = models.TextField(max_length=1000, null=True)
    correo = models.TextField(max_length=1000, null=True)
    direccion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'


class Facultad(models.Model):
    id = models.AutoField(primary_key=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True)
    telefono = models.TextField(max_length=1000, null=True)
    correo = models.TextField(max_length=1000, null=True)
    direccion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'


class Carrera(models.Model):
    id = models.AutoField(primary_key=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True)
    telefono = models.TextField(max_length=1000, null=True)
    correo = models.TextField(max_length=1000, null=True)
    direccion = models.TextField(max_length=1000, null=True)
    responsable = models.TextField(max_length=1000, null=True)
    telf_responsable = models.TextField(max_length=1000, null=True)
    correo_responsable = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'


class RolMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        db_table = 'conf_rol_menu'


class RolMoodle(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.IntegerField(null=True)
    descripcion = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.descripcion}'

    class Meta:
        db_table = 'conf_rol_moodle'
