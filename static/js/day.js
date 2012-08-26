var save_timeout=null;

$(document).ready(function(){
    //place_tags();
    //place_people();
    //setup_tag_clicks();
    $(".add-note").click(add_note);
    $(".add-note").click();
});

myinitSelection = function(element, callback) {
    var data = [];
    console.log(element.val());
    var ids = element.val().split(",");
    console.log(ids);
    $(ids).each(function() {
        var id=this;
        $(full_notekinds).each(function() {
            if (id.localeCompare(""+this.id)==0) data.push(this);
        });
    });
    callback(data);                   
}

function setup_nkselect(){
    $.each($(".notekindselect.new"), function(index, thing){
        $("#notekindsel-"+thing['id']);
        $(thing).removeClass("new");
        console.log('doing',thing);
        $.each(notekinds, function(index, nk){
            var th=$(thing);
            var option=$('<option value="'+index+'">'+nk+'</option>');
            th.append(option);
        });
        $(thing).select2({data:full_notekinds, 
            multiple: true,
            initSelection: myinitSelection,
        });
        
        $(".notekindselect").unbind('change').on('change', change_tag);
    });
    var divs=$(".select2-search-choice").find('div');
    $.each(divs, function(index, div){
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/notekind/'+div.innerHTML+'/">'+div.innerHTML+'</a>';
        }
    });
}

function change_tag(e){
    data_changed($(e.target), 'notekind');
}

function setup_savebutton(){
    $('.savebutton').unbind('click').click(function(e){data_changed($(e.target), 'note_text')});
}

function setup_textarea(){
    $(".textarea").live('keyup', function(e){
        clearTimeout(save_timeout);
        console.log('target is ',$(e.target));
        tar=$(e.target);
        save_timeout=setTimeout(function(e){data_changed(tar, 'note_text')}, 700);
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

function data_changed(target, kind){
    var data={'kind':kind};
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
    }else if (kind=='note_text'){
        data['note_text']=target.closest('.textarea').val();
        data['note_id']=target.closest('.note-row').attr('note_id');
    }else if (kind=='notekind'){
        data['note_id']=target.closest('.note-row').attr('note_id');
        data['notekind_ids']=target.attr('value');
    }else if (kind=='deletenote'){
        data['note_id']=target.closest('.note-row').attr('note_id');
        data['notekind_ids']=target.attr('value');
    }
    data['day_id']=$("#day_id").attr('day_id');
    send_data(data, target);
}

function send_data(data, target){
    console.log(data);
    $.ajax({
        url:'/ajax/day_data/',
        type:'POST',
        data:data,
        success:function(dat){
            var pdat=JSON.parse(dat)
            $("#notification").find('.alert').slideUp()
            $("#notification").append($('<div class="alert alert-success">'+pdat['message']+'</div>'));
            console.log('pdat',pdat);
            setTimeout(function(){$(".alert").slideUp()}, 1500);
            target.closest('.note-row').attr('note_id',pdat['note_id']);
            if (pdat['deleted']){
                debugger;
                if (target.closest('.note-row').attr('note_id')!='new'){
                    target.closest('.note-row').slideUp(function(){$(this).remove()});
                }
            }
        },
        error:function(pdat){
            $("#notification").find('.alert').slideUp().append($('<div class="alert alert-error">'+pdat['message']+'</div>'));
        }   
    });
}

function add_note(){
    $(".notezone").prepend($('#notemodel').clone().attr('id','').show());
    setup_textarea();
    setup_nkselect();
    setup_savebutton();
}

