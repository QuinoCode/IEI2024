import sqlite3
import os
from database.data_eligibility import *

class Sql_manager:
    def __init__(self):
        self.dbfile = 'EstructuraGlobal.db'
        self.dbcursor = None
        self.conn = None

    @staticmethod
    def borrar_estructura_global():
        """
        Borra el archivo 'EstructuraGlobal.db' ubicado en la carpeta principal 'IEI2024'.
        """
        # Obtener la ruta absoluta de la carpeta principal
        carpeta_principal = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Construir la ruta completa del archivo a borrar
        archivo_a_borrar = os.path.join(carpeta_principal, 'EstructuraGlobal.db')

        try:
            if os.path.exists(archivo_a_borrar):
                os.remove(archivo_a_borrar)
                print(f"Archivo '{archivo_a_borrar}' eliminado exitosamente.")
                return True
            else:
                print(f"El archivo '{archivo_a_borrar}' no existe.")
                return False
        except Exception as e:
            print(f"Ocurrió un error al intentar borrar el archivo: {e}")
            return False

    def getSingleton(self):
        if not os.path.exists(self.dbfile):
            self.conn = sqlite3.connect(self.dbfile)
            self.dbcursor = self.conn.cursor()
            self.createTables()
        self.conn = sqlite3.connect(self.dbfile)
        self.dbcursor = self.conn.cursor()

    def deleteContentTables(self):
        self.dbcursor.execute('DELETE FROM Monumento')
        self.dbcursor.execute('DELETE FROM Localidad')
        self.dbcursor.execute('DELETE FROM Provincia')
        self.conn.commit()
        self.dbcursor.execute('VACUUM')

    def createTables(self):
        self.dbcursor.execute('CREATE TABLE Monumento(codigo INTEGER PRIMARY KEY, nombre, tipo, direccion, codigo_postal, longitud, latitud, descripcion, en_localidad)')
        self.dbcursor.execute('CREATE TABLE Localidad(codigo INTEGER PRIMARY KEY, nombre, en_provincia)')
        self.dbcursor.execute('CREATE TABLE Provincia(codigo INTEGER PRIMARY KEY, nombre)')
        self.conn.commit()

    def query_monumento(self, localidad, codigo_postal, provincia, tipo):
        self.dbcursor.execute("PRAGMA foreign_keys = ON;")
        query = """SELECT m.*, l.en_provincia FROM Monumento m JOIN Localidad l ON m.en_localidad = l.nombre"""
        conditions = []
        values = []

        if localidad:
            conditions.append("l.nombre = ?")
            values.append(str(localidad))
        if codigo_postal:
            conditions.append("m.codigo_postal = ?")
            values.append(str(codigo_postal))
        if provincia is not None:
            conditions.append("l.en_provincia = ?")
            values.append(str(provincia))
        if tipo is not None:
            conditions.append("m.tipo = ?")
            values.append(tipo)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.dbcursor.execute(query, values)
        results = self.dbcursor.fetchall()

        return self.convert_query_into_properly_structurated_json(results)

