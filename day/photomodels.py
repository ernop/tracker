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

class Photo(DayModel):
    ''''''
    created=models.DateTimeField(auto_now_add=True) #photo db object created
    modified=models.DateTimeField(auto_now=True)
    
    name=models.CharField(max_length=100,blank=True,null=True)
    fp=models.CharField(max_length=500,blank=True,null=True)
    thumbfp=models.CharField(max_length=500,blank=True,null=True) #may not exist
    day=models.ForeignKey('Day',blank=True,null=True,related_name='photos') #related day, probably when taken.
    resolutionx=models.IntegerField(blank=True,null=True)
    resolutiony=models.IntegerField(blank=True,null=True)
    hash=models.CharField(max_length=100,blank=True,null=True)    
    
    #photospot
    photospot=models.ForeignKey('PhotoSpot',related_name='photos',blank=True,null=True)
    xcrop=models.IntegerField(default=0) #how off it is from the default image.
    ycrop=models.IntegerField(default=0)
    
    #camdata
    taken=models.DateTimeField(blank=True,null=True) #from exif data
    photo_created=models.DateTimeField()
    photo_modified=models.DateTimeField()
    camera=models.CharField(max_length=100,blank=True,null=True)
    iso=models.CharField(max_length=100,blank=True,null=True)
    mm=models.CharField(max_length=100,blank=True,null=True)
    exposure=models.CharField(max_length=100,blank=True,null=True)
    aperture=models.CharField(max_length=100,blank=True,null=True)
    filesize=models.IntegerField(blank=True,null=True)
    
    #admin
    deleted=models.BooleanField(default=False)
    incoming=models.BooleanField(default=False) #opposite is "done"
    setup=models.BooleanField(default=False)
    myphoto=models.BooleanField(default=False)
    thumb_ok=models.BooleanField(default=False)
    
    
        
    class Meta:
        db_table='photo'

    def file_exists(self):
        if not self.fp:
            log.error('image missing fp, hard deleting obj. %s',fp)
            self.kill_thumb()
            self.delete()
            return False
        res=os.path.exists(self.fp)
        if not res:
            if settings.LOCAL:
                print 'del',self
            else:
                log.error('fp not exist. hard deleting. %s %s',self.id and str(self.id) or 'already deleted',self.fp)
            self.kill_thumb()
            self.delete()
            return False            
        return True
    
    def kill_this(self):
        log.info('killing this. %s',self)
        res=self.file_exists()
        if res:
            if Photo.objects.exclude(id=self.id).filter(fp=self.fp,deleted=False).exists():
                #another photo db object for the same thing exists, so dont kill fp.
                pass
            else:
                os.remove(self.fp)  
        else:
            #already deleted.
            return True
        self.kill_thumb()
        self.delete()
        return True
    
    def delete_file(self):
        if self.file_exists():
            os.remove(self.fp)  
        if os.path.exists(self.thumbfp):
            os.remove(self.thumbfp)

    def vlink(self,text=None, wrap=False, tooltip=None):
        if wrap:
            wrap=' nb'
        else:
            wrap=''
        if not tooltip:
            tooltip=''
        if not text:
            if self.name:
                text=self.name
            else:
                text='no name photo'
        return '<a class="btn%s" title="%s" href="%s">%s</a>'%(wrap, tooltip, self.exhref(), text)
    
    
    def ajaxlink(self,text=None,wrap=False,tooltip=None):
        if wrap:
            wrap=' nb'
        else:
            wrap=''
        if not text:
            text='ajax link'
        '''link to /photo/photoajax/#!id'''
        if not tooltip:
            tooltip=''
        res='<a class="%s" title="%s" href="/photo/photoajax/#!id=%d">%s</a>'%(wrap, tooltip, self.id, text)
        return res
    
    def exhref(self):
        return '/photo/photo/%d/'%self.id

    def __unicode__(self):
        return self.name or self.fp or 'no name'
    
    def get_using_time(self, formatter=None):
        using_time=self.taken or (self.day and self.day.date) or self.photo_created or None
        if using_time:
            if not formatter:
                formatter=DATE_DASH_REV_DAY
            return using_time.strftime(formatter)
        return ''
    
    def inhtml(self,clink=False,vlink=False,size='scaled',ajaxlink=False,tooltip_tags=True, date=True):
        if not vlink and not clink and not ajaxlink:
            clink=True
        thumb=False
        width=None
        height=None
        if size=='scaled':
            if self.resolutiony>1000 or self.resolutionx>1000:
                if self.resolutionx>self.resolutiony:
                    width=settings.PHOTO_SCALED
                    height=int(1.0*settings.PHOTO_SCALED*self.resolutiony/self.resolutionx)
                else:
                    height=settings.PHOTO_SCALED
                    width=int(1.0*settings.PHOTO_SCALED*self.resolutionx/self.resolutiony)
            else:
                height=self.resolutiony
                width=self.resolutionx
        elif size=='thumb':
            height= settings.THUMB_HEIGHT
            thumb=True
            if self.resolutionx and self.resolutiony:
                width=int(1.0*settings.THUMB_HEIGHT*self.resolutionx/self.resolutiony)
            else:
                width=''
        elif size=='orig':
            height=None
        else:
            height=100
        if thumb:
            tooltip_tags=True
            src=self.get_external_fp(thumb=True)
        else:
            src=self.get_external_fp()
        if tooltip_tags:
            tooltip=', '.join([t.tag.name for t in self.tags.all()])
            if date:
                tooltip += '&#10;'+self.get_using_time()
        else:
            tooltip=''
        if height:
            if width:
                img='<img src="%s" height=%d width=%d>'%(src, height, width)
            else:
                img='<img src="%s" height=%d>'%(src, height)
        else:
            img='<img src="%s">'%(self.get_external_fp())
        if vlink:
            return self.vlink(text=img,wrap=False, tooltip=tooltip)
        elif clink:
            return self.clink(text=img,wrap=False,skip_btn=True, tooltip=tooltip)
        elif ajaxlink:
            return self.ajaxlink(text=img,wrap=False, tooltip=tooltip)
        return img
        
    def is_thumb_ok(self):
        if self.thumbfp:
            try:
                if os.path.exists(self.thumbfp):
                    return True
            except UnicodeEncodeError:
                log.error('error dealing with thumbfp for %s',self)
                self.thumbfp=''
                self.save()
                return False
        return False
        
    def create_thumb(self,force=False):
        '''maybe not actually recreate it'''
        if self.is_thumb_ok() and not force:
            return True
        else:
            return self._create_thumb()
            
    def _create_thumb(self):
        '''really create it'''
        if self.thumbfp:
            if os.path.exists(self.thumbfp):
                os.remove(self.thumbfp)
        #else:
            #self.thumbfp=self.get_thumbfp()
            #self.save()
        newthumbfp=self.get_thumbfp()
        self.thumbfp=newthumbfp
        cmd='convert -define "jpeg:size=500x%d" "%s" \
        -auto-orient -thumbnail 250x%d \
        -unsharp 0x.5 "%s"'%(settings.THUMB_HEIGHT*3, 
                             self.fp, 
                             settings.THUMB_HEIGHT,
                             newthumbfp)
        
        log.info("create thumb doing cmd %s",cmd)
        #import locale
        #aa=locale.CODESET
        #bb=locale.nl_langinfo(locale.CODESET)
        #cc=os.path.supports_unicode_filenames
        if not os.path.exists(self.fp.encode('utf8')):
            return False
        try:
            res=os.system(cmd)
        except:
            log.error('failure in cmd %s',cmd)
            return False
        if res:
            log.error('failure of convert command %s',cmd)
            self.thumb_ok=False
            self.save()
            return False
        self.thumb_ok=True
        self.save()
        return True
            
            
    def get_thumbfp(self):
        thumbfp=get_nonexisting_fp(settings.THUMB_PHOTO_DIR, self.filename())
        return thumbfp
        
    def get_external_fp(self, thumb=False):
        if thumb:
            res=self.create_thumb(force=False)
            if res:
                return self.get_photo_external_link(thumb=True)
            else:
                return self.get_photo_external_link(thumb=False)
            #return '/photo_thumb_passthrough/%d.jpg'%self.id
        if 1 or not settings.LOCAL:
            return self.get_photo_external_link()
        return '/photo_passthrough/%d.jpg'%self.id
    
    def initialize(self):
        if not self.file_exists():
            return False
        import datetime, os
        from PIL import Image
        try:
            im=Image.open(self.fp)
            
            tags=self.get_exif(im)
            exif2db={'Model':'camera','ISOSpeedRatings':'iso','DateTime':'taken'}
            if tags:
                for k,v in exif2db.items():
                    if k in tags:
                        val=tags[k]
                        if v=='taken':
                            try:
                                val=datetime.datetime.strptime(val,EXIF_TAKEN_FORMAT)
                            except:return False
                        setattr(self,v,val)
                if 'ApertureValue' in tags:
                    try:
                        self.aperture='%0.2f'%(1.0*tags['ApertureValue'][0]/tags['ApertureValue'][1])
                    except:
                        self.aperture=''
                if 'FocalLength' in tags:
                    self.mm=tags['FocalLength'][0]
                if 'ExposureTime' in tags:
                    try:
                        self.exposure='%0.5f'%(1.0*tags['ExposureTime'][0]/tags['ExposureTime'][1])
                    except:
                        self.exposure=''
            else:
                pass
            self.resolutionx=im.size[0]
            self.resolutiony=im.size[1]
            
        except IOError:
            #just continue with stat stuff.
            pass
        
        #get resolution
        #get exif data etc.
        stat=os.stat(self.fp.encode('utf8'))
        self.photo_modified=datetime.datetime.fromtimestamp(stat.st_mtime)
        self.photo_created=min(self.photo_modified,datetime.datetime.fromtimestamp(stat.st_ctime))
        
        self.filesize=stat.st_size
        #should create thumb.
        self.setup=True
        if self.modified<self.created:
            self.created=self.modified
        #if self.taken and self.created and self.created<self.taken:
            #self.taken=self.created
            #self.day=None
            #self.set_day()
            #reset the day in the weird case where they somehow get an incorrectly-future set taken date
            #even though photo created is later.
        if self.taken and self.photo_created and self.photo_created<self.taken:
            self.taken=self.photo_created
            self.day=None
            self.set_day()
        try:
            self.save()
        except Exception,e:
            log.error('could not save. %s %d',e,self.id)
        return True
    
    def get_exif(self,im=None):
        if not self.file_exists():
            return None
        if not im:
            from PIL import Image
            try:
                im=Image.open(self.fp)
            except IOError:
                return False
        return get_exif(im)
    
    
    def rehash(self):
        '''hash the first few K of data'''
        import hashlib
        if self.fp.endswith('.bmp'):
            self.hash=''
            return
        if os.path.exists(self.fp):
            data=open(self.fp,'rb').read(10000)
            hsh=hashlib.md5(data).hexdigest()
            self.hash=hsh
    
    def save(self, *args, **kwargs):
        #TODO: when settings not incoming, should move to storage.
        #but for now, probably fine.
        if not self.hash:
            self.rehash()
        if self.xcrop == None:
            self.xcrop=0
        if self.ycrop == None:
            self.ycrop=0
        if not self.setup:
            res=self.initialize()
            if not res:
                return
        if self.incoming==None:
            self.incoming=True
        try:
            if not self.name:
                if '/' in self.fp:
                    self.name=self.fp.rsplit('/')[-1]
                else:
                    self.name=self.fp
        except:
            log.error('bad name. %d',self.id)
        self.name=make_safe_filename(self.name)[:100]
        #no longer set day every single time you save; it is ok to have exif day taken but not a day
        #day should only be for photos which i took myself
        #if self.taken and not self.day:
            #self.set_day()
        super(Photo, self).save(*args, **kwargs)
            
    def set_day(self):
        #make the day
        from day.models import Day
        if not self.taken:
            log.error('tried to set day but no taken date set. %s'%(self.id and str(self.id) or 'no id'))
            return False
        date=self.taken.date()
        qq=date
        try:
            day=Day.objects.filter(date=date).get()
        except Day.DoesNotExist:
            day=Day(date=date)
            day.save()
        #first time through myphoto is null.
        if self.id:
            #if self.myphoto==False:
                #do nothing, don't re-add the day
                #pass
            
            #elif self.myphoto:
                self.day=day
                return True
        else: #when you are first saved, treat as myphoto.
            self.day=day
            self.myphoto=True
            return True
        
    
    def filename(self):    
        fn=os.path.split(self.fp)[-1]
        return fn
    
    def kill_thumb(self):
        if self.thumbfp and os.path.exists(self.thumbfp):
            os.remove(self.thumbfp)
    
    def undoable_delete(self):
        log.info('test file exists. %s', self.fp)
        if self.file_exists():
            log.info('it did exists. %s', self.fp)
            fn=self.filename()
            delfp=get_nonexisting_fp(settings.DELETED_PHOTO_DIR,fn)
            self.tags.filter(tag__name='undelete').delete()
            log.info("deleting; moving from %s 5o %s",self.fp,delfp)
            shutil.move(self.fp,delfp)
            self.fp=delfp
        else:
            #if file not exist, its been deleted in the file exist check.
            return
        self.deleted=True
        self.incoming=False
        self.save()
        return True
    
    
    def autoorient(self):
        '''mogrify, while preserving a,mtime.  ffs.'''
        if not os.path.exists(self.fp):
            log.error('tried to auto-orient an fp which then no longer existed. photoid:fp:%s',self.fp)
            return False
        log.info('autoorient id %d',self.id)
        log.info('autoorient %s',self.fp)
        try:
            ufp=self.fp.encode('utf8')
        except Exception,e:
            id=self.id
            #storing local variables
            ufp=''
        try:
            stat=os.stat(self.fp):
        except:
            stat = os.stat(self.fp.encode('utf8'))
        atime, mtime = stat.st_atime,stat.st_mtime
        if self.fp.endswith('webp'):
            #mogrify doesn't work on webp anyway.
            res=0
        else:
            cmd='mogrify -auto-orient "%s"'%self.fp
            log.info("mogrify cmd %s",cmd)
            res=0
            if not settings.LOCAL:
                res=os.system(cmd)
                try:
                    os.utime(self.fp, (atime, mtime))
                except OSError,e:
                    log.error('error doing utime %s',e)
        self.rehash()
        if res:
            log.error("fail cmd %s for fp %s"%(cmd,self.fp))
            self.save()
            return False
        try:
            self.save()
        except Exception, e:
            log.error("error saving self. %s %s",self,e)
            return False
        return True
    
    def done(self):
        if self.file_exists():
            fn=self.filename()
            donefp=get_nonexisting_fp(settings.DONE_PHOTO_DIR,fn)
            self.tags.filter(tag__name='incoming').delete()
            if not self.tags.filter(tag__name='done').exists():
                from photomodels import PhotoTag,PhotoTag
                tt=PhotoHasTag(photo=self,tag=PhotoTag.objects.get(name='done'))
                log.info('added done tag. %s', self)
                tt.save()
            log.info("moving from %s 5o %s", self.fp, donefp)
            shutil.move(self.fp,donefp)
            self.fp=donefp
            self.incoming=False
            self.save()
            log.info('moved photo %s to done folder %s',self,donefp)
            return True
        else:
            log.error('couldn\'t move photo to done folder cause file not exist. %s %s',self,self.fp)
    
    def undelete(self):
        if self.file_exists():
            if self.deleted:
                self.tags.filter(tag__name='delete').delete()
                infp=get_nonexisting_fp(settings.INCOMING_PHOTO_DIR, self.filename())
                log.info("undeleting: moving from %s 5o %s",self.fp,infp)
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
        if self.day:
            daylink=self.day.vlink()
            kill_daylink='<div class="btn btn-default kill_day_btn">X</div>'
            daylink+=' '+kill_daylink
        else:
            daylink=None
        founded=self.founded.exists() and self.founded.get() or False
        fspot=''
        if founded:
            fspot=founded.clink(text='founded photospot %s'%founded)
        dat=(('deleted',dd),
             
             ('day',daylink),
             ('incoming',icon(self.incoming)),
             ('setup',icon(self.setup)),
             ('myphoto',icon(self.myphoto)),
             
             ('thumb ok',icon(self.thumb_ok)),
             ('done',icon(self.done)),
             ('crop',(self.xcrop or self.ycrop) and ('x=%d y=%d'%(self.xcrop,self.ycrop)) or ''),
             ('taken',self.taken and self.taken.strftime(DATE_DASH_REV_DAY) or ''),
             ('photo created',self.photo_created.strftime(DATE_DASH_REV_DAY)),
             ('photo modified',self.photo_modified.strftime(DATE_DASH_REV_DAY)),
             ('obj created',self.created.strftime(DATE_DASH_REV)),
             ('obj modified',self.modified.strftime(DATE_DASH_REV)),
             ('fspot',fspot),
             )
        res=mktable(dat,skip_false=True,nb=True)
        return res

    def name_table(self,include_image=True,clink=False,vlink=False,ajaxlink=False):
        dat=[('id',self.clink(text=self.id)),
            ('name',self.name),
            ('hash',self.hash),
            ('fn',os.path.split(self.fp)[-1]),
             ]
        if include_image:
            dat.insert(2,('img',self.inhtml(size='thumb',clink=clink,vlink=vlink,ajaxlink=ajaxlink)),)
        res=mktable(dat,skip_false=True)
        return res
    
    def links_table(self):
        from trackerutils import div
        #vtags=div(klass='vtagzone',contents=', '.join([tag.tag.vlink() for tag in self.tags.all()]))
        vspot=''
        if self.photospot:
            vspot=self.photospot.vlink()
        
        vspot=div(klass='vspotzone',contents=vspot or '&nbsp;')
        data=(#('tags vlink',vtags),
        ('photospot vlink',vspot),)
        res=mktable(data,skip_false=False)
        return res
    
    def exif_table(self):
        from trackerutils import div
        ctags=div(klass='ctagzone',contents=''.join([tag.tag.clink() for tag in self.tags.all()]))
        photoset=div(klass='photosetzone',contents=''.join([tag.tag.photosetlink() for tag in self.tags.all()]))
        cspot=''
        if self.photospot:
            cspot=self.photospot.clink()
        cspot=div(klass='cspotzone',contents=cspot or '&nbsp;')
        if self.resolutionx and self.resolutiony:
            size='%dx%d'%(self.resolutionx,self.resolutiony)
        else:
            size=''
        dat=(('camera',self.camera),
             ('iso',self.iso),
             ('mm',self.mm),
             ('size',size),
             ('filesize',humanize_size(self.filesize)),
             ('tags clink',ctags),
             ('photoset',photoset),
             ('photospot clink',cspot),
             )
        res=mktable(dat,skip_false=True)
        return res
    
    def can_be_seen_by(self,user=None):
        if self.is_private() and not can_access_private(user):
            return False
        return True
    
    def is_private(self):
        return self.tags.filter(tag__name__in=settings.EXCLUDED_TAGS).exists()
    
    def get_photospothtml(self):
        if self.photospot:
            cl=self.photospot.clink()
            vl=self.photospot.vlink()
            data=[('name',self.photospot.name),
                  ('clink',cl),
                  ('vlink',vl),
                  ('count',self.photospot.photos.count()),]
            return mktable(data)
        
        else:
            return ''
    
    def get_photo_external_link(self,thumb=False):
        if thumb:
            exfp='/static/'+'/'.join(self.thumbfp.rsplit('/')[-2:])
        else:
            exfp='/static/'+'/'.join(self.fp.rsplit('/')[-2:])
        return exfp


