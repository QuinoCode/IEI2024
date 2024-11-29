class ComunitatValenciana:
    def __init__(self, igpcv, denominacion, provincia, municipio, utmeste, utmnorte, codclasificacion, clasificacion, codcategoria, categoria):
        self.igpcv = igpcv
        self.denominacion = denominacion
        self.provincia = provincia
        self.municipio = municipio
        self.utmeste = utmeste
        self.utmnorte = utmnorte
        self.codclasificacion = codclasificacion
        self.clasificacion = clasificacion
        self.codcategoria = codcategoria
        self.categoria = categoria




if __name__ == "__main__":
    carpeta = 'C:/Users/usuario/Documents/00 Universidad/GII 24-25/A - IEI - Integración e interoperabilidad/Laboratorio/'
    original = carpeta + 'bienes_inmuebles_interes_cultural.csv'
    archivo_json = carpeta + 'ComunitatValenciana.json'

    lista = leer_csv(original)
    generar_json(lista, archivo_json)
