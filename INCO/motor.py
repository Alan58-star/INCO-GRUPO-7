import rdflib
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, RDFS, OWL, XSD
from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
import uuid
g = Graph()
EX = Namespace("http://miEX.sidad7.edu/ontologias#")
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("owl", OWL)

# ================================================================
# 1) DEFINIR CLASES
# ================================================================
clases = [
    "Estudiante", "TiempoEstudio", "CargaHoraria", "Materia",
    "Requisito", "Optativa", "Recomendacion", "EstrategiaEstudio",
    "ErrorFrecuente", "Modalidad"
]

for c in clases:
    g.add((EX[c], RDF.type, OWL.Class))

# Subclases de Materia
g.add((EX.MateriaBase, RDFS.subClassOf, EX.Materia))

# Subclases de Recomendacion
g.add((EX.RecomendacionIngresante, RDFS.subClassOf, EX.Recomendacion))
g.add((EX.RecomendacionIntermedio, RDFS.subClassOf, EX.Recomendacion))
g.add((EX.RecomendacionAvanzado, RDFS.subClassOf, EX.Recomendacion))


# ================================================================
# 2) DEFINIR PROPIEDADES
# ================================================================

# --- Object Properties ---
object_props = {
    "tieneTiempoEstudio": ("Estudiante", "TiempoEstudio"),
    "usaEstrategiaEstudio": ("Estudiante", "EstrategiaEstudio"),
    "cometeErrorFrecuente": ("Estudiante", "ErrorFrecuente"),
    "prefiereModalidad": ("Estudiante", "Modalidad"),
    "esCorrelativaDe": ("Materia", "Materia"),
    "tieneModalidad": ("Materia", "Modalidad"),
    "tieneSinergia": ("Materia", "Materia"),
    "materiaAprobada": ("Estudiante", "Materia"),
    "materiaRegular": ("Estudiante", "Materia"),
    "requiereError": ("Recomendacion", "ErrorFrecuente"),
    "requiereEstrategia": ("Recomendacion", "EstrategiaEstudio"),
    "requiereModalidad": ("Recomendacion", "Modalidad"),
    "requiereTiempoEstudio": ("Recomendacion", "TiempoEstudio"),
}

for p, (dom, ran) in object_props.items():
    g.add((EX[p], RDF.type, OWL.ObjectProperty))
    g.add((EX[p], RDFS.domain, EX[dom]))
    g.add((EX[p], RDFS.range, EX[ran]))

# --- Data Properties ---
data_props = {
    "trabaja": ("Estudiante", XSD.boolean),
    "tieneHolgura": ("Estudiante", XSD.boolean),
    "horasDisponiblesSemana": ("Estudiante", XSD.integer),
    "distanciaFacultad": ("Estudiante", XSD.string),
    "nivelAvance": ("Estudiante", XSD.string),
    "cargaHoraria": ("Materia", XSD.positiveInteger),
    "requiereTrabajo": ("Recomendacion", XSD.string),
    "requiereHolgura": ("Recomendacion", XSD.string),
    "requiereDistancia": ("Recomendacion", XSD.string),
    "prioridad": ("Recomendacion", XSD.integer),
    "anio": ("Materia", XSD.integer),
}

for prop, (dom, ran) in data_props.items():
    g.add((EX[prop], RDF.type, OWL.DatatypeProperty))
    g.add((EX[prop], RDFS.domain, EX[dom]))
    g.add((EX[prop], RDFS.range, ran))
# ================================================================
# 3) CREAR INDIVIDUOS - MATERIAS (AMPLIADO)
# ================================================================

materias = {
    # --- PRIMER AÑO (todas MOD_Hibrida) ---
    "MAT_1": ("Introducción a la Programación", 90, "MOD_Hibrida", 1),
    "MAT_2": ("Algebra Lineal", 90, "MOD_Presencial", 1),
    "MAT_3": ("Organización de Computadoras", 90, "MOD_Hibrida", 1),
    "MAT_4": ("Analisis Matematico I", 90, "MOD_Presencial", 1),
    
    "MAT_5": ("Metodología de la Programación", 90, "MOD_Hibrida", 1),
    "MAT_6": ("Análisis Matemático II", 90, "MOD_Hibrida", 1),
    "MAT_7": ("Física Mecánica", 90, "MOD_Hibrida", 1),
    "MAT_8": ("Estructura de Datos", 90, "MOD_Hibrida", 1),

    # --- SEGUNDO AÑO ---
    "MAT_9":  ("Matemática Discreta", 90, "MOD_Hibrida", 2),
    "MAT_10": ("Teoría de la Información y la Comunicación", 60, "MOD_Hibrida", 2),
    "MAT_11": ("Desarrollo Sistemático de Programas", 90, "MOD_Hibrida", 2),
    "MAT_12": ("Probabilidades y Estadística", 90, "MOD_Hibrida", 2),
    "MAT_13": ("Electricidad y Magnetismo", 90, "MOD_Presencial", 2),
    "MAT_14": ("Bases de Datos", 90, "MOD_Hibrida", 2),
    "MAT_15": ("Programación Concurrente", 90, "MOD_Virtual", 2),
    "MAT_16": ("Cálculo Numérico", 90, "MOD_Virtual", 2),

    # --- TERCER AÑO ---
    "MAT_17": ("Lógica Computacional", 60, "MOD_Presencial", 3),
    "MAT_18": ("Sistemas Operativos I", 90, "MOD_Virtual", 3),
    "MAT_19": ("Organización Empresarial y Modelos de Negocios", 90, "MOD_Virtual", 3),
    "MAT_20": ("Modelado Orientado a Objetos", 90, "MOD_Hibrida", 3),
    "MAT_21": ("Cursos Optativos (90h)", 90, "MOD_Hibrida", 3),
    "MAT_22": ("Teoría de Autómatas, Lenguajes y Computación", 90, "MOD_Hibrida", 3),
    "MAT_23": ("Sistemas Operativos II", 90, "MOD_Virtual", 3),
    "MAT_24": ("Métodos de Simulación", 60, "MOD_Virtual", 3),

    # --- CUARTO AÑO ---
    "MAT_25": ("Formulación y Evaluación de Proyectos Informáticos y Emprendedorismo Digital", 90, "MOD_Hibrida", 4),
    "MAT_26": ("Calidad del Software y Testing", 90, "MOD_Presencial", 4),
    "MAT_27": ("Arquitectura de Redes", 90, "MOD_Presencial", 4),
    "MAT_28": ("Ingeniería del Conocimiento", 90, "MOD_Hibrida", 4),
    "MAT_29": ("Arquitectura de Computadoras Paralelas", 60, "MOD_Presencial", 4),
    "MAT_30": ("Sistemas de Información", 90, "MOD_Presencial", 4),
    "MAT_31": ("Cursos Optativos (180h)", 180, "MOD_Hibrida", 4),
    "MAT_32": ("Seguridad y Auditoría Informática", 75, "MOD_Presencial", 4),

    # --- QUINTO AÑO ---
    "MAT_33": ("Ingeniería de Software I", 60, "MOD_Presencial", 5),
    "MAT_34": ("Sistemas Inteligentes", 90, "MOD_Hibrida", 5),
    "MAT_35": ("Legislación, Ética y Ejercicio Profesional", 75, "MOD_Presencial", 5),
    "MAT_36": ("Ingeniería de Software II", 60, "MOD_Presencial", 5),

    # --- OPTATIVAS ---
    "OPT_37": ("Compiladores", 90, "MOD_Hibrida", 3),
    "OPT_38": ("Aplicaciones de Bases de Datos I", 90, "MOD_Virtual", 3),
    "OPT_39": ("Aplicaciones de Bases de Datos II", 90, "MOD_Virtual", 3),
    "OPT_40": ("Introducción al Procesamiento Digital de Imágenes", 90, "MOD_Presencial", 3),
    "OPT_41": ("Inteligencia Artificial", 90, "MOD_Hibrida", 3),
    "OPT_42": ("Recuperación Avanzada de la Información", 90, "MOD_Virtual", 3),
    "OPT_43": ("Desarrollo y Arquitecturas Avanzadas de Software", 90, "MOD_Hibrida", 3),
    "OPT_44": ("Modelado y Proceso de Negocios", 90, "MOD_Hibrida", 3),
    "OPT_45": ("Taller de Formación Profesional", 60, "MOD_Hibrida", 3),
    "OPT_46": ("Taller de Metodología de la Investigación Científica", 60, "MOD_Hibrida", 3),
    "OPT_47": ("Gestión Ambiental", 60, "MOD_Hibrida", 3),

    # REQUISITOS
    "R1": ("Nivel de Suficiencia de Ingles", 0, "MOD_Hibrida", 0),
    "R2": ("Nivel de Aptitud de Ingles", 0, "MOD_Hibrida", 0),
    "R3": ("Todas las materias regulares hasta Cuarto", 0, "MOD_Hibrida", 0),
    # PRACTICA PROFESIONAL
    "PPS": ("Práctica Profesional Supervisada", 200, "MOD_Presencial", 5),
    # FINAL
    "TF": ("Trabajo Final", 200, "MOD_Presencial", 5),
}

