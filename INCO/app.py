from flask import Flask, render_template, request
import AAAAAAAAA
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def ejecutarConsulta():
    resultado = None

    lista_materias = AAAAAAAAA.obtener_materias()

    if request.method == "POST":
        nombre = request.form["nombre"]
       
    return render_template("index.html", resultado=resultado, materias=lista_materias)
if __name__ == "__main__":
    app.run(debug=True)

