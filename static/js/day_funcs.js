function setup_change_describer(){
	$("#purchase-product").change(show_popular_from_product)
	$("#purchase-source").change(show_popular_from_source)
}

function show_popular_from_product(){
	//for the current selection of the product,
	//show the popular prices, sources, hour etc. for quick selection!
	var thing=$("#purchase-product").select2('data');
	if (!thing){return}
	var data={'product_id':thing.id}
	$.ajax({
		type:'POST',
		url:'/ajax/get_popular/',
		data:data,
		success:function(data){display_popular(data);},
		error:function(a,b,c){}
	});
}


function show_popular_from_source(){
	//for the current selection of the product, show the popular prices,
	//sources, hour etc. for quick selection!
	var thing=$("#purchase-source").select2('data');
	if (!thing){return}
	var data={'source_id':thing.id}
	$.ajax({
		type:'POST',
		url:'/ajax/get_popular/',
		data:data,
		success:function(data){display_popular(data);},
		error:function(a,b,c){}
	});
}

function setup_popular_measurements(){
	var data={'today':today};
	$.ajax({
		type:'POST',
		url:'/ajax/get_common_measurements/',
		data:data,
		success:function(data){display_common_measurements(data);},
		error:function(a,b,c){}
	});
}

function display_popular(data){
	$(".autochooser").remove();
	$.each(data['prices'], function(index,thing){add_thing_to_price_zone(thing)});
	$('.price-autochooser').click(function(e){set_price(e)});

	$.each(data['sources'], function(index,thing){add_thing_to_source_zone(thing)})
	$('.source-autochooser').click(function(e){set_source(e)});

	$.each(data['products'], function(index,thing){add_thing_to_product_zone(thing)})
	$('.product-autochooser').click(function(e){set_product(e)});

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

function add_thing_to_product_zone(thing){
	var sz=$(".product-chooser");
	var txt=$("<div class='product-autochooser autochooser' val_id="+thing[0][1]+" val_name="+thing[0][0]+">"+thing[0][0]+" ("+thing[1]+")</div>");
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


function add_thing_to_price_zone(thing){
	var pz=$(".price-chooser");
	var txt=$("<div style='float:left;' class='autochooser price-autochooser' val="+thing[0]+">"+thing[0]+"</div>")
	pz.append(txt);
}

function set_source(e){
	$("#purchase-source").select2('val', $(e.target).attr('val_id'));
}

function set_product(e){
	$("#purchase-product").select2('val', $(e.target).attr('val_id'));
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

function set_measurement(e){
	var thing=$(e.target);
	notify(thing.attr('val'));
	$("#measurement-spot").select2('val', $(e.target).attr('val_id'));
}

function setup_new_purch(){
    //setup new purch zone. run it again whne you change people, products, sources etc. objects
    //to get select2 to pick them up.
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
	$('#new_person_met_through').select2({data:people, multiple: false}).css("width','50px;");
	$('#new_source_region_chooser').select2({data:regions, multiple: false}).css("width','50px;");
	$('#new_source_region_chooser').select2('val',1)
	$("#purchase-hour").select2({data:hours});
	$(".person-saver").unbind('click').click(function(e){
		var saver=$(this).closest('.person-adder')
		var fn=saver.find('.first-name').val()
		var ln=saver.find('.last-name').val() || '?'

		var gender=saver.find('input[name=gender]:checked').val()
		var met_through=saver.find('#new_person_met_through').select2('val')
		var text=fn+' '+ln
		if (!fn || !fn.length){
			notify('needs at least a first name',false)
			return
		}
		var data={text:text,kind:'person',action:'new',first_name:fn,last_name:ln,
			gender:gender,met_through:met_through}
		get_data(data, wrap_callback_with_original_data(data, new_person_callback))
	})
	$('.person-adder-toggler').unbind('click').click(function(){$('.person-adder').slideToggle()})
	$(".source-saver").unbind('click').click(function(e){
		var saver=$(this).closest('.source-adder')
		var name=saver.find('.name').val()
		var region_id=saver.find('#new_source_region_chooser').select2('val')
		var data={text:name, kind:'source', action:'new', name:name, region_id:region_id,}
		get_data(data, wrap_callback_with_original_data(data, new_source_callback))
	})
	$('.source-adder-toggler').unbind('click').click(function(){$('.source-adder').slideToggle()})
    $(".make-purchase").unbind('click').click(submit_purchase)
}

function wrap_callback_with_original_data(dat, inner_callback){
	var orig_dat=dat
	function x(return_data){
		inner_callback(return_data, orig_dat)
	}

	return x
}

function new_source_callback(dat, orig_dat){
	notify(dat['message'],true)
	if (dat['success']){
		sources.push({text:orig_dat['text'],name:orig_dat['name'],
		id:dat['source_id']})
		setup_new_purch()
	}

}

function new_person_callback(dat, orig_dat){
	notify(dat['message'],true)
	if (dat['success']){
		people.push({text:orig_dat['text'],first_name:orig_dat['first_name'],
		last_name:orig_dat['last_name'],id:dat['person_id']})
		setup_new_purch()
	}

}

function setup_new_measurement(){
    var pz=$(".measurement-zone");
    $("#measurement-spot").select2({data:measurement_spots});
    $(".make-measurement").click(submit_measurement)
}

var submitting=false;

function get_purchase_data(){
	var dat={};
	var prod=$("#purchase-product").select2('data')
	if (!prod){
		notify('product missing.',false);
		return false;
	}
	dat['product_id']=$("#purchase-product").select2('data').id;
	var source=$("#purchase-source").select2('data');
	if (!(source)){
		notify('source missing.',false);
		return false;
	}
	dat['source_id']=source.id;
	dat['cost']=$("#purchase-cost").val();
	if (!(dat['cost'])){
		notify('cost missing.',false);
		return false;
	}
	dat['quantity']=$("#purchase-quantity").val();
	dat['size']=$("#purchase-size").val();
	dat['hour']=$("#purchase-hour").select2('data').id;
	if (!(dat['hour'])){
		notify('hour missing.',false);
		return false;
	}
	if (!dat['source_id']||!dat['cost']||!dat['hour']){
		notify('data missing.'+dat,false);
		return false;
	}
	var ids=[]
	$.each($("#purchase-who_with").select2('data'), function(index, thing){
		ids.push(thing.id);
	});
	dat['who_with']=ids;
	dat['note']=$("#purchase-note").val();
	dat['currency']=$("#purchase-currency").val();
	return dat;
}

function get_measurement_data(){
	var dat={};
	dat['spot_id']=$("#measurement-spot").select2('data').id;
	dat['amount']=$("#measurement-amount").val();
	return dat;
}

function submit_purchase(){
	if (submitting){return}
	submitting=true;
	data=get_purchase_data();
	if (data){
		data['today']=today;
		notify('saving',true)
		$.ajax({
			type:'POST',
			url:'/ajax/make_purchase/',
			data:data,
			//dataType:"json",
			//contentType: "application/json; charset=utf-8",
			success:function(data){
				$('.loading').slideUp();
				clear_notifications()
				display_purch();
			},
			error:function(a,b,c){
				$('.loading').text('error'+a+b+c)
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
	$('.measurement-loading-zone').append('<span style="float:left;" class="alert alert-error loading">saving</span>')
	$.ajax({
		type:'POST',
		url:'/ajax/make_measurement/',
		data:data,
		//dataType:"json",
		//contentType: "application/json; charset=utf-8",
		success:function(data){
			$('.measurement-loading-zone').find($('.loading')).slideUp();
			//$('.make-measurement').parent().
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
	return '<tr class="purchase"><td>'+pur_alink(purchase)+'<td>'+prod_clink(purchase)+'<td class="nb">'+purchase.cost+purchase.cur_symbol+'<td>'+count+'<td>'+source_clink(purchase)+'<td>'+purchase.hour+'<td>'+who_with_clinks(purchase)+'</tr>';
}

function source_clink(purchase){
	return '<a href="/admin/day/source/?id='+purchase.source.id+'">'+purchase.source.name+'</a>'
}

function who_with_clink(guy){
	return '<a href="/admin/day/person/?id='+guy.id+'">'+guy.text+'</a>'
}

function who_with_clinks(purchase){
	var res=''
	$.each(purchase.who_with, function(index,guy){
		res+='<td class="nb">'+who_with_clink(guy);
	})
	return res
}

function obj2measurement(measurement){
	return '<tr class="measurement"><td>'+m_clink(measurement)+'<td>'+m_p_alink(measurement)+'<td>'+measurement_all_spot(measurement)+'<td>'+measurement_domain_clink(measurement)+'<td>'+ measurement.amount+'</tr>';
}

function measurement_domain_clink(m){
	return '<a href="/admin/day/domain/?id='+m.domain_id+'">'+m.domain_name+'</a>'
}

function m_clink(m){
	return '<a href="/admin/day/measurement/?id='+m.id+'">'+m.id+'</a>'
}

function m_p_alink(m){
	return '<a href="/admin/day/measuringspot/?id='+m.spot_id+'">'+m.name+'</a>'
}

function measurement_all_spot(m){
	return '<a href="/admin/day/measurement/?spot__id='+m.spot_id+'">'+'all spot</a>'
}

function pur_alink(purch){//the direct purchase
	return '<a href="/admin/day/purchase/'+purch.id+'/">'+purch.id+'</a>'
}

function prod_alink(purch){//the product - useless
	return '<a href="/admin/day/product/'+purch.product_id+'/">'+purch.name+'</a>'
}

function pur_clink(purch){
	return '<a href="/admin/day/purchase/?id='+purch.id+'">'+purch.name+'</a>'
}

function prod_purchases_clink(purch){
	return '<a href="/admin/day/purchase/?product__id='+purch.product_id+'">'+purch.name+'</a>'
}

function prod_clink(purch){
	return '<a href="/admin/day/product/?id='+purch.product_id+'">'+purch.name+'</a>'
}