class PhotoTag(DayModel):
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100,blank=True,null=True) #to describe "control" tags
    person=models.ForeignKey('Person', blank=True,null=True,related_name='as_tag')
    
    #admin
    control_tag=models.BooleanField(default=False) #ajax/js will take more actions
    use_count=models.IntegerField()
    
    @classmethod
    def setup_my_person_tag(self,person):
        if PhotoTag.objects.filter(person=person).exists():
            #edits propagate
            exitag=PhotoTag.objects.get(person=person)
            exitag.name=unicode(person)
            exitag.save()
            return
        tg=PhotoTag(name=unicode(person), person=person)
        tg.save()
    
    @classmethod
    def setup_people_tags(self):
        from day.models import Person
        for person in Person.objects.all():
            self.setup_my_person_tag(person)
    
    @classmethod
    def setup_initial_tags(self):
        tagnames=settings.DEFAULT_TAG_NAMES
        for tn in tagnames:
            exi=PhotoTag.objects.filter(name=tn)
            if exi.exists():
                continue
            pt=PhotoTag(name=tn)
            pt.save()
    
    @classmethod
    def update_tag_counts(self):
        for pt in PhotoTag.objects.all():
            ct=pt.photos.count()
            if pt.person:
                ct=ct+pt.person.purchases.count()
            pt.use_count=ct
            pt.save()
    
    def save(self, *args, **kwargs):
        if self.use_count is None:
            self.use_count=0
        super(PhotoTag, self).save(*args, **kwargs)
    
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
        return '<a class="btn btn-default" href="/photo/phototag/%s/">%s</a>'%(self.name, text)


        #

    
    def photosetlink(self,text=None):
        if not text:
            text=self.name
        return '<a class="btn btn-default" href="/photo/photoset/%s/">%s</a>'%(self.name,text)
    
    def history_sparkline(self):
        #photos=Photo.objects.filter(tags__tag=obj)
        photos=Photo.objects.raw('select p.id,date(p.photo_created) as date,\
        count(*) as ct from photo p inner join \
        photohastag pht on pht.photo_id=p.id inner join phototag pt on \
        pt.id=pht.tag_id where pt.id=%d group by 2'%self.id)
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
        from utils import nice_sparkline
        spl=nice_sparkline(dat2,500,300)
        return spl

class PhotoSpot(DayModel):
    '''a specific spot & angle to take photos from'''
    created=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500,blank=True,null=True)
    tour=models.CharField(max_length=100,blank=True,null=True)
    tour_order=models.FloatField(blank=True,null=True)
    slug=models.CharField(max_length=100,blank=True,null=True)
    latitude=models.CharField(max_length=30,blank=True,null=True)
    longitude=models.CharField(max_length=30,blank=True,null=True)
    
    founding_photo=models.ForeignKey('Photo',blank=True,null=True,related_name='founded')
    
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
        return '<a class="btn btn-default" href="/photo/photospot/%s/">%s</a>'%(self.name.replace(' ','_'), text)

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
    
#class PhotoHasPhotospot(DayModel):
    #'''linkage between photo and photospot'''
    #created=models.DateTimeField(auto_now_add=True)
    #modified=models.DateTimeField(auto_now=True)
    #photo=models.ForeignKey('Photo',related_name='photospot')
    #photospot=models.ForeignKey('PhotoSpot',related_name='photos')
    
    #class Meta:
        #db_table='photohasphotospot'
        
    #def __unicode__(self):
        #return '%s has "%s"'%(self.photo.name,self.photospot.name)
