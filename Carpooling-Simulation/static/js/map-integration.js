/**
 * Map integration using OpenRouteService
 */

// OpenRouteService API key
const ORS_API_KEY = '5b3ce3597851110001cf6248332da58066754fecb0017d09549fb12f';

// Bangalore coordinates (center)
const BANGALORE_CENTER = [12.9716, 77.5946];

// Real coordinates for our stops
const ROUTE_COORDINATES = {
    "Banashankari": [12.9255, 77.5468],
    "Jayanagar": [12.9299, 77.5833],
    "BTM Layout": [12.9166, 77.6101],
    "Silk Board": [12.9167, 77.6167],
    "HSR Layout": [12.9116, 77.6389],
    "Bommanahalli": [12.9018, 77.6170],
    "Kudlu Gate": [12.8895, 77.6387],
    "Hosa Road": [12.8762, 77.6458],
    "Electronic City Phase 1": [12.8451, 77.6619],
    "Electronic City Phase 2": [12.8385, 77.6771],
    "Neeladri Road": [12.8306, 77.6784],
    "Huskur Gate": [12.8160, 77.6687],
    "Hebbagodi": [12.8236, 77.6630],
    "Bommasandra": [12.8173, 77.6968],
    "Jigani": [12.7828, 77.6374],
    "Chandapura": [12.7978, 77.7140],
    "Hennagara": [12.7811, 77.7184],
    "Anekal": [12.7105, 77.6975],
    "Marsur": [12.7354, 77.7343],
    "Jigani Cross": [12.7683, 77.6372],
    "Sarjapur": [12.8588, 77.7881],
    "Dommasandra": [12.8546, 77.7572],
    "Carmelaram": [12.9051, 77.7156],
    "Ambedkar Nagar": [12.7835, 77.7284],
    "Kodathi": [12.8981, 77.7208],
    "Mugalur": [12.8058, 77.7920],
    "Sarjapur Circle": [12.8553, 77.7877],
    "Attibele Industrial Area": [12.7784, 77.7647],
    "Attibele Bus Stop": [12.7815, 77.7706],
    "Attibele": [12.7784, 77.7718]
};

// Store calculated routes
let routeCache = {};
let routePolylines = {};

// Initialize the map
let map;
let carMarkers = {};
let requestMarkers = {};
let locationMarkers = {};
let demandHeatmap = {};

// Add at the top of your file
window.mapInitialized = false;

function initMap() {
    try {
        // Create a map centered on Bangalore
        map = L.map('map').setView(BANGALORE_CENTER, 11);

        // Add OpenStreetMap tiles (free)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);
        
        // Add location markers for all stops
        Object.entries(ROUTE_COORDINATES).forEach(([name, coords]) => {
            const marker = L.circleMarker(coords, {
                radius: 6,
                fillColor: '#3388ff',
                color: '#3388ff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.5,
                className: 'location-marker'
            }).addTo(map);
            
            marker.bindTooltip(name, {
                permanent: false,
                direction: 'top'
            });
            
            locationMarkers[name] = marker;
        });
        
        // Calculate and display routes between major destinations
        calculateAllRoutes();
        
        // Fit map to show all locations
        const bounds = L.latLngBounds(Object.values(ROUTE_COORDINATES));
        map.fitBounds(bounds);
        
        window.mapInitialized = true;
        console.log("Map initialized successfully");
        return true;
    } catch (error) {
        console.error("Error initializing map:", error);
        window.mapInitialized = false;
        return false;
    }
}

// Enable map click to add car
function enableMapClickToAddCar() {
    // Add click handler to map
    map.on('click', function(e) {
        addCarAtClickedLocation(e);
    });
    
    // Add a helper message
    showToast('Click anywhere on the map to add a car at the nearest stop', 'info-toast');
}

// Disable map click functionality
function disableMapClickToAddCar() {
    map.off('click');
}

