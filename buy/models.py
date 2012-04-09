from django.db import models

def lnk(nodel, id, obj):
    return '<a href="/admin/buy/%s/%d/">%s</a>'%(nodel, id, str(obj))

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
    quantity=models.IntegerField()
    cost=models.FloatField()
    currency=models.ForeignKey('Currency')
    source=models.ForeignKey(Source, related_name='purchases')
    who_with=models.ManyToManyField('Person', related_name='purchases', blank=True, null=True)
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
    
