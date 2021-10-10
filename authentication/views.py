import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from authentication.forms import UserLoginForm, UsuarioPerfilForm
from django.contrib.auth.models import auth
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from authentication.models import Usuario
from authentication.forms import UserRegisterForm
from secoed.settings import TOKEN_MOODLE, API_BASE, CONTEXT_ID

username = '';


class PagesLoginView(View):
    template_name = "authentication/pages-login.html"

    def get(self, request):
        if 'username' in request.session:
            return redirect('dashboard')
        else:
            return render(request, self.template_name, {'form': UserLoginForm})

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username == '':
                messages.error(request, 'Ingrese su usuario')
                return redirect('pages-login')
            elif password == '':
                messages.error(request, 'Ingrese su contraseña')
                return redirect('pages-login')
            else:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    if user.usuario_activo:
                        request.session['username'] = username
                        request.session['isModulo'] = False
                        auth.login(request, user)
                        return redirect('dashboard')
                    else:
                        user = None
                        messages.error(request, 'Usuario inactivo')
                        return redirect('pages-login')
                else:
                    messages.error(request, 'Credenciales invalidas')
                    return redirect('pages-login')
        else:
            return render(request, self.template_name)


class PagesRecoverpwView(View):
    template_name = 'authentication/pages-recoverpw.html'

    def get(self, request):
        if 'username' in request.session:
            return redirect('dashboard')
        else:
            return render(request, self.template_name, {'form': PasswordResetForm})

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("email", "default value")
            if Usuario.objects.filter(email=email).exists():
                password_reset_form = PasswordResetForm(request.POST)
                if password_reset_form.is_valid():
                    data = password_reset_form.cleaned_data['email']
                    associated_users = Usuario.objects.filter(Q(email=data))
                    if associated_users.exists():
                        for user in associated_users:
                            subject = "RECUPERACIÓN DE CONTRASEÑA"
                            email_template_name = "authentication/email.txt"
                            c = {
                                "username": user.username,
                                "email": user.email,
                                'domain': '95.216.216.98:8086',
                                'site_name': 'Website',
                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                "user": user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                            }
                            email = render_to_string(email_template_name, c)
                            try:
                                send_mail(subject, email, 'secoed.web@gmail.com',
                                          [user.email], fail_silently=False)
                            except BadHeaderError:
                                messages.info(request, "Email Doesn't Exists ")
                                return redirect('pages-recoverpw')
                            return redirect("password_reset_done")
                password_reset_form = PasswordResetForm()
                return render(request=request, template_name="authentication/pages-recoverpw.html",
                              context={"password_reset_form": password_reset_form})
            else:
                if email == "":
                    messages.info(request, 'Ingrese su email')
                    return redirect('pages-recoverpw')
                else:
                    messages.info(request, "Ingrese su email")
                    return redirect('pages-recoverpw')
        else:
            return render(request, 'authentication/pages-recoverpw.html')


class PagesLockscreenView(View):
    def get(self, request):
        return render(request, 'authentication/pages-lockscreen.html')


class PagesConfirmmailView(View):
    def get(self, request):
        return render(request, 'authentication/pages-confirmmail.html')


class PagesEmailVerificationView(View):
    def get(self, request):
        return render(request, 'authentication/pages-emailverificationmail.html')


class PagesTwoStepVerificationView(View):
    def get(self, request):
        return render(request, 'authentication/pages-twostepverificationmail.html')


def logout(request):
    auth.logout(request)
    return redirect('pages-login')


def verificar(nro):
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 24:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] == '001'  # se verifica que los ultimos numeros sean 001
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1) and nro[10:13] == '001'  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2) and nro[10:13] == '001'  # sociedades privadas
            else:
                return False
        else:
            return False
    else:
        return False


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


