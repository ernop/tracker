from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tracker/', include('tracker.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls),),
    url(r'^/?$', lambda x:HttpResponseRedirect('/admin/'), name='redir'),
    url(r'^do_measurementset/$', 'tracker.workout.views.do_measurementset', name='do_set'),
    url(r'^do_measurementset/(?P<measurementset_id>[0-9]+)/$', 'tracker.workout.views.do_measurementset', name='do_set_id'),
    url(r'^make_workout','tracker.workout.views.make_workout',name='make_workout'),
    url(r'^ajax/day_data/$','tracker.day.views.ajax_day_data',name='ajax_day_data'),
    url(r'^day/$','tracker.day.views.index',name='day'),
    url(r'^today/$','tracker.day.views.today',name='today'),
    url(r'^yesterday/$','tracker.day.views.yesterday',name='yesterday'),
    url(r'^y2day/$','tracker.day.views.y2day',name='y2day'),
    url(r'^aday/(?P<day>[0-9\-]+)/$','tracker.day.views.aday',name='aday'),
    url(r'^notekind/(?P<id>[0-9]+)/$','tracker.day.views.notekind',name='notekind'),
    url(r'^notekind/(?P<name>[a-z]+)/$','tracker.day.views.notekind',name='notekind'),

    #-------------------------------------------AJAX-------------------------------------------
    
    url(r'^ajax/get_purchases/$','tracker.day.ajax_views.ajax_get_purchases',name='ajax_get_purchases'),
    url(r'^ajax/make_purchase/$','tracker.day.ajax_views.ajax_make_purchase',name='ajax_make_purchase'),
)


