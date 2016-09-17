# Create your views here.

import datetime,uuid

# Create your views here.

#from coffin.shortcuts import *
from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet)
from django.shortcuts import HttpResponseRedirect, HttpResponse
from trackerutils import *
from day.models import *
from trackerutils import *
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from utils import *
from choices import *
log=logging.getLogger(__name__)
from forms import DayForm

@user_passes_test(staff_test)
def ajax_get_data(request):
    try:
        data=request.POST.dict()
        kind=data['kind']
        action=data['action']
        #kind2klass={'note':Note, }
        if kind=='note':
            if action=='new':
                day=Day.objects.get(id=data['day_id'])
                guy=Note(day=day)
                guy.save()
                html=guy.as_html()
                res={'success':True,'html':html,'message':None}
            elif action=='delete':
                guy=Note.objects.get(id=data['id'])
                guy.deleted=True
                guy.save()
                res={'success':True,'message':'deleted','note_id':data['id']}
            elif action=='get':
                guy=Note.objects.get(id=data['id'])
                html=guy.as_html()
                res={'success':True,'html':html,'message':None}
        elif kind=='person':
            if action=='new':
                exiperson=Person.objects.filter(first_name=data['first_name'],last_name=data['last_name'])
                if exiperson.exists():
                    person=exiperson[0]
                    res={'success':True,'person_id':person.id,'message':'person already existed'}
                else:
                    if 'gender' not in data or not data['gender']:
                        res={'success':False,'message':'needs gender'}
                        return r2j(res)
                    gender=gender2id(data['gender'])
                    if not 'met_through' in data or not data['met_through']:
                        res={'success':False,'message':'needs met through'}
                        return r2j(res)
                    person=Person(first_name=data['first_name'],last_name=data['last_name'],gender=gender)
                    person.save()
                    through=Person.objects.get(id=data['met_through'])
                    person.met_through.add(through)
                    
                    #only need to send new data, other stuff is wrapped.
                    res={'success':True,'person_id':person.id,'message':'created %s'%person}
        elif kind=='source':
            if action=='new':
                if 'name' not in data or not data['name']:
                    res={'success':False,'message':'needs name'}
                    return r2j(res)
                exisource=Source.objects.filter(name=data['name'])
                if exisource.exists():
                    source=exisource[0]
                    res={'success':True,'source_id':source.id,'message':'source already existed'}
                else:
                    region=Region.objects.get(id=data['region_id'])
                    source=Source(name=data['name'],region=region)
                    source.save()
                    res={'success':True,'source_id':source.id,'message':'created %s'%source}
        return r2j(res)
    except Exception,e:
        from utils import ipdb;ipdb()
        tb=traceback.format_exc(e)
        res={'success':False,'message':'error: %s<div class="pre">%s</div>%s'%(e,tb,data)}
        return r2j(res)

@user_passes_test(staff_test)
def ajax_serve_mp3(request,mp3_filename):
    fn=make_safe_filename(mp3_filename)
    fp=os.path.join(settings.MP3_DIR,fn)
    assert os.path.exists(fp),fp
    data=open(fp,'rb')
    resp=HttpResponse(content=data.read(), mimetype="audio/mpeg")
    return resp

@user_passes_test(staff_test)
def ajax_receive_mp3(request, note_id):
    fn=str(uuid.uuid4())+'.mp3'
    fp=os.path.join(settings.MP3_DIR,fn)
    while os.path.exists(fp):
        fn=str(uuid.uuid4())
        fp=os.path.join(settings.MP3_DIR,fn)
    note=Note.objects.get(id=note_id)
    note.mp3path=fn
    note.save()
    out=open(fp,'wb')
    import base64
    
    data = request.POST['data']
    data2 = base64.decodestring(data[22:])
    out.write(data2)
    out.close()
    log.info('outfp for saved mp3 is %s',fp)
    return r2j({'success':True,'message':'okay'})
    
        
    

