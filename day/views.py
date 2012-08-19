# Create your views here.

import datetime

# Create your views here.

#from coffin.shortcuts import *
from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet)
from django.shortcuts import HttpResponseRedirect, HttpResponse
from trackerutils import *
from day.models import *
from buy.models import Person, Purchase
from trackerutils import name2hour

from forms import DayForm

def ajax_day_data(request):
    day_id=request.POST['day_id']
    day=Day.objects.get(id=day_id)
    vals={}
    vals['success']=True
    todo=request.POST.items()
    if 'tagnames' not in request.POST:
        todo.append(('tagnames',''))
    for k,v in todo:
        if k=='tagnames':
            newtags=v.split(',')
            exitags=day.tagdays.all()
            todelete=[]
            had=[]
            for td in exitags:
                had.append(td.tag.name)
                if td.tag.name in newtags:
                    continue
                else:
                    todelete.append(td)
            for td in todelete:
                td.delete()
            for nt in newtags:
                if not nt:continue
                if nt in had:
                    continue
                td=TagDay(day=day, tag=Tag.objects.get_or_create(name=nt)[0])
                td.save()
        elif k=='text':
            day.text=v
            day.save()
        elif k=='people_ids':
            day.text=v
            day.save()
        elif k=='day_id':
            continue
        else:
            print 'bad k',k
            continue
    vals['message']='success'
    return r2j(vals)

def gettoday():
    now=datetime.datetime.now()
    today=datetime.date(year=now.year, day=now.day, month=now.month)
    return today

def index(request):
    now=datetime.datetime.now()
    today=datetime.date(year=now.year, day=now.day, month=now.month)
    day, new=Day.objects.get_or_create(date=today)
    vals={}
    vals['day']=day
    vals['df']=DayForm()
    return r2r('jinja2/day.html',request, vals)

def today(request):
    
    today=gettoday()
    return HttpResponseRedirect('/day/%s'%str(today))
    #d,created=Day.objects.get_or_create(date=today)
    return aday(request, d)
    
def yesterday(request):
    today=gettoday()
    yesterday=today-datetime.timedelta(days=1)
    return HttpResponseRedirect('/day/%s'%str(yesterdaytoday))
    #d,created=Day.objects.get_or_create(date=yesterday)
    #return aday(request, d)

def y2day(request):
    dtoday=gettoday()
    y2day=dtoday-datetime.timedelta(days=2)
    return HttpResponseRedirect('/day/%s'%str(y2today))
    #d,created=Day.objects.get_or_create(date=yesterday)
    #return aday(request, d)
    
def aday(request, day):
    day=datetime.datetime.strptime(day, '%Y-%m-%d')
    day=Day.objects.get_or_create(date=day)[0]
    day.text=''
    day.save()
    dtoday=gettoday()
    vals={}
    vals['day']=day
    vals['recenttags']=Tag.objects.filter(created__gte=(dtoday-datetime.timedelta(days=30)))
    vals['alltags']=Tag.objects.all()
    vals['people']=Person.objects.all()
    vals['exipeople']=set([pd.person for pd in day.persondays.all()])
    vals['exitags']=[dt.tag for dt in day.tagdays.all()]
    
    vals['name2hour']=name2hour
    nextday=day.date+datetime.timedelta(days=1)
    vals['purchases']=Purchase.objects.filter(created__gte=day.date, created__lt=nextday).order_by('hour')
    return r2r('jinja2/day.html', request, vals)