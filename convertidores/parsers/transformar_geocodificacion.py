import requests
import json
import os
import sys

def retrieveDataFromAPI():
    url_destination = "http://localhost:5004/getEUS"
    response = requests.get(url_destination)

    if (response.status_code == 200):
        return response.json()
    return {"error": "Something went wrong when fetching data from EUS API"}

# Función para transformar el tipo basado en nombre y descripción
def transformar_tipo_con_parroquia(document_name, document_description):
    text = (document_name or "") + " " + (document_description or "")
    if "Yacimiento arqueológico" in text:
        return "Yacimiento arqueológico"
    elif any(x in text for x in ["Iglesia", "Ermita", "Basílica", "Catedral", "Parroquia"]):
        return "Iglesia-Ermita"
    elif any(x in text for x in ["Monasterio", "Convento"]):
        return "Monasterio-Convento"
    elif any(x in text for x in ["Castillo", "Fortaleza", "Torre", "Palacio"]):
        return "Castillo-Fortaleza-Torre"
    elif "Edificio" in text:
        return "Edificio Singular"
    elif "Puente" in text:
        return "Puente"
    else:
        return "Otros"

# Función para geocodificar coordenadas usando Nominatim API
def coordenadas_a_direccion(latitud, longitud):
    if not latitud or not longitud:
        return None
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Dirección no encontrada")
    except Exception as e:
        print(f"Error al obtener dirección para lat: {latitud}, lon: {longitud}: {e}")
    return "Dirección no encontrada"

# Función para validar el código postal
def validar_codigo_postal(codigo_postal):
    try:
        cp_int = int(codigo_postal)
        if cp_int >= 53000:
            return None
        return codigo_postal
    except (ValueError, TypeError):
        return None

# Función para transformar datos con validación
def transformar_datos_con_geocodificacion(datos_entrada):
    datos_transformados = []
    for idx, item in enumerate(datos_entrada, start=1):
        latitud = item.get("latwgs84")
        longitud = item.get("lonwgs84")
        direccion = item.get("address", "")
        codigo_postal_original = item.get("postalCode")

        # Validar latitud y longitud
        if not latitud or not longitud:
            print(f"[WARN] Registro {idx}: Latitud o longitud no válida. Registro omitido.")
            continue

        # Validar código postal
        codigo_postal = validar_codigo_postal(codigo_postal_original)
        if codigo_postal is None and codigo_postal_original is not None:
            print(f"[WARN] Registro {idx}: Código postal inválido ('{codigo_postal_original}'). Registro omitido.")
            continue

        nuevo_item = {
            "Monumento": {
                "nombre": item.get("documentName", ""),
                "tipo": transformar_tipo_con_parroquia(item.get("documentName", ""), item.get("documentDescription", "")),
                "direccion": direccion,
                "codigo_postal": codigo_postal if codigo_postal is not None else "",
                "longitud": longitud,
                "latitud": latitud,
                "descripcion": item.get("documentDescription", "")
            },
            "Localidad": item.get("municipality", ""),
            "Provincia": item.get("territory", "")
        }

        datos_transformados.append(nuevo_item)
    return datos_transformados
def saveDataToFile():
    data = retrieveDataFromAPI()  # Llama a la función para obtener los datos
    file_path = "response_data.json"  # Nombre del archivo a crear
    
    with open(file_path, "w") as file:  # Abre el archivo en modo escritura
        json.dump(data, file, indent=4)  # Guarda los datos en formato JSON con sangría
    
    return file_path


def main():
    archivo_entrada = saveDataToFile() if len(sys.argv) < 2 else sys.argv[1]
    archivo_salida = "properly_formated.json"
    
    if os.path.exists(archivo_entrada):
        # Preprocesar el archivo para eliminar todas las apariciones vacías de 'address'
        with open(archivo_entrada, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Eliminar todas las apariciones de "address" : "",
        contenido = contenido.replace('"address" : "",', '')

        # Convertir el contenido modificado a JSON
        datos_originales = json.loads(contenido)

        # Transformar los datos
        datos_transformados = transformar_datos_con_geocodificacion(datos_originales)

        # Guardar los datos transformados en la misma carpeta que el script
        with open(archivo_salida, "w", encoding="utf-8") as archivo_salida_json:
            json.dump(datos_transformados, archivo_salida_json, ensure_ascii=False, indent=4)

        print(f"Transformación completada. Archivo generado: {archivo_salida}")
    else:
        print(f"Archivo {archivo_entrada} no encontrado.")


