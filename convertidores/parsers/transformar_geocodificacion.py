import requests
import json
import os
import sys


def retrieveDataFromAPI():
    """
    Realiza una solicitud GET al endpoint /getEUS y devuelve los datos en formato JSON.
    """
    url_destination = "http://localhost:5004/getEUS"
    try:
        response = requests.get(url_destination)
        if response.status_code == 200:
            return response.json()
        print(f"[ERROR] Error {response.status_code}: {response.text}")
        return []
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al API: {e}")
        return []


def saveDataToFile():
    """
    Llama a retrieveDataFromAPI para obtener datos y los guarda en un archivo JSON.
    """
    data = retrieveDataFromAPI()  # Llama a la función para obtener los datos
    file_path = "response_data.json"  # Nombre del archivo a crear

    try:
        with open(file_path, "w", encoding="utf-8") as file:  # Abre el archivo en modo escritura
            json.dump(data, file, ensure_ascii=False, indent=4)  # Guarda los datos en formato JSON con sangría
        return file_path
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo: {e}")
        sys.exit(1)


def main():
    """
    Función principal que procesa los datos de entrada, realiza validaciones, y genera un archivo de salida.
    """
    # Determina el archivo de entrada
    INPUT_FILE = saveDataToFile() if len(sys.argv) < 2 else sys.argv[1]
    OUTPUT_FILE = "datos/properly_formated.json"

    # Verifica si el archivo de entrada existe
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Archivo {INPUT_FILE} no encontrado.")
        sys.exit(1)

    try:
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

        # Resultado final
        return {
            "sucessfully_loaded_registers": len(validos),
            "repaired_registers": reparados,
            "rejected_registers": rechazados
        }

    except Exception as e:
        print(f"[ERROR] Error al procesar el archivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    resultado = main()
    if resultado:
        print(json.dumps(resultado, ensure_ascii=False, indent=4))

