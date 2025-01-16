import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request

api = Flask(__name__)
CLElocation = 'datos/entrega2/monumentos.xml'

# Metodo post de ejemplo para que copieis la estructura de como funciona 
@api.post("/prueba") #URL que "escucha"
def metodo_post_ejemplo():
    # Cómo es un método post recibe un JSON
    data = request.get_json() #recuperamos el JSON
    # El json es así { "name": "Nombre introducido por el usuario"}
    name = data.get('name')
    print(name) #Para que lo muestre por consola
    return jsonify({"received_name": name}), 200 
    #Cuando devolvemos la respuesta casi siempre tiene que ser un json, usamos jsonify sobre un mapa de python con formato de JSON (casi son lo mismo)

def extract_children(element):
    """Helper function to extract child elements as a dictionary."""
    children_data = {}
    for child in element:
        # If a child has further children, call extract_children recursively
        if len(child):
            children_data[child.tag] = extract_children(child)
        else:
            children_data[child.tag] = child.text.strip() if child.text else ''
    return children_data

# Translation function to process XML into a structured dictionary
def translate(root):
    result = []
    
    for monumento in root.findall('monumento'):
        datos_monumento = {}

        for element in monumento:
            # Check if the element has children
            if len(element):
                datos_monumento[element.tag] = extract_children(element)
            else:
                datos_monumento[element.tag] = element.text.strip() if element.text else ''
        
        result.append(datos_monumento)
    return result

# API route to process the XML and return the JSON response
@api.get("/getCLE")
def translate_api():
    try:
        tree = ET.parse(CLElocation)
        root = tree.getroot()
        result = translate(root)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
Además de devolver el json devolvemos el status code de HTTP
------------------------------------------------------------
200 OK – Petición correcta.
201 Created - Recurso creado satisfactoriamente.
400 Bad Request - El cliente envio una petición incorrecta
401 Unauthorized - El cliente no pasó el proceso de autenticación (no vamos a tener así que nos da igual)
403 Forbidden - El cliente no tiene permitido el acceso a ese recurso/endpoint (si está autenticado pero con ese nivel no puede acceder).
404 Not Found - El recurso solicitado no existe.
500 Internal Server Error - El procesado interno de los datos ha fallado (una excepción o algo rompe el programa)
"""
if __name__ == '__main__':
    api.run(debug=True, port=5003)
