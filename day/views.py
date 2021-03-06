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
from personviews import person

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
            day=Day.objects.get(date=datetime.datetime.now().today())
            m=Measurement(spot=spot, created=datetime.datetime.now(), amount=0,day=day)
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
    
    vals['today']=day
    day,created=Day.objects.get_or_create(date=dtday)
    day.save()
    day=Day.objects.get_or_create(date=dtday)[0]
    dtoday=gettoday()
    vals['day']=day
    vals['daytitle'] = day.date.strftime('%A %B %d %Y')
    vals['recenttags']=Tag.objects.filter(created__gte=(dtoday-datetime.timedelta(days=30)))
    vals['exitags']=day.tags.all()
    vals['alltags']=Tag.objects.all()
    vals['exipeople']=set([pd.person for pd in day.persondays.all()])
    #vals['allpeople']=Person.objects.all()
    vals['allpeople']=[]
    vals['name2hour']=name2hour
    vals['notes']=day.notes.filter(deleted=False)
    vals['noteids']=[note.id for note in day.notes.filter(deleted=False).order_by('-created')]
    nextday=day.date+datetime.timedelta(days=1)
    vals['purchases']=Purchase.objects.filter(created__gte=day.date, created__lt=nextday).order_by('hour')
    vals['full_notekinds']=[{'id':n.id,'text':n.name} for n in NoteKind.objects.order_by('name')]
    vals['notekinds']=[n.name for n in NoteKind.objects.order_by('name')]
    vals['products']=[{'id':p.id,'text':p.name} for p in Product.objects.all()]
    vals['sources']=[source2obj(s) for s in Source.objects.all()]
    vals['regions']=[region2obj(r) for r in Region.objects.all()]
    vals['people']=[per2obj(p) for p in Person.objects.exclude(disabled=True).order_by('-rough_purchase_count')]
    vals['currencies']=[currency2obj(c) for c in Currency.objects.all()]
    vals['hour']=name2hour[gethour()]
    vals['hours'] = [{'id': id, 'name': name, 'text': name,} for name, id in name2hour.items()]
    vals['measurement_spots']=[{'id':p.id, 'name':p.name,'text':p.name,} for p in MeasuringSpot.objects.all()]
    #from utils import ipdb;ipdb()
    #calculate histories
    trydate=add_months(dtday.date(),months=12)
    #should include the current year! duh.
    histories=[]
    vals['histories']=histories
    while trydate>(settings.LONG_AGO-datetime.timedelta(days=365*20)):
        trydate=datetime.date(year=trydate.year-1,month=trydate.month,day=trydate.day)
        exi=Day.objects.filter(date=trydate)
        if exi.exists():
            day=exi[0]
            if day.has_any_history():
                histories.append(day)
    #vals['anniversary_photos']=day.get_photos_of_day(user=request.user)
    return r2r('jinja2/day.html', request, vals)


@login_required
def previous_year(request,dt = None):
    if dt == None:
        today = datetime.datetime.today().date().strftime(DATE_DASH_REV)
        return HttpResponseRedirect('/prevyear/%s'%str(today))
    mm = datetime.datetime.strptime(dt, DATE_DASH_REV)
    end = datetime.datetime(year=mm.year, month=mm.month, day=mm.day)
    start = add_months(end, months=-12)
    return summary_timespan(start,end,request,include_people=False,include_measurements=False,include_days=False,include_span_tags=False,top_purchases_count=10,
                            include_permonth=True)

@login_required
def previous_month(request,dt = None):
    if dt == None:
        today = datetime.datetime.today().date().strftime(DATE_DASH_REV)
        return HttpResponseRedirect('/prevmonth/%s'%str(today))
    else:
        mm = datetime.datetime.strptime(dt, DATE_DASH_REV)
    end = datetime.datetime(year=mm.year, month=mm.month, day=mm.day)
    start = add_months(end, months=-1)
    return summary_timespan(start,end,request)

@login_required
def themonth(request, dt = None):
    if dt == None:
        today = datetime.datetime.today().date().strftime(DATE_DASH_REV)
        return HttpResponseRedirect('/themonth/%s'%str(today))
    else:
        mm = datetime.datetime.strptime(dt, DATE_DASH_REV)
    start = datetime.datetime(year=mm.year, month=mm.month, day=1)
    #"starts" the last day of the previous month
    end = add_days(add_months(start, months=1), days = -1)
    return summary_timespan(start,end,request, include_start = True)

