from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS
api = Flask(__name__)
CORS(api)
INPUT_FILE = "edificios.json"
OUTPUT_FILE = "datos/properly_formated.json"

@api.route("/getEUS", methods=['GET'])
def get_eus():
    """Endpoint para devolver el contenido del archivo edificios.json."""
    try:
        if not os.path.exists(INPUT_FILE):
            return jsonify({"error": f"Archivo {INPUT_FILE} no encontrado."}), 404

        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            contenido = json.load(f)
        
        return jsonify(contenido), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"}), 500

@api.route("/health", methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio."""
    return jsonify({"status": "healthy", "service": "EUS Monuments API"}), 200

@api.route("/carga", methods=["PUT"])
def cargar_datos():
    """
    Procesa la solicitud POST para cargar datos de diferentes fuentes.
    """
    try:
        # Leer los datos enviados en el cuerpo de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos válidos."}), 400

        # Leer el archivo de entrada
        if not os.path.exists(INPUT_FILE):
            return jsonify({"error": f"Archivo {INPUT_FILE} no encontrado."}), 404

        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Eliminar registros con "address": "" y procesar
        contenido = contenido.replace('"address" : "",', '')
        datos = json.loads(contenido)

        # Separar registros válidos, reparados y rechazados
        validos = []
        reparados = []
        rechazados = []

        for idx, item in enumerate(datos, start=1):
            nombre = item.get("documentName", "Sin nombre")
            latitud = item.get("latwgs84")
            longitud = item.get("lonwgs84")
            codigo_postal = item.get("postalCode")

            # Validación básica
            if not latitud or not longitud:
                rechazados.append({
                    "fuenteDatos": "EUS",
                    "nombre": nombre,
                    "Localidad": item.get("municipality", ""),
                    "motivoError": f"Latitud/Longitud no válidas (lat={latitud}, lon={longitud})"
                })
                continue

            if not codigo_postal:
                rechazados.append({
                    "fuenteDatos": "EUS",
                    "nombre": nombre,
                    "Localidad": item.get("municipality", ""),
                    "motivoError": "Código postal inválido ()"
                })
                continue

            # Agregar a los registros válidos
            validos.append({
                "Monumento": {
                    "nombre": nombre,
                    "direccion": item.get("address", ""),
                    "codigo_postal": codigo_postal,
                    "longitud": longitud,
                    "latitud": latitud,
                    "descripcion": item.get("documentDescription", "")
                },
                "Localidad": item.get("municipality", ""),
                "Provincia": item.get("territory", "")
            })

        # Guardar registros válidos en el archivo de salida
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(validos, f, ensure_ascii=False, indent=4)

        # Devolver resultados
        return jsonify({
            "sucessfully_loaded_registers": len(validos),
            "repaired_registers": reparados,
            "rejected_registers": rechazados
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500

if __name__ == "__main__":
    api.run(debug=True, port=5004)
