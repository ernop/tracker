function fix_links(){
    var divs=$(".select2-search-choice").find('div');
    $.each(divs, function(index, div){
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/notekind/'+div.innerHTML+'/">'+div.innerHTML+'</a>';
        }
    });
}


function fix_phototags(){
    //make them links to the admin.
    var divs=$(".select2-search-choice").find('div');
    var s2=$(".select2-search-choice").closest('.select2-container')
    var choices=$(".select2-search-choice").closest('.select2-container').select2('data')
    $.each(divs, function(index, div){
	var txt=$(div).text()
	choice_id=null;
	$.each(choices, function(index, choice){
		if (choice.text==txt){
			choice_id=choice.id
			return false
		}
	})
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/photo/phototag_id/'+choice_id+'/">'+div.innerHTML+'</a>';
        }
    });
}
function clear_notifications(){
	$('.fixed-notification .alert').slideUp()
}

function notify(msg, success){
	if (success){
		var klass='success'}
	else{
		var klass='failure';
	}
	var note=$('<div class="alert alert-'+klass+'">'+msg+'</div>');
	var nzone=$(".fixed-notification");
	if (nzone.length){
		nzone.find('.alert').slideUp(function(){this.remove()});
		nzone.append(note);
	}
}