def obtener_materias():
    """
    Devuelve una lista de diccionarios:
    [{ "codigo": "MAT_1", "nombre": "Introducción a la Programación" }, ...]
    """
    lista = []
    for codigo, (nombre, carga, modalidad, anio) in materias.items():
        lista.append({
            "codigo": codigo,
            "nombre": nombre,
            "carga": carga,
            "modalidad": modalidad,
            "anio": anio
        })
    return lista


# Crear materias regulares
for id, (nombre, carga, modalidad, anio) in materias.items():
    g.add((EX[id], RDF.type, EX.Materia))
    g.add((EX[id], RDFS.label, Literal(nombre)))
    g.add((EX[id], EX.cargaHoraria, Literal(carga, datatype=XSD.positiveInteger)))
    g.add((EX[id], EX.tieneModalidad, EX[modalidad]))
    g.add((EX[id], EX.anio, Literal(anio, datatype=XSD.integer)))

# ================================================================
# 4) MODALIDADES, ERRORES, ESTRATEGIAS, TIEMPOS
# ================================================================
modalidades = {
    "MOD_Virtual": "Modalidad Virtual",
    "MOD_Presencial": "Modalidad Presencial",
    "MOD_Hibrida": "Modalidad Hibrida"
}

for id, nombre in modalidades.items():
    g.add((EX[id], RDF.type, EX.Modalidad))
    g.add((EX[id], RDFS.label, Literal(nombre)))

errores_frecuentes = {
    "ERR_Procrastinacion": "Procrastinacion antes de parciales",
    "ERR_NoCronogramas": "No revisar cronogramas",
    "ERR_SobrecargaMaterias": "Inscribirse en demasiadas materias",
    "ERR_EstudioUltimoDia": "Estudiar el ultimo dia",
    "ERR_IgnorarCorrelatividades": "Ignorar correlatividades",
}

for id, nombre in errores_frecuentes.items():
    g.add((EX[id], RDF.type, EX.ErrorFrecuente))
    g.add((EX[id], RDFS.label, Literal(nombre)))

estrategias_estudio = {
    "EST_MicroEstudios": "Micro-estudios de 25-30 minutos",
    "EST_RutinaSemanal": "Rutina semanal estricta",
    "EST_EstudioAnticipado": "Estudiar con anticipacion",
    "EST_GrabarClases": "Grabar clases para revisar",
}

for id, nombre in estrategias_estudio.items():
    g.add((EX[id], RDF.type, EX.EstrategiaEstudio))
    g.add((EX[id], RDFS.label, Literal(nombre)))

tiempos_estudio = {
    "TIEMPO_Bajo": "Menos de 10 horas semanales",
    "TIEMPO_Medio": "Entre 10 y 20 horas semanales",
    "TIEMPO_Alto": "Mas de 20 horas semanales"
}

for id, nombre in tiempos_estudio.items():
    g.add((EX[id], RDF.type, EX.TiempoEstudio))
    g.add((EX[id], RDFS.label, Literal(nombre)))

