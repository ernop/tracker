var force, svg, link, gnodes
var width = 2200;
var height = 1300;
$(document).ready(function(){
  width=$('body').width()-130;
  $("#control-area").height(window.innerHeight)-40
  height=window.innerHeight-10
  nodes=all_nodes;
  edges=all_edges;
  filter_edges()
  setup_dicts();
  fix_nodes();
  fix_edges();
  draw()
  })

function filter_edges(){
  var new_edges=[];
  edges.forEach(function (e){
	if (Math.random()>0.5){
	  new_edges.push(e)
	}
  })
  edges=new_edges
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

function charge_func(d){ return -200}

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

