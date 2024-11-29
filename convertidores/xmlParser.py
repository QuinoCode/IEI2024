import xml.etree.ElementTree as ET
import json

# To modify - receiving any file
file = 'datos/monumentos.xml'
tree = ET.parse(file)
root = tree.getroot()
result = []

def typeCheck(tipo):
    answer = None
    if tipo in("Yacimientos arqueológicos","Puente") :
        return tipo
    elif tipo in ("Iglesias y Ermitas", "Catedrales", "Sinagogas"):
        answer = "Iglesia-Ermita"
    elif tipo in ("Monasterios", "Santuarios"):
        answer = "Monasterio-Convento"
    elif tipo in ("Castillos", "Casas Nobles", "Torres"):
        answer = "Castillo-Fortaleza-Torre"
    elif tipo in ("Reales Sitios","Palacio","Casa consistorial"):
        answer = "Edificio Singular"
    return answer

with open('datos/CLEdata.json', 'w', encoding='utf-8') as f:
    for monumento in root.iter('monumento'):
        coords = monumento.find('coordenadas')
        provincia = 'null'
        localidad = 'null'

        codpost = monumento.find('codigoPostal')
        if codpost is not None :
            codpost = codpost.text

        poblacion = monumento.find('poblacion')
        if poblacion is not None:
            localidad = poblacion.find('localidad').text
            provincia = poblacion.find('provincia').text

        calle = monumento.find('calle')
        if calle is not None :
            calle = calle.text

        descripcion = monumento.find('Descripcion')
        if descripcion is not None :
            descripcion = descripcion.text

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
