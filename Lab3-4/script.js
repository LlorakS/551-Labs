console.log("JS loaded");

// CREATE MAP
var map = L.map('map').setView([51.0447, -114.0719], 11);

// BASEMAP (OSM)
var osmLayer = L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { attribution: '© OpenStreetMap' }
).addTo(map);

// MAPBOX STYLE (VISUAL LAYER)
var mapboxLayer = L.tileLayer(
  'https://api.mapbox.com/styles/v1/kmoyano/cmmwgzav900e501skbpi072ym/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia21veWFubyIsImEiOiJjbW13a3Q1b2oydmEzMnFvZWloZWdtbnE2In0.AgD8wsqS20f_8JiXUw71kQ',
  {
    tileSize: 512,
    zoomOffset: -1,
    attribution: '© Mapbox'
  }
);

// PERMIT MARKERS (LAB 3)
var permitMarkers = L.markerClusterGroup();
map.addLayer(permitMarkers);

// TRAFFIC INCIDENT MARKERS (INTERACTIVE)
var trafficLayer = L.layerGroup();

// SEARCH PERMITS (DATE FILTERED)
async function searchPermits() {

    let start = document.getElementById("startDate").value;
    let end = document.getElementById("endDate").value;

    if (!start || !end) {
        alert("Please choose dates");
        return;
    }

    let url = `https://data.calgary.ca/resource/c2es-76ed.json?$where=issueddate between '${start}' and '${end}'&$limit=200`;

    try {
        let response = await fetch(url);
        let data = await response.json();

        displayPermits(data);

    } catch (error) {
        console.error("Error loading permits:", error);
    }
}

// DISPLAY PERMITS
function displayPermits(data) {

    permitMarkers.clearLayers();

    data.forEach(function (permit) {

        if (!permit.latitude || !permit.longitude) return;

        let marker = L.marker([
            parseFloat(permit.latitude),
            parseFloat(permit.longitude)
        ]);

        let popup = `
        <b>Issued Date:</b> ${permit.issueddate}<br>
        <b>Work Class:</b> ${permit.workclassgroup}<br>
        <b>Contractor:</b> ${permit.contractorname}<br>
        <b>Community:</b> ${permit.communityname}<br>
        <b>Address:</b> ${permit.originaladdress}
        `;

        marker.bindPopup(popup);

        permitMarkers.addLayer(marker);
    });

    if (permitMarkers.getLayers().length > 0) {
        map.fitBounds(permitMarkers.getBounds());
    }
}

// LOAD TRAFFIC INCIDENTS (WITH POPUPS)
async function loadTrafficData() {

    let url = "https://data.calgary.ca/resource/35ra-9556.json?$limit=1000";

    try {

        let response = await fetch(url);
        let data = await response.json();

        trafficLayer.clearLayers();

        data.forEach(function (incident) {

            if (!incident.latitude || !incident.longitude) return;

            let marker = L.circleMarker(
                [parseFloat(incident.latitude), parseFloat(incident.longitude)],
                {
                    radius: 6,
                    color: "black",
                    fillColor: "red",
                    fillOpacity: 0.8
                }
            );

            let popup = `
            <b>Description:</b> ${incident.description || "N/A"}<br>
            <b>Info:</b> ${incident.incident_info || "N/A"}<br>
            <b>Info:</b> ${incident.start_dt || "N/A"}<br>

            `;

            marker.bindPopup(popup);

            trafficLayer.addLayer(marker);
        });

    } catch (error) {
        console.error("Error loading traffic data:", error);
    }
}

// LOAD traffic data ONCE
loadTrafficData();

// =======================
// LAYER CONTROL (CHECKBOX STYLE)
// =======================
var baseMaps = {
    "OpenStreetMap": osmLayer
};

var overlayMaps = {
    "Permit Data": permitMarkers,
    "Traffic Incidents (Mapbox Style)": mapboxLayer,
    "Traffic Incidents (Interactive)": trafficLayer
};

L.control.layers(baseMaps, overlayMaps).addTo(map);