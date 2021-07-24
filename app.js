var y0 = [];
var y1 = [];
for (var i = 0; i < data.length; i ++) {
	y0[i] = Math.random();
	y1[i] = Math.random() + 1;
}

var trace1 = {
  y: y0,
  type: 'box'
};

var trace2 = {
  y: y1,
  type: 'box'
};

var data = [trace1, trace2];

Plotly.newPlot('myDiv', data);


function boxPlot() {
    d3.json("/api/v1.0/Projected_Data").then( PjPts => {
        
    })
}


d3.selectAll("#positionDropDown").on("change", statChart);

function statChart() {
    // Use D3 to select the dropdown menu
    var dropdownMenu = d3.select("#positionDropDown").on("change", statChart);
    // Assign the value of the dropdown menu option to a variable
    var dataset = dropdownMenu.property("value");
  
    // // Initialize x and y arrays
    // var x = [];
    // var y = [];
  
    if (dataset === 'QB') {
        d3.json("http://127.0.0.1:5000/api/v1.0/QB").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
        })
    }
  
        // else if (dataset === 'RB') {
        //     x = [10, 20, 30, 40, 50];
        //     y = [1, 10, 100, 1000, 10000];
        // }
}
         
// function adpGraph(adpData) {
//     d3.json(flaskurl).then(data => {
        
//     })

// }

function init(){
    var dropDown = d3.select("#positionDropDown");

    d3.json(flaskurl).then(positions => {
        var positionIds = positions;
        positionIds.forEach(adpData => {
            dropDown.append("option").text(adpData).proptery("value",adpData);
        })
    })

    statchart();
    adpGraph();
}

function optionChange() {
    function statChart();
    // function adpGraph(newAdpData);
}

init();