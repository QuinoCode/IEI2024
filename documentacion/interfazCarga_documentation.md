openapi: 3.0.0
info:
  title: API para la carga de fuentes
  description: API que renderiza un formulario HTML para la selección de fuentes a cargar.
  version: 1.0.0
servers:
  - url: http://localhost:5007
    description: Servidor de desarrollo local
paths:
  /:
    get:
      summary: Mostrar formulario HTML
      description: Renderiza la interfaz HTML para seleccionar fuentes y realizar la carga de datos.
      responses:
        '200':
          description: Interfaz HTML renderizada correctamente.
          content:
            text/html:
              schema:
                type: string
                example: "<!DOCTYPE html><html><head><title>Formulario</title></head><body>...</body></html>"
        '500':
          description: Error interno del servidor al intentar renderizar la plantilla.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error detallado.
                    example: "Error interno del servidor."
