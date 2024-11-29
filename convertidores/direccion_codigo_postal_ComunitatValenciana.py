import http.client
import json
from urllib.parse import quote

API_KEY = "0de8b6c75c6048a382e50ff276c6ba90"

def direccion_codigo_postal(laLatitud, laLongitud, API_KEY):
    if not (laLatitud == "Error") and not (laLongitud == "Error") and not (API_KEY == ""):
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
                return "Error", "Error"
        except Exception as e:
            print(f"Error al procesar los datos: {e}")
            return "Error", "Error"
    else:
        return "Error", "Error"
