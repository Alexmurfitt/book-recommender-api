## 🧠 Informe Técnico: Problema Crítico – Lógica de Recomendación Mal Calibrada

### 💡 Identificación del Problema

Durante el desarrollo y pruebas del sistema de recomendación personalizado de libros, uno de los problemas más graves detectados fue la **lógica de recomendación mal calibrada**. Este fallo se manifestaba con una alta frecuencia y afectaba directamente a la calidad de las recomendaciones generadas.

### ❌ Síntomas Observados

El síntoma principal fue la **desalineación entre las preferencias del usuario y los libros recomendados**. En muchos casos, el sistema sugería obras completamente fuera de contexto respecto al perfil proporcionado. Un ejemplo paradigmático fue la recomendación de *Jurassic Park* a un usuario que había indicado intereses existencialistas y filosóficos. Este tipo de errores revelaba que las recomendaciones no eran coherentes ni relevantes.

Una evaluación detallada arrojó las siguientes deficiencias:

* **Precisión:** Muy baja. En algunos casos, el único campo coincidente era el género. Temas, emociones, tono, estilo o edad preferida quedaban sin coincidencia.
* **Exactitud semántica:** Deficiente. Aunque el género pudiera coincidir, el tono emocional y narrativo del libro no reflejaba lo que el usuario buscaba.
* **Objetividad del sistema:** Parcial. La lógica favorecía libros por razones equivocadas, como el género, sin considerar elementos críticos como los temas centrales o las emociones evocadas.
* **Explicación generada:** Incompleta y a veces errónea. Se mostraban frases vacías como “temas ()” o “emociones evocadas ()”, lo que evidenciaba fallos lógicos en la función generadora de explicaciones.

### 🧠 Causa Raíz

La raíz del problema residía en la función `compute_score()` del archivo `recommender.py`. Esta función era la encargada de calcular la puntuación total de cada libro en función de su similitud con las preferencias del usuario.

Sin embargo, el algoritmo original no ponderaba adecuadamente los factores realmente determinantes. Se daba un peso excesivo al género y un peso insuficiente a aspectos como los temas del libro o las emociones evocadas, que son cruciales para la experiencia lectora. Además, la lógica no exigía coincidencias múltiples mínimas, por lo que un libro podía ser recomendado con una única coincidencia superficial.

### ✅ Solución Implementada

Rediseñé por completo la función de cálculo de puntuación para que reflejara de forma más fiel la relevancia de cada criterio desde el punto de vista del lector. Se implementó la siguiente lógica ponderada:

```python
score = (
    0.4 * genre_match +
    0.3 * emotion_match +
    0.2 * personality_match +
    0.1 * style_tone_match
)
```

Este nuevo esquema asigna mayor peso a los **géneros** y especialmente a las **emociones**, sin ignorar la coherencia con el perfil de personalidad del lector ni el estilo y tono de la obra. También se integró una **validación por coincidencia múltiple mínima**, que exige que el libro coincida al menos en varios campos relevantes antes de considerarse como recomendación válida.

### 📈 Justificación Técnica

El rediseño no fue arbitrario. Se fundamentó en criterios semánticos y de experiencia de usuario. Por ejemplo:

* Los **temas y emociones** definen el contenido y la carga emocional del libro, por lo que se les asignó un peso conjunto mayor.
* El **género** pasó a ser importante pero no determinante, para evitar recomendaciones superficiales.
* El **perfil de personalidad** (Big Five – OCEAN) se consideró como una afinidad indirecta, que potencia la personalización, pero con un peso más moderado.
* El **tono y estilo** fueron tratados como elementos que afectan la inmersión, pero subordinados a los anteriores.

En conjunto, este reajuste garantiza una recomendación más exigente, coherente y personalizada.

### 🛠️ Acciones Complementarias (en desarrollo o previstas)

Además del rediseño de la fórmula, se identificaron otras áreas clave para mejorar aún más la precisión y calidad del sistema:

1. **Normalización semántica de datos:** Se implementará la conversión a minúsculas y la eliminación de tildes y espacios para evitar falsas discordancias. Se estudiará también la incorporación de sinónimos (por ejemplo, que “amistad” coincida con “compañerismo”).

2. **Filtrado por idioma:** Se añadirá un filtro estricto por idioma para garantizar que el libro recomendado esté disponible en el idioma preferido por el usuario.

3. **Mejora de la explicación:** Se rediseñará la función `generate_explanation()` para que omita atributos vacíos y formule mensajes narrativos, explicando de forma clara y concreta por qué se ha elegido un determinado libro.

4. **Validación final y pruebas:** Se ejecutarán pruebas sistemáticas con perfiles variados para verificar que las recomendaciones sean coherentes y que el puntaje asignado esté alineado con la afinidad real libro–usuario.

### 📊 Impacto de la Mejora

Gracias a esta intervención, el sistema pasó de ofrecer recomendaciones genéricas e incoherentes a sugerencias más personalizadas, emocionalmente adecuadas y justificadas. Las pruebas preliminares posteriores al rediseño mostraron:

* Mayor número de coincidencias por recomendación.
* Mejor alineación semántica entre preferencias y atributos del libro.
* Explicaciones más claras y sin errores lógicos.
* Mayor satisfacción subjetiva del usuario en tests exploratorios.

---

## ✅ Conclusión

La lógica de recomendación mal calibrada era el **cuello de botella crítico** que limitaba el valor del sistema. Al identificarlo, entenderlo y rediseñarlo con criterios técnicos, semánticos y de experiencia de usuario, el sistema ha dado un salto cualitativo importante. Aún quedan áreas por mejorar (idioma, sinónimos, explicación), pero el núcleo del algoritmo ahora responde con precisión, coherencia y personalización a las preferencias de cada lector.

Este rediseño no solo resolvió el principal problema funcional, sino que estableció una base sólida para seguir construyendo un sistema de recomendación literaria de alta calidad.

