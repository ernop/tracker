
import datetime

from django.db import models
from django.conf import settings
from django.db.models import Sum
from utils import rstripz
from trackerutils import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from choices import *

def lnk(nodel, id, obj):
    return '<a href="/admin/buy/%s/%d/">%s</a>'%(nodel, id, str(obj))

def clink(nodel, id, obj):
    return '<a style="white-space:nowrap;" href="/admin/buy/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

from trackerutils import BuyModel

class Domain(BuyModel):
    """
    body, house, experiences, food, stuff, clothes, etc.
    """
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)

    class Meta:
        db_table='domain'
        ordering=['name',]

    def __unicode__(self):
        return self.name

    def all_products_link(self):
        return '<a href="/admin/buy/product/?domain__id=%d">all prod</a>'%(self.id)

    def all_purchases_link(self):
        return '<a href="/admin/buy/purchase/?product__domain__id__exact=%d">all purch</a>'%(self.id)

    def summary(self):
        rows = []
        for pp in self.products.all():
            link, count, cost, symbol = pp.summarydat()
            if not cost:
                continue
            rows.append((link, count, '%s%s'%(cost, symbol), cost))
        rows = sorted(rows, key=lambda x:x[3]*-1)
        rows = [r[:3] for r in rows]
        #sums=''.join([oo.summarydat() for oo in self.products.all() if oo.summary()])
        #ct=self.products.count()

        tbl = mktable(rows)
        return tbl
        if ct:
            return '%d products (%s) (%s)<br>%s'%(ct,

                                                             self.all_products_link(),
                                                             self.all_purchases_link(),
                                                             sums,)
        else:
            return '%d products'%(ct,)

    def piechart(self):
        return clink('domain', self.id, self)

