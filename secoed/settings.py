import os
from pathlib import Path
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd!m50t)w$$&ff(*pn7%oqw-1yxo+eub*xcxd^8pzo=*2)ynq=w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['95.216.216.98', '127.0.0.1', 'localhost']

# Base APP

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

# Third Party App

THIRD_APPS = [
    'crispy_forms',
    'widget_tweaks',
    'import_export',
]

# Local App

LOCAL_APPS = [
    'layout',
    'authentication',
    'conf',
    'cursos',
    'eva',
    'asesor',
    'components',
    'easyaudit',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

AUTH_USER_MODEL = 'authentication.Usuario'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'secoed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'secoed.initialize.load_menu'
            ],
        },
    },
]

WSGI_APPLICATION = 'secoed.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# CONEXION LOCAL --> debe regitrar su conexion si trabajara localmente
# CONEXION_NAME = 'pg_secoed'
# CONEXION_USER = 'secoed'
# CONEXION_PASSWORD = 'secoed2021'
# CONEXION_HOST = 'localhost'
# CONEXION_PORT = '5432'

# CONEXION PREPRODUCCION --> debe regitrar su conexion si trabajara con preproduccion

"""
CONEXION_NAME = 'db_pre_secoed'
CONEXION_USER = 'secoed'
CONEXION_PASSWORD = 'secoed2021'
CONEXION_HOST = '95.216.216.98'
CONEXION_PORT = 5434
"""

CONEXION_NAME = 'secoed'
CONEXION_USER = 'dba'
CONEXION_PASSWORD = 'dba2021'
CONEXION_HOST = 'localhost'
CONEXION_PORT = 5432

# CONEXION PRODUCCION --> debe regitrar su conexion si trabajara con produccion
# CONEXION_NAME = 'db_pro_secoed'
# CONEXION_USER = 'secoed'
# CONEXION_PASSWORD = 'secoed2021'
# CONEXION_HOST = 'pgdb'
# CONEXION_PORT = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': CONEXION_NAME,
        'USER': CONEXION_USER,
        'PASSWORD': CONEXION_PASSWORD,
        'HOST': CONEXION_HOST,
        'PORT': CONEXION_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SMTP Configure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'secoed.web@gmail.com'
EMAIL_HOST_PASSWORD = 'lV0G1b7xRLII&D$x1*xK'
DEFAULT_FROM_EMAIL = 'secoed.web@gmail.com'

LOGIN_REDIRECT_URL = '/authentication/pages-login'
LOGOUT_REDIRECT_URL = '/authentication/pages-login'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True

DJANGO_EASY_AUDIT_ADMIN_SHOW_MODEL_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_ADMIN_SHOW_REQUEST_EVENTS = False

TOKEN_MOODLE = 'cae40824ddd52a292888f736c8843929'
API_BASE = 'http://academyec.com/moodle/webservice/rest/server.php'
CONTEXT_ID = 116
