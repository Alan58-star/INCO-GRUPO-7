import rdflib
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, RDFS, OWL, XSD
from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
import matplotlib.pyplot as plt
g = Graph()
EX = Namespace("http://miuniversidad7.edu/ontologias#")
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
    "MAT_37_PPS": ("Práctica Profesional Supervisada", 200, "MOD_Presencial", 5),
    "MAT_38_TF": ("Trabajo Final", 200, "MOD_Presencial", 5),

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

# Optativas
g.add((EX.MAT_15, EX.esCorrelativaDe, EX.OPT_37))
g.add((EX.MAT_14, EX.esCorrelativaDe, EX.OPT_38))
g.add((EX.MAT_14, EX.esCorrelativaDe, EX.OPT_39))
g.add((EX.MAT_15, EX.esCorrelativaDe, EX.OPT_40))
g.add((EX.MAT_22, EX.esCorrelativaDe, EX.OPT_41))
g.add((EX.MAT_20, EX.esCorrelativaDe, EX.OPT_42))
g.add((EX.MAT_20, EX.esCorrelativaDe, EX.OPT_43))
g.add((EX.MAT_19, EX.esCorrelativaDe, EX.OPT_44))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_45))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_46))
g.add((EX.MAT_12, EX.esCorrelativaDe, EX.OPT_47))

