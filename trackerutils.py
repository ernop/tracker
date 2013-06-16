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
    def clink(self, text=None):
        if not text:            text=self
        return u'<a  style="white-space:nowrap;"  href="%s/workout/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

    def alink(self, text=None):
        if not text:            text=self
        return u'<a  style="white-space:nowrap;"  href="%s/workout/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)
    class Meta:
        app_label='workout'
        abstract=True

class BuyModel(models.Model):
    def clink(self, text=None):
        if not text:            text=self
        return u'<a  style="white-space:nowrap;"  href="%s/buy/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

    def alink(self, text=None):
        if not text:            text=self
        return u'<a  style="white-space:nowrap;"  href="%s/buy/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)
    class Meta:
        app_label='buy'
        abstract=True

class DayModel(models.Model):

    def clink(self, text=None):
        if not text:            text=self
        return u'<a class="btn"  style="white-space:nowrap;"  href="%s/day/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

    def alink(self, text=None):
        if not text:            text=self
        return u'<a class="btn"  style="white-space:nowrap;"  href="%s/day/%s/%d/">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)
    class Meta:
        app_label='day'
        abstract=True

class MyJsReplacementBuy(models.Model):
    #def _media(self):
        #js = (settings.MEDIA_URL + 'static/admin/js/admin/DateTimeShortcuts.js', settings.MEDIA_URL + 'static/js/DjangoAjax.js',)

    #media=property(_media)

    class Meta:
        app_label='buy'
        abstract=True

def gethour(hour=None):
    if not hour:
        hour=datetime.datetime.now().hour
    if hour<2:
        res= 'midnight'
    elif hour<5:
        res='deep night'
    elif hour<7:
        res='early morning'
    elif hour<11:
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




HOUR_CHOICES=zip([0,1,2,3,4,5], 'morning noon afternoon evening night midnight'.split())
HOUR_CHOICES.append((6, 'deep night'))
HOUR_CHOICES.append((7, 'early morning'))
hour2name={}
name2hour={}
for a in HOUR_CHOICES:
    name2hour[a[1]]=a[0]
    hour2name[a[0]]=a[1]

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



def purchase2obj(p):
    return {'id':p.id, 'name':p.product.name, 'quantity':p.quantity,
            'size':p.size,'cost':p.cost,'source':source2obj(p.source),
            'who_with':[per2obj(per) for per in p.who_with.all()],
            'note':p.note,
            'text':p.product.name,
            'product_id':p.product.id,}

def measurement2obj(m):
    return {'id':m.id, 'place_id':m.place.id, 'amount':m.amount,
            'name':m.place.name,'text':m.place.name,}

def per2obj(per):
    return {'id':per.id,'first_name':per.first_name,'last_name':per.last_name,'text':'%s %s'%(per.first_name, per.last_name),}

def source2obj(source):
    return {'id':source.id,'name':source.name,'text':source.name,}

def currency2obj(cur):
    return {'id':cur.id,'name':cur.name,'text':'%s %s'%(cur.symbol, cur.name),'symbol':cur.symbol,}