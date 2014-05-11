total_photos=photos.length
current_index=0;
show_current()

$(document).ready(function(){
  start_preloading()
  setup_keynav();
  setup_buttons();
  show_current()
})

function setup_buttons(){
  $('.next-btn').click(function(){
        show_next();
    })
    $('.prev-btn').click(function(){
        show_prev();
    })
    $('.save-crops').click(function(){
      save_crops();    
    })
}

function setup_keynav(){
  //keyboard left/right to cycle through photos
  //keyboard wasd to adjust crop
}

function start_preloading(){
  //preload all photos in order from the first.
  $.each(photos, function(index, photo){
    var thumbim=new Image;
    thumbim.src=photo.thumbfp;
    var im=new Image;
    im.src=photo.fp;
    photo.thumbim=thumbim;
    photo.im=im;
  })
}

function show_next(){
  if (current_index==total_photos-1){
    current_index=0
  }else{current_index=current_index+1}
  show_current()
}
function show_prev(){
  if (current_index==0){
    current_index=total_photos-1;
  }else{current_index=current_index-1}
  show_current()
}

function add_css(obj,xcrop,ycrop){
  obj.css('position','relative')
  obj.css('left','0')
  obj.css('right','0')
  if (xcrop){
    obj.css('left',String(-1*parseInt(xcrop))+'px')
    notify('cropped x'+parseInt(xcrop),true);    
    }
  if (ycrop){
    obj.css('top',String(parseInt(ycrop))+'px')
    notify('y'+parseInt(ycrop),true);    
    }
}

function show_current(){
  var photo=photos[current_index];
  $('.current-photo').find('img').remove()
  add_css($('.current-photo'), photo.xcrop, photo.ycrop)
  $('.current-photo').append(photo.im);
  $('.active-photo').removeClass('active-photo')
  $('.photothumb[photo_id='+photo.id+']').addClass('active-photo')
}

function crop_current(xx,yy){
  var photo=photos[current_index];
  photo.xcrop=photo.xcrop-xx
  photo.ycrop=photo.ycrop-yy
  show_current();
}

function save_crops(){
  var data={'kind':'save photospot crops'}
  var crops=[]
  $.each(photos, function(index, photo){
    var crop={'xcrop':photo.xcrop,'ycrop':photo.ycrop,'photo_id':photo.id}
    crops.push(crop)
  });
  data['crops']=crops;
  $.ajax({
    url:'/ajax/photo_data/',
    type:'post',
    //dataType:'json',
    data:JSON.stringify(data),
    success:function(json){
      notify(json['message'],json['success'])
    },
    error:function(json){
      notify('error',false);
    },
  })
}

function setup_keynav(){
  $(document.documentElement).keydown(function (event) {
     //handle cursor keys
     if (event.keyCode == 37) {
        show_prev()
    } else if (event.keyCode == 39) {
    
      show_next()
    }
    else if (event.keyCode==87){//up
      crop_current(0,-1);
    }
    else if (event.keyCode==65){//left
      crop_current(-1,0);
    }
    else if (event.keyCode==83){//down
      crop_current(0,1);
    }
    else if (event.keyCode==68){//right
      crop_current(1,0);
    }
    
});
}