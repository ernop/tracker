# Create your views here.
from tracker.buy.models import *

def counts(request):
    pp=Purchase.objects.all()
    
def days(request):
    sixmonthago=datetime.datetime.now()-datetime.timedelta(days=180)
    total=Purchase.objects.filter(currency__name='rmb').filter(created__gte=sixmonthago).aggregate(Sum('cost'))['cost__sum']
    ear=Purchase.objects.filter(currency__name='rmb').order_by('created')
    earliest=None
    if ear:
        earliest=datetime.datetime.combine(ear[0].created, datetime.time())
    else:
        return ''
    now=datetime.datetime.now()
    dayrange=min(180.0,(abs((now-earliest).days))+1)
    return '%s%s<br>%s%s/day<br>(%d days)'%(rstripz(total), Currency.objects.get(id=1).symbol, rstripz(total/dayrange), Currency.objects.get(id=1).symbol, dayrange)    