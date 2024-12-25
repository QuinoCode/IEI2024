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
        print(f"Monumento '{monumento["nombre"]}' ha sido descartado porque ya existe en la base de datos")
        return True
    return False

def valoresMonumentoNulos(monumento):
    # TODO: extraer el if de debajo a un método que los valores importantes no son null, sino descartar comprobarValoresMonumentoNull (con todos los campos)
    # Devuelve true si hay algún valor nulo, devuelve false si todos tiene valor
    atributos = ["tipo", "direccion", "codigo_postal", "longitud", "latitud", "descripcion"]
    for atributo in atributos:
        if monumento[atributo] == None or monumento[atributo] == "":
            print("Monumento descartado por no tener el artibuto {atributo} definido")
            return True
    return False
    
def codigoPostalInvalido(monumento):
    #Comprobar si codigo postal está entre 1000 y 52999
    if 999 < int(monumento["codigo_postal"]) > 53000:
        print('Formato codigo postal incorrecto, descartado')
        return True
    return False
    # Devuelve true si es invalido devuelve false si es valido

def latitudOlongitudInvalidas(monumento):
    #Comprobar que longitud esté dentro de 180 y latitud dentro de 90
    if -180.1 < float(monumento["longitud"]) > 180.1:
        print('Formato longitud incorrecto, descartado')
        return True

    if -90.1 < float(monumento["latitud"]) > 90.1:
        print('Formato latitud incorrecto, descartado')
        return True
    
    return False
    # Devuelve true si son invalidas false si son validas

def validToInsertLocalidad(sql_manager, localidad):
    if localidad == None:
        print("Localidad descartada por no tener nombre")
        return False
    if (localidadYaInsertada(sql_manager, localidad)):
        return False
    return True

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
        return False
    provincia = unificaLenguaje(provincia) #Devuelve la provincia estandarizada a los valores esperados (siempre y cuando haga matching con uno de los valores plurilingues esperados)
    provincia = corregirProvinica(provincia)
    if (nombreProvinciaInvalido(provincia)):
        return False
    if (provinciaYaInsertada(sql_manager, provincia)):
        return False
    return True

def provinciaYaInsertada(sql_manager, provincia):
    check = sql_manager.execute("SELECT * FROM Provincia WHERE nombre=?", (provincia,))
    exists = check.fetchone()
    exists = exists is not None
    if exists:
        print(f"Provincia '{provincia}' ha sido descartada porque ya existe en la base de datos")
        return True
    return False

def corregirProvinica(provincia):
    provincia_acento = {
        "Alava" : "Álava",
        "Almeria" : "Almería",
        "Avila" : "Ávila",
        "Caceres" : "Cáceres",
        "Cadiz" : "Cádiz",
        "Castellon" : "Castellón",
        "Cordoba" : "Córdoba",
        "Guipuzcoa" : "Guipúzcoa",
        "Jaen" : "Jaén",
        "Leon" : "León",
        "Malaga" : "Málaga",
        "ALAVA" : "ÁLAVA",
        "ALMERIA" : "ALMERÍA",
        "AVILA" : "ÁVILA",
        "CACERES" : "CÁCERES",
        "CADIZ" : "CÁDIZ",
        "CASTELLON" : "CASTELLÓN",
        "CORDOBA" : "CÓRDOBA",
        "GUIPUZCOA" : "GUIPÚZCOA",
        "JAEN" : "JAÉN",
        "LEON" : "LEÓN",
        "MALAGA" : "MÁLAGA"
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
        "Araba": "ÁLAVA",
        "Araba/Álava": "ÁLAVA",
        "Bizkaia": "VIZCAYA",
        "Gipuzkoa": "GUIPÚZCOA",
        "Ávila": "ÁVILA",
        "A Coruña" : "LA CORUÑA",
        "A CORUÑA" : "LA CORUÑA"
    }
    # TODO: Aquí llamas un método que corrija con un mapa: { "Alacant": "Alicante", "València": "Valencia" }# Busca la provincia en el mapa y corrige si es necesario
    provincia_correcta = provincia_bilingue.get(provincia, provincia)
    if (provincia_correcta != provincia):
        print(f"El nombre de la provincia {provincia} ha sido estandarizado a {provincia_correcta}")
    return provincia_correcta

def nombreProvinciaInvalido(provincia):
    # TODO: crear una lista de provincias validas de manera que se pueda buscar "provincia" in lista y que devuelva si existe o no
    provincias = ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila",
        "Badajoz", "Baleares", "Barcelona", "Burgos", "Cáceres", "Cádiz",
        "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", 
        "Girona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", 
        "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lleida", 
        "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", 
        "Palencia", "Pontevedra", "Salamanca", "Segovia", "Sevilla", 
        "Soria", "Tarragona", "Santa Cruz de Tenerife", "Teruel", "Toledo", 
        "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza",
        "ÁLAVA", "ALBACETE", "ALICANTE", "ALMERÍA", "ÁVILA",
        "BADAJOZ", "BALEARES", "BARCELONA", "BURGOS", "CÁCERES", "CÁDIZ",
        "CASTELLÓN", "CIUDAD REAL", "CÓRDOBA", "LA CORUÑA", "CUENCA",
        "GIRONA", "GRANADA", "GUADALAJARA", "GUIPÚZCOA", "HUELVA", "HUESCA",
        "JAÉN", "LA CORUÑA", "LA RIOJA", "LAS PALMAS", "LEÓN", "LLEIDA",
        "LUGO", "MADRID", "MÁLAGA", "MURCIA", "NAVARRA", "OURENSE",
        "PALENCIA", "PONTEVEDRA", "SALAMANCA", "SEGOVIA", "SEVILLA",
        "SORIA", "TARRAGONA", "SANTA CRUZ DE TENERIFE", "TERUEL", "TOLEDO",
        "VALENCIA", "VALLADOLID", "VIZCAYA", "ZAMORA", "ZARAGOZA"]
    # TODO: aquí llamas un método que compruebe que el nombre está dentro de los esperados. (dentro de la lista)
    if not provincia in provincias:
        print("La provincia {provincia} no es válida")
        return True
    return False
