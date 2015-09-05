
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
def photoajax_nonmine(request):
    return photoajax(nonmine=True, mine=False)

@user_passes_test(staff_test)
def photoajax(request, nonmine=False, mine=True):
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
    vals['TAGIDS_WHICH_FORCE_NEXT']=[tt.id for tt in PhotoTag.objects.filter(name__in=settings.ADVANCING_TAGS)]
    vals['TAGIDS_WHICH_FORCE_PREV']=[tt.id for tt in PhotoTag.objects.filter(name__in=['back','undo','last'])]
    #get the tags
    vals['delete_phototag_id']=PhotoTag.objects.get(name='delete').id
    vals['done_phototag_id']=PhotoTag.objects.get(name='done').id
    vals['screenshot_phototag_id']=PhotoTag.objects.get(name='screenshot').id
    vals['nonmine']=nonmine
    vals['mine']=mine
    return r2r('jinja2/photo/photoajax.html',request,vals)

#def incoming_photospot_photos_ajax(request):
    #'''go through all photospos incoming photos '''
        #vals={}
    #vals['full_phototags']=get_full_phototags()
    #vals['full_photospots']=get_full_photospots()
    ##vals['TAGIDS_WHICH_FORCE_NEXT']=[tt.id for tt in PhotoTag.objects.filter(name__in=settings.ADVANCING_TAGS)]
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
def phototag_id(request,id):
    pt=PhotoTag.objects.get(id=id)
    return phototag(request,name=pt.name)

@user_passes_test(staff_test)
def phototag(request,name=None):
    name=name.replace('%20',' ')
    phototag=PhotoTag.objects.get(name=name)
    if not can_access_private(request.user) and phototag.name in settings.EXCLUDED_TAGS:
        return HttpResponseRedirect('/photo/incoming/')
    vals={}
    vals['phototag']=phototag
    return r2r('jinja2/photo/phototag.html',request,vals)


@user_passes_test(staff_test)
def photoset(request,tagset):
    '''show a bunch of photo thumbnails.  clicking one results in a nice fast preloaded display (like photoajax)
    with/without edit options.  along the top are the currently defined tags & links to +1 tag / -1 tag
    
    v1 just thumbnails.'''
    vals={}
    from urllib import unquote
    names=unquote(unquote(tagset))
    names=names.split(',')
    
    rawphotos=Photo.objects.filter(deleted=False)
    addnames=[]
    killnames=[]
    jumps=[]
    photos=rawphotos
    phototags=[]
    for name in names:
        if name in settings.EXCLUDE_FROM_PHOTOSET_TAGS:
            continue
        #clean it cause this is a bit messy
        lookupname=name.replace("(organization)",'').strip()
        photos=photos.filter(tags__tag__name=lookupname)
        phototags.append(PhotoTag.objects.get(name=lookupname))
        nt=names[:]
        nt.remove(name)
        nt.sort()
        
        if len(nt)>0:
            subphotos=rawphotos
            for subnt in nt:
                lookupsub=subnt.replace("(organization)",'').strip()
                subphotos=subphotos.filter(tags__tag__name=lookupsub)
            killtext=name
            killcount=subphotos.count()
        else:
            killtext=name
            killcount=0
        killnames.append((','.join(nt),killtext, killcount))
        if len(names)!=1:
            jumps.append((name, name, photos.count()))
    photos=photos.distinct()
    #self.taken or (self.day and self.day.date) or self.photo_created or No
    photoids=[p.id for p in photos]
    #PhotoHasTag.objects.filter(photo__id__in=photoids)
    rel_tags=PhotoTag.objects.filter(photos__photo__id__in=photoids)
    from django.db.models import Count
    rel_tags=rel_tags.annotate(ct=Count('name')).order_by('-ct')
    for rt in rel_tags[:25]:
        if rt.name in names or rt.name in settings.EXCLUDE_FROM_PHOTOSET_TAGS:
            continue
        
        nt=names[:]
        nt.append(rt.name)
        nt.sort()
        addlinkname=rt.name
        addnames.append((','.join(nt),addlinkname,rt.ct))
        jumps.append((rt.name,rt.name,rt.photos.count()))
    vals['photocount']=photos.count()
    photos=photos[:500]
    photos.sort(key=lambda x:x.get_using_time())
    #addnames=[]
    vals['photos']=photos
    #vals['phototags']=[PhotoTag.objects.get(name=name) for name in names]
    vals['phototags']=phototags
    if len(killnames)==1:
        #cant kill the last one...
        vals['killnames']=[]
    else:vals['killnames']=killnames
    
    vals['addnames']=addnames
    vals['jumps']=sorted(list(set(jumps)))
    return r2r('jinja2/photo/photoset.html',request,vals)

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
    vals['photos']=pspot.photos.exclude(deleted=True).order_by('-founded','day__date')
    vals['photo_objs']=[photo2obj(pho) for pho in pspot.photos.exclude(deleted=True).order_by('-founded','day__date')]
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
        from util import ipdb;ipdb()
    response['Cache-Control'] = 'max-age=86400	'
    return response

