# Lab 6 — Line Simplification

A web mapping application that lets users draw a polyline and visualize a simplified version of it using **Turf.js** and **Leaflet.js**.

## Features
- Click on the map to draw a polyline point by point
- Adjust the simplification tolerance with a slider
- Click **Simplify Line** to generate a simplified version of the drawn line in red
- Stats panel shows original point count, simplified point count, and % reduction
- Click **Clear & Reset** to wipe the map and draw a new line

## How to Run
It is a single HTML file.

1. Clone or download this repository
2. Open `index.html` in any modern browser (Chrome, Firefox, Edge)

Or serve it locally with Python:
python -m http.server 8000
Then open `http://localhost:8000` in your browser.

## How to Use
1. **Zoom in** on the map to a region you want to draw on
2. **Click** on the map repeatedly to place points — the blue polyline draws in real time
3. Adjust the **Tolerance slider** (higher = more aggressive simplification)
4. Click **Simplify Line** — a red simplified line appears over the original
5. Check the **stats panel** to see how many points were removed
6. Click **Clear & Reset** to start over

> **NOTE** Zoom in before drawing. If your points are spaced very far apart (continent scale), the simplification effect will be minimal and difficult to see. Zooming in so your line spans a city or region gives the best results.

## How It Works
The app uses **Turf.js's `simplify` function**, which implements the [Ramer–Douglas–Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm). The algorithm works by:

1. Drawing a straight line between the first and last points
2. Finding the point furthest from that line
3. If it's within the tolerance threshold, all middle points are removed
4. If not, the line is split at that point and the process repeats recursively

The `tolerance` value is in degrees. A higher tolerance removes more points; a lower tolerance preserves more of the original shape.

## Libraries Used
- [Leaflet.js v1.9.4](https://leafletjs.com/) — interactive map rendering
- [Turf.js v6](https://turfjs.org/) — geospatial analysis (line simplification)
- [OpenStreetMap](https://www.openstreetmap.org/) — map tile layer

## File Structure

```
lab6/
└── index.html    # entire application (single file, no dependencies to install)
```