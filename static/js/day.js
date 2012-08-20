$(document).ready(function(){
    console.log("docready.h")
    place_tags();
    place_people();
    setup_tag_clicks();
    setup_textarea();
    setup_savebutton();
});

var save_timeout=null;

function setup_savebutton(){
    $('.savebutton').click(function(){data_changed('text')});
}

function setup_textarea(){
    $(".textarea").bind('keyup', function(){
        clearTimeout(save_timeout);
        save_timeout=setTimeout(function(){data_changed('text')}, 2000);
    });
}

function zplace_tags(array, all, target, alltarget){
    $.each(array, function(index){
        $("#"+target).append(tagify(array[index]));   
    });
    $.each(all, function(index){
        var identifier=all[index];
        if (!($("#"+target).find('.tag[name="'+identifier+'"]').length)){
            $("#"+alltarget).append(tagify(all[index]));      
        }
    })
}

function place_tags(){
    $.each(exitags, function(index){
        $("#exitags").append(tagify(exitags[index]));   
    });
    $.each(alltags, function(index){
        var tagname=alltags[index];
        if (!($("#exitags").find('.tag[name="'+tagname+'"]').length)){
            $("#alltags").append(tagify(alltags[index]));      
        }
    })
}

function place_people(){
    $.each(exipeople, function(index){
        $("#exipeople").append(tagify(exipeople[index]));   
    });
    $.each(allpeople, function(index){
        var personname=allpeople[index];
        if (!($("#exipeople").find('.tag[name="'+personname+'"]').length)){
            $("#allpeople").append(tagify(allpeople[index]));      
        }
    })
}

function setup_tag_clicks(){
    $(".tag").live('click', toggle_tag);
}

function toggle_tag(e){
    var tag=$(e.target)
    var tagname=tag.attr('name')
    console.log("toggle tag"+tagname);
    var par=tag.parent();
    var zone=tag.closest('.zone');
    if (zone.hasClass('tagzone')){
        if (par.attr('id')=='exitags'){
            $("#alltags").append(tagify(tagname));
        }else{
            $("#exitags").append(tagify(tagname));
        }
        var dtype='tags';
    }
    else if (zone.hasClass('peoplezone')){
        if (par.attr('id')=='exipeople'){
            $("#allpeople").append(tagify(tagname));
        }else{
            $("#exipeople").append(tagify(tagname));
        }
        var dtype='people';
    }
    tag.remove();
    data_changed(dtype);
}   

function tagify(txt){
    return $("<div class='tag btn' name='"+txt+"'>"+txt+"</div>");
}

function data_changed(kind){
    var data={};
    if (kind=='tags'){
        var tags=$("#exitags").find('.tag')
        var tagnames=[];
        $.each(tags, function(index){
            tagnames.push($(tags[index]).attr('name'));
        });
        data['tagnames']=tagnames.join(',');
    }else if (kind=='people'){
        var tags=$("#exipeople").find('.tag')
        var tagnames=[];
        $.each(tags, function(index){
            tagnames.push($(tags[index]).attr('name'));
        });
        data['peoplenames']=tagnames.join(',');
    }else if (kind=='text'){
        var dat=$('.textarea').val();
        data['text']=dat;
    }
    send_data(data);
}

function send_data(data){
    data['day_id']=day_id;
    console.log('data is'+data);
    $.ajax({
        url:'/ajax/day_data/',
        type:'POST',
        data:data,
        success:function(dat){
            var pdat=JSON.parse(dat)
            $("#notification").find('.alert').slideUp()
            $("#notification").append($('<div class="alert alert-success">'+pdat['message']+'</div>'));
            setTimeout(function(){$(".alert").slideUp()}, 500);
        }   ,
        error:function(dat){
            $("#notification").find('.alert').slideUp().append($('<div class="alert alert-error">'+pdat['message']+'</div>'));
        }   
    });
}