@user_passes_test(staff_test)
def ajax_photo_data_nonmine(request):
    return ajax_photo_data(request, mine=False, nonmine=True)

@user_passes_test(staff_test)
def ajax_photo_data(request, mine=True, nonmine=False):
    '''also if "force id" is sent just return that photo.'''
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
        goto_same=False
        nextphoto=''
        if kind=='ajax photo preload':
            try:
                if 'exclude_ids[]' in request.POST and request.POST['exclude_ids[]']:
                    #exclude_ids=[int(_) for _ in request.POST['exclude_ids[]'].split(',')]
                    exclude_ids=request.POST.getlist('exclude_ids[]')
                else:
                    exclude_ids=None
            except Exception,e:
                from utils import ipdb;ipdb()
            if 'force id' in todo and todo['force id']:
                nextphoto=get_next_incoming(force_id=todo['force id'], exclude=exclude_ids)
            else:
                nextphoto=get_next_incoming(exclude=exclude_ids, mine=mine, nonmine=nonmine)
            log.info('got nextphoto %s',nextphoto)
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
                              'resolutionx':nextphoto.resolutionx,
                              'resolutiony':nextphoto.resolutiony,
                              }
                vals['nextphoto']=nextphoto_js
                vals['success']=True
                vals['message']='preloaded %s'%nextphoto.name
        elif kind=='kill day' or kind=='restore day':
            '''restore/kill the associated "day" object on a given photo.'''
            ph=Photo.objects.get(id=todo['photo_id'])
            vals['success']=True
            if kind=='kill day':
                ph.day=None
                ph.myphoto=False
                vals['message']='day killed'
            elif kind=='restore day':
                daysetres=ph.set_day()
                ph.myphoto=True
                if daysetres:
                    vals['message']='set day.'
                else:
                    vals['message']='no day set.'
                    vals['success']=False
            ph.save()
            
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
                    log.info('same name existed: %s',name)
                except PhotoSpot.DoesNotExist:
                    photo=Photo.objects.get(id=todo['photo_id'])
                    ps=PhotoSpot(name=name,founding_photo=photo)
                    ps.save()
                    vals['message']='created photospot %s with this as the founding.'%ps
                    vals['photospot_id']=ps.id
                    vals['name']=name
                    log.error('new photospot name created: %s', name)
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
            #return the thumb
            if spot.founding_photo:
                vals['founding_thumb_fp']=spot.founding_photo.get_external_fp(thumb=True)
            else:
                vals['founding_thumb_fp']=''
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
            elif PhotoHasTag.objects.filter(tag__name='undelete').exists() and photo.deleted:
                photo.undelete()
                photo.tags.filter(tag__name='undelete').delete()
                #dont actually leave the "undelete" tag on there, its weird
            if photo.tags.filter(tag__name='done').exists() and photo.incoming:
                #move on from incoming guys once "done" is entered
                photo.done()
            if photo.tags.filter(tag__name='myphoto').exists():
                #move on from incoming guys once "done" is entered
                photo.myphoto=True
                photo.save()
            if photo.tags.filter(tag__name__in=settings.ADVANCING_TAGS).exclude(tag__id__in=kept_tagids):
                #actually was assigned this tag
                photo.done()
            #vals['message']='saved %d tags.'%photo.tags.count()
            vals['message']=''
        
        elif kind=='remove photo from photospot':        
            #disassociate a photo from a photospot.
            #also mark it as not interesting any longer at all (so its out of incoming)
            photo=Photo.objects.get(id=todo['photo_id'])
            #photo.undoable_delete()
            photo.photospot=None
            photo.tags.find(tag__name='done').remove()
            photo.incoming=True
            photo.save()
            #also mark it done & not incoming anymore.
            
            vals['message']='disassociated photo from photospot. %s'%photo.clink()
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
            vals['message']='saved %d crops'%len(todo['crops'])
        else:
            log.error('bad k %s',k)
            from utils import ipdb;ipdb()
        return r2j(vals)
    except Exception,e:
        from utils import ipdb;ipdb()
        tb=traceback.format_exc()
        log.error('error; exception. %s %s %s %s',e,todo,nextphoto,tb)
        vals['success']=False
        vals['message']='%s %s %s %s'%(todo,kind,e,nextphoto)
        return r2j(vals)
    

