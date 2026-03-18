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
        map.fitBounds(markers.getBounds());h
    }

}


var mapboxLayer = L.tileLayer(
'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia21veWFubyIsImEiOiJjbW13Zms5ZHkwY3hoMnJvc25lcm00eHp2In0.wgIehNN2_gWDoPH1qBvV8g', {
    id: 'kmoyano/cmmwgzav900e501skbpi072ym',
    tileSize: 512,
    zoomOffset: -1,
    attribution: '© Mapbox'
});

var overlayMaps = {
    "Traffic Incidents Layer": mapboxLayer
};

var baseMaps = {
    "OpenStreetMap": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
};

L.control.layers(baseMaps, overlayMaps).addTo(map);