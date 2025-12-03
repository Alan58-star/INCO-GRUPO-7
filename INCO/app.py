from flask import Flask, render_template, request, jsonify
import motor  # Importamos nuestro motor.py

app = Flask(__name__)

# --- DICCIONARIOS DE MAPEO (HTML Values -> Ontology IDs) ---
# Esto es necesario porque en tu HTML los 'value' son genéricos.
MAPEO_ERRORES = {
    "programacion": "ERR_Procrastinacion",
    "diseno": "ERR_NoCronogramas",
    "matematicas": "ERR_SobrecargaMaterias",
    "idiomas": "ERR_EstudioUltimoDia",
    "investigacion": "ERR_IgnorarCorrelatividades"
}

MAPEO_ESTRATEGIAS = {
    "programacion": "EST_MicroEstudios",
    "diseno": "EST_RutinaSemanal",
    "matematicas": "EST_EstudioAnticipado",
    "idiomas": "EST_GrabarClases"
}

MAPEO_MODALIDAD = {
    "presencial": "MOD_Presencial",
    "virtual": "MOD_Virtual",
    "hibrida": "MOD_Hibrida"
}

MAPEO_TIEMPO = {
    "presencial": "TIEMPO_Bajo",   # Asumimos mapeo según orden del HTML
    "virtual": "TIEMPO_Medio",
    "hibrida": "TIEMPO_Alto"
}

@app.route("/", methods=["GET"])
def index():
    # Obtenemos las materias para pintar los checkboxes dinámicamente si quieres
    lista_materias = motor.obtener_todas_materias()
    return render_template("index.html", materias=lista_materias)

@app.route("/procesar", methods=["POST"])
def procesar():
    try:
        # 1. Recibir datos del formulario
        datos_html = {
            "nombre": request.form.get("nombre"),
            "nivel": request.form.get("nivel"),
            "trabaja": request.form.get("trabaja"), # si/no
            "holgura": request.form.get("horario"), # si/no (name='horario' en html)
            "distancia": request.form.get("distancia"), # si/no -> hay que convertir a string lógico
            "horas": request.form.get("horas"),
            "modalidad_raw": request.form.get("modalidad"),
            "tiempo_raw": request.form.get("tiempo"),
            "materias_aprobadas": request.form.getlist("materias_aprobadas"),
            "errores_raw": request.form.getlist("intereses"), # name='intereses' en html son los errores
            "estrategias_raw": request.form.getlist("estrategias")
        }

        # 2. Limpieza y Traducción de datos
        datos_procesados = {
            "nivel": datos_html["nivel"],
            "trabaja": datos_html["trabaja"],
            "holgura": datos_html["holgura"],
            # Lógica para distancia: si html dice "si" (vive lejos) -> "lejos", sino "cerca"
            "distancia": "lejos" if datos_html["distancia"] == "si" else "cerca",
            "horas": datos_html["horas"],
            "materias_aprobadas": datos_html["materias_aprobadas"],
            
            # Mapeos usando los diccionarios
            "modalidad": MAPEO_MODALIDAD.get(datos_html["modalidad_raw"]),
            "tiempo_estudio": MAPEO_TIEMPO.get(datos_html["tiempo_raw"]),
            "errores": [MAPEO_ERRORES.get(e) for e in datos_html["errores_raw"] if MAPEO_ERRORES.get(e)],
            "estrategias": [MAPEO_ESTRATEGIAS.get(e) for e in datos_html["estrategias_raw"] if MAPEO_ESTRATEGIAS.get(e)]
        }

        print("Datos procesados:", datos_procesados) # Debug

        # 3. Llamar al Motor
        # A) Crear perfil en el grafo
        id_estudiante = motor.crear_estudiante_y_razonar(datos_procesados)
        
        # B) Obtener resultados
        rec_estaticas = motor.obtener_recomendaciones_json(id_estudiante)
        rec_inferidas = motor.obtener_inferencias_json(id_estudiante)
        materias_disponibles = motor.obtener_materias_disponibles_json(id_estudiante)

        # 4. Responder JSON al Frontend
        return jsonify({
            "status": "success",
            "usuario": datos_html["nombre"],
            "recomendaciones": rec_estaticas + rec_inferidas, # Unimos ambas listas
            "materias_disponibles": materias_disponibles
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)