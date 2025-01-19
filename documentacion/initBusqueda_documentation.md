openapi: 3.0.3
info:
  title: "API para Interfaz de Búsqueda"
  description: "Una API simple que proporciona una interfaz HTML para búsquedas."
  version: "1.0.0"
  contact:
    name: "Desarrollador"
    email: "developer@example.com"

servers:
  - url: "http://localhost:5008"
    description: "Servidor local para desarrollo"

paths:
  /:
    get:
      summary: "Mostrar interfaz HTML"
      description: "Muestra la página HTML utilizando el template `busqueda.html`."
      responses:
        '200':
          description: "Página HTML cargada con éxito."
          content:
            text/html:
              schema:
                type: string
                example: "<html><body><h1>Interfaz de Búsqueda</h1></body></html>"
        '500':
          description: "Error del servidor al cargar la página HTML."
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Mensaje de error.
                    example: "Error interno del servidor."