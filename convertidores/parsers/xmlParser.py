import xml.etree.ElementTree as ET
import html
import json
import re

result = []
CLEANR = re.compile('<.*?>')

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

def execute(root):
    with open('datos/properly_formated.json', 'w', encoding='utf-8') as f:
        for monumento in root.iter('monumento'):
            coords = monumento.find('coordenadas')
            provincia = 'null'
            localidad = 'null'

            codpost = monumento.find('codigoPostal')
            if codpost is not None:
                codpost = codpost.text
            else:
                codpost = ""

            poblacion = monumento.find('poblacion')
            if poblacion is not None:
                localidad = poblacion.find('localidad').text
                provincia = poblacion.find('provincia').text
            else: 
                localidad = ""
                provincia = ""

            calle = monumento.find('calle')
            if calle is not None:
                calle = calle.text
            else: 
                calle = ""

            descripcion = monumento.find('Descripcion')
            if descripcion is not None :
                descripcion = findReplace(descripcion.text)
            else: 
                descripcion = ""

            tipo = monumento.find('tipoMonumento').text
            tip = typeCheck(tipo)    

            item = {
                "Monumento" : {
                    "nombre" : monumento.find('nombre').text,
                    "tipo" : tip,
                    "direccion" : calle,
                    "codigo_postal" : codpost,
                    "longitud" : coords.find('longitud').text,
                    "latitud" : coords.find('latitud').text,
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
    execute(root)

if __name__ == '__main__':
    main('datos/monumentos.xml')
