from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from APIs.carga.carga_service import cargar_dataset_service, borrar_almacen_service
from flask_cors import CORS
from carga import carga_service



api = Flask(__name__)
CORS(api)
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
@api.put("/carga")
def cargar_dataset():
    diccionario_respuesta = None
    diccionario_respuesta = cargar_dataset_service(request.get_json()) #importado base de datos
    if not  diccionario_respuesta:
        return jsonify({"error": "No hubo respuesta de la base de datos"}), 404
    print(f"Puerto carga reparados: \n {diccionario_respuesta["repaired_registers"]} \n")
    print(f"Puerto carga rechazados: \n {diccionario_respuesta["rejected_registers"]}\n")

    return jsonify(diccionario_respuesta), 200

@api.delete("/borrar")
def borrar_almacen():
    borrar_almacen_service() #importado base de datos
    return jsonify("{'holi': 1}") ,200
# It's a post method since it has to wrapp the data inputted by the user in a json and get methods don't allow for a body
if __name__ == '__main__':
    api.run(debug=True, port=5001)
