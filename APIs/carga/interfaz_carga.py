

from flask import Flask, render_template, request, jsonify



api = Flask(__name__)

# 1) GET /carga -> Muestra la interfaz HTML
@api.get("/carga")
def mostrar_interfaz_html():
    """
    Muestra el formulario (templates/carga.html) para seleccionar
    qué fuentes cargar (CV, CLE, EUS...) y un botón "Cargar".
    """
    return render_template("carga.html")
if __name__ == '__main__':
    # Levantamos la app en el puerto 5001 (o el que prefieras)
    api.run(debug=True, port=5007)