@login_required
def theyear(request,dt = None):
    if dt == None:
        today = datetime.datetime.today().date().strftime(DATE_DASH_REV)
        return HttpResponseRedirect('/theyear/%s'%str(today))
    else:
        mm = datetime.datetime.strptime(dt, DATE_DASH_REV)
    start = datetime.datetime(year=mm.year, month=1, day=1)
    end = add_months(start, months=12)
    return summary_timespan(start,end,request,include_people=True,include_measurements=False,include_days=False,include_span_tags=False,top_purchases_count=10,
                            include_permonth=True)

def alltime(request):
    start = settings.LONG_AGO
    end = datetime.datetime.now()
    return summary_timespan(start,end,request,include_people=False,include_measurements=False,include_days=False,include_span_tags=False,top_purchases_count=15)
    

def summary_timespan(start,end,request,
                     include_people=True,
                     include_measurements=True,
                     include_days=True,
                     include_span_tags=True,
                     top_purchases_count=12,
                     include_permonth=False,
                     include_d3_people=True,
                     include_ages=True,
                     include_origins=False,
                     include_start = False  #whether to include first day.
                     ):
    vals = {}
    vals['start'] = start
    vals['end'] = end
    vals['startshow'] = start.strftime(DATE_DASH_REV_DAY)
    vals['endshow'] = end.strftime(DATE_DASH_REV_DAY)
    vals['include_permonth'] = True
    try:
        dd=Day.objects.get(date=end)
    except Day.DoesNotExist:
        dd=Day(created=datetime.datetime.now(), date=end)
        dd.save()
    vals['day']=dd
    bits = []
    if include_permonth:
        bits.append(['domain','per month','total','purchs','top'])
    monthtotal = 0
    monthtotalreal = 0
    FORCE_DOMAINS = 'alcohol life money transportation food drink recurring house life body clothes'.split()
    income=0
    expenses_by_essentiality = {'none': 0,}
    for ess in Essentiality.objects.all():
        expenses_by_essentiality[ess.name] = 0
    expenses_unknown_count = 0
    for dd in Domain.objects.all():
        if include_start:
            use_start = add_days(start, -1)
        else:
            use_start = start
        dinfo = dd.spent_history(start = use_start, end=end, top_purchases_count=top_purchases_count)
        if dd.name=='money':
            income=-1*dinfo['total_cost']
        if dd.name not in FORCE_DOMAINS and not dinfo['counts']:
            continue
        if dinfo['all_purchases_html']:
            summary = mkinfobox(title=dinfo['top_purchases_html'], content=dinfo['all_purchases_html'])
        else:
            summary = dinfo['top_purchases_html']
        guy=[dd.clink(skip_btn = True), str(int(dinfo['total_cost'])), '<a href="/admin/day/purchase/?created__month=%d&created__year=%d&product__domain__id=%d">%s</a>'% (start.month, start.year, dd.id, str(int(dinfo['purchase_count']))), summary]
        if include_permonth:
            val=int(dinfo['total_cost'])/12
            guy.insert(1, val)
        bits.append(guy)
        if dd.name!='money':
            monthtotal += dinfo['total_cost']
            for purch in dinfo['purchases']:
                if purch.essentiality is not None:
                    expenses_by_essentiality[purch.essentiality.name] = expenses_by_essentiality[purch.essentiality.name] + purch.get_cost()
                else:
                    expenses_by_essentiality['none'] = expenses_by_essentiality['none'] + purch.get_cost()
                    expenses_unknown_count += 1
            if dd.name not in ['tax','recurring',]:
                monthtotalreal += dinfo['total_cost']
    domaintable = mktable(bits, rights=[1, 2], bigs=[1, 2])
    vals['domaintable'] = domaintable
    #purchases summary by domain
    if include_measurements:
        measurements = Measurement.objects.filter(created__gt=use_start, created__lte=end).exclude(amount=None)
        spots = [MeasuringSpot.objects.get(id=ms) for ms in list(set([ms[0] for ms in measurements.values_list('spot__id').distinct()]))]
        vals['spots'] = sorted(spots, key=lambda x:(x.domain.name, x.name))
    else:
        vals['spots']=[]
    # if d.notes.exists() or d.getmeasurements().exclude(amount=None).exists()
    if include_days:
        vals['days'] = [d for d in Day.objects.filter(date__gt = use_start, date__lte=end).order_by('-date')]
    else:
        vals['days']=[]
    vals['month'] = start
    vals['pastmonth'] = add_months(start, -1)
    vals['nextmonth'] = add_months(start, 1)
    vals['monthtotal'] = monthtotal
    #calc savings amount.
    saved=0
    saverate=0
    if income:
        saved=income-monthtotal
        saverate=round(saved*1.0/income*100.0,1)
    vals['saverate']=saverate
    vals['saved']=saved
    vals['salaryshow']='%0.1f'%(round(income/100)/10.0)
    vals['expensesshow']='%0.1f'%(round(monthtotal/100)/10.0)
    vals['realexpensesshow']='%0.1f'%(round(monthtotalreal/100)/10.0)
    vals['savedshow']='%0.1f'%(round(saved/100)/10.0)
    vals['projected_saving'] = monthtotal
    
    #calculating amounts.
    vals['expenses_vital'] = expenses_by_essentiality['0 - vital']
    vals['expenses_important'] = expenses_by_essentiality['1 - important']
    vals['expenses_major'] = expenses_by_essentiality['2 - major']
    vals['expenses_fun'] = expenses_by_essentiality['3 - fun'] 
    vals['expenses_waste'] = expenses_by_essentiality['4 - waste']
    vals['expenses_unknown'] = expenses_by_essentiality['none']
    for k in 'expenses_vital expenses_important expenses_major expenses_fun expenses_waste expenses_unknown'.split():
        vals[k] = '%0.0f' % (vals[k])
    vals['expenses_unknown_link'] = '<a href="../../admin/day/purchase/?created__month=%d&created__year=%d&essentiality__isnull=True">%d</a>' % (vals['day'].date.month, vals['day'].date.year, expenses_unknown_count)
    
    vals['met_with_age_count']=None
    vals['metagerageage']=None
    vals['month_with_age_count']=None
    vals['monthaverageage']=None
    vals['monthaverage_raw']=None    
    origins={}
    vals['origins']=origins
    if include_people:
        vals['metpeople']=Person.objects.filter(created__lte=end,created__gt=start)
        data=average_age(vals['metpeople'], asof=start)
        vals['met_with_age_count']=data['people_included_count']
        vals['metaverageage']='%0.1f'%(data['average_age'] or 0)
        vals['monthpeople']=Person.objects.filter(purchases__created__lte=end,purchases__created__gt=start)
        vals['monthpeople']=vals['monthpeople']|vals['metpeople']
        vals['monthpeople']=vals['monthpeople'].distinct().order_by('-rough_purchase_count')
        
        for pp in vals['monthpeople']:
            pp.update_purchase_count()
        for pp in vals['monthpeople']:
            if pp in vals['metpeople']:
                pp.newperson=True
            else:
                pp.newperson=False
            pp.month_purchase_count=Purchase.objects.filter(created__gt=start,created__lte=end,who_with=pp).count()
            
            if pp.origin:
                if pp.origin in origins:
                    oldpeople=origins[pp.origin]
                    if pp not in oldpeople:
                        oldpeople.append(pp)
                    origins[pp.origin]=oldpeople
                else:
                    origins[pp.origin]=[pp,]
        vals['origins_counted']=sum([len(v) for k,v in origins.items()])
        vals['len']=len
        for k,v in origins.items():
            v.sort(key=lambda x:x.rough_purchase_count and x.rough_purchase_count*-1 or 0)
        origins_list=sorted(origins.items(), key=lambda x:len(x[1])*-1)
        vals['origins']=origins_list
        vals['monthpeople']=[pp for pp in vals['monthpeople']]
        ppls=[(person, person.month_purchase_count,) for person in vals['monthpeople'] if person.month_purchase_count>0]
        data=weighted_average_age(ppls, asof=start)
        vals['month_with_age_count']=data['people_included_count']
        vals['monthaverageage']='%0.1f'%(data['average_age'] or 0)
        raw_ppls=[pp[0] for pp in ppls]
        unweighted_data=average_age(raw_ppls, asof=start)
        vals['monthaverage_raw']='%0.1f'%(unweighted_data['average_age'] or 0)
        vals['monthpeople'].sort(key=lambda x:-1*x.month_purchase_count)
    else:
        vals['monthpeople']=[]
    if include_span_tags:
        vals['span_tags']=get_span_tags(start,end,user=request.user)
    else:
        vals['span_tags']=[]
    now=datetime.datetime.today().date()
    if type(start) is not datetime.date:
        start=start.date()
    people_connections_data=people_connections(request, since=start, until=end, exclude_disabled=True, data_only=True)        
    vals.update(people_connections_data)
    return r2r('jinja2/timespan_summary.html', request, vals)

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
    now=datetime.datetime.today().date()
    yearago=datetime.date(month=now.month,day=now.day,year=now.year-1)
    return people_connections(request, since=yearago, exclude_disabled=True)

