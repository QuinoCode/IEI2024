from database.sql_create import Sql_manager

def query_database(request):
    sql_manager = Sql_manager()
    sql_manager.getSingleton()
    diccionario_respuesta = None
    localidad = request.args.get('localidad')
    codigo_postal = request.args.get('codigo_postal')
    provincia = request.args.get('provincia')
    tipo = request.args.get('tipo')

    results = sql_manager.query_monumento(localidad, codigo_postal, provincia, tipo)
    return results
