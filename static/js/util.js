function fix_links(){
    var divs=$(".select2-search-choice").find('div');
    $.each(divs, function(index, div){
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/notekind/'+div.innerHTML+'/">'+div.innerHTML+'</a>';
        }
    });
}


function fix_phototags(){
    var divs=$(".select2-search-choice").find('div');
    $.each(divs, function(index, div){
        if ($(div).find('a').length){}else{
            div.innerHTML='<a href="/photo/phototag/'+div.innerHTML+'/">'+div.innerHTML+'</a>';
        }
    });
}


function notify(msg, success){
	if (success){
		var klass='success'}
	else{
		var klass='failure';
	}
	var note=$('<div class="alert alert-'+klass+'">'+msg+'</div>');
	var nzone=$(".fixed-notification");
	
	if (!nzone.length){var nzone=$('.notification-zone')}
	if (nzone.length){
		nzone.find('.alert').slideUp(function(){this.remove()});
		nzone.append(note);
	}
}
