import csv
import json

def convertir_csv_a_json(csv_origen, csvConverted_out):
    data = []

    # Abrimos el archivo CSV y lo leemos
    with open(csv_origen, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        # Leemos la primera línea para obtener las cabeceras
        headers = next(csv_reader)

        # Recorremos cada fila del CSV
        for row in csv_reader:
            # Creamos un diccionario con las cabeceras como claves y los valores de la fila
            row_dict = {}

            for i, header in enumerate(headers):
                # Convertimos todos los valores a string
                row_dict[header] = str(row[i])

            # Añadimos el diccionario a la lista de datos
            data.append(row_dict)

    # Escribimos los datos en un archivo JSON
    with open(csvConverted_out, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Datos convertidos y guardados en: {csvConverted_out}")

    return data