@login_required
def month_connections(request, exclude_disabled=False):
    now=datetime.datetime.today().date()
    return people_connections(request, since=now-datetime.timedelta(days=30), exclude_disabled=True)



@login_required
def initial_annual(request):
    now=datetime.datetime.today().date()
    yearago=datetime.date(month=now.month,day=now.day,year=now.year-1)
    return people_connections(request,detail_level='initials',since=yearago)

@login_required
def anon_annual(request):
    now=datetime.datetime.today().date()
    yearago=datetime.date(month=now.month,day=now.day,year=now.year-1)
    return people_connections(request,detail_level='anon',since=yearago)


@login_required
def people_connections(request, exclude_disabled=False, since=None, until=None, detail_level=None,
                       data_only=False):
    if type(until) is datetime.datetime:
        until=until.date()
    if not detail_level:
        detail_level='short name'
    vals = {}
    people = Person.objects.all()
    if exclude_disabled:
        people = people.exclude(disabled=True)
    edges = []
    nodes = {}
    linked_ids = set()
    #the ones who really should be highlighted here.
    
    supporting_linked_ids=set()
    #just linkers, included because there was action in ppl they introduced me to.
    
    ID=45299
    newly_created=set()
    purch_existed=set()
    
    for person in people:
        if person.id==ID:
            from util import ipdb;ipdb()
        #include them if they've got purch in the last year, or they introduced me to sb in the last year.
        if since and person.created>since and ((not until) or person.created<=until):
            #at some point should also include them if they're in a new phototag.
            newly_created.add(person.id)
        if since:
            if until:
                if person.purchases.filter(created__gt=since).filter(created__lte=until).exists():
                    purch_existed.add(person.id)                
            else:
                if person.purchases.filter(created__gt=since).exists():
                    purch_existed.add(person.id)
        else:
            purch_existed.add(person.id)
        
            #also add the person who introduced me.
    for person in people:
        if person.id in newly_created or person.id in purch_existed:
            for from_person in person.met_through.all():
                if from_person.id==ID:
                    from util import ipdb;ipdb()
                supporting_linked_ids.add(from_person.id)
    for person in people:
        if person.id==ID:
            from util import ipdb;ipdb()
        #ordering matters.  default is supporting, then is purch existed
        #then is newly created in green.
        if person.id in supporting_linked_ids:
            nodes[person.id]=person2obj(person,kind=detail_level)
            nodes[person.id]['newly_created']=False
            nodes[person.id]['supporting']=True
        #make edges for these.
        if person.id in purch_existed or person.id in newly_created:
            for from_person in person.met_through.all():
                #only include edges where both poeple are mentioned.
                edges.append({'target': from_person.id, 'source': person.id, 'value': 1,})
        if person.id in purch_existed: #and (not person.purchases.exists()) 
            nodes[person.id] = person2obj(person,kind=detail_level)
            nodes[person.id]['newly_created']=False
            nodes[person.id]['supporting']=False
        if person.id in newly_created: #and (not person.purchases.exists()) 
            nodes[person.id] = person2obj(person,kind=detail_level)
            nodes[person.id]['newly_created']=True
            nodes[person.id]['supporting']=False
        if not since:
            nodes[person.id]['newly_created']=False
            nodes[person.id]['supporting']=True
    vals['nodes'] = nodes
    vals['edges'] = edges
    if data_only:
        return vals
    return r2r('jinja2/people_connections.html', request, vals)

