import datetime, tempfile, shutil, os

from django import forms
from django.contrib import admin, messages
from django.conf import settings
from django.db.models import Sum
from django.forms.models import BaseModelFormSet, BaseInlineFormSet

from choices import *
from trackerutils import *
from utils import *
from day.models import *
from admin_helpers import *

class PhotoAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    list_display='id myname myinfo myexif'.split()
    #list_filter=' product__domain currency source who_with'.split()
    list_filter=['incoming','deleted',PhotoHasDayFilter,PhotoDoneFilter,PhotoExtensionFilter, NullHashFilter,PhotoTaggedWithFilter, 
                 PhotoHasSpotFilter, MyCameraFilter,'iso','camera','thumb_ok','setup','myphoto']
    
    #date_hierarchy='created'
    #list_editable=['note',]
    search_fields= ['name']
    list_per_page=100
    date_hierarchy='photo_created'
    
    actions=['undoable_delete','not_myphoto','delete_file',
             'undelete','reinitialize','force_recreate_thumbs',
             'autoorient','redo_classification','kill_entry',
             'unlink_from_day','rename_name','remove_photospot',]
    actions.extend(['remove_photospot','remove_day','rehash','merge_photos_lowest_id','check_thumbs',])
    actions.append('set_founding')
    actions.sort()
    
    def set_founding(self,request,queryset):
        for ph in queryset:
            if ph.photospot:
                spot=ph.photospot
                spot.founding_photo=ph
                spot.save()
                messages.info(request,'set as founding photo')
            else:
                messages.error(request,'this photo has no spot')
                
    def rename_name(self, request, queryset):
        for ph in queryset:
            for n in range(5):
                ph.name+=getletter()
            ph.save()
            
    def remove_photospot(self, request, queryset):
        for ph in queryset:
            ph.photospot=None
            ph.save()
    
    def merge_photos_lowest_id(self, request, queryset):
        lowest=queryset.order_by('-filesize')[0]
        #combine tags & undoable delete the others
        has=[t.tag.name for t in lowest.tags.all()]
        for other in queryset.exclude(id=lowest.id):
            tags=other.tags.all()
            for ot in tags:
                if ot.tag.name not in has:
                    ht=PhotoHasTag(tag=ot.tag,photo=lowest)
                    ht.save()
            lowest.photo_created=min(lowest.photo_created,other.photo_created)
            lowest.created=min(lowest.created,other.created)
            lowest.photo_modified=min(lowest.photo_modified,other.photo_modified)
            if other.taken and not lowest.taken:
                lowest.taken=other.taken
            other.kill_this()
        lowest.save()
    
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
            
    def autoorient(self,request,queryset):
        for photo in queryset:
            photo.autoorient()
    
    
    def remove_day(self,request,queryset):
        for ph in queryset:
            ph.day=None
            ph.save()
    
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
    
    def undoable_delete(self,request,queryset):
        for photo in queryset:
            photo.undoable_delete()
            
    def force_recreate_thumbs(self,request,queryset):
        for photo in queryset:
            photo.create_thumb(force=True)
    
    def check_thumbs(self,request,queryset):
        for photo in queryset:
            photo.create_thumb()
            
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
        et=obj.exif_table()
        lt=obj.links_table()
        return '%s %s'%(et,lt)
    
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
    actions=['reinitialize_tags','create_people_tags','redo_classification','kill_all_days',]
    
    def kill_all_days(self,request,queryset):
        for ptag in queryset:
            photos=ptag.photos.all()
            for ph in photos:
                if ph.photo.day:
                    dd=ph.photo
                    dd.day=None
                    dd.save()
            messages.info(request,'killed all days for related %d photos for %s'%(ptag.photos.count(),ptag))
        
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
        done_ids=set()
        for pho in obj.photos.order_by('photo__photo_created').all()[:80]:
            if pho.photo.id in done_ids:
                continue
            realpho=pho.photo
            res.append(realpho.inhtml(size='thumb'))
            done_ids.add(pho.photo.id)
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
        return mktable(res2,nb=True)
        
    def myname(self,obj):
        have_day_count=(obj.photos.exclude(photo__day=None).count())
        data=(('vlink',obj.vlink()),
              ('use count',obj.use_count),
              ('person clink',obj.person and '%s'%(obj.person.clink()) or ''),
              ('photoset','<a href="/photo/photoset/%s/">%s</a>'%(obj.name,obj.name)),
              ('have day','<a href="../photo/?has_taken_day=yes&tagged_with=%d">have day (%d)</a>'%(obj.id,have_day_count)),
              )
        return mktable(data)
    adminify(myname, myphotos, mytags)

class PhotoSpotAdmin(OverriddenModelAdmin):
    #list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    #list_filter=' product__domain currency source who_with'.split()
    #date_hierarchy='created'
    list_editable=['name',]
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
        data=[('tour',obj.tour or 'no tour'),
              ('description',obj.description or ''),
              ('photo count',obj.photos.count()),
              (obj.vlink(text='spotpage')),
              ]
        return mktable(data,skip_false=True)
    
    def myphotos(self,obj):
        photos=[]
        for ph in obj.photos.order_by('taken')[:10]:
            if ph==obj.founding_photo:
                photos.append(div(contents=ph.inhtml(size='thumb', clink=True),klass='founding-photo'))
            else:
                photos.append(ph.inhtml(size='thumb', clink=True))
        return ''.join(photos)
    
    
    adminify(myinfo,myphotos)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(PhotoSpot, PhotoSpotAdmin)
