import urllib, urlparse, re, os, ConfigParser, logging, uuid, logging.config, types, datetime, json, calendar
import shutil, random

log=logging.getLogger(__name__)

from django.template import RequestContext

def get_fps_from_incoming():
    from django.conf import settings
    fps=[]
    for fn in os.listdir(settings.INCOMING_PHOTO_DIR):
        if fn.startswith('.') or fn.startswith('_'):
            continue
        fp=os.path.join(settings.INCOMING_PHOTO_DIR,fn)
        if not os.path.isfile(fp):
            continue
        if not os.access(fp,6):
            continue
        fplower=fp.lower()
        if fplower.endswith('.jpeg'):
            fplower=fplower.rsplit('.jpeg',1)[-2]+'.jpg'
        if fplower!=fp:
            shutil.move(fp, fplower)
        cmd='mogrify -auto-orient "%s"'%fplower
        res=os.system(cmd)
        if res:
            log.error("fail cmd %s for fp %s"%(cmd,fp))
            continue
        fps.append(fplower)
    return fps
        
def check_incoming():
    photos=get_fps_from_incoming()
    from day.photomodels import Photo
    new=[fp for fp in photos if not Photo.objects.filter(fp=fp,incoming=True).exists()]
    
    for fp in new:
        ph=Photo(fp=fp,incoming=True)
        ph.save()

def phototag2obj(phototag):
    return {'id':phototag.id,'name':phototag.name,'text':phototag.name,}

def get_exif(im):
    ret = {}
    from PIL.ExifTags import TAGS
    try:
        info = im._getexif()
    except:
        info=None
    if not info:
        return False
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def getletter():
    import random
    return random.choice('a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9'.split())

def get_nonexisting_fp(basedir,basefn):
    fn=basefn
    ii=0
    testfp=os.path.join(basedir,fn)
    while os.path.exists(testfp):
        fn=getletter()+fn
        testfp=os.path.join(basedir,fn)
        ii+=1
        if ii>20:
            log.error('timeout.')
            import ipdb;ipdb.set_trace()
    return testfp

def get_next_incoming(exclude):
    #goto next incoming photo by id for quick shifting.
    #actually i should preload this...
    from day.models import Photo
    if type(exclude) is not list:
        exclude=[exclude]
    exis=Photo.objects.exclude(id__in=exclude).filter(incoming=True).order_by('id')
    ii=0
    found=False
    while 1:
        if len(exis)>ii:
            exi=exis[ii]
        else:
            return False #out the end
        ii+=1
        if exi.file_exists():
            return exi

def get_next_photopaths(count,excludes=None):
    if not excludes:excludes=[]
    excludes=excludes[:]
    photopaths=[]
    for n in range(count):
        next_incoming=get_next_incoming(exclude=excludes)
        if next_incoming:
            if next_incoming.file_exists():
                photopaths.append(next_incoming.get_external_fp())
                excludes.append(next_incoming.id)
        else:
            break
    return photopaths
    
def can_access_private(user):
    if not user:
        return False
    if user.username=='superuser':
        return True
    return False