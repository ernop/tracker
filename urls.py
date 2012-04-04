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
    #url(r'.*', lambda x:HttpResponseRedirect('/admin/'), name='redir'),
)
