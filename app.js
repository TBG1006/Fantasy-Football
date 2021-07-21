function statchart(adpData) {
    d3.json(flaskurl).then(data => {
        var statTable = d3.select('tbody');


    })
}

function adpGraph(adpData) {
    d3.json(flaskurl).then(data => {
        
    })

}

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

function optionChange(newAdpData){
    function statchart(newAdpData);
    function adpGraph(newAdpData);
}

init();