import json

def denominacion(data, id_primero):
    descartados = []

    for wrapper in data:
        # Filtrar por DENOMINACION
        if wrapper["DENOMINACION"].replace('"', "") == "":

            # Guardar monumento a descartar
            descartados.append(id_primero)

            # Descartar monumento
            wrapper["IGPCV"] = None
            wrapper["DENOMINACION"] = None
            wrapper["PROVINCIA"] = None
            wrapper["MUNICIPIO"] = None
            wrapper["UTMESTE"] = None
            wrapper["UTMNORTE"] = None
            wrapper["CODCLASIFICACION"] = None
            wrapper["CLASIFICACION"] = None
            wrapper["CODCATEGORIA"] = None
            wrapper["CATEGORIA"] = None

            # Imprimir descarte
            print(f"El monumento {id_primero} se ha descartado por no tener definido el campo DENOMINACION")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def provincia_descartar_nulos(data, id_primero, descartados):
    for wrapper in data:
        if not id_primero in descartados:

            provincia = wrapper["PROVINCIA"]

            if provincia == "":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por no tener definido el campo PROVINCIA")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def provincia_corregir(data, id_primero, descartados):
    corregidos = []

    correcciones_provincia = [("CASTELLON", "CASTELLÓN"), ("CASTELLÓ", "CASTELLÓN"), ("ALACANT", "ALICANTE"), ("VALÈNCIA", "VALENCIA")]

    for wrapper in data:
        provincia = wrapper["PROVINCIA"]

        for tupla in correcciones:
            if provincia == tupla[0]:
                # Corregir
                wrapper["PROVINCIA"] = tupla[1]

                # Guardar monumento corregido
                corregidos.append(id_primero)

                # Imprimir corrección
                print(f"El monumento {id_primero} se ha corregido el campo MUNICIPIO")

        # Aumentar contador
        id_primero += 1

    return data, corregidos

def provincia_descartar_errores(data, id_primero, descartados):

    provincias_esperables = ["CASTELLÓN", "ALICANTE", "VALENCIA"]

    for wrapper in data:
        if not id_primero in descartados:

            provincia = wrapper["PROVINCIA"]

            if not provincia in provincias_esperables:
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por tener definido el campo MUNICIPIO mal definido")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def municipio(data, id_primero, descartados):
    for wrapper in data:
        if not id_primero in descartados:

            municipio = wrapper["MUNICIPIO"]

            if municipio == "":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por no tener definido el campo MUNICIPIO")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def utm(data, id_primero, descartados):
    for wrapper in data:
        if not id_primero in descartados:

            este = wrapper["UTMESTE"]
            norte = wrapper["UTMNORTE"]

            if este == "" or norte == "":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                if este == "" and norte == "":
                    print(f"El monumento {id_primero} se ha descartado por no tener definido el campo UTMESTE ni el UTMNORTE")
                elif este == "":
                    print(f"El monumento {id_primero} se ha descartado por no tener definido el campo UTMESTE")
                else:
                    print(f"El monumento {id_primero} se ha descartado por no tener definido el campo UTMNORTE")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def clasificacion_descartar_nulos(data, id_primero, descartados):
    for wrapper in data:
        if not id_primero in descartados:

            codclasificacion = wrapper["CODCLASIFICACION"]
            clasificacion = wrapper["CLASIFICACION"]

            if codclasificacion == "" and clasificacion == "":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por no tener definido el campo CODCLASIFICACION ni el CLASIFICACION")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def clasificacion_corregir(data, id_primero, descartados, corregidos):

    clasificacion_esperable = [("1", "Bienes inmuebles 1ª"), ("2", "Bienes muebles 1ª")]

    for wrapper in data:
        if not id_primero in descartados:

            codclasificacion = wrapper["CODCLASIFICACION"]
            clasificacion = wrapper["CLASIFICACION"]

            if codclasificacion == "":
                # Marcar como error
                wrapper["CODCLASIFICACION"] = "ERROR_INEXISTENTE"

                # Buscar si la clasificacion está en las tuplas
                for tupla in clasificacion_esperable:
                    if clasificacion == tupla[1]:
                        # Corregir
                        wraper["CODCLASIFICACION"] = tupla[0]

                        # Guardar monumento corregido
                        if not id_primero in corregidos:
                            corregidos.append(id_primero)

                        # Imprimir corrección
                        print(f"El monumento {id_primero} se ha corregido el campo CODCLASIFICACION")
                        break

            elif clasificacion == "":
                # Marcar como error
                wrapper["CLASIFICACION"] = "ERROR_INEXISTENTE"

                # Buscar si el codclasificacion está en las tuplas
                for tupla in clasificacion_esperable:
                    if codclasificacion == tupla[0]:
                        # Corregir
                        wraper["CLASIFICACION"] = tupla[1]

                        # Guardar monumento corregido
                        if not id_primero in corregidos:
                            corregidos.append(id_primero)

                        # Imprimir corrección
                        print(f"El monumento {id_primero} se ha corregido el campo CLASIFICACION")
                        break

        # Aumentar contador
        id_primero += 1

    return data, corregidos

