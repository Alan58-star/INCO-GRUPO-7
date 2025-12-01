from flask import Flask, render_template, request, jsonify
import AAAAAAAAA  # tu archivo de reglas

app = Flask(__name__)

# Página principal (solo muestra el formulario)
@app.route("/", methods=["GET"])
def index():
    lista_materias = AAAAAAAAA.obtener_materias()
    return render_template("index.html", materias=lista_materias)


# Endpoint AJAX que no recarga la página
@app.route("/procesar", methods=["POST"])
def procesar():
    # Ejemplo: obtenés datos enviados desde JS
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    trabaja = request.form.get("trabaja")
    horario = request.form.get("horario")
    distancia = request.form.get("distancia")
    presupuesto = request.form.get("presupuesto")

    materias_aprobadas = request.form.getlist("materias_aprobadas")
    estrategias = request.form.getlist("estrategias")
    intereses = request.form.getlist("intereses")
    print(materias_aprobadas, edad,nombre,trabaja,horario,distancia,presupuesto,estrategias,intereses)
    # Ejecutás tus reglas
    resultado = AAAAAAAAA.mostrar_recomendaciones("EST001")

    return jsonify({
        "resultado": resultado
    })


if __name__ == "__main__":
    app.run(debug=True)

