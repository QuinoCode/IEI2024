import json
def filtrar_monumentos_CSV(data, id_primero):
    corregidos = []
    descartados = []

    correcciones_provincia = [("CASTELLON", "CASTELLÓN"), ("CASTELLÓ", "CASTELLÓN"), ("ALACANT", "ALICANTE"), ("VALÈNCIA", "VALENCIA")]
    provincias_corregibles = ["CASTELLON", "CASTELLÓ", "ALACANT", "VALENCIA"]
    provincias_esperables = ["CASTELLÓN", "ALICANTE", "VALENCIA"]

    clasificacion_esperable = [("1", "Bienes inmuebles 1ª"), ("2", "Bienes muebles 1ª")]

    categoria_esperable = [("1", "Conjunto histórico"), ("2", "Sitio histórico"), ("3", "Jardín histórico"),
                    ("4", "Monumento"), ("5", "Zona arqueológica"), ("6", "Archivo"),
                    ("7", "Zona paleontológica"), ("8", "Espacio etnológico"), ("9", "Parque cultural"),
                    ("11", "Monumento de interés local"), ("18", "Individual (mueble)"), ("20", "Fondo de museo (primera)"),]

    for wrapper in data:
        provincia = wrapper["PROVINCIA"]
        utmeste = wrapper["UTMESTE"]
        utmnorte = wrapper["UTMNORTE"]
        codclasifiacion = wrapper["CODCLASIFICACION"]
        clasificacion = wrapper["CLASIFICACION"]
        categoria = wrapper["CATEGORIA"]
        codcategoria = wrapper["CODCATEGORIA"]

        # Filtrar por DENOMINACION
        if not wrapper["DENOMINACION"].replace('"', "") == "":

            # Filtrar por PROVINCIA
            if not provincia == "":
                if provincia in provincias_corregibles:
                    for tupla in correcciones_provincia:
                        if provincia == tupla[0]: # El error corregible
                            wrapper["PROVINCIA"] = tupla[1] # La corrección
                            provincia = tupla[1]
                            break
                    print(f"En el monumento {id_primero} se ha corregido el campo PROVINCIA")
                    corregidos.append(id_primero)

                if provincia in provincias_esperables:

                    # Filtrar por MUNICIPIO
                    if not wrapper["MUNICIPIO"] == "":

                        # Filtrar por UTM
                        if not utmeste == "" and not utmnorte == "":

                            # Filtrar por CLASIFICACION
                            if not (clasificacion == "" and codclasificacion == ""):

                                if clasificacion == "":
                                    for tupla in clasificacion_esperable:
                                        if clasificacion == tupla[1]:
                                            codclasificacion = tupla[0]
                                            wrapper["CODCLASIFICACION"] = tupla[0]
                                            print(f"El monumento {id_primero} se ha corregido el campo CODCLASIFICACION")
                                            if not id_primero in corregidos:
                                                corregidos.append(id_primero)
                                            break

                                elif codclasificacion == "":
                                    for tupla in clasificacion_esperable:
                                        if codclasificacion == tupla[0]:
                                            clasificacion = tupla[1]
                                            wrapper["CLASIFICACION"] = tupla[1]
                                            print(f"El monumento {id_primero} se ha corregido el campo CLASIFICACION")
                                            if not id_primero in corregidos:
                                                corregidos.append(id_primero)
                                            break

                                aceptable = 0
                                for tupla in clasificacion_esperable:
                                    if codclasificacion == tupla[0] and clasifiacion == tupla[1]:
                                        aceptable = 1
                                        break

                                if aceptable == 1:

                                    # Filtrar por CATEGORIA
                                    if not (categoria == "" and codcategoria == ""):

                                        if categoria == "":
                                            for tupla in categoria_esperable:
                                                if codcategoria == tupla[0]:
                                                    categoria = tupla[1]
                                                    wrapper["CATEGORIA"] = tupla[1]
                                                    print(f"El monumento {id_primero} se ha corregido el campo CATEGORIA")
                                                    if not id_primero in corregidos:
                                                        corregidos.append(id_primero)
                                                    break

                                        elif codcategoria == "":
                                            for tupla in categoria_esperable:
                                                if categoria == tupla[1]:
                                                    codcategoria = tupla[0]
                                                    wrapper["CODCATEGORIA"] = tupla[0]
                                                    print(f"El monumento {id_primero} se ha corregido el campo CODCATEGORIA")
                                                    if not id_primero in corregidos:
                                                        corregidos.append(id_primero)
                                                    break

                                        aceptable = 1
                                        for tupla in categoria_esperable:
                                            if codcategoria == tupla[0] and categoria == tupla[1]:
                                                aceptable = 0
                                                break

                                        if aceptable == 1:
                                            descartados.append(id_primero)
                                            print(f"El monumento {id_primero} se ha descartado por tener los campos CODCATEGORIA y CATEGORIA mal definidos")

                                    else :
                                        descartados.append(id_primero)
                                        print(f"El monumento {id_primero} se ha descartado por no tener definidos los campos CODCATEGORIA y CATEGORIA")

                                else :
                                    descartados.append(id_primero)
                                    print(f"El monumento {id_primero} se ha descartado por tener los campos CODCLASIFICACION y CLASIFICACION mal definidos")

                            else :
                                descartados.append(id_primero)
                                print(f"El monumento {id_primero} se ha descartado por no tener definidos los campos CODCLASIFICACION y CLASIFICACION")

                        elif utmneste == "" and utmnorte == "":
                            descartados.append(id_primero)
                            print(f"El monumento {id_primero} se ha descartado por no tener definidos los campos UTMESTE y UTMNORTE")

                        elif utmeste == "":
                            descartados.append(id_primero)
                            print(f"El monumento {id_primero} se ha descartado por no tener definido el campo UTMESTE")

                        else :
                            descartados.append(id_primero)
                            print(f"El monumento {id_primero} se ha descartado por no tener definido el campo UTMNORTE")

                    else :
                        descartados.append(id_primero)
                        print(f"El monumento {id_primero} se ha descartado por no tener definido el campo MUNICIPIO}")

                else :
                    descartados.append(id_primero)
                    print(f"El monumento {id_primero} se ha descartado por tener el campo PROVINCIA mal definido")

            else :
                descartados.append(id_primero)
                print(f"El monumento {id_primero} se ha descartado por no tener definido el campo PROVINCIA")

        else :
            descartados.append(id_primero)
            print(f"El monumento {id_primero} se ha descartado por no tener definido el campo DENOMINACION")

        # Descartar monumento
        if id_primero in descartados:
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

        # Aumentar contador
        id_primero += 1

    return data, corregidos, descartados