# ================================================================
# 5) RECOMENDACIONES CON METADATOS
# ================================================================
recomendaciones_ing = {
    "REC_I1": {
        "texto": "Planificar dias enfocados en las materias",
        "trabaja": "no",
        "distancia": None,
        "holgura": "si",
        "prioridad": 1
    },
    "REC_I2": {
        "texto": "Aprovechar cercania a la facultad para estudiar en biblioteca",
        "trabaja": None,
        "distancia": "cerca",
        "holgura": None,
        "prioridad": 2
    },
    "REC_I3": {
        "texto": "Estudiar durante el viaje (lecturas, resumenes, videos)",
        "trabaja": None,
        "distancia": "lejos",
        "holgura": None,
        "prioridad": 2
    },
    "REC_I5": {
        "texto": "Conversar en el trabajo la posibilidad de flexibilizar dias clave",
        "trabaja": "si",
        "distancia": None,
        "holgura": "no",
        "prioridad": 3
    },
    "REC_I6": {
        "texto": "Usar los huecos del trabajo para estudiar en biblioteca",
        "trabaja": "si",
        "distancia": "cerca",
        "holgura": None,
        "prioridad": 2
    },
    "REC_I7": {
        "texto": "Mantener un equilibrio saludable para evitar burnout",
        "trabaja": "si",
        "distancia": None,
        "holgura": "no",
        "prioridad": 4
    },
    "REC_I8": {
        "texto": "Mantener una rutina semanal estricta para estudiar en horarios fijos",
        "trabaja": "no",
        "distancia": None,
        "holgura": "si",
        "prioridad": 1
    },
}

recomendaciones_int = {
    "REC_M1": {
        "texto": "Estudiar con anticipacion y revisar cronogramas de examenes y actividades",
        "trabaja": None,
        "distancia": None,
        "holgura": None,
        "prioridad": 1
    },
    "REC_M2": {
        "texto": "Aprovechar la cercania para asistir a clases presenciales",
        "trabaja": None,
        "distancia": "cerca",
        "holgura": None,
        "prioridad": 2
    },
    "REC_M3": {
        "texto": "Reorganizar los viajes para cursar varios dias seguidos",
        "trabaja": None,
        "distancia": "lejos",
        "holgura": None,
        "prioridad": 2
    },
    "REC_M5": {
        "texto": "Organizarse con micro-estudios de 25-30 min diarios",
        "trabaja": "si",
        "distancia": None,
        "holgura": "no",
        "prioridad": 3
    },
    "REC_M7": {
        "texto": "Inscribirse solo en materias esenciales o correlativas de avance",
        "trabaja": "si",
        "distancia": None,
        "holgura": "no",
        "prioridad": 2
    },
    "REC_M8": {
        "texto": "Priorizar materias virtuales y grabar clases",
        "trabaja": "si",
        "distancia": "lejos",
        "holgura": None,
        "prioridad": 3
    },
}

recomendaciones_avan = {
    "REC_A1": {
        "texto": "Identificar de donde viene la falta de tiempo y corregir desviaciones",
        "trabaja": None,
        "distancia": None,
        "holgura": "no",
        "prioridad": 1
    },
    "REC_A2": {
        "texto": "Enfocar materias de años anteriores para cumplir requisitos de PPS y TF",
        "trabaja": None,
        "distancia": None,
        "holgura": None,
        "prioridad": 1
    },
    "REC_A3": {
        "texto": "Buscar material de años anteriores",
        "trabaja": None,
        "distancia": None,
        "holgura": None,
        "prioridad": 2
    },
    "REC_A6": {
        "texto": "Preparar y organizar mesas de examenes de materias pendientes",
        "trabaja": None,
        "distancia": None,
        "holgura": None,
        "prioridad": 1
    },
    "REC_A7": {
        "texto": "Negociar con el trabajo dias de estudio previos a parciales",
        "trabaja": "si",
        "distancia": None,
        "holgura": "no",
        "prioridad": 3
    },
    "REC_A8": {
        "texto": "Organizar viajes solo para las clases obligatorias",
        "trabaja": None,
        "distancia": "lejos",
        "holgura": "no",
        "prioridad": 2
    },
}

# Cargar recomendaciones con metadatos
def agregar_recomendaciones(recom_dict, tipo_clase):
    for id, data in recom_dict.items():
        g.add((EX[id], RDF.type, tipo_clase))
        g.add((EX[id], RDFS.label, Literal(data["texto"])))
        g.add((EX[id], EX.prioridad, Literal(data["prioridad"], datatype=XSD.integer)))
        
        if data["trabaja"] is not None:
            g.add((EX[id], EX.requiereTrabajo, Literal(data["trabaja"])))
        if data["holgura"] is not None:
            g.add((EX[id], EX.requiereHolgura, Literal(data["holgura"])))
        if data["distancia"] is not None:
            g.add((EX[id], EX.requiereDistancia, Literal(data["distancia"])))

agregar_recomendaciones(recomendaciones_ing, EX.RecomendacionIngresante)
agregar_recomendaciones(recomendaciones_int, EX.RecomendacionIntermedio)
agregar_recomendaciones(recomendaciones_avan, EX.RecomendacionAvanzado)

# ================================================================
# 6) CORRELATIVIDADES (AMPLIADO Y REALISTA)
# ================================================================

# Primer año → Segundo año
g.add((EX.MAT_1, EX.esCorrelativaDe, EX.MAT_5))
g.add((EX.MAT_1, EX.esCorrelativaDe, EX.MAT_8))
g.add((EX.MAT_2, EX.esCorrelativaDe, EX.MAT_9))
g.add((EX.MAT_2, EX.esCorrelativaDe, EX.MAT_7))
g.add((EX.MAT_4, EX.esCorrelativaDe, EX.MAT_6))
g.add((EX.MAT_4, EX.esCorrelativaDe, EX.MAT_7))

# Segundo año → Tercer año
g.add((EX.MAT_3, EX.esCorrelativaDe, EX.MAT_10))
g.add((EX.MAT_5, EX.esCorrelativaDe, EX.MAT_11))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_11))
g.add((EX.MAT_2, EX.esCorrelativaDe, EX.MAT_12))
g.add((EX.MAT_6, EX.esCorrelativaDe, EX.MAT_12))
g.add((EX.MAT_7, EX.esCorrelativaDe, EX.MAT_13))
g.add((EX.MAT_5, EX.esCorrelativaDe, EX.MAT_14))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_14))
g.add((EX.MAT_5, EX.esCorrelativaDe, EX.MAT_15))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_15))
g.add((EX.MAT_6, EX.esCorrelativaDe, EX.MAT_16))

# Tercer año → Cuarto año
g.add((EX.MAT_2, EX.esCorrelativaDe, EX.MAT_17))
g.add((EX.MAT_3, EX.esCorrelativaDe, EX.MAT_18))
g.add((EX.MAT_5, EX.esCorrelativaDe, EX.MAT_18))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_18))
g.add((EX.MAT_5, EX.esCorrelativaDe, EX.MAT_19))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_19))
g.add((EX.MAT_15, EX.esCorrelativaDe, EX.MAT_20))
g.add((EX.MAT_8, EX.esCorrelativaDe, EX.MAT_22))
g.add((EX.MAT_17, EX.esCorrelativaDe, EX.MAT_22))
g.add((EX.MAT_18, EX.esCorrelativaDe, EX.MAT_23))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.MAT_24))
g.add((EX.MAT_16, EX.esCorrelativaDe, EX.MAT_24))

