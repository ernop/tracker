import datetime

from django.db import models
from django.contrib import admin
from buy.models import Person

from trackerutils import DayModel, debu

class Tag(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    days=models.ManyToManyField('Day', related_name='tags')
    #day=models.ForeignKey('Day')
    class Meta:
        db_table='tag'
        ordering='name'
        
    def __unicode__(self):
        return self.name
    
    def html(self):
        return '<div class="tag">%s%s</div>'%(self.name, self.day)
    
class Day(DayModel):
    date=models.DateField()
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='day'
        ordering='date'
        
    def __unicode__(self):
        return str(self.date)
    
    def plus(self, days=None, years=None):
        days=days or 0
        years=years or 0
        newyear=self.date.year+years
        t=self.date+datetime.timedelta(days=days)
        return str(datetime.date(newyear, day=t.day, month=t.month))
    
    def vlink(self, text=None):
        if not text:
            text=str(self.date)+' '+datetime.datetime.strftime(self.date, '%a')
        return '<a class="btn" href="/aday/%s/">%s</a>'%(str(self.date), text)
    
    def day(self):
        return datetime.datetime.strftime(self.date, '%A')
    
    def getmeasurements(self):
        try:
            from workout.models import Measurement
            nextday=self.date+datetime.timedelta(days=1)
            return Measurement.objects.filter(created__gte=self.date, created__lt=nextday).order_by('place__domain','place__name')
        except:
            return []
        
    def getworkouts(self):
        try:
            from workout.models import Workout
            nextday=self.date+datetime.timedelta(days=1)
            return Workout.objects.filter(created__gte=self.date, created__lt=nextday)
        except:
            return []
        
        
    
class PersonDay(DayModel):
    person=models.ForeignKey(Person, related_name='persondays')
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
        return (self.text and len(self.text)/3+100) or '120'
    
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