openapi: 3.0.0
info:
  title: API wrapper CV
  description: API para devolver datos de monumentos de Comunidad Valenciana a partir de un CSV
  version: 1.0.0
servers:
  - url: http://localhost:5002
    description: Servidor de desarrollo local
paths:
  /getCV:
    get:
      summary: Obtener un JSON del CSV de monumentos de Comunidad Valenciana
      description: Convierte un archivo CSV a un JSON y lo devuelve como respuesta a la petición
      responses:
        '200':
          description: El CSV fue traducido y devuelto sin error
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  description: Objeto dinámico representando los datos del CSV
                  additionalProperties:
                    type: string
        '400':
          description: Bad request, causado por errores de traducción
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error
                    example: "Archivo no encontrado o formato incorrecto"
