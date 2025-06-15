import json
import os
import shutil

# 📁 Ruta al archivo de libros
FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "books_openlibrary_enriched.json")
BACKUP_FILE = FILE_PATH.replace(".json", "_backup.json")

# 🔒 Validación: asegurar que nuevos_libros es una lista PLANA de diccionarios
def validar_formato(libros):
    if not isinstance(libros, list):
        raise ValueError("❌ Error: 'nuevos_libros' debe ser una lista.")
    if any(isinstance(item, list) for item in libros):
        raise ValueError("❌ Error: 'nuevos_libros' contiene una lista anidada. Usa una lista plana de diccionarios.")
    if not all(isinstance(item, dict) for item in libros):
        raise ValueError("❌ Error: Todos los elementos de 'nuevos_libros' deben ser diccionarios.")

# 🔹 Libros nuevos a insertar
nuevos_libros = [
  {
    "title": "Storytelling como estrategia de comunicación",
    "author": "Guillaume Lamarre",
    "genres": ["Comunicación", "Empresa"],
    "subgenres": ["Narrativa corporativa", "Marketing"],
    "themes": ["influencia", "mensaje", "persuasión"],
    "emotion_tags": ["claridad", "conexión", "curiosidad"],
    "tone": "profesional",
    "style": "didáctico",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta extraversión", "Alta apertura"],
    "year": 2019,
    "description": "Una guía para emplear técnicas narrativas en la comunicación empresarial y la conexión con la audiencia."
  },
  {
    "title": "Tecnofeudalismo",
    "author": "Yanis Varoufakis",
    "genres": ["Economía", "Tecnología"],
    "subgenres": ["Crítica del capitalismo digital", "Política global"],
    "themes": ["poder digital", "explotación", "sistemas económicos"],
    "emotion_tags": ["alerta", "reflexión", "urgencia"],
    "tone": "crítico",
    "style": "ensayístico",
    "age_range": "18+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta racionalidad"],
    "year": 2023,
    "description": "Una denuncia del dominio de las grandes tecnológicas como una nueva forma de feudalismo global."
  },
  {
    "title": "Una breve historia de la economía",
    "author": "Niall Kishtainy",
    "genres": ["Economía", "Historia"],
    "subgenres": ["Divulgación económica", "Historia económica"],
    "themes": ["mercado", "crisis", "pensamiento económico"],
    "emotion_tags": ["curiosidad", "claridad", "aprendizaje"],
    "tone": "informativo",
    "style": "sintético",
    "age_range": "14+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta conciencia"],
    "year": 2017,
    "description": "Un recorrido accesible por los momentos clave y las grandes ideas que han moldeado la economía moderna."
  },
  {
    "title": "Una breve historia de la igualdad",
    "author": "Thomas Piketty",
    "genres": ["Economía", "Historia"],
    "subgenres": ["Ensayo", "Historia social"],
    "themes": ["igualdad", "redistribución", "progreso"],
    "emotion_tags": ["esperanza", "conciencia", "compromiso"],
    "tone": "optimista",
    "style": "ensayístico",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta responsabilidad"],
    "year": 2021,
    "description": "Un ensayo que resume siglos de lucha por la igualdad y propone caminos para avanzar hacia sociedades más justas."
  },
  {
    "title": "Un paso por delante de Wall Street",
    "author": "Peter Lynch",
    "genres": ["Finanzas", "Inversión"],
    "subgenres": ["Mercado de valores", "Inversión a largo plazo"],
    "themes": ["rentabilidad", "oportunidad", "análisis financiero"],
    "emotion_tags": ["motivación", "confianza", "ambición"],
    "tone": "práctico",
    "style": "experiencial",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta responsabilidad", "Alta racionalidad"],
    "year": 1989,
    "description": "Un clásico de la inversión que enseña cómo cualquier persona puede batir al mercado con conocimiento y disciplina."
  },
  {
    "title": "Walden",
    "author": "Henry David Thoreau",
    "genres": ["Filosofía", "Naturaleza"],
    "subgenres": ["Vida simple", "Individualismo"],
    "themes": ["naturaleza", "soledad", "libertad"],
    "emotion_tags": ["paz", "reflexión", "contemplación"],
    "tone": "sereno",
    "style": "ensayístico-narrativo",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta introspección"],
    "year": 1854,
    "description": "Una meditación filosófica sobre la autosuficiencia y la vida en armonía con la naturaleza."
  },
  {
    "title": "Walden Dos",
    "author": "B. F. Skinner",
    "genres": ["Psicología", "Ficción utópica"],
    "subgenres": ["Conductismo", "Sociedad ideal"],
    "themes": ["comportamiento", "utopía", "organización social"],
    "emotion_tags": ["curiosidad", "desafío", "reflexión"],
    "tone": "experimental",
    "style": "narrativo-ensayístico",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta racionalidad"],
    "year": 1948,
    "description": "Una novela que explora cómo una comunidad basada en principios científicos puede crear una sociedad más feliz."
  },
  {
    "title": "Demian",
    "author": "Hermann Hesse",
    "genres": ["Filosofía", "Ficción"],
    "subgenres": ["Bildungsroman", "Psicología", "Existencialismo"],
    "themes": ["identidad", "dualidad", "búsqueda interior"],
    "emotion_tags": ["reflexión", "melancolía", "inquietud"],
    "tone": "reflexivo",
    "style": "poético",
    "age_range": "16+",
    "language": "es",
    "personality_match": ["Alta apertura", "Alta amabilidad"],
    "year": 1919,
    "description": "Una novela iniciática que explora la transformación del alma a través del conflicto interno."
  }
]


# ✅ Validar estructura de entrada
validar_formato(nuevos_libros)

# 🔹 Cargar archivo actual
with open(FILE_PATH, "r", encoding="utf-8") as f:
    libros_existentes = json.load(f)

# 🔁 Aplanar si hay listas anidadas en el archivo (prevención)
libros_existentes_flat = []
for item in libros_existentes:
    if isinstance(item, list):
        libros_existentes_flat.extend(item)
    elif isinstance(item, dict):
        libros_existentes_flat.append(item)

# 🧠 Crear conjunto de claves únicas existentes
claves_existentes = set(
    (libro.get("title", "").strip().lower(), libro.get("author", "").strip().lower())
    for libro in libros_existentes_flat if isinstance(libro, dict)
)

# 🔎 Filtrar nuevos libros que no estén ya presentes
nuevos_libros_filtrados = []
for libro in nuevos_libros:
    clave = (libro.get("title", "").strip().lower(), libro.get("author", "").strip().lower())
    if clave not in claves_existentes:
        nuevos_libros_filtrados.append(libro)
        claves_existentes.add(clave)  # Evita duplicación múltiple si script se ejecuta varias veces

# 📦 Hacer backup antes de escribir
shutil.copy(FILE_PATH, BACKUP_FILE)
print(f"🛡️  Backup creado: {BACKUP_FILE}")

# ➕ Añadir los libros filtrados
libros_final = libros_existentes_flat + nuevos_libros_filtrados

# 💾 Guardar el archivo actualizado
with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(libros_final, f, ensure_ascii=False, indent=4)

print(f"✅ {len(nuevos_libros_filtrados)} libros nuevos añadidos.")
print(f"📚 Total actual: {len(libros_final)} libros.")