# Cuarto año → Quinto año
g.add((EX.MAT_19, EX.esCorrelativaDe, EX.MAT_25))
g.add((EX.MAT_20, EX.esCorrelativaDe, EX.MAT_26))
g.add((EX.MAT_23, EX.esCorrelativaDe, EX.MAT_27))
g.add((EX.MAT_17, EX.esCorrelativaDe, EX.MAT_28))
g.add((EX.MAT_20, EX.esCorrelativaDe, EX.MAT_28))
g.add((EX.MAT_23, EX.esCorrelativaDe, EX.MAT_29))
g.add((EX.MAT_27, EX.esCorrelativaDe, EX.MAT_29))
g.add((EX.MAT_20, EX.esCorrelativaDe, EX.MAT_30))
g.add((EX.MAT_23, EX.esCorrelativaDe, EX.MAT_32))

# Quinto Año
g.add((EX.MAT_30, EX.esCorrelativaDe, EX.MAT_33))
g.add((EX.MAT_9, EX.esCorrelativaDe, EX.MAT_34))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.MAT_34))
g.add((EX.MAT_16, EX.esCorrelativaDe, EX.MAT_34))
g.add((EX.MAT_33, EX.esCorrelativaDe, EX.MAT_36))

g.add((EX.R1, EX.esCorrelativaDe, EX.MAT_28))  
g.add((EX.R1, EX.esCorrelativaDe, EX.MAT_29))  
g.add((EX.R1, EX.esCorrelativaDe, EX.MAT_30))  
g.add((EX.R1, EX.esCorrelativaDe, EX.MAT_32))  

g.add((EX.R2, EX.esCorrelativaDe, EX.MAT_33))  
g.add((EX.R2, EX.esCorrelativaDe, EX.MAT_34))  
g.add((EX.R2, EX.esCorrelativaDe, EX.MAT_35))  
for c in range(1, 33):
    g.add((EX["MAT_" + str(c)], EX.esCorrelativaDe, EX.R3))

g.add((EX.MAT_27, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_28, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_29, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_30, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_32, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria

g.add((EX.R3, EX.esCorrelativaDe, EX.PPS))
g.add((EX.R3, EX.esCorrelativaDe, EX.TF))

for m in ["MAT_33", "MAT_34", "MAT_35"]:
    g.add((EX.MAT_31, EX.esCorrelativaDe, EX[m]))

for opt in ["OPT_37","OPT_38","OPT_39","OPT_40","OPT_41","OPT_42","OPT_43","OPT_44","OPT_45","OPT_46","OPT_47"]:
    g.add((EX[opt], EX.esCorrelativaDe, EX.MAT_21))
    g.add((EX[opt], EX.esCorrelativaDe, EX.MAT_31))

for m in ["OPT_37", "OPT_40"]:
    g.add((EX.MAT_15, EX.esCorrelativaDe, EX[m]))

for m in ["OPT_38", "OPT_39"]:
    g.add((EX.MAT_14, EX.esCorrelativaDe, EX[m]))

for m in ["OPT_41"]:
    g.add((EX.MAT_22, EX.esCorrelativaDe, EX[m]))

for m in ["OPT_42", "OPT_43"]:
    g.add((EX.MAT_20, EX.esCorrelativaDe, EX[m]))

for m in ["OPT_44"]:
    g.add((EX.MAT_19, EX.esCorrelativaDe, EX[m]))

g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_45))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_46))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_47))
# ================================================================
# 7) AXIOMAS OWL
# ================================================================
g.add((EX.tieneSinergia, RDF.type, OWL.SymmetricProperty))
g.add((EX.esCorrelativaDe, RDF.type, OWL.TransitiveProperty))

# Aplicar razonador
DeductiveClosure(OWLRL_Semantics).expand(g)

# ================================================================
# 8) FUNCIONES DE CONSULTA Y RECOMENDACIÓN
# ================================================================
def crear_estudiante_y_razonar(datos):
    """
    Crea un estudiante temporal, ejecuta el razonador y devuelve resultados.
    Usa un ID único para no mezclar peticiones.
    """
    id_est = f"EST_{uuid.uuid4().hex[:8]}"
    
    # 1. Crear Estudiante
    g.add((EX[id_est], RDF.type, EX.Estudiante))
    g.add((EX[id_est], EX.nivelAvance, Literal(datos['nivel'])))
    
    # Booleanos
    g.add((EX[id_est], EX.trabaja, Literal(datos['trabaja'] == "si", datatype=XSD.boolean)))
    g.add((EX[id_est], EX.tieneHolgura, Literal(datos['holgura'] == "si", datatype=XSD.boolean)))
    g.add((EX[id_est], EX.distanciaFacultad, Literal(datos['distancia']))) # "cerca" o "lejos"
    g.add((EX[id_est], EX.horasDisponiblesSemana, Literal(int(datos['horas']), datatype=XSD.integer)))
    
    # Listas
    for error in datos['errores']:
        g.add((EX[id_est], EX.cometeErrorFrecuente, EX[error]))
    
    for est in datos['estrategias']:
        g.add((EX[id_est], EX.usaEstrategiaEstudio, EX[est]))
        
    for mat in datos['materias_aprobadas']:
        g.add((EX[id_est], EX.materiaAprobada, EX[mat]))

    if datos['modalidad']:
        g.add((EX[id_est], EX.prefiereModalidad, EX[datos['modalidad']]))
        
    if datos['tiempo_estudio']:
        g.add((EX[id_est], EX.tieneTiempoEstudio, EX[datos['tiempo_estudio']]))

    # 2. Aplicar Razonador (Solo expansión simple si es necesario, o confiar en SPARQL)
    # DeductiveClosure(OWLRL_Semantics).expand(g) # Opcional: puede ser lento en cada request. 
    # Usaremos SPARQL directo que es más rápido para web.

    return id_est

