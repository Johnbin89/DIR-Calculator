/*
var dataset = [
    {
        depth: 45,
        time: 0
    },
    {
      depth: 45,
      time: 20
    },
    {
      depth: 24,
      time: 25
    },
    {
      depth: 21,
      time: 27
    },
    {
        depth: 18,
      time: 30
    },
    { 
        depth: 15,
      time: 40
    },
    {
        depth: 6,
      time: 50
    }
  ];
*/
console.log(dataset)
//  Use the margin convention practice 
var margin = {top: 50, right: 50, bottom: 80, left: 80}
  , width = 1478 - margin.left - margin.right 
  , height = 770 - margin.top - margin.bottom; 

// 5. X scale will use the index of our data
var xScale = d3.scaleLinear()
    .domain(d3.extent(dataset, dataPoint => dataPoint.time)) // input
    .range([0, width]); // output

// 6. Y scale will use the randomly generate number 
var yScale = d3.scaleLinear()
    .domain([d3.max(dataset, dataPoint => dataPoint.depth) + 5, 0]) // input 
    .range([height, 0]); // output 

// 7. d3's line generator
var line = d3.line()
    .x(function(d) { return xScale(d.time); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.depth); }) // set the y values for the line generator 
   // .curve(d3.curveMonotoneX) // apply smoothing to the line


// 1. Add the SVG to the page and employ #2
var svg = d3.select(".d3line").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    //.attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 1478 770")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// 3. Call the x axis in a group tag
svg.append("g")
    .attr("class", "x axis")
    .attr("class", "axisColor")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom


    svg.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
    .style("text-anchor", "middle")
    .style("fill", "olive")
    .text("Runtime (min)");

// 4. Call the y axis in a group tag
svg.append("g")
    .attr("class", "y axis")
    .attr("class", "axisColor")
    .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft


    // Add the text label for the Y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "start")
        .style("fill", "olive")
        .text("Depth (meters)");


// 9. Append the path, bind the data, and call the line generator 
svg.append("path")
    .datum(dataset) // 10. Binds data to the line 
    .attr("class", "line") // Assign a class for styling 
    .attr("d", line); // 11. Calls the line generator 

// 12. Appends a circle for each datapoint 
svg.selectAll(".dot")
    .data(dataset)
  .enter().append("circle") // Uses the enter().append() method
    .attr("class", "dot") // Assign a class for styling
    .attr("cx", function(d) { return xScale(d.time) })
    .attr("cy", function(d) { return yScale(d.depth) })
    .attr("r", 5);
/* 
      .on("mouseover", function() { 
  			//console.log(a) 
       this.attr('class', 'focus')
		})
      .on("mouseout", function() {  })
       .on("mousemove", mousemove);

  var focus = svg.append("g")
       .attr("class", "focus")
       .style("display", "none");

   focus.append("circle")
       .attr("r", 4.5);

  focus.append("text")
       .attr("x", 9)
       .attr("dy", ".35em");

   svg.append("rect")
       .attr("class", "overlay")
       .attr("width", width)
       .attr("height", height)
       .on("mouseover", function() { focus.style("display", null); })
       .on("mouseout", function() { focus.style("display", "none"); })
       .on("mousemove", mousemove);
  
   function mousemove() {
     var x0 = xScale.invert(d3.mouse(this)[0]),
         i = bisectDate(data, x0, 1),
         d0 = dataset[i - 1],
         d1 = dataset[i],
         d = x0 - d0.date > d1.date - x0 ? d1 : d0;
     focus.attr("transform", "translate(" + x(d.time) + "," + y(d.depth) + ")");
     focus.select("text").text(d);
   }
*/
 // This allows to find the closest X index of the mouse:
 var bisect = d3.bisector(function(d) { return d.time; }).left;

 // Create the circle that travels along the curve of chart
 var focus = svg
   .append('g')
   .append('circle')
     .style("fill", "none")
     .attr("stroke", "black")
     .attr('r', 7)
     .style("opacity", 0)

 // Create the text that travels along the curve of chart
 var focusText = svg
   .append('g')
   .append('text')
     .style("opacity", 0)
     .style('fill', 'olive')
     .attr("text-anchor", "start")
     .attr("alignment-baseline", "top")

 // Create a rect on top of the svg area: this rectangle recovers mouse position
 svg
   .append('rect')
   .style("fill", "none")
   .style("pointer-events", "all")
   .attr('width', width)
   .attr('height', height)
   .on('mouseover', mouseover)
   .on('mousemove', mousemove)
   .on('mouseout', mouseout);

// What happens when the mouse move -> show the annotations at the right positions.
function mouseover() {
  focus.style("opacity", 1)
  focusText.style("opacity",1)
}

function mousemove() {
  // recover coordinate we need
  var x0 = xScale.invert(d3.mouse(this)[0]);
  var i = bisect(dataset, x0, 1);
  selectedData = dataset[i]
  focus
    .attr("cx", xScale(selectedData.time))
    .attr("cy", yScale(selectedData.depth))
  focusText
    .html(selectedData.depth + " m" + " - "  +  selectedData.time + "min(RT)")
    .attr("x", xScale(selectedData.time)-80)
    .attr("y", yScale(selectedData.depth)-20)
  }
function mouseout() {
  focus.style("opacity", 0)
  focusText.style("opacity", 0)
}