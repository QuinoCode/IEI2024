# Importación de módulos y funciones necesarios para el manejo de datos, bases de datos y peticiones HTTP
from convertidores.parsers import csvParser
from convertidores.parsers import xmlParser
from convertidores.parsers import transformar_geocodificacion
from convertidores.parsers.csvParser import main  # Importa la función principal del parser CSV
from convertidores.parsers.xmlParser import main  # Importa la función principal del parser XML
from convertidores.parsers.transformar_geocodificacion import main  # Importa la función principal de transformación de geocodificación
from database.sql_create import Sql_manager  # Importa el gestor de bases de datos
from flask import request
from database import sql_create

# Función para borrar toda la estructura global de la base de datos
def borrar_estructura_global():
    return sql_create.Sql_manager.borrar_estructura_global()

# Servicio para cargar un dataset en la base de datos
def cargar_dataset_service(data):
    """
    Procesa una solicitud para cargar datasets en la base de datos.
    Recibe un JSON con las claves que especifican qué datasets cargar:
    - "todas": Si está presente, carga todos los datasets disponibles.
    - "cv": Si está presente, carga el dataset CV.
    - "cle": Si está presente, carga el dataset CLE.
    - "eus": Si está presente, carga el dataset EUS.
    
    Devuelve un diccionario con el estado de la operación.
    """
    diccionario_respuesta = None
    requested_dataset_list = []  # Lista para almacenar los resultados de carga de cada dataset
    todas_requested = data.get('todas')  # Verifica si se solicitó cargar todos los datasets

    if todas_requested: 
        # Carga todos los datasets disponibles
        cv_return = retrieve_CV()
        cle_return = retrieve_CLE()
        eus_return = retrieve_EUS()
        # Combina los resultados en un único diccionario
        diccionario_respuesta = squash_json_feedback_results_into_single_json([cv_return, cle_return, eus_return])
        return diccionario_respuesta

    # Carga de dataset CV si está solicitado
    cv_requested = data.get('cv')
    if cv_requested:
        cv_return = retrieve_CV()
        requested_dataset_list.append(cv_return)

    # Carga de dataset CLE si está solicitado
    cle_requested = data.get('cle')
    if cle_requested:
        cle_return = retrieve_CLE()
        requested_dataset_list.append(cle_return)

    # Carga de dataset EUS si está solicitado
    eus_requested = data.get('eus')
    if eus_requested:
        eus_return = retrieve_EUS()
        requested_dataset_list.append(eus_return)

    # Combina los resultados de los datasets seleccionados en un único diccionario
    diccionario_respuesta = squash_json_feedback_results_into_single_json(requested_dataset_list)

    # Si no se generó una respuesta, devuelve un error
    if not diccionario_respuesta:
        return {"error": "No hubo respuesta de la base de datos"}
    return diccionario_respuesta

# Función para combinar los resultados de carga de varios datasets en un único JSON
def squash_json_feedback_results_into_single_json(list_of_jsons):
    """
    Recibe una lista de resultados en formato JSON y los combina en un único diccionario.
    Suma los registros cargados exitosamente y agrupa los registros reparados y rechazados.
    """
    sum_of_successfully_loaded_registers = 0
    list_of_repaired_registers = []
    list_of_rejected_registers = []

    # Itera sobre cada JSON en la lista para sumar y agrupar los datos
    for json in list_of_jsons:
        sum_of_successfully_loaded_registers += json['successfully_loaded_registers']
        list_of_repaired_registers.append(json['repaired_registers'])
        list_of_rejected_registers.append(json['rejected_registers'])

    # Aplana las listas de registros reparados y rechazados
    list_of_repaired_registers = [register for sublist in list_of_repaired_registers for register in sublist]
    list_of_rejected_registers = [register for sublist in list_of_rejected_registers for register in sublist]

    # Devuelve el resultado combinado
    return {
        "successfully_loaded_registers": sum_of_successfully_loaded_registers,
        "repaired_registers": list_of_repaired_registers,
        "rejected_registers": list_of_rejected_registers
    }

# Función para cargar el dataset CV utilizando el parser correspondiente
def retrieve_CV():
    """
    Carga el dataset CV utilizando el parser CSV.
    Devuelve un JSON con el resultado de la operación.
    """
    cv_loading_feedback = csvParser.main()
    return cv_loading_feedback

# Función para cargar el dataset CLE utilizando el parser correspondiente
def retrieve_CLE():
    """
    Carga el dataset CLE utilizando el parser XML.
    Devuelve un JSON con el resultado de la operación.
    """
    cle_loading_feedback = xmlParser.main()
    return cle_loading_feedback

# Función para cargar el dataset EUS utilizando el parser correspondiente
def retrieve_EUS():
    """
    Carga el dataset EUS utilizando la transformación de geocodificación.
    Devuelve un JSON con el resultado de la operación.
    """
    eus_loading_feedback = transformar_geocodificacion.main()
    return eus_loading_feedback

# Servicio para borrar el contenido almacenado en la base de datos
def borrar_almacen_service():
    """
    Elimina todo el contenido de las tablas en la base de datos utilizando el gestor SQL.
    """
    sql_manager = Sql_manager()
    sql_manager.getSingleton()  # Obtiene una instancia única del gestor de base de datos
    sql_manager.deleteContentTables()  # Borra el contenido de las tablas
