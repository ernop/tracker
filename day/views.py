import datetime

from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django import forms
from day.models import *

from trackerutils import *
from utils import *
from choices import *

import logging
log=logging.getLogger(__name__)

from forms import DayForm

def do_measurementset(request, measurementset_id=None):
    vals={}
    if request.method=='POST':
        formset=modelformset_factory(Measurement)
        ff=formset(request.POST)
        ff.save()
        #that's it!
        return HttpResponseRedirect('/admin/day/')
    else:
        ms=MeasurementSet.objects.get(id=measurementset_id)
        msids=[]
        for spot in ms.measurement_spots.all():
            m=Measurement(place=spot, created=datetime.datetime.now(), amount=0)
            m.save()
            msids.append(m.id)
        qs=Measurement.objects.filter(id__in=msids)
    formset=modelformset_factory(Measurement, extra=0)
    vals['formset']=formset(queryset=qs)
    return render_to_response('many.html',vals,RequestContext(request))

class WorkoutForm(forms.ModelForm):
    class Meta:
        model=ExWeight

def make_workout(request):
    vals={}
    vals['form']=WorkoutForm()
    return render_to_response('make_workout.html',vals,RequestContext(request))

@login_required
def ajax_day_data(request):
    vals={}
    vals['success']=True
    vals['message']='start.'
    todo=request.POST
    kind=request.POST['kind']
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
        log.error('Bad K %s',kind)
        import ipdb;ipdb.set_trace()
    vals['message']='success'
    return r2j(vals)

def gettoday():
    now=datetime.datetime.now()
    today=datetime.date(year=now.year, day=now.day, month=now.month)
    return today

@login_required
def index(request):
    now=datetime.datetime.now()
    today=datetime.date(year=now.year, day=now.day, month=now.month)
    day, new=Day.objects.get_or_create(date=today)
    vals={}

    vals['day']=day
    vals['df']=DayForm()
    return r2r('jinja2/day.html',request, vals)

@login_required
def today(request):
    today=gettoday()
    return HttpResponseRedirect('/aday/%s'%str(today))
    #d,created=Day.objects.get_or_create(date=today)
    return aday(request, d)

@login_required
def yesterday(request):
    today=gettoday()
    yesterday=today-datetime.timedelta(days=1)
    return HttpResponseRedirect('/day/%s'%str(yesterdaytoday))

@login_required
def y2day(request):
    dtoday=gettoday()
    y2day=dtoday-datetime.timedelta(days=2)
    return HttpResponseRedirect('/day/%s'%str(y2today))

@login_required
def aday(request, day):
    dtday=datetime.datetime.strptime(day, DATE_DASH_REV)
    vals={}
    #log.info('day is %s',day)
    vals['today']=day
    day,created=Day.objects.get_or_create(date=dtday)
    day.save()
    day=Day.objects.get_or_create(date=dtday)[0]
    dtoday=gettoday()
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
    from day.models import Product
    vals['products']=[{'id':p.id,'text':p.name} for p in Product.objects.all()]
    vals['sources']=[source2obj(s) for s in Source.objects.all()]
    vals['people']=[per2obj(p) for p in Person.objects.exclude(disabled=True).order_by('-rough_purchase_count')]
    vals['currencies']=[currency2obj(c) for c in Currency.objects.all()]
    vals['hour']=name2hour[gethour()]
    vals['hours'] = [{'id': id, 'name': name, 'text': name,} for name, id in name2hour.items()]
    from day.models import MeasuringSpot
    vals['measurement_places']=[{'id':p.id, 'name':p.name,'text':p.name,} for p in MeasuringSpot.objects.all()]

    #calculate histories
    trydate=dtday.date()
    histories=[]
    vals['histories']=histories
    while trydate>(settings.LONG_AGO-datetime.timedelta(days=365*20)):
        trydate=datetime.date(year=trydate.year-1,month=trydate.month,day=trydate.day)
        exi=Day.objects.filter(date=trydate)
        if exi.exists():
            day=exi[0]
            if day.has_any_history():
                histories.append(day)
    return r2r('jinja2/day.html', request, vals)

