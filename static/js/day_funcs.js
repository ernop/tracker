$(document).ready(function(){
    
    setup_new_purch();
});

function setup_new_purch(){
    var pz=$(".purchase-zone");
    $("#product").select2({data:products});
	$("#source").select2({data:sources});
	$("#currency").select2({data:currencies});
	$("#who_with").select2({data:people, multiple: true});
	$("#hour").select2({data:hours});
    pz.after('<div id="save-purchase" class="btn">save</div>');
    $(".make-purchase").click(submit_purchase)
}

var submitting=false;

function get_purchase_data(){
	var dat={};
	dat['product_id']=$("#product").select2('data').id;
	dat['source_id']=$("#source").select2('data').id;
	dat['cost']=$("#cost").val();
	dat['quantity']=$("#quantity").val();
	dat['size']=$("#size").val();
	dat['hour']=$("#hour").select2('data').id;
	var ids=[]
	$.each($("#who_with").select2('data'), function(index, thing){
		ids.push(thing.id);
	});
	dat['who_with']=ids;
	dat['note']=$("#note").val();
	dat['note']=$("#currency").val();
	return dat;
}

function submit_purchase(){
	if (submitting){return}
	submitting=true;
	data=get_purchase_data();
	data['today']=today;
	$.ajax({
		type:'POST',
		url:'/ajax/make_purchase/',
		data:data,
		dataType:"json",
		contentType: "application/json; charset=utf-8",
		success:function(data){    
			display_purch();
		},
		error:function(a,b,c){
		}
	});
	submitting=false;
};

function display_purch(){
    $.ajax({
		type:'POST',
		url:'/ajax/get_purchases/',
		data:{'today':today},
		dataType:"json",
		contentType: "application/json; charset=utf-8",
		success:function(data){    
			var pz=$(".purchase-list");
			pz.find('.purchase').remove();
			$.each(data['purchases'], function(index, thing){
				var row=obj2row(thing);
				pz.append(row);
				$(row).slideDown();
			});
		},
		error:function(a,b,c){
		}
	});
}

function obj2row(purchase){
	return '<div class="purchase">'+purchase.name+' '+purchase.cost+'元</div>';
}