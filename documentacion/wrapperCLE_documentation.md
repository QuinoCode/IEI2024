openapi: 3.0.0
info:
  title: API wrapper CLE
  description: API para devolver datos de monumentos de Castilla y León a partir de un XML
  version: 1.0.0
servers:
  - url: http://localhost:5003
    description: Servidor de desarrollo local
paths:
  /getCLE:
    get:
      summary: Obtener un JSON del XML de monumentos de Castilla y Leon
      description: Convierte un archivo XML a un JSON y lo devuelve como respuesta a la petición
      responses:
        '200':
          description: El XML fue traducido y devuelto sin error
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  description: Objeto dinámico representando los datos del XML
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
