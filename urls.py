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
    url(r'^do_measurementset/(?P<measurementset_id>[0-9]+)$', 'tracker.workout.views.do_measurementset', name='do_set_id'),
    url(r'^make_workout','tracker.workout.views.make_workout',name='make_workout'),
)

