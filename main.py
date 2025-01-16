# Este script recibe un data set con extension csv, xml o JSON y lo parsea a JSON para posteriormente introducirlo en la base de datos sqlite. 

# Checkear que tipo de parámetro se usa 
import os
import sys
import json
from subprocess import call
from convertidores.parsers import xmlParser
from convertidores.parsers import csvParser
from database import sql_create
from database.sql_create import * 
# from convertidores.transformar_geocodificacion import *

def identificar_tipo_de_datos(file):
    # Test if xml
    if (file.split('.')[-1] == "xml"):
        return "xml"
    if (file.split('.')[-1] == "csv"):
        return "csv"
    if (file.split('.')[-1] == "json"):
        return "json"

def convertir_datos_a_json(tipo):
    if (tipo == "xml"):
        convertir_xml_a_json(file)
    if (tipo == "csv"):
        convertir_csv_a_json(file)
    if (tipo == "json"):
        convertir_json_a_json(file)

def convertir_csv_a_json(file):
    csvParser.main(file)

def convertir_xml_a_json(file):
    xmlParser.main()

def convertir_json_a_json(file):
    call(["python3", "convertidores/parsers/transformar_geocodificacion.py", file])
    
try: 
    file = sys.argv[1] # Si no tiene el argumento da un out of bounds exception
    tipo_de_datos = identificar_tipo_de_datos(file)
    convertir_datos_a_json(tipo_de_datos)
    location_of_parsed_data = "./datos/properly_formated.json"

    file = open(location_of_parsed_data)
    data = json.load(file, encoding="utf-8")
    sql_manager = Sql_manager()

    sql_manager.main(data)
    
except Exception as exception:
    print("Algo ha sucedido, probablemente no se ha proporcionado la ruta del archivo a tratar ", exception)


