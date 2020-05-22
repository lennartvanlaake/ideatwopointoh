from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

try:
    from .local import *
except ImportError:
    pass

DEBUG = False

sentry_sdk.init(
    dsn="https://d9b20c83c5fa4ba280c39f89de9bea17@o396671.ingest.sentry.io/5250303",
    integrations=[DjangoIntegration()],
)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'empoweryouth2debate.com']
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
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/code/application.log',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        }
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
