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
    list_display='id myname myinfo myexif'.split()
    #list_filter=' product__domain currency source who_with'.split()
    list_filter='deleted camera incoming setup myphoto iso'.split()
    list_filter.extend([PhotoHasDayFilter])
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    actions=['undoable_delete','undelete','reinitialize',]
    
    def reinitialize(self,request,queryset):
        for photo in queryset:
            photo.initialize()
    
    def undoable_delete(self,request,queryset):
        for photo in queryset:
            photo.undoable_delete()
        
    def undelete(self,request,queryset):
        for photo in queryset:
            photo.undelete()
    
    def myday(self,obj):
        if obj.day:
            return obj.day.vlink()
        return ''
    
    def myinfo(self,obj):
        return obj.info_table()
    @debu
    def myname(self,obj):
        return obj.name_table()
    
    def myexif(self,obj):
        return obj.exif_table()
    
    def queryset(self, request):
        queryset = super(PhotoAdmin, self).queryset(request)
        user=request.user
        #return queryset
        if can_access_private(user):
            pass
        else:
            queryset=queryset.exclude(tags__tag__name__in=settings.EXCLUDED_TAGS)
        return queryset
    
    adminify(myday,myinfo,myexif,myname)

class PhotoTagAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    list_display='id myname myphotos'.split()
    actions=['reinitialize_tags',]
    
    def queryset(self, request):
        queryset = super(PhotoTagAdmin, self).queryset(request)
        user=request.user
        if can_access_private(user):
            pass
        else:
            queryset=queryset.exclude(name__in=settings.EXCLUDED_TAGS)
        return queryset
    
    def reinitialize_tags(self,request,queryset):
        PhotoTag.setup_initial_tags()
        
    def myphotos(self,obj):
        res=[]
        ct=obj.photos.count()
        for pho in obj.photos.all()[:20]:
            realpho=pho.photo
            res.append(realpho.inhtml(size='small'))
        pres=''.join(res)
        alllink='<a href="../photos/?photohastag__photo__id=%d">All Photos</a>'%obj.id
        res='<div class="big">%d</div>%s<br>%s'%(ct,pres,alllink)
        return res
        
    def myname(self,obj):
        return obj.vlink()
        
    adminify(myname, myphotos)

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