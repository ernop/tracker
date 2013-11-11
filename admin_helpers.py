import datetime, operator

from django.contrib import admin
from django import forms
from django.forms import widgets
#from django.utils.translation import ugettext_lazy as _
#from django.contrib.admin import SimpleListFilter
from django.forms.models import BaseModelFormSet
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.views.main import SuspiciousOperation, ImproperlyConfigured, IncorrectLookupParameters
from django.contrib.admin.util import lookup_needs_distinct
from django.db.models import Q, Count

class GenderFilter(SimpleListFilter):
    title = 'gender'
    parameter_name = 'gender'
    def lookups(self, request, model_admin):
        return (
            ('male', 'male'),
            ('female', 'female'),
            ('org', 'org'),
            ('none', 'none'),
        )
    def queryset(self, request, queryset):
        if self.value()=='male':
            return queryset.filter(gender=1)
        elif self.value()=='female':
            return queryset.filter(gender=2)
        elif self.value()=='org':
            return queryset.filter(gender=3)
        elif self.value()=='none':
            return queryset.filter(gender=None)
