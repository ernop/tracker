$(document).ready(function(){
    
    setup_new_purch();
	display_purch();
	setup_new_measurement();
	display_measurement();
});

function setup_new_purch(){
    var pz=$(".purchase-zone");
    $("#purchase-product").select2({data:products});
	$("#purchase-source").select2({data:sources});
	$("#purchase-currency").select2({data:currencies});
	$("#purchase-who_with").select2({data:people, multiple: true});
	$("#purchase-hour").select2({data:hours});
    $(".make-purchase").click(submit_purchase)
}

function setup_new_measurement(){
    var pz=$(".measurement-zone");
    $("#measurement-place").select2({data:measurement_places});
    $(".make-measurement").click(submit_measurement)
}

var submitting=false;

function get_purchase_data(){
	var dat={};
	
	dat['product_id']=$("#purchase-product").select2('data').id;
	var dd=$("#purchase-source").select2('data');
	if (dd){
		dat['source_id']=dd.id;
	}
	else{
	notify('no source.',false);
	return false;
	}
	dat['cost']=$("#purchase-cost").val();
	dat['quantity']=$("#purchase-quantity").val();
	dat['size']=$("#purchase-size").val();
	dat['hour']=$("#purchase-hour").select2('data').id;
	var ids=[]
	$.each($("#purchase-who_with").select2('data'), function(index, thing){
		ids.push(thing.id);
	});
	dat['who_with']=ids;
	dat['note']=$("#purchase-note").val();
	dat['currency']=$("#purchase-currency").val();
	return dat;
}

function notify(msg, success){
	if (success){
		var klass='success'}
	else{
		var klass='failure';
	}
	var note=$('<div class="alert alert-'+klass+'">'+msg+'</div>');
	var nzone=$(".fixed-notification notification");
	if (nzone.length){
		nzone.find('.alert').slideUp();
		nzone.append(note);
	}
}

function get_measurement_data(){
	var dat={};
	dat['place_id']=$("#measurement-place").select2('data').id;
	dat['amount']=$("#measurement-amount").val();
	return dat;
}

function submit_purchase(){
	if (submitting){return}
	submitting=true;
	data=get_purchase_data();
	if (data){
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
	}else{
	1
	}
	submitting=false;
};

function submit_measurement(){
	if (submitting){return}
	submitting=true;
	data=get_measurement_data();
	data['today']=today;
	$.ajax({
		type:'POST',
		url:'/ajax/make_measurement/',
		data:data,
		dataType:"json",
		contentType: "application/json; charset=utf-8",
		success:function(data){    
			display_measurement();
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
				var row=obj2purchase(thing);
				pz.append(row);
				$(row).slideDown();
			});
		},
		error:function(a,b,c){
		}
	});
}

function display_measurement(){
    $.ajax({
		type:'POST',
		url:'/ajax/get_measurements/',
		data:{'today':today},
		dataType:"json",
		contentType: "application/json; charset=utf-8",
		success:function(data){    
			var pz=$(".measurement-list");
			pz.find('.measurement').remove();
			$.each(data['measurements'], function(index, thing){
				var row=obj2measurement(thing);
				pz.append(row);
				$(row).slideDown();
			});
		},
		error:function(a,b,c){
		}
	});
}

function obj2purchase(purchase){
	if (purchase.quantity!=1){
		var count=' ('+purchase.quantity+')';
	}else{
		var count=''
	}
	return '<div class="purchase">'+pur_alink(purchase)+' - '+prod_purchases_clink(purchase)+' '+purchase.cost+'元'+count+'</div>';
}

function obj2measurement(measurement){
	return '<div class="measurement">'+m_clink(measurement)+' '+m_p_alink(measurement)+' '+ measurement.amount+'</div>';
}

function m_clink(m){
	return '<a href="/admin/workout/measurement/?place__id='+m.place_id+'">all '+m.name+'</a>'
}

function m_p_alink(m){
	return '<a href="/admin/workout/measuringspot/?id='+m.place_id+'">summary '+m.name+'</a>'
}

function pur_alink(purch){//the direct purchase
	return '<a href="/admin/buy/purchase/'+purch.id+'/">edit</a>'
}

function prod_alink(purch){//the product - useless
	return '<a href="/admin/buy/product/'+purch.product_id+'/">'+purch.name+'</a>'
}

function pur_clink(purch){
	return '<a href="/admin/buy/purchase/?id='+purch.id+'">'+purch.name+'</a>'
}

function prod_purchases_clink(purch){
	return '<a href="/admin/buy/purchase/?product__id='+purch.product_id+'">all '+purch.name+'</a>'
}