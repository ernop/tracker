from django.db import models
from buy.models import Domain
from tracker.utils import DATE
def lnk(nodel, id, obj):
    return '<a href="/admin/workout/%s/%d/">%s</a>'%(nodel, id, str(obj))

# Create your models here.
def clink(nodel, id, obj):
    return '<a href="/admin/workout/%s/?id=%d">%s</a>'%(nodel, id, str(obj))

class Exercise(models.Model):
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
    
    def adm(self):
        return lnk('exercise',self.id, self)

    def clink(self):
        return clink('exercise', self.id, self)

class Muscle(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateField(auto_now_add=True)
    class Meta:
        ordering=['name',]
        db_table='muscle'    
        
    def __unicode__(self):
        return self.name
    
    def adm(self):
        return lnk('muscle',self.id, self)

class Set(models.Model):
    exweight=models.ForeignKey('ExWeight', related_name='sets')
    workout=models.ForeignKey('Workout', related_name='sets')
    count=models.IntegerField(blank=True)
    note=models.CharField(max_length=500, blank=True)
    created=models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s %s@%s lb'%(self.exweight.exercise, self.count, self.exweight.weight)            

    def adm(self):
        return lnk('set',self.id, self)    
    
    def save(self, *args, **kwargs):
        if not self.count:
            self.count=5    
        super(Set, self).save(*args, **kwargs)
        
    class Meta:
        ordering=['exweight__exercise',]
        db_table='set'

class ExWeight(models.Model):
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
        
class Workout(models.Model):
    exweights=models.ManyToManyField(ExWeight, through=Set, related_name='workout')
    created=models.DateTimeField()
    def __unicode__(self):
        return '%s'%(self.created.strftime(DATE), )#','.join([str(s) for s in self.sets.all()]),)
    
    class Meta:
        db_table='workout'
        ordering=['-created',]
        
    def adm(self):
        return lnk('workout',self.id, self)
    
class Measurement(models.Model):
    place=models.ForeignKey('MeasuringSpot', related_name='measurements')
    amount=models.FloatField()
    created=models.DateTimeField()
    def __unicode__(self):
            return '%s %s: <b>%0.2f</b>'%(self.place, self.created.strftime(DATE), self.amount)#','.join([str(s) for s in self.sets.all()]),)
    
    class Meta:
        db_table='measurement'
        ordering=['-created',]
        
    def adm(self):
        return lnk('measurement',self.id,  '%s: <b>%0.2f</b>'%(self.date.strftime(DATE), self.amount))
        
class MeasuringSpot(models.Model):
    name=models.CharField(max_length=100, unique=True)
    domain=models.ForeignKey(Domain, related_name='measuring_spots')
    created=models.DateField(auto_now_add=True)
    def __unicode__(self):
        return '%s'%(self.name, )
        
    class Meta:
        db_table='measuringspot'
        ordering=['name',]
        
    def adm(self):
        return lnk('measuringspot',self.id, self)
    
class MeasurementSet(models.Model):
    measurements=models.ManyToManyField(MeasuringSpot, related_name='measurementsets')
    created=models.DateField(auto_now_add=True)
        