@user_passes_test(staff_test)
def ajax_get_purchases(request):
    day=request.POST['today']
    day=datetime.datetime.strptime(day, DATE)
    ps=Purchase.objects.filter(created__year=day.year, created__month=day.month, created__day=day.day)
    res={'success':True, 'message':'got', 'purchases':[purchase2obj(p) for p in ps]}
    return r2j(res)

@user_passes_test(staff_test)
def ajax_get_popular(request):
    '''only show sources which have more than 2...'''
    res = {}
    if 'product_id' in request.POST:
        product_id = request.POST['product_id']
        purches = Purchase.objects.filter(product__id=product_id)
    elif 'source_id' in request.POST:
        source_id = request.POST['source_id']
        purches = Purchase.objects.filter(source__id=source_id)
    else:
        import ipdb;ipdb.set_trace()
    prices = {}
    products = {}
    sources = {}
    who_with= {}
    hours= {}
    for p in purches:
        cost = round(p.get_cost(), 1)
        prices[cost] = prices.get(cost, 0) + 1
        sources[p.source] = sources.get(p.source, 0) + 1
        products[p.product] = products.get(p.product, 0) + 1

        for who in p.who_with.all():
            who_with[who] = who_with.get(who, 0) + 1
        hours[p.hour] = hours.get(p.hour, 0) + 1

    res['prices'] = [k for k in sorted(prices.items(), key=lambda x:-1*x[1])  if k[1] > 1]
    res['sources'] = [((k[0].name, k[0].id), k[1]) for k in sorted(sources.items(), key=lambda x:-1*x[1]) if k[1] > 1]
    res['products'] =[((k[0].name, k[0].id), k[1]) for k in sorted(products.items(), key=lambda x:-1*x[1]) if k[1] > 1]
    res['who_with'] = [((str(k[0]), k[0].id), k[1]) for k in sorted(who_with.items(), key=lambda x:-1*x[1])][:50]
    res['sources'] = [k for k in res['sources']][:15]
    res['prices'] = sorted([k for k in res['prices']], key=lambda x:x[0])
    try:
        res['hours'] = [((hour2name[k[0]], k[0]), k[1]) for k in sorted(hours.items(), key=lambda x:-1*x[1]) if k[0] is not None]
    except Exception,e:
        from utils import ipdb;ipdb()
    return r2j(res)

@user_passes_test(staff_test)
def ajax_get_measurements(request):
    day=request.POST['today']
    day=datetime.datetime.strptime(day, DATE)
    dayobj=Day.objects.get(date=day.date())
    ms=Measurement.objects.filter(day=dayobj)
    res={'success':True, 'message':'got', 'measurements':[measurement2obj(m) for m in ms]}
    return r2j(res)

# based on the day of week, date, and total count, display measurement categories, one year cutoff
@user_passes_test(staff_test)
def ajax_get_common_measurements(request):
    res = {'samedate': [], 'samedow': [], 'all': [],}
    #this should actually be based on the day in question.
    source_date = datetime.datetime.strptime(request.POST['today'], DATE_DASH_REV)
    #by date of month
    day = source_date.day
    yearago = source_date - datetime.timedelta(days = 365)
    samedate = Measurement.objects.filter(day__date__day = day, day__date__gte = yearago)
    
    #should add in measurements which are also "last day of month" style.
    spotcounts = {}
    for mm in samedate:
        spotcounts[mm.spot] = spotcounts.get(mm.spot, 0) + 1
    
    byday = [{'name': spot.name, 'id': spot.id,'count': count,} for spot, count in spotcounts.items()]
    byday.sort(key = lambda x:(-1 * x['count'], x['name']))
    res['samedate'] = byday[:10]
    done_spotids = set([thing['id'] for thing in byday[:10]])
    
    #by day of week
    dows = [source_date - datetime.timedelta(days = 7 * n) for n in range(52)]
    samedows =  Measurement.objects.filter(day__date__in = dows, day__date__gte = yearago)
    spotcounts = {}
    for mm in samedows:
        if mm.spot.id in done_spotids:continue
        spotcounts[mm.spot] = spotcounts.get(mm.spot, 0) + 1
    
    bydow = [{'name': spot.name, 'id': spot.id,'count': count,} for spot, count in spotcounts.items()]
    bydow.sort(key = lambda x:(-1 * x['count'], x['name']))
    res['samedow'] = bydow[:10]
    done_spotids.update(set([thing['id'] for thing in bydow[:10]]))
    
    #by all
    allms = Measurement.objects.filter(day__date__gte = yearago)
    spotcounts = {}
    for mm in allms:
        if mm.spot.id in done_spotids:continue
        spotcounts[mm.spot] = spotcounts.get(mm.spot, 0) + 1
    allthings= [{'name': spot.name, 'id': spot.id,'count': count,} for spot, count in spotcounts.items()]
    allthings.sort(key = lambda x:(-1 * x['count'], x['name']))
    res['all'] = allthings[:10]
    done_spotids = set([thing['id'] for thing in allthings[:10]])
    
    return r2j(res)

