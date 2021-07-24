function makeResponsive() {
  // if the SVG area isn't empty when the browser loads,
  // remove it and replace it with a resized version of the chart
  var svgArea = d3.select("body").select("svg");

  // clear svg is not empty
  if (!svgArea.empty()) {
    svgArea.remove();
  }
  var svgWidth = window.innerWidth;
  var svgHeight = window.innerHeight;

  // Chart Params
  var margin = {
    top: 50,
    right: 50,
    bottom: 50,
    left: 50,
  };

  //Define chart area
  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;

  // append the svg object to the body of the page
  // Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
  var svg = d3
    .select("#my_dataviz")
    .append("svg")
    //   .attr("width", width + margin.left + margin.right)
    .attr("width", svgWidth)
    //   .attr("height", height + margin.top + margin.bottom)
    .attr("height", svgHeight);

  var chartGroup = svg
    .append("g")
    // .attr("transform","translate(" + margin.left + "," + margin.top + ")");
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Read CSV convert points to number values
  d3.json("/api/v1.0/Projected_Data").then(function (data) {
    data.forEach(function (d) {
      d.PROJECTED_POINTS = +d.PROJECTED_POINTS;
    });
    console.log(data);

    // Compute quartiles, median, inter quantile range min and max --> used to draw the box.
    var sumstat = d3
      .nest() // nest function allows to group the calculation by position
      .key(function (d) {
        return d.POSITION;
      })
      .rollup(function (d) {
        q1 = d3.quantile(
          d
            .map(function (g) {
              return g.PROJECTED_POINTS;
            })
            .sort(d3.ascending),
          0.25
        );
        median = d3.quantile(
          d
            .map(function (g) {
              return g.PROJECTED_POINTS;
            })
            .sort(d3.ascending),
          0.5
        );
        q3 = d3.quantile(
          d
            .map(function (g) {
              return g.PROJECTED_POINTS;
            })
            .sort(d3.ascending),
          0.75
        );
        min = d3.min(
          d.map(function (g) {
            return g.PROJECTED_POINTS;
          })
        );
        max = d3.max(
          d.map(function (g) {
            return g.PROJECTED_POINTS;
          })
        );
        interQuantileRange = q3 - q1;
        return {
          q1: q1,
          median: median,
          q3: q3,
          interQuantileRange: interQuantileRange,
          min: min,
          max: max,
        };
      })
      .entries(data);
    console.log(JSON.stringify(sumstat));

    // create scales
    var x = d3
      .scaleBand()
      .range([0, width])
      .domain(["QB", "RB", "WR", "TE", "DEF", "K"])
      .paddingInner(1)
      .paddingOuter(0.5);
    //  svg.append("g")
    chartGroup
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Show the Y scale
    var y = d3
      .scaleLinear()
      .domain([d3.min(data, (d) => d.PROJECTED_POINTS * 1.1), d3.max(data, (d) => d.PROJECTED_POINTS * 1.1)])
      .range([height, 0]);

    // var xAxis = d3.axisBottom(x);
    var yAxis = d3.axisLeft(y).ticks(6);

    // chartGroup.append("g")
    //     .attr("transform", `translate(0, ${height})`)
    //     .call(xAxis);

    chartGroup.append("g").call(yAxis);

    // var leftAxis = d3.axisLeft(y);
    // svg.append("g").call(d3.axisLeft(y))

    // Show the main vertical line
    // svg
    chartGroup
      .append("g")
      .selectAll("vertLines")
      .data(sumstat)
      .enter()
      .append("line")
      .attr("x1", function (d) {
        return x(d.key);
      })
      .attr("x2", function (d) {
        return x(d.key);
      })
      .attr("y1", function (d) {
        return y(d.value.min);
      })
      .attr("y2", function (d) {
        return y(d.value.max);
      })
      .attr("stroke", "black")
      .style("width", 40);

    // rectangle for the main box
    var boxWidth = 100;
    // svg
    chartGroup
      .append("g")
      .selectAll("boxes")
      .data(sumstat)
      .enter()
      .append("rect")
      .attr("x", function (d) {
        return x(d.key) - boxWidth / 2;
      })
      .attr("y", function (d) {
        return y(d.value.q3);
      })
      .attr("height", function (d) {
        return y(d.value.q1) - y(d.value.q3);
      })
      .attr("width", boxWidth)
      .attr("stroke", "black")
      .style("fill", "#69b3a2");

    // Show the median
    // svg
    chartGroup
      .append("g")
      .selectAll("medianLines")
      .data(sumstat)
      .enter()
      .append("line")
      .attr("x1", function (d) {
        return x(d.key) - boxWidth / 2;
      })
      .attr("x2", function (d) {
        return x(d.key) + boxWidth / 2;
      })
      .attr("y1", function (d) {
        return y(d.value.median);
      })
      .attr("y2", function (d) {
        return y(d.value.median);
      })
      .attr("stroke", "black")
      .style("width", 80);

    // Add individual points with jitter
    var jitterWidth = 100;
    var circlesGroup = chartGroup.selectAll("circle");
    // svg
    chartGroup
      .append("g")
      .selectAll("indPoints")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", function (d) {
        return x(d.POSITION) - jitterWidth / 2 + Math.random() * jitterWidth;
      })
      .attr("cy", function (d) {
        return y(d.PROJECTED_POINTS);
      })
      .attr("r", 5)
      .style("fill", "white")
      .attr("stroke", "black");

    // Initialize Tooltip
    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([40, -20])
      .html(function(d) {
        return (`${d.NAME}`);
      });
      // console.log(`${d.NAME}`);
    // Create tooltip in the chart
    svg.call(toolTip);

    //  Create event listeners to display and hide the tooltip
    circlesGroup
      .on("mouseover", function(data) {
        toolTip.show(data, this);
      })
      // onmouseout event
      .on("mouseout", function (data) {
        toolTip.hide(data);
      });

    // Create axes labels
    chartGroup
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 0)
      .attr("x", 0 - height / 1.5)
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("PROJECTED FANTASY POINTS");

    chartGroup
      .append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top - 10})`)
      .attr("class", "axisText")
      .text("POSITION");
  });
}

// When the browser loads, makeResponsive() is called.
makeResponsive();

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);
