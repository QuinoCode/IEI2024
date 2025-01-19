

from flask import Flask, render_template



api = Flask(__name__)

# 1) GET Muestra la interfaz HTML
@api.get("/")
def mostrar_interfaz_html():
    # Usa busqueda.html como template y lo carga al llamar a localhost
    print("holi")
    return render_template("busqueda.html")
if __name__ == '__main__':
    # Levantamos la app en el puerto 5008
    api.run(debug=True, port=5008)
