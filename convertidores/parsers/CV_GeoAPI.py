import time
import http.client
import json
from urllib.parse import urlencode

def direccion_codigo_postal(laLatitud, laLongitud, API_KEY):
    direccion = None
    codigo_postal = None

    if laLatitud != "Error" and laLongitud != "Error" and API_KEY:
        time.sleep(2)
        try:
            query_params = {
                "q": f"{laLatitud},{laLongitud}",
                "key": API_KEY
            }
            query = f"/geocode/v1/json?{urlencode(query_params)}"

            conn = http.client.HTTPSConnection("api.opencagedata.com")
            try:
                conn.request("GET", query)
                response = conn.getresponse()

                if response.status != 200:
                    raise Exception(f"Error en la respuesta de la API: {response.status} {response.reason}")

                data = response.read().decode("utf-8")
                parsed_data = json.loads(data)

                if 'results' in parsed_data and parsed_data['results']:
                    components = parsed_data['results'][0].get('components', {})
                    calle = components.get('road', None)
                    ciudad = components.get('city', None)
                    codigo_postal = components.get('postcode', None)

                    if calle and ciudad:
                        direccion = f"{calle}, {ciudad}"
                    elif calle:
                        direccion = f"{calle}, CIUDAD DESCONOCIDA"
                    elif ciudad:
                        direccion = ciudad
            finally:
                conn.close()
        except Exception as e:
            print(f"Error al procesar los datos: {e}")

    return direccion, codigo_postal