import sys, os
sys.path.insert(1,'/home/ernop/django.fuseki.net/')
sys.path.insert(1,'/home/ernop/django.fuseki.net/tracker/')
sys.path.insert(1, '/home/ernop/django.fuseki.net/tracker/trackerenv/lib/python2.6/site-packages')
if sys.hexversion < 0x2060000: 
  print 'doing'
  os.execl("/home/ernop/django.fuseki.net/tracker/trackerenv/bin/python", "python2.6", *sys.argv)
  print 'did'
os.environ['DJANGO_SETTINGS_MODULE'] = "tracker.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
