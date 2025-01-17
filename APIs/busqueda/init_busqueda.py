

from flask import Flask, render_template



api = Flask(__name__)

# 1) GET /carga -> Muestra la interfaz HTML
@api.get("/")
def mostrar_interfaz_html():
    """
    Muestra el formulario (templates/carga.html) para seleccionar
    qué fuentes cargar (CV, CLE, EUS...) y un botón "Cargar".
    """
    print("holi")
    return render_template("busqueda.html")
if __name__ == '__main__':
    # Levantamos la app en el puerto 5008
    api.run(debug=True, port=5008)
