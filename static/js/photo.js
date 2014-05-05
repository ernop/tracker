photoInitSelection = function(element, callback) {
    var data = [];
    var ids = element.val().split(",");
    $(ids).each(function() {
        var id=this;
        $(full_phototags).each(function() {
            if (id.localeCompare(""+this.id)==0) data.push(this);
        });
    });
    callback(data);
}


$(document).ready(function(){
    setup_phototagselect();
    var select2=$('#phototagselect2').data('select2');
    setTimeout(function() {
        if (!select2.opened()) {
            select2.open();
        }
    }, 0); 
    if (next_photopaths){
        $.each(next_photopaths, function(index,photopath){
            var nxt=new Image();
            nxt.src=photopath;
            console.log('starting to load',photopath)
        })
        
    }
})
    
function setup_phototagselect(){
    var ptg=$('#phototagselect2');
    $.each(full_phototags, function(index,pt){
        var phototagselect=$('#phototagselect2');
        var option=$('<option value="'+index+'">'+pt+'</option>');
        ptg.append(option);
    });
    ptg.select2({data:full_phototags,
        multiple:true,
        initSelection: photoInitSelection ,})
    fix_phototags()
    ptg.unbind('change').on('change', change_phototag)
}

function change_phototag(e){
    data_changed($(e.target), 'phototag');
    fix_phototags();
}

function data_changed(target, kind){
    var data={'kind':kind};
    if (kind=='phototag'){
        data['phototag_ids']=target.attr('value');
    }
    data['photo_id']=$(".photo-display").attr('photoid')
    send_data(data, target);
}

function send_data(data, target){
    $.ajax({
        url:'/ajax/photo_data/',
        type:'POST',
        data:data,
        success:function(dat){
            $("#notification").find('.alert').slideUp()
            $("#notification").append($('<div class="alert alert-success">'+dat['message']+'</div>'));
            setTimeout(function(){$(".alert").slideUp()}, 1500);
            target.closest('.note-row').attr('note_id',dat['note_id']);
            //if various things are returned, trigger a page redirect
            if (dat['goto_next_photo']){
                document.location.href=dat['next_photo_href']
            }
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