class Source(BuyModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
        db_table='source'
        ordering=['name',]

    def __unicode__(self):
            return self.name

    def summary(self):
        if self.purchases.count():
            ptable = ''
            rowcosts = []
            for oo in Product.objects.filter(purchases__source=self).distinct():
                link, count, cost, symbol = oo.summarydat(source=self)
                if count == int(count):
                    count = int(count)
                pfilterlink = '<a href="/admin/buy/purchase/?product__id=%d&source__id=%d">filter</a>' % (oo.id, self.id)
                rowcosts.append(('<tr><td>%s<td>%0.0f%s<td>%s<td>%s'% (link, cost, symbol, count, pfilterlink), cost))
            rowcosts = sorted(rowcosts, key=lambda x:-1*x[1])
            ptable = '<table style="background-color:white;"  class="table">' + '\n'.join([th[0] for th in rowcosts])+ '</table>'
            return '%d purchases (%s)<br>%s'%(self.purchases.count(),
                #self.all_products_link(),
                self.all_purchases_link(),
                ptable,)

    def all_purchases_link(self):
        return '<a href="/admin/buy/purchase/?source__id=%d">all purch</a>'%(self.id)

    def total_spent(self, start=None, end=None, product=None, domain=None):
        valid=Purchase.objects.filter(source=self).filter(currency__id__in=RMB_CURRENCY_IDS)
        if domain:
            valid=valid.filter(product__domain=domain)
        if product:
            valid=valid.filter(product=product)
        if start:
            valid=valid.filter(created__gt=start)
        if end:
            valid=valid.filter(created__lt=end)
        cost=valid.aggregate(Sum('cost'))['cost__sum'] or 0
        return cost

class Product(BuyModel):
    name=models.CharField(max_length=100, unique=True)
    created=models.DateField(auto_now_add=True)
    domain=models.ForeignKey(Domain, related_name='products')
    class Meta:
        db_table='product'
        ordering=['name',]

    def __unicode__(self):
        return self.name

    def summary(self, source=None):
        """summary of all purchases of this product."""
        plink, count, cost, symbol= self.summarydat(source=source)
        return ' %s%s for %0.1f%s' % (plink, count != 1 and '(%d)' % count or '', cost, symbol)

    def summarydat(self, source=None):
        '''return link, count, cost,symbol'''
        if source:
            count=Purchase.objects.filter(product=self, source=source).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
        else:
            count=Purchase.objects.filter(product=self).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
        if not count:
            count = 0
        if count == int(count):
            count = int(count)
        else:
            count = round(count, 2)
        if source:
            purches=Purchase.objects.filter(product=self, source=source)
        else:
            purches=Purchase.objects.filter(product=self)
        try:
            symbol=purches[0].currency.symbol
        except:
            symbol = None
        cost=self.total_spent(source=source)
        if cost == int(cost):
            cost = int(cost)
        plink = '<a href="/admin/buy/product/?id=%d">%s</a>'%(self.id, str(self))
        return plink, count, cost, symbol

    def total_spent(self, start=None, end=None, source=None):
        valid=Purchase.objects.filter(product=self).filter(currency__id__in=RMB_CURRENCY_IDS)
        if source:
            valid=valid.filter(source=source)
        if start:
            valid=valid.filter(created__gt=start)
        if end:
            valid=valid.filter(created__lt=end)
        cost=valid.aggregate(Sum('cost'))['cost__sum'] or 0
        return cost

class Currency(BuyModel):
    """changed from currency; now, it represents an account i.e. cash, a specific bank acct, taobao"""
    name=models.CharField(max_length=100, unique=True)
    symbol=models.CharField(max_length=10)
    created=models.DateField(auto_now_add=True)
    class Meta:
        db_table='currency'
        ordering=['name',]

    def __unicode__(self):
        return self.name
    def adm(self):
        return lnk('currency',self.id, self)

class Purchase(BuyModel):
    product=models.ForeignKey(Product, related_name='purchases')
    #domain=models.ForeignKey(Domain, related_name='purchases')
    created=models.DateField()
    quantity=models.FloatField()
    size=models.CharField(max_length=100, null=True, blank=True)
    cost=models.FloatField()
    currency=models.ForeignKey('Currency')
    source=models.ForeignKey(Source, related_name='purchases')
    who_with=models.ManyToManyField('Person', related_name='purchases', blank=True, null=True)
    hour=models.IntegerField(choices=HOUR_CHOICES)
    note=models.CharField(max_length=2000, blank=True, null=True)
    object_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='purchase'
        ordering=['-created','product__name',]

    def __unicode__(self):
        res='%s'%self.product
        if not self.quantity==1:
            res+='(%d)'%self.quantity
        res+=' for %s%s'%(rstripz(self.cost), self.currency.symbol)
        return res

    def prodlink(self):
        return u'<a href="%s/buy/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.product.__class__.__name__.lower(), self.product.id, unicode(self))

    def save(self, *args, **kwargs):
        if not self.created:
            self.created=datetime.datetime.now()
        super(Purchase, self).save(*args, **kwargs)

class Person(BuyModel):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True)
    created=models.DateField(auto_now_add=True, blank=True, null=True)
    disabled = models.BooleanField()  #if they're gone forever / probably never meet again, just remove them form most convenience functions.

    class Meta:
        db_table='person'
        ordering=['first_name','last_name',]

    def __unicode__(self):
        return '%s%s'%(self.first_name, self.last_name and ' %s' % self.last_name)



#class SpanAverage(BuyModel):
    #"""for a span of time, starting date, and given domain (not general enough...) what was the running average per day spent on it?"""
    #"""not working"""
    #domain=models.ForeignKey('Domain')
    #start_date=models.DateField()
    #span=models.CharField(max_length=1, choices=SPAN_CHOICES)
    #value=models.FloatField()

    #def calc(self):
        #days=span2days[self.span]
        #now=datetime.datetime.now()
        #end=min(now, start_date+datetime.timedelta(days=days))
        #partial=False
        #if end==now:
            #partial=True
        #purch=Purchase.objects.filter(product__domain=self.domain, created__gt=self.start_date, created__lte=end)
        #res=0
        #for p in purch:
            #res+=p.cost
        #self.value=res
        #self.save()

    #def __unicode__(self):
        #if self.value is None:
            #self.calc()
        #return '%0.1f/day for the %s starting %s'%(self.value, self.span, self.start_date)