import datetime

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.admin.widgets import FilteredSelectMultiple

from utils import rstripz,make_safe_filename
from trackerutils import *

DATE='%Y-%m-%d'

from trackerutils import DayModel, debu
from photoutil import *

from choices import *

class PhotoTag(DayModel):
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    
    class Meta:
        db_table='phototag'
        
    def __unicode__(self):
        return '%s (%d)'%(self.name,self.id)
    
    def vlink(self,text=None):
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name phototag'
        return '<a href="/photos/phototag/%d/">%s</a>'%(self.id, text)

class PhotoSpot(DayModel):
    '''a specific spot & angle to take photos from'''
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    slug=models.CharField(max_length=100)
    latitude=models.CharField(max_length=30,blank=True,null=True)
    longitude=models.CharField(max_length=30,blank=True,null=True)
    tag=models.ForeignKey('PhotoTag',related_name='photospot')
    
    class Meta:
        db_table='photospot'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=make_safe_filename(self.name)
        self.slug=make_safe_filename(self.slug)
        super(PhotoSpot, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
    def vlink(self,text):
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name photospot'
        return '<a href="/photo/photospot/%s/">%s</a>'%(self.slug, text)

class PhotoHasTag(DayModel):
    '''through object for photo&phototag'''
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    photo=models.ForeignKey('Photo',related_name='tags')
    tag=models.ForeignKey('PhotoTag',related_name='photos')
    class Meta:
        db_table='photohastag'
        
    def __unicode__(self):
        return '%s has %s'%(self.photo.name,self.tag.name)
        
class Photo(DayModel):
    ''''''
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    
    name=models.CharField(max_length=100,blank=True,null=True)
    fp=models.CharField(max_length=500,blank=True,null=True)
    day=models.ForeignKey('Day',blank=True,null=True,related_name='photos') #related day, probably when taken.
    resolutionx=models.IntegerField(blank=True,null=True)
    resolutiony=models.IntegerField(blank=True,null=True)
    incoming=models.BooleanField(default=False)
    setup=models.BooleanField(default=False)
    myphoto=models.BooleanField(default=False)
    taken=models.DateTimeField(blank=True,null=True) #from exif data
    camera=models.CharField(max_length=100,blank=True,null=True)
    iso=models.CharField(max_length=100,blank=True,null=True)
    mm=models.CharField(max_length=100,blank=True,null=True)
    exposure=models.CharField(max_length=100,blank=True,null=True)
    aperture=models.CharField(max_length=100,blank=True,null=True)
    filesize=models.CharField(max_length=20,blank=True,null=True)
        
    class Meta:
        db_table='photo'

    def file_exists(self):
        if not self.fp:
            return False
        return os.path.exists(self.fp)
    
    def delete_file(self):
        if self.file_exists():
            os.path.remove(self.fp)        

    def vlink(self,text):
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name photo'
        return '<a href="/photo/photo/%d/">%s</a>'%(self.id, text)

    def __unicode__(self):
        return self.name
    
    def inhtml(self,link=True,size='scaled'):
        if size=='scaled':
            height = settings.DEFAULT_PHOTO_HEIGHT or 400
        elif size=='small':
            height=50
        elif size=='orig':
            height=None
        else:
            height=100
        if height:
            img='<img src="%s" height=%d>'%(self.get_external_fp(), height)
        else:
            img='<img src="%s">'%(self.get_external_fp())
        if link:
            return self.vlink(text=img)
        return img
        
    def get_external_fp(self):
        return '/photo_passthrough/%d/'%self.id
    
    def initialize(self):
        if not self.file_exists():
            return False
        import datetime, os
        from PIL import Image
        im=Image.open(self.fp)
        tags=self.get_exif(im)
        exif2db={'Model':'camera','ISOSpeedRatings':'iso','DateTime':'taken'}
        if tags:
            for k,v in exif2db.items():
                if k in tags:
                    val=tags[k]
                    if v=='taken':
                        val=datetime.datetime.strptime(val,EXIF_TAKEN_FORMAT)
                    setattr(self,v,val)
            if 'ApertureValue' in tags:
                val='%0.2f'%(1.0*tags['ApertureValue'][0]/tags['ApertureValue'][1])
                self.aperture=val
            if 'FocalLength' in tags:
                self.mm=tags['FocalLength'][0]
            if 'ExposureTime' in tags:
                self.exposure='%0.5f'%(1.0*tags['ExposureTime'][0]/tags['ExposureTime'][1])
        else:
            pass
        self.resolutionx=im.size[0]
        self.resolutiony=im.size[1]
        #get resolution
        #get exif data etc.
        
        filesize=os.stat(self.fp).st_size
        self.filesize=filesize
        self.setup=True
        return True
    
    def get_exif(self,im=None):
        if not self.file_exists():
            return None
        if not im:
            from PIL import Image
            im=Image.open(self.fp)
        return get_exif(im)
    
    def save(self, *args, **kwargs):
        if not self.setup:
            self.initialize()
        if self.incoming==None:
            self.incoming=True
        if not self.name:
            if '/' in self.fp:
                self.name=self.fp.rsplit('/')[-1]
            else:
                self.name=self.fp
        self.name=make_safe_filename(self.name)
        if self.taken and not self.day:
            #make the day
            from day.models import Day
            date=self.taken.date()
            try:
                day=Day.objects.filter(date=date).get()
            except Day.DoesNotExist:
                day=Day(date=date)
                day.save()
            self.day=day
        super(Photo, self).save(*args, **kwargs)
        
    def tagids(self):
        return ','.join([str(n.tag.id) for n in self.tags.all()])