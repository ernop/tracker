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

class DayModel(models.Model):
    
    #should add default modified & created here.

    def clink(self, text=None,wrap=True,skip_btn=False):
        if skip_btn:
            klass=''
        else:
            klass='btn'
        if wrap:
            wrap=' nb'
        else:
            wrap=''
        if not text:
            text=self
        return u'<a class="%s%s" href="%s/day/%s/?id=%d">%s</a>'%(klass, wrap, settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

    def alink(self, text=None,wrap=True):
        if wrap:
            wrap=' nb'
        else:
            wrap=''
        if not text:
            text=self
        return u'<a class="btn btn-default" href="%s/day/%s/%d/">%s</a>'%(wrap,settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

    class Meta:
        app_label='day'
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
    #log.info('hour %d res %s',hour, res)
    return res

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
    return {'id':p.id,
            'name':p.product.name,
            'quantity':p.quantity,
            'cur_symbol': p.currency.symbol,
            'size':p.size,
            'cost':p.cost,  #ok not to use get_cost here because it includes currency.
            'source':source2obj(p.source),
            'who_with':[per2obj(per) for per in p.who_with.all()],
            'note':p.note,
            'text':p.product.name,
            'product_id':p.product.id,
            'hour': hour2name[p.hour],}

def measurement2obj(m):
    return {'id':m.id, 'spot_id':m.spot.id, 'amount':m.amount,
            'name':m.spot.name,'text':m.spot.name,'domain_id':m.spot.domain.id,'domain_name':m.spot.domain.name}

def per2obj(per):
    return {'id':per.id,'first_name':per.first_name,'last_name':per.last_name,'text':'%s %s'%(per.first_name, per.last_name),}

def source2obj(source):
    return {'id':source.id,'name':source.name,'text':source.name,}

def currency2obj(cur):
    return {'id':cur.id,'name':cur.name,'text':'%s %s'%(cur.symbol, cur.name),'symbol':cur.symbol,}

def mktable(dat, rights=None, bigs=None, skip_false=False, nb=False):
    rows = []
    for row in dat:
        if not row:
            continue
        if type(row) not in [list, set, tuple]:
            row=[row,]
        if skip_false and not row[-1]:
            continue
        res = '<tr>'
        for ii, thing in enumerate(row):
            klasses = []
            if nb:
                klasses.append('nb')
            if rights and ii in rights:
                klasses.append('right')
            if bigs and ii in bigs:
                klasses.append('big')
            if klasses:
                res += '<td class="%s">%s</td>' % (' '.join(klasses), thing)
            else:
                res += '<td>%s</td>' % (thing)
        rows.append(res+'</tr>')
    return '<table class="table thintable" style="background-color:white;">%s</table>' % ''.join(rows)


def div(klass=None,contents=None):
    klasszone=''
    if klass:
        klasszone='class="%s"'%klass
    res='<div %s>%s</div>'%(klasszone,contents)
    return res