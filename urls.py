from django.contrib import admin
admin.autodiscover()

import logging
log=logging.getLogger(__name__)

from django.conf.urls import *
from django.http import HttpResponseRedirect
from day.models import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls),),
    url(r'^do_measurementset/$', 'day.views.do_measurementset', name='do_set'),
    url(r'^do_measurementset/(?P<measurementset_id>[0-9]+)/$', 'day.views.do_measurementset', name='do_set_id'),
    url(r'^make_workout','day.views.make_workout',name='make_workout'),
    url(r'^ajax/day_data/$','day.views.ajax_day_data',name='ajax_day_data'),
    url(r'^day/$','day.views.index',name='day'),
    url(r'^today/$','day.views.today',name='today'),
    url(r'^yesterday/$','day.views.yesterday',name='yesterday'),
    url(r'^y2day/$','day.views.y2day',name='y2day'),
    url(r'^aday/(?P<day>[0-9\-]+)/$','day.views.aday',name='aday'),
    url(r'^states/$','day.states.states',name='states'),
    url(r'^amonth/(?P<month>[0-9\-]+)/$','day.views.amonth', name='amonth'),

    url(r'^notekind/(?P<id>[0-9]+)/$','day.views.notekind',name='notekind'),
    url(r'^notekind/(?P<name>[a-z]+)/$','day.views.notekind',name='notekind'),

    url(r'^people_connections/$','day.views.people_connections',name='people_connections'),
    url(r'^recent_connections/$','day.views.recent_connections',name='recent_connections'),
    url(r'^month_connections/$','day.views.month_connections',name='month_connections'),
    url(r'^initial_annual/$','day.views.initial_annual',name='initial_annual'),
    url(r'^anon_annual/$','day.views.anon_annual',name='anon_annual'),

    #-------------------------------------------AJAX-------------------------------------------

    url(r'^ajax/get_purchases/$','day.ajax_views.ajax_get_purchases',name='ajax_get_purchases'),
    url(r'^ajax/get_popular/$','day.ajax_views.ajax_get_popular',name='ajax_get_popular'),
    url(r'^ajax/make_purchase/$','day.ajax_views.ajax_make_purchase',name='ajax_make_purchase'),
    url(r'^ajax/serve_mp3/(?P<mp3_filename>.*)/$','day.ajax_views.ajax_serve_mp3',name='ajax_serve_mp3'),
    url(r'^ajax/receive_mp3/(?P<note_id>.*)/$','day.ajax_views.ajax_receive_mp3',name='ajax_receive_mp3'),
    url(r'^ajax/get_measurements/$','day.ajax_views.ajax_get_measurements',name='ajax_get_measurements'),
    url(r'^ajax/make_measurement/$','day.ajax_views.ajax_make_measurement',name='ajax_make_measurement'),
    #url(r'^ajax/get_founding_for_spot/$','day.ajax_views.ajax_get_founding_for_spot',name='ajax_get_founding_for_spot'),
        url(r'^/?$', 'day.views.redir', name='redir'),

    #--------------------------D3 jumping.-----------------------------------
    url(r'^person/d3/(?P<id>[0-9]+)/$','day.jumping.jumping_person',name='jumping_person'),
    url(r'^source/d3/(?P<id>[0-9]+)/$','day.jumping.jumping_source',name='jumping_source'),
    url(r'^product/d3/(?P<id>[0-9]+)/$','day.jumping.jumping_product',name='jumping_product'),
    
    url(r'^photo/stats/$','day.photoviews.photostats', name='photostats'),
    url(r'^photo/dups/$','day.photoviews.photodups', name='photodups'),
    url(r'^photo/hashes/$','day.photoviews.photohashdups', name='photohashdups'),
    url(r'^photo/photo/(?P<id>[0-9]+)/$','day.photoviews.photo',name='photo'),
    url(r'^photo/phototag/(?P<name>[a-zA-Z_\-0-9 \%]+)/$','day.photoviews.phototag',name='phototag'),
    url(r'^photo/phototag_id/(?P<id>[\d]+)/$','day.photoviews.phototag_id',name='phototag_id'),
    url(r'^photo/photospot/(?P<name>[a-zA-Z_\-0-9 \%]+)/$','day.photoviews.photospot',name='photospot'),
    url(r'^photo/incoming/$','day.photoviews.incoming',name='photospot'),
    url(r'^photo_passthrough/(?P<id>[0-9]+).(jpg|gif|webp|png)$','day.photoviews.photo_passthrough',name='photo_passthrough'),
    url(r'^photo_thumb_passthrough/(?P<id>[0-9]+).(jpg|gif|webp|png)$','day.photoviews.photo_thumb_passthrough',name='photo_thumb_passthrough'),
    url(r'^ajax/photo_data/$','day.photoviews.ajax_photo_data',name='ajax_photo_data'),
    url(r'^photo/photoajax/$','day.photoviews.photoajax',name='ajax_photoajax'),
    #url(r'^photo/photospotajax/$','day.photoviews.incoming_photospot_photos_ajax',name='ajax_photospotajax'),
    url(r'^photo/photoset/(?P<tagset>.*)/','day.photoviews.photoset')
)



