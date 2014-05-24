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
    list_filter='thumb_ok deleted incoming setup myphoto iso camera'.split()
    list_filter=[PhotoHasDayFilter, PhotoTaggedWithFilter, PhotoHasSpotFilter, PhotoDoneFilter,PhotoExtensionFilter,MyCameraFilter]+list_filter
    
    #date_hierarchy='created'
    #list_editable=['note',]
    search_fields= ['name']
    list_per_page=100
    actions=['undoable_delete','not_myphoto','delete_file','undelete','reinitialize','re_autoorient','force_recreate_thumbs','autoorient','redo_classification','kill_entry',]
    
    def redo_classification(self,request,queryset):
        for photo in queryset:
            photo.tags.delete()
            photo.incoming=True
            photo.save()
            
    def reinitialize(self,request,queryset):
        for photo in queryset:
            photo.initialize()
            
    def not_myphoto(self,request,queryset):
        for photo in queryset:
            photo.day=None
            photo.myphoto=False
            photo.save()
            
    def re_autoorient(self,request,queryset):
        for photo in queryset:
            photo.auto_orient()
    
    
    def kill_entry(self,request,queryset):
        for photo in queryset:
            photo.kill_this()
    
    def delete_file(self,request,queryset):    
        for photo in queryset:
            photo.delete_file()
            
    def autoorient(self,request,queryset):    
        for photo in queryset:
            photo.autoorient()
    
    def undoable_delete(self,request,queryset):
        for photo in queryset:
            photo.undoable_delete()
            
    def force_recreate_thumbs(self,request,queryset):
        for photo in queryset:
            photo.create_thumb(force=True)
        
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
    search_fields= ['name']
    list_filter=['control_tag', TagHasPersonFilter]
    list_display='id myname myphotos myhistory mytags'.split()
    actions=['reinitialize_tags','create_people_tags','redo_classification']
    
    def redo_classification(self,request,queryset):
        for phototag in queryset:
            for photo in Photo.objects.filter(tags__tag=phototag):
                photo.tags.all().delete()
                photo.incoming=True
                photo.save()
   
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
        PhotoTag.setup_people_tags()
        PhotoTag.update_tag_counts()
        
    def myphotos(self,obj):
        res=[]
        ct=obj.photos.count()
        for pho in obj.photos.all()[:50]:
            realpho=pho.photo
            res.append(realpho.inhtml(size='thumb'))
        pres=''.join(res)
        alllink='<a href="../photo/?tagged_with=%s">All Photos</a>'%obj.id
        res='<div class="big">%d</div>%s<br>%s'%(ct,pres,alllink)
        return res
        
    def mytags(self,obj):
        '''co-occuring tags'''
        #import ipdb;ipdb.set_trace()
        photos=Photo.objects.filter(tags__tag=obj)
        photoids=[ph.id for ph in photos]
        reltags=PhotoTag.objects.filter(photos__photo__id__in=photoids).distinct()
        comma_separated_photoids=','.join([str(pid) for pid in photoids])
        grouped_tags=PhotoTag.objects.raw('select pt.id, pt.name,count(*) as ct \
        from phototag pt \
        inner join photohastag pht on pht.tag_id=pt.id inner join photo p on \
        p.id=pht.photo_id where p.id in (%s) group by 1 order by ct desc,pt.name'\
                                          %comma_separated_photoids)
        res=[]
        for n in range(20):
            try:
                gt=grouped_tags[n]
                res.append((gt.id,gt.name,gt.ct))
            except:
                break
        res2=[('<h2>Related Tags</h2>')]
        
        for rr in res:
            res2.append(('<a href="/admin/day/phototag/?id=%d">%s</a>'%(rr[0],rr[1]),rr[2]))
        return mktable(res2)
        
    def myname(self,obj):
        data=(('vlink',obj.vlink()),
              ('use count',obj.use_count),
              ('person clink',obj.person and '%s'%(obj.person.clink()) or ''),
              )
        return mktable(data)
        
    
    def myhistory(self,obj):
        #photos=Photo.objects.filter(tags__tag=obj)
        photos=Photo.objects.raw('select p.id,date(p.created) as date,\
        count(*) as ct from photo p inner join \
        photohastag pht on pht.photo_id=p.id inner join phototag pt on \
        pt.id=pht.tag_id group by 2')
        nn=0
        res={}
        md=settings.LONG_AGO
        while 1:
            
            try:
                pho=photos[nn]
                nn+=1
                res[datetime.datetime.strftime(pho.date,DATE)]=pho.ct
                md=min(md,pho.date)
            except IndexError,e:
                break
        #
        dat2=group_day_dat(res,by='month',mindate=md)
        #
        from admin import nice_sparkline
        spl=nice_sparkline(dat2,500,300)
        return spl
    
    
    adminify(myname, myphotos, mytags,myhistory)

class PhotoSpotAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    #list_editable=['note',]
    #search_fields= ['name']
    list_display='id mylinks'.split()
    def mylinks(self,obj):
        data=[('vlink',obj.vlink()),
              ('count',obj.photos.count()),
              ]
        
        return mktable(data)
    adminify(mylinks)
    pass

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(PhotoSpot, PhotoSpotAdmin)
