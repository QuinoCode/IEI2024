import csv
import json
from CV_JsonAPI import convertir_csv_a_json
from CV_GeoAPI import direccion_codigo_postal
from convertidores.Scrapper.scrapper import Scrapper
from convertidores.parsers.direccion_codigo_postal import *

import http.client
from urllib.parse import quote

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
            return ""

def mappingCategoria(json):
    if json.get("CATEGORIA", "") == "":
        return convertCodCategoria(json.get("CODCATEGORIA", ""))
    
    return json.get("CATEGORIA", "")

def mappingClasificacion(json):
    if json.get("CLASIFICACION", "") == "":
        return convertCodClasificacion(json.get("CODCLASIFICACION", ""))
    return json.get("CLASIFICACION", "")

def mappingTipo(json):
    denominacion = json.get("DENOMINACION", "").lower()
    categoria = mappingCategoria(json)
    clasificacion = mappingClasificacion(json)

    if denominacion == "" or categoria == "" or clasificacion == "":
        return None

    if categoria == "Zona arqueológica" or categoria == "Zona paleontológica":
        return "Yacimiento arqueológico"
    
    if "puente" in denominacion:
        return "Puente"
    
    if any(type in denominacion for type in ["torre", "castillo", "castellet", "castell", "fortaleza"]):
        return "Castillo-Fortaleza-Torre"

    if any(type in denominacion for type in ["escudo", "emblema"]) or clasificacion == "Archivo" or denominacion.startswith("casa") or denominacion.startswith("cruz"):
        return "Edificio Singular"

    if "iglesia" in denominacion:
        return "Iglesia-Ermita"

    return "Otros"

def mappingDescripcion(json):
    categoria = mappingCategoria(json)
    clasificacion = mappingClasificacion(json)
    if categoria != "" and clasificacion != "":
        return "'" + (categoria + " - " + clasificacion).replace('"', "") + "'"
    elif categoria != "":
        return categoria
    elif clasificacion != "":
        return clasificacion
    return None

def mappingProvincia(json):
    provincia = json.get("PROVINCIA", "")
    match provincia:
        case "CASTELLON":
            return "CASTELLÓN"
        case "CASTELLÓ":
            return "CASTELLÓN"
        case "ALACANT":
            return "ALICANTE"
        case "VALÈNCIA":
            return "VALENCIA"
        case "CASTELLÓN":
            return "CASTELLÓN"
        case "ALICANTE":
            return "ALICANTE"
        case "VALENCIA":
            return "VALENCIA"
        case _:
            return None

def mappingsToJson(listCSV):
    jsonMapped = []
    for json in listCSV:
        item = {
            "Monumento": {
                "nombre": json.get("DENOMINACION", "").replace('"', ""),
                "tipo": mappingTipo(json),
                "direccion": None,
                "codigo_postal": None,
                "longitud": json.get("UTMESTE", "").replace("\"", ""),
                "latitud": json.get("UTMNORTE", "").replace("\"", ""),
                "descripcion": mappingDescripcion(json)
            }, 
            "Localidad": json.get("MUNICIPIO", ""),
            "Provincia": mappingProvincia(json)
        }
        jsonMapped.append(item)
    return jsonMapped

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
        monument["direccion"], monument["codigo_postal"] = direccion_codigo_postal(monument["latitud"], monument["longitud"])
    return data

def obtainValidatedCodePostal(data):
    for wrapper in data:
        monument = wrapper["Monumento"]
        codigo_postal = monument["codigo_postal"]
        if codigo_postal is not None:
            try:
                if int(codigo_postal) >= 53000:
                    monument["codigo_postal"] = None
            except Exception as e:
                monument["codigo_postal"] = None

    return data

def write(data, path_out):
    if not isinstance(data, (list, dict)):
        raise ValueError("Los datos no son válidos para escribir en el archivo.")
    
    with open(path_out, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main(csv_origen, csvConverted_out, json_out):
    jsonConverted = convertir_csv_a_json(csv_origen, csvConverted_out)
    jsonMapped = mappingsToJson(jsonConverted)
    jsonCoordenates = obtainCoordenatesFromScrapper(jsonMapped)
    jsonAddress = obtainPostalCodeAddress(jsonCoordenates)
    jsonPostalCode = obtainValidatedCodePostal(jsonAddress)
    write(jsonPostalCode, json_out)
