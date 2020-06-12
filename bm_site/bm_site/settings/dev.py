from .base import *
from .pg_local_settings import NAME, HOST, PORT, TEMPLATE, USER, PASSWORD

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
        'TEMPLATE': TEMPLATE
    }
}
