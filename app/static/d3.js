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

// 4. Call the y axis in a group tag
svg.append("g")
    .attr("class", "y axis")
    .attr("class", "axisColor")
    .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

// 9. Append the path, bind the data, and call the line generator 
svg.append("path")
    .datum(dataset) // 10. Binds data to the line 
    .attr("class", "line") // Assign a class for styling 
    .attr("d", line); // 11. Calls the line generator 
/*
// 12. Appends a circle for each datapoint 
//svg.selectAll(".dot")
//    .data(dataset)
 // .enter().append("circle") // Uses the enter().append() method
 //   .attr("class", "dot") // Assign a class for styling
 //   .attr("cx", function(d, i) { return xScale(i) })
 //   .attr("cy", function(d) { return yScale(d.y) })
 //   .attr("r", 5)
 //     .on("mouseover", function(a, b, c) { 
 // 			console.log(a) 
 //      this.attr('class', 'focus')
//		})
//      .on("mouseout", function() {  })
//       .on("mousemove", mousemove);

//   var focus = svg.append("g")
//       .attr("class", "focus")
//       .style("display", "none");

//   focus.append("circle")
//       .attr("r", 4.5);

//   focus.append("text")
//       .attr("x", 9)
//       .attr("dy", ".35em");

//   svg.append("rect")
//       .attr("class", "overlay")
//       .attr("width", width)
//       .attr("height", height)
//       .on("mouseover", function() { focus.style("display", null); })
//       .on("mouseout", function() { focus.style("display", "none"); })
//       .on("mousemove", mousemove);
  
//   function mousemove() {
//     var x0 = x.invert(d3.mouse(this)[0]),
//         i = bisectDate(data, x0, 1),
//         d0 = data[i - 1],
//         d1 = data[i],
//         d = x0 - d0.date > d1.date - x0 ? d1 : d0;
//     focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
//     focus.select("text").text(d);
//   }
*/