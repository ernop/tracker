import datetime, tempfile, os

from django.db import models
from django.conf import settings

class MyJsReplacementWorkout(models.Model):
    class Media:
        js = (settings.MEDIA_URL + 'static/admin/js/admin/DateTimeShortcuts.js',)    
        
    class Meta:
        app_label='workout'
        abstract=True
        
class MyJsReplacementBuy(models.Model):
    class Media:
        js = (settings.MEDIA_URL + 'static/admin/js/admin/DateTimeShortcuts.js',)    
        
    class Meta:
        app_label='buy'
        abstract=True
        
def gethour():
    hour=datetime.datetime.now().hour
    if hour<2:
        return 'midnight'
    if hour<5:
        return 'deep night'
    if hour<7:
        return 'early morning'
    if hour<11:
        return 'morning'
    elif hour<14:
        return 'noon'
    elif hour<=20:
        return 'evening'
    elif hour<=23:
        return 'night'
    return 'midnight'

def savetmp(self):
    out=tempfile.NamedTemporaryFile(dir=settings.SPARKLINES_DIR, delete=False)
    self.save(out,'png')
    print 'created',out.name
    os.chmod(out.name, 0644)
    return out

def get_named_hour():
    return hour2name[gethour()]


HOUR_CHOICES=zip(range(10), 'morning noon afternoon evening night midnight'.split())
hour2name={}
name2hour={}
for a in HOUR_CHOICES:
    hour2name[a[1]]=a[0]
    name2hour[a[0]]=a[1]