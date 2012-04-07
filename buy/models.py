from django.db import models

# Create your models here.
class Domain(models.Model):
    """
    body, house, experiences, food, stuff, clothes, etc.
    """
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
            db_table='domain'    
            
    def __unicode__(self):
        return self.name
    
class Source(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
            db_table='source'    
            
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

class Currency(models.Model):
    name=models.CharField(max_length=100, unique=True)
    symbol=models.CharField(max_length=10)
    class Meta:
        db_table='currency'    
            
    def __unicode__(self):
        return self.name            

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
        return '%s %d for %0.02f%s each, total %0.2f'%(self.product, self.quantity, float(self.cost)/self.quantity, self.currency.symbol, self.cost)
    
class Person(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True)
    
    class Meta:
        db_table='person'
        
    def __unicode__(self):
        return '%s %s'%(self.first_name, self.last_name)