@login_required
def amonth(request, month):
    mm = datetime.datetime.strptime(month, DATE_DASH_REV)
    start = datetime.datetime(year=mm.year, month=mm.month, day=1)
    end = add_months(start, months=1)
    vals = {}
    vals['start'] = start
    vals['end'] = end
    vals['startshow'] = start.strftime(DATE_DASH_REV)
    vals['endshow'] = end.strftime(DATE_DASH_REV)
    bits = []
    monthtotal = 0
    FORCE_DOMAINS = 'alcohol life money transportation food drink recurring house life body clothes'.split()
    income=0
    for dd in Domain.objects.all():
        dinfo = dd.spent_history(start=start, end=end)
        if dd.name=='money':
            income=-1*dinfo['total_cost']
        if dd.name not in FORCE_DOMAINS and not dinfo['counts']:
            continue
        if dinfo['all_purchases_html']:
            summary = mkinfobox(title=dinfo['top_purchases_html'], content=dinfo['all_purchases_html'])
        else:
            summary = dinfo['top_purchases_html']
        bits.append([dd.name, str(int(dinfo['total_cost'])), '<a href="/admin/day/purchase/?created__month=%d&created__year=%d&product__domain__id=%d">%s</a>'% (start.month, start.year, dd.id, str(int(dinfo['total_quantity']))), summary])
        if dd.name!='money':
            monthtotal += dinfo['total_cost']
    domaintable = mktable(bits, rights=[1, 2], bigs=[1, 2])
    #purchases summary by domain
    measurements = Measurement.objects.filter(created__gte=start, created__lt=end).exclude(amount=None)
    spots = [MeasuringSpot.objects.get(id=ms) for ms in list(set([ms[0] for ms in measurements.values_list('place__id').distinct()]))]
    vals['spots'] = sorted(spots, key=lambda x:(x.domain.name, x.name))
    vals['days'] = [d for d in Day.objects.filter(date__gte=start, date__lt=end).order_by('-date') if d.notes.exists() or d.getmeasurements().exclude(amount=None).exists()]
    
    vals['domaintable'] = domaintable
    vals['month'] = mm
    vals['pastmonth'] = add_months(mm, -1)
    vals['nextmonth'] = add_months(mm, 1)
    vals['monthtotal'] = monthtotal
    #calc savings amount.
    saved=None
    saverate=None
    if income:
        saved=income-monthtotal
        saverate=round(saved*1.0/income*100.0,1)
    vals['saverate']=saverate
    vals['saved']=saved
    vals['projected_saving'] = monthtotal
    return r2r('jinja2/month.html', request, vals)

def mkinfobox(title, content):
    '''makes an html infobox which lists the title with a "more" button on the right that expands it inline and also hoveralbe'''
    #not implemented
    return title

@login_required
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

def simple_namefunc(person):
    res = ''
    if person.first_name:
        res += person.first_name[0].upper()
    if person.last_name:
        res += person.last_name[0].upper()
    return res

@login_required
def recent_connections(request, exclude_disabled=False):
    return people_connections(request, recent_only=True, exclude_disabled=True)

@login_required
def people_connections(request, exclude_disabled=False, recent_only=False):
    vals = {}
    people = Person.objects.all()
    if exclude_disabled:
        people = people.exclude(disabled=True)

    edges = []
    nodes = {}
    linked_ids = set()
    for person in people:
        if person.met_through.exists():
            for operson in person.met_through.all():
                edges.append({'target': operson.id, 'source': person.id, 'value': 1,})
            for operson in person.introduced_to.all():
                if recent_only and not operson.purchases.exists():
                    continue
                linked_ids.add(operson.id)
                linked_ids.add(person.id)
            if recent_only and not person.purchases.exists():
                continue
            linked_ids.add(person.id)
    for person in people:
        if recent_only and (not person.purchases.exists()) and person.id not in linked_ids:
            print 'skipping', person
            continue
        nodes[person.id] = person2obj(person)
    vals['nodes'] = nodes
    vals['edges'] = edges
    vals['recent_only'] = recent_only
    return r2r('jinja2/people_connections.html', request, vals)

def person2obj(person):
    return {'id': person.id,
                               'gender':person.gender,
                               'reflexive':False,
                               'left': True,
                               'right': False,
                               'name': person.d3_name(),
                               'created': person.created.strftime(DATE_DASH_REV),
                               'last_purchase': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).order_by('-created')[0].created.strftime(DATE_DASH_REV_DAY) or '2011-01-01',
                               'purchases_together': Purchase.objects.filter(who_with=person).count(),
                               'weight': 1,
                               'spent_together': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).aggregate(Sum('cost'))['cost__sum'] or 0,}

@login_required
def days(request):
    sixmonthago=datetime.datetime.now()-datetime.timedelta(days=180)
    total=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(created__gte=sixmonthago).aggregate(Sum('cost'))['cost__sum']
    ear=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).order_by('created')
    earliest=None
    if ear:
        earliest=datetime.datetime.combine(ear[0].created, datetime.time())
    else:
        return ''
    now=datetime.datetime.now()
    dayrange=(abs((now-earliest).days))+1
    return '%s%s<br>%s%s/day<br>(%d days)'%(rstripz(total), Currency.objects.get(id=1).symbol, rstripz(total/dayrange), Currency.objects.get(id=1).symbol, dayrange)
def redir(request):
    return HttpResponseRedirect('/today/')