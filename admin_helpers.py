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

def make_null_filter(field, title=None, param_name=None, include_empty_string=True):
    if not title:
        title = 'null filter for %s' % field
    if not param_name:
        param_name = 'has_'+''.join([c for c in field if c.isalpha()])
    '''rather than making a whole class for these, just make them on the fly...'''
    bb = title
    if include_empty_string:
        use_klass = BaseNullEmptyFilter
    else:
        use_klass = BaseNullFilter

    class InnerFilter(use_klass):
        title= bb
        parameter_name= param_name
        args={field:None}
    return InnerFilter


def construct_querystring_without_field(request, field):
    q = request.GET.copy()
    del q[field]
    return q

def make_untoggle_link(request, field):
    qs = construct_querystring_without_field(request, field)
    newqs = qs.urlencode()
    return '<a href=%s?%s>X</a>' % (request.path, newqs)

from django.contrib import admin
class OverriddenModelAdmin(admin.ModelAdmin):
    """normal, except overrides some widgets."""
    formfield_overrides = {
        #models.DateTimeField: {'widget': admin.widgets.AdminDateWidget,},
        #models.DateField: { 'widget': admin.widgets.AdminDateWidget,},
        #models.DateTimeField: {'widget': BetterDateWidget,},
        #models.DateField: { 'widget': BetterDateWidget,},
    }

    def _media(self):
        from django.forms import Media
        js = ("/static/admin/js/core.js","/static/admin/js/admin/RelatedObjectLookups.js",
              '/static/admin/js/jquery.js',"/static/admin/js/jquery.init.js",
              "/static/admin/js/actions.js",
              '/static/admin/js/calendar.js',
              '/static/admin/js/admin/DateTimeShortcuts.js',
              '/static/js/jquery-1.7.2.min.js',
              '/static/js/DjangoAjax.js',
              '/static/js/jquery.sparkline.min.js',
              '/static/js/admin_init.js',
              )
        #css=('/static/css/select2.css',)
        med=Media(js=js)
        return med

    media=property(_media)

    #def changelist_view(self, request, extra_context=None):
        ##the way searches work in django is fucking stupid.
        ##when you view by ID and then apply a filter/search it doesn't cancel the previous ID.  so you get no results
        ##and confuse yourself.
        #if request.GET.has_key('id'):
            ##delete id parameter if there are other filters! yes!
            #real_keys = [k for k in request.GET.keys() if k not in getattr(self, 'not_count_filters', [])]
            #if len(real_keys) != 1:
                #q = request.GET.copy()
                #del q['id']
                #request.GET = q
                #request.META['QUERY_STRING'] = request.GET.urlencode()
        #return super(OverriddenModelAdmin,self).changelist_view(request, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        '''rewriting this to sometimes kill the "ID" filter when you click on another one.'''
        if request.GET.has_key('id'):
            #delete id parameter if there are other filters! yes!
            real_keys = [k for k in request.GET.keys() if k not in getattr(self, 'not_count_filters', [])]
            if len(real_keys) != 1:
                q = request.GET.copy()
                del q['id']
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
        if request.method == 'GET':
            '''re-create a changelist, get the filter specs, and put them into the
            request somewhere to be picked up by a future edit to the change list template,
            which would allow them to be displayed for all normal changelist_view pages'''
            #this is so that I can display filters on the top of the page for easy cancelling them.

            if request.GET.has_key('_changelist_filters'):
                qq = request.GET.copy()
                del qq['_changelist_filters']
                log.info('killed extraneous weird filter thingie which would have caused a 500 error.')
                request.GET = qq

            ChangeList = self.get_changelist(request)
            list_display = self.get_list_display(request)
            list_display_links = self.get_list_display_links(request, list_display)
            from django.contrib.admin import options
            list_filter = self.get_list_filter(request)
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
            used_filters = [xx for xx in cl.filter_specs if xx.used_parameters]
            filter_descriptions = []
            from django.contrib.admin.filters import BooleanFieldListFilter
            if 'id' in request.GET:
                desc = ('id', request.GET['id'], make_untoggle_link(request, 'id'))
                filter_descriptions.append(desc)
            for key in request.GET.keys():
                if key.endswith('__id'):
                    desc = ('%s id' % key.split('__')[0], request.GET[key], make_untoggle_link(request, key))
                    filter_descriptions.append(desc)
            for uf in used_filters:
                if type(uf) == BooleanFieldListFilter:
                    current_val = bool(int(uf.used_parameters.values()[0]))
                    if current_val:
                        desc = (uf.title, current_val, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                    else:
                        desc = (uf.title, current_val, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                    filter_descriptions.append(desc)
                else:
                    try:
                        current_val = uf.used_parameters.values()[0]
                        choice = None
                        if getattr(uf, 'lookup_choices', False):
                            got = False
                            #looking up the "descriptive" way to describe the value.
                            for choice in uf.lookup_choices:
                                if choice[0] == current_val:
                                    choice = choice[1]
                                    break
                                try:
                                    int(current_val)
                                    if choice[0] == int(current_val):
                                        choice = choice[1]
                                        break
                                except ValueError:
                                    pass
                                try:
                                    float(current_val)
                                    if choice[0] == float(current_val):
                                        choice = choice[1]
                                        break
                                except ValueError:
                                    pass
                            if not choice:
                               from utils import ipdb;ipdb() 
                        else:
                            choice = uf.used_parameters.keys()[0]
                            choice = current_val
                        desc = (uf.title, choice, make_untoggle_link(request, uf.used_parameters.items()[0][0]))
                        filter_descriptions.append(desc)
                    except Exception, e:
                        from utils import ipdb;ipdb()
            if request.GET and 'q' in request.GET:
                desc = ('Searching for', "\"%s\"" % request.GET['q'], make_untoggle_link(request, 'q'))
                filter_descriptions.append(desc)
            #import ipdb;ipdb.set_trace()
            request.filter_descriptions = filter_descriptions
        sup=super(OverriddenModelAdmin,self)
        return sup.changelist_view(request, extra_context=extra_context)



class BaseNullEmptyFilter(SimpleListFilter):
    '''an easy way to construct filters that are like __isnull'''
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        sargs=self.args
        if self.value()=='yes':
            for k in self.args.keys():
                queryset = queryset.exclude(**{k: '',})
                queryset = queryset.exclude(**{k: None,})
            return queryset
        if self.value()=='no':
            for k in self.args.keys():
                queryset = queryset.filter(**{k: '',}) | queryset.filter(**{k: None,})
            return queryset

class BaseNullFilter(SimpleListFilter):
    '''an easy way to construct filters that are like __isnull'''
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        sargs=self.args
        if self.value()=='yes':
            return queryset.exclude(**self.args)
        if self.value()=='no':
            return queryset.filter(**self.args)

PHOTO_SIZES=(
            (3*1024,'3k',),
            (10*1024,'10k', ),
            (25*1024,'25k', ),
            (50*1024,'50k', ),
            (100*1024,'100k', ),
            (150*1024,'150k', ),
            (250*1024,'250k', ),
            (500*1024,'500k', ),
            (1024*1024,'1m', ),
            ( 2048*1024,'2m',),
        )

class PhotoSizeFilterGreaterThan(SimpleListFilter):
    title='size greater than'
    parameter_name='size_gt'
    def lookups(self, request, model_admin):
        return PHOTO_SIZES
    
    def queryset(self, request, queryset):
        val=self.value()
        if val:
            val=int(val)
            for bits,name in PHOTO_SIZES:
                if bits==val:
                    comparator=bits
                    break
            return queryset.filter(filesize__gte=comparator)
        
class PhotoSizeFilterLessThan(SimpleListFilter):
    title='size less than'
    parameter_name='size_lt'
    def lookups(self, request, model_admin):
        return PHOTO_SIZES
    
    def queryset(self, request, queryset):
        val=self.value()
        if val:
            val=int(val)
            for bits,name in PHOTO_SIZES:
                if bits==val:
                    comparator=bits
                    break
            return queryset.filter(filesize__lte=comparator)

class MyCameraFilter(SimpleListFilter):
    title='My Camera'
    parameter_name='mycam'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    
    def queryset(self, request, queryset):
        from settings import MYCAMERAS
        if self.value()=='yes':
            return queryset.filter(camera__in=MYCAMERAS)
            #return queryset.filter(camera=NEXUS)|queryset.filter(camera=CANON)|queryset.filter(camera=OLDCAM)|queryset.filter(camera=GALAXYNOTE)
        elif self.value()=='no':
            return queryset.exclude(camera__in=MYCAMERAS)
            #return queryset.exclude(camera=NEXUS).exclude(camera=CANON).exclude(camera=OLDCAM).exclude(camera=GALAXYNOTE).exclude(camera=None).exclude(camera='')

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
    title = 'photo done tag'
    parameter_name = 'photo_done_tag'
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

class DecadeFilter(SimpleListFilter):
    title = "Decade"
    parameter_name='decade'
    def lookups(self,request,model_admin):
        return ((nn*10, str(nn*10)+'s') for nn in range(0, 9))
    
    def queryset(self, request, queryset):
        if self.value():
            today=datetime.datetime.today()
            lower=today-datetime.timedelta(days=(int(self.value())+10)*365)
            higher=lower+datetime.timedelta(days=10*365)
            return queryset.filter(birthday__gte=lower, birthday__lt=lower+datetime.timedelta(days=365))    

class AgeFilter(SimpleListFilter):
    title="Age"
    parameter_name="age"
    def lookups(self,request,model_admin):
        return ((nn,nn) for nn in range(10, 70))
    
    def queryset(self, request, queryset):
        if self.value():
            lower=datetime.datetime.today()-datetime.timedelta(days=365*int(self.value())+1)
            return queryset.filter(birthday__gte=lower, birthday__lt=lower+datetime.timedelta(days=365))

class HasPhotoFilter(SimpleListFilter):
    title = 'Has Photos'
    parameter_name = 'has_photo'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
            ('no', 'no'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            return queryset.exclude(as_tag__photos=None)
        elif self.value()=='no':
            return queryset.filter(as_tag__photos=None)

class AnyPurchaseFilter(SimpleListFilter):
    title = 'Has Purchase'
    parameter_name = 'has_purchase'
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

class LastWeekPurchaseFilter(SimpleListFilter):
    title = 'Last Week'
    parameter_name = 'lastweek'
    def lookups(self, request, model_admin):
        return (
            ('yes', 'yes'),
        )
    def queryset(self, request, queryset):
        if self.value()=='yes':
            now=datetime.datetime.now()
            weekago=(now-datetime.timedelta(days=7)).date()
            weekago=datetime.datetime(year=weekago.year,month=weekago.month,day=weekago.day,hour=0,minute=0)
            return queryset.filter(created__gt=weekago).filter(created__lt=now).order_by('-created')

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
