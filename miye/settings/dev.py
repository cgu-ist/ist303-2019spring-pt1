from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition, support debug toolbar in development environment.
INSTALLED_APPS += (
        'debug_toolbar',
    )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}