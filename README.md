# Archi Research Harness

Harness agéntico para revisión sistemática de literatura y validación estratégica de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2)** en ingeniería y ciencias.

---

## Arquitectura Híbrida: Reglas (Guardrails) + Skills de Orquestación

El arnés combina **reglas del sistema** (que prohíben la superficialidad y fuerzan rigor) con **skills modulares** (que ejecutan los flujos paso a paso):

```
archi-harness/
├── .agent/
│   ├── rules/
│   │   ├── 00-router.md                      # Enrutador de tareas según la intención del usuario
│   │   ├── 01-systematic-literature-review.md # Guardrail estricto: obliga a invocar systematic-slr
│   │   ├── 02-paper-idea-validator.md        # Criterios implacables de Reviewer 2 para revistas Q1/Q2
│   │   └── 03-venue-evaluation-criteria.md   # Criterios de indexación (H5-index, SJR, JCR)
│   └── templates/
│       ├── slr_report_template.md            # Plantilla formal para el estado del arte
│       └── paper_validation_report_template.md # Plantilla formal de dictamen y pivotes a Q1
├── skills/
│   ├── systematic-slr/                       # << SKILL ORQUESTADORA DE 7 PASOS >>
│   │   └── SKILL.md                          # Flujo con checkpoints interactivos
│   ├── literature-harvester/                 # << SKILL DE EXTRACCIÓN Y RANKING >>
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── search_openalex.py            # Búsqueda abierta (IEEE, ACM, Springer) sin API key
│   │       ├── import_scopus_wos.py          # Ingesta de CSV/BibTeX con acceso universitario
│   │       └── rank_and_filter.py            # Ranking por H5-index, citas anuales y Joyas Emergentes
│   └── paper-validator/                      # << SKILL AUDITORA DE IDEAS >>
│       ├── SKILL.md
│       └── scripts/
│           └── assess_novelty.py             # Detección de solapamiento semántico bilingüe y plan de pivote
├── data/
│   └── venues_hindex.json                    # Base curada de cuartiles Q1/Q2 y H5 de revistas top
├── investigations/                           # Espacio de trabajo para cada proyecto
├── pyproject.toml
└── README.md
```

---

## Catálogo de Skills

### 1. `systematic-slr` (Orquestación del Estado del Arte)
Implementa el protocolo de 7 pasos diseñado por investigadores experimentados:
1. **Descomposición booleana atómica:** Prohibido usar lenguaje natural en motores de búsqueda.
2. **Checkpoint de términos:** El agente valida las palabras clave y el filtro negativo (`NOT`) con el investigador antes de extraer.
3. **Ventana de 3 a 5 años:** Prioriza literatura reciente.
4. **Filtro de exclusión negativa:** Elimina ruido de disciplinas adyacentes (ej. `mechanics optics` en computación).
5. **Ranking multidimensional:** Pondera citas anuales con el prestigio del journal (H5-index y cuartil).
6. **Checkpoint de Joyas Emergentes:** El sistema reserva cupos para artículos de 2025/2026 y consulta al investigador si desea incorporar preprints recientes sin citas.
7. **Generación del entregable:** Redacción del reporte estructurado con enlaces DOI institucionales.

### 2. `literature-harvester` (Extracción y Procesamiento)
* **OpenAlex API:** Descarga metadatos completos, títulos y abstracts reconstruidos de editoriales como IEEE, ACM, Springer, Elsevier y Nature sin requerir claves de pago.
* **Scopus & Web of Science Importer:** Si tienes acceso universitario, puedes exportar búsquedas en CSV o BibTeX y colocarlas en `investigations/<tema>/raw/`; el script `import_scopus_wos.py` las procesa directamente.
* **Ranking Multidimensional:** Identifica artículos canónicos consolidados y Joyas Emergentes de 2025/2026.

### 3. `paper-validator` (Reviewer 2 y Viabilidad Q1/Q2)
* **Auditoría Adversarial:** Compara la idea del paper contra el corpus recopilado calculando solapamiento semántico conceptual (soporta español e inglés).
* **Cálculo de Probabilidad:** Estima las probabilidades reales de aceptación en revistas Q1 vs Q2.
* **Planes de Pivote:** Genera 3 opciones estratégicas (Complejidad/Escala, Estudio de Ablación o Frontera de Pareto/Eficiencia) para elevar una idea con riesgo de rechazo a nivel Q1.

---

## Instalación y Configuración

```bash
# Entrar al repositorio
cd ~/Documents/PROFESIONAL/archi-harness

# Crear entorno virtual con uv e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## Guía de Uso Rápido

### A. Ejecutar una Búsqueda Sistematizada (SLR)
```bash
# 1. Extraer artículos de repositorios abiertos
python skills/literature-harvester/scripts/search_openalex.py \
    --include quantum graph routing \
    --exclude mechanics optics \
    --years 3 \
    --max 30 \
    --output investigations/mi_proyecto/raw/articles.json

# 2. Generar ranking con H5-index y Joyas Emergentes
python skills/literature-harvester/scripts/rank_and_filter.py \
    --input investigations/mi_proyecto/raw/articles.json \
    --top 10 \
    --emerging 2 \
    --format markdown \
    --output investigations/mi_proyecto/summary_table.md
```

### B. Importar datos exportados de Scopus / Web of Science (Universidad)
```bash
python skills/literature-harvester/scripts/import_scopus_wos.py \
    --input investigations/mi_proyecto/raw/scopus_export.csv \
    --output investigations/mi_proyecto/raw/articles.json
```

### C. Validar una Idea de Paper contra el Estado del Arte
```bash
python skills/paper-validator/scripts/assess_novelty.py \
    --idea "Proponemos un algoritmo híbrido cuántico en grafos para ruteo de vehículos con atención neuronal" \
    --literature investigations/mi_proyecto/raw/articles.json \
    --output investigations/mi_proyecto/paper_validation_dictamen.md
```
