showing=false;
loaded_photos=[];
current_photo=null
past_photos=[]
keynav_active=true;
ii=0
initial_load_done=false
force_id=null;
last_saved_tags=null;

function get_hash_id(){
    //check if there's something like #!id=<id> and if so, load that one first.
    hsh=document.location.hash;
    if (hsh.indexOf('id=')!=-1){
        var id=hsh.slice(5);   
        id=parseInt(id);
        if (id){
            return id;        
        }
    }
}

$(document).ready(function(){
    force_id=get_hash_id();
    was_force_id=force_id;
    load_show()
    setup_buttons();
    setup_keynav();
    
})

function setup_kill_day(){
    $('.kill_day_btn').unbind('click')
    $('.kill_day_btn').click(function(){
	kill_day();
    })
}

function load_show(id){
    //console.log('in load show, calling load')
    var only_one=false;
    if (was_force_id){var only_one=true}
    //if its a force_id only load one.
    load(maybe_show, only_one)
}

function load_one(){
    //console.log('calling load one.')
    load(null, true)}



function kill_day(restore){
    //kill the related day for a photo
    var photo_id=$(".photozone").attr('photo_id')
    var data={'photo_id':photo_id,kind:'kill day'}
    if (restore){
	data['kind']='restore day'	
    }
    send_data(data)
}

function load(donefunc, only_one){
    if (loaded_photos.length>25){initial_load_done=true;return}
    ii=ii+1
    
    var fake=0
    if (fake){
        var fakephoto={tagids:[ii*3,ii*4+1],id:ii,fp:'/static/incomingphoto/'+ii+'.jpg',infozone:'<table class="table thintable"><tr><td>stuff</table>'}
        //receive fp, infobox.  add on a photo image.
        var im=new Image()
        im.height=800
        im.src=fakephoto.fp;
        fakephoto.image=im
        loaded_photos.push(fakephoto)
        if (donefunc){donefunc.call()}
    }else{
        var exclude_ids=[]
        $.each(loaded_photos, function(index,guy){exclude_ids.push(guy.id)})
        $.each(past_photos, function(index,guy){exclude_ids.push(guy.id)})
        if (current_photo){
	    if (exclude_ids.indexOf(current_photo.id)==-1)
                {exclude_ids.push(current_photo.id)}
        }
        if (!exclude_ids){exclude_ids=null}
        var dat={'kind':'ajax photo preload','smithee':'blather'}
        if (exclude_ids && exclude_ids.length){
            dat['exclude_ids']=exclude_ids
        }
        if (force_id){
            dat['force id']=force_id;
            force_id=null;
        }
        //console.log('doing load',exclude_ids.length)
        $.ajax({
            url:'/ajax/photo_data/',
            type:'post',
            data:dat,
            success:function(json){
                if (json['success']){
                    var nextphoto=json.nextphoto
                    var exi=false
                    $.each(loaded_photos, function(index, lp){
                        if (lp.id==nextphoto.id){
                            exi=true
                            //console.log("got duplicate",nextphoto.fp)
                            notify('dup, loaded:'+loaded_photos.length,true);
                            setTimeout(load_one(),0);
                            return false}
                    })
                    if (!exi){//we actually got a new one...
                        //console.log("got new",nextphoto.id)
                        notify(json['message']+' preloaded this many:'+loaded_photos.length,json['success'])
                        loaded_photos.push(nextphoto)
                        //should calculate the display height here.
                        //maxes: height 800, width 1100
                        var im=new Image()
                        var xmax=1100;
                        var ymax=800;
                        if (nextphoto.resolutionx>xmax && nextphoto.resolutiony>ymax){
                            //scale both
                            var scale=Math.max(nextphoto.resolutionx/xmax,nextphoto.resolutiony/ymax)
                            im.height=nextphoto.resolutiony/scale
                            im.width=nextphoto.resolutionx/scale
                        }else if (nextphoto.resolutionx>=xmax){
                            var scale=nextphoto.resolutionx/xmax
                            im.height=nextphoto.resolutiony/scale
                            im.width=xmax
                        }else if (nextphoto.resolutiony>=ymax){
                            var scale=nextphoto.resolutiony/ymax
                            im.height=ymax
                            im.width=nextphoto.resolutionx/scale
                        }else{
                            if (nextphoto.resolutionx != null)
                            {im.height=nextphoto.resolutiony
                            im.width=nextphoto.resolutionx}
                        }
                        //im.height=800
                        im.src=nextphoto.fp;
                        nextphoto.image=im
                        if (donefunc){donefunc.call(json)}
                    }
                    if (!only_one){
                        //console.log('calling load in success of load')
                        setTimeout(load(),1000);
                    }
                }
            },
            error:function(json){
                notify('error',false);
            },
        });
    }
}

