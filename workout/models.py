import datetime

from django.db import models
from buy.models import Domain
from tracker.utils import DATE

from django.db import models
from django.conf import settings
from django.db.models import Sum
from utils import rstripz

HOUR_CHOICES=zip(range(10), 'morning noon afternoon evening night midnight'.split())
HOUR_CHOICES.append((6,'deep night'))
HOUR_CHOICES.append((7,'early morning'))
hour2name={}
name2hour={}
for a in HOUR_CHOICES:
    hour2name[a[1]]=a[0]
    name2hour[a[0]]=a[1]

def lnk(nodel, id, obj):
    return '<a href="/admin/workout/%s/%d/">%s</a>'%(nodel, id, str(obj))

def clink(nodel, id, obj):
    #a link to the object list display with a filter only showing this guy
    return '<a href="/admin/workout/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

from trackerutils import WorkoutModel
class Exercise(WorkoutModel):
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
    

class Muscle(WorkoutModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    
    class Meta:
        ordering=['name',]
        db_table='muscle'    
        
    def __unicode__(self):
        return self.name
    
    def adm(self):
        return lnk('muscle',self.id, self)

class Set(WorkoutModel):
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

class ExWeight(WorkoutModel):
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
        
class Workout(WorkoutModel):
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
        #import ipdb;ipdb.set_trace()
        for exercise,zets in res.items():
            #import ipdb;ipdb.set_trace()
            weights={}
            ct=0 #counter - merge sequential sets of the same weight.
            lastweight=None
            #import ipdb;ipdb.set_trace()
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
                #import ipdb;ipdb.set_trace()
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
    
    
class Measurement(WorkoutModel):
    place=models.ForeignKey('MeasuringSpot', related_name='measurements')
    amount=models.FloatField()
    created=models.DateField()
    
    def __unicode__(self):
        return '%s %s: <b>%s</b>'%(self.place, self.created.strftime(DATE), rstripz(self.amount))#','.join([str(s) for s in self.sets.all()]),)
    
    class Meta:
        db_table='measurement'
        ordering=['-created',]
        

class MeasuringSpot(WorkoutModel):
    name=models.CharField(max_length=100, unique=True)
    domain=models.ForeignKey(Domain, related_name='measuring_spots')
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
    
class MeasurementSet(WorkoutModel):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    measurement_spots=models.ManyToManyField(MeasuringSpot)
    
    class Meta:
        db_table='measurementset'
        
    def __unicode__(self):
        return u'MeasurementSet %s'%self.name
    
  