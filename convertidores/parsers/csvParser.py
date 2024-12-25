import csv
import json
import time
from CV_JsonAPI import convertir_csv_a_json
from CV_GeoAPI import direccion_codigo_postal
from convertidores.Scrapper.scrapper import Scrapper
from convertidores.parsers.direccion_codigo_postal import *

import http.client
from urllib.parse import quote

destination = 'datos/properly_formated.json'

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
    match codClasificacion:
        case "1":
            return "Bienes inmuebles 1ª"
        case "2":
            return "Bienes muebles 1ª"
        case _:
            return ""

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

def mappingProvincia(json):
    provincia = json.get("provincia", "")
    match provincia:
        case "CASTELLON":
            return "CASTELLÓN"
        case "ALIGANTE":
            return "ALICANTE"
        case "ALACANT":
            return "ALICANTE"
        case "VALÈNCIA":
            return "VALENCIA"
        case _:
            return provincia

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
                "Provincia" : mappingProvincia(json)
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
    api_key = '0de8b6c75c6048a382e50ff276c6ba90'
    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["direccion"], monument["codigo_postal"] = direccion_codigo_postal(monument["latitud"], monument["longitud"], api_key)
    return data

def obtainValidatedCodePostal(data):
    # Recorre cada elemento en los datos
    for wrapper in data:
        monument = wrapper["Monumento"]
        
        # Obtiene el codigo_postal
        codigo_postal = monument["codigo_postal"]

        # Verifica si es no nulo
        if codigo_postal is not None:

            # Comprueba si es valido
                try:
                    if int(codigo_postal) >= 53000:
                        # Asigna como no valido el codigo_postal
                        monument["codigo_postal"] = None
                except Excepton as e:
                    print(f"Error al validar el código postal: {codigo_postal}: {e}")

    return data

def main(csvFile):
    listCSV = csvToJson(csvFile)
    jsonMapped = mappingsToJson(listCSV)
    jsonCoordenates = obtainCoordenatesFromScrapper(jsonMapped)
    jsonAddress = obtainPostalCodeAddress(jsonCoordenates)
    jsonCodes = obtainValidatedCodePostal(jsonAddress)
    with open(destination,'w') as f:
        json.dump(jsonCodes, f, ensure_ascii=False, indent=4)
        # json.dump(jsonCoordenates, f, ensure_ascii=False, indent=4)
    return destination
