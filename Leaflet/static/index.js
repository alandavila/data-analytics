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

  for (var i = 0; i < data.features.length; i++) {
    // set the data location property to a variable
    var location = data.features[i].geometry;
    // If the data has a location property...
    if (location) {
      // Add a new marker to the map
      var latlng = L.latLng(location.coordinates[1], location.coordinates[0]);
      var magnitude = data.features[i].properties.mag;
      L.circleMarker(latlng,
        {radius:2*magnitude,
         fill:true,
         color:getColor(magnitude),
         fillOpacity: 1.0
       })
       .on(
         {click: function(event) {
          layer = event.target;
          layer.bindPopup("<h1>" what "</h1>");
          }
        })
       .addTo(map);

    }
  }
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
