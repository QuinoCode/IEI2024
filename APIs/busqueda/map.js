var ui;

function cancelarBusqueda() {
    console.log("cancelar")
}

function realizarBusqueda() {
    var localidad = document.getElementById('localidad').value;
    var codigo_postal = document.getElementById('codigo_postal').value;
    var provincia = document.getElementById('provincia').value;
    var tipo = document.getElementById('tipo').value;

    var url = `http://localhost:5000/buscar?localidad=${localidad}&codigo_postal=${codigo_postal}&provincia=${provincia}&tipo=${tipo}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })  // Parse the response as JSON
        .then(data => {
            // Call the update function with the response data
            update(data);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function update(data) {

    // Get the table body element where rows will be added
    var tableBody = document.getElementById('resultsTable').getElementsByTagName('tbody')[0];

    // Clear any existing rows in the table
    tableBody.innerHTML = '';

    // Loop through the JSON response and add each row to the table
    data.forEach(item => {
        var row = tableBody.insertRow();

        var nameCell = row.insertCell(0);
        nameCell.textContent = item.nombre;

        var tipCell = row.insertCell(1);
        tipCell.textContent = item.tipo;

        var dirCell = row.insertCell(2);
        dirCell.textContent = item.direccion;
        
        var locCell = row.insertCell(3);
        locCell.textContent = item.localidad;

        var postCell = row.insertCell(4);
        postCell.textContent = item.codigo_postal;

        var provCell = row.insertCell(5);
        provCell.textContent = item.provincia;

        var desCell = row.insertCell(6);
        desCell.textContent = item.descripcion;

        var markerPosition = { lat: item.latitud , lng: item.longitud };
        var marker = new H.map.Marker(markerPosition);
        map.addObject(marker);

        // Create a speech bubble (InfoBubble) that will appear on hover
        var bubble = new H.ui.InfoBubble(markerPosition, {
            content: '<div class="bubble-content">'+item.nombre+'</div>'
        });

        ui.addBubble(bubble);

        marker.addEventListener('pointerenter', function () {
            bubble.open();
        });

        marker.addEventListener('pointerleave', function () {
            bubble.close();
        });
    });
}

function loadHEREApiScript(callback) {
    var script = document.createElement('script');
    script.src = 'https://js.api.here.com/v3/3.1/mapsjs-core.js';
    script.onload = function() {
        // Load additional script for events and UI
        var eventsScript = document.createElement('script');
        eventsScript.src = 'https://js.api.here.com/v3/3.1/mapsjs-mapevents.js';
        eventsScript.onload = function() {
            var uiScript = document.createElement('script');
            uiScript.src = 'https://js.api.here.com/v3/3.1/mapsjs-ui.js';
            uiScript.onload = callback;
            document.head.appendChild(uiScript);
        };
        document.head.appendChild(eventsScript);
    };
    document.head.appendChild(script);
}

// Ensure the HERE Maps API is loaded and ready
function initializeMap() {
    // Initialize the platform object with your HERE API credentials
    var platform = new H.service.Platform({
        apikey: 'MR12EWIiTrOwSWtbdzGMH68u35qrgH0-59fLrTzHN9k'  // Replace with your actual API key
    });

    // Get the default map layers from the platform
    var layers = platform.createDefaultLayers();


    // Initialize the map with a center point and zoom level
    var map = new H.Map(
        document.getElementById('mapContainer'),
        layers.vector.normal.map, {
            center: { lat: 40.4637, lng: -3.1492 }, // Coordinates of Spain
            zoom: 5.7
        }
    );
}

loadHEREApiScript(initializeMap());