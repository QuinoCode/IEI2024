from flask import Flask, jsonify, request
from APIs.busqueda.busqueda_service import *
api = Flask(__name__)

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
@api.post("/buscar")
def buscar_monumento():
    diccionario_respuesta = None
    data = request.get_json()
    localidad = data.get('localidad')
    codigo_postal = data.get('codigo_postal')
    provincia = data.get('provincia')
    tipo = data.get('tipo')
    diccionario_respuesta = query_database(localidad, codigo_postal, provincia, tipo)
    if not  diccionario_respuesta:
        return jsonify({"error": "No ha habido ningún resultado con esos parámetros"}), 404
    return jsonify(diccionario_respuesta), 200

# It's a post method since it has to wrapp the data inputted by the user in a json and get methods don't allow for a body
if __name__ == '__main__':
    api.run(debug=True, port=5000)