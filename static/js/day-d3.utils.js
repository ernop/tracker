function gendercolor(d){
	if (d.gender=='1'){return 'lightblue'};
	if (d.gender=='2'){return 'pink'}
	if (d.gender=='3'){return 'steelblue'}
	return 'grey'
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

function fix_nodes(){
  //fucking d3
  var newnodes=[]
  var exi_ids=Object.keys(id2node)
  for (ii=0;ii<Math.max.apply(null, exi_ids)+1;ii++){
	exinode=id2node[ii]
	if (exinode){
	  exinode['x']=500+((exinode.id%20)-10)*10*(Math.pow(-1,(exinode.id/2)%2))
	  exinode['y']=500+((exinode.id%20)-10)*10*(Math.pow(-1,exinode.id%2))
	  exinode['x']=width/2
	  exinode['y']=height/2
	  if (exinode.name=='Existence'){
		exinode['fixed']=true
		exinode['x']=width/2
		exinode['y']=height/2
	  }
	  newnodes.push(exinode)
	}else{
	  newnodes.push({})
	}
  }
  nodes=newnodes
}

function fix_edges(){
  var newedges=[]
  $.each(edges, function(index,edge){
	var newedge={'source':id2node[edge['source']],'target':id2node[edge['target']],'value':edge['value']}
	if (newedge['source'] && newedge['target']){
	newedges.push(newedge)}
  })
  edges=newedges
}
var id2node={};

function setup_dicts(){
  $.each(nodes, function(index,node){
	id2node[node.id]=node
  })
}