def obtener_recomendaciones_json(id_estudiante):
    """Devuelve lista de diccionarios con recomendaciones estáticas"""
    # Recuperar perfil para explicar
    perfil_query = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    SELECT ?nivel ?trabaja ?holgura ?distancia
    WHERE {{ ex:{id_estudiante} ex:nivelAvance ?nivel ; ex:trabaja ?trabaja ; 
             ex:tieneHolgura ?holgura ; ex:distanciaFacultad ?distancia . }}
    """
    p_res = list(g.query(perfil_query))
    if not p_res: return []
    
    nivel, trabaja, holgura, distancia = p_res[0]
    trabaja_str = "si" if trabaja.toPython() else "no"
    holgura_str = "si" if holgura.toPython() else "no"
    distancia_str = str(distancia)
    
    tipo_rec = "ex:RecomendacionIngresante" if str(nivel) == "ingresante" else \
               "ex:RecomendacionIntermedio" if str(nivel) == "intermedio" else "ex:RecomendacionAvanzado"

    query = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?recomendacion ?texto ?prioridad ?reqTrabajo ?reqHolgura ?reqDistancia
    WHERE {{
        ?recomendacion rdf:type {tipo_rec} ; rdfs:label ?texto ; ex:prioridad ?prioridad .
        OPTIONAL {{ ?recomendacion ex:requiereTrabajo ?reqTrabajo }}
        OPTIONAL {{ ?recomendacion ex:requiereHolgura ?reqHolgura }}
        OPTIONAL {{ ?recomendacion ex:requiereDistancia ?reqDistancia }}
        FILTER(
            (!BOUND(?reqTrabajo) || ?reqTrabajo = "{trabaja_str}") &&
            (!BOUND(?reqHolgura) || ?reqHolgura = "{holgura_str}") &&
            (!BOUND(?reqDistancia) || ?reqDistancia = "{distancia_str}")
        )
    }} ORDER BY ?prioridad
    """
    
    results = []
    for row in g.query(query):
        rec, texto, prio, rt, rh, rd = row
        motivos = []
        if rt: motivos.append(f"trabajas ({rt})")
        if rh: motivos.append(f"tienes holgura ({rh})")
        if rd: motivos.append(f"distancia es {rd}")
        
        explicacion = "Sugerencia general para tu nivel."
        if motivos: explicacion = "Porque " + " y ".join(motivos) + "."
        
        results.append({
            "tipo": "Consejo",
            "texto": str(texto),
            "explicacion": explicacion,
            "prioridad": int(prio)
        })
    return results

def obtener_inferencias_json(id_estudiante):
    """Devuelve lista de diccionarios con reglas inferidas"""
    reglas = [
        # (Aquí van tus strings de queries CONSTRUCT de las reglas R1 a R9...)
        # COPIA LAS REGLAS QUE TE DI EN LA RESPUESTA ANTERIOR (CON EL MOTIVO)
        # Ejemplo abreviado:
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada "Usar micro-estudios" .
            ?estudiante ex:motivoGenerado "Detectado error: Procrastinación." 
        } WHERE { ?estudiante ex:cometeErrorFrecuente ex:ERR_Procrastinacion . }
        """,
        # ... Agrega el resto de reglas R2 a R10 aquí ...
    ]
    
    inferencias = []
    for r in reglas:
        res = g.query(r)
        temp_g = Graph()
        for t in res: temp_g.add(t)
        
        q = f"PREFIX ex: <http://miEX.sidad7.edu/ontologias#> SELECT ?rec ?mot WHERE {{ ex:{id_estudiante} ex:recomendacionGenerada ?rec . OPTIONAL {{ ex:{id_estudiante} ex:motivoGenerado ?mot }} }}"
        
        for row in temp_g.query(q):
            inferencias.append({
                "tipo": "Estrategia/Alerta",
                "texto": str(row[0]),
                "explicacion": str(row[1]) if row[1] else "Regla lógica activada.",
                "prioridad": 0
            })
    return inferencias

def obtener_materias_disponibles_json(id_estudiante):
    """Devuelve materias que puede cursar ya"""
    # (Usa la lógica de tu función obtener_materias_disponibles_para_cursar pero devuelve dict)
    # Asumo que tienes la función original, solo cambiamos el return:
    
    # ... Logica de query ...
    # Supongamos que llamas a tu funcion original y obtienes una lista de tuplas
    # lista_tuplas = obtener_materias_disponibles_para_cursar(id_estudiante) 
    
    # AQUI SIMULO LA LLAMADA (Debes integrar tu query original aqui)
    query = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?materia ?nombre ?modalidad ?anio
    WHERE {{
        {{ ?materia a ex:Materia }} UNION {{ ?materia a ex:MateriaBase }}
        ?materia rdfs:label ?nombre ; ex:anio ?anio .
        OPTIONAL {{ ?materia ex:tieneModalidad ?mObj . ?mObj rdfs:label ?modalidad }}
        FILTER NOT EXISTS {{ ex:{id_estudiante} ex:materiaAprobada ?materia }}
        FILTER NOT EXISTS {{ 
            ?correlativa ex:esCorrelativaDe ?materia . 
            FILTER NOT EXISTS {{ ex:{id_estudiante} ex:materiaAprobada ?correlativa }}
        }}
    }} ORDER BY ?anio
    """
    
    materias = []
    for row in g.query(query):
        materias.append({
            "codigo": str(row[0]).split("#")[-1],
            "nombre": str(row[1]),
            "modalidad": str(row[2]) if row[2] else "N/A",
            "anio": int(row[3])
        })
    return materias

def obtener_todas_materias():
    """Para llenar el checkbox del frontend"""
    q = """PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
           SELECT ?id ?lbl WHERE { ?s a ex:Materia ; rdfs:label ?lbl . BIND(STRAFTER(STR(?s), "#") AS ?id) } ORDER BY ?lbl"""
    return [{"codigo": str(r[0]), "nombre": str(r[1])} for r in g.query(q)]

