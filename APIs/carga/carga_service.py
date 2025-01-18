from convertidores.parsers import csvParser
from convertidores.parsers import xmlParser
from convertidores.parsers import transformar_geocodificacion
from convertidores.parsers.csvParser import main
from convertidores.parsers.xmlParser import main
from convertidores.parsers.transformar_geocodificacion import main
from flask import request

def cargar_dataset_service(data):
    diccionario_respuesta = None
    requested_dataset_list = []
    todas_requested = data.get('todas')

    if (todas_requested): 
        cv_return = retrieve_CV()
        cle_return = retrieve_CLE()
        eus_return = retrieve_EUS()
        diccionario_respuesta = squash_json_feedback_results_into_single_json([cv_return, cle_return, eus_return])
        return diccionario_respuesta

    cv_requested = data.get('cv')
    if (cv_requested):
        cv_return = retrieve_CV()
        requested_dataset_list.append(cv_return)

    cle_requested = data.get('cle')
    if (cle_requested):
        cle_return = retrieve_CLE()
        requested_dataset_list.append(cle_return)

    eus_requested = data.get('eus')
    if (eus_requested):
        eus_return = retrieve_EUS()
        requested_dataset_list.append(eus_return)

    diccionario_respuesta = squash_json_feedback_results_into_single_json(requested_dataset_list)

    if not  diccionario_respuesta:
        return {"error": "No hubo respuesta de la base de datos"}
    return diccionario_respuesta

def squash_json_feedback_results_into_single_json(list_of_jsons):
    sum_of_successfully_loaded_registers = 0
    list_of_repaired_registers = []
    list_of_rejected_registers = []

    for json in list_of_jsons:
        sum_of_successfully_loaded_registers += json['successfully_loaded_registers']
        list_of_repaired_registers.append(json['repaired_registers'])
        list_of_rejected_registers.append(json['rejected_registers'])
    list_of_repaired_registers = [register for sublist in list_of_repaired_registers for register in sublist]
    list_of_rejected_registers = [register for sublist in list_of_rejected_registers for register in sublist]
    return {
        "successfully_loaded_registers": sum_of_successfully_loaded_registers,
        "repaired_registers": list_of_repaired_registers,
        "rejected_registers": list_of_rejected_registers
    }


def retrieve_CV():
    cv_loading_feedback = csvParser.main()
    return cv_loading_feedback

def retrieve_CLE():
    cle_loading_feedback = xmlParser.main()
    return cle_loading_feedback

def retrieve_EUS():
    eus_loading_feedback = transformar_geocodificacion.main()
    return eus_loading_feedback
