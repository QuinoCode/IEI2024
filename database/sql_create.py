import sqlite3
import os
from database.data_eligibility import *


class Sql_manager:
    def __init__(self):
        self.dbfile = 'EstructuraGlobal.db'
        self.dbcursor = None
        self.conn = None

    def getSingleton(self):
        if not os.path.exists(self.dbfile):
            self.conn = sqlite3.connect(self.dbfile)
            self.dbcursor = self.conn.cursor()
            self.createTables()
        self.conn = sqlite3.connect(self.dbfile)
        self.dbcursor = self.conn.cursor()

    def createTables(self):
        self.dbcursor.execute('CREATE TABLE Monumento(codigo INTEGER PRIMARY KEY, nombre, tipo, direccion, codigo_postal, longitud, latitud, descripcion, en_localidad)')
        self.dbcursor.execute('CREATE TABLE Localidad(codigo INTEGER PRIMARY KEY, nombre, en_provincia)')
        self.dbcursor.execute('CREATE TABLE Provincia(codigo INTEGER PRIMARY KEY, nombre)')
        self.conn.commit()

    def query_monumento(self, localidad, codigo_postal, provincia, tipo):
        self.dbcursor.execute("PRAGMA foreign_keys = ON;")
        query = """SELECT m.* FROM Monumento m JOIN Localidad l ON m.en_localidad = l.nombre"""
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

        print(query)
        print(values)
        self.dbcursor.execute(query, values)
        results = self.dbcursor.fetchall()

        if results:
            print(results)
        else: 
            print("No results")

        return results

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
            validProvincia, provincia_corregida = validToInsertProvincia(self.dbcursor, item["Provincia"].replace('"', "").replace("'", ""))
            validMonumento = validToInsertMonument(self.dbcursor, item["Monumento"])
            validLocalidad = validToInsertLocalidad(self.dbcursor, item["Localidad"].replace('"', "").replace("'", ""))
            validProvincia, provincia_corregida = validToInsertProvincia(self.dbcursor, item["Provincia"].replace('"', "").replace("'", ""))

            if (validProvincia and validLocalidad and validMonumento):
                self.insertLocalidad(item, provincia_corregida)
                self.insertProvincia(provincia_corregida)
                self.insertMonumento(item)
                successfully_loaded_registers += 1

        response_map = {
            "sucessfully_loaded_registers": successfully_loaded_registers,
            "repaired_registers": repaired_registers,
            "rejected_registers": rejected_registers,
            }
        return response_map

    # Este método es el método lanzadera de la clase, inserta los datos y devuelve el feedback
    """Parámetros
     jsonArray => Json con los valores a introducir en la base de datos
     source => String con la procedencia del json (csv, xml, sql)
    """
    """Salida
    { 
    "sucessfully_loaded_registers" : int, 
    "repaired_registers": [{"fuente_datos": valor, "nombre": valor "localidad": valor, "motivo_de_error": valor, "operacion_realizada": valor} ,..., ] 
    "rejected_registers": [{"fuente_datos": valor, "nombre": valor, "localidad": valor, "motivo_de_error": valor }, ...]
    }
    """
    def main(self, jsonArray, source):
        self.getSingleton()
        response = self.insertData(jsonArray, source)
        return response


