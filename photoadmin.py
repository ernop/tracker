import datetime, tempfile, shutil, os

from django import forms
from django.contrib import admin, messages
from django.conf import settings
from django.db.models import Sum
from django.forms.models import BaseModelFormSet, BaseInlineFormSet

#import djangoplus.widgets
#from spark import *
LG=[700, 427]
MED=[340,200]
SM=[200,100]
from choices import *
from trackerutils import *
from utils import *
from day.models import *
#from tracker.utils import adminify, mk_default_field, nowdate, rstripz, mk_default_fkfield, rstripzb
from admin_helpers import *

class PhotoAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    list_display='id myname myday myinfo myexif'.split()
    #list_filter=' product__domain currency source who_with'.split()
    list_filter='camera incoming setup myphoto iso'.split()
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    
    @debu
    def myday(self,obj):
        if obj.day:
            return obj.day.vlink()
        return ''
    
    @debu
    def myinfo(self,obj):
        dat=(('taken',obj.taken and obj.taken.strftime(DATE_DASH) or ''),
             ('created',obj.created.strftime(DATE_DASH)),
             ('modified',obj.modified.strftime(DATE_DASH)),
             ('incoming',icon(obj.incoming)),
             ('setup',icon(obj.setup)),
             ('myphoto',icon(obj.myphoto))
             )
        res=mktable(dat)
        return res
    
    def myname(self,obj):
        tags=', '.join([tag.tag.vlink() for tag in obj.tags.all()])
        dat=(('name',obj.name),
             ('fp',obj.fp),
             ('img',obj.inhtml(size='small',link=True)),
             ('tags',tags),)
        res=mktable(dat)
        return res
        
    
    @debu
    def myexif(self,obj):
        if obj.resolutionx and obj.resolutiony:
            size='%dx%d'%(obj.resolutionx,obj.resolutiony)
        else:
            size=''
        dat=(('camera',obj.camera),
             ('iso',obj.iso),
             ('mm',obj.mm),
             ('size',size),
             ('filesize',humanize_size(obj.filesize)),
             )
        res=mktable(dat)
        return res
    
    adminify(myday,myinfo,myexif,myname)

class PhotoTagAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    list_display='id name'.split()
    pass

class PhotoSpotAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    pass

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(PhotoSpot, PhotoSpotAdmin)
