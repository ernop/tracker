ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Ernie','ernestfrench@gmail.com',),
)
import os
LOCAL=os.path.exists('local')

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ=False

if LOCAL:
    DEBUG=True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'django_track',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD':'',
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      #WSGI Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'django_track',                      # Or path to database file if using sqlite3.
            'USER': 'djangotrack',                      # Not used with sqlite3.
            'PASSWORD':open('pw','r').read().strip(),
            'HOST': 'mysql.fuseki.net',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
    
MEDIA_ROOT = '/home/ernop/django.fuseki.net/public/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/ernop/django.fuseki.net/tracker/staticx'

if LOCAL:
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        'p:/proj/tracker/static',
    )
    SPARKLINES_DIR='p:/proj/tracker/static/sparklines'
else:
    STATICFILES_DIRS=(
        '/home/ernop/django.fuseki.net/tracker/static',
        )
    SPARKLINES_DIR='/home/ernop/django.fuseki.net/public/static/sparklines'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'vz(@$wgfooz%itxr8(vib2ck5w4m=d4iqt#u#+j!qdw2ta((!@'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zu6$ez2+__k@gqinbw0bgmsb&zu-44pl)r-+kh@ba-e%l$8nnf'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/ernie/proj/tracker/templates',
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='mail.fuseki.net'
EMAIL_PORT=26
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
SERVER_EMAIL='error@django.fuseki.net'#for my email error reports.
#SEND_BROKEN_LINK_EMAILS=True
DJANGO_BASE='/home/ernop/django.fuseki.net/tracker/'
