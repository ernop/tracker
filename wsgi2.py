import os, sys
sys.path.insert(0, '/home/ernie/tracker/')
sys.path.insert(0, '/home/ernie/tracker/day/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/ernop/eggs/.python-eggs")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
