from django.db import models
from django.db.models import Sum

HOUR_CHOICES=zip(range(10), 'morning noon afternoon evening night midnight'.split())
hour2name={}
name2hour={}
for a in HOUR_CHOICES:
    hour2name[a[1]]=a[0]
    name2hour[a[0]]=a[1]
#hour2name={a[1]:a[0] for a in HOUR_CHOICES}
#name2hour={a[0]:a[1] for a in HOUR_CHOICES}


def lnk(nodel, id, obj):
    return '<a href="/admin/buy/%s/%d/">%s</a>'%(nodel, id, str(obj))

def clink(nodel, id, obj):
    return '<a href="/admin/buy/%s/?id=%d">%s</a>'%(nodel, id, str(obj))


# Create your models here.
class Domain(models.Model):
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
        return '%d products (%s) (%s)<br>%s'%(self.products.count(),
                                                             self.all_products_link(),
                                                             self.all_purchases_link(),
                                         '<br>'.join([oo.summary() for oo in self.products.all() if oo.summary()]),)        
    
class Source(models.Model):
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
        #import ipdb;ipdb.set_trace()
        if self.purchases.count():
            return '%d purchases (%s)<br>%s'%(self.purchases.exclude(currency__name__ne='rmb').aggregate(Sum('quantity'))['quantity__sum'],
                                                             #self.all_products_link(),
                                                             self.all_purchases_link(),
                                         '<br>'.join([oo.summary(source=self) for oo in Product.objects.filter(purchases__source=self).distinct()]),)
    
    def all_purchases_link(self):
        return '<a href="/admin/buy/purchase/?source__id=%d">all purch</a>'%(self.id)    
    
class Product(models.Model):
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
            count=Purchase.objects.filter(product=self, source=source).filter(currency__id=1).aggregate(Sum('quantity'))['quantity__sum']
        else:
            count=Purchase.objects.filter(product=self).filter(currency__id=1).aggregate(Sum('quantity'))['quantity__sum']
        if not count:
            return ''
        cost=Purchase.objects.filter(product=self).filter(currency__id=1).aggregate(Sum('cost'))['cost__sum'] or 0
        return '<a href="/admin/buy/purchase/?product__id=%d">%s</a> (%d) for %0.2f'%(self.id, str(self), count, cost)

class Currency(models.Model):
    name=models.CharField(max_length=100, unique=True)
    symbol=models.CharField(max_length=10)
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
    cost=models.FloatField()
    currency=models.ForeignKey('Currency')
    source=models.ForeignKey(Source, related_name='purchases')
    who_with=models.ManyToManyField('Person', related_name='purchases', blank=True, null=True)
    hour=models.IntegerField(choices=HOUR_CHOICES)
    class Meta:
        db_table='purchase'    
        ordering=['product__name',]
    
    def __unicode__(self):
        res='%s'%self.product
        if not self.quantity==1:
            res+='(%d)'%self.quantity
        res+=' for %s%0.2f'%(self.currency.symbol, self.cost)
        return res
    
    def adm(self):
        return lnk('purchase',self.id, self)    
    
    def clink(self):
        return clink('purchase', self.id, self)
    
class Person(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True)
    
    class Meta:
        db_table='person'
        ordering=['first_name','last_name',]
        
    def __unicode__(self):
        return '%s %s'%(self.first_name, self.last_name)

    def adm(self):
        return lnk('person',self.id, self)
    
