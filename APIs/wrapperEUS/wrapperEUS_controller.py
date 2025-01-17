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


if __name__ == "__main__":
    api.run(debug=True, port=5004)
