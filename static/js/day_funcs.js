function setup_change_describer(){
	$("#purchase-product").change(show_popular)
}

function show_popular(){
	//for the current selection of the product, show the popular prices, sources, hour etc. for quick selection!
	var thing=$("#purchase-product").select2('data');
	if (!thing){
		return
	}

	var data={'product_id':thing.id}
	$.ajax({
		type:'POST',
		url:'/ajax/get_popular/',
		data:data,
		dataType:"json",
		contentType: "application/json; charset=utf-8",
		success:function(data){
			display_popular(data);
		},
			error:function(a,b,c){
		}
	});
}

function display_popular(data){
	$(".autochooser").remove();
	$.each(data['prices'], function(index,thing){add_thing_to_price_zone(thing)});
	$('.price-autochooser').click(function(e){set_price(e)});

	$.each(data['sources'], function(index,thing){add_thing_to_source_zone(thing)})
	$('.source-autochooser').click(function(e){set_source(e)});

	$.each(data['who_with'], function(index,thing){add_thing_to_who_zone(thing)})
	$('.who_with-autochooser').click(function(e){set_who_with(e)});

	$.each(data['hours'], function(index,thing){add_thing_to_hour_zone(thing)})
	$('.hour-autochooser').click(function(e){set_hour(e)});
}

function add_thing_to_source_zone(thing){
	var sz=$(".source-chooser");
	var txt=$("<div class='source-autochooser autochooser' val_id="+thing[0][1]+" val_name="+thing[0][0]+">"+thing[0][0]+" ("+thing[1]+")</div>");
	sz.append(txt);
}

function add_thing_to_who_zone(thing){
	var wc=$(".who_with-chooser");
	var txt=$("<div class='who_with-autochooser autochooser' val_id="+thing[0][1]+" val_name="+thing[0][0]+">"+thing[0][0]+" ("+thing[1]+")</div>");
	wc.append(txt);
}

function add_thing_to_hour_zone(thing){
	var wc=$(".hour-chooser");
	var txt=$("<div class='hour-autochooser autochooser' val_id="+thing[0][1]+" val_name="+thing[0][0]+">"+thing[0][0]+" ("+thing[1]+")</div>");
	wc.append(txt);
}

function set_source(e){
	$("#purchase-source").select2('val', $(e.target).attr('val_id'));
}

function set_hour(e){
	$("#purchase-hour").select2('val', $(e.target).attr('val_id'));
}

function set_who_with(e){
	var list=$("#purchase-who_with").select2('val')
	list.push($(e.target).attr('val_id'))
	$("#purchase-who_with").select2('val', list);
}

function set_price(e){
	var thing=$(e.target);
	$("#purchase-cost").val(thing.attr('val'))
}

function add_thing_to_price_zone(thing){
	var pz=$(".price-chooser");
	var txt=$("<div style='float:left;' class='autochooser price-autochooser' val="+thing[0]+">"+thing[0]+"</div>")
	pz.append(txt);
}

function setup_new_purch(){
    var pz=$(".purchase-zone");
    $("#purchase-product").select2({data:products});
	$("#purchase-source").select2({data:sources,initSelection: function (item, callback) {
		//this is fucking retarded.  despite select2 having already read the whole sources list
		//when you do .val(n) you have to explicitly tell it how to find that item again.
			var to_be_selected=null;
			$.each(sources,function(index,thing){
				if (thing.id==item.val()){
					to_be_selected=thing;
					return
				}
			})
            callback(to_be_selected);
        },});
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
				pz.prepend(row);
				$(row).show();
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
	return '<tr class="purchase"><td>'+pur_alink(purchase)+'<td>'+prod_clink(purchase)+'<td class="nb">'+purchase.cost+'元<td>'+count+'<td>'+source_clink(purchase)+'<td>'+purchase.hour+'<td>'+who_with_clinks(purchase)+'</tr>';
}

function source_clink(purchase){
	return '<a href="/admin/buy/source/?id='+purchase.source.id+'">'+purchase.source.name+'</a>'
}

function who_with_clink(guy){
	return '<a href="/admin/buy/person/?id='+guy.id+'">'+guy.text+'</a>'
}

function who_with_clinks(purchase){
	var res=''
	$.each(purchase.who_with, function(index,guy){
		res+='<td class="nb">'+who_with_clink(guy);
	})
	return res
}

function obj2measurement(measurement){
	return '<div class="measurement">'+m_clink(measurement)+' '+m_p_alink(measurement)+' '+ measurement.amount+'</div>';
}

function m_clink(m){
	return '<a href="/admin/workout/measurement/?place__id='+m.place_id+'">'+m.name+'</a>'
}

function m_p_alink(m){
	return '<a href="/admin/workout/measuringspot/?id='+m.place_id+'">summary '+m.name+'</a>'
}

function pur_alink(purch){//the direct purchase
	return '<a href="/admin/buy/purchase/'+purch.id+'/">'+purch.id+'</a>'
}

function prod_alink(purch){//the product - useless
	return '<a href="/admin/buy/product/'+purch.product_id+'/">'+purch.name+'</a>'
}

function pur_clink(purch){
	return '<a href="/admin/buy/purchase/?id='+purch.id+'">'+purch.name+'</a>'
}

function prod_purchases_clink(purch){
	return '<a href="/admin/buy/purchase/?product__id='+purch.product_id+'">'+purch.name+'</a>'
}

function prod_clink(purch){
	return '<a href="/admin/buy/product/?id='+purch.product_id+'">'+purch.name+'</a>'
}