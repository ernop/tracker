function formatter(el,options,object){
    var res=el.$el.attr('labels').split(',')[object.offset];
    return res;
}

var piestuff={'type':'pie','tooltipFormatter':formatter,'height':300};
var sparkstuff={'height':140}

$(document).ready(function(){
    $(".piespark").sparkline('html',piestuff);
    $(".sparkline-data").sparkline('html',sparkstuff)

});