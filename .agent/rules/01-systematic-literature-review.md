# Regla 01: Protocolo de Estado del Arte Sistematizado (SLR)

Este protocolo formaliza la metodología rigurosa para construir el estado del arte de una investigación con miras a publicaciones en revistas indexadas **JCR / Scopus (Q1/Q2)**.

---

## Metodología en 7 Pasos

### Paso 1: Búsqueda Booleana Avanzada con Palabras Clave Atómicas
- **Regla estricta:** NUNCA coloques frases en lenguaje natural en los motores de búsqueda (ej. NO usar: *"métodos de computación cuántica para la búsqueda de caminos en un grafo"*).
- **Correcto:** Extrae las entidades conceptuales nucleares y combínalas con operadores booleanos:
  - Término 1 (Dominio): `"quantum"`
  - Término 2 (Estructura/Técnica): `"graphs"` o `"graph theory"`
  - Combinación: `"quantum" AND ("graphs" OR "graph algorithms")`
- Fuentes recomendadas: OpenAlex (indexa IEEE, ACM, Springer, Elsevier de forma abierta y gratuita), Scopus y Web of Science (con acceso institucional).

### Paso 2: Ventana Temporal (Filtro por Antigüedad)
- **Filtro inicial:** Limita la búsqueda a los **últimos 3 años** (ej. 2024–2026).
- **Excepción de ampliación:** Si la cantidad de resultados relevantes es inferior a 15 artículos, amplía la ventana a los **últimos 5 años** (ej. 2022–2026).

### Paso 3: Filtrado Negativo por Términos de Exclusión (`NOT`)
- Identifica disciplinas adyacentes no deseadas que distorsionen los resultados.
- *Ejemplo en Ciencias de la Computación / Cuántica:* Si buscas algoritmos cuánticos en grafos pero aparecen artículos de física teórica pura, aplica exclusión de palabras en título/abstract:
  - `EXCLUDE = ["Mechanics", "Optics", "Thermodynamics", "Materials"]`
- Esto reduce el ruido inicial de cientos de artículos a una lista manejable de ~30 a 50 artículos altamente pertinentes.

### Paso 4: Extracción de Metadatos y Abstract
- Para cada artículo de la lista filtrada, extrae y almacena:
  - Título
  - Abstract completo
  - Autores y Año de publicación
  - Nombre del Journal o Conferencia (Venue)
  - DOI y URL
  - Número de citas recibidas
  - Indicador de Open Access (`true` / `false`)

### Paso 5: Ranking Multidimensional de Prestigio e Impacto
Ordena la lista de artículos evaluando tres dimensiones:
1. **Impacto del Artículo:** Número absoluto de citas recibidas y **tasa de citación anual** ($\text{Citas} / (\text{Año Actual} - \text{Año Pub} + 1)$).
2. **Prestigio del Venue (Journal / Conferencia):**
   - Medido a través del **H5-index** (Google Scholar Metrics) o Cuartil JCR/Scimago SJR (Q1 > Q2 > Q3 > Q4).
   - *Referencia de H-index:*
     - Eventos / Revistas top mundiales: H-index > 150
     - Revistas IEEE / ACM Transactions de referencia: H-index 40 - 90
     - Revistas regionales / especializadas: H-index 10 - 30
3. **Puntaje Compuesto ($Score$):**
   $$\text{Score} = (\text{Citas Anualizadas} \times 0.4) + (\text{H-index Venue} \times 0.4) + (\text{Similitud Abstract} \times 0.2)$$

### Paso 6: Corte Selectivo (Top 5 a 10 Artículos Nucleares)
- Reduce la lista a los **5 a 10 artículos más influyentes y directamente comparables**, que constituirán la columna vertebral de la sección de "Trabajos Relacionados" y los baselines obligatorios.

### Paso 7: Inyección Manual de "Joyas Emergentes"
- No limites la revisión exclusivamente a artículos hipercitados.
- **Regla de Joya Emergente:** Agrega 1 o 2 artículos publicados en el año en curso (2025 o 2026) que aún tengan 0 o muy pocas citas pero que coincidan exactamente con la propuesta metodológica que deseas realizar.
