import json

archivoL = 'C:/Users/usuario/Documents/00 Universidad/GII 24-25/A - IEI - Integración e interoperabilidad/Laboratorio/ComunitatValenciana_a_json.json'
archivoR = 'C:/Users/usuario/Documents/00 Universidad/GII 24-25/A - IEI - Integración e interoperabilidad/Laboratorio/ComunitatValenciana_para_Quino.json'
lista = []

@staticmethod
def tipo(denominacion, clasificacion, categoria):
        if denominacion == "ERROR_404_NO_ENCONTRADO":
            return "ERROR_404_NO_ENCONTRADO"
        elif not categoria == "ERROR_404_NO_ENCONTRADO":
            if categoria == "Zona arqueológica" or categoria == "Zona paleontológica":
                return "Yacimiento arqueológico"
            elif denominacion.startswith("Torre") or denominacion.startswith("Castillo") or denominacion.startswith("Castellet") or denominacion.startswith("Castell ") or ("Fortaleza" in denominacion and clasificacion == "Monumento"):
                return "Castillo-Fortaleza-Torre"
            elif denominacion.startswith("Escudo") or denominacion.startswith("Emblema") or clasificacion == "Archiva":
                return "Edificio Singular"
            elif "Puente" in denominacion:
                return "Puente"
            elif clasificacion == "Conjunto histórico" or clasificacion == "Jardín histórico" or "Escudo" in denominacion:
                return "Otros"
            else:
                return "ERROR_404_NO_ENCONTRADO"
        elif not clasificacion == "ERROR_404_NO_ENCONTRADO":
            if clasificacion == "Bienes muebles 1ª":
                return "Otros"
            elif denominacion.startswith("Peirò") or "iglesia-" in denominacion:
                return "Iglesia-Ermita"
            elif denominacion.startswith("Casa") or denominacion.startswith("Cruz"):
                return "Edificio Singular"
            else:
                return "Otros"
        else:
            return "ERROR_404_NO_ENCONTRADO"

@staticmethod
def laDescripcion(clasificacion, categoria):
    if clasificacion == "ERROR_404_NO_ENCONTRADO" and categoria == "ERROR_404_NO_ENCONTRADO":
        return "ERROR_404_NO_ENCONTRADO"
    elif not categoria == "ERROR_404_NO_ENCONTRADO" and not clasificacion == "ERROR_404_NO_ENCONTRADO":
        return f"{clasificacion} - {categoria}"
    elif not categoria == "ERROR_404_NO_ENCONTRADO":
        return categoria
    else:
        return clasificacion

@staticmethod
def laClasificacion(codclasificacion, clasificacion):
    if not clasificacion == "ERROR_404_NO_ENCONTRADO":
        return clasificacion
    elif not codclasificacion == "ERROR_404_NO_ENCONTRADO":
        if codclasificacion == "1":
            return "Bienes inmuebles 1ª"
        else:
            return "Bienes muebles 1ª"
    else:
        return "ERROR_404_NO_ENCONTRADO"

@staticmethod
def laCategoria(codcategoria, categoria):
        if not categoria == "ERROR_404_NO_ENCONTRADO":
            return categoria
        elif codcategoria == "1":
            return "Conjunto histórico"
        elif codcategoria == "2":
            return "Sitio histórico"
        elif codcategoria == "3":
            return "Jardín histórico"
        elif codcategoria == "4":
            return "Monumento"
        elif codcategoria == "5":
            return "Zona arqueológica"
        elif codcategoria == "6":
            return "Archivo"
        elif codcategoria == "7":
            return "Zona paleontológica"
        elif codcategoria == "8":
            return "Espacio etnológico"
        elif codcategoria == "9":
            return "Parque cultural"
        elif codcategoria == "11":
            return "Monumento de interés local"
        elif codcategoria == "18":
            return "Individual (mueble)"
        elif codcategoria == "20":
            return "Fondo de museo (primera)"
        else:
            return "ERROR_404_NO_ENCONTRADO"

class ComunitatValencianaGuarda:
    def __init__(self, igpcv, denominacion, provincia, municipio, utmeste, utmnorte, codclasificacion, clasificacion, codcategoria, categoria):
        clasificacioAuxiliar = laClasificacion(codclasificacion, clasificacion)
        categoriaAuxiliar = laCategoria(codcategoria, categoria)
        self.id = id
        self.nombre = denominacion
        self.tipo = tipo(denominacion, clasificacioAuxiliar, categoriaAuxiliar)
        self.longitud = utmeste
        self.latitud = utmnorte
        self.direccion = "ERROR_404_NO_ENCONTRADO"
        self.codigo_postal = "ERROR_404_NO_ENCONTRADO"
        self.descripcion = laDescripcion(clasificacioAuxiliar, categoriaAuxiliar)
        self.municipio = municipio
        self.provincia = provincia


try:
    with open(archivoL, 'r', encoding='utf-8') as file:
        jsonContent = json.load(file)
        for entry in jsonContent:
            igpcv = entry.get("IGPCV", "")
            if igpcv == "":
                igpcv = "ERROR_404_NO_ENCONTRADO"

            denominacion = entry.get("DENOMINACION", "")
            if denominacion == "":
                denominacion = "ERROR_404_NO_ENCONTRADO"

            provincia = entry.get("PROVINCIA", "")
            if provincia == "":
                provincia = "ERROR_404_NO_ENCONTRADO"

            municipio = entry.get("MUNICIPIO", "")
            if municipio == "":
                municipio = "ERROR_404_NO_ENCONTRADO"

            utmeste = entry.get("UTMESTE", "")
            if utmeste == "":
                utmeste = "ERROR_404_NO_ENCONTRADO"

            utmnorte = entry.get("UTMNORTE", "")
            if utmnorte == "":
                utmnorte = "ERROR_404_NO_ENCONTRADO"

            codclasificacion = entry.get("CODCLASIFICACION", "")
            if codclasificacion == "":
                codclasificacion = "ERROR_404_NO_ENCONTRADO"

            clasificacion = entry.get("CLASIFICACION", "")
            if clasificacion == "":
                clasificacion = "ERROR_404_NO_ENCONTRADO"

            codcategoria = entry.get("CODCATEGORIA", "")
            if codcategoria == "":
                codcategoria = "ERROR_404_NO_ENCONTRADO"

            categoria = entry.get("CATEGORIA", "")
            if categoria == "":
                categoria = "ERROR_404_NO_ENCONTRADO"

            comunitat = ComunitatValencianaGuarda(igpcv,denominacion, provincia, municipio, utmeste, utmnorte,codclasificacion, clasificacion, codcategoria, categoria)

            item = {
                "Monumento" : {
                    "nombre" : comunitat.nombre,
                    "tipo" : comunitat.tipo,
                    "direccion" : comunitat.direccion,
                    "codigo_postal" : comunitat.codigo_postal,
                    "longitud" : comunitat.longitud,
                    "latitud" : comunitat.latitud,
                    "descripcion" : comunitat.descripcion
                }, 
                "Localidad" : comunitat.provincia,
                "Provincia" : comunitat.municipio
            }
            lista.append(item)
        print("Todo bien")
except Exception as e:
    print(f"Error al leer el archivo JSON: {e}")

with open(archivoR, 'w', encoding='utf-8') as file:
    json.dump(lista, file, ensure_ascii=False, indent=4)
print("Fin del programa")
