import datetime

from django.db import models
from django.contrib import admin
from buy.models import Person

from trackerutils import DayModel, debu

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
        except Exception, e:
            print 'bad'
            return []

    def getworkouts(self):
        try:
            from workout.models import Workout
            nextday=self.date+datetime.timedelta(days=1)
            return Workout.objects.filter(created__gte=self.date, created__lt=nextday)
        except Exception, e:
            print 'bad get workouts.'
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