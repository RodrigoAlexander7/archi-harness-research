# Regla 00: Enrutador del Harness de Investigación

Este arnés orquesta la investigación científica rigurosa y la validación de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2/Q3)** en ingeniería y ciencias.

---

## 1. Clasificación de la Intención del Investigador

Al recibir cualquier solicitud, clasifica la tarea y activa la skill o script correspondiente:

| Intención | Descripción | Skill / Herramienta Principal | Origen |
| :--- | :--- | :--- | :--- |
| **`SLR_DISCOVERY`** | Búsqueda agéntica iterativa (Top 20 -> Top 10) con crítico 1 a 1 | `skills/literature-harvester/scripts/iterative_harvest.py` | Nativa |
| **`PAPER_VALIDATION`** | Evaluar idea de paper con entrevista y Reviewer 2 | `skills/paper-validator` (Intake + Cuartiles) | Nativa |
| **`MULTI_SCHOLAR_LOOKUP`** | Búsqueda en 18 APIs académicas (PubMed, arXiv, Crossref) | `skills/paper-lookup` | K-Dense (`scientific-agent-skills`) |
| **`BIBTEX_MANAGEMENT`** | Conversión DOI a BibTeX y validación de referencias | `skills/citation-management` | K-Dense (`scientific-agent-skills`) |
| **`MANUSCRIPT_AUDIT`** | Revisión editorial exhaustiva de borrador completo | `skills/peer-review` | K-Dense (`scientific-agent-skills`) |
| **`ACADEMIC_PLOTTING`** | Gráficas y curvas en Python con estándar IEEE/Springer | `skills/academic-plotting` | Orchestra (`AI-research-SKILLs`) |
| **`PAPER_WRITING_GUIDE`** | Guía de redacción de papers de ML y sistemas para journals | `skills/ml-paper-writing` | Orchestra (`AI-research-SKILLs`) |
| **`WEB_DEEP_RESEARCH`** | Investigación web profunda en blogs, docs y reportes | `skills/gpt-researcher` | Assaf Elovic (`gpt-researcher`) |
| **`COMMUNITY_PULSE`** | Rastreo de tendencias recientes en Reddit, HN y X | `skills/last30days` | mvanhorn (`last30days-skill`) |
| **`IMPORT_INSTITUTIONAL`** | Ingesta de exportaciones CSV/BibTeX de Scopus/WoS | `skills/literature-harvester/scripts/import_scopus_wos.py` | Nativa |

---

## 2. Protocolo de Ejecución y Trazabilidad

1. **Estado del Arte Sistematizado (SLR):**
   - Siempre ejecuta el motor agéntico `iterative_harvest.py`: genera de forma obligatoria `top20_candidatos_revisados.md` (pool auditable) y `summary_table.md` (Top 10 ordenado) + `references.bib` antes de redactar el informe final.
2. **Validación de Ideas (Reviewer 2):**
   - Aplica primero la entrevista de admisión de 6 dimensiones (`skills/paper-validator/references/intake_rubric.md`).
   - Compara con el estado del arte y emite veredicto transparente de cuartiles.
3. **Escritura y Gráficos:**
   - Para las figuras del paper (curvas de scaling, matrices de confusión), utiliza los estilos editoriales de `skills/academic-plotting`.
   - Para generar las referencias bibliográficas sin errores, utiliza `skills/citation-management`.
4. **Aislamiento Estricto de Salidas (Regla 04):**
   - Todos los entregables deben generarse dentro de `outputs/[nombre_de_propuesta]/`. Jamás escribas en la raíz de `outputs/` para no ensuciar el repositorio y permitir comparativas de rendimiento.
