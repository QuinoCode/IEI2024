openapi: 3.0.0
info:
  title: API de Carga y Almacenamiento
  description: API para cargar un dataset en una base de datos y borrar su almacenamiento.
  version: 1.0.0
servers:
  - url: http://localhost:5001
    description: Servidor de desarrollo local
paths:
  /carga:
    put:
      summary: Cargar un dataset en la base de datos
      description: Carga un dataset proporcionado por el usuario en formato JSON a la base de datos.
      requestBody:
        description: JSON que contiene los datos del dataset a cargar.
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: string
      responses:
        '200':
          description: Dataset cargado correctamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  repaired_registers:
                    type: integer
                    description: Número de registros reparados durante la carga.
                    example: 5
                  rejected_registers:
                    type: integer
                    description: Número de registros rechazados durante la carga.
                    example: 2
        '404':
          description: No hubo respuesta de la base de datos.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "No hubo respuesta de la base de datos."
        '500':
          description: Error interno del servidor al cargar los datos.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "Error interno del servidor."
  /borrar:
    delete:
      summary: Borrar los datos almacenados
      description: Elimina todos los datos almacenados en la base de datos.
      responses:
        '200':
          description: Datos borrados correctamente.
          content:
            application/json:
              schema:
                type: object
                additionalProperties:
                  type: string
        '500':
          description: Error interno al intentar borrar los datos.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "Error interno del servidor."