async function calculateAndDisplayRoute(start, end) {
    const cacheKey = `${start}-${end}`;
    
    // Check if route is cached
    if (routeCache[cacheKey]) {
        displayRoute(routeCache[cacheKey], start, end);
        return routeCache[cacheKey];
    }
    
    try {
        const startCoords = ROUTE_COORDINATES[start];
        const endCoords = ROUTE_COORDINATES[end];
        
        if (!startCoords || !endCoords) {
            console.error("Invalid start or end location");
            return null;
        }
        
        // Make API request to OpenRouteService
        const response = await fetch(`https://api.openrouteservice.org/v2/directions/driving-car?api_key=${ORS_API_KEY}&start=${startCoords[1]},${startCoords[0]}&end=${endCoords[1]},${endCoords[0]}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json, application/geo+json, application/gpx+xml',
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.features && data.features.length > 0) {
            const route = data.features[0];
            routeCache[cacheKey] = route;
            displayRoute(route, start, end);
            return route;
        } else {
            console.error("No route found", data);
            return null;
        }
    } catch (error) {
        console.error("Error calculating route:", error);
        return null;
    }
}

function displayRoute(route, start, end) {
    // Convert GeoJSON coordinates (long, lat) to Leaflet coordinates (lat, long)
    const coords = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
    
    // Draw the route on the map
    const routeKey = `${start}-${end}`;
    
    // Remove existing polyline if any
    if (routePolylines[routeKey] && map.hasLayer(routePolylines[routeKey])) {
        map.removeLayer(routePolylines[routeKey]);
    }
    
    // Create new polyline
    const polyline = L.polyline(coords, {
        color: '#3388ff',
        weight: 4,
        opacity: 0.7
    }).addTo(map);
    
    // Store reference
    routePolylines[routeKey] = polyline;
    
    return polyline;
}

// Update the interpolatePosition function

function interpolatePosition(start, end, progress) {
    // Get coordinates for start and end locations
    const startCoords = ROUTE_COORDINATES[start];
    const endCoords = ROUTE_COORDINATES[end];
    
    if (!startCoords || !endCoords) {
        return startCoords || endCoords || BANGALORE_CENTER;
    }
    
    // Check if we have a cached route for this segment
    const routeKey = `${start}-${end}`;
    if (routeCache[routeKey]) {
        const route = routeCache[routeKey];
        // Get coordinates from route geometry
        const coords = route.geometry.coordinates;
        
        if (coords && coords.length > 1) {
            // Calculate which segment of the route we're on based on progress
            const totalSegments = coords.length - 1;
            const currentSegmentIdx = Math.min(Math.floor(progress * totalSegments), totalSegments - 1);
            
            // Calculate progress within this segment
            const segmentProgress = (progress * totalSegments) - currentSegmentIdx;
            
            // Get the two points of the current segment
            const point1 = coords[currentSegmentIdx];
            const point2 = coords[currentSegmentIdx + 1];
            
            // Interpolate between these two points
            const lng = point1[0] + (point2[0] - point1[0]) * segmentProgress;
            const lat = point1[1] + (point2[1] - point1[1]) * segmentProgress;
            
            return [lat, lng]; // Convert to [lat, lng] for Leaflet
        }
    }
    
    // Fallback to direct line interpolation if no route found
    const lat = startCoords[0] + (endCoords[0] - startCoords[0]) * progress;
    const lng = startCoords[1] + (endCoords[1] - startCoords[1]) * progress;
    
    return [lat, lng];
}

function updateCarPositions(cars) {
    // Remove existing car markers
    Object.values(carMarkers).forEach(marker => {
        if (map.hasLayer(marker)) {
            map.removeLayer(marker);
        }
    });
    
    // Add new car markers
    cars.forEach(car => {
        if (!car.active) return;
        
        let coords;
        
        // If car is between locations, interpolate position
        if (car.progress > 0 && car.progress < 1 && car.next_location) {
            coords = interpolatePosition(car.current_location, car.next_location, car.progress);
        } else {
            coords = ROUTE_COORDINATES[car.current_location];
        }
        
        if (!coords) return;
        
        const isToAttibele = car.id.includes('BAN-ATT');
        
        const carIcon = L.divIcon({
            className: 'car-marker',
            html: `<div class="car-icon ${isToAttibele ? 'banashankari' : 'attibele'}">${car.passenger_count}</div>`,
            iconSize: [30, 30]
        });
        
        const marker = L.marker(coords, {
            icon: carIcon,
            title: car.id,
            zIndexOffset: 1000
        }).addTo(map);
        
        // Calculate percent full
        const percentFull = (car.passenger_count / car.capacity) * 100;
        
        marker.bindPopup(`
            <div class="car-popup">
                <strong>${car.id}</strong>
                Passengers: ${car.passenger_count}/${car.capacity}<br>
                From: ${car.current_location}<br>
                To: ${car.destination}
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: ${percentFull}%;"></div>
                </div>
            </div>
        `);
        
        carMarkers[car.id] = marker;
    });
}

function updateRequestMarkers(requests) {
    // Remove existing request markers
    Object.values(requestMarkers).forEach(marker => {
        if (map.hasLayer(marker)) {
            map.removeLayer(marker);
        }
    });
    
    // Reset demand highlighting
    Object.values(locationMarkers).forEach(marker => {
        marker.setStyle({
            fillColor: '#3388ff',
            color: '#3388ff'
        });
    });
    
    // Group requests by pickup location to show demand
    const demandByLocation = {};
    
    requests.forEach(request => {
        if (!demandByLocation[request.pickup]) {
            demandByLocation[request.pickup] = 0;
        }
        demandByLocation[request.pickup]++;
    });
    
    // Highlight locations with high demand
    Object.entries(demandByLocation).forEach(([location, count]) => {
        if (locationMarkers[location]) {
            // Change color based on demand
            if (count >= 3) {
                // High demand - red
                locationMarkers[location].setStyle({
                    fillColor: '#e63946',
                    color: '#e63946',
                    fillOpacity: 0.8,
                });
                locationMarkers[location].setRadius(8); // Make it bigger
            } else if (count >= 2) {
                // Medium demand - orange
                locationMarkers[location].setStyle({
                    fillColor: '#f4a261',
                    color: '#f4a261',
                    fillOpacity: 0.7
                });
                locationMarkers[location].setRadius(7);
            }
            
            // Add demand highlight class for pulsing effect
            if (count >= 2) {
                locationMarkers[location]._path.classList.add('demand-highlight');
            }
        }
    });
    
    // Add new request markers
    requests.forEach(request => {
        const coords = ROUTE_COORDINATES[request.pickup];
        if (!coords) return;
        
        const requestIcon = L.divIcon({
            className: 'request-marker',
            html: '<div class="request-icon"></div>',
            iconSize: [20, 20]
        });
        
        const marker = L.marker(coords, {
            icon: requestIcon,
            title: `Request: ${request.pickup} → ${request.dropoff}`,
            zIndexOffset: 900
        }).addTo(map);
        
        marker.bindPopup(`
            <div class="request-popup">
                <strong>Pickup Request</strong>
                From: ${request.pickup}<br>
                To: ${request.dropoff}
            </div>
        `);
        
        requestMarkers[request.id] = marker;
    });
}

// Calculate routes between consecutive stops
async function calculateAllRoutes() {
    try {
        // Calculate main route from Banashankari to Attibele
        await calculateAndDisplayRoute("Banashankari", "Attibele");
        
        // Calculate shorter segment routes for more accurate car positioning
        const stopNames = Object.keys(ROUTE_COORDINATES);
        for (let i = 0; i < stopNames.length - 1; i++) {
            // Only calculate routes between adjacent stops
            if (i % 5 === 0) {  // Calculate every 5th segment to avoid API limits
                const start = stopNames[i];
                const end = stopNames[i + 5 >= stopNames.length ? stopNames.length - 1 : i + 5];
                await calculateAndDisplayRoute(start, end);
                
                // Small delay to not overload the API
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    } catch (error) {
        console.error("Error calculating routes:", error);
    }
}

// Handle map interaction for user to manually add a car
function addCarAtClickedLocation(e) {
    // Find closest stop to the clicked location
    const clickedPoint = e.latlng;
    let minDistance = Infinity;
    let closestLocation = null;
    
    Object.entries(ROUTE_COORDINATES).forEach(([name, coords]) => {
        const distance = clickedPoint.distanceTo(L.latLng(coords));
        if (distance < minDistance) {
            minDistance = distance;
            closestLocation = name;
        }
    });
    
    if (closestLocation && minDistance < 2000) { // Within 2km
        // Show confirmation to add a car here
        if (confirm(`Add a new car at ${closestLocation}?`)) {
            // Determine default direction based on location index
            const locations = Object.keys(ROUTE_COORDINATES);
            const locIndex = locations.indexOf(closestLocation);
            const middleIndex = Math.floor(locations.length / 2);
            const suggestedDirection = locIndex < middleIndex ? "to_attibele" : "to_banashankari";
            
            // Create a simple popup for direction choice
            const direction = confirm(`Set direction to Attibele?`) ? 
                "to_attibele" : "to_banashankari";
            
            // Call the API to add a car
            fetch('/add_car', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    location: closestLocation,
                    direction: direction
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Car added:", data);
                // Update map and show toast notification (handled by main script)
            })
            .catch(error => {
                console.error('Error adding car:', error);
            });
        }
    } else {
        alert("Please click closer to a route location to add a car");
    }
}

// Add this function to handle traffic layer

let trafficLayer = null;

function toggleTrafficLayer() {
    if (trafficLayer) {
        // Remove existing traffic layer
        map.removeLayer(trafficLayer);
        trafficLayer = null;
        return false;
    } else {
        // Add traffic layer
        // Note: This requires a premium OpenRouteService plan
        // Using a basic visualization for demonstration
        trafficLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            opacity: 0.5,
            attribution: 'Traffic data (simulated)'
        }).addTo(map);
        
        // Add some simulated traffic congestion indicators
        const congestionPoints = [
            { location: ROUTE_COORDINATES["Silk Board"], severity: "high" },
            { location: ROUTE_COORDINATES["Electronic City Phase 1"], severity: "medium" },
            { location: ROUTE_COORDINATES["BTM Layout"], severity: "medium" }
        ];
        
        congestionPoints.forEach(point => {
            const color = point.severity === "high" ? "#ff0000" : 
                         (point.severity === "medium" ? "#ff9900" : "#ffff00");
                         
            L.circle(point.location, {
                color: color,
                fillColor: color,
                fillOpacity: 0.5,
                radius: 300
            }).addTo(map).bindTooltip(`${point.severity.toUpperCase()} traffic congestion`);
        });
        
        return true;
    }
}

// Add this function

function findNearestCar(location) {
    // Get all active cars
    const activeCars = Object.values(carMarkers);
    if (activeCars.length === 0) {
        showToast('No active cars available', 'error-toast');
        return;
    }
    
    // Find coordinates of the location
    const locationCoords = ROUTE_COORDINATES[location];
    if (!locationCoords) {
        showToast('Invalid location', 'error-toast');
        return;
    }
    
    // Calculate distance to each car
    let nearestCar = null;
    let shortestDistance = Infinity;
    
    activeCars.forEach(carMarker => {
        const distance = L.latLng(locationCoords).distanceTo(carMarker.getLatLng());
        if (distance < shortestDistance) {
            shortestDistance = distance;
            nearestCar = carMarker;
        }
    });
    
    if (nearestCar) {
        // Highlight the nearest car
        nearestCar.openPopup();
        map.panTo(nearestCar.getLatLng());
        
        // Create a pulsing line between location and car
        const line = L.polyline([locationCoords, nearestCar.getLatLng()], {
            color: '#ff3860',
            weight: 3,
            opacity: 0.8,
            dashArray: '10, 10',
            className: 'pulsing-line'
        }).addTo(map);
        
        // Remove line after a few seconds
        setTimeout(() => {
            map.removeLayer(line);
        }, 5000);
        
        return nearestCar;
    }
    
    return null;
}

// Export functions to be used in the main script
window.mapFunctions = {
    initMap,
    updateCarPositions,
    updateRequestMarkers,
    calculateAndDisplayRoute,
    addCarAtClickedLocation,
    enableMapClickToAddCar,
    disableMapClickToAddCar,
    toggleTrafficLayer,
    findNearestCar
};