function maybe_show(){
    //console.log('maybe show start')
    if (!showing){
        show_next()
    }
    //console.log('maybe show end')
}

function show_prev(){
    var last=past_photos.pop()
    loaded_photos.unshift(last)
    show_next(true)
}

function show_next(going_backwards){
    if (initial_load_done && loaded_photos.length<23){
        initial_load_done=false;
        load();
        //console.log('restarted load process.')
    }
    //console.log('show next start')
    next=loaded_photos.shift()
    if (next){
        //console.log('got next',next.id)
        if (current_photo){
            if (going_backwards)
                {loaded_photos.unshift(current_photo)}   
            else{
                past_photos.push(current_photo)
                if (past_photos.length>10){
                    //keep more old photos.
                    past_photos.shift();                
                }
            }
        }
        current_photo=next
        clear_infozone()
        clear_photozone()
        put_infozone(next)
        put_photozone(next)
        put_photospot(next)
        //notify(next.fp,true);
        showing=true;
        reset_photo_tags();
        reset_photospot_select2();
        keynav_active=true
	setup_kill_day();
    }else{
        notify('no photo was ready',false)
    }
    //console.log('show next end')
    //if (loaded_photos.length<20)
        //{console.log('calling load one since loaded photos length < 20')
        //load_one();}
}

function pop_tag(){
    //force focus to the tag/control box select 2 thing.
    var select2=$('#phototagselect2').data('select2');
    setTimeout(function() {
        if (!select2.opened()) {
            select2.open();
        }
    }, 0); 
}

function pop_photospot(){
    //force focus to the tag/control box select 2 thing.
    var select2=$('#photospotselect2').data('select2');
    setTimeout(function() {
        if (!select2.opened()) {
            select2.open();
        }
    }, 0); 
}

function reset_photospot_select2(){
    var sel=$('#photospotselect2');
    if (current_photo.photospot){
        //console.log('setting current')
        sel.attr('value',current_photo.photospot.id);
    }else{
        sel.attr('value',null);
    }
    sel.select2({data:full_photospots,
        multiple:false,
        //initSelection: function(element,callback){
            //callback(get_photospot_for_current_photo())
        //}
	formatResult:function(guy){return guy['text']},
    })
    
    
    
    
    
    sel.unbind('change').on('change', change_photospot)
}

function reset_photo_tags(){
    //after loading a photo, set the phototags for it
    //based on the current_photo object
    //console.log('reset photo tags start')
    var sel=$('#phototagselect2');
    sel.attr('value',current_photo.tagids.join(','))
    //sucks that even if you setup initselection based, select2 won't call it
    //unless you ALSO define a "value" field on the select2 element, EVEN if you never use that!
    sel.select2({data:full_phototags,
        multiple:true,
        minimumInputLength: 2,
        initSelection: function(element,callback){
            callback(get_tags_for_current_photo())
        }
    })
    //first time you set it up its empty.  each re-getting data will re-set it.
    //fix_phototags()
    sel.unbind('change').on('change', change_phototag)
    //console.log('reset photo tags end')
}

function get_tags_for_current_photo(){
    //console.log('get current tags start')
    //grab the tags from the full tag js object.
    var data = [];
    var ids = current_photo.tagids;
    $.each(ids, function(index,id){
        $.each(full_phototags, function(pindex, phototag){
            if (phototag.id==id){
                data.push(phototag);
            }
        })
    })
    //console.log('get current tags end',data)
    return data;
}

function get_photospot_for_current_photo(){
    if (current_photo && current_photo.photospot)
        {return current_photo.photospot.id}
    return []
}

function maybe_goto_next(tagids){
    //console.log('tagids are',tagids);
    $.each(tagids, function(index, tagid){
        if (TAGIDS_WHICH_FORCE_NEXT.indexOf(parseInt(tagid))!=-1){
            show_next()
            return false;
        }else if (TAGIDS_WHICH_FORCE_PREV.indexOf(parseInt(tagid))!=-1){
            show_prev()
            return false;
        }
    })
}

