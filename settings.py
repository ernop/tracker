import os


ADVANCING_TAGS=[]
EXCLUDED_TAGS=['done','delete','undelete',]
#tags which if you add them, automatically advance to the next photo.
#these are in addition to "done" etc. which are built in.

LOCAL=os.path.exists('local')
#controls whether debugging will stop the server or be skipped
from local_settings import *
#you should put the db settings in there.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS
STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS=(
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'processors.static_url_processor',
    )

MIDDLEWARE_CLASSES = (
    'general_middleware.PatchDebugMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'day',
    'django_extensions',
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

LOGIN_URL = '/admin/'

#the date you start using this.  everyone/thing from before this date doesn't have accurate time tracking.  
#and as you fill in old info, just set them to longago so that
#time sequence stuff doesn't get messed up if you added it out of order.
import datetime
LONG_AGO = datetime.date(year=2012, month=5, day=1)
LONG_AGO_STR= '2012-05-01'

#INCOMING_PHOTO_DIR is set in local.
assert os.path.exists(INCOMING_PHOTO_DIR),INCOMING_PHOTO_DIR
assert os.path.exists(DONE_PHOTO_DIR),DONE_PHOTO_DIR
assert os.path.exists(DELETED_PHOTO_DIR),DELETED_PHOTO_DIR
assert os.path.exists(DONE_PHOTO_DIR),DONE_PHOTO_DIR
assert os.path.exists(THUMB_PHOTO_DIR),THUMB_PHOTO_DIR

PHOTO_SCALED=750
THUMB_HEIGHT=120

DEFAULT_CURRENCIES=(('dollar','$',6.1),('rmb','rmb',1),)
DEFAULT_DOMAINS=('money','life','work','transportation','body','health','clothes','friends','fun','food','drink','alcohol',)
DEFAULT_REGIONS=(('home','rmb',),('new york','dollar'),('beijing','rmb'),('shanghai','rmb'),('internet','dollar'),)
DEFAULT_PRODUCTS=(('milk','drink',),('water','drink'),('chicken','food',),('vitamins','body',),('taxi','transportation',),('bike','transportation'),)
DEFAULT_PEOPLE=(('existence','the fact of',[],3),('father','',['existence'],1),('mother','',['existence',],2),)
DEFAULT_SOURCES=(('7-11','shanghai'),('corner store','shanghai'),('amazon','internet'),('starbucks','shanghai'))
DEFAULT_PHOTOTAGS='delete undelete done myphoto timelapse friends family meme background mosaic graphics painting done next last undo prev'.split()

TEMPLATE_DEBUG = True
EXCLUDE_FROM_PHOTOSET_TAGS=['done',]