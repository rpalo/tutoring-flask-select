var mymap = L.map('map').setView([40, -100], 4);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox.streets',
  accessToken: apiKey
}).addTo(mymap);

// Until you put in your api key, this code won't work.
//console.error("Make sure the 'accessToken' on main.js:6 is your real api key.");

var markers = [];
var items = new Set;
var selector = document.querySelector("#choice");

d3.json('/data', function (data) {
  data.forEach(function (datapoint) {
    marker = L.marker(datapoint.coords,
      {
        items: datapoint.items,
        name: datapoint.name
      }
    );
    markers.push(marker);
    marker.addTo(mymap);
    Object.keys(datapoint.items).forEach(function (item) {
      items.add(item);
    }
  });

  items.forEach(function (item) {
    const option = document.createElement('option');
    option.innerHTML = item;
    selector.appendChild(option);
  })
});

selector.addEventListener('change', function () {
  const selected = this.value;
  markers.forEach(function (marker) {
    if (marker.options.item == selected || selected == '') {
      marker.setOpacity(1);
    } else {
      marker.setOpacity(0);
    }
  });
});