function change_phototag(e){
    //console.log('change phototag start')
    if (e){var target=$(e.target)}else{
    var target=$('#phototagselect2')}
    data_changed(target, 'phototag');
    fix_phototags();
    current_photo.tagids=target.attr('value').split(',');
    maybe_goto_next(current_photo.tagids)
    //console.log('change phototag end')
}

function change_photospot(e){
    console.log('change photospot start')
    if (e){var target=$(e.target)}else{
    var target=$('#photospotselect2')}
    current_photo.photoid=target.attr('value');
    data_changed(target, 'photospot');
    
    //maybe_goto_next(current_photo.tagids)
    //console.log('change photospot end')
}

function create_tag(tagname, success_func){
    //check we dont have it already
    data={kind:'new phototag',tagname:tagname}
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            if (dat['message'] && dat['message'].length)
            {notify(dat['message'],dat['success']);}
            if (dat['success']){
                var ptag={id:dat.phototag_id,text:dat.name,name:dat.name};
                full_phototags.push(ptag);
                if (success_func){
                    success_func(ptag)
                }
            }
        },
        error:function(dat){
            notify('error',false);
        }
    })
}


function create_photospot(spotname, success_func){
    //check we dont have it already
    data={kind:'new photospot',spotname:spotname,'photo_id':$(".photozone").attr('photo_id')}
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            if (dat['message'] && dat['message'].length)
            {notify(dat['message'],dat['success']);}
            if (dat['success']){
                var pspot={id:dat.photospot_id,text:dat.name,name:dat.name};
                full_photospots.push(pspot);
                if (success_func){
                    success_func(pspot)
                }
            }
        },
        error:function(dat){
            notify('error',false);
        }
    })
}

function update_tag_info(tagids){
  //as you add tags etc. fix the name info zone too.  could be done with
  //ajax but this is faster
  var ctarget=$('.ctagzone')
  var vtarget=$('.vtagzone')
  var settarget=$('.photosetzone')
  ctarget.find('a').remove()
  vtarget.find('a').remove()
  settarget.find('a').remove()
  combo=''
  clean_tags=[]
  META_TAGS=['done','delete','repeat']
  $.each(tagids, function(index,tagid){
    var tag=get_phototag(tagid);
    if (!tag){return}
    ctarget.append('<a class="btn btn-default" href="/admin/day/phototag/?id='+tag.id+'">'+tag.name+'</a> ')
    vtarget.append('<a class="btn btn-default" href="/photo/phototag_id/'+tag.id+'">'+tag.name+'</a> ')
    clean_name=tag.name.replace(' (person)','')
    settarget.append('<a class="btn btn-default" href="/photo/photoset/'+clean_name+'">'+tag.name+'</a> ')
    if (META_TAGS.indexOf(clean_name)==-1){
        clean_tags.push(clean_name)}
  })
    var alltags=clean_tags.join(',')
  settarget.append('<a class="btn btn-default" href="/photo/photoset/'+alltags+'">ALL</a> ')
}

function update_spot_info(spotid){
    //draw in the photospot link etc.
    //would be better if this came through ajax rather than hacked ...
  var ctarget=$('.cspotzone')
  var vtarget=$('.vspotzone')
  ctarget.find('a').remove()
  vtarget.find('a').remove()
  var spot=get_photospot(spotid);
  if (spot){
    ctarget.append('<a class="btn btn-default" href="/admin/day/photospot/?id='+spot.id+'">'+spot.name+'</a> ')
    vtarget.append('<a class="btn btn-default" href="/photo/photospot/'+spot.name.replace(/ /g,'_')+'">'+spot.name+'</a> ')
  }
}

function get_phototag(tagid){
  var res=null
  $.each(full_phototags, function(index, tag){
    if (tag.id==tagid){res=tag;return false}
    
  })
  return res
}

function get_photospot(photospot_id){
  var res=null
  $.each(full_photospots, function(index, photospot){
    if (photospot.id==photospot_id){
        res=photospot;return false}
  })
  return res
}

