# Regla 00: Enrutador del Harness de Investigación

Este arnés orquesta la investigación científica rigurosa y la validación de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2)** en ingeniería y ciencias.

## 1. Clasificación de la Intención del Investigador

Al recibir cualquier solicitud, clasifica la tarea en uno de los siguientes flujos de trabajo:

| Intención | Descripción | Skill / Script Principal | Plantilla de Salida |
| :--- | :--- | :--- | :--- |
| **`SLR_DISCOVERY`** | Búsqueda y estado del arte sistematizado desde cero | `skills/systematic-slr` (Orquestador 7 Pasos) | `slr_report_template.md` |
| **`IMPORT_INSTITUTIONAL`** | Procesar datos exportados de Scopus o Web of Science | `skills/literature-harvester/scripts/import_scopus_wos.py` | `slr_report_template.md` |
| **`PAPER_VALIDATION`** | Evaluar una idea, hipótesis o abstract para revista Q1/Q2 | `skills/paper-validator/scripts/assess_novelty.py` | `paper_validation_report_template.md` |
| **`RANK_AND_FILTER`** | Filtrar por palabras negativas y ordenar por H-index/citas | `skills/literature-harvester/scripts/rank_and_filter.py` | Tabla Top 5-10 |

---

## 2. Protocolo de Ejecución

1. **Si el usuario quiere construir el estado del arte de un tema:**
   - Sigue estrictamente la regla `01-systematic-literature-review.md`.
   - Formula palabras clave booleanas atómicas (ej: `"quantum" AND "graph"`). Nunca uses lenguaje natural como consulta.
   - Aplica ventana de 3 años (o 5 si hay escasez).
   - Aplica filtros negativos (`NOT`).
   - Descarga metadatos completos (títulos y abstracts).
   - Clasifica por impacto y prestigio del journal (H-index / Cuartiles).

2. **Si el usuario proporciona un archivo de Scopus o Web of Science:**
   - Ubica el archivo en `investigations/<nombre_proyecto>/raw/`.
   - Ejecuta `import_scopus_wos.py` para normalizar los metadatos y evaluar los abstracts.

3. **Si el usuario quiere validar una idea de paper:**
   - Sigue estrictamente la regla `02-paper-idea-validator.md`.
   - Extrae el delta técnico, baselines obligatorios y riesgos de rechazo (*Reviewer 2*).
   - Clasifica la factibilidad en JCR/Scopus Q1/Q2 y propone pivotes estratégicos.
