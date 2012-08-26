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
import logging
log=logging.getLogger(__name__)
from forms import DayForm
@debu
def ajax_day_data(request):
    log.info(request.POST)
    vals={}
    vals['success']=True
    vals['message']='start.'
    todo=request.POST
    kind=request.POST['kind']
    #import ipdb;ipdb.set_trace()
    if kind=='tagnames':
        day_id=request.POST['day_id']
        day=Day.objects.get(id=day_id)
        newtags=v.split(',')
        exitags=day.tags.all()
        todelete=[]
        had=[]
        for tag in exitags:
            had.append(tag.name)
            if tag.name in newtags:
                continue
            else:
                day.tags.remove(tag)
        for nt in newtags:
            if not nt:continue
            if nt in had:
                continue
            tag=Tag.objects.get_or_create(name=nt)[0]
            day.tags.add(tag)
            #td=TagDay(day=day, tag=Tag.objects.get_or_create(name=nt)[0])
            #td.save()
    elif kind=='note_text':
        note_id=todo['note_id']
        if note_id=='new':
            note=Note(day_id=todo['day_id'])
            vals['message']+=' created.'
        else:
            note=Note.objects.get(pk=int(note_id))
        note.text=todo['note_text']
        note.save()
        vals['note_id']=note.id
        if not note.text and not note.kinds.count():
            note.delete()
            vals['message']+=' deleted.'
            vals['deleted']=True
    elif kind=='peoplenames':
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
    elif kind=='notekind':
        if todo['note_id']=='new':
            note=Note(day_id=int(todo['day_id']))
            vals['message']+=' created.'
            note.save()
        else:
            note=Note.objects.get(id=todo['note_id'])
        nks=NoteKind.objects.filter(id__in=[int(th) for th in todo['notekind_ids'].split(',') if th])
        for rel in note.kinds.all():note.kinds.remove(rel)
        for n in nks:note.kinds.add(n)
        note.save()
        vals['note_id']=note.id
        if not note.text and not note.kinds.count():
            note.delete()
            vals['message']+=' deleted.'
            vals['deleted']=True
    else:
        print 'bad k',k
        import ipdb;ipdb.set_trace()
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
    return HttpResponseRedirect('/aday/%s'%str(today))
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
    dtday=datetime.datetime.strptime(day, '%Y-%m-%d')
    day,created=Day.objects.get_or_create(date=dtday)
    day.save()
    day=Day.objects.get_or_create(date=dtday)[0]
    dtoday=gettoday()
    vals={}
    vals['day']=day
    
    vals['recenttags']=Tag.objects.filter(created__gte=(dtoday-datetime.timedelta(days=30)))
    vals['exitags']=day.tags.all()
    
    vals['alltags']=Tag.objects.all()
    
    vals['exipeople']=set([pd.person for pd in day.persondays.all()])
    vals['allpeople']=Person.objects.all()
    vals['allpeople']=[]
    vals['name2hour']=name2hour
    vals['notes']=day.notes.all()
    nextday=day.date+datetime.timedelta(days=1)
    vals['purchases']=Purchase.objects.filter(created__gte=day.date, created__lt=nextday).order_by('hour')
    vals['full_notekinds']=[{'id':n.id,'text':n.name} for n in NoteKind.objects.order_by('name')]
    vals['notekinds']=[n.name for n in NoteKind.objects.order_by('name')]
    #vals['notekind_list']
    return r2r('jinja2/day.html', request, vals)

def notekind(request, id=None, name=None):
    if id:
        nk=NoteKind.objects.get(id=id)
    elif name:
        nk=NoteKind.objects.get(name=name)
    else:
        assert False
    vals={}
    vals['nk']=nk
    vals['notes']=nk.notes.all().order_by('-day__date')
    vals['allnks']=NoteKind.objects.all()
    return r2r('jinja2/notekind.html', request, vals)