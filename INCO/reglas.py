import rdflib
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, RDFS, OWL, XSD
from rdflib import Namespace
from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
g=Graph()
EX = Namespace("http://miuniversidad7.edu/ontologias#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("owl", OWL)


def graficador():
    G_nx = nx.DiGraph()

    # 1) Agregar solo las clases como nodos
    clases = set(g.subjects(RDF.type, OWL.Class))
    for c in clases:
        G_nx.add_node(str(c).replace(EX, ""))

    # 2) Agregar aristas solo si conectan CLASES mediante PROPIEDADES
    for s, p, o in g:
        if s in clases and o in clases:
            G_nx.add_edge(
                str(s).replace(EX, ""),
                str(o).replace(EX, ""),
                label=str(p).replace(EX, "")
            )

    # 3) Dibujar grafo
    plt.figure(figsize=(22, 22))
    pos = nx.spring_layout(G_nx, k=0.5, iterations=50)

    nx.draw(
        G_nx,
        pos,
        with_labels=True,
        node_size=2500,
        font_size=10,
        font_weight="bold"
    )

    # Mostrar etiquetas de las propiedades (nombres de aristas)
    labels = nx.get_edge_attributes(G_nx, 'label')
    nx.draw_networkx_edge_labels(G_nx, pos, edge_labels=labels, font_size=8)

    plt.title("Clases + Propiedades del Grafo RDF")
    plt.show()

# ----------------------------------------------------------------
# 1) Definir clases
# ----------------------------------------------------------------
materias_base = {
    "2": "Álgebra Lineal",
    "4": "Análisis Matemático I",
}
materias = {
    # MATERIAS
    # PRIMER AÑO
    "1": "Introduccion a la Programacion",
    "3": "Organizacion de Computadoras",
    "5": "Metodologia de la Programacion",
    "6": "Analisis Matematico II",
    "7": "Fisica Mecanica",
    "8": "Estructura de Datos",
    # SEGUNDO AÑO
    "9": "Matematica Discreta",
    "10": "Teoria de la Informacion y la Comunicacion",
    "11": "Desarrollo Sistematico de Programas",
    "12": "Probabilidades y Estadistica",
    "13": "Electricidad y Magnetismo",
    "14": "Bases de Datos",
    "15": "Programacion Concurrente",
    "16": "Calculo Numerico",
    # TERCER AÑO
    "17": "Logica Computacional",
    "18": "Sistemas Operativos I",
    "19": "Organizacion Empresarial y Modelo de Negocios",
    "20": "Modelado Orientado a Objetos",
    "21": "Cursos Optativos I",
    "22": "Teoria de Automatas, Lenguajes y Computacion",
    "23": "Sistemas Operativos II",
    "24": "Metodos de Simulacion",
    # CUARTO AÑO
    "25": "Formulacion, Evaluacion de Proyectos Informaticos y Emprendedorismo Digital",
    "26": "Calidad del Software y Testing",
    "27": "Arquitectura de Redes",
    "28": "Ingenieria del Conocimiento",
    "29": "Arquitectura de Computadoras Paralelas",
    "30": "Sistemas de Informacion",
    "31": "Cursos Optativos II",
    "32": "Seguridad y Auditoria Informatica",
    # QUINTO AÑO
    "33": "Ingenieria de Software I",
    "34": "Sistemas Inteligentes",
    "35": "Legislacion, Etica y Ejercicio Profesional",
    "36": "Ingenieria de Software II",
    
    # PRACTICA PROFESIONAL
    "PPS": "Practica Profesional Supervisada",
    # FINAL
    "TF": "Trabajo Final"
}
optativas={
    # OPTATIVAS
    "37": "Compiladores",
    "38": "Aplicaciones de Bases de Datos I",
    "39": "Aplicaciones de Bases de Datos II",
    "40": "Introduccion al Procesamiento Digital de Imagenes",
    "41": "Inteligencia Artificial",
    "42": "Recuperacion Avanzada de la Informacion",
    "43": "Desarrollo y Arquitecturas Avanzadas de Software",
    "44": "Modelado y Proceso de Negocios",
    "45": "Taller de Formacion Profesional",
    "46": "Taller de Metodologia de la Investigacion Cientifica",
    "47": "Gestion Ambiental",
}
requisitos={
    "R1": "Nivel de Suficiencia de Ingles",
    "R2": "Nivel de Aptitud de Ingles",
    "R3": "Todas las materias regulares hasta Cuarto"
}
recomendacionesIng={
    # INGRESANTES
    "I1": "Planificar dias enfocados en las materias",
    "I2": "Aprovechar cercanía a la facultad para estudiar en biblioteca",
    "I3": "Estudiar durante el viaje (lecturas, resúmenes, videos)",
    "I4": "Aprovechar tiempos entre materias para estudiar en biblioteca",
    "I5": "Conversar en el trabajo la posibilidad de flexibilizar días clave",
    "I6": "Usar los huecos del trabajo para estudiar en biblioteca",
    "I7": "Mantener un equilibrio saludable para evitar burnout",
    "I8": "Mantener una rutina semanal estricta para estudiar en horarios fijos",
}
recomendacionesInt={
    # INTERMEDIO
    "M1": "Estudiar con anticipacion y revisar cronogramas de examenes y actividades",
    "M2": "Aprovechar la cercanía para asistir a tutorías y prácticas",
    "M3": "Reorganizar los viajes para cursar varios días seguidos (ej: lunes y martes)",
    "M4": "Elegir 3–4 materias por cuatrimestre si la distancia lo permite",
    "M5": "Organizarse con micro-estudios de 25–30 min diarios",
    "M6": "Usar los huecos del trabajo para avanzar en teoría y lecturas",
    "M7": "Inscribirse solo en materias esenciales o correlativas de avance.",
    "M8": "Priorizar materias virtuales y grabar clases",   
}
recomendacionesAvan={
    # AVANZADOS
    "A1": "Identificar de dónde viene la falta de tiempo y corregir desviaciones",
    "A2": "Enfocar materias de años anteriores para cumplir requisitos de PPS y TF",
    "A3": "Buscar material de años anteriores",
    "A4": "Enfocar materias de años anteriores para cumplir requisitos de PPS y TF",
    "A5": "Revisar parciales de años anteriores",
    "A6": "Preparar y organizar mesas de examenes de materias pendientes",
    "A7": "Negociar con el trabajo días de estudio previos a parciales",
    "A8": "Organizar viajes solo para las clases obligatorias",
}
#CLASES
for c in [
    "Estudiante",
    "TiempoEstudio",
    "CargaHoraria",
    "Materia",
    "Requisito",
    "Optativa",
    "Recomendacion",
    "EstrategiaEstudio",
    "ErrorFrecuente",
    "Modalidad",
    "Examen",
    "EstrategiaMejora",
]:
    g.add((EX[c], RDF.type, OWL.Class))
# Subclases
g.add((EX.MateriaBase, RDFS.subClassOf, EX.Materia))
g.add((EX.RecomendacionIngresante, RDFS.subClassOf, EX.Recomendacion))
g.add((EX.RecomendacionIntermedio, RDFS.subClassOf, EX.Recomendacion))
g.add((EX.RecomendacionAvanzado, RDFS.subClassOf, EX.Recomendacion))
props = {
    # --- Estudiante ---
    "tieneTiempoEstudio": ("Estudiante", "TiempoEstudio"),
    "cursaMateria": ("Estudiante", "Materia"),
    "priorizaMateriaBase": ("Estudiante", "MateriaBase"),
    "usaEstrategiaEstudio": ("Estudiante", "EstrategiaEstudio"),
    "usaEstrategiaMejora": ("Estudiante", "EstrategiaMejora"),
    "cometeErrorFrecuente": ("Estudiante", "ErrorFrecuente"),
    "prefiereModalidad": ("Estudiante", "Modalidad"),
    "rindeExamen": ("Estudiante", "Examen"),
     # --- Materias ---
    "esCorrelativaDe": ("Materia", "Materia"),
    
    # --- Recomendación ---
    "incluyeMateria": ("Recomendacion", "Materia"),
    "incluyeEstrategiaEstudio": ("Recomendacion", "EstrategiaEstudio"),
    "incluyeEstrategiaMejora": ("Recomendacion", "EstrategiaMejora"),
    "incluyeExamen": ("Recomendacion", "Examen"),
    "dependeDeTiempoEstudio": ("Recomendacion", "TiempoEstudio"),
    "dependeDeModalidad": ("Recomendacion", "Modalidad"),
    "dependeDeCorrelativa": ("Recomendacion", "MateriaBase"),

     # --- Estrategias y errores ---
    "evitaError": ("EstrategiaMejora", "ErrorFrecuente"),
    "produceError": ("EstrategiaEstudio", "ErrorFrecuente"),
    "mejoraCon": ("Materia", "EstrategiaMejora"),
    "requiereHabito": ("Materia", "EstrategiaEstudio"),

    # --- Exámenes ---
    "preparaCon": ("Examen", "EstrategiaEstudio"),
}
for p, (dom, ran) in props.items():
    g.add((EX[p], RDF.type, OWL.ObjectProperty))
    g.add((EX[p], RDFS.domain, EX[dom]))
    g.add((EX[p], RDFS.range, EX[ran]))
#Carga instancias de materias
for id, nombre in materias.items():
    g.add((EX[id], RDF.type, EX.Materia))
    g.add((EX[id], RDFS.label, Literal(nombre)))
for id, nombre in requisitos.items():
    g.add((EX[id], RDF.type, EX.Requisito))
    g.add((EX[id], RDFS.label, Literal(nombre)))  
for id, nombre in optativas.items():
    g.add((EX[id], RDF.type, EX.Optativa))
    g.add((EX[id], RDFS.label, Literal(nombre))) 
for id, nombre in materias_base.items():
    g.add((EX[id], RDF.type, EX.MateriaBase))
    g.add((EX[id], RDFS.label, Literal(nombre))) 
for id,nombre in recomendacionesIng.items():
  g.add((EX[id], RDF.type, EX.RecomendacionIngresante))
  g.add((EX[id], RDFS.label, Literal(nombre)))
for id,nombre in recomendacionesInt.items():
  g.add((EX[id], RDF.type, EX.RecomendacionIntermedio))
  g.add((EX[id], RDFS.label, Literal(nombre)))
for id,nombre in recomendacionesAvan.items():
  g.add((EX[id], RDF.type, EX.RecomendacionAvanzado))
  g.add((EX[id], RDFS.label, Literal(nombre)))
g.add((EX["TF"], EX.cargaHoraria, Literal(200, datatype=XSD.positiveInteger)))
g.add((EX["PPS"], EX.cargaHoraria, Literal(200, datatype=XSD.positiveInteger)))
g.add((EX["31"], EX.cargaHoraria, Literal(180, datatype=XSD.positiveInteger)))
for c in ["1","2","3","4","5","6","7","8","9","11","12","13","14","15","16","18","19","20","21","22","23","25","26","27","28","30","31","32","34","35","37","38","39","40","41","42","43","44"]:
  g.add((EX[c], EX.cargaHoraria, Literal(90, datatype=XSD.positiveInteger)))
for c in ["32","35"]:
  g.add((EX[c], EX.cargaHoraria, Literal(75, datatype=XSD.positiveInteger)))
for c in ["10","17","24","29","33","36"]:
  g.add((EX[c], EX.cargaHoraria, Literal(60, datatype=XSD.positiveInteger)))
# CORRELATIVAS
for m in ["1", "2", "3", "4"]:
    g.add((EX["0"], EX.esCorrelativaDe, EX[m]))
for m in ["5", "8"]:
    g.add((EX["1"], EX.esCorrelativaDe, EX[m]))
"""
for m in ["7", "12", "17"]:
    g.add((EX["2"], EX.esCorrelativaDe, EX[m]))
for m in ["10", "18"]:
    g.add((EX["3"], EX.esCorrelativaDe, EX[m]))
for m in ["6", "7"]:
    g.add((EX["4"], EX.esCorrelativaDe, EX[m]))
for m in ["11", "14", "15", "18", "19"]:
    g.add((EX["5"], EX.esCorrelativaDe, EX[m]))
for m in ["12", "16"]:
    g.add((EX["6"], EX.esCorrelativaDe, EX[m]))
for m in ["13"]:
    g.add((EX["7"], EX.esCorrelativaDe, EX[m]))
for m in ["11", "14", "15", "18", "19", "22"]:
    g.add((EX["8"], EX.esCorrelativaDe, EX[m]))
for m in ["34"]:
    g.add((EX["9"], EX.esCorrelativaDe, EX[m]))
for m in ["24", "34", "45", "46", "47"]:
    g.add((EX["12"], EX.esCorrelativaDe, EX[m]))
for m in ["38", "39"]:
    g.add((EX["14"], EX.esCorrelativaDe, EX[m]))
for m in ["20", "37", "40"]:
    g.add((EX["15"], EX.esCorrelativaDe, EX[m]))
for m in ["24", "34"]:
    g.add((EX["16"], EX.esCorrelativaDe, EX[m]))
for m in ["22", "28"]:
    g.add((EX["17"], EX.esCorrelativaDe, EX[m]))
for m in ["23"]:
    g.add((EX["18"], EX.esCorrelativaDe, EX[m]))
for m in ["25", "44"]:
    g.add((EX["19"], EX.esCorrelativaDe, EX[m]))
for m in ["26", "28", "30", "42", "43"]:
    g.add((EX["20"], EX.esCorrelativaDe, EX[m]))
for m in ["28","29","30","32"]:
    g.add((EX["21"], EX.esCorrelativaDe, EX[m]))
for m in ["41"]:
    g.add((EX["22"], EX.esCorrelativaDe, EX[m]))
for m in ["27", "29", "32", ]:
    g.add((EX["23"], EX.esCorrelativaDe, EX[m]))
for m in ["27", "29", "32", ]:
    g.add((EX["23"], EX.esCorrelativaDe, EX[m]))
for m in ["29"]:
    g.add((EX["27"], EX.esCorrelativaDe, EX[m]))
for m in ["33"]:
    g.add((EX["30"], EX.esCorrelativaDe, EX[m]))
for m in ["33", "34", "35"]:
    g.add((EX["31"], EX.esCorrelativaDe, EX[m]))
for m in ["36"]:
    g.add((EX["33"], EX.esCorrelativaDe, EX[m]))
for opt in ["37","38","39","40","41","42","43","44","45","46","47"]:
    g.add((EX[opt], EX.esCorrelativaDe, EX["21"]))
    g.add((EX[opt], EX.esCorrelativaDe, EX["31"]))
for opt in ["28","29","30","32"]:
    g.add((EX["R1"], EX.esCorrelativaDe, EX[opt]))
for opt in ["33","34","35"]:
    g.add((EX["R2"], EX.esCorrelativaDe, EX[opt]))
for c in range(1, 33):
    g.add((EX[str(c)], EX.esCorrelativaDe, EX["R3"]))
g.add((EX["R3"], EX.esCorrelativaDe, EX["PPS"]))
g.add((EX["R3"], EX.esCorrelativaDe, EX["TF"]))
# SINERGIA
g.add((EX["9"], EX.tieneSinergia, EX["17"]))
g.add((EX["11"], EX.tieneSinergia, EX["15"]))
g.add((EX["12"], EX.tieneSinergia, EX["16"]))
g.add((EX["20"], EX.tieneSinergia, EX["22"]))
g.add((EX["25"], EX.tieneSinergia, EX["32"]))
g.add((EX["28"], EX.tieneSinergia, EX["30"]))
g.add((EX["28"], EX.tieneSinergia, EX["34"]))
g.add((EX["32"], EX.tieneSinergia, EX["35"]))

#                                --- --- --- 5. Razonamiento OWL --- --- ---
# AXIOMA DE LA PROPIEDAD SIMETRICA
g.add((EX.tieneSinergia, RDF.type, owl.SymmetricProperty))
# AXIOMA DE LA PROPIEDAD TRANSITIVA
g.add((EX.esCorrelativaDe, RDF.type, owl.TransitiveProperty))
g.add((EX.cursa, RDF.type, owl.TransitiveProperty))
# AXIOMA DE LA PROPIEDAD INVERSA
g.add((EX.esCorrelativaDe, owl.inverseOf, EX.tieneCorrelativa))
# RAZONADOR
DeductiveClosure(OWLRL_Semantics).expand(g)
"""
graficador()

