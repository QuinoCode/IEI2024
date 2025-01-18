import sqlite3

"""output
1. Monumento válido para ser insertado? 
2. Motivo de la invalidez es la duplicación?
3. Motivo por el que el monumento ha sido rechazado en caso de serlo
"""
def validToInsertMonument(sql_manager, monumento):
    if monumento["nombre"] == None or "":
        print("Monumento descartado por no tener nombre")
        return False, "El nombre del monumento es nulo"

    if (monumentoYaInsertado(sql_manager, monumento)):
        return False, "El monumento ya había sido insertado en la base de datos"
    algunAtributoNulo, mensajeError = valoresMonumentoNulos(monumento)
    if  (algunAtributoNulo):
        return False, mensajeError

    if  (codigoPostalInvalido(monumento)):
        return False, "El código postal no es correcto"
    if  (latitudOlongitudInvalidas(monumento)):
        return False, "Las coordenadas no son correctas"

    return True, ""

def monumentoYaInsertado(sql_manager, monumento):
    check = sql_manager.execute("SELECT * FROM Monumento WHERE nombre ="+"\'"+monumento["nombre"].replace("'", "")+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Monumento '{monumento['nombre']}' ha sido descartado porque ya existe en la base de datos")
        return True
    return False

# Devuelve true si hay algún valor nulo, devuelve false si todos tiene valor
"""output
1. Tiene todos los valores válidos?
2. mensaje que dice lo que ha sucedido 
"""
def valoresMonumentoNulos(monumento):
    mensajeValoresMonumentoNulos = ""
    atributos = ["tipo", "direccion", "codigo_postal", "longitud", "latitud", "descripcion"]
    for atributo in atributos:
        if monumento[atributo] == None or monumento[atributo] == "":
            print(f"El monumento '{monumento['nombre']}' se ha descartado por no tener el atributo '{atributo}' definido")
            mensajeValoresMonumentoNulos+= f"El campo {atributo} no tiene valor,"
            return True, mensajeValoresMonumentoNulos
    return False, ""
    
def codigoPostalInvalido(monumento):
    # TODO: Comprobar si codigo postal no tiene caracteres no numéricos
    try:
        #Comprobar si codigo postal está entre 1000 y 52999
        if 999 < int(monumento["codigo_postal"]) > 53000:
            print(f"El monumento {monumento['nombre']} se ha descartado porque su código postal {monumento['codigo_postal']} está fuera de rango")
            return True
    except ValueError as e:
        print(f"El monumento {monumento['nombre']} se ha descartado porque su código postal {monumento['codigo_postal']} no es un número")
        return True
    return False
    # Devuelve true si es invalido devuelve false si es valido

# Comprobar que longitud esté dentro de 180 y latitud dentro de 90
# Devuelve true si son invalidas false si son validas
def latitudOlongitudInvalidas(monumento):
    if -180.0 < float(monumento["longitud"]) >= 180.0:
        print(f"El monumento {monumento['nombre']} se ha descartado porque la longitud '{monumento['longitud']}' esta fuera de rango")
        return True

    if -90.0 <= float(monumento["latitud"]) >= 90.0:
        print(f"El monumento {monumento['nombre']} se ha descartado porque latitud '{monumento['latitud']}' esta fuera de rango")
        return True
    
    return False

"""output
1. Localidad valida para ser insertada?
2. Motivo del rechazo es la duplicación?
3. Razón por la que ha sido rechazado si es el caso
"""
def validToInsertLocalidad(sql_manager, localidad):
    if localidad == None:
        print("Localidad descartada por no tener nombre")
        return False, False, "La Localidad es nula"
    if (localidadYaInsertada(sql_manager, localidad)):
        return False, True, ""
    return True, False, "" 

def localidadYaInsertada(sql_manager, localidad):
    check = sql_manager.execute("SELECT * FROM Localidad WHERE nombre ="+"\'"+localidad+"\'")
    exists = check.fetchone()
    if exists:
        print(f"Localidad '{localidad}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

"""output
--------------------
1. es valida la provincia?
2. provincia corregida
3. La razón de que sea invalida es porque está duplicada?
4. Lista cuyo primer valor es el motivo por el que ha sido tratado el dato (reparado/rechazado)
   segundo valor es el mensaje que tiene
"""
def validToInsertProvincia(sql_manager, provincia, source):
    mensajeModificación = ""
    if provincia == None:
        print("Provincia descartada por no tener nombre")
        return False, provincia, False, ["Rechazado", "La provincia es nula"]
    provincia = unificarEstiloProvincia(provincia)
    provincia, modificacionUnificaLenguaje = unificaLenguaje(provincia) #Devuelve la provincia estandarizada a los valores esperados (siempre y cuando haga matching con uno de los valores plurilingues esperados)
    provincia, modificacionAñadirAcentoAProvincia = añadirAcentoAProvincia(provincia)
    if (nombreProvinciaInvalido(provincia, source)):
        return False, provincia, False, ["Rechazado", "La provincia no está correctamente escrita"]
    if (provinciaYaInsertada(sql_manager, provincia)):
        return False, provincia, True, ["Nada", "Nada de nada"]
    mensajeModificación = modificacionUnificaLenguaje + modificacionAñadirAcentoAProvincia
    if (mensajeModificación == ""):
        return True, provincia, False, ["Nada", "Nada de nada"]
    return True, provincia, False, ["Reparado", mensajeModificación]

def provinciaYaInsertada(sql_manager, provincia):
    check = sql_manager.execute("SELECT * FROM Provincia WHERE nombre=?", (provincia,))
    exists = check.fetchone()
    exists = exists is not None
    if exists:
        print(f"Provincia '{provincia}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

"""output
1. nombre de la provincia 
2. Se ha modificado o no?
"""
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
        return provincia_correcta, f"El nombre de la provincia {provincia} ha sido corregido a {provincia_correcta}"
    return provincia_correcta,""

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
    provincia_correcta = provincia_bilingue.get(provincia, provincia)
    if (provincia_correcta != provincia):
        print(f"El nombre de la provincia {provincia} ha sido estandarizado al castellano: {provincia_correcta}")
        return provincia_correcta, f"El nombre de la provincia {provincia} ha sido estandarizado al castellano: {provincia_correcta}"
    return provincia_correcta, ""

def nombreProvinciaInvalido(provincia, source):
    provincias_CV = ["ALICANTE", "CASTELLÓN", "VALENCIA"]
    provincias_CLE = ["ÁVILA", "BURGOS", "SEGOVIA", "LEÓN", "PALENCIA", "SALAMANCA","SORIA", "VALLADOLID", "ZAMORA",]
    provincias_EUS = ["ÁLAVA", "GUIPÚZCOA", "VIZCAYA"]

    match source:
        case "bienes_inmuebles_interes_cultural.csv":
            if provincia in provincias_CV:
                return False
        case "monumentos.xml":
            if provincia in provincias_CLE:
                return False
        case "edificios.json":
            if provincia in provincias_EUS:
                return False
        case _:
            return True
    return True