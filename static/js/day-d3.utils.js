function gendercolor(d){
	if (d.gender=='1'){return 'lightblue'};
	if (d.gender=='2'){return 'pink'}
	if (d.gender=='3'){return 'steelblue'}
	return 'grey'
}

function push_out(height, width, oldx,oldy, mult){
  var x=oldx-width/2;
  var y=oldy-height/2;
  return [x*mult+width/2,y*mult+height/2]
}

function filter(objs, func){
  var res=[]
  $.each(objs, function(index,obj){
	if (func(obj)){
	  res.push(obj)
	}
  })
  return res
}

function male(obj){return obj.gender==1}
function female(obj){return obj.gender==2}

function edge_either(func, edges){
  var res=[]
  $.each(edges, function(index,edge){
	if (func(edge.target) && func(edge.source))  {
	  res.push(edge);
	}
  })
  return res
}

function fix_nodes(filter){
  //fucking d3
  var newnodes=[];
  var use_ids=[];
  var exi_ids=Object.keys(id2node);
  for (ii=0;ii<Math.max.apply(null, exi_ids)+1;ii++){
	exinode=id2node[ii]

	if (exinode && filter(exinode)){
	  exinode['x']=ii
	  exinode['y']=ii
	  if (exinode.name=='Existence'){
		exinode['fixed']=true
		exinode['x']=width/2
		exinode['y']=height/2
	  }
	  newnodes.push(exinode)
	  use_ids.push(ii)
	}else{
	  newnodes.push({})

	}
  }
  nodes=newnodes
  return use_ids;
}

function inlist(list, val){
  if (list.indexOf(val)!=-1){return true}
  return false;
}

function fix_edges(node_ids){
  var newedges=[]
  $.each(edges, function(index,edge){
	if (inlist(node_ids,edge['source']) && inlist(node_ids, edge['target'])){
	  var newedge={'source':id2node[edge['source']],'target':id2node[edge['target']],'value':edge['value']}
	  if (newedge['source'] && newedge['target']){
	  newedges.push(newedge)}}
	})
  return newedges
}

var id2node={};

function setup_dicts(){
  $.each(nodes, function(index,node){
	id2node[node.id]=node
  })
}