// var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

d3.json("/api/v1.0/QB").then (QB => {
    console.log(QB);
})