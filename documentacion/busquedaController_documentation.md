openapi: 3.0.0
info:
  title: API de búsqueda de monumentos
  version: 1.0.0
  description: El API permite realizar una búsqueda en la base de datos con condiciones

servers:
  - url: http://localhost:5000
    description: Servidor de desarrollo local

paths:
  /buscar:
    get:
      summary: Realizar la petición de búsqueda
      description: Devuelve una lista de monumentos basándose en las condiciones adjuntas.
      parameters:
        - name: localidad
          in: query
          description: La localidad del monumento en cuestión
          required: false
          schema:
            type: string
            example: Requena
        - name: codigo_postal
          in: query
          description: El código postal del monumento
          required: false
          schema:
            type: string
            example: 46340
        - name: provincia
          in: query
          description: La provincia del monumento
          required: false
          schema:
            type: string
            example: VALENCIA
            pattern: '^[A-Z]+$'
        - name: tipo
          in: query
          description: El tipo de monumento
          required: false
          schema:
            type: string
            example: Puente
      responses:
        200:
          description: Una lista de monumentos que satisfacen los criterios
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        404:
          description: No se han encontrado resultados con esos parámetros
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
              example:
                error: "No ha habido ningún resultado con esos parámetros"
        500:
          description: Error del servidor interno
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
              example:
                error: "Internal server error"

components:
  schemas:
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
