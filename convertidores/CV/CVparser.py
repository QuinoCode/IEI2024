import json
import http.client
from urllib.parse import quote
from scrapper import Scrapper

API_KEY = "0de8b6c75c6048a382e50ff276c6ba90"

def direccion_codigo_postal(laLatitud, laLongitud, API_KEY):
    if not (laLatitud == "ERROR_404_NO_ENCONTRADO") and not (laLongitud == "ERROR_404_NO_ENCONTRADO") and not (API_KEY == ""):
        # Se prepara la consulta para la API de OpenCage
        conn = http.client.HTTPSConnection("api.opencagedata.com")
        query = f"/geocode/v1/json?q={quote(str(laLatitud))}+{quote(str(laLongitud))}&key={API_KEY}"
        conn.request("GET", query)
        
        # Obtener la respuesta
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()

        # Procesar la respuesta JSON
        try:
            parsed_data = json.loads(data)
            if parsed_data['results']:
                components = parsed_data['results'][0]['components']
                direccion = components.get('road', 'Desconocido') + ", " + components.get('city', 'Desconocido')
                codigo_postal = components.get('postcode', 'Desconocido')
                return direccion, codigo_postal
            else:
                return "ERROR_404_NO_ENCONTRADO", "ERROR_404_NO_ENCONTRADO"
        except Exception as e:
            print(f"Error al procesar los datos: {e}")
            return "ERROR_404_NO_ENCONTRADO", "ERROR_404_NO_ENCONTRADO"
    else:
        return "ERROR_404_NO_ENCONTRADO", "ERROR_404_NO_ENCONTRADO"

# Inicializar Scrapper
scrapper_instance = Scrapper()
scrapper_instance.stablish_connection_and_initialize_variables()
scrapper_instance.set_up_site()

# Cargar JSON
with open('data.json', 'r') as file:
    data = json.load(file)

# Procesar datos y añadir dirección y código postal
for wrapper in data:
    monument = wrapper["Monumento"]
    monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["longitud"], monument["latitud"])
    
    # Obtener dirección y código postal usando las coordenadas procesadas
    monument["direccion"], monument["codigo_postal"] = direccion_codigo_postal(monument["latitud"], monument["longitud"], API_KEY)

# Guardar el resultado en 'result.json'
with open('result.json', 'w') as file: 
    json.dump(data, file, indent=4)

# Cerrar el driver del scrapper
scrapper_instance.close_driver()
