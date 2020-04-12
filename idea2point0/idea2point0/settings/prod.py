from .base import *

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]
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


