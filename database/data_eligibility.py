import sqlite3

def validToInsertMonument(sql_manager, monumento):
    if monumento["nombre"] == None or "":
        print("Monumento descartado por no tener nombre")
        return False

    if (monumentoYaInsertado(sql_manager, monumento)):
        return False

    if  (valoresMonumentoNulos(monumento)):
        return False;

    if  (codigoPostalInvalido(monumento)):
        return False;
    if  (latitudOlongitudInvalidas(monumento)):
        return False;

    return True

def monumentoYaInsertado(sql_manager, monumento):
    check = sql_manager.dbcursor.execute("SELECT * FROM Monumento WHERE nombre ="+"\'"+monumento["nombre"].replace("'", "")+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Monumento '{monumento["nombre"]}' ha sido descartado porque ya existe en la base de datos")
        return True
    return False

def valoresMonumentoNulos(monumento):
    # TODO: extraer el if de debajo a un método que los valores importantes no son null, sino descartar comprobarValoresMonumentoNull (con todos los campos)
    # Faltan cosas abajo probablemente
    if monumento["latitud"] == None or monumento["latitud"] == "" or monumento["longitud"] == None or monumento["longitud"] == "" or monumento["tipo"] == None:
        print()
        return False
    # Devuelve true si hay algún valor nulo, devuelve false si todos tiene valor
    
def codigoPostalInvalido(monumento):
    # TODO: Comprobar que el código postal sea valido (no mayor de 52999 ni menor de 01000)
    print()
    pass
    # Devuelve true si es invalido devuelve false si es valido

def latitudOlongitudInvalidas(monumento):
    # TODO: Comprobar que la latitud y la longitud no sea ni mayor que 180 ni menor que -180 
    print()
    pass
    # Devuelve true si son invalidas false si son validas

def validToInsertLocalidad(sql_manager, localidad):
    if localidad == None:
        print("Localidad descartada por no tener nombre")
        return False
    if (localidadYaInsertada(sql_manager, localidad)):
        return False
    return True

def localidadYaInsertada(sql_manager, localidad):
    check = sql_manager.dbcursor.execute("SELECT * FROM Localidad WHERE nombre ="+"\'"+localidad+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Localidad '{localidad}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

def validToInsertProvincia(sql_manager, provincia):
    if provincia == None:
        print("Provincia descartada por no tener nombre")
        return False
    provincia = unificaLenguaje(provincia) #Devuelve la provincia estandarizada a los valores esperados (siempre y cuando haga matching con uno de los valores plurilingues esperados)
    if (nombreProvinciaInvalido(provincia)):
        return False
    if (provinciaYaInsertada(sql_manager, provincia)):
        return False
    return True

def provinciaYaInsertada(sql_manager, provincia):
    check = sql_manager.dbcursor.execute("SELECT * FROM Provincia WHERE nombre=?", (provincia,))
    exists = check.fetchone()
    exists = exists is not None
    if exists:
        print(f"Provincia '{provincia}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

def unificaLenguaje(provincia):
    provincia_bilingue = {
        "CASTELLÓ": "CASTELLÓN",
        "ALACANT": "ALICANTE",
        "VALÈNCIA": "VALENCIA",
        "Araba": "ÁLAVA",
        "Araba/Álava": "ÁLAVA",
        "Bizkaia": "VIZCAYA",
        "Gipuzkoa": "GUIPÚZCOA"
    }
    # TODO: Aquí llamas un método que corrija con un mapa: { "Alacant": "Alicante", "València": "Valencia" }
    # Busca la provincia en el mapa y corrige si es necesario
    provincia_correcta = provincia_bilingue.get(provincia, provincia)
    if (provincia_correcta != provincia):
        print(f"El nombre de la provincia {provincia} ha sido estandarizado a {provincia_correcta}")
    return provincia_correcta

def nombreProvinciaInvalido(provincia):
    # TODO: crear una lista de provincias validas de manera que se pueda buscar "provincia" in lista y que devuelva si existe o no
    # TODO: aquí llamas un método que compruebe que el nombre está dentro de los esperados. (dentro de la lista)
    print()
    # Devuelve true si el nombre de la provincia no se encuentra en la lista de valores válidos, false en caso contrario
