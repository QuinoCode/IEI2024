import requests
import json
from database.sql_create import * 

def retrieveDataFromAPI():
    """
    Realiza una solicitud GET al endpoint /getEUS y devuelve los datos en formato JSON.
    """
    url_destination = "http://localhost:5004/getEUS"
    try:
        response = requests.get(url_destination)
        if response.status_code == 200:
            return response.text
        print(f"[ERROR] Error {response.status_code}: {response.text}")
        return []
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al API: {e}")
        return []

def mappingTipo(item):
    """
    Mapea el tipo de monumento basado en las reglas definidas previamente.
    """
    text = (item.get("documentName", "") + " " + item.get("documentDescription", "")).lower()
    if "yacimiento arqueológico" in text:
        return "Yacimiento arqueológico"
    elif any(keyword in text for keyword in ["iglesia", "ermita", "basílica", "catedral", "parroquia"]):
        return "Iglesia-Ermita"
    elif any(keyword in text for keyword in ["monasterio", "convento"]):
        return "Monasterio-Convento"
    elif any(keyword in text for keyword in ["castillo", "fortaleza", "torre", "palacio", "fuerte"]):
        return "Castillo-Fortaleza-Torre"
    elif any(keyword in text for keyword in ["edificio", "teatro", "molino"]):
        return "Edificio singular"
    elif "puente" in text:
        return "Puente"
    else:
        return "Otros"

def main():
    """
    Función principal que procesa los datos de entrada, realiza validaciones, y genera un archivo de salida.
    """
    # Determina el archivo de entrada
    unfiltered_data_string = retrieveDataFromAPI()  # Llama a la función para obtener los datos
    unfiltered_data_string = unfiltered_data_string.encode('utf-8').decode('utf-8')
    # Eliminar registros con "address": "" y procesar
    unfiltered_data_string = unfiltered_data_string.replace('"address" : "",', '')
    filtered_data = json.loads(unfiltered_data_string)
    properly_formatted_json = []

    # Separar registros válidos, reparados y rechazados

    for item in filtered_data:
        nombre = item.get("documentName", "Sin nombre")
        latitud = item.get("latwgs84")
        longitud = item.get("lonwgs84")
        codigo_postal = item.get("postalCode")

        properly_formatted_json.append({
            "Monumento": {
                "tipo": mappingTipo(item),
                "nombre": nombre,
                "direccion": item.get("address", ""),
                "codigo_postal": codigo_postal,
                "longitud": longitud,
                "latitud": latitud,
                "descripcion": item.get("documentDescription", "")
            },
            "Localidad": item.get("municipality", ""),
            "Provincia": item.get("territory", "")
        })


    sql_manager = Sql_manager()

    feedback_resulsts = sql_manager.main(properly_formatted_json, "edificios.json")
    # Resultado final
    return feedback_resulsts

if __name__ == "__main__":
    resultado = main()
    if resultado:
        print(json.dumps(resultado, ensure_ascii=False, indent=4))

