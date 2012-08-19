import datetime

from django.db import models
from django.contrib import admin
# Create your models here.
from buy.models import Person

from trackerutils import DayModel

class Tag(DayModel):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    #day=models.ForeignKey('Day')
    class Meta:
        db_table='tag'
        
    def __unicode__(self):
        return self.name
    
    def html(self):
        return '<div class="tag">%s%s</div>'%(self.name, self.day)
    
class TagDay(DayModel):
    day=models.ForeignKey('Day', related_name='tagdays')
    tag=models.ForeignKey('Tag', related_name='tagdays')
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='tagday'

class TagDayInline(admin.StackedInline):
    model=TagDay
    
class Day(DayModel):
    date=models.DateField()
    text=models.TextField()
    #inlines=[TagDayInline,]
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='day'
        
    def __unicode__(self):
        return str(self.date)
    
    def tomorrow(self):
        t=datetime.timedelta(days=1)+self.date
        return str(datetime.date(year=t.year, day=t.day, month=t.month))
    
    def yesterday(self):
        y=self.date-datetime.timedelta(days=1)
        return str(datetime.date(year=y.year, day=y.day, month=y.month))
    
class PersonDay(DayModel):
    person=models.ForeignKey(Person, related_name='persondays')
    day=models.ForeignKey('Day', related_name='persondays')
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='personday'
        
    def __unicode__(self):
        return '%s%s'%(self.person, str(self.day))
    
