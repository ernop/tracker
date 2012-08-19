import datetime, tempfile, os, json

from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.db import models
from django.conf import settings

SPAN_CHOICES=(('m','month'),('w','week'),('y','year'))
span2days={'w':7,'m':30,'y':365}

from django.template import RequestContext

import logging
log=logging.getLogger(__name__)

def monthago():
    return datetime.datetime.now()-datetime.timedelta(days=30)

class WorkoutModel(models.Model):
    def clink(self):
        return u'<a href="%s/workout/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    
    def alink(self):
        return u'<a href="%s/workout/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    class Meta:
        app_label='workout'
        abstract=True
        
class BuyModel(models.Model):
    def clink(self):
        return u'<a href="%s/buy/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    
    def alink(self):
        return u'<a href="%s/buy/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    class Meta:
        app_label='buy'
        abstract=True
        
class DayModel(models.Model):
    def clink(self):
        #import ipdb;ipdb.set_trace()
        return u'<a href="%s/day/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    
    def alink(self):
        return u'<a href="%s/day/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, self)
    class Meta:
        app_label='day'
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
    return res

def savetmp(self):
    out=tempfile.NamedTemporaryFile(dir=settings.SPARKLINES_DIR, delete=False)
    self.save(out,'png')
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
    
def r2r(template, request, context=None, lang=None):
    from django.conf import settings
    if not context:
        context={}
    from coffin.shortcuts import render_to_response
    context['request'] = request
    context['is_auth'] = request.user.is_authenticated()
    return render_to_response(template, context, RequestContext(request))

def r2s(template, context=None):
    from coffin.shortcuts import render_to_string
    #fake=FakeRequestContext(None, dict_=context)
    from django.conf import settings
    return render_to_string(template, dictionary=context)

def r2j(vals):
    return HttpResponse(json.dumps(vals), mimetype='text/html')

def debu(func, *args, **kwgs):
    def inner(*args, **kwgs):
        try:
            return func(*args, **kwgs)
        except Exception, e:
            log.error('exception %s',e)
            if settings.LOCAL:
                import ipdb;ipdb.set_trace()
            else:
                return 'Error <contact Ernie>'
            return func(*args, **kwgs)
            return None
    inner.__doc__=func.__doc__
    inner.__name__=func.__name__    
    return inner
