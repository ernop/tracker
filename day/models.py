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

def lnk(nodel, id, obj):
    return '<a href="/admin/day/%s/%d/">%s</a>'%(nodel, id, str(obj))

def clink(nodel, id, obj):
    #a link to the object list display with a filter only showing this guy
    return '<a  style="white-space:nowrap;" href="/admin/day/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

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

class Day(DayModel):
    date=models.DateField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='day'
        ordering=['date',]

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
        #import ipdb;ipdb.set_trace()
        newmonth = tt.month + months
        newyear = tt.year
        if newmonth == 0:
            newmonth = 12
            newyear = tt.year - 1
        if newmonth > 12:
            newyear = tt.year + 1
            newmonth = newmonth % 12
        return str(datetime.date(newyear, day=tt.day, month=newmonth))

    def vlink(self, text=None):
        if not text:
            text=str(self.date)+' '+datetime.datetime.strftime(self.date, '%a')
        return '<a class="btn" href="/aday/%s/">%s</a>'%(str(self.date), text)

    def day(self):
        return datetime.datetime.strftime(self.date, '%A')

    def getmeasurements(self):
        try:
            from day.models import Measurement
            nextday=self.date+datetime.timedelta(days=1)
            return Measurement.objects.filter(created__gte=self.date, created__lt=nextday).order_by('place__domain','place__name')
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

class PersonDay(DayModel):
    person=models.ForeignKey('Person', related_name='persondays')
    day=models.ForeignKey('Day', related_name='persondays')
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='personday'

    def __unicode__(self):
        return '%s%s'%(self.person, str(self.day))

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

class ExWeight(DayModel):
    exercise=models.ForeignKey(Exercise, related_name='exsets')
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

class Measurement(DayModel):
    place=models.ForeignKey('MeasuringSpot', related_name='measurements')
    amount=models.FloatField()
    created=models.DateField()

    def __unicode__(self):
        return '%s %s: %s'%(self.place, self.created.strftime(DATE), rstripz(self.amount))#','.join([str(s) for s in self.sets.all()]),)

    class Meta:
        db_table='measurement'
        ordering=['-created',]

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
            total_cost += p.cost
            total_quantity += p.quantity
            costs[p.product.id] = costs.get(p.product.id, 0) + p.cost
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

class Region(DayModel):
    '''geographical region'''
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    currency = models.ForeignKey('Currency')
    class Meta:
        db_table='region'

    def __unicode__(self):
            return self.name

class Source(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    region = models.ForeignKey(Region, blank=True, null=True)
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

class Product(DayModel):
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
        plink = '<a href="/admin/day/product/?id=%d">%s</a>'%(self.id, str(self))
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

class Currency(DayModel):
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

class Purchase(DayModel):
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
        return u'<a href="%s/day/%s/?id=%d">%s</a>'%(settings.ADMIN_EXTERNAL_BASE, self.product.__class__.__name__.lower(), self.product.id, unicode(self))

    def save(self, *args, **kwargs):
        if not self.created:
            self.created=datetime.datetime.now()
        super(Purchase, self).save(*args, **kwargs)

class Person(DayModel):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100, blank=True, null=True)
    birthday=models.DateField(blank=True, null=True)
    met_through=models.ManyToManyField('Person', symmetrical=False, blank=True, null=True, related_name='introduced_to')
    created=models.DateField(auto_now_add=True, blank=True, null=True)
    disabled = models.BooleanField()  #if they're gone forever / probably never meet again, just remove them form most convenience functions.
    gender=models.IntegerField() #1 male 2 female 3 organization 0 undefined

    class Meta:
        db_table='person'
        ordering=['first_name','last_name',]

    def __unicode__(self):
        return '%s%s'%(self.first_name, self.last_name and ' %s' % self.last_name)

    def d3_name(self):
        return self.first_name.title().replace('\'S', '\'s')


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

    def get_gender(self):
        if self.gender==1:return 'male'
        if self.gender==2:return 'female'
        if self.gender==3:return 'org'
        return 'undef'