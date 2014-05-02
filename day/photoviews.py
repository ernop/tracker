open('/home/ernop/django.fuseki.net/err.txt','a').write("started pviews.\n")

import datetime

from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django import forms
from day.models import *

from trackerutils import *
from utils import *
from choices import *

import logging
log=logging.getLogger(__name__)

from photoutil import *

@user_passes_test(staff_test)
def photo(request,id):
    photo=Photo.objects.get(id=id)
    if not can_access_private(request.user) and photo.tags.filter(tag__name__in=settings.EXCLUDED_TAGS).exists():
        return HttpResponseRedirect('/')
    vals={}
    vals['photo']=photo
    vals['full_phototags']=[phototag2obj(pt) for pt in PhotoTag.objects.all()]
    return r2r('jinja2/photo/photo.html',request,vals)

@user_passes_test(staff_test)
def phototag(request,name):
    phototag=PhotoTag.objects.get(name=name)
    if not can_access_private(request.user) and phototag.name in settings.EXCLUDED_TAGS:
        return HttpResponseRedirect('/')
    vals={}
    vals['phototag']=phototag
    return r2r('jinja2/photo/phototag.html',request,vals)

@user_passes_test(staff_test)
def photospot(request,slug):
    photo=PhotoSpot.objects.get(slug=slug)
    vals={}
    vals['photospot']=photospot
    vals['phototags']=[phototag2obj(pt) for pt in PhotoTag.objects.all()]
    return r2r('jinja2/photo/photospot.html',request,vals)

@user_passes_test(staff_test)
def incoming(request):
    '''view & start classifying photos in the incoming dir'''
    check_incoming()
    photos=Photo.objects.filter(incoming=True)
    vals={}
    vals['title']='incoming photos'
    vals['photos']=photos[:100]
    return r2r('jinja2/photo/photolist.html',request,vals)

@user_passes_test(staff_test)
def photo_passthrough(request, id):
    from utils import staff_test
    if not staff_test(request.user):
        return False
    from utils import is_secure_path
    photo=Photo.objects.get(id=id)
    fp=photo.fp
    if not is_secure_path(fp):
        assert False
    assert os.path.exists(fp)
    ext=os.path.splitext(fp)[-1]
    data=open(fp, 'rb').read()
    if ext in ['.jpg','.jpeg']:
        return HttpResponse(data, mimetype="Image/jpeg")
    elif ext=='.png':
        return HttpResponse(data, mimetype="Image/png")
    else:
        log.error('wronge filetype. %s',ext)
        import ipdb;ipdb.set_trace()
    return response

@user_passes_test(staff_test)
def ajax_photo_data(request):
    log.info(request.POST)
    vals={}
    vals['success']=True
    vals['message']='start.'
    todo=request.POST
    kind=request.POST['kind']
    goto_next_incoming=False
    if kind=='phototag':
        photo=Photo.objects.get(id=todo['photo_id'])
        new_tagids=[]
        for tagid in todo['phototag_ids'].split(','):
            if tagid:
                new_tagids.append(int(tagid))
        kept_tagids=[]
        for tag in photo.tags.all():
            if int(tag.tag.id) not in new_tagids:
                if tag.tag.name=='delete':
                    photo.undelete()
                tag.delete()
            else:
                kept_tagids.append(int(tag.tag.id))
        for tagid in new_tagids:
            if tagid not in kept_tagids:
                pht=PhotoHasTag(tag=PhotoTag.objects.get(id=tagid), photo=photo)
                pht.save()
        if photo.tags.filter(tag__name='delete').exists() and not photo.deleted:
            photo.undoable_delete()
            goto_next_incoming=True
        elif PhotoHasTag.objects.filter(tag__name='undelete').exists() and photo.deleted:
            photo.undelete()
            photo.tags.filter(tag__name='undelete').delete()
            #dont actually leave the "undelete" tag on there, its weird
        if photo.tags.filter(tag__name='done').exists() and photo.incoming:
            #move on from incoming guys once "done" is entered
            goto_next_incoming=True
            photo.done()
        if photo.tags.filter(tag__name='myphoto').exists():
            #move on from incoming guys once "done" is entered
            photo.myphoto=True
            photo.save()
        if photo.tags.filter(tag__name__in=settings.CLOSING_TAGS).exclude(tag__id__in=kept_tagids):
            #actually was assigned this tag
            photo.done()
            goto_next_incoming=True
    else:
        log.error('bad k %s',k)
        import ipdb;ipdb.set_trace()
    if goto_next_incoming:
        next_incoming=get_next_incoming(exclude=photo.id)
        if next_incoming:
            vals['message']='undeleted'
            vals['goto_next_photo']=True
            vals['next_photo_href']=next_incoming.exhref()
        else:
            vals['message']='no more photos to process'
            vals['goto_next_photo']=True
            vals['next_photo_href']='/photo/incoming/'
        vals['last_photo_href']=photo.exhref()
    vals['message']='success'
    return r2j(vals)

open('/home/ernop/django.fuseki.net/err.txt','a').write("end pviews.\n")