var SanDiegoCoords = [32.715736, -117.161087];
var mapZoomLevel = 12;

var mymap = L.map("map-id",  {
  center: SanDiegoCoords,
  zoom: mapZoomLevel
});
   
// Create the createMap function
console.log(positions)

  // Create the tile layer that will be the background of our map
var lightmap = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: API_KEY
}).addTo(mymap);

//"Name","Ranking","Address","zipcode","median","latitude","longitude",

// Loop through the cities array and create one marker for each city, bind a popup containing its name and population add it to the map
for (var i = 0; i < positions.length; i++) {
  var position = positions[i];
  L.marker([position.latitude,position.longitude])
    .bindPopup("<h1>" + position.Name + "</h1> <hr>" +"School Ranking: " +position.Ranking+"</h1> <hr>"+position.Address+"</h1> <hr>"+position.zipcode+"</h1> <hr>",position.median+"</h1> <hr>")
    .addTo(mymap);
}

// Create a new marker 
//L.marker([45.52, -122.67]).addTo(myMap);



//   // Create a baseMaps object to hold the lightmap layer
// var baseMaps = {
//     "Light Map": lightmap, 
//   };


//   // Create an overlayMaps object to hold the bikeStations layer
// var overlayMaps = {
//   "Bike Station": bike-stations,
// };

//   // Create the map object with options
// var mymap = L.map("map-id",  {
//     center: newYorkCoords,
//     zoom: mapZoomLevel,
//     layers: [baseMaps, overlayMaps]
// });


//   // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
// L.control.layers(baseMaps, overlayMaps, {
//   collapsed: true
// }).addTo(mymap);


// var newtry = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json";

// d3.json(newtry, function(response) {

//   console.log(response);

//   for (var i = 0; i < response.length; i++) {
//     var location = response[i].location;

//     if (location) {
//       L.marker([location.coordinates[1], location.coordinates[0]]).addTo(myMap);
//     }
//   }

// });
