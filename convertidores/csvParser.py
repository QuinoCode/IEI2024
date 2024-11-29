from convertidores.Scrapper.scrapper import *
from convertidores.CV.direccion_codigo_postal import *
import csv
import json
import sys
import time

csvFile = sys.argv[1]
destination = 'datos/CVdata.json'

def csvToJson():
    listCSV = []   
    with open(csvFile, encoding='utf-8') as csvf:
        csvRead = csv.DictReader(csvf)
        for row in csvRead:
            # IGCPV denominación provincia municipio UTMeste UTMnorte codclasificacion clasificacion codcategoria categoria
            campos = row.split(';')
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

def mappingTipo(json):
    pass

def mappingDescripcion(json):
    pass

def mappingsToJson(listCSV):
    jsonMapped = []
    for json in listCSV:
        item = {
            "Monumento" : {
                    "nombre" : json["denominacion"],
                    "tipo" : mappingTipo(json),
                    "direccion" : 'null',
                    "codigo_postal" : 'null',
                    "longitud" : json["UTMeste"],
                    "latitud" : json["UTMnorte"],
                    "descripcion" : mappingDescripcion(json)
                }, 
                "Localidad" : json["municipio"],
                "Provincia" : json["provincia"]
        }
        jsonMapped.append(item)
    return jsonMapped

# nombre tipo direccion codigo_postal longitud latitud descripcion, localidad provincia


def mappingCategoria():
    pass

def obtainCoordenatesFromScrapper(data):
    scrapper_instance = Scrapper()
    scrapper_instance.stablish_connection_and_initialize_variables()
    scrapper_instance.set_up_site()

    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["longitud"], monument["latitud"] = scrapper_instance.process_data(monument["longitud"], monument["latitud"])

    scrapper_instance.close()
    return data

def obtainPostalCodeAddress(data):
    for wrapper in data:
        monument = wrapper["Monumento"]
        monument["direccion"], monument["codigo_postal"] = direccion_codigo_postal(monument["longitud"], monument["latitud"])
        time.sleep(1)
    return data

def main():
    listCSV = csvToJson()
    jsonMapped = mappingsToJson(listCSV)
    jsonCoordenates = obtainCoordenatesFromScrapper(jsonMapped)
    jsonCodes = obtainPostalCodeAddress(jsonCoordenates)
    json.dump(jsonCodes, destination, ensure_ascii=False, indent=4)

