import requests
import json
import os

# Función para transformar el tipo basado en nombre y descripción
def transformar_tipo_con_parroquia(document_name, document_description):
    text = (document_name or "") + " " + (document_description or "")
    if "Yacimiento arqueológico" in text:
        return "Yacimiento arqueológico"
    elif "Iglesia" in text or "Ermita" in text or "Basílica" in text or "Catedral" in text or "Parroquia" in text:
        return "Iglesia-Ermita"
    elif "Monasterio" in text or "Convento" in text:
        return "Monasterio-Convento"
    elif "Castillo" in text or "Fortaleza" in text or "Torre" in text or "Palacio" in text:
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
        if int(codigo_postal) >= 53000:
            return None
        return codigo_postal
    except (ValueError, TypeError):
        return None  # Devuelve `None` si el código postal no es un número válido

# Función para transformar datos con validación y geocodificación
def transformar_datos_con_geocodificacion(datos_entrada):
    datos_transformados = []
    for item in datos_entrada:
        latitud = item.get("latwgs84")
        longitud = item.get("lonwgs84")
        direccion = coordenadas_a_direccion(latitud, longitud)
        codigo_postal = validar_codigo_postal(item.get("postalCode"))

        nuevo_item = {
            "Monumento": {
                "nombre": item.get("documentName", ""),
                "tipo": transformar_tipo_con_parroquia(item.get("documentName", ""), item.get("documentDescription", "")),
                "dirección": direccion,
                "codigo_postal": codigo_postal,
                "longitud": longitud,
                "latitud": latitud,
                "descripcion": item.get("documentDescription", "")
            },
            "Localidad": item.get("municipality", ""),
            "Provincia": item.get("territory", "")
        }
        print(json.dumps(nuevo_item, ensure_ascii=False, indent=4))  # Imprimir el item transformado
        datos_transformados.append(nuevo_item)
    return datos_transformados

# Ruta del archivo JSON de entrada y salida
archivo_entrada = "edificios.json"
archivo_salida = "edificios_transformados.json"

if __name__ == "__main__":
    if os.path.exists(archivo_entrada):
        # Cargar datos originales
        with open(archivo_entrada, "r", encoding="utf-8") as archivo:
            datos_originales = json.load(archivo)

        # Transformar los datos
        datos_transformados = transformar_datos_con_geocodificacion(datos_originales)

        # Guardar los datos transformados
        with open(archivo_salida, "w", encoding="utf-8") as archivo_salida_json:
            json.dump(datos_transformados, archivo_salida_json, ensure_ascii=False, indent=4)

        print(f"Transformación completada. Archivo generado: {archivo_salida}")
    else:
        print(f"Archivo {archivo_entrada} no encontrado.")