def crear_estudiante(id_est, nivel, trabaja, holgura, distancia, horas_sem, 
                    errores=None, estrategias=None, modalidad_pref=None, 
                    tiempo_est=None, materias_aprobadas=None):
    """Crea un perfil completo de estudiante en la ontología"""
    g.add((EX[id_est], RDF.type, EX.Estudiante))
    g.add((EX[id_est], EX.nivelAvance, Literal(nivel)))
    
    # Convertir booleanos a strings para consistencia
    trabaja_str = "si" if trabaja else "no"
    holgura_str = "si" if holgura else "no"
    
    g.add((EX[id_est], EX.trabaja, Literal(trabaja, datatype=XSD.boolean)))
    g.add((EX[id_est], EX.tieneHolgura, Literal(holgura, datatype=XSD.boolean)))
    g.add((EX[id_est], EX.distanciaFacultad, Literal(distancia)))
    g.add((EX[id_est], EX.horasDisponiblesSemana, Literal(horas_sem, datatype=XSD.integer)))
    
    if errores:
        for error in errores:
            g.add((EX[id_est], EX.cometeErrorFrecuente, EX[error]))
    
    if estrategias:
        for estrategia in estrategias:
            g.add((EX[id_est], EX.usaEstrategiaEstudio, EX[estrategia]))
    
    if modalidad_pref:
        g.add((EX[id_est], EX.prefiereModalidad, EX[modalidad_pref]))
    
    if tiempo_est:
        g.add((EX[id_est], EX.tieneTiempoEstudio, EX[tiempo_est]))
    
    if materias_aprobadas:
        for materia in materias_aprobadas:
            g.add((EX[id_est], EX.materiaAprobada, EX[materia]))
    
    print(f"[OK] Estudiante {id_est} creado:")
    print(f"     Nivel: {nivel}, Trabaja: {trabaja_str}, Distancia: {distancia}, Holgura: {holgura_str}")

    if materias_aprobadas:
        print(f"     Materias aprobadas: {len(materias_aprobadas)}")

def obtener_recomendaciones(id_estudiante):
    """Obtiene recomendaciones personalizadas CON EXPLICACIÓN"""
    # 1. Obtenemos el perfil del estudiante
    perfil_query = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    SELECT ?nivel ?trabaja ?holgura ?distancia
    WHERE {{
        ex:{id_estudiante} ex:nivelAvance ?nivel ;
                        ex:trabaja ?trabaja ;
                        ex:tieneHolgura ?holgura ;
                        ex:distanciaFacultad ?distancia .
    }}
    """
    perfil_result = list(g.query(perfil_query))
    if not perfil_result:
        return []

    nivel, trabaja, holgura, distancia = perfil_result[0]
    trabaja_str = "si" if trabaja.toPython() else "no"
    holgura_str = "si" if holgura.toPython() else "no"
    distancia_str = str(distancia)

    # Definir tipo de recomendación según nivel
    if str(nivel) == "ingresante":
        tipo_rec = "ex:RecomendacionIngresante"
    elif str(nivel) == "intermedio":
        tipo_rec = "ex:RecomendacionIntermedio"
    else:
        tipo_rec = "ex:RecomendacionAvanzado"

    # 2. Query modificada para traer los requisitos de la recomendación
    query = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?recomendacion ?texto ?prioridad ?reqTrabajo ?reqHolgura ?reqDistancia
    WHERE {{
        ?recomendacion rdf:type {tipo_rec} ;
                    rdfs:label ?texto ;
                    ex:prioridad ?prioridad .
        
        OPTIONAL {{ ?recomendacion ex:requiereTrabajo ?reqTrabajo }}
        OPTIONAL {{ ?recomendacion ex:requiereHolgura ?reqHolgura }}
        OPTIONAL {{ ?recomendacion ex:requiereDistancia ?reqDistancia }}
        
        FILTER(
            (!BOUND(?reqTrabajo) || ?reqTrabajo = "{trabaja_str}") &&
            (!BOUND(?reqHolgura) || ?reqHolgura = "{holgura_str}") &&
            (!BOUND(?reqDistancia) || ?reqDistancia = "{distancia_str}")
        )
    }}
    ORDER BY ?prioridad
    """

    resultados_raw = list(g.query(query))
    recomendaciones_explicadas = []

    # 3. Procesamiento en Python para generar la explicación "human-readable"
    for row in resultados_raw:
        rec, texto, prioridad, req_trabajo, req_holgura, req_distancia = row
        
        motivos = []
        if req_trabajo:
            motivos.append(f"tu situación laboral es '{req_trabajo}'")
        if req_holgura:
            motivos.append(f"tu disponibilidad horaria es '{req_holgura}' (holgura)")
        if req_distancia:
            motivos.append(f"vives '{req_distancia}' de la facultad")
        
        # Si no tiene requisitos específicos, es una recomendación general para el nivel
        explicacion = "Recomendación general para tu nivel de avance."
        if motivos:
            explicacion = "Se sugiere porque " + " y ".join(motivos) + "."

        recomendaciones_explicadas.append({
            "id": str(rec).split("#")[-1],
            "texto": str(texto),
            "prioridad": prioridad,
            "explicacion": explicacion
        })

    return recomendaciones_explicadas

def obtener_materias_restantes(id_estudiante):
    """Obtiene las materias que AÚN NO HA APROBADO el estudiante"""
    query_aprobadas = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    SELECT ?materia
    WHERE {{
        ex:{id_estudiante} ex:materiaAprobada ?materia .
    }}
    """

    aprobadas_result = list(g.query(query_aprobadas))
    aprobadas = [str(row[0]).split("#")[-1] for row in aprobadas_result]

    query_todas = """
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?materia ?nombre ?modalidad ?anio ?carga
    WHERE {
        { ?materia a ex:Materia } UNION { ?materia a ex:MateriaBase }
        ?materia rdfs:label ?nombre ;
                ex:anio ?anio ;
                ex:cargaHoraria ?carga .
        OPTIONAL { 
            ?materia ex:tieneModalidad ?mod_obj .
            ?mod_obj rdfs:label ?modalidad 
        }
    }
    ORDER BY ?anio ?nombre
    """

    todas = list(g.query(query_todas))

    restantes = []
    for mat, nombre, modalidad, anio, carga in todas:
        mat_id = str(mat).split("#")[-1]
        if mat_id not in aprobadas:
            restantes.append((mat, nombre, modalidad, anio, carga, mat_id))

    return restantes, aprobadas

def obtener_materias_disponibles_para_cursar(id_estudiante):
    """Obtiene las materias que puede cursar AHORA (correlativas cumplidas)"""
    query_aprobadas = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    SELECT ?materia
    WHERE {{
        ex:{id_estudiante} ex:materiaAprobada ?materia .
    }}
    """

    aprobadas_result = list(g.query(query_aprobadas))
    aprobadas = [str(row[0]).split("#")[-1] for row in aprobadas_result]

    if not aprobadas:
        query_sin_correlativas = """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?materia ?nombre ?modalidad ?anio
        WHERE {
            { ?materia a ex:Materia } UNION { ?materia a ex:MateriaBase }
            ?materia rdfs:label ?nombre ;
                    ex:anio ?anio .
            OPTIONAL { 
                ?materia ex:tieneModalidad ?mod_obj .
                ?mod_obj rdfs:label ?modalidad 
            }
            
            FILTER NOT EXISTS {
                ?cualquier ex:esCorrelativaDe ?materia .
            }
        }
        ORDER BY ?anio ?nombre
        """
        return list(g.query(query_sin_correlativas))

    aprobadas_uris = ", ".join([f"ex:{m}" for m in aprobadas])

    query_disponibles = f"""
    PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?materia ?nombre ?modalidad ?anio
    WHERE {{
        {{ ?materia a ex:Materia }} UNION {{ ?materia a ex:MateriaBase }}
        ?materia rdfs:label ?nombre ;
                ex:anio ?anio .
        OPTIONAL {{ 
            ?materia ex:tieneModalidad ?mod_obj .
            ?mod_obj rdfs:label ?modalidad 
        }}
        
        FILTER(?materia NOT IN ({aprobadas_uris}))
        
        FILTER NOT EXISTS {{
            ?correlativa ex:esCorrelativaDe ?materia .
            FILTER(?correlativa NOT IN ({aprobadas_uris}))
        }}
    }}
    ORDER BY ?anio ?nombre
    """
    return list(g.query(query_disponibles))

