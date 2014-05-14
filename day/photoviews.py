
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
def photoajax(request):
    '''load & then preload a bunch of photos.  basically, ajax-enabled fast flickr
    
    format: load js only.
    js:
    1. load_show()
    load show: load(show())
               
               load()
    load:      send current list to server, to get another and preload it
    '''
    vals={}
    vals['full_phototags']=get_full_phototags()
    vals['full_photospots']=get_full_photospots()
    vals['TAGIDS_WHICH_FORCE_NEXT']=[tt.id for tt in PhotoTag.objects.filter(name__in=settings.CLOSING_TAGS)]
    #get the tags
    return r2r('jinja2/photo/photoajax.html',request,vals)

#def incoming_photospot_photos_ajax(request):
    #'''go through all photospos incoming photos '''
        #vals={}
    #vals['full_phototags']=get_full_phototags()
    #vals['full_photospots']=get_full_photospots()
    ##vals['TAGIDS_WHICH_FORCE_NEXT']=[tt.id for tt in PhotoTag.objects.filter(name__in=settings.CLOSING_TAGS)]
    ##get the tags
    #return r2r('jinja2/photo/incoming_photospot_ajax.html',request,vals)

@user_passes_test(staff_test)
def photo(request,id):
    photo=Photo.objects.get(id=id)
    if not can_access_private(request.user) and photo.tags.filter(tag__name__in=settings.EXCLUDED_TAGS).exists():
        return HttpResponseRedirect('/photo/incoming/')
    vals={}
    vals['photo']=photo
    vals['full_phototags']=get_full_phototags()
    vals['next_photopaths']=get_next_photopaths(count=1,excludes=[photo.id])
    return r2r('jinja2/photo/photo.html',request,vals)

@user_passes_test(staff_test)
def phototag(request,name):
    name=name.replace('%20',' ')
    phototag=PhotoTag.objects.get(name=name)
    if not can_access_private(request.user) and phototag.name in settings.EXCLUDED_TAGS:
        return HttpResponseRedirect('/photo/incoming/')
    vals={}
    vals['phototag']=phototag
    return r2r('jinja2/photo/phototag.html',request,vals)

@user_passes_test(staff_test)
def photospot(request,name):
    name=name.replace('%20',' ').replace('_',' ')
    #should load all the full images inline.
    #keyboard controls to quickly move between them
    #and also to adjust their crop
    #and to kill them (remove them from photospot)
    pspot=PhotoSpot.objects.get(name=name)
    vals={}
    vals['photospot']=pspot
    vals['photos']=pspot.photos.exclude(deleted=True)
    vals['photo_objs']=[photo2obj(pho) for pho in pspot.photos.exclude(deleted=True)]
    vals['phototags']=[phototag2obj(pt) for pt in sorted(PhotoTag.objects.all(),key=phototagsort)]
    return r2r('jinja2/photo/photospot.html',request,vals)

@user_passes_test(staff_test)
def incoming(request):
    '''view & start classifying photos in the incoming dir'''
    check_incoming()
    photos=Photo.objects.filter(incoming=True)
    vals={}
    vals['title']='incoming photos'
    vals['photos']=photos[:20]
    return r2r('jinja2/photo/photolist.html',request,vals)

@user_passes_test(staff_test)
def photo_thumb_passthrough(request,id):
    return photo_passthrough(request, id, thumb=True)

@user_passes_test(staff_test)
def photo_passthrough(request, id, thumb=False):
    from utils import staff_test
    if not staff_test(request.user):
        return False
    photo=Photo.objects.get(id=id)
    from utils import is_secure_path
    if thumb:
        fp=photo.thumbfp
    else:
        fp=photo.fp
    ext=os.path.splitext(fp)[-1]
    data=open(fp, 'rb').read()
    
    if ext in ['.jpg','.jpeg']:
        response=HttpResponse(data, mimetype="Image/jpeg")
    elif ext=='.png':
        response=HttpResponse(data, mimetype="Image/png")
    elif ext=='.gif':
        response=HttpResponse(data, mimetype="Image/gif")
    elif ext=='.webp':
        response=HttpResponse(data, mimetype="Image/webp")
    else:
        log.error('wronge filetype. %s',ext)
        import ipdb;ipdb.set_trace()
    response['Cache-Control'] = 'max-age=86400	'
    return response

