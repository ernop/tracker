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
    return '<a href="/admin/buy/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

# Create your models here.

from trackerutils import MyJsReplacementBuy

class SpanAverage(MyJsReplacementBuy):
    """for a span of time, starting date, and given domain (not general enough...) what was the running average per day spent on it?"""
    """not working"""
    domain=models.ForeignKey('Domain')
    start_date=models.DateField()
    span=models.CharField(max_length=1, choices=SPAN_CHOICES)
    value=models.FloatField()
    
    def calc(self):
        days=span2days[self.span]
        now=datetime.datetime.now()
        end=min(now, start_date+datetime.timedelta(days=days))
        partial=False
        if end==now:
            partial=True
        purch=Purchase.objects.filter(product__domain=self.domain, created__gt=self.start_date, created__lte=end)
        res=0
        for p in purch:
            res+=p.cost
        self.value=res
        self.save()

    def __unicode__(self):
        if self.value is None:
            self.calc()
        return '%0.1f/day for the %s starting %s'%(self.value, self.span, self.start_date)



class Domain(MyJsReplacementBuy):
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
        sums='<br>'.join([oo.summary() for oo in self.products.all() if oo.summary()])
        ct=self.products.count()
        if ct:
            return '%d products (%s) (%s)<br>%s'%(ct,

                                                             self.all_products_link(),
                                                             self.all_purchases_link(),
                                                             sums,)
        else:
            return '%d products'%(ct,)

    def clink(self):
        return clink('domain', self.id, self)            

    def piechart(self):
        return clink('domain', self.id, self)

class Source(MyJsReplacementBuy):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
        db_table='source'
        ordering=['name',]

    def __unicode__(self):
            return self.name
    def clink(self):
        return clink('source', self.id, self)
    def summary(self):
        if self.purchases.count():
            #self.purchases.filter(currency__name='rmb').aggregate(Sum('quantity'))['quantity__sum']
            return '%d purchases (%s)<br>%s'%(self.purchases.count(),
                #self.all_products_link(),
                self.all_purchases_link(),
                '<br>'.join([oo.summary(source=self) for oo in Product.objects.filter(purchases__source=self).distinct()]),)

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

class Product(MyJsReplacementBuy):
    name=models.CharField(max_length=100, unique=True)
    created=models.DateField(auto_now_add=True)
    domain=models.ForeignKey(Domain, related_name='products')
    class Meta:
        db_table='product'
        ordering=['name',]
    def __unicode__(self):
        return self.name

    def adm(self):
        return lnk('product',self.id, self)

    def clink(self):
        return clink('product', self.id, self)

    def summary(self, source=None):
        """summary of all purchases of this product."""
        if source:
            count=Purchase.objects.filter(product=self, source=source).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
        else:
            count=Purchase.objects.filter(product=self).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
        if not count:
            return ''
        if count==1:
            count=''
        else:
            count='('+str(count).rstrip('0').rstrip('.')+')'
        purches=Purchase.objects.filter(product=self)
        symbol=purches[0].currency.symbol
        cost=self.total_spent(source=source)
        return '<a href="/admin/buy/product/?id=%d">%s</a> %s for %s%s'%(self.id, str(self), count, ('%f'%cost).rstrip('0').rstrip('.'), symbol)

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

class Currency(MyJsReplacementBuy):
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

class Purchase(models.Model):
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

    class Meta:
        db_table='purchase'
        ordering=['-created','product__name',]

    def __unicode__(self):
        res='%s'%self.product
        if not self.quantity==1:
            res+='(%d)'%self.quantity
        res+=' for %s%s'%(self.currency.symbol, rstripz(self.cost))
        return res

    def adm(self):
        return lnk('purchase',self.id, self)

    def clink(self):
        return clink('purchase', self.id, self)

class Person(MyJsReplacementBuy):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True)
    created=models.DateField(auto_now_add=True)

    class Meta:
        db_table='person'
        ordering=['first_name','last_name',]

    def __unicode__(self):
        return '%s %s'%(self.first_name, self.last_name)

    def adm(self):
        return lnk('person',self.id, self)

