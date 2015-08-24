function formatter(el,options,object){
    var res=el.$el.attr('labels').split(',')[object.offset];
    return res;
}
labels=[];
var piestuff={'type':'pie','tooltipFormatter':formatter,'height':300};
var sparkstuff={'height':160,'tooltipFormatter':sparkFormatter,'width':400}
var simplesparkstuff={'height':160,'width':400}

function sparkFormatter(el, options, object){
    //debugger;
    var sparkid=$(el.el).attr('sparkid')
    var label=labels[sparkid][object.x]
    return label
    //check my "sparkid" and then use the var
    //spark_labels_<sparkid> to look up labels.
}

$(document).ready(function(){
    $(".piespark").sparkline('html',piestuff);
    $(".simple-sparkline-data").sparkline('html',simplesparkstuff)
    $(".sparkline-data").sparkline('html',sparkstuff)

});
