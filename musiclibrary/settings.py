import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '42xi-j8*3rpzb418g6kpvdr=8pbgsn#0lr9b#62cb-e9gdp&iq'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'goovewolf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'musiclibrary.urls'
WSGI_APPLICATION = 'musiclibrary.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'es-PE'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../groovewolf-static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../groovewolf-media/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)