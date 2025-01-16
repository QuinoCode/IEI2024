openapi: 3.0.0
info:
  title: CLE Monument API
  description: API to process and serve data from an XML file dynamically.
  version: 1.0.0
servers:
  - url: http://localhost:5003
    description: Local development server
paths:
  /getCLE:
    get:
      summary: Get processed data from the XML file
      description: Parses a dynamic XML file and returns its content as JSON. The structure of the response depends on the file used.
      responses:
        '200':
          description: Successfully parsed and returned XML data as JSON.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  description: A dynamic object representing the parsed XML data
                  additionalProperties:
                    type: string
        '400':
          description: Bad request, possibly due to XML parsing errors.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    description: Error message
                    example: "File not found or invalid format"
