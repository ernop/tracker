import os

LOCAL=os.path.exists('local')
from local_settings import *

# Django settings for tracker project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#MANAGERS = ADMINS
#DJANGO_BASE='d:/proj/tracker'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS=(
    "django.contrib.auth.context_processors.auth",
    ##"django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    #"django.core.context_processors.request",
    #"django.contrib.messages.context_processors.messages",
    "processors.static_url_processor",
    #'django_notices.context_processors.notices',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tracker.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tracker.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tracker',
    'tracker.buy',
    'tracker.workout',
    'tracker.day',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s.py:%(lineno)d %(funcName)s() %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'db':{
            'format':'%(levelname)s %(duration)s %(sql)s %(params)s %(message)s',
        }
    },
    'handlers': {
        'file_log':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': DJANGO_BASE+'/logs/tracker.log',
            'maxBytes': 500*1024**2, # 500 MB, dumb windows not being able to roll over...
            'backupCount': 5,
            'formatter':'verbose',
        },
        'error_log':{
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': DJANGO_BASE+'/logs/error.log',
            'maxBytes': 500*1024**2, # 500 MB, dumb windows not being able to roll over...
            'backupCount': 5,
            'formatter':'verbose',
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': { #most loggers have this in addition to their normal file log.  if an error+ thing happens mail me too.
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'verbose',
        }
    },
    'loggers': {
        '': {
                'handlers': ['file_log','error_log','mail_admins',],
                'level': 'INFO',
                'propagate': True
            },
        'django': {
            'handlers':['null','console','file_log','mail_admins',],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins','file_log'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

ADMIN_EXTERNAL_BASE='/admin'

JINJA2_FILTERS=('filters.ipdbfilter','filters.jsonify')