def mostrar_recomendaciones(id_estudiante):
    """Muestra las recomendaciones personalizadas con explicaciones"""
    print(f"\n{'='*70}")
    print(f"RECOMENDACIONES PARA ESTUDIANTE: {id_estudiante}")
    print(f"{'='*70}\n")
    recomendaciones = obtener_recomendaciones(id_estudiante)
    
    if not recomendaciones:
        print("No se encontraron recomendaciones para este perfil.")
    else:
        for i, item in enumerate(recomendaciones, 1):
            print(f"{i}. [{item['id']}] (Prioridad {item['prioridad']})")
            print(f"   SUGERENCIA: {item['texto']}")
            print(f"   POR QUÉ:    {item['explicacion']}\n")
        
        print(f"Total de recomendaciones: {len(recomendaciones)}")

def mostrar_materias_restantes(id_estudiante):
    """Muestra solo las materias que AÚN NO HA APROBADO"""
    print(f"\n{'='*70}")
    print(f"MATERIAS RESTANTES POR CURSAR: {id_estudiante}")
    print(f"{'='*70}\n")
    restantes, aprobadas = obtener_materias_restantes(id_estudiante)
    if not restantes:
        print("¡Felicitaciones! Has aprobado todas las materias.")
        return

    por_anio = {}
    for mat, nombre, modalidad, anio, carga, mat_id in restantes:
        anio_val = int(anio)
        if anio_val not in por_anio:
            por_anio[anio_val] = []
        por_anio[anio_val].append((mat_id, nombre, modalidad, carga))

    for anio in sorted(por_anio.keys()):
        print(f"\n  AÑO {anio}:")
        print(f"  {'-'*66}")
        for mat_id, nombre, modalidad, carga in por_anio[anio]:
            mod_str = f" [{modalidad}]" if modalidad else ""
            print(f"  • [{mat_id}] {nombre}{mod_str} ({carga}hs)")

    print(f"\n{'='*70}")
    print(f"Total materias restantes: {len(restantes)}")
    print(f"Materias aprobadas: {len(aprobadas)}")
    total_materias = len(restantes) + len(aprobadas)
    porcentaje = (len(aprobadas) / total_materias * 100) if total_materias > 0 else 0
    print(f"Progreso de carrera: {porcentaje:.1f}%")
    print(f"{'='*70}")

def mostrar_materias_disponibles_para_cursar(id_estudiante):
    """Muestra las materias que puede cursar ahora"""
    print(f"\n{'='*70}")
    print(f"MATERIAS DISPONIBLES PARA CURSAR AHORA: {id_estudiante}")
    print(f"{'='*70}\n")
    materias = obtener_materias_disponibles_para_cursar(id_estudiante)
    if not materias:
        print("No hay materias disponibles para cursar en este momento.")
    else:
        for i, (mat, nombre, modalidad, anio) in enumerate(materias, 1):
            mat_id = str(mat).split("#")[-1]
            mod_str = f" [{modalidad}]" if modalidad else ""
            print(f"{i}. [{mat_id}] {nombre}{mod_str} (Año {anio})")
        
        print(f"\nTotal de materias que puedes cursar: {len(materias)}")

# ================================================================
# 9) REGLAS DE INFERENCIA CON CONSTRUCT
# ================================================================

