var map_1fbdc53d09fdfcc16967e6300e913c4b = L.map(
    "map_1fbdc53d09fdfcc16967e6300e913c4b",
    {
        center: [55.7, 37.6],
        crs: L.CRS.EPSG3857,
        zoom: 12,
        zoomControl: true,
        preferCanvas: false,
    }
);
var tile_layer_8850fe7d28726b53a0505b0b9213f19c = L.tileLayer(
    "https://tile.thunderforest.com/pioneer/{z}/{x}/{y}.png?apikey=6f3a690732a641eb9409e4dfec02bf3e"
).addTo(map_1fbdc53d09fdfcc16967e6300e913c4b);  

mapMarkers1 = []; // for 1 client

var source = new EventSource('/topic/testFrontend');
source.addEventListener('message', function(e){

console.log('Message');
obj = JSON.parse(e.data);
console.log(obj);
for (var i = 0; i < mapMarkers1.length; i++) {
  map_1fbdc53d09fdfcc16967e6300e913c4b.removeLayer(mapMarkers1[i]);
}
//point with speed
marker1 = L.marker([obj.coords[1], obj.coords[0]]).addTo(map_1fbdc53d09fdfcc16967e6300e913c4b)
.bindPopup("Velocity: " + JSON.stringify(obj.velocity)+" km/h").openPopup();

var circle2 = L.circle([obj.coords[1], obj.coords[0]], {
  color: 'red',
  fillColor: 'red',
  fillOpacity: 0.1,
  radius: obj.accuracy[1]
}).addTo(map_1fbdc53d09fdfcc16967e6300e913c4b);

var circle = L.circle([obj.coords[1], obj.coords[0]], {
  color: 'blue',
  fillColor: 'blue',
  fillOpacity: 0.1,
  radius: obj.accuracy[0]
}).addTo(map_1fbdc53d09fdfcc16967e6300e913c4b);


  mapMarkers1.push(marker1);

}, false);  