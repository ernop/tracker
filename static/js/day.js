$(document).ready(function(){
    console.log("docready.h")
    place_tags();
    setup_tag_clicks();
});

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

function setup_tag_clicks(){
    $(".tag").live('click', toggle_tag);
}

function toggle_tag(e){
    var tag=$(e.target)
    var tagname=tag.attr('name')
    console.log("toggle tag"+tagname);
    var par=tag.parent();
    if (par.attr('id')=='exitags'){
        $("#alltags").append(tagify(tagname));
    }else{
        $("#exitags").append(tagify(tagname));
    }
    tag.remove();
    data_changed('tags');
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
        }   ,
        error:function(dat){
            $("#notification").find('.alert').slideUp().append($('<div class="alert alert-error">'+pdat['message']+'</div>'));
        }   
        
        }
        );
}