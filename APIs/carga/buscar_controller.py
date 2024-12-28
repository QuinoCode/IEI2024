from flask import Flask, jsonify, request

api = Flask(__name__)

@api.post("/buscar")
def buscar_monumentos():
    # Obtener datos enviados desde el frontend
    data = request.get_json()
    localidad = data.get('localidad', '').strip()
    codigo_postal = data.get('codigoPostal', '').strip()
    provincia = data.get('provincia', '').strip()
    tipo = data.get('tipo', '').strip()
    
    # Aquí deberíamos interactuar con una base de datos o fuente de datos
    # Ejemplo simulado:
    resultados_simulados = [
        {"nombre": "Puente Romano", "tipo": "Puente", "direccion": "Calle Antigua 1", "localidad": "Salamanca", "codigoPostal": "37001", "provincia": "Salamanca", "descripcion": "Puente histórico sobre el río Tormes."},
        {"nombre": "Castillo de Gormaz", "tipo": "Castillo", "direccion": "S/N", "localidad": "Gormaz", "codigoPostal": "42313", "provincia": "Soria", "descripcion": "Fortaleza califal del siglo IX."},
    ]
    
    # Filtrar resultados según los parámetros recibidos
    resultados_filtrados = [
        item for item in resultados_simulados
        if (not localidad or localidad.lower() in item['localidad'].lower())
        and (not codigo_postal or codigo_postal == item['codigoPostal'])
        and (not provincia or provincia.lower() in item['provincia'].lower())
        and (not tipo or tipo.lower() == item['tipo'].lower())
    ]
    
    return jsonify({"resultados": resultados_filtrados}), 200

if __name__ == "__main__":
    api.run(debug=True, port=5001)
