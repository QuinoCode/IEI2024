import sqlite3

def validToInsertMonument(sql_manager, monumento):
    if monumento["nombre"] == None or "":
        print("Monumento descartado por no tener nombre")
        return False

    if (monumentoYaInsertado(sql_manager, monumento)):
        return False

    if  (valoresMonumentoNulos(monumento)):
        return False

    if  (codigoPostalInvalido(monumento)):
        return False
    if  (latitudOlongitudInvalidas(monumento)):
        return False

    return True

def monumentoYaInsertado(sql_manager, monumento):
    check = sql_manager.execute("SELECT * FROM Monumento WHERE nombre ="+"\'"+monumento["nombre"].replace("'", "")+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Monumento \'{monumento["nombre"]}\' ha sido descartado porque ya existe en la base de datos")
        return True
    return False

# Devuelve true si hay algún valor nulo, devuelve false si todos tiene valor
def valoresMonumentoNulos(monumento):
    atributos = ["tipo", "direccion", "codigo_postal", "longitud", "latitud", "descripcion"]
    for atributo in atributos:
        if monumento[atributo] == None or monumento[atributo] == "":
            print(f"El monumento \'{monumento["nombre"]}\' se ha descartado por no tener el atributo \'{atributo}\' definido")
            return True
    return False
    
def codigoPostalInvalido(monumento):
    # TODO: Comprobar si codigo postal no tiene caracteres no numéricos
    try:
        #Comprobar si codigo postal está entre 1000 y 52999
        if 999 < int(monumento["codigo_postal"]) > 53000:
            print(f"El monumento {monumento["nombre"]} se ha descartado porque su código postal {monumento["codigo_postal"]} está fuera de rango")
            return True
    except ValueError as e:
        print(f"El monumento {monumento["nombre"]} se ha descartado porque su código postal {monumento["codigo_postal"]} no es un número")
        return True
    return False
    # Devuelve true si es invalido devuelve false si es valido

# Comprobar que longitud esté dentro de 180 y latitud dentro de 90
# Devuelve true si son invalidas false si son validas
def latitudOlongitudInvalidas(monumento):
    if -180.0 < float(monumento["longitud"]) >= 180.0:
        print(f"El monumento {monumento["nombre"]} se ha descartado porque la longitud \'{monumento["longitud"]}\' esta fuera de rango")
        return True

    if -90.0 <= float(monumento["latitud"]) >= 90.0:
        print(f"El monumento {monumento["nombre"]} se ha descartado porque latitud \'{monumento["latitud"]}\' esta fuera de rango")
        return True
    
    return False

def validToInsertLocalidad(sql_manager, localidad):
    if localidad == None:
        print("Localidad descartada por no tener nombre")
        return False
    if (localidadYaInsertada(sql_manager, localidad)):
        return False
    return True

# def unificarEstiloLocalidad(localidad):
#     localidad_estanderizada = localidad.upper()
#     if (localidad_estanderizada != localidad):
#         print(f"El nombre de la localidad {localidad} ha sido estandarizada a {localidad_estanderizada}")

def localidadYaInsertada(sql_manager, localidad):
    check = sql_manager.execute("SELECT * FROM Localidad WHERE nombre ="+"\'"+localidad+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Localidad '{localidad}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

def validToInsertProvincia(sql_manager, provincia):
    if provincia == None:
        print("Provincia descartada por no tener nombre")
        return False, provincia
    provincia = unificarEstiloProvincia(provincia)
    provincia = unificaLenguaje(provincia) #Devuelve la provincia estandarizada a los valores esperados (siempre y cuando haga matching con uno de los valores plurilingues esperados)
    provincia = añadirAcentoAProvincia(provincia)
    if (nombreProvinciaInvalido(provincia)):
        return False, provincia
    if (provinciaYaInsertada(sql_manager, provincia)):
        return False, provincia
    return True, provincia

def provinciaYaInsertada(sql_manager, provincia):
    check = sql_manager.execute("SELECT * FROM Provincia WHERE nombre=?", (provincia,))
    exists = check.fetchone()
    exists = exists is not None
    if exists:
        print(f"Provincia \'{provincia}\' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

def unificarEstiloProvincia(provincia):
    provincia_estandarizada = provincia.upper()
    if (provincia_estandarizada != provincia):
        print(f"El nombre de la provincia {provincia} ha sido estandarizada a mayúsculas: {provincia_estandarizada}")
        return provincia_estandarizada

def añadirAcentoAProvincia(provincia):
    provincia_acento = {
        "ALAVA" : "ÁLAVA",
        "LEON" : "LEÓN",
        "ALAVA" : "ÁLAVA",
        "GUIPUZCOA" : "GUIPÚZCOA",
        "CASTELLON" : "CASTELLÓN",
        "AVILA" : "ÁVILA"
    }
    provincia_correcta = provincia_acento.get(provincia, provincia)
    if (provincia_correcta != provincia):
        print(f"El nombre de la provincia {provincia} ha sido corregido a {provincia_correcta}")
    return provincia_correcta

def unificaLenguaje(provincia):
    provincia_bilingue = {
        "CASTELLÓ": "CASTELLÓN",
        "ALACANT": "ALICANTE",
        "VALÈNCIA": "VALENCIA",
        "ARABA": "ÁLAVA",
        "ARABA/ÁLAVA": "ÁLAVA",
        "BIZKAIA": "VIZCAYA",
        "GIPUZKOA": "GUIPÚZCOA"
    }
    # TODO: Aquí llamas un método que corrija con un mapa: { "Alacant": "Alicante", "València": "Valencia" }# Busca la provincia en el mapa y corrige si es necesario
    provincia_correcta = provincia_bilingue.get(provincia, provincia)
    if (provincia_correcta != provincia):
        print(f"El nombre de la provincia {provincia} ha sido estandarizado al castellano: {provincia_correcta}")
    return provincia_correcta

def nombreProvinciaInvalido(provincia):
    provincias = ["ÁVILA", "BURGOS", "LEÓN", "PALENCIA", "SALAMANCA",
                  "SEGOVIA", "SORIA", "VALLADOLID", "ZAMORA",
                  "ÁLAVA", "GUIPÚZCOA", "VIZCAYA",
                  "ALICANTE", "CASTELLÓN", "VALENCIA"]
    if not provincia in provincias:
        print(f"La provincia \'{provincia}\' no es válida")
        return True
    return False
