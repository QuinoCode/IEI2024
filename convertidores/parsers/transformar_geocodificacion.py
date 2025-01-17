import requests
import json
import os
import sys

def retrieveDataFromAPI():
    url_destination = "http://localhost:5004/getEUS"
    response = requests.get(url_destination)

    if response.status_code == 200:
        return response.json()
    return {"error": "Something went wrong when fetching data from EUS API"}


# Función para guardar datos en un archivo
def saveDataToFile():
    data = retrieveDataFromAPI()  # Llama a la función para obtener los datos
    file_path = "response_data.json"  # Nombre del archivo a crear

    with open(file_path, "w") as file:  # Abre el archivo en modo escritura
        json.dump(data, file, indent=4)  # Guarda los datos en formato JSON con sangría

    return file_path

def main():
    INPUT_FILE = saveDataToFile() if len(sys.argv) < 2 else sys.argv[1]
    OUTPUT_FILE = "datos/properly_formated.json"

    # Leer el archivo de entrada
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Archivo {INPUT_FILE} no encontrado.")
        sys.exit(1)

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

    # Imprimir resultados
    print(json.dumps({
        "sucessfully_loaded_registers": len(validos),
        "repaired_registers": reparados,
        "rejected_registers": rechazados
    }, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
