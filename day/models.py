import datetime

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.admin.widgets import FilteredSelectMultiple

from utils import rstripz
from trackerutils import *
DATE='%Y-%m-%d'

from trackerutils import DayModel, debu

from choices import *

from photomodels import *

def lnk(nodel, id, obj):
    return '<a href="/admin/day/%s/%d/">%s</a>'%(nodel, id, str(obj))

def clink(nodel, id, obj):
    #a link to the object list display with a filter only showing this guy
    return '<a  style="white-space:nowrap;" href="/admin/day/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

class Currency(DayModel):
    """changed from currency; now, it represents an account i.e. cash, a specific bank acct, taobao"""
    name=models.CharField(max_length=100, unique=True)
    symbol=models.CharField(max_length=10)
    created=models.DateField(auto_now_add=True)
    rmb_value = models.FloatField()  #how many rmb one of these babies is worth. used by purchase.get_cost
    class Meta:
        db_table='currency'
        ordering=['name',]

    def __unicode__(self):
        return self.name
    def adm(self):
        return lnk('currency',self.id, self)
class Day(DayModel):
    date=models.DateField()
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='day'

    def __unicode__(self):
        return str(self.date)

    def plus(self, days=None, months=None, years=None):
        if years:
            return str(datetime.date(self.date.year+years, day=self.date.day, month=self.date.month))
        from utils import add_months
        if months:
            return str(add_months(self.date, months))
        days=days or 0
        months = months or 0
        years=years or 0
        newyear=self.date.year+years
        tt=self.date+datetime.timedelta(days=days)
        #just add the days

        #if got a month, bump that.
        newmonth = tt.month + months
        newyear = tt.year
        if newmonth == 0:
            newmonth = 12
            newyear = tt.year - 1
        if newmonth > 12:
            newyear = tt.year + 1
            newmonth = newmonth % 12
        return str(datetime.date(newyear, day=tt.day, month=newmonth))

    def vlink(self, text=None,max_length=False):
        if not text:
            text=str(self.date)+' '+datetime.datetime.strftime(self.date, '%a')
        if max_length:
            extra_style='width:inherit;'
        else:
            extra_style=''
        return '<a style="%s" class="stdbtn btn nb" href="/aday/%s/">%s</a>'%(extra_style,str(self.date), text)

    def show_day(self):
        return datetime.datetime.strftime(self.date, '%A')

    def show_notekinds(self):
        return ', '.join(['%s%s'%(nk[0],nk[1] and nk[1]!=1 and '(%d)'%(nk[1]) or '') for nk in self.get_notekinds()])

    def get_notekinds(self):
        nks = {}
        for note in self.notes.all():
            for nk in note.kinds.all():
                nks[nk.name] = nks.get(nk.name, 0) + 1
        return sorted(nks.items(), key=lambda x:x[0])

    def getmeasurements(self):
        try:
            from day.models import Measurement
            nextday=self.date+datetime.timedelta(days=1)
            return Measurement.objects.filter(created__gte=self.date, created__lt=nextday).order_by('spot__domain','spot__name')
        except Exception, e:
            print 'bad'
            return []

    def getworkouts(self):
        try:
            from day.models import Workout
            nextday=self.date+datetime.timedelta(days=1)
            return Workout.objects.filter(created__gte=self.date, created__lt=nextday)
        except Exception, e:
            print 'bad get workouts.'
            return []
        
    def has_any_history(self):
        return self.get_photos_for_history() or self.notes.exists()

    def get_history_description(self):
        '''text used on historylink on day.'''
        res=self.__unicode__()+' '+self.show_notekinds()
        return res
    
    def get_photos_for_history(self,user=None):
        res=[]
        photos=self.photos.exclude(incoming=True).exclude(deleted=True).exclude(tags=None)
        for ph in photos:
            if user:
                if ph.can_be_seen_by(user):
                    res.append(ph)
            else:
                if ph.can_be_seen_by(user=None):
                    res.append(ph)
        return res
    
    
