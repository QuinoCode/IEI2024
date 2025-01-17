import xml.etree.ElementTree as ET
import html
import json
import re
import requests
from database.sql_create import * 

result = []
CLEANR = re.compile('<.*?>')

# Función que realiza petición al API
def retrieveDataFromAPI():
    url_destination = "http://localhost:5003/getCLE"
    response = requests.get(url_destination)

    #Si encuentra el elemento del API, devuelve un json de la respuesta del API
    if (response.status_code == 200):
        print("API response correct")
        return response.json()
    return {"error": "Something went wrong when fetching data from CLE API"}


#Función responsable de la conversión de tipos de monumento
def typeCheck(tipo):
    answer = None
    if tipo in("Yacimientos arqueológicos") :
        return tipo
    elif tipo in ("Puentes","Puente"):
        answer = "Puente"
    elif tipo in ("Iglesias y Ermitas", "Catedrales", "Sinagogas"):
        answer = "Iglesia-Ermita"
    elif tipo in ("Monasterios", "Santuarios"):
        answer = "Monasterio-Convento"
    elif tipo in ("Castillos", "Casas Nobles", "Torres"):
        answer = "Castillo-Fortaleza-Torre"
    elif tipo in ("Reales Sitios","Palacio", "Palacios","Casa consistorial"):
        answer = "Edificio Singular"
    else:
        answer = "Otros"
    return answer

#Función principal que genera el json final
def execute(response):
    with open('datos/properly_formated.json', 'w', encoding='utf-8') as f:
        for monumento in response:
            #obtenemos los datos del json respuesta
            nombre = monumento["nombre"]

            coords = monumento["coordenadas"]
            latitud = coords["latitud"]
            longitud = coords["longitud"]

            codpost = monumento.get("codigoPostal", "")

            poblacion = monumento["poblacion"]
            if poblacion is not None:
                localidad = poblacion['localidad']
                provincia = poblacion['provincia']

            calle = monumento.get("calle", "")

            descripcion = monumento["Descripcion"]
            if descripcion is not None :
                descripcion = findReplace(descripcion)
            else: 
                descripcion = ""

            tipo = monumento["tipoMonumento"]
            tip = typeCheck(tipo)    

            #generamos un objeto para guardar en el json formateado
            item = {
                "Monumento" : {
                    "nombre" : nombre,
                    "tipo" : tip,
                    "direccion" : calle,
                    "codigo_postal" : codpost,
                    "longitud" : longitud,
                    "latitud" : latitud,
                    "descripcion" : descripcion
                }, 
                "Localidad" : localidad,
                "Provincia" : provincia
            }
            result.append(item)
        #al terminar el bucle, se guarda la lista generada como json
        json.dump(result, f, ensure_ascii=True, indent=4)

#Función para limpiar el código de elementos XML. Usa un CLEANR para los tags, y replaces para cdata y saltos de línea
def findReplace(desc):
    cdatad = desc.replace('<![CDATA[', "")
    endtag = re.sub(CLEANR, '', cdatad)
    brack = endtag.replace(']]>', "")
    n = brack.replace('\n', "")
    return html.unescape(n)
    
#Main busca la respuesta para poder ejecutar el resto del código.
def main():
    response = retrieveDataFromAPI()
    execute(response)

    file = open('datos/properly_formated.json')
    data = json.load(file)
    sql_manager = Sql_manager()

    sql_manager.main(data,response)

if __name__ == '__main__':
    main()