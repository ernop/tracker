var save_timeout=null;

$(document).ready(function(){
    setup_new_purch();
    display_purch();
    setup_new_measurement();
    display_measurement();
    setup_change_describer();
    //setup_mp3_recording();
    setup_notes();
    setup_popular_measurements();
});

function draw_note(dat, orig_dat){
    //callback for get_data(note)
    $('.notezone').prepend(dat['html']);
    setup_nkselect();
    setup_textarea();
    setup_savebutton();
    setup_notedel();
}

function del_note(dat){
    //userland hide note (option to undo later)
    $('.note-outline[note_id='+dat['note_id']+']').slideUp();
}

function setup_notedel(){
    $('.del-note').unbind('click').click(function(e){
        var note_id=$(this).closest('.note-outline').attr('note_id')
        get_data({'kind':'note','id':note_id,'action':'delete'}, del_note)
    })
}

function setup_notes(){
    $.each(noteids, function(index, noteid){
        var data={'kind':'note', 'id':noteid, 'action':'get'}
        get_data(data, wrap_callback_with_original_data(data, draw_note))
    })
    $(".add-note").click(function(){get_data({'kind':'note', 'action':'new', 'day_id':day_id},draw_note)});
}

myinitSelection = function(element, callback) {
    var data = [];
    var ids = element.val().split(",");
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
        $(thing).removeClass("new");
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
    fix_links();
}

function fix_links(){
    var divs=$(".select2-search-choice").find('div');
    $.each(divs, function(index, div){
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/notekind/'+div.innerHTML+'/">'+div.innerHTML+'</a>';
        }
    });
}

function change_tag(e){
    data_changed($(e.target), 'notekind');
    fix_links();
}

function setup_savebutton(){
    $('.savebutton').unbind('click').click(function(e){data_changed($(e.target), 'note_text')});
}

function setup_textarea(){
    $(".textarea").live('keyup', function(e){
        clearTimeout(save_timeout);
        tar=$(e.target);
        save_timeout=setTimeout(function(e){data_changed(tar, 'note_text')}, 700);
    });
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

//make them into clickable buttons.
function display_common_measurements(data){
    var dest = $(".common-measurement-spots");
    
    $.each(['samedate','samedow','all'], function(index, klass){
        var target = dest.find('#'+klass);
        $.each(data[klass], function(index, thing){
            var thingie='<div class="measurement-autochooser autochooser" val_id='+thing['id']+'>'+thing['name']+' ('+thing['count']+')</div>';
            target.append(thingie);
        });
    });
    
    $('.measurement-autochooser').click(function(e){set_measurement(e)});
}

function setup_tag_clicks(){
    $(".tag").live('click', toggle_tag);
}

function toggle_tag(e){
    var tag=$(e.target)
    var tagname=tag.attr('name')
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
    data['day_id']=day_id;
    send_data(data, target);
}

function get_data(data, callback){
    //lookup the html for a blob
    //new version of day page: everything as just IDs and then js looks it up & draws it
    $.ajax({
        url:'/ajax/get_data/',
        type:'POST',
        data:data,
        success:function(dat){
            notify(dat['message'], dat['success'])
            if (dat['success']){
                callback(dat)
            }
        },
        error:function(dat){
            notify('error',false)
        }
    });
}

function send_data(data, target){
    $.ajax({
        url:'/ajax/day_data/',
        type:'POST',
        data:data,
        success:function(dat){
            clear_notifications()
            notify(dat['message'],dat['success'])
            //$("#notification").find('.alert').slideUp()
            //$("#notification").append($('<div class="alert alert-success">'+dat['message']+'</div>'));
            setTimeout(function(){$(".alert").slideUp()}, 1500);
            target.closest('.note-row').attr('note_id',dat['note_id']);
            if (dat['deleted']){
                if (target.closest('.note-row').attr('note_id')!='new'){
                    target.closest('.note-row').slideUp(function(){$(this).remove()});
                }
            }
        },
        error:function(dat){
            $("#notification").find('.alert').slideUp().append($('<div class="alert alert-error">'+dat['message']+'</div>'));
        }
    });
}


