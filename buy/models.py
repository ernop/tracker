from django.db import models

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

def apl(nodel, id, obj):
    return '<a href="/admin/buy/%s/?domain__id=%d">all</a>'%(nodel, id,)

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
        return apl('product', self.id, self)
    
class Source(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
        db_table='source'    
        ordering=['name',]
            
    def __unicode__(self):
            return self.name        

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
    created=models.DateField(auto_now_add=True)
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
    