class Domain(DayModel):
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
        return '<a href="/admin/day/product/?domain__id=%d">all prod</a>'%(self.id)

    def all_purchases_link(self):
        return '<a href="/admin/day/purchase/?product__domain__id__exact=%d">all purch</a>'%(self.id)

    def spent_history(self, start, end):
        counts = {}
        costs = {}
        res = {}
        ps = Purchase.objects.filter(product__domain=self, created__gte=start, created__lt=end)
        total_quantity = 0
        total_cost = 0
        for p in ps:
            total_cost += p.get_cost()
            total_quantity += p.quantity
            costs[p.product.id] = costs.get(p.product.id, 0) + p.get_cost()
            counts[p.product.id] = counts.get(p.product.id, 0) + p.quantity
        res['costs'] = costs
        res['counts'] = counts
        res['total_quantity'] = total_quantity
        res['total_cost'] = total_cost
        tops = costs.items()
        tops.sort(key=lambda x:-1*x[1])
        res['top_purchases_html'] = '<div class="top-purchases">'+', '.join(['%s (%d)'%(Product.objects.get(id=top[0]).name, top[1]) for top in tops[:3]])+'</div>'
        if len(tops) > 3:
            res['all_purchases_html'] = '<div class="all-purchases">' + '<br> '.join(['%s (%d)'%(Product.objects.get(id=top[0]).name, top[1]) for top in tops[:3]])+'</div>'
        else:
            res['all_purchases_html'] = ''
        return res

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
class Exercise(DayModel):
    name=models.CharField(max_length=100, unique=True)
    pmuscles=models.ManyToManyField('Muscle', related_name='primary_exercises')
    smuscles=models.ManyToManyField('Muscle', related_name='synergists_exercises')
    barbell=models.BooleanField()
    note=models.CharField(max_length=500, blank=True)
    created=models.DateField(auto_now_add=True)

    class Meta:
        db_table='exercise'
        ordering=['name',]

    def __unicode__(self):
        return self.name
class ExWeight(DayModel):
    exercise=models.ForeignKey('Exercise', related_name='exsets')
    weight=models.FloatField(blank=True)
    side=models.FloatField(blank=True)
    created=models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.side and self.exercise.barbell:
            self.weight=self.side*2+45
        else:
            if self.exercise.barbell:
                self.side=(self.weight-45)/2.0
            else:
                self.side=self.weight/2
        super(ExWeight, self).save(*args, **kwargs)

    def __unicode__(self):
        res='%s %s'%(self.exercise, self.weight)
        if self.exercise.barbell:
            res+=' (%0.1f)'%self.side
        return res

    class Meta:
        db_table='exweight'
        ordering=['exercise','weight',]

    def adm(self):
        return lnk('exweight',self.id, self)
    
class Measurement(DayModel):
    spot=models.ForeignKey('MeasuringSpot', related_name='measurements')
    amount=models.FloatField()
    created=models.DateField() #bit weird these are not datetime...
    day=models.ForeignKey('Day',related_name='measurements')

    def __unicode__(self):
        return '%s %s: %s'%(self.spot, self.created.strftime(DATE), rstripz(self.amount))#','.join([str(s) for s in self.sets.all()]),)

    def get_amount(self):
        '''return int(amount) if it looks ok'''
        try:
            if int(self.amount) == self.amount:
                return int(self.amount)
            return self.amount
        except:
            return self.amount

    class Meta:
        db_table='measurement'
        ordering=['-created',]
        
    def save(self):
        if not self.created:
            self.created=datetime.datetime.now()
        try:
            self.day
        except:
            self.day=Day.objects.get(date=self.created)
        #if not self.pk:
            #self.created=datetime.datetime.now()
        super(Measurement, self).save()
        
class MeasuringSpot(DayModel):
    name=models.CharField(max_length=100, unique=True)
    domain=models.ForeignKey('Domain', related_name='measuring_spots')
    created=models.DateField(auto_now_add=True)
    exclude_zeros=models.BooleanField()
    def __unicode__(self):
        return '%s'%(self.name, )

    class Meta:
        db_table='measuringspot'
        ordering=['name',]


    def save(self):
        if not self.created:
            self.created=datetime.datetime.now()
        if not self.pk:
            self.created=datetime.datetime.now()
        super(MeasuringSpot, self).save()
