// function makeResponsive() {
//     // if the SVG area isn't empty when the browser loads,
//     // remove it and replace it with a resized version of the chart
//     var svgArea = d3.select("body").select("svg");
  
//     // clear svg is not empty
//     if (!svgArea.empty()) {
//       svgArea.remove();
//     }
    var svgWidth = 1000;
    var svgHeight = 700;
  
    // Chart Params
    var margin = {
      top: 20,
      right: 40,
      bottom: 50,
      left: 40,
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
        .domain([d3.min(data, (d) => d.PROJECTED_POINTS * .5), d3.max(data, (d) => d.PROJECTED_POINTS * 1.1)])
        .range([height, 0]);
  
      // var xAxis = d3.axisBottom(x);
      var yAxis = d3.axisLeft(y).ticks(6);
  
      chartGroup.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(x);
  
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
  
      // // Initialize Tooltip
      // var toolTip = d3.tip()
      //   .attr("class", "tooltip")
      //   .offset([40, -20])
      //   .html(function(d) {
      //     console.log(`${d.NAME}`);
      //     return (`${d.NAME}`);
      //   });
      // // Create tooltip in the chart
      // svg.call(toolTip);
  
      // //  Create event listeners to display and hide the tooltip
      // circlesGroup
      //   .on("mouseover", function(data) {
      //     toolTip.show(data, this);
      //   })
      //   // onmouseout event
      //   .on("mouseout", function (data) {
      //     toolTip.hide(data);
      //   });
  
      // Create axes labels
      chartGroup
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left - 2)
        .attr("x", 0 - height / 1.5)
        .attr("dy", "1em")
        .attr("class", "axisText")
        .text("PROJECTED FANTASY POINTS");
  
      chartGroup
        .append("text")
        .attr("transform", `translate(${width / 2}, ${height + margin.top + 8})`)
        .attr("class", "axisText")
        .text("POSITION");
    });
//   }
  
  // When the browser loads, makeResponsive() is called.
//   makeResponsive();
  
  // When the browser window is resized, makeResponsive() is called.
//   d3.select(window).on("resize", makeResponsive);

function bubbleChart (data) {
    var AvgDP = data.AverageDraftPosition;
    var Name = data.Name;
    var Position = data.Position;
    var LSFP = data.LastSeasonFantasyPoints;
    var PFP = data.ProjectedFantasyPoints;
    var colors = [];

    var ADP = [];
    var Position =[];
    var Player =[];

    for (var i = 0; i < data.length; i++){
        ADP.push(data[i].AverageDraftPosition);
        Position.push(data[i].Position);
        Player.push(data[i].Name);
    }

    var bubblelayout = {
        title: "Player Average Draft Positions",
        hovermode: "closest",
        xaxis: {title: "Average Draft Position" },
        height: 600,
        width: 600
    };

    var bubbledata = [
        {
            x: Position,
            y: ADP,
            text: Player,
            mode: "markers",
            marker: {
                opacity: 0.3,
                size: 15,
                color: "green",
            }
        }
    ];
    Plotly.newPlot("bubble", bubbledata, bubblelayout);

}

const tbody = d3.select("tbody");


  
d3.selectAll("#positionDropDown").on("change", statChart);

function buildTable(data) {
    // First, clear out any existing data
    tbody.html("");
    console.log("in buildTable")
    console.log(data)
    // Next, loop through each object in the data
    // and append a row and cells for each value in the row
    data.forEach((dataRow) => {
        // Append a row to the table body
        const row = tbody.append("tr");
        
        // Loop through each field in the dataRow and add
        // each value as a table cell (td)
        Object.values(dataRow).forEach((val) => {
            let cell = row.append("td");
            cell.text(val);
        }
    );
    });
}

function statChart(adpData) {
    // Use D3 to select the dropdown menu
    var dropdownMenu = d3.select("#positionDropDown");
    // Assign the value of the dropdown menu option to a variable
    var dataset = dropdownMenu.property("value");

    // // Initialize x and y arrays
    // var x = [];
    // var y = [];

    if (dataset === 'QB') {
        d3.json("/api/v1.0/QB").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    }
    else if (dataset === 'ALL_PLAYERS') {
        d3.json("/api/v1.0/ADP_Data").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    }
    else if (dataset === 'DEF') {
        d3.json("/api/v1.0/DEF").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    }
    else if (dataset === 'RB') {
        d3.json("/api/v1.0/RB").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    } 
    else if (dataset === 'K') {
        d3.json("/api/v1.0/K").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    } 
    else if (dataset === 'TE') {
        d3.json("/api/v1.0/TE").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    }  
    else if (dataset === 'WR') {
        d3.json("/api/v1.0/WR").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
            bubbleChart(data);
        })
    }
}


function handleClick() {

    // Grab the datetime value from the filter
    const date = d3.select("#positionDropDown").property("value");
    let filteredData = data;
  
    // Check to see if a date was entered and filter the
    // data using that date.
    if (position) {
      // Apply `filter` to the table data to only keep the
      // rows where the `datetime` value matches the filter value
      filteredData = filteredData.filter(row => row.Position === position);
    }
  
    // Rebuild the table using the filtered data
    // @NOTE: If no date was entered, then filteredData will
    // just be the original tableData.
    buildTable(filteredData);
}
  // Attach an event to listen for the form button
d3.selectAll("#filter-btn").on("click", handleClick);

// Build the table when the page loads
// buildTable(data);

function initTable(highlights) {
    // First, clear out any existing data
    d3.json("/api/v1.0/Highlights").then(highlights => {
        var statTable = d3.select('tbody');
        // buildTable(highlights);
        bubbleChart(highlights);
        makeResponsive(highlights);
    })
}
initTable();