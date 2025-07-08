// Dashboard JavaScript Functions

let map;
let trafficChart;

// Initialize the map with location data
function initializeMap(locations) {
    // Initialize map
    map = L.map('map').setView([20, 0], 2);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add markers for each location
    locations.forEach(function(location) {
        const marker = L.marker([location.lat, location.lon]).addTo(map);
        
        // Create popup content
        const popupContent = `
            <div class="popup-content">
                <h6><strong>${location.city}, ${location.country}</strong></h6>
                <p><strong>IP:</strong> ${location.ip}</p>
                <p><strong>Visits:</strong> ${location.visits}</p>
            </div>
        `;
        
        marker.bindPopup(popupContent);
    });
    
    // If we have locations, fit the map to show all markers
    if (locations.length > 0) {
        const group = new L.featureGroup(
            locations.map(loc => L.marker([loc.lat, loc.lon]))
        );
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// Initialize traffic trends chart
function initializeChart(trafficData) {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    
    // Prepare data for Chart.js
    const labels = trafficData.map(item => {
        const date = new Date(item[0]);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    });
    
    const data = trafficData.map(item => item[1]);
    
    trafficChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Visits per Hour',
                data: data,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Refresh data function
function refreshData() {
    fetch('/api/locations')
        .then(response => response.json())
        .then(data => {
            // Clear existing markers
            map.eachLayer(function(layer) {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
            
            // Add new markers
            data.locations.forEach(function(location) {
                const marker = L.marker([location.lat, location.lon]).addTo(map);
                
                const popupContent = `
                    <div class="popup-content">
                        <h6><strong>${location.city}, ${location.country}</strong></h6>
                        <p><strong>IP:</strong> ${location.ip}</p>
                        <p><strong>Visits:</strong> ${location.visits}</p>
                    </div>
                `;
                
                marker.bindPopup(popupContent);
            });
            
            // Fit bounds if we have locations
            if (data.locations.length > 0) {
                const group = new L.featureGroup(
                    data.locations.map(loc => L.marker([loc.lat, loc.lon]))
                );
                map.fitBounds(group.getBounds().pad(0.1));
            }
        })
        .catch(error => {
            console.error('Error refreshing data:', error);
        });
}

// Auto-refresh every 5 minutes
setInterval(refreshData, 300000);

// Utility functions
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function truncateUrl(url, maxLength = 30) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Add click handlers for interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Add refresh button functionality if needed
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshData);
    }
    
    // Add tooltips to truncated URLs
    const urlElements = document.querySelectorAll('.text-truncate');
    urlElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            if (this.scrollWidth > this.clientWidth) {
                this.setAttribute('data-bs-toggle', 'tooltip');
                this.setAttribute('data-bs-placement', 'top');
                const tooltip = new bootstrap.Tooltip(this);
                tooltip.show();
            }
        });
    });
});

// Error handling for map initialization
function handleMapError(error) {
    console.error('Map initialization error:', error);
    document.getElementById('map').innerHTML = `
        <div class="alert alert-warning text-center">
            <i class="fas fa-exclamation-triangle"></i>
            Unable to load map. Please check your internet connection.
        </div>
    `;
}

// Error handling for chart initialization
function handleChartError(error) {
    console.error('Chart initialization error:', error);
    document.getElementById('trafficChart').innerHTML = `
        <div class="alert alert-warning text-center">
            <i class="fas fa-exclamation-triangle"></i>
            Unable to load traffic chart.
        </div>
    `;
}