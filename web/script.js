// Inicializar mapa
const map = L.map('map').setView([0, 0], 3);

// Agregar capa base satelital
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Imagery © NASA'
}).addTo(map);

// Agregar capa de países
fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: {
                color: 'white',
                weight: 1,
                fillOpacity: 0
            }
        }).addTo(map);
    });

// Variable para almacenar la capa de incendios
let firesLayer;
let activeButton = document.querySelector('button.active');

// Función para cargar incendios
async function loadFires(hours) {
    console.log('Fetching fires data...');
    
    // Actualizar botón activo
    if (activeButton) {
        activeButton.classList.remove('active');
    }
    activeButton = document.querySelector(`button[onclick="loadFires(${hours})"]`);
    activeButton.classList.add('active');

    // Limpiar capa anterior si existe
    if (firesLayer) {
        map.removeLayer(firesLayer);
    }

    try {
        const response = await fetch(`http://localhost:8001/fires/recent?hours=${hours}`);
        console.log('Response:', response);
        const data = await response.json();
        console.log('Data:', data);
		console.log("GeoJSON Features:", data.features);

        if (!data.features) {
            console.error('Invalid GeoJSON format:', data);
            return;
        }

        // Actualizar contador
        document.getElementById('fireCount').textContent = data.features.length;

        firesLayer = L.geoJSON(data, {
            pointToLayer: (feature, latlng) => {
                return L.circleMarker(latlng, {
                    radius: 1,
                    fillColor: "#ff3300",
                    color: "#ff0000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                }).bindPopup(`
                    <strong>Fire Details</strong><br>
                    Brightness: ${feature.properties.brightness}<br>
                    Confidence: ${feature.properties.confidence}<br>
                    Date: ${new Date(feature.properties.acquisition_date).toLocaleDateString()}
                `);
            }
        }).addTo(map);
    } catch (error) {
        console.error('Error loading fires:', error);
        alert('Error loading fires data. Check console for details.');
    }
}

// Cargar datos iniciales (últimas 24h)
loadFires(24);