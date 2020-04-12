var svg = dimple.newSvg(".dimpleline", 1400, 700);


var myChart = new dimple.chart(svg, dataset);
console.log(dataset);
//myChart.setBounds(60, 30, 505, 305);
var x = myChart.addAxis("x", "time", "time");

var y = myChart.addMeasureAxis("y", "depth");


myChart.addSeries(null, dimple.plot.line);
//myChart.addSeries(null, dimple.plot.scatter);
myChart.draw();