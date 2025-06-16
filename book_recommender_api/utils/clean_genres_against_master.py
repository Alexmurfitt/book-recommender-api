# ✅ utils/clean_genres_against_master.py

import json
from collections import Counter

# 1. Ruta de entrada y salida
INPUT_FILE = "../data/books_openlibrary_enriched.json"
OUTPUT_FILE = "../books_openlibrary_cleaned.json"
REPORT_FILE = "../genres_invalid_report.json"

# 2. Clasificación oficial de géneros válidos (nivel práctico y real)
VALID_GENRES = {
    "literaria", "contemporánea", "experimental", "minimalista", "realismo mágico",
    "ficción psicológica", "ficción filosófica", "histórica", "época antigua", "edad media",
    "renacimiento", "siglo xix", "guerras mundiales", "romántica", "paranormal",
    "romántica erótica", "chick lit", "lgtb romántica", "misterio", "suspense", "thriller",
    "policíaco", "detectives", "thriller psicológico", "thriller legal", "thriller judicial",
    "thriller médico", "thriller político", "thriller conspiración", "noir", "novela negra",
    "terror", "horror", "gótico", "sobrenatural", "psicológico", "criaturas",
    "ciencia ficción", "distopía", "utopía", "cyberpunk", "steampunk", "space opera",
    "viajes en el tiempo", "postapocalíptica", "fantasía", "épica", "medieval", "urbana",
    "oscura", "juvenil", "mitológica", "sword & sorcery", "aventura", "supervivencia",
    "viajes", "exploración", "piratas", "oeste", "western", "queer ficción", "drama contemporáneo",
    "romance queer", "coming-of-age", "romance juvenil", "fantasía juvenil", "distopía juvenil",
    "realismo juvenil", "thriller juvenil", "álbum ilustrado", "cuento clásico", "aventura infantil",
    "fábulas", "moraleja", "humor", "sátira", "parodia", "sátira política", "sátira social",
    "comedia romántica", "relatos", "cuentos", "microficción", "biografía", "autobiografía",
    "memorias", "ensayo", "filosofía", "psicología", "sociología", "crítica literaria", "arte",
    "estética", "religión", "espiritualidad", "ciencia", "tecnología", "historia", "autoayuda",
    "desarrollo personal", "inteligencia emocional", "motivación", "productividad", "mindfulness",
    "educación", "pedagogía", "política", "economía", "sociedad", "geopolítica", "feminismo",
    "antropología", "ecología", "divulgación científica", "astronomía", "biología", "salud",
    "inteligencia artificial", "true crime", "crónica periodística", "gastronomía", "cocina",
    "manualidades", "diy", "jardinería", "hogar", "finanzas personales", "inversión", "nutrición",
    "fitness", "poesía clásica", "poesía moderna", "poesía contemporánea", "poesía amorosa",
    "poesía existencial", "slam poetry", "poesía visual", "poesía experimental", "teatro clásico",
    "teatro contemporáneo", "tragedia", "comedia", "teatro del absurdo", "superhéroes",
    "slice of life", "manga shōnen", "manga shōjo", "manga seinen", "humor gráfico",
    "cómic histórico", "cómic político", "literatura feminista", "literatura queer",
    "literatura indígena", "afrofuturista", "ficción real", "autoficción", "narrativa epistolar",
    "literatura de viajes", "literatura existencialista", "literatura testimonial"
}

# Convertir todo a minúsculas sin espacios alrededor
VALID_GENRES = {g.lower().strip() for g in VALID_GENRES}

# 3. Cargar archivo original
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    books = json.load(f)

invalid_genres_counter = Counter()
cleaned_books = []

# 4. Validar y limpiar
for book in books:
    genres = book.get("genres", [])
    valid = []
    for g in genres:
        g_clean = g.strip().lower()
        if g_clean in VALID_GENRES:
            valid.append(g)
        else:
            invalid_genres_counter[g_clean] += 1
    book["genres"] = valid
    cleaned_books.append(book)

# 5. Guardar archivo corregido
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_books, f, ensure_ascii=False, indent=2)

# 6. Guardar reporte de géneros inválidos
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(invalid_genres_counter.most_common(), f, indent=2, ensure_ascii=False)

print("✅ Limpieza completada con éxito.")
print(f"📁 Archivo corregido guardado en: {OUTPUT_FILE}")
print(f"📄 Reporte de géneros inválidos en: {REPORT_FILE}")
