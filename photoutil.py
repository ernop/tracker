import urllib, urlparse, re, os, ConfigParser, logging, uuid, logging.config, types, datetime, json, calendar

from django.template import RequestContext


def get_fps_from_incoming():
    from django.conf import settings
    fps=[]
    for fn in os.listdir(settings.INCOMING_PHOTO_FOLDER):
        fp=os.path.join(settings.INCOMING_PHOTO_FOLDER,fn)
        if not os.path.isfile(fp):
            continue
        fplower=fp.lower()
        if fplower!=fp:
            import shutil
            shutil.move(fp, fplower)
        fps.append(fp)
    return fps
        
def check_incoming():
    'rechecks incoming and makes new photo objects'
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
    info = im._getexif()
    
    if not info:
        return False
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret