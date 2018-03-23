// Creating map object
var myMap = L.map("map", {
    center: [0,0],
    zoom: 2
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFyaW5lbGxpam9zZXBoIiwiYSI6ImNqZXZ6N3lvejBram8ydnJ5dHNndDZ6OGUifQ.TkCbx1WD-lh0UPvHMhvbvg").addTo(myMap);

// Link to GeoJSON*****
var APILink = "http://data.beta.nyc//dataset/d6ffa9a4-c598-4b18-8caf-14abde6a5755/resource/74cdcc33-512f-439c-" +
    "a43e-c09588c4b391/download/60dbe69bcd3640d5bedde86d69ba7666geojsonmedianhouseholdincomecensustract.geojson";

var geojson;

// Grabbing data with d3...
d3.json(APILink, function (data) {

    // Creating a new choropleth layer
    geojson = L.choropleth(data, {
        // Which property in the features to use
        valueProperty: "MHI",
        // Color scale
        scale: ["#ffffb2", "#b10026"],
        // Number of breaks in step range
        steps: 10,
        // q for quantile, e for equidistant, k for k-means
        mode: "q",
        style: {
            // Border color
            color: "#fff",
            weight: 1,
            fillOpacity: 0.8
        },
        // Binding a pop-up to each layer
        onEachFeature: function (feature, layer) {
            layer.bindPopup(feature.properties.COUNTY + " " + feature.properties.State + "<br>Median Household Income:<br>" +
                "$" + feature.properties.MHI);
        }
    }).addTo(myMap);

    // Setting up the legend
    var legend = L.control({ position: "bottomright" });
    legend.onAdd = function () {
        var div = L.DomUtil.create("div", "info legend");
        var limits = geojson.options.limits;
        var colors = geojson.options.colors;
        var labels = [];

        // Add min & max
        var legendInfo = "<h1>Median Income</h1>" +
            "<div class=\"labels\">" +
            "<div class=\"min\">" + limits[0] + "</div>" +
            "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
            "</div>";

        div.innerHTML = legendInfo;

        limits.forEach(function (limit, index) {
            labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
        });

        div.innerHTML += "<ul>" + labels.join("") + "</ul>";
        return div;
    };

    // Adding legend to the map
    legend.addTo(myMap);

});