function data_changed(target, kind, override){
    var data={'kind':kind};
    if (kind=='phototag'){
        if (override){
            data['phototag_ids']=override
        }
        else{
            data['phototag_ids']=target.attr('value');
            last_saved_tags=target.attr('value')
            last_saved_tags_list=last_saved_tags.split(',')
            last_saved_tags_text=[]
            $.each(last_saved_tags_list, function(index,guy){
                var tag=get_phototag(guy);
                last_saved_tags_text.push(tag.name)
            })
            last_saved_tags_text=last_saved_tags_text.join(' ')
            update_tag_info(last_saved_tags_list);
        }
    }
    else if (kind=='photospot'){
        data['photospot_id']=target.attr('value');
        update_spot_info(target.attr('value'))
	//also show the thumb for the rel spot.
    }
    data['photo_id']=$(".photozone").attr('photo_id')
    send_data(data);
}

function send_data(data){
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            if (dat['message'] && dat['message'].length)
            {notify(dat['message'],dat['success']);}
        },
        error:function(dat){
            notify('error',false);
        }
    });
}

function setup_buttons(){
    $('.next-btn').click(function(){
        show_next();
    })
    $('.prev-btn').click(function(){
        show_prev();
    })
    
    $('#create-new-tag-form').submit(function(e){
        var tagname=$('#create-new-tag-input').val();
        notify('creating tag based on form submit '+tagname,true);
        create_tag(tagname, function(ptag){
            //function to be called if creation is ok.
                if (ptag){
                    current_photo.tagids.push(ptag.id)
                    reset_photo_tags();
                    change_phototag();
                }
            })
        $('#create-new-tag-input').val('')
    });
    
    $('#create-new-photospot-form').submit(function(e){
        var photospotname=$('#create-new-photospot-input').val();
        notify('creating photospot based on form submit '+photospotname, true);

        create_photospot(photospotname, function(pspot){
            //function to be called if creation is ok.
                if (pspot){
                    current_photo.photospot=ptag
                    reset_photospot_select2();
                    change_photospot();
                }
            })
        $('#create-new-photospot-input').val('')
    });    
    
}

function clear_infozone(){
    $('.infozone').empty()
}
function clear_photozone(){
    $('.photozone').empty()
}

function put_infozone(photo){
    //console.log('put infozone')
    $('.infozone').append(make_infozone(photo))
}
function put_photozone(photo){
    //console.log('put photozone')
    $('.photozone').append(make_photozone(photo))
    $('.photozone').attr('photo_id',photo.id)
}

function put_photospot(photo){
    $('.photospotzone').append(photo.photospothtml)
}

function make_infozone(photo){
    return photo.infozone;
}

function make_photozone(photo){
    var photo=$(photo.image).wrap('<div class="photo">').parent()
    return photo
}

function setup_keynav(){
    //manually clicking tag zone disables it.
    $('.tagzone').bind('click',function(e){
        if (keynav_active && !(e.isTrigger)){
            //wow, pushing enter triggers click.  so just dont cancel in this case.
            keynav_active=false;
            notify('keynav inactive',0)
        }
    })
    $(document.documentElement).keydown(function (event) {
        //notify(event.keyCode,1);
        if (!keynav_active){return}
        if (event.keyCode==84){ //t
            pop_tag()
            keynav_active=false;
        }
        else if (event.keyCode==80){ //p
            pop_photospot()
            keynav_active=false;
        }
        else if (event.keyCode==68){ //d for delete
            if (keynav_active){
                data_changed(null,'phototag',(delete_phototag_id+''))
                show_next();
                notify('deleted',1)
            }
        }
        else if (event.keyCode==78){ //done, go to next.
            if (keynav_active){
                data_changed(null,'phototag',(done_phototag_id+''))
                show_next();
                notify('skipped',1)
            }
        }
        else if (event.keyCode==83){ //done, go to next.
            if (keynav_active){
                data_changed(null,'phototag',(screenshot_phototag_id+''))
                show_next();
                notify('screenshot',1)
            }
        }
        else if (event.keyCode==82){ //done, go to next.
            if (keynav_active){
                if (last_saved_tags){
                    data_changed(null,'phototag',last_saved_tags)
                    show_next();
                    notify('repeat tags '+last_saved_tags_text,1)
                }else{
                    notify('no saved tags.',0)
                }
                
            }
        }
    });
}
