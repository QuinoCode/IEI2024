import sqlite3
import os

dbfile = 'EstructuraGlobal.db'
dbcursor = None
conn = None

def getSingleton():
    if not os.path.exists(dbfile):
        createSQL()

def createSQL():
    conn = sqlite3.connect(dbfile)
    dbcursor = conn.cursor()
    dbcursor.execute('CREATE TABLE Monumento(codigo, nombre, tipo, direccion, codigo_postal, longitud, latitud, descripcion, en_localidad)')
    dbcursor.execute('CREATE TABLE Localidad(codigo, nombre, en_provincia)')
    dbcursor.execute('CREATE TABLE Provincia(codigo, nombre)')

def validToInsertMonument(monumento):
    if monumento["nombre"] == None or "":
        return False
    
    check = dbcursor.execute("SELECT * FROM Monumento WHERE nombre ="+"\'"+monumento["nombre"]+"\'")
    exists = check.fetchOne()
    if exists:
        return False
    
    if monumento["latitud"] == None or monumento["longitud"] == None or monumento["tipo"] == None:
        return False

    return True
    

def validToInsertLocalidad(localidad):
    check = dbcursor.execute("SELECT * FROM Localidad WHERE nombre ="+"\'"+localidad+"\'")
    exists = check.fetchOne()
    if exists:
        return False
    
    if localidad == None:
        return False

    return True

def validToInsertProvincia(provincia):
    check = dbcursor.execute("SELECT * FROM Provincia WHERE nombre ="+"\'"+provincia+"\'")
    exists = check.fetchOne()
    if exists:
        return False
    
    if provincia == None:
        return False

    return True

def insertData(arrayJson):
    for item in arrayJson:
        if validToInsertMonument(item["Monumento"]):
            idDB = dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Monumento') + 1
            monNombre =  item["Monumento"]["nombre"]
            monTipo =  item["Monumento"]["tipo"]
            monDireccion =  item["Monumento"]["direccion"]
            monCodPost =  item["Monumento"]["codigo_postal"]
            monLatitud =  item["Monumento"]["latitud"]
            monLongitud =  item["Monumento"]["longitud"]
            monDescripcion =  item["Monumento"]["descripcion"]
            dbcursor.execute('INSERT INTO Monumento VALUES('+idDB+', '+monNombre+', '+monTipo+', '+monDireccion+', '+monCodPost+', '+monLatitud+', '+monLongitud+', '+monDescripcion+')') 
        
        if validToInsertLocalidad(item["Localidad"]):
            idLoc = dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Localidad') + 1
            localidad = item["Localidad"]
            dbcursor.execute('INSERT INTO Localidad VALUES('+idLoc+', '+localidad+')')
        
        if validToInsertProvincia(item["Provincia"]):
            idProv = dbcursor.execute('SELECT COALESCE(MAX(codigo), 0) FROM Provincia') + 1
            provincia = item["Provincia"]
            dbcursor.execute('INSERT INTO Provincia VALUES('+idProv+', '+provincia+')')

def main(jsonArray):
    getSingleton()
    insertData(jsonArray)


