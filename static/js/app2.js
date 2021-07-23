// // var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

// d3.json("/api/v1.0/QB").then (QB => {
//     console.log(QB);
// }) 

// function buildTable(data) { 

//     d3.json("/api/v1.0/ADP_Data").then(data => {
//         var statTable = d3.select('tbody');
//         console.log(data);
//         function buildTable(data) {
//             // First, clear out any existing data
//             tbody.html("");
    
//             // Next, loop through each object in the data
//             // and append a row and cells for each value in the row
//             data.forEach((dataRow) => {
//                 // Append a row to the table body
//                 const row = tbody.append("tr");
    
//                 // Loop through each field in the dataRow and add
//                 // each value as a table cell (td)
//                 Object.values(dataRow).forEach((val) => {
//                     let cell = row.append("td");
//                     cell.text(val);
//                 }
//             );
//             });
//         }
//     })
//   }
const tbody = d3.select("tbody");

// function initTable(highlights) {
//     // First, clear out any existing data
//     d3.json("/api/v1.0/Highlights").then(highlights => {
//         var statTable = d3.select('tbody');
//         buildTable(highlights);
//     })
// }
// initTable;
  
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
        })
    }
    else if (dataset === 'ALL_PLAYERS') {
        d3.json("/api/v1.0/ADP_Data").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
        })
    }
    else if (dataset === 'DEF') {
        d3.json("/api/v1.0/DEF").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
        })
    }
    else if (dataset === 'RB') {
        d3.json("/api/v1.0/RB").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
        })
    } 
    else if (dataset === 'K') {
        d3.json("/api/v1.0/K").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
        })
    } 
    else if (dataset === 'TE') {
        d3.json("/api/v1.0/TE").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
        })
    }  
    else if (dataset === 'WR') {
        d3.json("/api/v1.0/WR").then(data => {
            var statTable = d3.select('tbody');
            console.log(data);
            buildTable(data);
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