def clasificacion_descartar_errores(data, id_primero, descartados):

    clasificacion_esperable = [("1", "Bienes inmuebles 1ª"), ("2", "Bienes muebles 1ª")]

    for wrapper in data:
        if not id_primero in descartados:

            codclasificacion = wrapper["CODCLASIFICACION"]
            clasificacion = wrapper["CLASIFICACION"]

            flag = "KO"

            for tupla in clasificacion_esperable:
                if tupla[0] == codclasificacion and tupla[1] == clasificacion:
                    flag = "Stop"
                    break

            if flag == "KO":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por tener mal definido los campos CODCLASIFICACION y CLASIFICACION")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def categoria_descartar_nulos(data, id_primero, descartados):
    for wrapper in data:
        if not id_primero in descartados:

            codclasificacion = wrapper["CODCATEGORIA"]
            clasificacion = wrapper["CATEGORIA"]

            if codclasificacion == "" and clasificacion == "":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por no tener definido el campo CODCLASIFICACION ni el CLASIFICACION")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def categoria_corregir(data, id_primero, descartados, corregidos):

    categoria_esperable = [("1", "Conjunto histórico"), ("2", "Sitio histórico"), ("3", "Jardín histórico"),
                    ("4", "Monumento"), ("5", "Zona arqueológica"), ("6", "Archivo"),
                    ("7", "Zona paleontológica"), ("8", "Espacio etnológico"), ("9", "Parque cultural"),
                    ("11", "Monumento de interés local"), ("18", "Individual (mueble)"), ("20", "Fondo de museo (primera)"),]

    for wrapper in data:
        if not id_primero in descartados:

            codcategoria = wrapper["CODCATEGORIA"]
            categoria = wrapper["CLASIFICACION"]

            if codcategoria == "":
                # Marcar como error
                wrapper["CODCATEGORIA"] = "ERROR_INEXISTENTE"

                # Buscar si la categoria está en las tuplas
                for tupla in categoria_esperable:
                    if categoria == tupla[1]:
                        # Corregir
                        wraper["CODCATEGORIA"] = tupla[0]

                        # Guardar monumento corregido
                        if not id_primero in corregidos:
                            corregidos.append(id_primero)

                        # Imprimir corrección
                        print(f"El monumento {id_primero} se ha corregido el campo CODCATEGORIA")
                        break

            elif categoria == "":
                # Marcar como error
                wrapper["CLASIFICACION"] = "ERROR_INEXISTENTE"

                # Buscar si el codcategoria está en las tuplas
                for tupla in categoria_esperable:
                    if codcategoria == tupla[0]:
                        # Corregir
                        wraper["CATEGORIA"] = tupla[1]

                        # Guardar monumento corregido
                        if not id_primero in corregidos:
                            corregidos.append(id_primero)

                        # Imprimir corrección
                        print(f"El monumento {id_primero} se ha corregido el campo CATEGORIA")
                        break

        # Aumentar contador
        id_primero += 1

    return data, corregidos

def categoria_descartar_errores(data, id_primero, descartados):

    categoria_esperable = [("1", "Conjunto histórico"), ("2", "Sitio histórico"), ("3", "Jardín histórico"),
                           ("4", "Monumento"), ("5", "Zona arqueológica"), ("6", "Archivo"),
                           ("7", "Zona paleontológica"), ("8", "Espacio etnológico"), ("9", "Parque cultural"),
                           ("11", "Monumento de interés local"), ("18", "Individual (mueble)"), ("20", "Fondo de museo (primera)"),]

    for wrapper in data:
        if not id_primero in descartados:

            codcategoria = wrapper["CODCATEGORIA"]
            categoria = wrapper["CATEGORIA"]

            flag = "KO"

            for tupla in categoria_esperable:
                if tupla[0] == codcategoria and tupla[1] == categoria:
                    flag = "Stop"
                    break

            if flag == "KO":
                # Guardar monumento a descartar
                descartados.append(id_primero)

                # Descartar monumento
                wrapper["IGPCV"] = None
                wrapper["DENOMINACION"] = None
                wrapper["PROVINCIA"] = None
                wrapper["MUNICIPIO"] = None
                wrapper["UTMESTE"] = None
                wrapper["UTMNORTE"] = None
                wrapper["CODCLASIFICACION"] = None
                wrapper["CLASIFICACION"] = None
                wrapper["CODCATEGORIA"] = None
                wrapper["CATEGORIA"] = None

                # Imprimir descarte
                print(f"El monumento {id_primero} se ha descartado por tener mal definido los campos CODCATEGORIA y CATEGORIA")

        # Aumentar contador
        id_primero += 1

    return data, descartados

def filtrar_monumentos_CSV(data, id_primero_lanzadera):
    data, descartados = denominacion(data, id_primero_lanzadera)
    data, descartados = provincia_descartar_nulos(data, id_primero_lanzadera, descartados)
    data, descartados = municipio(data, id_primero_lanzadera, descartados)
    data, descartados = utm(data, id_primero_lanzadera, descartados)
    data, descartados = clasificacion_descartar_nulos(data, id_primero_lanzadera, descartados)
    data, descartados = categoria_descartar_nulos(data, id_primero_lanzadera, descartados)
    data, corregidos = provincia_corregir(data, id_primero_lanzadera, descartados)
    data, corregidos = clasificacion_corregir(data, id_primero_lanzadera, descartados, corregidos)
    data, corregidos = categoria_corregir(data, id_primero_lanzadera, descartados, corregidos)
    data, descartados = provincia_descartar_errores(data, id_primero_lanzadera, descartados)
    data, descartados = clasificacion_descartar_errores(data, id_primero_lanzadera, descartados)
    data, descartados = categoria_descartar_errores(data, id_primero_lanzadera, descartados)

    return data, descartados, corregidos
