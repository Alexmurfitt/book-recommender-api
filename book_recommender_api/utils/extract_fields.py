import json

# Ruta al archivo JSON enriquecido
with open("../data/books_openlibrary_enriched.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# Inicializar conjuntos para evitar duplicados
genres = set()
subgenres = set()
themes = set()
emotion_tags = set()
tones = set()
styles = set()
age_ranges = set()
languages = set()  # ✅ Añadido

# Recorrer cada libro y extraer campos
for book in books:
    genres.update(book.get("genres", []))
    subgenres.update(book.get("subgenres", []))
    themes.update(book.get("themes", []))
    emotion_tags.update(book.get("emotion_tags", []))
    
    tone = book.get("tone")
    if tone:
        tones.add(tone)
    
    style = book.get("style")
    if style:
        styles.add(style)
    
    age_range = book.get("age_range")
    if age_range:
        age_ranges.add(age_range)
    
    language = book.get("language")  # ✅ Extraer idioma
    if language:
        languages.add(language)

# Diccionario para exportar
field_data = {
    "genres": sorted(genres),
    "subgenres": sorted(subgenres),
    "themes": sorted(themes),
    "emotion_tags": sorted(emotion_tags),
    "tone": sorted(tones),
    "style": sorted(styles),
    "age_range": sorted(age_ranges),
    "language": sorted(languages)  # ✅ Ya definido correctamente
}

# Guardar en archivo JSON
with open("field_options.json", "w", encoding="utf-8") as f:

    json.dump(field_data, f, ensure_ascii=False, indent=2)

# Imprimir resumen
print("📚 Géneros:")
print(sorted(genres))
print("\n📚 Subgéneros:")
print(sorted(subgenres))
print("\n🎯 Temas:")
print(sorted(themes))
print("\n🎭 Emociones:")
print(sorted(emotion_tags))
print("\n🎨 Tonos:")
print(sorted(tones))
print("\n✍️ Estilos:")
print(sorted(styles))
print("\n👶 Rangos de edad:")
print(sorted(age_ranges))
print("\n🌍 Idiomas:")
print(sorted(languages))
