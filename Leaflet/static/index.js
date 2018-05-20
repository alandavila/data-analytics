//Earthquakes from past 7 days of magnitude 1.0 and above
//Data from: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
var link = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson";

// Creating map object
var map = L.map("map", {
  center: [19.4326, -99.1332],
  zoom: 3
});

var mapboxkey = 'pk.eyJ1IjoiYWxhbmRhdmlsYSIsImEiOiJjamd5YjFhZGcwM2VvMndxbHR3NHU3a3B6In0.mR4nyx_r_Ap_M1eTz0M35A'

// Adding tile layer from mapbox
//L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=" + mapboxkey).addTo(map);

//L.tileLayer("https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + mapboxkey).addTo(map);
//
L.tileLayer("https://api.mapbox.com/v4/mapbox.light/{z}/{x}/{y}.png?access_token=" + mapboxkey).addTo(map);

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  L.geoJson(data, {

    onEachFeature: function(feature, layer){

      var latlng = L.latLng(feature.geometry.coordinates[1], feature.geometry.coordinates[0]);
      var a_circle = L.circleMarker(latlng,
        {radius:2* feature.properties.mag,
         fill:true,
         color:getColor(feature.properties.mag),
         fillOpacity: 1.0
       }).bindPopup("<h3> Magnitude: " + feature.properties.mag   + " </h3>"
                       + "<p> Place: "+ feature.properties.place + "<p>").addTo(map);
    }
  });
});

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [2.5, 5.4, 6.0, 6.9, 7.9, 8.0],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] ) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

// Utilities
function getColor(d) {
    return d > 8.0  ? '#BD0026' :
           d > 7.9  ? '#E31A1C' :
           d > 6.9  ? '#FC4E2A' :
           d > 6.0   ? '#FD8D3C' :
           d > 5.4   ? '#FEB24C' :
           d > 2.5   ? '#FED976' :
                      '#FFEDA0';
}
