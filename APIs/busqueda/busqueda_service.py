from database.sql_create import Sql_manager

def query_database(localidad, codigo_postal, provincia, tipo):
    sql_manager = Sql_manager()
    sql_manager.getSingleton()
    results = sql_manager.query_monumento(localidad, codigo_postal, provincia, tipo)
    return results