class UsuarioView(View):
    # Carga los datos iniciales del HTML
    def get(self, request):
        usuario = Usuario.objects.filter(usuario_activo=True).order_by('apellidos')
        greeting = {'heading': "Usuario", 'pageview': "Administración", 'usuarioview': usuario}
        return render(request, 'authentication/usuario.html', greeting)

    # Metodo para guardar un nuevo usuario
    def newUsuario(request):
        if request.method == 'POST':
            userForm = UserRegisterForm(request.POST)
            # Validar identificacion
            identificacion = request.POST['identificacion']
            if verificar(identificacion) == False:
                messages.warning(request, "El numero de identificación es invalida", "warning")
                return redirect('usuario')
            # Registrar user moodle
            split = request.POST['nombres'].split(' ')
            split1 = request.POST['apellidos'].split(' ')
            pswd = split[0][0].upper() + split1[0][0].lower() + "-" + request.POST['identificacion']
            # Registar usuario en moodle
            params = {
                "wstoken": TOKEN_MOODLE,
                "wsfunction": "core_user_create_users",
                "moodlewsrestformat": "json",
                "users[0][username]": request.POST['username'],
                "users[0][firstname]": request.POST['nombres'],
                "users[0][lastname]": request.POST['apellidos'],
                "users[0][email]": request.POST['email'],
                "users[0][password]": pswd,
            }
            try:
                respuesta = requests.post(API_BASE, params)
                if respuesta:
                    r = respuesta.json()
                    if respuesta.status_code == 400:
                        messages.success(request, "Error 400", "error")
                        return redirect('usuario')
                    else:
                        mutable = request.POST._mutable
                        request.POST._mutable = True
                        for id in r:
                            request.POST['moodle_user'] = id['id']
                        request.POST._mutable = mutable
            except Exception as e:
                messages.success(request, "Error al registrar el usuario en el moodle", "error")
                return redirect('usuario')
            # crear rol-usuario en moodle
            parameters = {
                "wstoken": TOKEN_MOODLE,
                "wsfunction": "core_role_assign_roles",
                "moodlewsrestformat": "json",
                "assignments[0][userid]": request.POST['moodle_user'],
                "assignments[0][roleid]": request.POST['rol_moodle'],
                "assignments[0][contextid]": CONTEXT_ID,
            }
            try:
                result = requests.post(API_BASE, parameters)
                if result:
                    r = result.json()
                    print(r)
                    if result.status_code == 400:
                        messages.success(request, "Error 400", "error")
                        return redirect('usuario')
            except Exception as e:
                print(e)
                messages.success(request, "Error al registrar el rol-usuario en el moodle", "error")
                return redirect('usuario')
            if userForm.is_valid():
                subject = "USUARIO DE INGRESO PARA EL SECOED"
                email_template_name = "authentication/register-email.txt"
                emailUser = request.POST['email']
                c = {
                    'username': request.POST['identificacion'],
                    'password': pswd,
                    'nombres': request.POST['nombres'],
                    'apellidos': request.POST['apellidos'],
                }
                email_1 = render_to_string(email_template_name, c)
                send_mail(subject, email_1, 'secoed.web@gmail.com',
                          [emailUser], fail_silently=False)
                userForm.save()
                messages.success(request, "Se registro correctamente", "success")
            else:
                # validar email existente
                aux = Usuario.objects.filter(email=request.POST['email'])
                if aux:
                    messages.warning(request, "Ya exite ese correo", "warning")
                # validar email existente
                aux = Usuario.objects.filter(identificacion=request.POST['identificacion'])
                if aux:
                    messages.warning(request, "Ya exite un usuario con esta identificación", "warning")
            return redirect('usuario')
        else:
            usuarioFormView = UserRegisterForm();
            usuario = Usuario()
            view = False
            context = {'usuarioFormView': usuarioFormView, 'usuario': usuario, 'view': view}
        return render(request, 'authentication/usuarioForm.html', context)

    # Consulta el registro de un usuario por su pk
    def viewUsuario(request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        usuarioFormView = UserRegisterForm(instance=usuario)
        view = True
        context = {'usuarioFormView': usuarioFormView, 'usuario': usuario, 'view': view}
        return render(request, 'authentication/usuarioForm.html', context)

    # Editar los datos de un usuario por su pk
    def editUsuario(request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if request.method == 'POST':
            identificacion = request.POST['identificacion']
            if not verificar(identificacion):
                messages.warning(request, "El número de identificación es invalida", "warning")
                return redirect('usuario')
            form = UserRegisterForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, "Se edito correctamente", "success")
                return redirect('usuario')
        else:
            usuarioFormView = UserRegisterForm(instance=usuario)
            view = False
            context = {'usuarioFormView': usuarioFormView, 'usuario': usuario, 'view': view}
        return render(request, 'authentication/usuarioForm.html', context)

    # Elimina un registro del usuario
    def deleteUsuario(request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if usuario:
            usuario.delete()
            messages.success(request, "Se ha eliminado correctamente", "success")
        return redirect('usuario')


class UsuarioPerfilView(View):
    template_name = 'authentication/usuarioPerfil.html'

    def get(self, request):
        usuario = get_object_or_404(Usuario, pk=request.user.id)
        usuarioPerfilForm = UsuarioPerfilForm(instance=usuario)
        greeting = {'heading': "Perfil", 'pageview': "Perfil", "form": usuarioPerfilForm, "usuario": usuario}
        return render(request, self.template_name, greeting)

    def editUsuarioPerfil(request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if request.method == 'POST':
            usuarioPerfilForm = UsuarioPerfilForm(data = request.POST, instance=usuario, files=request.FILES)
            print(usuarioPerfilForm)
            if usuarioPerfilForm.is_valid():
                usuarioPerfilForm.save()
                messages.success(request, "Se edito correctamente", "success")
                return redirect('user')
            else:
                messages.success(request, "No se puede editar", "error")
                return redirect('user')
        else:
            usuarioPerfilForm = UsuarioPerfilForm(instance=usuario)
            view = False
            context = {'usuarioPerfilForm': usuarioPerfilForm, 'usuario': usuario, 'view': view}
        return render(request, 'authentication/usuario-perfil.html', context)
