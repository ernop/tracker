import datetime, tempfile, os

from django.db import models
from django.conf import settings
SPAN_CHOICES=(('m','month'),('w','week'),('y','year'))
span2days={'w':7,'m':30,'y':365}

import logging
log=logging.getLogger(__name__)

class MyJsReplacementWorkout(models.Model):
    #def _media(self):
        #import ipdb;ipdb.set_trace()
        #js = (settings.MEDIA_URL + 'static/admin/js/admin/DateTimeShortcuts.js',)

    #media=property(_media)

    class Meta:
        app_label='workout'
        abstract=True

class MyJsReplacementBuy(models.Model):
    #def _media(self):
        #import ipdb;ipdb.set_trace()
        #js = (settings.MEDIA_URL + 'static/admin/js/admin/DateTimeShortcuts.js', settings.MEDIA_URL + 'static/js/DjangoAjax.js',)

    #media=property(_media)

    class Meta:
        app_label='buy'
        abstract=True

def gethour():
    hour=datetime.datetime.now().hour
    if hour<2:
        res= 'midnight'
    if hour<5:
        res='deep night'
    if hour<7:
        res='early morning'
    if hour<11:
        res='morning'
    elif hour<14:
        res='noon'
    elif hour<=20:
        res='evening'
    elif hour<=23:
        res='night'
    else:
        res='midnight'
    log.info('hour %d res %s',hour, res)

def savetmp(self):
    #import ipdb;ipdb.set_trace()
    out=tempfile.NamedTemporaryFile(dir=settings.SPARKLINES_DIR, delete=False)
    self.save(out,'png')
    print 'created',out.name
    os.chmod(out.name, 0644)
    return out

def get_named_hour():
    return hour2name[gethour()]


HOUR_CHOICES=zip(range(10), 'morning noon afternoon evening night midnight'.split())
HOUR_CHOICES.append((6,'early morning'))
hour2name={}
name2hour={}
for a in HOUR_CHOICES:
    hour2name[a[1]]=a[0]
    name2hour[a[0]]=a[1]