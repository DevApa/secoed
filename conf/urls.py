from django.contrib.auth.decorators import login_required
from django.urls import path
from conf import views

urlpatterns = [
    # menu
    path(r'menu', login_required(views.MenuContentView.as_view()), name='menu'),
    path(r'newMenu', login_required(views.MenuContentView.newMenu), name='newMenu'),
    path(r'editMenu/<int:pk>', login_required(views.MenuContentView.editMenu), name='editMenu'),
    path(r'viewMenu/<int:pk>', login_required(views.MenuContentView.viewMenu), name='viewMenu'),
    path(r'deleteMenu/<int:pk>', login_required(views.MenuContentView.deleteMenu), name='deleteMenu'),
    path(r'ajax/loadMenus', login_required(views.MenuContentView.loadMenus), name='loadMenus'),

    # modulo
    path(r'modulo', login_required(views.ModuloContentView.as_view()), name='modulo'),
    path(r'newModulo', login_required(views.ModuloContentView.newModulo), name='newModulo'),
    path(r'editModulo/<int:pk>', login_required(views.ModuloContentView.editModulo), name='editModulo'),
    path(r'viewModulo/<int:pk>', login_required(views.ModuloContentView.viewModulo), name='viewModulo'),
    path(r'deleteModulo/<int:pk>', login_required(views.ModuloContentView.deleteModulo), name='deleteModulo'),

    # universidad
    path(r'universidad', login_required(views.UniversidadContentView.as_view()), name='universidad'),
    path(r'newUniversidad', login_required(views.UniversidadContentView.newUniversidad), name='newUniversidad'),
    path(r'editUniversidad/<int:pk>', login_required(views.UniversidadContentView.editUniversidad),
         name='editUniversidad'),
    path(r'viewUniversidad/<int:pk>', login_required(views.UniversidadContentView.viewUniversidad),
         name='viewUniversidad'),
    path(r'deleteUniversidad/<int:pk>', login_required(views.UniversidadContentView.deleteUniversidad),
         name='deleteUniversidad'),

    # facultad
    path(r'facultad', login_required(views.FacultadContentView.as_view()), name='facultad'),
    path(r'newFacultad', login_required(views.FacultadContentView.newFacultad), name='newFacultad'),
    path(r'editFacultad/<int:pk>', login_required(views.FacultadContentView.editFacultad), name='editFacultad'),
    path(r'viewFacultad/<int:pk>', login_required(views.FacultadContentView.viewFacultad), name='viewFacultad'),
    path(r'deleteFacultad/<int:pk>', login_required(views.FacultadContentView.deleteFacultad), name='deleteFacultad'),

    # carrera
    path(r'carrera', login_required(views.CarreraContentView.as_view()), name='carrera'),
    path(r'newCarrera', login_required(views.CarreraContentView.newCarrera), name='newCarrera'),
    path(r'editCarrera/<int:pk>', login_required(views.CarreraContentView.editCarrera), name='editCarrera'),
    path(r'viewCarrera/<int:pk>', login_required(views.CarreraContentView.viewCarrera), name='viewCarrera'),
    path(r'deleteCarrera/<int:pk>', login_required(views.CarreraContentView.deleteCarrera), name='deleteCarrera'),

    # roles
    path(r'roles', login_required(views.RolContentView.as_view()), name='roles'),
    path(r'newRol', login_required(views.RolContentView.newRol), name='newRol'),
    path(r'editRol/<int:pk>', login_required(views.RolContentView.editRol), name='editRol'),
    path(r'viewRol/<int:pk>', login_required(views.RolContentView.viewRol), name='viewRol'),
    path(r'deleteRol/<int:pk>', login_required(views.RolContentView.deleteRol), name='deleteRol'),

    path(r'roles-menu', login_required(views.RolMenuContentView.as_view()), name='roles-menu'),
    path(r'roles-usuario', login_required(views.RolUsuarioContentView.as_view()), name='roles-usuario'),
    path(r'deleteRolMenu/<int:pk>', login_required(views.RolMenuContentView.deleteRolMenu), name='deleteRolMenu'),
    path(r'deleteRolUsuario/<int:pk>', login_required(views.RolUsuarioContentView.deleteRolUsuario),
         name='deleteRolUsuario'),

    # roles de moodle
    path(r'roles-moodle', login_required(views.RolMoodleContentView.as_view()), name='roles-moodle'),
    path(r'newRolMoodle', login_required(views.RolMoodleContentView.newRolMoodle), name='newRolMoodle'),
    path(r'editRolMoodle/<int:pk>', login_required(views.RolMoodleContentView.editRolMoodle), name='editRolMoodle'),
    path(r'viewRolMoodle/<int:pk>', login_required(views.RolMoodleContentView.viewRolMoodle), name='viewRolMoodle'),
    path(r'deleteRolMoodle/<int:pk>', login_required(views.RolMoodleContentView.deleteRolMoodle),
         name='deleteRolMoodle'),
]
