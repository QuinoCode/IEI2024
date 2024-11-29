import csv
import json

# Ruta del archivo CSV de entrada
csv_file_path = 'C:/Users/usuario/Documents/00 Universidad/GII 24-25/A - IEI - Integración e interoperabilidad/Laboratorio/bienes_inmuebles_interes_cultural.csv'

# Ruta del archivo JSON de salida
json_file_path = 'C:/Users/usuario/Documents/00 Universidad/GII 24-25/A - IEI - Integración e interoperabilidad/Laboratorio/ComunitatValenciana_a_json.json'

# Lista para almacenar los registros del CSV como diccionarios
data = []

# Abrimos el archivo CSV y lo leemos
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
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
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Datos convertidos y guardados en: {json_file_path}")