@user_passes_test(staff_test)
def ajax_make_purchase(request):
    import ipdb;ipdb.set_trace()
    try:
        dat=request.POST
        today=dat['today']
        obj=datetime.datetime.strptime(today, DATE)
        hour=int(dat['hour'])
        dt=datetime.datetime(year=obj.year, month=obj.month, day=obj.day, hour=hour)
        product_id=dat['product_id']
        source_id=dat['source_id']
        cost=float(dat['cost'])
        quantity=dat['quantity'] and float(dat['quantity']) or 1
        size=dat['size']
        if 'who_with[]' in dat:
            who_with=dat.getlist('who_with[]')
        else:
            who_with=[]
        note=dat['note']
        currency = Currency.objects.get(id=1)
        if 'currency' in dat and dat['currency']:
            currency = Currency.objects.get(id=dat['currency'])
        else:
            source = Source.objects.get(id=source_id)
            if source.region and source.region.currency:
                currency = source.region.currency
        cur_id='currency' in dat and dat['currency'] or 1
        #hour_id=name2hour[gethour(hour)]
        purch=Purchase(hour=hour, created=dt, product_id=product_id, source_id=source_id, cost=cost, quantity=quantity, size=size, note=note, currency=currency)
        purch.save()
        for ww in who_with:
            purch.who_with.add(Person.objects.get(id=ww))
        purch.save()
        res={'success':True,'message':'saved %s'%purch}
        return r2j(res)
    except Exception, e:
        return r2j({'success':False,'message':'%s'%e})

@user_passes_test(staff_test)
def ajax_make_measurement(request):
    try:
        dat=request.POST
        today=dat['today']
        obj=datetime.datetime.strptime(today, DATE)
        dt=datetime.datetime(year=obj.year, month=obj.month, day=obj.day)
        spot_id=dat['spot_id']
        amount=float(dat['amount'])
        day=Day.objects.get(date=dt.date())
        measurement=Measurement(spot_id=spot_id, amount=amount, day=day,created=dt)
        measurement.save()
        res={'success':True,'message':'saved %s'%measurement}
        return r2j(res)
    except Exception, e:
        return r2j({'success':False,'message':'%s'%e})
    
#@user_passes_test(staff_test)
#def ajax_get_founding_for_spot(request):
    #'''return info to load the founding photo thumb for a spot if exists'''
    #try:
        #dat=request.POST
        #spot=PhotoSpot.objects.get(id=dat['photospot_id'])
        #from utils import ipdb;ipdb()
        #if spot.founding_photo:
            #founding=spot.founding_photo
            #exfp=founding.get_external_fp(thumb=True)
            #res={'success':True,'fp':exfp}
            #return r2j(res)
        #else:
            #res={'success':False,'message':'spot has no founding photo'}
            #return r2j(res)
    #except Exception, e:
        #return r2j({'success':False,'message':'%s'%e})