def person2obj(person, kind=None):
    if not kind:
        kind='full'
    dat={'id': person.id,
            'gender':person.gender,
            'reflexive':False,
            'left': True,
            'right': False,
            'name': person.short_name(),
            'created': person.created.strftime(DATE_DASH_REV),
            'last_purchase': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).order_by('-created')[0].created.strftime(DATE_DASH_REV_DAY) or '2011-01-01',
            'purchases_together': Purchase.objects.filter(who_with=person).count(),
            'weight': 1,
            'spent_together': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).aggregate(Sum('cost'))['cost__sum'] or 0,}
    if kind=='supporting':
        dat['name']=person.initial()
    elif kind=='anon':
        dat['name']=''
        dat['gender']=1
    elif kind=='initials':
        dat['name']=person.initial()
    elif kind=='extended':
        dat['name']=unicode(person)
    elif kind=='short name':
        #the default.
        pass
    else:
        from util import ipdb;ipdb()
    return dat

@login_required
def days(request):
    sixmonthago=datetime.datetime.now()-datetime.timedelta(days=180)
    total=sum([pur.get_cost() for pu in Purchase.objects.filter(created__gte=sixmonthago)])
    ear=Purchase.objects.order_by('created')
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

def logout(request):
    from django.contrib.auth import logout
    from utils import ipdb;ipdb()
    logout(request)

