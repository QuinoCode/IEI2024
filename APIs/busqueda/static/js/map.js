var map;
var markers = [];

function cancelarBusqueda() {
    console.log("cancelar");
}

function realizarBusqueda() {
    var localidad = document.getElementById('localidad').value;
    var codigo_postal = document.getElementById('codigoPostal').value;
    var provincia = document.getElementById('provincia').value;
    var tipo = document.getElementById('tipo').value;

    var url = `http://localhost:5000/buscar?`;

    if (localidad) {
        url += `localidad=${encodeURIComponent(localidad)}&`;
    }
    if (codigo_postal) {
        url += `codigo_postal=${encodeURIComponent(codigo_postal)}&`;
    }
    if (provincia) {
        url += `provincia=${encodeURIComponent(provincia.toUpperCase())}&`;
    }
    if (tipo != "") {
        url += `tipo=${encodeURIComponent(tipo)}&`;
    }

    // Remove the trailing '&' if it exists
    if (url.endsWith('&')) {
        url = url.slice(0, -1);
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })  // Parse the response as JSON
        .then(data => {
            clearMarkers();
            // Call the update function with the response data
            update(data);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function clearMarkers(){
    for(var i = 0; i < markers.length; i++){
        this.map.removeLayer(this.markers[i]);
    }
}

function update(data) {
    // Get the table body element where rows will be added
    var tableBody = document.getElementById('tablaResultados').getElementsByTagName('tbody')[0];

    // Clear any existing rows in the table
    tableBody.innerHTML = '';

    // Loop through the JSON response and add each row to the table
    data.forEach(item => {
        console.log(item)
        var row = tableBody.insertRow();

        var nameCell = row.insertCell(0);
        nameCell.textContent = item.nombre;

        var tipCell = row.insertCell(1);
        tipCell.textContent = item.tipo;

        var dirCell = row.insertCell(2);
        dirCell.textContent = item.direccion;

        var locCell = row.insertCell(3);
        locCell.textContent = item.en_localidad;

        var postCell = row.insertCell(4);
        postCell.textContent = item.codigo_postal;

        var provCell = row.insertCell(5);
        provCell.textContent = item.en_provincia;

        var desCell = row.insertCell(6);
        desCell.textContent = item.descripcion;

        var latitude = parseFloat(item.latitud);
        var longitude = parseFloat(item.longitud);

        // Create a marker at the specified latitude and longitude
        var marker = L.marker([latitude, longitude]).addTo(map);
        markers.push(marker);
    
        // Add a popup to the marker that shows the name of the item
        marker.bindPopup(`<b>${item.nombre}</b>`).openPopup();
    });
}


// Initialize Leaflet map
function initializeMap() {
    // Create a Leaflet map centered in Spain (40.4637, -3.1492)
    map = L.map('mapContainer').setView([40.4637, -3.1492], 5.8);

    // Add OpenStreetMap tile layer to the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

// Call the Leaflet map initialization
initializeMap();
