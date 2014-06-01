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
    list_filter=[PhotoHasDayFilter, NullHashFilter,PhotoTaggedWithFilter, PhotoHasSpotFilter, PhotoDoneFilter,PhotoExtensionFilter,MyCameraFilter]+list_filter
    
    #date_hierarchy='created'
    #list_editable=['note',]
    search_fields= ['name']
    list_per_page=100
    date_hierarchy='taken'
    
    actions=['undoable_delete','not_myphoto','delete_file',
             'undelete','reinitialize','re_autoorient','force_recreate_thumbs',
             'autoorient','redo_classification','kill_entry',
             'unlink_from_day',]
    actions.extend(['remove_photospot','rehash',])
    actions.sort()
    
    def unlink_from_day(self,request,queryset):
        for pho in queryset:
            pho.day=None
            pho.save()
    
    def remove_photospot(self,request,queryset):
        for pho in queryset:
            pho.photospot=None
            pho.save()
    
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
    def rehash(self,request,queryset):
        for pic in queryset:
            pic.rehash()
            pic.save()
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
    
    def myname(self,obj):
        return obj.name_table(ajaxlink=True)
    
    myname.admin_order_field='hash'
    
    def myexif(self,obj):
        return obj.exif_table()+obj.links_table()
    
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
    list_display='id myname myphotos mytags'.split()
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
        sparkline=obj.history_sparkline()
        res=[]
        ct=obj.photos.count()
        for pho in obj.photos.order_by('photo__photo_created').all()[:80]:
            realpho=pho.photo
            res.append(realpho.inhtml(size='thumb'))
        pres=''.join(res)
        alllink='<a href="../photo/?tagged_with=%s">All Photos</a>'%obj.id
        res='<div class="big">%d</div><div style="display:inline-block;float:right;">%s</div>%s<br>%s'%(ct,sparkline,pres,alllink)
        return res
        
    def mytags(self,obj):
        '''co-occuring tags'''
        EXCLUDE_PHOTOTAGS='done next last autoorient'.split()
        photoids=[ph.id for ph in Photo.objects.filter(tags__tag=obj)]
        comma_separated_photoids=','.join([str(pid) for pid in photoids])
        bad_ptids=','.join([str(pt.id) for pt in PhotoTag.objects.filter(name__in=EXCLUDE_PHOTOTAGS)])
        grouped_tags=PhotoTag.objects.raw('select pt.id, pt.name,pt.use_count,count(*) as ct \
        from phototag pt \
        inner join photohastag pht on pht.tag_id=pt.id inner join photo p on \
        p.id=pht.photo_id where p.id in (%s) and pt.id not in (%s) group by 1 order by ct desc,pt.name'\
                                          %(comma_separated_photoids,bad_ptids))
        res=[]
        for n in range(20):
            try:
                gt=grouped_tags[n]
                if gt.id==obj.id:continue
                res.append((gt.id,'%s (%d)'%(gt.name,gt.use_count),gt.ct))
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
        
    
    
    
    adminify(myname, myphotos, mytags)

class PhotoSpotAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    list_editable=['name','tour_order', 'description',]
    search_fields= ['name']
    list_display='id myinfo name tour_order description  myphotos'.split()
    list_filter=['tour','tour_order',]
    actions=[]
    
    def make_assign(tn):
        def assign_guy(self,request,queryset):
            for photospot in queryset:
                photospot.tour=tn
                photospot.save()
        assign_guy.__name__=str(('assign to tour %s'%tn).replace(' ','_'))
        return assign_guy
    
    for guy in PhotoSpot.objects.all().values_list('tour').distinct():
        tourname=guy[0]
        actions.append(make_assign(tourname))
  
    def myinfo(self,obj):
        data=[('tour',obj.tour or ''),
              ('description',obj.description),
              ('photo count',obj.photos.count()),
              ('vlink',obj.vlink(text='vlink')),
              ]
        return mktable(data)
    
    def myphotos(self,obj):
        photos=[]
        for ph in obj.photos.order_by('taken')[:10]:
            photos.append(ph.inhtml(size='thumb', clink=True))
        return ''.join(photos)
    
    
    adminify(myinfo,myphotos)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(PhotoSpot, PhotoSpotAdmin)
