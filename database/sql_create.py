import sqlite3
import os


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

    def validToInsertMonument(self, monumento):
        if monumento["nombre"] == None or "":
            return False
        
        check = self.dbcursor.execute("SELECT * FROM Monumento WHERE nombre ="+"\'"+monumento["nombre"].replace("'", "")+"\'")
        exists = check.fetchone()
        if exists:
            return False
        
        if monumento["latitud"] == None or monumento["latitud"] == "" or monumento["longitud"] == None or monumento["longitud"] == "" or monumento["tipo"] == None:
            return False

        return True
        

    def validToInsertLocalidad(self, localidad):
        if localidad == None:
            return False

        check = self.dbcursor.execute("SELECT * FROM Localidad WHERE nombre ="+"\'"+localidad+"\'")
        exists = check.fetchone()
        if exists:
            return False
        

        return True

    def validToInsertProvincia(self, provincia):
        if provincia == None:
            return False

        check = self.dbcursor.execute("SELECT * FROM Provincia WHERE nombre=?", (provincia,))
        exists = check.fetchone()
        exists = exists is not None
        if exists:
            return False
        return True

    def insertData(self, arrayJson):
        for item in arrayJson:
            if self.validToInsertMonument(item["Monumento"]):
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
            
            if self.validToInsertLocalidad(item["Localidad"].replace('"', "").replace("'", "")):
                idLoc = self.dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Localidad').fetchone()[0]
                idLoc = str(int(idLoc) + 1)
                localidad = item["Localidad"].replace("'", "").replace('"', "")
                en_provincia = item["Provincia"].replace("'", "").replace('"', "")
                self.dbcursor.execute(
                    'INSERT INTO Localidad VALUES(?, ?, ?)',
                    (idLoc, localidad, en_provincia)
                )
                self.conn.commit()
            
            if self.validToInsertProvincia(item["Provincia"].replace('"', "").replace("'", "")):
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


