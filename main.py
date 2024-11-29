# este script recibe un data set con extension csv, xml o JSON y lo parsea a JSON para posteriormente introducirlo en la base de datos sqlite. 

# Checkear que tipo de parámetro se usa 
import sys
from convertidores.xmlParser import *
# from convertidores.transformar_geocodificacion import *

def identificar_tipo_de_datos(file):
    # Test if xml
    if (file.split('.')[-1] == "xml"):
        return "xml"
    if (file.split('.')[-1] == "csv"):
        return "csv"
    if (file.split('.')[-1] == "json"):
        return "json"
try: 
    file = sys.argv[1] # Si no tiene el argumento da un out of bounds exception
    tipo_de_datos = identificar_tipo_de_datos(file)
    print(tipo_de_datos)



except:
    print("No se ha proporcionado la ruta del archivo a tratar")