def aplicar_reglas_recomendacion(id_estudiante):
    """
    Aplica reglas CONSTRUCT y extrae la explicación de por qué se disparó la regla.
    """
    print(f"\n{'='*70}")
    print(f"REGLAS DE INFERENCIA APLICADAS (Lógica Deductiva): {id_estudiante}")
    print(f"{'='*70}\n")
    
    # Definimos las reglas inyectando el motivo explícito
    reglas = [
        # R1: Procrastinación
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_MicroEstudios .
            ?estudiante ex:recomendacionGenerada "Usar micro-estudios para evitar procrastinación" .
            ?estudiante ex:motivoGenerado "Detectado error frecuente: Procrastinación." .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_Procrastinacion .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_MicroEstudios }
        }
        """,
        
        # R2: No cronogramas
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_EstudioAnticipado .
            ?estudiante ex:recomendacionGenerada "Implementar estudio anticipado" .
            ?estudiante ex:motivoGenerado "Detectado error: No revisar cronogramas." .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_NoCronogramas .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_EstudioAnticipado }
        }
        """,
        
        # R3: Estudio último día
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_RutinaSemanal .
            ?estudiante ex:recomendacionGenerada "Establecer rutina semanal estricta" .
            ?estudiante ex:motivoGenerado "Detectado hábito de estudiar el último día." .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_EstudioUltimoDia .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_RutinaSemanal }
        }
        """,
        
        # R4: Preferencia Virtual
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada ?textoRec .
            ?estudiante ex:motivoGenerado "Coincidencia: Prefieres modalidad Virtual y la materia es Virtual." .
        }
        WHERE {
            ?estudiante ex:prefiereModalidad ex:MOD_Virtual .
            ?materia ex:tieneModalidad ex:MOD_Virtual .
            ?materia rdfs:label ?nombreMateria .
            
            # Verificar que puede cursarla (no aprobada y correlativas ok)
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("Priorizar materia virtual: ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R5: Preferencia Presencial
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada ?textoRec .
            ?estudiante ex:motivoGenerado "Coincidencia: Prefieres modalidad Presencial y la materia es Presencial." .
        }
        WHERE {
            ?estudiante ex:prefiereModalidad ex:MOD_Presencial .
            ?materia ex:tieneModalidad ex:MOD_Presencial .
            ?materia rdfs:label ?nombreMateria .
            
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("Priorizar materia presencial: ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R6: Trabaja y vive lejos
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada ?textoRec .
            ?estudiante ex:motivoGenerado "Estrategia de optimización: Trabajas y vives lejos, conviene virtual." .
        }
        WHERE {
            ?estudiante ex:trabaja true .
            ?estudiante ex:distanciaFacultad "lejos" .
            ?materia ex:tieneModalidad ex:MOD_Virtual .
            ?materia rdfs:label ?nombreMateria .
            
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("Recomendada por logística (Virtual): ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R7: Sobrecarga
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada "Limitar inscripción: Máx 2 materias." .
            ?estudiante ex:motivoGenerado "Riesgo detectado: Tiendes a sobrecargar materias y tienes menos de 20hs disponibles." .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_SobrecargaMaterias .
            ?estudiante ex:horasDisponiblesSemana ?horas .
            FILTER(?horas < 20)
        }
        """,

        # R9: Materias pendientes de años anteriores (Avanzado)
        """
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada ?textoRec .
            ?estudiante ex:motivoGenerado ?textoMotivo .
        }
        WHERE {
            ?estudiante ex:nivelAvance "avanzado" .
            ?materia ex:anio ?anio .
            ?materia rdfs:label ?nombreMateria .
            
            FILTER(?anio <= 3)
            
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("URGENTE - Materia pendiente de año ", STR(?anio), ": ", STR(?nombreMateria)) AS ?textoRec)
            BIND(CONCAT("Eres avanzado pero debes esta materia de año ", STR(?anio), ". Bloquea titulación.") AS ?textoMotivo)
        }
        """
    ]

    count_inferencias = 0

    for i, regla in enumerate(reglas, 1):
        # Ejecutamos la regla CONSTRUCT
        resultado = g.query(regla)
        
        # Creamos un grafo temporal con los resultados de ESTA regla
        temp_graph = Graph()
        for triple in resultado:
            temp_graph.add(triple)
        
        # Extraemos la información del grafo temporal
        # Buscamos pares (Recomendación, Motivo) para el estudiante actual
        query_temp = f"""
        PREFIX ex: <http://miEX.sidad7.edu/ontologias#>
        SELECT DISTINCT ?rec ?motivo
        WHERE {{
            ex:{id_estudiante} ex:recomendacionGenerada ?rec .
            OPTIONAL {{ ex:{id_estudiante} ex:motivoGenerado ?motivo }}
        }}
        """
        hits = list(temp_graph.query(query_temp))
        
        if hits:
            for rec_text, motivo_text in hits:
                count_inferencias += 1
                print(f"[R{i}] SUGERENCIA: {rec_text}")
                if motivo_text:
                    print(f"     POR QUÉ:    {motivo_text}")
                else:
                    print(f"     POR QUÉ:    Regla de inferencia {i} activada.")
                print("-" * 40)

    if count_inferencias == 0:
        print("No se generaron inferencias adicionales para este perfil.")
    else:
        print(f"Total de inferencias lógicas: {count_inferencias}")

# ================================================================
# 10) EJEMPLOS DE USO
# ================================================================

print("\n" + "="*70)
print("CREANDO PERFILES DE ESTUDIANTES")
print("="*70)
# Estudiante 1: Ingresante sin materias aprobadas
crear_estudiante(
"EST001",
"ingresante",
trabaja=True,
holgura=False,
distancia="lejos",
horas_sem=15,
errores=["ERR_Procrastinacion", "ERR_EstudioUltimoDia"],
estrategias=["EST_MicroEstudios"],
modalidad_pref="MOD_Virtual",
tiempo_est="TIEMPO_Bajo",
materias_aprobadas=[]
)
# Estudiante 2: Intermedio con algunas materias
crear_estudiante(
"EST002",
"intermedio",
trabaja=False,
holgura=True,
distancia="cerca",
horas_sem=30,
errores=["ERR_NoCronogramas"],
estrategias=["EST_RutinaSemanal", "EST_EstudioAnticipado"],
modalidad_pref="MOD_Presencial",
tiempo_est="TIEMPO_Alto",
materias_aprobadas=["MAT_1", "MAT_2", "MAT_3", "MAT_4", "MAT_5", "MAT_8"]
)
# Estudiante 3: Avanzado con muchas materias
crear_estudiante(
"EST003",
"avanzado",
trabaja=True,
holgura=False,
distancia="lejos",
horas_sem=12,
errores=["ERR_SobrecargaMaterias"],
estrategias=["EST_GrabarClases"],
modalidad_pref="MOD_Virtual",
tiempo_est="TIEMPO_Bajo",
materias_aprobadas=["MAT_1", "MAT_2", "MAT_3", "MAT_4", "MAT_5", "MAT_6",
"MAT_7", "MAT_8", "MAT_9", "MAT_10", "MAT_11", "MAT_12"]
)
# MOSTRAR RESULTADOS
print("\n" + "="*70)
print("ANÁLISIS ESTUDIANTE 1 (INGRESANTE)")
print("="*70)
mostrar_recomendaciones("EST001")
aplicar_reglas_recomendacion("EST001")  # NUEVO
# mostrar_materias_restantes("EST001")
mostrar_materias_disponibles_para_cursar("EST001")
print("\n" + "="*70)
print("ANÁLISIS ESTUDIANTE 2 (INTERMEDIO)")
print("="*70)
mostrar_recomendaciones("EST002")
aplicar_reglas_recomendacion("EST002")  # NUEVO
# mostrar_materias_restantes("EST002")
mostrar_materias_disponibles_para_cursar("EST002")
print("\n" + "="*70)
print("ANÁLISIS ESTUDIANTE 3 (AVANZADO)")
print("="*70)
mostrar_recomendaciones("EST003")
aplicar_reglas_recomendacion("EST003")  # NUEVO
# mostrar_materias_restantes("EST003")
mostrar_materias_disponibles_para_cursar("EST003")
print("\n[OK] Sistema de recomendación académica completado")
print(f"Total de tripletas en el grafo: {len(g)}")
