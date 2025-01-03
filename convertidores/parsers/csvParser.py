import csv
import requests
import json
import time
from convertidores.Scrapper.scrapper import Scrapper
from convertidores.parsers.direccion_codigo_postal import *

import http.client
from urllib.parse import quote
from urllib.parse import urlencode

destination = 'datos/properly_formated.json'
def retrieveDataFromAPI():
    url_destination = "http://localhost:5002"
    response = requests.get(url_destination)

    if (response.status_code == 200):
        return response.json()
    return {"error": "Something went wrong when fetching data from CV API"}

def csvToJson(csvFile):
    listCSV = []   
    with open(csvFile, encoding='utf-8') as csvf:
        csvRead = csv.reader(csvf)
        next(csvRead)
        for row in  csvRead:
            # IGCPV denominación provincia municipio UTMeste UTMnorte codclasificacion clasificacion codcategoria categoria
            campos = row[0].split(';')
            item = {
                "IGCPV": campos[0],
                "denominacion": campos[1],
                "provincia": campos[2],
                "municipio": campos[3],
                "UTMeste": campos[4],
                "UTMnorte": campos[5],
                "codclasificacion": campos[6],
                "clasificacion": campos[7],
                "codcategoria": campos[8],
                "categoria": campos[9]
            }
            listCSV.append(item)
    return listCSV

def convertCodClasificacion(codClasificacion):
    if codClasificacion is None:
        return None
    
    if codClasificacion == "1":
        return "Bienes inmuebles 1ª"
    
    return "Bienes muebles 1ª"

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

def mappingCategoria(json):
    if json["categoria"] is None:
        return convertCodCategoria(json["codcategoria"])
    
    return json["categoria"]

def mappingClasificacion(json):
    if json["clasificacion"] is None:
        return convertCodClasificacion(json["codclasificacion"])
    
    return json["clasificacion"]

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

def mappingDescripcion(json):
    categoria = mappingCategoria(json)
    clasificacion = mappingClasificacion(json)
    if (categoria is not None and clasificacion is not None):
        return "'"+ (categoria + " - " + clasificacion).replace('"', "") +"'"
    return None

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

# nombre tipo direccion codigo_postal longitud latitud descripcion, localidad provincia

def obtainCoordenatesFromScrapper(data):
    scrapper_instance = Scrapper()
    scrapper_instance.stablish_connection_and_initialize_variables()
    scrapper_instance.set_up_site()

    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["longitud"], monument["latitud"])

    scrapper_instance.close_driver()
    return data

def obtainPostalCodeAddress(data):
    for wrapper in data:
        monument = wrapper["Monumento"]
        API_KEY = "06a875f723d14e6798dadfb93eced894"
        if monument["latitud"] != "Error" and monument["longitud"] != "Error":
            time.sleep(1)
            try:
                query_params = {
                    "q": f"{monument["latitud"]},{monument["longitud"]}",
                    "key": API_KEY
                }
                query = f"/geocode/v1/json?{urlencode(query_params)}"
            
                with http.client.HTTPSConnection("api.opencagedata.com") as conn:
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
                        monument["codigo_postal"] = components.get('postcode', None)
                    
                        if calle and ciudad:
                            monument["direccion"] = f"{calle}, {ciudad}"
                        elif calle:
                            monument["direccion"] = f"{calle}, CIUDAD DESCONOCIDA"
                        elif ciudad:
                            monument["direccion"] = ciudad
            except Exception as e:
                print(f"Error al procesar los datos: {e}")
    return data

def main(csvFile):
    listCSV = csvToJson(csvFile)
    jsonMapped = mappingsToJson(listCSV)
    jsonCoordenates = obtainCoordenatesFromScrapper(jsonMapped)
    # jsonCodes = obtainPostalCodeAddress(jsonCoordenates)
    with open(destination,'w') as f:
        # json.dump(jsonCodes, f, ensure_ascii=False, indent=4)
        json.dump(jsonCoordenates, f, ensure_ascii=False, indent=4)
    return destination