@user_passes_test(staff_test)
def ajax_photo_data(request):
    vals={}
    try:
        vals['success']=True
        vals['message']='start.'
        try:
            todo=request.POST
            kind=request.POST['kind']
        except:
            todo=json.loads(request.raw_post_data)
            kind=todo['kind']
        goto_next_incoming=False
        goto_same=False
        if kind=='ajax photo preload':
            try:
                if 'exclude_ids[]' in request.POST and request.POST['exclude_ids[]']:
                    #exclude_ids=[int(_) for _ in request.POST['exclude_ids[]'].split(',')]
                    exclude_ids=request.POST.getlist('exclude_ids[]')
                else:
                    exclude_ids=None
            except Exception,e:
                import ipdb;ipdb.set_trace()
            nextphoto=get_next_incoming(exclude=exclude_ids)
            if not nextphoto:
                vals['success']=False
                vals['message']='could not get next incoming'
                log.error('failed to get next.')
            else:
                infozone=nextphoto.name_table(include_image=False)+nextphoto.info_table()+nextphoto.exif_table()
                nextphoto_js={'tagids':[t.tag.id for t in nextphoto.tags.all()],
                              'id':nextphoto.id,
                              'fp':nextphoto.get_external_fp(),
                              'infozone':infozone,
                              'dayvlink':nextphoto.day and nextphoto.day.vlink() or '',
                              'photospothtml':nextphoto.get_photospothtml(),
                              }
                
                vals['nextphoto']=nextphoto_js
                vals['success']=True
                vals['message']='preloaded fp %s'%nextphoto_js['fp']
        elif kind=='new phototag':
            if 'tagname' in todo and todo['tagname']:
                name=make_safe_tag_name(todo['tagname'])
                try:
                    exi=PhotoTag.objects.get(name=name)
                    vals['message']='phototag of this name already existed'
                    vals['success']=False
                except PhotoTag.DoesNotExist:
                    pt=PhotoTag(name=name)
                    pt.save()
                    vals['message']='created phototag %s'%pt
                    vals['phototag_id']=pt.id
                    vals['name']=name
            else:
                vals['message']='bad text %s'%todo['tagname']
                vals['success']=False
        elif kind=='new photospot':
            if 'spotname' in todo and todo['spotname']:
                name=make_safe_tag_name(todo['spotname'])
                try:
                    exi=PhotoSpot.objects.get(name=name)
                    vals['message']='photospot of this name already existed'
                    vals['success']=False
                except PhotoSpot.DoesNotExist:
                    ps=PhotoSpot(name=name)
                    ps.save()
                    vals['message']='created photospot %s'%ps
                    vals['photospot_id']=ps.id
                    vals['name']=name
            else:
                vals['message']='bad text %s'%todo['tagname']
                vals['success']=False
        elif kind=='photospot':
            #assigning a photospot to a photo
            photo=Photo.objects.get(id=todo['photo_id'])
            spot=PhotoSpot.objects.get(id=todo['photospot_id'])
            photo.photospot=spot
            photo.save()
            vals['message']='assigned photospot.'
        
        elif kind=='phototag':
            #setting/removing phototags on a given Photo
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
                    tag=PhotoTag.objects.get(id=tagid)
                    if tag.name=='autoorient':
                        photo.autoorient()
                        goto_same=True
                    pht=PhotoHasTag(tag=tag, photo=photo)
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
            vals['message']='saved %d tags.'%photo.tags.count()
        
        elif kind=='remove photo from photospot':        
            #disassociate a photo from a photospot.
            #also mark it as not interesting any longer at all (so its out of incoming)
            photo=Photo.objects.get(id=todo['photo_id'])
            photo.undoable_delete()
            photo.save()
            #also mark it done & not incoming anymore.
            
            vals['message']='disassociated photo from photospot.  to undo, go here: %s'%photo.clink()
        elif kind=='save photospot crops':
            for crop in todo['crops']:
                photo=Photo.objects.get(id=crop['photo_id'])
                save=False
                if crop['xcrop']!=photo.xcrop:
                    photo.xcrop=crop['xcrop']
                    save=True
                if crop['ycrop']!=photo.ycrop:
                    photo.ycrop=crop['ycrop']
                    save=True
                if save:
                    photo.save()
            #save new crop info for a photo.  
            #the photo won't actually be modified on disk, but pages which support cropped views
            #(mostly photospot view page) will show it with cropping info.
            pass
        
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
        if goto_same:
            vals['message']='auto-oriented'
            vals['goto_next_photo']=True
            vals['next_photo_href']=photo.exhref()
        return r2j(vals)
    except Exception,e:
        vals['success']=False
        vals['message']=str(e)
        return r2j(vals)