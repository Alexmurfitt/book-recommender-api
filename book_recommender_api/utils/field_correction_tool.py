# field_correction_tool.py
import json
import difflib
from pathlib import Path
import streamlit as st

# ---------------------------
# 📥 Cargar datos normalizados
# ---------------------------

cleaned_path = Path(__file__).resolve().parent / "field_options_cleaned.json"
with open(cleaned_path, "r", encoding="utf-8") as f:
    fields = json.load(f)

# ---------------------------
# ⚙️ Interfaz Streamlit
# ---------------------------

st.set_page_config(page_title="🔧 Corrección de Campos", layout="wide")
st.title("🔍 Herramienta de Revisión y Corrección de Campos")
st.markdown("Corrige valores similares, duplicados o incoherentes en los campos del dataset.")

selected_field = st.selectbox("Selecciona el campo a revisar:", list(fields.keys()))
values = sorted(fields[selected_field])

similarities = {}
for i, val in enumerate(values):
    matches = difflib.get_close_matches(val, values, n=5, cutoff=0.85)
    if len(matches) > 1:
        key = tuple(sorted(matches))
        similarities[key] = matches

if similarities:
    st.subheader(f"🔁 Posibles valores duplicados o similares en `{selected_field}`")
    corrected = {}
    for idx, group in enumerate(similarities):
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown("**Valores similares detectados:**")
            for v in group:
                st.write(f"- {v}")
        with col2:
            key = f"replace_group_{idx}"
            new_val = st.text_input("Reemplazar por:", group[0], key=key)
            for v in group:
                corrected[v] = new_val

    if st.button("💾 Guardar correcciones"):
        # Aplicar correcciones
        updated_values = sorted(set(corrected.get(v, v) for v in values))
        fields[selected_field] = updated_values

        # Guardar archivo corregido
        corrected_path = Path(__file__).resolve().parent / "field_options_corrected.json"
        with open(corrected_path, "w", encoding="utf-8") as f:
            json.dump(fields, f, ensure_ascii=False, indent=2)

        st.success(f"Correcciones guardadas en {corrected_path.name}")
else:
    st.info("✅ No se detectaron valores suficientemente similares en este campo.")
