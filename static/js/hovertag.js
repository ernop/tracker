//every .hovertagable has two fields.  is and has.  hovering over an is "a" triggers all "has a".  hovering over "has a,b,c" triggers "is" a, is b, is c.
hover_iss={} //definitions of tags (used when hovering over a photo)
hover_hass={} //everyone who has that tag. 2 => []
$(document).ready(function(){
    
    $.each($('.hovertagable'), function(index,domguy){
        domguy=$(domguy)
        var iss=domguy.attr('iss')&& domguy.attr('iss').split(',')
        if (iss && iss.length>0){
            $.each(iss, function(iss_index,thisiss){
                if (!hover_iss.hasOwnProperty(thisiss)){hover_iss[thisiss]=[]}
                hover_iss[thisiss].push(domguy)
            })
        }
        var hass=domguy.attr('hass') && domguy.attr('hass').split(',')
        if (hass && hass.length>0){
            $.each(hass, function(hass_index,thishass){
                if (!hover_hass.hasOwnProperty(thishass)){hover_hass[thishass]=[]}
                hover_hass[thishass].push(domguy)
            })
        }
        
    })
    
    setup_hovers()
})

function setup_hovers(){
    $.each($('.hovertagable'), function(index,ht){
        var iss=$(this).attr('iss') && $(this).attr('iss').split(',')
        
        $(ht).mouseover(function(e){
            clear();
            if (iss && iss.length){
                $.each(iss, function(index, thisiss){
                    $.each(hover_hass[iss], function(index,guy){
                        $(guy).addClass('hovered')
                    })
                })
            }
        })
        $(ht).mouseout(function(e){clear()})
    
    
        var hass=$(this).attr('hass') && $(this).attr('hass').split(',')
        
        if (hass && hass.length){
            $(ht).unbind('mouseover')
            $(ht).mouseover(function(){
                $.each(hass, function(index, thishass){
                    var definitions=hover_iss[thishass]
                    if (definitions && definitions.length){
                        $.each(definitions, function(index,guy){
                            $(guy).addClass('hovered')
                        })
                    }
                })
            })
        }
    })
}

function clear(){
    $(".hovertagable").removeClass('hovered')
    
}