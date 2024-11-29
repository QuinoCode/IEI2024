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

# Función para geocodificar coordenadas
def coordenadas_a_direccion(latitud, longitud):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        return datos.get("display_name", "Dirección no encontrada")
    else:
        return "Error al obtener la dirección"
        
def validar_codigo_postal(codigo_postal):
    try:
        if int(codigo_postal) >= 53000:
            return None
        return codigo_postal
    except (ValueError, TypeError):
        return None  # Devuelve `None` si el código postal no es un número válido
# Función para transformar datos con geocodificación
def transformar_datos_con_geocodificacion(datos_entrada):
    datos_transformados = []
    for item in datos_entrada:
        latitud = item.get("latwgs84")
        longitud = item.get("lonwgs84")
        direccion = ""
        if latitud and longitud:
            direccion = coordenadas_a_direccion(latitud, longitud)
        codigo_postal = validar_codigo_postal(item.get("postalCode"))

        
        nuevo_item = {
            "Monumento": {
                "nombre": item.get("documentName", ""),
                "tipo": transformar_tipo_con_parroquia(item.get("documentName", ""), item.get("documentDescription", "")),
                "dirección": direccion,
                "codigo_postal": item.get("postalCode", ""),
                "longitud": item.get("lonwgs84", ""),
                "latitud": item.get("latwgs84", ""),
                "descripcion": item.get("documentDescription", "")
            },
                "Localidad": item.get("municipality", "")
                "Pais": item.get("territory", "")
            
        }
        datos_transformados.append(nuevo_item)
    return datos_transformados

# Obtener la ruta del archivo JSON en la misma carpeta
archivo_entrada = "edificios.json"
archivo_salida = "edificios_transformados_con_geocodificacion.json"

# Leer los datos del archivo original
if os.path.exists(archivo_entrada):
    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        datos_originales = json.load(archivo)

    # Transformar los datos
    datos_transformados = transformar_datos_con_geocodificacion(datos_originales)

    # Guardar los datos transformados en un nuevo archivo
    with open(archivo_salida, "w", encoding="utf-8") as archivo_salida_json:
        json.dump(datos_transformados, archivo_salida_json, ensure_ascii=False, indent=4)

    print(f"Transformación completada. Archivo generado: {archivo_salida}")
else:
    print(f"Archivo {archivo_entrada} no encontrado.")
