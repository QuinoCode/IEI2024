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

        


    def insertData(self, arrayJson):
        for item in arrayJson:
            if validToInsertMonument(self.dbcursor, item["Monumento"]):
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
            
            if validToInsertLocalidad(self.dbcursor, item["Localidad"].replace('"', "").replace("'", "")):
                idLoc = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Localidad').fetchone()[0]
                idLoc = str(int(idLoc) + 1)
                localidad = item["Localidad"].replace("'", "").replace('"', "")
                en_provincia = item["Provincia"].replace("'", "").replace('"', "")
                self.dbcursor.execute(
                    'INSERT INTO Localidad VALUES(?, ?, ?)',
                    (idLoc, localidad, en_provincia)
                )
                self.conn.commit()
            
            if validToInsertProvincia(self.dbcursor, item["Provincia"].replace('"', "").replace("'", "")):
                idProv = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Provincia').fetchone()[0]
                idProv = str(int(idProv) + 1)
                provincia = item["Provincia"].replace("'", "").replace('"', "")
                self.dbcursor.execute(
                    'INSERT INTO Provincia VALUES(?, ?)',
                    (idProv, provincia)
                )
                self.conn.commit()

    def main(self, jsonArray):
        self.getSingleton()
        self.insertData(jsonArray)


