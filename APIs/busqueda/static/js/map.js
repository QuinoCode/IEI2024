var map;
var markers = [];

//vaciar los campos del html
function cancelarBusqueda() {
    document.getElementById('localidad').value = "";
    document.getElementById('codigoPostal').value = "";
    document.getElementById('tipo').value = "";
    document.getElementById('provincia').value = "";
}

function realizarBusqueda() {
    //obtener datos
    var localidad = document.getElementById('localidad').value;
    var codigo_postal = document.getElementById('codigoPostal').value;
    var provincia = document.getElementById('provincia').value;
    var tipo = document.getElementById('tipo').value;

    var url = `http://localhost:5000/buscar?`;

    //si existen datos, los añade a url
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

    // Quitar las & del final
    if (url.endsWith('&')) {
        url = url.slice(0, -1);
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                //Si no da 200, limpia la tabla para indicar que no recibión datos
                clearTable();
                throw new Error('Network response was not ok');
            }
            return response.json();
        })  //Sigue con la respuesta como json
        .then(data => {
            //llamar a la funcion principal
            update(data);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

//función muerta para limpiar markers
function clearMarkers(){
    for(var i = 0; i < markers.length; i++){
        this.map.removeLayer(this.markers[i]);
    }
}

//lógica principal para mostrar la tabla en el html
function update(data) {
    //obtiene la tabla
    var tableBody = document.querySelector('#tablaResultados tbody');

    //Limpia la tabla de filas
    while (tableBody.firstChild){
        tableBody.removeChild(tableBody.firstChild);
    }

    //Usa el JSON para insertar filas nuevas con los datos recibidos
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

        //Crea un marker en el mapa Leaflet
        var marker = L.marker([latitude, longitude]).addTo(map);
        markers.push(marker);
    
        //Añade un popup con el nombre al marker
        marker.bindPopup(`<b>${item.nombre}</b>`).openPopup();
    });
}

function clearTable(){
    //obtiene la tabla
    var tableBody = document.querySelector('#tablaResultados tbody');

    //Limpia las filas de la tabla
    while (tableBody.firstChild){
        tableBody.removeChild(tableBody.firstChild);
    }
}

//Inicializa el mapa Leaflet
function initializeMap() {
    //Crea un mapa centrado en España
    map = L.map('mapContainer').setView([40.4637, -3.1492], 5.8);

    //Usa openstreetmap para visualizar el mapa
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

//Al llamar el script por primera vez, genera el mapa
initializeMap();
