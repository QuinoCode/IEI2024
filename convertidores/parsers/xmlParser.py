import xml.etree.ElementTree as ET
import html
import json
import re

result = []
CLEANR = re.compile('<.*?>')

def retrieveDataFromAPI():
    url_destination = "http://localhost:5003"
    response = requests.get(url_destination)

    if (response.status_code == 200):
        return response.json()
    return {"error": "Something went wrong when fetching data from CLE API"}

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


def translate(root):
    result = []
    for monumento in root.findall('monumento'):
        datos_monumento = {}

        for element in monumento:
            if len(element):
                datos_monumento[element.tag] = extract_children(element)
            else:
                datos_monumento[element.tag] = element.text.strip()
        result.append(datos_monumento)
    print(result)
    return result

def extract_children(element):
    children_data = {}
    for child in element:
        # If a child has further children, call extract_children recursively
        if len(child):
            children_data[child.tag] = extract_children(child)
        else:
            children_data[child.tag] = child.text.strip() if child.text else ''
    return children_data

def execute(listCV):
    with open('datos/properly_formated.json', 'w', encoding='utf-8') as f:
        for monumento in listCV:
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
        json.dump(result, f, ensure_ascii=False, indent=4)

def findReplace(desc):
    cdatad = desc.replace('<![CDATA[', "")
    endtag = re.sub(CLEANR, '', cdatad)
    brack = endtag.replace(']]>', "")
    n = brack.replace('\n', "")
    return html.unescape(n)
    
def main(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    list = translate(root)
    execute(list)

if __name__ == '__main__':
    main('datos/entrega2/monumentos.xml')
