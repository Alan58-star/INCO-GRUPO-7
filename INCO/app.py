from flask import Flask, render_template, request
import reglas
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def ejecutarConsulta():
    resultado = None
    if request.method == "POST":
        nombre = request.form["nombre"]
        q5=reglas.q5
        resultado = reglas.q5
    return render_template("index.html", resultado=resultado)
if __name__ == "__main__":
    app.run(debug=True)