# Este método ordena los arrays de hacer una query en sqlite al formato esperado y habitual
    def convert_query_into_properly_structurated_json(self, arrayDeArrays):
        resultArray = []
        for array in arrayDeArrays:
            map = {
                "nombre": array[1],
                "tipo": array[2],
                "direccion":array[3],
                "codigo_postal": array[4],
                "longitud": array[6],
                "latitud": array[5],
                "descripcion": array[7],
                "en_localidad": array[8],
                "en_provincia": array[9],
            }
            resultArray.append(map)
        return resultArray
    """
    { 
        "successfully_loaded_registers" : int, 
        "repaired_registers": [{"fuente_datos": valor, "nombre": valor "localidad": valor, "motivo_de_error": valor, "operacion_realizada": valor} ,..., ] 
        "rejected_registers": [{"fuente_datos": valor, "nombre": valor, "localidad": valor, "motivo_de_error": valor }, ...]
    }
    """
    def insertMonumento(self, item):
        idDB = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Monumento').fetchone()[0]
        idDB = str(int(idDB) + 1) 
        monNombre =  item["Monumento"]["nombre"].replace("'", "")
        monTipo =  item["Monumento"]["tipo"]
        monDireccion =  item["Monumento"]["direccion"].replace("'", "")
        monCodPost =  item["Monumento"]["codigo_postal"]
        monLatitud =  item["Monumento"]["latitud"]
        monLongitud =  item["Monumento"]["longitud"]
        monDescripcion =  item["Monumento"]["descripcion"].replace("'", "")
        en_localidad = item["Localidad"].replace("'", "")
        self.dbcursor.execute(
            "INSERT INTO Monumento VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (idDB, monNombre, monTipo, monDireccion, monCodPost, monLatitud, monLongitud, monDescripcion, en_localidad)
        ) 
        
        self.conn.commit()

    def insertLocalidad(self, item, provincia_corregida):
        idLoc = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Localidad').fetchone()[0]
        idLoc = str(int(idLoc) + 1)
        localidad = item["Localidad"].replace("'", "").replace('"', "")
        en_provincia =  provincia_corregida.replace("'", "").replace('"', "") if provincia_corregida else ""
        self.dbcursor.execute(
            'INSERT INTO Localidad VALUES(?, ?, ?)',
            (idLoc, localidad, en_provincia)
        )
        self.conn.commit()
        
    def insertProvincia(self, provincia_corregida):
        idProv = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Provincia').fetchone()[0]
        idProv = str(int(idProv) + 1)
        provincia = provincia_corregida.replace("'", "").replace('"', "")
        self.dbcursor.execute(
            'INSERT INTO Provincia VALUES(?, ?)',
            (idProv, provincia)
        )
        self.conn.commit()

    def insertData(self, arrayJson, source):
        successfully_loaded_registers = 0
        repaired_registers = []
        rejected_registers = []

        for item in arrayJson:
            validProvincia, provincia_corregida, provinciaYaInsertada, reasonManagedProvincia = validToInsertProvincia(self.dbcursor, item["Provincia"].replace('"', "").replace("'", ""), source)
            validMonumento, reasonRejectedMonument = validToInsertMonument(self.dbcursor, item["Monumento"])
            validLocalidad, localidadYaInsertada, reasonRejectedLocalidad = validToInsertLocalidad(self.dbcursor, item["Localidad"].replace('"', "").replace("'", ""))

            # El monumento se puede insertar y tanto provincia como localidad son correctas 
            if ((validProvincia or provinciaYaInsertada) and (validLocalidad or localidadYaInsertada) and validMonumento):
                self.insertMonumento(item)
                if (validProvincia):
                    self.insertProvincia(provincia_corregida)
                    if (reasonManagedProvincia[0] == "Reparado"): 
                        repaired_registers.append({
                            "fuente_datos": source,
                            "nombre": item["Monumento"]["nombre"].replace("'", ""),
                            "localidad": item["Localidad"],
                            "motivo_de_error": "La provincia necesitaba estandarización",
                            "operacion_realizada": f"Sustituido {item['Provincia']} por {provincia_corregida}"
                        })
                if (validLocalidad):
                    self.insertLocalidad(item, provincia_corregida)
                successfully_loaded_registers += 1
            # Fin del caso en el que se inserta

            if (not validMonumento):
                rejected_registers.append({
                    "fuente_datos": source,
                    "nombre": item["Monumento"]["nombre"].replace("'", ""),
                    "localidad": item["Localidad"],
                    "motivo_de_error": reasonRejectedMonument
                })
            if (not validLocalidad and not localidadYaInsertada):
                rejected_registers.append({
                    "fuente_datos": source,
                    "nombre": item["Monumento"]["nombre"].replace("'", ""),
                    "localidad": item["Localidad"],
                    "motivo_de_error": reasonRejectedLocalidad
                })
            if (not validProvincia and not provinciaYaInsertada):
                if (reasonManagedProvincia[0] == "Rechazado"):
                    rejected_registers.append({
                        "fuente_datos": source,
                        "nombre": item["Monumento"]["nombre"].replace("'", ""),
                        "localidad": item["Localidad"],
                        "motivo_de_error": reasonManagedProvincia[1]
                    })

        response_map = {
            "successfully_loaded_registers": successfully_loaded_registers,
            "repaired_registers": repaired_registers,
            "rejected_registers": rejected_registers,
        }
        print(f"Sql_create repaired: \n {response_map['repaired_registers']} \n")
        print(f"Sql_create rejected: \n {response_map['rejected_registers']} \n")
        return response_map

    # Este método es el método lanzadera de la clase, inserta los datos y devuelve el feedback
    """Parámetros
     jsonArray => Json con los valores a introducir en la base de datos
     source => String con la procedencia del json (csv, xml, sql)
    """
    """Salida
    { 
    "successfully_loaded_registers" : int, 
    "repaired_registers": [{"fuente_datos": valor, "nombre": valor "localidad": valor, "motivo_de_error": valor, "operacion_realizada": valor} ,..., ] 
    "rejected_registers": [{"fuente_datos": valor, "nombre": valor, "localidad": valor, "motivo_de_error": valor }, ...]
    }
    """
    def main(self, jsonArray, source):
        self.getSingleton()
        response = self.insertData(jsonArray, source)
        return response