class MeasurementSet(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    measurement_spots=models.ManyToManyField(MeasuringSpot)

    class Meta:
        db_table='measurementset'

    def __unicode__(self):
        return u'MeasurementSet %s'%self.name
class Muscle(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)

    class Meta:
        ordering=['name',]
        db_table='muscle'

    def __unicode__(self):
        return self.name

    def adm(self):
        return lnk('muscle',self.id, self)
class Note(DayModel):
    day=models.ForeignKey('Day', related_name='notes')
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    kinds=models.ManyToManyField('NoteKind', related_name='notes', blank=True, null=True)

    class Meta:
        db_table='note'

    def __unicode__(self):
        return '%s %s'%(str(self.day), self.nks() or 'no kind')

    def nks(self):
        return ','.join([str(nk) for nk in self.kinds.all()])
    
    def html(self):
        txt=self.text
        txt=txt.replace('\n','<br>')
        return txt
    
    def subnotelink(self):
        return ','.join([nk.clink() for nk in self.kinds.all()])

    def nkids(self):
        return ','.join([str(n.id) for n in self.kinds.all()])

    def getheight(self):
        return (self.text and len(self.text)/4+80) or '250'



class NoteKind(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s'%(self.name)

    class Meta:
        db_table='notekind'


    @debu
    def vlink(self, text=None):
        if not text:
            text='%s (%d)'%(self.name, self.notes.count())
        return '<a class="btn"  href="/notekind/%s/">%s </a>'%(self.id, text)
    
class Person(DayModel):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True, related_name='introduced_to')
    created=models.DateField(auto_now_add=True, blank=True, null=True) #when i met them.
    disabled = models.BooleanField()  #if they're gone forever / probably never meet again, just remove them form most convenience functions.
    gender=models.IntegerField() #1 male 2 female 3 organization 0 undefined
    rough_purchase_count = models.IntegerField(default=0)
    description=models.TextField(blank=True,null=True)
    origin=models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        db_table='person'
        ordering=['first_name','last_name',]
        
    def update_purchase_count(self):
        self.rough_purchase_count = self.purchases.count()
        self.save()

    def __unicode__(self):
        return self.name()
        return '%s%s'%(self.first_name, self.last_name and ' %s' % self.last_name)
    

    def short_name(self):
        return self.first_name.title().replace('\'S', '\'s')
    
    def initial(self):
        fn=self.first_name and self.first_name[0] or ''
        ln=self.last_name and self.last_name[0] or ''
        if fn or ln:
            return '%s%s'%(fn,ln)
        return '?'

    def domain_summary_data(self):
        res = {}
        purch = self.purchases.all()
        counts = {}
        costs = {}
        for domain in Domain.objects.all():
            if purch.filter(product__domain=domain).exists():
                counts[domain.id] = purch.filter(product__domain=domain).count()
                costs[domain.id]= purch.filter(product__domain=domain).aggregate(Sum('cost'))['cost__sum']
        res['counts'] = counts
        res['costs'] = costs
        return res

    
    def gender_html_class(self):
        return self.get_gender()
    
    #def gender_html_icon(self):
        #if self.gender==1:return 'male'
        #if self.gender==2:return 'female'
        #if self.gender==3:return '<i class='
        #return ''
    
    def get_gender(self):
        if self.gender==1:return 'male'
        if self.gender==2:return 'female'
        if self.gender==3:return 'org'
        return 'undef'
        
    def name(self):
        fn=self.first_name or ''
        res=fn
        ln=self.last_name or ''
        if ln=='?':
            ln=''
        if ln:
            res+=' '+ln
        return res
    
    def save(self,*args,**kwargs):
        self.first_name=self.first_name.strip()
        self.last_name=self.last_name.strip()
        self.description=self.description.strip()
        self.origin=self.origin.strip()
        super(Person, self).save(*args, **kwargs)
        
        try:
            from day.photomodels import PhotoTag
            PhotoTag.setup_my_person_tag(self)
            #setting up the related tag for this person.
        except:
            pass
        
    
class PersonDay(DayModel):
    #not used
    person=models.ForeignKey('Person', related_name='persondays')
    day=models.ForeignKey('Day', related_name='persondays')
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='personday'

    def __unicode__(self):
        return '%s%s'%(self.person, str(self.day))
class Product(DayModel):
    name=models.CharField(max_length=100, unique=True)
    created=models.DateField(auto_now_add=True)
    domain=models.ForeignKey('Domain', related_name='products')
    class Meta:
        db_table='product'
        ordering=['name',]

    def __unicode__(self):
        return self.name

    def summary(self, source=None):
        """summary of all purchases of this product."""
        vlink, count, cost, symbol= self.summarydat(source=source)
        return ' %s%s for %0.1f%s' % (vlink, count != 1 and '(%d)' % count or '', cost, symbol)

    def summarydat(self, source=None):
        '''return link, count, cost,symbol'''
        if source:
            count=Purchase.objects.filter(product=self, source=source).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
        else:
            count=Purchase.objects.filter(product=self).filter(currency__id__in=RMB_CURRENCY_IDS).aggregate(Sum('quantity'))['quantity__sum']
            #we only count RMB stuff here cause it's freaking annoying otherwise.
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
        vlink = '<a href="/admin/day/product/?id=%d">%s</a>'%(self.id, str(self))
        return vlink, count, cost, symbol

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
class Purchase(DayModel):
    product=models.ForeignKey('Product', related_name='purchases')
    #domain=models.ForeignKey(Domain, related_name='purchases')
    created=models.DateField()
    quantity=models.FloatField()
    size=models.CharField(max_length=100, null=True, blank=True)
    cost=models.FloatField()
    currency=models.ForeignKey('Currency')
    source=models.ForeignKey('Source', related_name='purchases')
    who_with=models.ManyToManyField('Person', related_name='purchases', blank=True, null=True)
    hour=models.IntegerField(choices=HOUR_CHOICES)
    note=models.CharField(max_length=2000, blank=True, null=True)
    object_created=models.DateTimeField(auto_now_add=True)
    day=models.ForeignKey('Day',related_name='purchases')

    class Meta:
        db_table='purchase'

    def __unicode__(self):
        res='%s'%self.product
        if not self.quantity==1:
            res+='(%d)'%self.quantity
        res+=' for %s%s'%(rstripz(self.cost), self.currency.symbol)
        return res

    def prodlink(self):
        return u'<a href="%s/day/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.product.__class__.__name__.lower(), self.product.id, unicode(self))

    def save(self, *args, **kwargs):
        cc=self.created or (datetime.datetime.now())
        try:ccdate=cc.date()
        except:ccdate=cc
        if not self.day_id:
            try:
                dd=Day.objects.get(date=ccdate)
            except Day.DoesNotExist:
                dd=Day(created=cc,date=ccdate)
                dd.save()
            self.day=dd
        if not self.created:
            self.created=datetime.datetime.now()
        super(Purchase, self).save(*args, **kwargs)

    def get_cost(self):
        '''because costs are stored in the local currency, sometimes you have to convert them.

        lots of things directly access cost which isn't really right. '''

        if self.currency.name != 'rmb':
            return self.currency.rmb_value * self.cost
        return self.cost
    
class Region(DayModel):
    '''geographical region'''
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    currency = models.ForeignKey('Currency')
    class Meta:
        db_table='region'

    def __unicode__(self):
            return self.name
class Set(DayModel):
    exweight=models.ForeignKey('ExWeight', related_name='sets')
    workout=models.ForeignKey('Workout', related_name='sets')
    count=models.IntegerField(blank=True)
    note=models.CharField(max_length=500, blank=True)
    created=models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s@%s lb'%(self.exweight.exercise, self.count, self.exweight.weight)


    def save(self, *args, **kwargs):
        if not self.count:
            self.count=5
        super(Set, self).save(*args, **kwargs)

    class Meta:
        ordering=['id',]
        db_table='set'
class Source(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    region = models.ForeignKey('Region', blank=True, null=True)
    class Meta:
        db_table='source'
        ordering=['name',]

    def __unicode__(self):
            return self.name

    def domain_summary_data(self):
        res = {}
        purch = self.purchases.all()
        counts = {}
        costs = {}
        for domain in Domain.objects.all():
            if purch.filter(product__domain=domain).exists():
                counts[domain.id] = purch.filter(product__domain=domain).count()
                costs[domain.id]= purch.filter(product__domain=domain).aggregate(Sum('cost'))['cost__sum']
        res['counts'] = counts
        res['costs'] = costs
        return res

    def summary(self):
        if self.purchases.count():
            ptable = ''
            rowcosts = []
            for oo in Product.objects.filter(purchases__source=self).distinct():
                link, count, cost, symbol = oo.summarydat(source=self)
                if count == int(count):
                    count = int(count)
                pfilterlink = '<a href="/admin/day/purchase/?product__id=%d&source__id=%d">filter</a>' % (oo.id, self.id)
                rowcosts.append(('<tr><td>%s<td>%0.0f%s<td>%s<td>%s'% (link, cost, symbol, count, pfilterlink), cost))
            rowcosts = sorted(rowcosts, key=lambda x:-1*x[1])
            ptable = '<table style="background-color:white;"  class="table">' + '\n'.join([th[0] for th in rowcosts])+ '</table>'
            return '%d purchases (%s)<br>%s'%(self.purchases.count(),
                #self.all_products_link(),
                self.all_purchases_link(),
                ptable,)

    def all_purchases_link(self):
        return '<a href="/admin/day/purchase/?source__id=%d">all purch</a>'%(self.id)

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

    def save(self, *args, **kwargs):
        if not self.region:
            if Region.objects.filter(name='beijing').exists():
                beijing = Region.objects.get(name='beijing')
                self.region = beijing
        super(Source, self).save(*args, **kwargs)
class Tag(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    days=models.ManyToManyField('Day', related_name='tags')

    class Meta:
        db_table='tag'
        ordering=['name',]

    def __unicode__(self):
        return self.name

    def html(self):
        return '<div class="tag">%s%s</div>'%(self.name, self.day)
class Workout(DayModel):
    exweights=models.ManyToManyField(ExWeight, through=Set, related_name='workout')
    created=models.DateTimeField()
    def __unicode__(self):
        return '%s'%(self.created.strftime(DATE), )#','.join([str(s) for s in self.sets.all()]),)

    class Meta:
        db_table='workout'
        ordering=['-created',]

    def adm(self):
        return lnk('workout',self.id, self)

    def mysets(self):
        res={}
        preres={}

        ex_order=[]
        for s in self.sets.all():
            res[s.exweight.exercise]=[]
            if s.exweight.exercise not in ex_order:
                ex_order.append(s.exweight.exercise)
        for s in self.sets.all():res[s.exweight.exercise].append(s)
        #res is dict of exercise => [exweights,]
        res2={}
        for exercise,zets in res.items():
            weights={}
            ct=0 #counter - merge sequential sets of the same weight.
            lastweight=None
            for zet in zets:
                if lastweight and zet.exweight.weight==lastweight:
                    pass
                else:
                    ct+=1
                    lastweight=zet.exweight.weight
                    if exercise.barbell:
                        weights[(ct, zet.exweight.weight, zet.exweight.side,)]=[]
                    else:
                        weights[(ct, zet.exweight.weight)]=[]
                if exercise.barbell:
                    weights[(ct, zet.exweight.weight, zet.exweight.side,)].append(zet.count)
                else:
                    weights[(ct, zet.exweight.weight)].append(zet.count)
            weights['sets']=zets
            res2[exercise]=weights
        res3=''
        for exercise, summary in sorted(res2.items(), key=lambda x:x[1]['sets'][0].id):
            #order by set id, so the order you do them in the workout is right.
            res3+='%s '%exercise.clink()
            for weight, counts in sorted(summary.items()):
                if weight=='sets':continue
                if exercise.barbell:
                    res3+=' <b>%d</b>(%d):'%(weight[1], weight[2])
                else:
                    res3+=' <b>%d</b>:'%(weight[1])
                res3+=','.join(['%d'%cc for cc in counts])
            #res3+='%s %s'%(exercise, ' ,'.join(['%d'%s for s in summary]))
            res3+='<br>'
        return res3
