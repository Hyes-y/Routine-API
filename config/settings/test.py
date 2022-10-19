"""
Test Settings
"""
from .base import *
# From Djcrety (https://djecrety.ir/)
SECRET_KEY = 'jll3)ve!+zmdf)wggf@b*0!^tb#)#*u(cyvj)0^)+ns89a(*t^'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
