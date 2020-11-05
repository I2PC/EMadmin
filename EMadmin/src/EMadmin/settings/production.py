# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=EMadmin.settings.production
from .base import *             # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = True
TEMPLATE_DEBUG = False

# Must mention ALLOWED_HOSTS in production!
ALLOWED_HOSTS = ["127.0.0.1", 'localhost']

# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

# Define STATIC_ROOT for the collectstatic command
STATIC_ROOT = join(BASE_DIR, '..', 'site', 'staticfiles')

# Log everything to the logs directory at the top
#ROB: LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')
LOGFILE_ROOT = '/home/scipionuser/logs'

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)

LATEX_REPORT_TEMPLATE = join(STATIC_ROOT, 'TEM_report.tex')
LATEX_REPORT_TEMPLATE_ICON = join(STATIC_ROOT, 'mic.jpg')
LATEX_INVOICE_TEMPLATE = join(STATIC_ROOT, 'TEM_invoice.tex')