g.add((EX.MAT_27, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_28, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_29, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_30, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria
g.add((EX.MAT_32, EX.esCorrelativaDe, EX.R3))  # Calculo Numerico → Seguridad y Auditoria


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
    """Obtiene recomendaciones personalizadas"""
    perfil_query = f"""
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
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

    if str(nivel) == "ingresante":
        tipo_rec = "ex:RecomendacionIngresante"
    elif str(nivel) == "intermedio":
        tipo_rec = "ex:RecomendacionIntermedio"
    else:
        tipo_rec = "ex:RecomendacionAvanzado"

    query = f"""
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?recomendacion ?texto ?prioridad
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

    resultados = list(g.query(query))
    return resultados

def obtener_materias_restantes(id_estudiante):
    """Obtiene las materias que AÚN NO HA APROBADO el estudiante"""
    query_aprobadas = f"""
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
    SELECT ?materia
    WHERE {{
        ex:{id_estudiante} ex:materiaAprobada ?materia .
    }}
    """

    aprobadas_result = list(g.query(query_aprobadas))
    aprobadas = [str(row[0]).split("#")[-1] for row in aprobadas_result]

    query_todas = """
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
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
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
    SELECT ?materia
    WHERE {{
        ex:{id_estudiante} ex:materiaAprobada ?materia .
    }}
    """

    aprobadas_result = list(g.query(query_aprobadas))
    aprobadas = [str(row[0]).split("#")[-1] for row in aprobadas_result]

    if not aprobadas:
        query_sin_correlativas = """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
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
    PREFIX ex: <http://miuniversidad7.edu/ontologias#>
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
    """Muestra las recomendaciones personalizadas"""
    print(f"\n{'='*70}")
    print(f"RECOMENDACIONES PARA ESTUDIANTE: {id_estudiante}")
    print(f"{'='*70}\n")
    recomendaciones = obtener_recomendaciones(id_estudiante)
    if not recomendaciones:
        print("No se encontraron recomendaciones para este perfil.")
    else:
        for i, (rec, texto, prioridad) in enumerate(recomendaciones, 1):
            rec_id = str(rec).split("#")[-1]
            print(f"{i}. [{rec_id}] (Prioridad {prioridad})")
            print(f"   {texto}\n")
        
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
    Aplica reglas CONSTRUCT para generar recomendaciones específicas
    basadas en el perfil del estudiante
    """
    print(f"\n{'='*70}")
    print(f"REGLAS DE INFERENCIA APLICADAS: {id_estudiante}")
    print(f"{'='*70}\n")
    reglas = [
        # R1: Si comete error de procrastinación, recomendar estrategia de micro-estudios
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_MicroEstudios .
            ?estudiante ex:recomendacionGenerada "Usar micro-estudios para evitar procrastinación" .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_Procrastinacion .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_MicroEstudios }
        }
        """,
        
        # R2: Si comete error de no revisar cronogramas, recomendar estudio anticipado
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_EstudioAnticipado .
            ?estudiante ex:recomendacionGenerada "Implementar estudio anticipado y revisar cronogramas semanalmente" .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_NoCronogramas .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_EstudioAnticipado }
        }
        """,
        
        # R3: Si estudia último día, recomendar rutina semanal
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:deberiaUsar ex:EST_RutinaSemanal .
            ?estudiante ex:recomendacionGenerada "Establecer rutina semanal de estudio constante" .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_EstudioUltimoDia .
            FILTER NOT EXISTS { ?estudiante ex:usaEstrategiaEstudio ex:EST_RutinaSemanal }
        }
        """,
        
        # R4: Si prefiere virtual y tiene materias virtuales disponibles
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:materiaPrioritaria ?materia .
            ?estudiante ex:recomendacionGenerada ?textoRec .
        }
        WHERE {
            ?estudiante ex:prefiereModalidad ex:MOD_Virtual .
            ?materia ex:tieneModalidad ex:MOD_Virtual .
            ?materia rdfs:label ?nombreMateria .
            
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("Priorizar materia virtual disponible: ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R5: Si prefiere presencial y tiene materias presenciales disponibles
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:materiaPrioritaria ?materia .
            ?estudiante ex:recomendacionGenerada ?textoRec .
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
            
            BIND(CONCAT("Priorizar materia presencial disponible: ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R6: Si trabaja y vive lejos, priorizar materias virtuales
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:materiaPrioritaria ?materia .
            ?estudiante ex:recomendacionGenerada ?textoRec .
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
            
            BIND(CONCAT("Materia virtual recomendada (trabajas y vives lejos): ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R7: Si comete error de sobrecarga, limitar materias según horas disponibles
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada "Limitar cantidad de materias: máximo 2 materias por cuatrimestre" .
        }
        WHERE {
            ?estudiante ex:cometeErrorFrecuente ex:ERR_SobrecargaMaterias .
            ?estudiante ex:horasDisponiblesSemana ?horas .
            FILTER(?horas < 20)
        }
        """,
        
        # R8: Si tiene tiempo bajo y trabaja, recomendar materias de menor carga
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:materiaPrioritaria ?materia .
            ?estudiante ex:recomendacionGenerada ?textoRec .
        }
        WHERE {
            ?estudiante ex:tieneTiempoEstudio ex:TIEMPO_Bajo .
            ?estudiante ex:trabaja true .
            ?materia ex:cargaHoraria ?carga .
            ?materia rdfs:label ?nombreMateria .
            
            FILTER(?carga <= 60)
            
            FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?materia }
            
            FILTER NOT EXISTS {
                ?correlativa ex:esCorrelativaDe ?materia .
                FILTER NOT EXISTS { ?estudiante ex:materiaAprobada ?correlativa }
            }
            
            BIND(CONCAT("Materia de baja carga horaria recomendada (", STR(?carga), "hs): ", STR(?nombreMateria)) AS ?textoRec)
        }
        """,
        
        # R9: Si es avanzado y le faltan materias de años anteriores
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        CONSTRUCT { 
            ?estudiante ex:materiaPrioritaria ?materia .
            ?estudiante ex:recomendacionGenerada ?textoRec .
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
        }
        """,
        
        # R10: Si tiene holgura y no trabaja, recomendar aumentar carga de materias
        """
        PREFIX ex: <http://miuniversidad7.edu/ontologias#>
        CONSTRUCT { 
            ?estudiante ex:recomendacionGenerada "Puedes aumentar tu carga académica: considera 3-4 materias por cuatrimestre" .
        }
        WHERE {
            ?estudiante ex:tieneHolgura true .
            ?estudiante ex:trabaja false .
            ?estudiante ex:tieneTiempoEstudio ex:TIEMPO_Alto .
        }
        """
    ]

    recomendaciones_inferidas = []

    for i, regla in enumerate(reglas, 1):
        resultado = g.query(regla)
        
        temp_graph = Graph()
        for triple in resultado:
            temp_graph.add(triple)
        
        for s, p, o in temp_graph:
            if str(s).endswith(id_estudiante):
                if str(p).endswith("recomendacionGenerada"):
                    recomendaciones_inferidas.append((f"R{i}", str(o)))
                elif str(p).endswith("deberiaUsar"):
                    estrategia = str(o).split("#")[-1]
                    recomendaciones_inferidas.append((f"R{i}", f"Debería usar estrategia: {estrategia}"))

    if recomendaciones_inferidas:
        print("RECOMENDACIONES INFERIDAS POR REGLAS:")
        print("-" * 70)
        for regla_id, texto in recomendaciones_inferidas:
            print(f"[{regla_id}] {texto}")
        print(f"\nTotal de recomendaciones inferidas: {len(recomendaciones_inferidas)}")
    else:
        print("No se generaron recomendaciones adicionales por reglas de inferencia.")

    return recomendaciones_inferidas

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