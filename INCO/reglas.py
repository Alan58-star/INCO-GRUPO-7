import rdflib
from rdflib import Graph, Literal
from rdflib.namespace import Namespace, RDF, RDFS, OWL, XSD
from rdflib import Namespace
g=Graph()
EX = Namespace("http://miuniversidad7.edu/ontologias#")
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("owl", OWL)

# ----------------------------------------------------------------
# 1) Definir clases
# ----------------------------------------------------------------
for c in [
    "Estudiante",
    "TiempoEstudio",
    "CargaHoraria",
    "Materia",
    "MateriaBase",
    "EstrategiaEstudio",
    "ErrorFrecuente",
    "Modalidad",
    "Examen",
    "Recomendacion",
    "EstrategiaMejora",
]:
    g.add((EX[c], RDF.type, OWL.Class))

# Subclase MateriaBase ⊆ Materia
g.add((EX.MateriaBase, RDFS.subClassOf, EX.Materia))

# ----------------------------------------------------------------
# 2) Definir propiedades (ObjectProperties)
# ----------------------------------------------------------------
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

    # --- Recomendación ---
    "incluyeMateria": ("Recomendacion", "Materia"),
    "incluyeEstrategiaEstudio": ("Recomendacion", "EstrategiaEstudio"),
    "incluyeEstrategiaMejora": ("Recomendacion", "EstrategiaMejora"),
    "incluyeExamen": ("Recomendacion", "Examen"),
    "dependeDeTiempoEstudio": ("Recomendacion", "TiempoEstudio"),
    "dependeDeModalidad": ("Recomendacion", "Modalidad"),
    "dependeDeCorrelativa": ("Recomendacion", "MateriaBase"),

    # --- Materias ---
    "tieneCorrelativa": ("Materia", "Materia"),
    "esBaseDe": ("MateriaBase", "Materia"),

    # --- Estrategias y errores ---
    "evitaError": ("EstrategiaMejora", "ErrorFrecuente"),
    "produceError": ("EstrategiaEstudio", "ErrorFrecuente"),
    "mejoraCon": ("Materia", "EstrategiaMejora"),
    "requiereHabito": ("Materia", "EstrategiaEstudio"),

    # --- Exámenes ---
    "preparaCon": ("Examen", "EstrategiaEstudio"),
}

# Crear cada propiedad
for p, (dom, ran) in props.items():
    g.add((EX[p], RDF.type, OWL.ObjectProperty))
    g.add((EX[p], RDFS.domain, EX[dom]))
    g.add((EX[p], RDFS.range, EX[ran]))

# Inversa solamente si va a existir
g.add((EX.esCorrelativaDe, RDF.type, OWL.ObjectProperty))
g.add((EX.tieneCorrelativa, OWL.inverseOf, EX.esCorrelativaDe))
print(g.triples)