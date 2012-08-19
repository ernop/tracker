#import django.forms import Model
from django import forms
from tracker.day.models import Day

class DayForm(forms.ModelForm):
    
    class Meta:
        model=Day