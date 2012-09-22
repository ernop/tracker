# Create your views here.

import datetime

# Create your views here.

#from coffin.shortcuts import *
from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet)
from django.shortcuts import HttpResponseRedirect, HttpResponse
from trackerutils import *
from day.models import *
from buy.models import Person, Purchase, Source
from trackerutils import *
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from utils import *
log=logging.getLogger(__name__)
from forms import DayForm


@user_passes_test(staff_test)
def ajax_get_purchases(request):
    
    day=request.POST['today']
    day=datetime.datetime.strptime(day, DATE)
    
    ps=Purchase.objects.filter(created__year=day.year, created__month=day.month, created__day=day.day)
    res={'success':True, 'message':'got', 'purchases':[purchase2obj(p) for p in ps]}
    return r2j(res)

@user_passes_test(staff_test)
def ajax_make_purchase(request):
    try:
        dat=request.POST
        today=dat['today']
        obj=datetime.datetime.strptime(today, DATE)
        hour=int(dat['hour'])
        #hour=hourid2hour[int(hour_id)]
        
        dt=datetime.datetime(year=obj.year, month=obj.month, day=obj.day, hour=hour)
        product_id=dat['product_id']
        source_id=dat['source_id']
        cost=float(dat['cost'])
        quantity=dat['quantity'] and int(dat['quantity']) or 1
        size=dat['size']
        if 'who_with[]' in dat:
            who_with=dat['who_with[]']
        else:
            who_with=[]
        note=dat['note']
        cur_id='cur_id' in dat and dat['cur_id'] or 1
        purch=Purchase(created=dt, product_id=product_id, source_id=source_id, cost=cost, quantity=quantity, size=size, note=note, currency_id=cur_id)
        purch.save()
        for ww in who_with:purch.who_with.add(Person.objects.get(id=ww))
        purch.save()
        res={'success':True,'message':'saved %s'%purch}
        return r2j(res)
    except Exception, e:
        return r2j({'success':False,'message':'%s'%e})