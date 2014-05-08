photoInitSelectionPhoto = function(element, callback) {
    var data = [];
    var ids = element.val().split(",");
    $(ids).each(function() {
        var id=this;
        $(full_phototags).each(function() {
            if (id.localeCompare(""+this.id)==0) data.push(this);
        });
    });
    console.log('setting initial data',data)
    callback(data);
}
    
function setup_phototagselect_photo(){
    var ptg=$('#phototagselect2');
    //$.each(full_phototags, function(index,pt){
        //var phototagselect=$('#phototagselect2');
        //var option=$('<option value="'+index+'">'+pt+'</option>');
        //ptg.append(option);
    //});
    ptg.select2({data:full_phototags,
        multiple:true,
        initSelection: photoInitSelectionPhoto ,})
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