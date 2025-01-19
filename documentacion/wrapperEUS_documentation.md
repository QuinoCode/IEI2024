openapi: 3.0.0
info:
  title: API wrapper EUS
  description: API para devolver datos de edificios desde un archivo JSON y verificar el estado del servicio.
  version: 1.0.0
servers:
  - url: http://localhost:5004
    description: Servidor de desarrollo local
paths:
  /getEUS:
    get:
      summary: Obtener el contenido del archivo edificios.json
      description: Devuelve el contenido del archivo JSON con información de edificios.
      responses:
        '200':
          description: El archivo JSON fue leído y devuelto sin errores.
          content:
            application/json:
              schema:
                type: object
                description: Contenido completo del archivo JSON.
                additionalProperties:
                  type: string
        '404':
          description: El archivo JSON no fue encontrado.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "Archivo datos/entrega2/edificios.json no encontrado."
        '500':
          description: Error interno al procesar el archivo.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "Error al procesar el archivo: [mensaje de error]"
  /health:
    get:
      summary: Verificar el estado del servicio
      description: Comprueba si el servicio está funcionando correctamente.
      responses:
        '200':
          description: El servicio está funcionando correctamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    description: Estado del servicio.
                    example: "healthy"
                  service:
                    type: string
                    description: Nombre del servicio.
                    example: "EUS Monuments API"
