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
