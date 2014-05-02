import datetime, shutil

from django.db import models
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.admin.widgets import FilteredSelectMultiple

from utils import *
log=logging.getLogger(__name__)
        
DATE='%Y-%m-%d'

from trackerutils import DayModel, debu,mktable
from day.photoutil import *

from choices import *

class PhotoTag(DayModel):
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100,blank=True,null=True) #to describe "control" tags
    
    @classmethod
    def setup_initial_tags(self):
        tagnames=settings.DEFAULT_TAG_NAMES
        for tn in tagnames:
            exi=PhotoTag.objects.filter(name=tn)
            if exi.exists():
                continue
            pt=PhotoTag(name=tn)
            pt.save()
    
    #admin
    control_tag=models.BooleanField(default=False) #ajax/js will take more actions
    #when this tag is added.  f.e. delete / undelete
    def get_external_page(self):
        return '/photo/phototag/%s/'%self.name
    class Meta:
        db_table='phototag'
        
    def __unicode__(self):
        return '%s'%(self.name)
    
    def vlink(self,text=None):
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name phototag'
        return '<a href="/photo/phototag/%s/">%s</a>'%(self.name, text)

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
    
    def vlink(self,text=None):
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
        return '%s has "%s"'%(self.photo.name,self.tag.name)
        
class Photo(DayModel):
    ''''''
    created=models.DateTimeField(auto_now_add=True) #photo db object created
    modified=models.DateTimeField(auto_now=True)
    
    name=models.CharField(max_length=100,blank=True,null=True)
    fp=models.CharField(max_length=500,blank=True,null=True)
    day=models.ForeignKey('Day',blank=True,null=True,related_name='photos') #related day, probably when taken.
    resolutionx=models.IntegerField(blank=True,null=True)
    resolutiony=models.IntegerField(blank=True,null=True)
    
    #camdata
    taken=models.DateTimeField(blank=True,null=True) #from exif data
    photo_created=models.DateTimeField()
    photo_modified=models.DateTimeField()
    camera=models.CharField(max_length=100,blank=True,null=True)
    iso=models.CharField(max_length=100,blank=True,null=True)
    mm=models.CharField(max_length=100,blank=True,null=True)
    exposure=models.CharField(max_length=100,blank=True,null=True)
    aperture=models.CharField(max_length=100,blank=True,null=True)
    filesize=models.CharField(max_length=20,blank=True,null=True)
    
    #admin
    deleted=models.BooleanField(default=False)
    incoming=models.BooleanField(default=False) #opposite is "done"
    setup=models.BooleanField(default=False)
    myphoto=models.BooleanField(default=False)
        
    class Meta:
        db_table='photo'

    def file_exists(self):
        if not self.fp:
            return False
        return os.path.exists(self.fp)
    
    def delete_file(self):
        if self.file_exists():
            os.path.remove(self.fp)        

    def vlink(self,text=None):
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name photo'
        return '<a href="%s">%s</a>'%(self.exhref(), text)
    
    def exhref(self):
        return '/photo/photo/%d/'%self.id

    def __unicode__(self):
        return self.name or self.fp or 'no name'
    
    def inhtml(self,link=True,size='scaled'):
        if size=='scaled':
            height = settings.PHOTO_SCALED
        elif size=='small':
            height= settings.PHOTO_SMALL
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
        stat=os.stat(self.fp)
        self.photo_modified=datetime.datetime.fromtimestamp(stat.st_mtime)
        self.photo_created=min(self.photo_modified,datetime.datetime.fromtimestamp(stat.st_ctime))
        
        self.filesize=stat.st_size
        
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
    
    def filename(self):    
        fn=os.path.split(self.fp)[-1]
        return fn
    
    def undoable_delete(self):
        if self.file_exists():
            fn=self.filename()
            delfp=get_nonexisting_fp(settings.DELETED_PHOTO_DIR,fn)
            self.tags.filter(tag__name='undelete').delete()
            shutil.move(self.fp,delfp)
            self.fp=delfp
            self.deleted=True
            self.incoming=False
            self.save()
            return True
        return False
    
    def done(self):
        if self.file_exists():
            fn=self.filename()
            donefp=get_nonexisting_fp(settings.DONE_PHOTO_DIR,fn)
            self.tags.filter(tag__name='incoming').delete()
            shutil.move(self.fp,donefp)
            self.fp=donefp
            self.incoming=False
            self.save()
            return True
    
    def undelete(self):
        if self.file_exists():
            if self.deleted:
                self.tags.filter(tag__name='delete').delete()
                infp=get_nonexisting_fp(settings.INCOMING_PHOTO_DIR, self.filename())
                shutil.move(self.fp,infp)
                self.fp=infp
                self.deleted=False
                self.incoming=True
                self.save()
                return True
            return False
        return False
    
    def tagids(self):
        return ','.join([str(n.tag.id) for n in self.tags.all()])
    
    
    
    def info_table(self):
        if self.deleted:
            dd='%sdeleted'%icon(0)
        else:
            dd=''
        dat=(('deleted',dd),
             ('taken',self.taken and self.taken.strftime(DATE_DASH_REV) or ''),
             ('photo created',self.photo_created.strftime(DATE_DASH_REV)),
             ('photo modified',self.photo_modified.strftime(DATE_DASH_REV)),
             ('obj created',self.created.strftime(DATE_DASH_REV)),
             ('obj modified',self.modified.strftime(DATE_DASH_REV)),
             ('incoming',icon(self.incoming)),
             ('setup',icon(self.setup)),
             ('myphoto',icon(self.myphoto))
             )
        res=mktable(dat,skip_false=True)
        return res
    
    def name_table(self,include_image=True):
        tags=', '.join([tag.tag.vlink() for tag in self.tags.all()])
        dat=[('name',self.name),
             ('fp',self.fp),
             ('tags',tags),]
        if include_image:
            dat.insert(2,('img',self.inhtml(size='small',link=True)),)
        res=mktable(dat,skip_false=True)
        return res
    
    def exif_table(self):
        if self.resolutionx and self.resolutiony:
            size='%dx%d'%(self.resolutionx,self.resolutiony)
        else:
            size=''
        dat=(('camera',self.camera),
             ('iso',self.iso),
             ('mm',self.mm),
             ('size',size),
             ('filesize',humanize_size(self.filesize)),
             )
        res=mktable(dat,skip_false=True)
        return res
    