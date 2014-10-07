var save_timeout=null;

$(document).ready(function(){
    setup_new_purch();
    display_purch();
    setup_new_measurement();
    display_measurement();
    setup_change_describer();
    $(".add-note").click(add_note);
    $(".add-note").click();
});


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
    data['day_id']=$("#day_id").attr('day_id');
    send_data(data, target);
}

function send_data(data, target){
    $.ajax({
        url:'/ajax/day_data/',
        type:'POST',
        data:data,
        success:function(dat){
            $("#notification").find('.alert').slideUp()
            $("#notification").append($('<div class="alert alert-success">'+dat['message']+'</div>'));
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

function add_note(){
    var newouter=$('#notemodel').clone().removeAttr('id');
    var innerrow=newouter.find('.note-row')
    $(".notezone").prepend(newouter);
    newouter.show();
    newouter.find('.notekindselect').addClass('new');
    setup_nkselect();
    setup_textarea();
    setup_savebutton();
}

