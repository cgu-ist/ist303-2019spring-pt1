from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../miye.sqlite3'),
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']