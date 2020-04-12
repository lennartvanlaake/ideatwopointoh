from .base import *
try:
    from .local import *
except ImportError:
    pass

DEBUG = False

password = os.environ['POSTGRES_PASSWORD']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'idea',
        'PASSWORD': password,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


