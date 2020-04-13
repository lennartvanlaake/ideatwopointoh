from .base import *
try:
    from .local import *
except ImportError:
    pass

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'empoweryouth2debate.com' ] 
SECRET_KEY = os.environ["SECRET_KEY"]
password = os.environ['POSTGRES_PASSWORD']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'idea',
        'PASSWORD': password,
        'HOST': 'empoweryouth2debate.com',
        'PORT': '5432',
    }
}




