## ENGO 551 Lab 5 - IoT Geo Tracker
A lightweight, browser based IoT dashboard that integrates MQTT messaging with Geographic Information Systems (GIS). This application allows users to connect to a broker, publich real time location and temperature data, and visualize incoming teleetry on an interactive map.

# Features
- real time MQTT connectivity: connects to any public or private WebSocket-enabled MQTT broker, dafaults to test.mosquitto.org:8080
- Live map visualization: uses leaflet.js to render incoming GeoJSON features as interactice circle markers.
- Dynamic data symbology:  markers are automatically color coded based on temperature values: blue < 10C, 10C < green > 29.9C,  red => 30C.
- Geolocation integration: 'share my ststus' fetches the user's GPS coordinates and generates a random temperature reading for testing.
- Acitivity console: a log window to track connection status, subscriptions, as well as incoming massages.

# Technology
- Frontend:  HTML5, CSS3
- Messaging: MQTT JS
- Basemap:   OpenStreetMap

# How to use
- Start connection: enter the Broker Host and Port, then click Start
- Subscribe: Enter a topic to automatically susbscribe to it upon connection.
- Publich manual data: enter a string in the message field and click Publish.
- Share location: this will request geolocationi permissions, format data into GeoJSON Feature, publish JSON to entered topic.
- View results: GeoJSON sent to your subcribed topic will appear instatntly as a colored marker on the map. Click marker to show the popup with specific attributes.