@user_passes_test(staff_test)
def photostats(request):
    #axes
    #incoming
    #deleted
    
    #iso
    #camera
    #mm
    #aperture
    #exposure
    fields='incoming deleted'.split()
    exiffields='iso camera mm aperture exposure'.split()
    
    photos=Photo.objects.all()
    res={}
    for exiffield in exiffields:
        #statfield='%s_%d'%(field,val)
        res[exiffield]=[]
        guys=Photo.objects.raw('select id,count(*) as ct,%s from photo group by 3 order by 2 desc'%(exiffield))
        for nn in range(100):
            try:
                guy=guys[nn]
            except:
                break
            exifval=(getattr(guy,exiffield))
            res[exiffield].append((exifval,guy.ct))
    vals={'res':res}
    vals['totaldone']=Photo.objects.filter(tags__tag__name='done').count()
    vals['totaldeleted']=Photo.objects.filter(deleted=True).count()
    vals['totalphotos']=Photo.objects.count()
    vals['totalincoming']=Photo.objects.filter(incoming=True).count()
    vals['total_mycam']=Photo.objects.filter(incoming=True).count()
    return r2r('jinja2/photo/photostats.html',request,vals)

@user_passes_test(staff_test)
def photodups(request):
    photos=Photo.objects.raw('select id,name,count(*) as ct from photo group by 2 having ct>1 order by ct desc,name')
    done_names=set()
    links=[]
    ii=0
    while 1:
        try:
            photo=photos[ii]
            if photo.name in done_names:
                continue
            done_names.add(photo.name)
            link='<a href="/admin/day/photo/?name=%s">%s</a>'%(photo.name, photo.name)
            links.append(link)
        except:
            break
        ii+=1
        if ii>30:
            break
    vals={}
    vals['links']=links
    return r2r('jinja2/photo/photodups.html',request,vals)

@user_passes_test(staff_test)
def photohashdups(request):
    photos=Photo.objects.raw('select id,hash,count(*) as ct from photo group by 2 having ct>1 order by ct desc,fp')
    done_names=set()
    links=[]
    ii=0
    while 1:
        try:
            photo=photos[ii]
            if photo.hash in done_names:
                continue
            done_names.add(photo.hash)
            link='<a href="/admin/day/photo/?hash=%s">%s</a>'%(photo.hash, photo.hash)
            links.append(link)
        except:
            break
        ii+=1
        if ii>30:
            break
    vals={}
    vals['links']=links
    return r2r('jinja2/photo/photodups.html',request,vals)
