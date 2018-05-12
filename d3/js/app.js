// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);

// When the browser loads, makeResponsive() is called.
makeResponsive();

// The code for the chart is wrapped inside a function that
// automatically resizes the chart
function makeResponsive() {

  // if the SVG area isn't empty when the browser loads,
  // remove it and replace it with a resized version of the chart
  var svgArea = d3.select("body").select("svg");

  // clear svg is not empty
  if (!svgArea.empty()) {
    svgArea.remove();
  }

  // SVG wrapper dimensions are determined by the current width and
  // height of the browser window.
  var svgWidth = window.innerWidth;
  var svgHeight = window.innerHeight;

  margin = {
    top: 50,
    bottom: 50,
    right: 50,
    left: 50
  };

  var height = svgHeight - margin.top - margin.bottom;
  var width = svgWidth - margin.left - margin.right;

  // Append SVG element
  var svg = d3
    .select(".chart")
    .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWidth);

  // Append group element
  var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Read CSV
  d3.csv("resources/data.csv", function (error, Data) {

    if (error) console.log(error);

    // parse data from string to float
    Data.forEach(function (data) {
      data.stroke_percent = +data.stroke_percent;
      data.heart_attack_percent = +data.heart_attack_percent;
      data.angina_percent = +data.angina_percent;
      data.low_income_percent = +data.low_income_percent;
      data.over_60_disability_percent = +data.over_60_disability_percent;
    });

    // create scales
    var xLinearScale = d3.scaleLinear()
      .domain(d3.extent(Data, d => d.over_60_disability_percent))
      .range([0, width]);

    var yLinearScale = d3.scaleLinear()
      .domain([0, d3.max(Data, d => d.stroke_percent)])
      .range([height, 0]);

    // create axes
    var xAxis = d3.axisBottom(xLinearScale);

    var yAxis = d3.axisLeft(yLinearScale);

    // append axes
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(xAxis);

    chartGroup.append("g")
      .call(yAxis);

    // append circles for scatter plot
    var circlesGroup = chartGroup.selectAll("circle")
      .data(Data)
      .enter()
      .append("circle")
      .attr("cx", d => xLinearScale(d.over_60_disability_percent))
      .attr("cy", d => yLinearScale(d.stroke_percent))
      .attr("r", "10")
      .attr("fill", "LightBlue")
      .attr("stroke-width", "1")
      .attr("stroke", "Gold")

      // append circles' text for scatter plot
    var textGroup = chartGroup.selectAll()
      .data(Data)
      .enter()
      .append('text')
      .attr('font-size','9px')
      .attr('fill','White')
      .attr("x", d => xLinearScale(d.over_60_disability_percent)-5)
      .attr("y", d => yLinearScale(d.stroke_percent)+5)
      .text( d =>  d.State)

    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([5,5])
      .html(function(d){
        return (`<strong>${d.State}<strong><hr>Stroke: ${d.stroke_percent}%<hr>Over 60 w/disability: ${d.over_60_disability_percent}%`)
      })


    // add the tooltip in chartGroup.
    chartGroup.call(toolTip)

    //Create "mouseover" event listener to display tooltip and "mouseout" event listener to hide tooltip
    circlesGroup.on("mouseover", function(d){
        toolTip.show(d)
    })
    .on("mouseout", function(d){
        toolTip.hide(d)
      });

   //add axis labelsto chartGroup
    var x_axis_label = "Over 60 w/Disabilities percent";
    var y_axis_label = "stroke percent";

    chartGroup.append("text")
      .attr("class", "xlabel")
      .attr("x", width/2 - x_axis_label.length)
      .attr("y", height + 50)
      .text(x_axis_label);

    chartGroup.append("text")
      .attr("class", "ylabel")
      .attr("x", -height/2)
      .attr("y", -25)
      .text(y_axis_label);

    chartGroup.selectAll(".ylabel")
       .attr("transform", "rotate(-90)");

  });
};
