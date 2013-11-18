var force, svg, link, gnodes
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

function distance_function(d){
  return 25;
  var res=20;
  if (d.target.gender==3 && d.source.gender==3){res=40};
  if (d.target.gender==d.source.gender){return 30};

  return res+(2*(radius(d.target)+radius(d.source)))
}

function radius(d){
  var res=Math.sqrt(d.purchases_together)+4;
  if (isNaN(res)){return 0;}
  return res}

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

function charge_func(d){
  return -200
  var res=-200+(radius(d)*radius(d))
  console.log(d,res)
  return res
}

function tick() {
	link.attr("x1", function(d) { return d.source.x; }).attr("y1", function(d) { return d.source.y; }).attr("x2", function(d) { return d.target.x; }).attr("y2", function(d) { return d.target.y; });
	gnodes.attr("transform", function(d) {
	  //if (d.id==1){return 'translate(300,100)'}
	  //if (d.name=='Existence'){
		//return 'translate(' + [width/2, height/2] + ')';
	  //}
	  return 'translate(' + [d.x, d.y] + ')';
	})
  }

width = 2200;
  height = 1300;
function draw(){

  svg = d3.select("#people-graph").append("svg").attr("width", width).attr("height", height);
  svg.append("svg:defs").selectAll("marker").data(["start"]).enter().append("svg:marker").attr("id", String).attr("viewBox", "0 -5 10 10")
  .attr("refX", 20).attr("refY", -1.5).attr("markerWidth", -8).attr("markerHeight", 6).attr("orient", "auto").append("svg:path").attr("d", "M0,-5L10,0L0,5");
  //edge_either(male, edges)
  force = d3.layout.force().charge(charge_func).linkDistance(distance_function).linkStrength(.5).friction(0.95).gravity(0.11).size([width, height]).nodes(nodes).links(edges).start().on("tick", tick)

  link = svg.selectAll(".link").data(force.links()).enter().append("line").attr('class','link').attr("marker-start", "url(#start)");

  gnodes = svg.selectAll('g.gnode').data(nodes).enter().append('g').classed('gnode', true);
  var node = gnodes.append("circle").attr("class", 'person-graph').attr("r", radius).style("fill", gendercolor).call(force.drag)
  var labels = gnodes.append("text").text(function(d) {return d.name;})
	.attr('class', 'd3-person-label').attr('transform', function(d){
	  //if (d.id==1){
	  //return 'translate(300,300)'}
	  //console.log(d)}
	  return 'translate('+[11,0]+')'
	})

};

function fix_nodes(){
  //fucking d3
  var newnodes=[]
  var exi_ids=[]
	$.each(nodes, function(index, node){
		exi_ids.push(node.id)
	})
  for (ii=0;ii<Math.max.apply(null, exi_ids)+1;ii++){
	exinode=id2node[ii]
	if (exinode){
	  exinode['x']=500+((exinode.id%20)-10)*20*(Math.pow(-1,(exinode.id/2)%2))
	  exinode['y']=500+((exinode.id%20)-10)*20*(Math.pow(-1,exinode.id%2))
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

$(document).ready(function(){
  setup_dicts();
  fix_nodes();
  fix_edges();
  draw()
  })