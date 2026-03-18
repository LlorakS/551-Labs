console.log("JS loaded");

// Create map
var map = L.map('map').setView([51.0447, -114.0719], 11);

// Basemap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);


// Marker cluster layer
var markers = L.markerClusterGroup();
map.addLayer(markers);


// Search permits
async function searchPermits() {

    let start = document.getElementById("startDate").value;
    let end = document.getElementById("endDate").value;

    if (!start || !end) {
        alert("Please choose dates");
        return;
    }

    // Calgary API endpoint
    let url = `https://data.calgary.ca/resource/c2es-76ed.json?$where=issueddate between '${start}' and '${end}'&$limit=200`;

    console.log("Request:", url);

    try {

        let response = await fetch(url);
        let data = await response.json();

        console.log("Records returned:", data.length);

        displayPermits(data);

    } catch (error) {

        console.error("Error loading data:", error);

    }

}


// Display permits
function displayPermits(data) {

    markers.clearLayers();

    data.forEach(function (permit) {

        if (!permit.latitude || !permit.longitude) return;

        let lat = parseFloat(permit.latitude);
        let lon = parseFloat(permit.longitude);

        let marker = L.marker([lat, lon]);

        let popup = `
        <b>Issued Date:</b> ${permit.issueddate}<br>
        <b>Work Class:</b> ${permit.workclassgroup}<br>
        <b>Contractor:</b> ${permit.contractorname}<br>
        <b>Community:</b> ${permit.communityname}<br>
        <b>Address:</b> ${permit.originaladdress}
        `;

        marker.bindPopup(popup);

        markers.addLayer(marker);

    });

    if (markers.getLayers().length > 0) {
        map.fitBounds(markers.getBounds());
    }

}





// OSM
var osmLayer = L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { attribution: '© OpenStreetMap' }
).addTo(map);

// Mapbox
var mapboxLayer = L.tileLayer(
  'https://api.mapbox.com/styles/v1/kmoyano/cmmwgzav900e501skbpi072ym/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia21veWFubyIsImEiOiJjbW13a3Q1b2oydmEzMnFvZWloZWdtbnE2In0.AgD8wsqS20f_8JiXUw71kQ',
  {
    tileSize: 512,
    zoomOffset: -1,
    attribution: '© Mapbox'
  }
);

// Layer control
var baseMaps = {
  "OpenStreetMap": osmLayer,
  "Traffic Incidents Map": mapboxLayer
};

L.control.layers(baseMaps).addTo(map);


//  FETChiNG TRAFFIC DATA
async function loadTrafficData() {

    let url = "https://data.calgary.ca/resource/35ra-9556.json?$limit=200";

    let response = await fetch(url);
    let data = await response.json();

    data.forEach(function (incident) {

        if (!incident.latitude || !incident.longitude) return;

        let marker = L.circleMarker(
            [parseFloat(incident.latitude), parseFloat(incident.longitude)],
            {
                radius: 5,
                color: "red"
            }
        );

        let popup = `
        <b>Description:</b> ${incident.description || "N/A"}<br>
        <b>Info:</b> ${incident.incident_info || "N/A"}
        `;

        marker.bindPopup(popup);

        marker.addTo(map);
    });
}
loadTrafficData();