@login_required
def summaries(request):
    vals={}
    for key, queryset, field in [('source', Source.objects.all(), 'created', ),
                                  ('people', Person.objects.all(), 'created', ),
                                  ('product', Product.objects.all(), 'created', )]:
        res = {}
        mindate = datetime.datetime.strptime(settings.LONG_AGO_STR, DATE).date()
        for obj in queryset:
            date = obj.created.strftime(DATE)
            res[date] = res.get(date, 0) + 1
            mindate = min(mindate, obj.created)
        res2=group_day_dat(res, by = 'month', mindate=mindate)
        width = 1200
        height = 300
        line = sparkline(res2, width, height, kind = 'bar')
        vals[key] = line
    
    return r2r('jinja2/summaries.html', request, vals)

@login_required
def timeline(request):
    vals={}
    vals['people'] = partition_queryset(Person.objects.all(), by = 'week', field = 'created', skip_first = True, order_by = '-rough_purchase_count')
    vals['source'] = partition_queryset(Source.objects.all(), by = 'week', field = 'created', skip_first = True)
    vals['product'] = partition_queryset(Product.objects.all(), by = 'week', field = 'created', skip_first = True)
    #ordered
    
    vals['keys'] = sorted(vals['people'].keys())
    vals['regions'] = {}
    vals['purchases'] = {}
    for k in vals['keys']:
        purchases = Purchase.objects.filter(day__date__gte = k, day__date__lt = vals['people'][k]['end'])
        pids = [p.id for p in purchases]
        sources = Source.objects.filter(purchases__id__in = pids)
        #regions = Region.objects.filter(source__purchases__id__in = pids)
        counts = {}
        for source in sources:
            if not source.region:continue
            counts[source.region] = counts.get(source.region, 0) + 1
        regionqs = [kk.clink(text = '%s (%d)' % (kk.name, vv)) for kk, vv in sorted(counts.items(), key = lambda x:-1 *x[1])]
        vals['regions'][k] = {'queryset': regionqs}
        vals['purchases'][k] = {'count': purchases.count()}
    
    return r2r('jinja2/newtimeline.html', request, vals)

def partition_queryset(queryset, by=None, mindate=None, field = None,
                       enddate = None, skip_first = False, order_by = None):
    if enddate == None:
        enddate = datetime.date.today()
    from choices import DATE,MONTH_YEAR,YEAR_MONTH
    if not mindate:
        mindate = settings.LONG_AGO
        if skip_first:
            mindate = mindate + datetime.timedelta(days = 7)
    if type(mindate)==datetime.date:
        mindate=datetime.datetime.strftime(mindate, DATE)
    adder_day=0
    adder_month=0
    adder_year=0
    first=datetime.datetime.strptime(mindate, DATE)
    now=datetime.datetime.now()
    start=mindate
    
    if not by:
        by='day'
    if by=='day':
        adder_day=1
        #move start back to the monday
        first=first.date()
    elif by=='week':
        adder_day=7
        #move start back to the monday
        while first.weekday()!=6:
            first=first-datetime.timedelta(days=1)
        first=first.date()
    elif by=='month':
        adder_month=1
        #move start back to the 1st of the month
        first=datetime.date(year=first.year,month=first.month,day=1)
    elif by=='year':
        adder_month=12
        #move start back to jan 1
        first=datetime.date(year=first.year,month=1,day=1)
    
    #start correctly defined, and the interval defined.    
    trying=first
    res = {}
    thisinterval_start=trying
    
    while 1:
        next_interval_start = add_months(thisinterval_start,adder_month)+datetime.timedelta(days=adder_day)
        ft = {field + '__gt' : thisinterval_start, field + '__lte' : next_interval_start }
        key = thisinterval_start.strftime(DATE_DASH_REV)
        qs = queryset.filter( **ft)
        if order_by:
            qs = qs.order_by(order_by)
        res[key] = {'start':thisinterval_start , 'end':next_interval_start, 'queryset': qs}
        thisinterval_start = next_interval_start
        if thisinterval_start > enddate:
            break
    return res