$(document).ready(function(){
    
    setup_new_purch();
	display_purch();
});


//function initHour(element, callback) {
	//debugger;
    //var data = [element.val()];
	
    ////var ids = element.val().split(",");
    ////$(ids).each(function() {
        ////var id=this;
        ////$(full_notekinds).each(function() {
            ////if (id.localeCompare(""+this.id)==0) data.push(this);
        ////});
    ////});
    //callback(data);                   
//}

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
	console.log(purchase)
	if (purchase.quantity!=1){
		var count=' ('+purchase.quantity+')';
	}else{
		var count=''
	}
	return '<div class="purchase">'+pur_alink(purchase)+' - '+prod_purchases_clink(purchase)+' '+purchase.cost+'元'+count+'</div>';
	//return '<div class="purchase">'+purchase.name+' '+purchase.cost+'元</div>';
}

function pur_alink(purch){//the direct purchase
	return '<a href="/admin/buy/purchase/'+purch.id+'/">edit</a>'
}

function prod_alink(purch){//the product - useless
	return '<a href="/admin/buy/product/'+purch.product_id+'/">'+purch.name+'</a>'
}

function pur_clink(purch){
	return '<a href="/admin/buy/purchase/?id='+purch.id+'">this '+purch.name+'</a>'
}

function prod_purchases_clink(purch){
	return '<a href="/admin/buy/purchase/?product__id='+purch.product_id+'">all '+purch.name+'</a>'
}