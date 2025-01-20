import csv
from flask import Flask, Response, request, jsonify
import json  # Importa json para personalizar la respuesta

api = Flask(__name__)

CVlocation = 'datos/entrega2/bienes_inmuebles_interes_cultural.csv'

# Translation function to process CSV into a JSON
def csvToJson(csvFile):
    listCSV = []   
    with open(csvFile, encoding='utf-8') as csvf:
        # Define csv.reader with the correct delimiter
        csvRead = csv.reader(csvf, delimiter=';')
        next(csvRead)  # Skip the header row
        for row in csvRead:
            # Ensure the row has the expected number of fields to avoid IndexError
            if len(row) >= 10:
                item = {
                    "IGCPV": row[0],
                    "denominacion": row[1],
                    "provincia": row[2],
                    "municipio": row[3],
                    "UTMeste": row[4],
                    "UTMnorte": row[5],
                    "codclasificacion": row[6],
                    "clasificacion": row[7],
                    "codcategoria": row[8],
                    "categoria": row[9]
                }
                listCSV.append(item)
    return listCSV

# API route to process the CSV and return the JSON response
@api.get("/getCV")
def translate_api():
    try:
        result = csvToJson(CVlocation)
        # Usar json.dumps para evitar ensure_ascii=True y respetar los acentos
        response = Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

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
    api.run(debug=True, port=5002)
