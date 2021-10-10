from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from authentication.models import RolUser, Usuario, Rol
from conf.models import Menu, Modulo, RolMenu


def load_menu(request):
    context = {}
    if isinstance(request.user, AnonymousUser):
        return context
    else:
        # Cargar menu si es administrador:
        if request.user.usuario_administrador:
            modulos = Modulo.objects.order_by('orden')
            setMenus(modulos)
            context['modulo'] = modulos
            return context
        # Cargar menu si no es administrador
        else:
            roles = Rol.objects.filter(usuario__id=request.user.id)
            modulos = Modulo.objects.filter(menu__menu__roles__in=roles).order_by('orden').distinct()
            for mod in modulos:
                mod.menus = []
                menus = Menu.objects.filter((Q(menu__roles__in=roles) & Q(modulo_id=mod.id)) | (
                        Q(roles__in=roles) & Q(modulo_id=mod.id))).order_by('orden').distinct()
                for item in menus:
                    item.items = []
                    items = Menu.objects.filter(Q(parent_id=item.id) & Q(roles__in=roles)).order_by('orden').distinct()
                    if items:
                        item.items = items
                    mod.menus.append(item)
            context['modulo'] = modulos
            return context


def setMenuItem(menu):
    for item in menu:
        item.items = Menu.objects.filter(parent_id=item.id)
        if item.items:
            setMenuItem(item.items)


def setMenus(modulos):
    for mod in modulos:
        mod.menus = Menu.objects.filter(modulo_id=mod.id)
        setMenuItem(mod.menus)
