import csv
import requests
import json
import time
from convertidores.Scrapper.scrapper import Scrapper
# from convertidores.parsers.direccion_codigo_postal import *

from database.sql_create import * 
from urllib.parse import quote
from urllib.parse import urlencode

destination = 'datos/properly_formated.json'
def retrieveDataFromAPI():
    url_destination = "http://localhost:5002/getCV"
    response = requests.get(url_destination)

    if (response.status_code == 200):
        return response.json()
    return {"error": response}

# Obtener la clasificación a traves de codClasificacion
def convertCodClasificacion(codClasificacion):
    if codClasificacion is None:
        return None
    
    if codClasificacion == "1":
        return "Bienes inmuebles 1ª"
    
    return "Bienes muebles 1ª"

# Obtener la categoría a traves de codCategoria
def convertCodCategoria(codCategoria):
    match codCategoria:
        case "1":
            return "Conjunto histórico"
        case "2":
            return "Sitio histórico"
        case "3":
            return "Jardín histórico"
        case "4":
            return "Monumento"
        case "5":
            return "Zona arqueológica"
        case "6":
            return "Archivo"
        case "7":
            return "Zona paleontológica"
        case "8":
            return "Espacio etnológico"
        case "9":
            return "Parque cultural"
        case "11":
            return "Monumento de interés local"
        case "18":
            return "Individual (mueble)"
        case "20":
            return "Fondo de museo (primera)"
        case _:
            return None

# Obtener la categoria del monumento
def mappingCategoria(json):
    if json["categoria"] is None:
        return convertCodCategoria(json["codcategoria"])
    
    return json["categoria"]

# Obtner la clasificacion del monumento
def mappingClasificacion(json):
    if json["clasificacion"] is None:
        return convertCodClasificacion(json["codclasificacion"])
    
    return json["clasificacion"]

# Obtner el tipo del monumento a partir de la denominacion, categoria y clasificacion del monumento
def mappingTipo (json):
    denominacion = json["denominacion"].lower()
    categoria = mappingCategoria(json)
    clasificacion = mappingClasificacion(json)

    if denominacion is None or categoria is None or clasificacion is None:
        return None

    if categoria == "Zona arqueológica" or categoria == "Zona paleontológica":
        return "Yacimiento arqueológico"
    
    if "puente" in denominacion:
        return "Puente"
    
    if any(type in denominacion for type in ["torre","castillo","castellet","castell","fortaleza"]):
        return "Castillo-Fortaleza-Torre"

    if any(type in denominacion for type in ["escudo","emblema"]) or clasificacion == "Archiva" or denominacion.startswith("casa") or denominacion.startswith("cruz"):
        return "Edificio Singular"

    if "iglesia" in denominacion:
        return "Iglesia-Ermita"

    return "Otros"

# Obtener la descripcion del monumento a partir de la categoria y clasificacion del monumento
def mappingDescripcion(json):
    categoria = mappingCategoria(json)
    clasificacion = mappingClasificacion(json)
    if (categoria is not None and clasificacion is not None):
        return "'"+ (categoria + " - " + clasificacion).replace('"', "") +"'"
    return None

# Generar un JSON con el esquema global a partir del CSV convertido en JSON
def mappingsToJson(listCSV):
    jsonMapped = []
    for json in listCSV:
        item = {
            "Monumento" : {
                    "nombre" : json["denominacion"].replace('"',""),
                    "tipo" : mappingTipo(json),
                    "direccion" : 'null',
                    "codigo_postal" : 'null',
                    "longitud" : json["UTMeste"].replace("\"", ""),
                    "latitud" : json["UTMnorte"].replace("\"",""),
                    "descripcion" : mappingDescripcion(json)
                }, 
                "Localidad" : json["municipio"],
                "Provincia" : json["provincia"]
        }
        jsonMapped.append(item)
    return jsonMapped

# Generar JSON con las coordenadas reales de latitud y longitud
def obtainCoordenatesFromScrapper(data):
    scrapper_instance = Scrapper()
    scrapper_instance.stablish_connection_and_initialize_variables()
    scrapper_instance.set_up_site()

    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["latitud"], monument["longitud"])

    scrapper_instance.close_driver()
    return data

# Obtener direccion y codigo postal a partir de longitud y latitud
def direccion_codigo_postal(latitud, longitud):
    direccion = None
    postcode = None

    if latitud != "ERROR" and longitud != "ERROR":
        time.sleep(1)

        # Define la URL base
        url = f"https://us1.locationiq.com/v1/reverse?key=pk.6fec0eca34494199b1038a312bddbb33&lat={latitud}&lon={longitud}&format=json"

        try:
            # Realiza la solicitud GET
            response = requests.get(url)

            # Convierte la respuesta a un diccionario
            data = response.json()
    
            # Extraer la calle
            road = data.get("address", {}).get("road", "")
            direccion = road
            if not road:
                square = data.get("address", {}).get("square", "")
                suburb = data.get("address", {}).get("suburb", "")
                direccion = square + suburb


            # Extraer el número de vivienda
            house_number = data.get("address", {}).get("house_number", "")

            # Generar la direccion a partir de la calle y el número de vivienda
            if house_number:
                direccion += f", {house_number}"

            # Extrae el codigo postal
            postcode = data.get("address", {}).get("postcode", "")
            if not postcode:
                city = data.get("address", {}).get("city", "")
                town = data.get("address", {}).get("town", "")
                if town:
                    postcode = alternativePostalCode(town)
                else:
                    postcode = alternativePostalCode(city)


        # Imprimir los datos de entrada para saber si se han generado la direccion y el código postal
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")

    print(f"lat:{latitud} lon:{longitud} -> direccion:{direccion} - postcode:{postcode}")
    return direccion, postcode

def alternativePostalCode(placename):
    postalCode = ""
    uncomplete_url_api = "http://api.geonames.org/postalCodeSearchJSON?placename=&maxRows=1&username=QuinoCode"
    url_api = uncomplete_url_api.replace('placename=', f'placename={placename}')
    try:
        response_api = requests.get(url_api)
        data = response_api.json()
        if not data.get("status"):
            postalCode = data.get('postalCodes')[0].get("postalCode")
    except:
        print(f"Error al realizar la solicitud:")
    return postalCode



# Generar JSON con direccion y código postal a partir de la latitud y longitud
def obtainPostalCodeAddress(data):
    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["direccion"], monument["codigo_postal"] = direccion_codigo_postal(monument["latitud"], monument["longitud"])
    return data

def main():
    listCSV = retrieveDataFromAPI()
    jsonMapped = mappingsToJson(listCSV)
    jsonCoordenates = obtainCoordenatesFromScrapper(jsonMapped)
    jsonCodes = obtainPostalCodeAddress(jsonCoordenates)
    with open(destination,'w', encoding='utf-8') as f:
        json.dump(jsonCodes, f, ensure_ascii=False, indent=4)
        # json.dump(jsonCoordenates, f, ensure_ascii=False, indent=4)
    sql_manager = Sql_manager()
    response_feedback = sql_manager.main(jsonCodes, "bienes_inmuebles_interes_cultural.csv")

    return response_feedback
