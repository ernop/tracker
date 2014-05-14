showing=false;
loaded_photos=[];
current_photo=null
past_photos=[]
keynav_active=true;
ii=0
$(document).ready(function(){
    load_show();
    setup_buttons();
    //setup_phototagselect(); //empty tags when first load, but all choices.
    setup_keynav();
})

function load_show(){
    console.log('load show start')
    load(maybe_show)
    console.log('load show end')
}

function load(donefunc){
    if (loaded_photos.length>25){return}
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
            exclude_ids.push(current_photo.id)
        }
        if (!exclude_ids){exclude_ids=null}
        var dat={'kind':'ajax photo preload','smithee':'blather'}
        if (exclude_ids && exclude_ids.length){
            dat['exclude_ids']=exclude_ids
        }
        console.log('doing dat',exclude_ids)
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
                            console.log("got duplicate",nextphoto.fp)
                            notify('dup',true)
                            return false}
                    })
                    if (!exi){//we actually got a new one...
                        
                        console.log("got new",nextphoto.id)
                        notify(json['message'],json['success'])
                        loaded_photos.push(nextphoto)
                        var im=new Image()
                        im.height=800
                        im.src=nextphoto.fp;
                        nextphoto.image=im
                        if (donefunc){donefunc.call(json)}
                    }
                    setTimeout(load(),1000);
                }
            },
            error:function(json){
                notify('error',false);
            },
        });
    }
}


function maybe_show(){
    console.log('maybe show start')
    if (!showing){
        show_next()
    }
    //setTimeout(load(),2000);
    console.log('maybe show end')
}

function show_prev(){
    var last=past_photos.pop()
    loaded_photos.unshift(last)
    show_next(true)
}

function show_next(going_backwards){
    console.log('show next start')
    next=loaded_photos.shift()
    console.log('got next',next)
    if (next){
        if (current_photo){
        
            if (going_backwards)
                {loaded_photos.unshift(current_photo)}   
            else{past_photos.push(current_photo)}
        }
        current_photo=next
        clear_infozone()
        clear_photozone()
        put_infozone(next)
        put_photozone(next)
        put_photospot(next)
        notify(next.fp,true);
        showing=true;
        reset_photo_tags();
        reset_photospot_select2();
        keynav_active=true
    }else{
        notify('no photo was ready',false)
    }
    console.log('show next end')
    //if (loaded_photos.length<10)
    //{load();}
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
        console.log('setting current')
        sel.attr('value',current_photo.photospot.id);
    }else{
        sel.attr('value',null);
    }
    sel.select2({data:full_photospots,
        multiple:false,
        //initSelection: function(element,callback){
            //callback(get_photospot_for_current_photo())
        //}
    })
    sel.unbind('change').on('change', change_photospot)
}

function reset_photo_tags(){
    //after loading a photo, set the phototags for it
    //based on the current_photo object
    console.log('reset photo tags start')
    var sel=$('#phototagselect2');
    sel.attr('value',current_photo.tagids.join(','))
    //sucks that even if you setup initselection based, select2 won't call it
    //unless you ALSO define a "value" field on the select2 element, EVEN if you never use that!
    sel.select2({data:full_phototags,
        multiple:true,
        initSelection: function(element,callback){
            callback(get_tags_for_current_photo())
        }
    })
    //first time you set it up its empty.  each re-getting data will re-set it.
    //fix_phototags()
    sel.unbind('change').on('change', change_phototag)
    console.log('reset photo tags end')
}

function get_tags_for_current_photo(){
    console.log('get current tags start')
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
    console.log('get current tags end',data)
    return data;
}

function get_photospot_for_current_photo(){
    if (current_photo && current_photo.photospot)
        {return current_photo.photospot.id}
    return []
}

function maybe_goto_next(tagids){
    console.log('tagids are',tagids);
    $.each(tagids, function(index, tagid){
        if (TAGIDS_WHICH_FORCE_NEXT.indexOf(parseInt(tagid))!=-1){
            show_next()
            return false;
        }
    })
}

function change_phototag(e){
    console.log('change phototag start')
    if (e){var target=$(e.target)}else{
    var target=$('#phototagselect2')}
    data_changed(target, 'phototag');
    fix_phototags();
    current_photo.tagids=target.attr('value').split(',');
    maybe_goto_next(current_photo.tagids)
    console.log('change phototag end')
}

function change_photospot(e){
    console.log('change photospot start')
    if (e){var target=$(e.target)}else{
    var target=$('#photospotselect2')}
    current_photo.photoid=target.attr('value');
    data_changed(target, 'photospot');
    
    //maybe_goto_next(current_photo.tagids)
    console.log('change photospot end')
}

function create_tag(tagname, success_func){
    //check we dont have it already
    data={kind:'new phototag',tagname:tagname}
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            notify(dat['message'],dat['success']);
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
    data={kind:'new photospot',spotname:spotname}
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            notify(dat['message'],dat['success']);
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
  ctarget.find('a').remove()
  vtarget.find('a').remove()
  $.each(tagids, function(index,tagid){
    var tag=get_phototag(tagid);
    if (!tag){return}
    ctarget.append('<a class="btn" href="/admin/day/phototag/?id='+tag.id+'">'+tag.name+'</a> ')
    vtarget.append('<a class="btn" href="/photo/phototag/'+tag.name.replace(/ /g,'_')+'">'+tag.name+'</a> ')
  })
}

function update_spot_info(spotid){
  var ctarget=$('.cspotzone')
  var vtarget=$('.vspotzone')
  ctarget.find('a').remove()
  vtarget.find('a').remove()
  var spot=get_photospot(spotid);
  if (spot){
    ctarget.append('<a class="btn" href="/admin/day/photospot/?id='+spot.id+'">'+spot.name+'</a> ')
    vtarget.append('<a class="btn" href="/photo/photospot/'+spot.name.replace(/ /g,'_')+'">'+spot.name+'</a> ')
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
    if (photospot.id==photospot_id){res=photospot;return false}
    
  })
  return res
}

function data_changed(target, kind){
    var data={'kind':kind};
    if (kind=='phototag'){
        data['phototag_ids']=target.attr('value');
        update_tag_info(target.attr('value').split(','));
    }else if (kind=='photospot'){
        data['photospot_id']=target.attr('value');
        update_spot_info(target.attr('value'))
    }
    data['photo_id']=$(".photozone").attr('photo_id')
    send_data(data, target);
}

function send_data(data, target){
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            notify(dat['message'],dat['success']);
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
        notify('creating photospot based on form submit '+photospotname,true);
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
    console.log('put infozone')
    $('.infozone').append(make_infozone(photo))
}
function put_photozone(photo){
    console.log('put photozone')
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
  $(document.documentElement).keydown(function (event) {
    if (!keynav_active){return}
    if (event.keyCode==84){ //t
        pop_tag()
        keynav_active=false;
    }
    if (event.keyCode==80){ //p
            pop_photospot()
            keynav_active=false;
    }
     //if (event.keyCode == 37) {
        //show_prev()
    //} else if (event.keyCode == 39) {
    
      //show_next()
    //}
    //else if (event.keyCode==87){//up
      //crop_current(0,1);
    //}
    //else if (event.keyCode==65){//left
      //crop_current(-1,0);
    //}
    //else if (event.keyCode==83){//down
      //crop_current(0,-1);
    //}
    //else if (event.keyCode==68){//right
      //crop_current(1,0);
    //}
    //else if (event.keyCode==88){//x
      //kill_current();
    //}
    //else if (event.keyCode==72){//x
      //flip_first();
    //}
    
});
}
