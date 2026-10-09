# Regla 00: Enrutador del Harness de Investigación

Este arnés orquesta la investigación científica rigurosa y la validación de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2/Q3)** en ingeniería y ciencias.

---

## 1. Clasificación de la Intención del Investigador

Al recibir cualquier solicitud, clasifica la tarea y activa la skill o script correspondiente:

| Intención | Descripción | Skill / Herramienta Principal | Origen |
| :--- | :--- | :--- | :--- |
| **`SLR_DISCOVERY`** | Búsqueda y estado del arte sistematizado en 7 pasos | `skills/systematic-slr` (Guía paso a paso) | Nativa |
| **`PAPER_VALIDATION`** | Evaluar idea de paper con entrevista y Reviewer 2 | `skills/paper-validator` (Intake + Cuartiles) | Nativa |
| **`MULTI_SCHOLAR_LOOKUP`** | Búsqueda en 18 APIs académicas (PubMed, arXiv, Crossref) | `skills/paper-lookup` | K-Dense (`scientific-agent-skills`) |
| **`BIBTEX_MANAGEMENT`** | Conversión DOI a BibTeX y validación de referencias | `skills/citation-management` | K-Dense (`scientific-agent-skills`) |
| **`MANUSCRIPT_AUDIT`** | Revisión editorial exhaustiva de borrador completo | `skills/peer-review` | K-Dense (`scientific-agent-skills`) |
| **`ACADEMIC_PLOTTING`** | Gráficas y curvas en Python con estándar IEEE/Springer | `skills/academic-plotting` | Orchestra (`AI-research-SKILLs`) |
| **`PAPER_WRITING_GUIDE`** | Guía de redacción de papers de ML y sistemas para journals | `skills/ml-paper-writing` | Orchestra (`AI-research-SKILLs`) |
| **`COMMUNITY_PULSE`** | Rastreo de tendencias recientes en Reddit, HN y X | `skills/last30days` | mvanhorn (`last30days-skill`) |
| **`IMPORT_INSTITUTIONAL`** | Ingesta de exportaciones CSV/BibTeX de Scopus/WoS | `skills/literature-harvester/scripts/import_scopus_wos.py` | Nativa |

---

## 2. Protocolo de Ejecución y Trazabilidad

1. **Estado del Arte Sistematizado (SLR):**
   - Siempre ejecuta con trazabilidad explícita: genera `fase1_identificacion_sin_filtrar.md`, `fase2_cribado_exclusiones.md` y `summary_table.md` antes del reporte final.
2. **Validación de Ideas (Reviewer 2):**
   - Aplica primero la entrevista de admisión de 6 dimensiones (`skills/paper-validator/references/intake_rubric.md`).
   - Compara con el estado del arte y emite veredicto transparente de cuartiles.
3. **Escritura y Gráficos:**
   - Para las figuras del paper (curvas de scaling, matrices de confusión), utiliza los estilos editoriales de `skills/academic-plotting`.
   - Para generar las referencias bibliográficas sin errores, utiliza `skills/citation-management`.
