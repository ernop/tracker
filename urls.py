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
    url(r'^do_measurementset/$', 'tracker.day.views.do_measurementset', name='do_set'),
    url(r'^do_measurementset/(?P<measurementset_id>[0-9]+)/$', 'tracker.day.views.do_measurementset', name='do_set_id'),
    url(r'^make_workout','tracker.day.views.make_workout',name='make_workout'),
    url(r'^ajax/day_data/$','tracker.day.views.ajax_day_data',name='ajax_day_data'),
    url(r'^day/$','tracker.day.views.index',name='day'),
    url(r'^today/$','tracker.day.views.today',name='today'),
    url(r'^yesterday/$','tracker.day.views.yesterday',name='yesterday'),
    url(r'^y2day/$','tracker.day.views.y2day',name='y2day'),
    url(r'^aday/(?P<day>[0-9\-]+)/$','tracker.day.views.aday',name='aday'),
    url(r'^states/$','tracker.day.states.states',name='states'),
    url(r'^amonth/(?P<month>[0-9\-]+)/$','tracker.day.views.amonth', name='amonth'),

    url(r'^notekind/(?P<id>[0-9]+)/$','tracker.day.views.notekind',name='notekind'),
    url(r'^notekind/(?P<name>[a-z]+)/$','tracker.day.views.notekind',name='notekind'),

    url(r'^people_connections/$','tracker.day.views.people_connections',name='people_connections'),
    url(r'^recent_connections/$','tracker.day.views.recent_connections',name='recent_connections'),

    #-------------------------------------------AJAX-------------------------------------------

    url(r'^ajax/get_purchases/$','tracker.day.ajax_views.ajax_get_purchases',name='ajax_get_purchases'),
    url(r'^ajax/get_popular/$','tracker.day.ajax_views.ajax_get_popular',name='ajax_get_popular'),
    url(r'^ajax/make_purchase/$','tracker.day.ajax_views.ajax_make_purchase',name='ajax_make_purchase'),

    url(r'^ajax/get_measurements/$','tracker.day.ajax_views.ajax_get_measurements',name='ajax_get_measurements'),
    url(r'^ajax/make_measurement/$','tracker.day.ajax_views.ajax_make_measurement',name='ajax_make_measurement'),
    url(r'^/?$', 'tracker.day.views.redir', name='redir'),

    #--------------------------D3 jumping.-----------------------------------
    url(r'^person/d3/(?P<id>[0-9]+)/$','tracker.day.jumping.jumping_person',name='jumping_person'),
    url(r'^source/d3/(?P<id>[0-9]+)/$','tracker.day.jumping.jumping_source',name='jumping_source'),
    url(r'^product/d3/(?P<id>[0-9]+)/$','tracker.day.jumping.jumping_product',name='jumping_product'),
    
    url(r'photo/photo/(?P<id>[0-9]+)/$','tracker.day.photoviews.photo',name='photo'),
    url(r'photo/phototag/(?P<name>[a-zA-Z_\-0-9]+)/$','tracker.day.photoviews.phototag',name='phototag'),
    url(r'photo/photospot/(?P<slug>[a-zA-Z_\-0-9]+)/$','tracker.day.photoviews.photospot',name='photospot'),
    url(r'photo/incoming/$','tracker.day.photoviews.incoming',name='photospot'),
    url(r'photo_passthrough/(?P<id>[0-9]+)/$','tracker.day.photoviews.photo_passthrough',name='photo_passthrough'),
    url(r'^ajax/photo_data/$','tracker.day.photoviews.ajax_photo_data',name='ajax_photo_data'),
)



