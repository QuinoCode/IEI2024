from flask import Flask, jsonify, request
from flask_cors import CORS
from APIs.busqueda.busqueda_service import *
api = Flask(__name__)
CORS(api)
# Metodo put de ejemplo para que copieis la estructura de como funciona 
"""
Además de devolver el json devolvemos el status code de HTTP
------------------------------------------------------------
200 OK - Petición correcta.
201 Created - Recurso creado satisfactoriamente.
400 Bad Request - El cliente envio una petición incorrecta
401 Unauthorized - El cliente no pasó el proceso de autenticación (no vamos a tener así que nos da igual)
403 Forbidden - El cliente no tiene permitido el acceso a ese recurso/endpoint (si está autenticado pero con ese nivel no puede acceder).
404 Not Found - El recurso solicitado no existe.
500 Internal Server Error - El procesado interno de los datos ha fallado (una excepción o algo rompe el programa)
"""
# Se ha seleccionado PUT debida a la idempotencia del método. Varias llamadas con los mismos parámetros dejan el recurso en el mismo estado, POST no lo conseguiría
#Se espera una petición del estilo (/buscar?localidad=Requena&codigo_postal=46340&provincia=Valencia&tipo=Puente)
@api.get("/buscar")
def buscar_monumento():
    diccionario_respuesta = query_database(request)
    if not  diccionario_respuesta:
        return jsonify({"error": "No ha habido ningún resultado con esos parámetros"}), 404
    return jsonify(diccionario_respuesta), 200

# It's a post method since it has to wrapp the data inputted by the user in a json and get methods don't allow for a body
if __name__ == '__main__':
    api.run(debug=True, port=5000)
