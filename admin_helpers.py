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

class MyCameraFilter(SimpleListFilter):
    title='My Camera'
    parameter_name='mycam'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    
    def queryset(self, request, queryset):
        NEXUS='Nexus S'
        CANON='Canon EOS 500D'
        if self.value()=='yes':
            return queryset.filter(camera=NEXUS)|queryset.filter(camera=CANON)
        elif self.value()=='no':
            return queryset.exclude(camera=NEXUS).exclude(camera=CANON).exclude(camera=None).exclude(camera='')

class PhotoExtensionFilter(SimpleListFilter):
    title='extension'
    parameter_name='extension'
    def lookups(self, request, model_admin):
        return (
            ('jpg', 'jpg'),
            ('gif', 'gif'),
            ('png', 'png'),
            ('webp', 'webp'),
        )
    
    def queryset(self, request, queryset):
        if self.value()=='jpg':
            return queryset.filter(fp__endswith='.jpg')
        elif self.value()=='gif':
            return queryset.filter(fp__endswith='.gif')
        elif self.value()=='png':
            return queryset.filter(fp__endswith='.png')
        elif self.value()=='webp':
            return queryset.filter(fp__endswith='.webp')

class PhotoDoneFilter(SimpleListFilter):
    title = 'photo done'
    parameter_name = 'photo_done'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.filter(tags__tag__name='done')
        elif self.value()=='no':
            return queryset.exclude(tags__tag__name='done')

class TagHasPersonFilter(SimpleListFilter):
    title = 'has person'
    parameter_name = 'has_person'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(person=None)
        elif self.value()=='no':
            return queryset.filter(person=None)

class PhotoTaggedWithFilter(SimpleListFilter):
    title = 'tagged with'
    parameter_name = 'tagged_with'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        val=self.value()
        if val:
            return queryset.filter(tags__tag__id=val)

class PhotoHasSpotFilter(SimpleListFilter):
    title = 'has photospot'
    parameter_name = 'has_photospot'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(photospot=None)
        elif self.value()=='no':
            return queryset.filter(photospot=None)

class NullHashFilter(SimpleListFilter):
    title = 'has a hash'
    parameter_name = 'has hash'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(hash=None).exclude(hash='')
        elif self.value()=='no':
            return queryset.filter(hash=None)
        
class PhotoHasDayFilter(SimpleListFilter):
    title = 'has taken day'
    parameter_name = 'has_taken_day'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(day=None)
        elif self.value()=='no':
            return queryset.filter(day=None)

class NoteHasKinds(SimpleListFilter):
    title = 'has kinds'
    parameter_name = 'has_kinds'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(kinds=None)
        elif self.value()=='no':
            return queryset.filter(kinds=None)

class HasNoteFilter(SimpleListFilter):
    title = 'has note'
    parameter_name = 'has_note'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(notes=None)
        elif self.value()=='no':
            return queryset.filter(notes=None)

class HasPurchFilter(SimpleListFilter):
    title = 'has purch'
    parameter_name = 'has_purch'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(purchases=None)
        elif self.value()=='no':
            return queryset.filter(purchases=None)
        
class NoteHasText(SimpleListFilter):
    title = 'has text'
    parameter_name = 'has_text'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(text=None).exclude(text='')
        elif self.value()=='no':
            return queryset.filter(text='')|queryset.filter(text=None)

class AnyPurchaseFilter(SimpleListFilter):
    title = 'Any Purchase?'
    parameter_name = 'any_purchase'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(purchases=None)
        elif self.value()=='no':
            return queryset.filter(purchases=None)

class KnownSinceLongAgo(SimpleListFilter):
    title = 'Known Since Long Ago'
    parameter_name = 'known_long'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        from django.conf import settings
        if self.value()=='yes':
            return queryset.filter(created=settings.LONG_AGO)
        elif self.value()=='no':
            return queryset.exclude(created=settings.LONG_AGO)

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
