# Archi Research Harness

Harness agéntico para revisión sistemática de literatura y validación estratégica de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2/Q3)** y conferencias en ingeniería y ciencias.

---

## Arquitectura del Harness

El arnés combina **reglas del sistema** (guardrails que prohíben la superficialidad) con **skills modulares y ejecutables**:

```text
archi-harness/
├── .agent/
│   ├── rules/
│   │   ├── 00-router.md                      # Enrutador de intenciones del usuario
│   │   ├── 01-systematic-literature-review.md # Guardrail estricto: activa systematic-slr
│   │   ├── 02-paper-idea-validator.md        # Rúbrica adversarial para revistas Q1/Q2/Q3
│   │   └── 03-venue-evaluation-criteria.md   # Criterios H5-index, SJR y JCR
│   └── templates/
│       ├── slr_report_template.md            # Plantilla formal de estado del arte
│       └── paper_validation_report_template.md # Plantilla formal de dictamen y pivotes
├── skills/
│   ├── systematic-slr/                       # Orquestador del protocolo de 7 pasos (SLR)
│   ├── literature-harvester/                 # Extracción con OpenAlex y Scopus/WoS
│   ├── paper-validator/                      # Validador de ideas & Reviewer 2 adversarial
│   ├── paper-lookup/                         # Conector multi-API a 18 bases académicas (K-Dense)
│   ├── citation-management/                  # Conversión DOI a BibTeX y validación de citas (K-Dense)
│   ├── peer-review/                          # Auditoría formal de manuscritos según directrices (K-Dense)
│   ├── academic-plotting/                    # Generador de gráficas científicas para IEEE/Springer (Orchestra)
│   ├── ml-paper-writing/                     # Guías y estructura para redacción de papers de ML (Orchestra)
│   ├── gpt-researcher/                       # Investigación web autónoma y reportes con citas (Assaf Elovic)
│   └── last30days/                           # Rastreador de tendencias y pulso comunitario en Reddit/HN/X (mvanhorn)
├── data/
│   └── venues_hindex.json                    # Base curada de cuartiles Q1/Q2/Q3 y H5 de journals top
├── investigations/                           # Proyectos e investigaciones en curso
├── outputs/                                  # Entregables con trazabilidad en fases (Fase 1 a 4)
├── pyproject.toml
└── README.md
```

---

## Instalación y Configuración

El entorno utiliza [`uv`](https://github.com/astral-sh/uv) para una gestión de dependencias rápida y reproducible:

```bash
# 1. Clonar y entrar al repositorio
cd ~/Documents/PROFESIONAL/archi-harness

# 2. Crear entorno virtual con uv e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## 📚 Guía Exhaustiva de Funcionalidades y Modo de Uso

El arnés dispone de **6 funcionalidades nucleares**. A continuación se detalla el propósito de cada una, sus comandos y ejemplos prácticos:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FLUJOS Y FUNCIONALIDADES                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. search_openalex.py             │ Búsqueda abierta sin API keys      │
│ 2. import_scopus_wos.py           │ Ingesta de Scopus/WoS universitario│
│ 3. rank_and_filter.py             │ Ranking H5-index y Joyas 2025/2026 │
│ 4. systematic-slr                 │ Orquestación guiada en 7 pasos     │
│ 5. Entrevista de Admisión         │ "Grill the Idea" (6 dimensiones)   │
│ 6. assess_novelty.py              │ Reviewer 2 & Estimador de Cuartil  │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

### Funcionalidad 1: Búsqueda Abierta de Literatura (`search_openalex.py`)

* **Propósito:** Consulta la API abierta de OpenAlex para buscar literatura indexada de IEEE, ACM, Springer, Elsevier, Nature y Wiley **sin requerir claves de API de pago ni registros**. Reconstruye el texto completo del abstract, extrae DOIs, autores, año, citas y detecta si es de acceso abierto o de pago.
* **Argumentos:**
  * `--include`: Palabras clave atómicas a incluir (ej: `quantum graph routing`).
  * `--exclude`: Palabras clave negativas para purgar disciplinas ajenas (ej: `mechanics optics`).
  * `--years`: Ventana temporal hacia atrás (por defecto `3`, ampliable a `5`).
  * `--max`: Cantidad máxima de artículos a recuperar (por defecto `30`).
  * `--output`: Archivo JSON donde se guardarán los resultados.

* **Ejemplo de Uso:**
```bash
python skills/literature-harvester/scripts/search_openalex.py \
    --include "oriented bounding box" vehicle traffic edge \
    --exclude mechanics optics \
    --years 3 \
    --max 30 \
    --output investigations/mi_proyecto/raw/articles.json
```

---

### Funcionalidad 2: Ingesta de Scopus y Web of Science (`import_scopus_wos.py`)

* **Propósito:** Si cuentas con acceso institucional a través de tu universidad a **Scopus** o **Web of Science**, puedes realizar una búsqueda avanzada en sus portales web, descargar el archivo de exportación en formato **CSV o BibTeX (`.bib`)** y normalizarlo automáticamente al esquema unificado del arnés.
* **Argumentos:**
  * `--input`: Ruta al archivo `.csv` o `.bib` exportado.
  * `--output`: Ruta al archivo `.json` resultante normalizado.

* **Ejemplo de Uso:**
```bash
python skills/literature-harvester/scripts/import_scopus_wos.py \
    --input investigations/mi_proyecto/raw/scopus_export.csv \
    --output investigations/mi_proyecto/raw/articles.json
```

---

### Funcionalidad 3: Ranking Multidimensional y Detección de Joyas Emergentes (`rank_and_filter.py`)

* **Propósito:** Aplica la fórmula de clasificación para ordenar los artículos según su relevancia científica real:
  $$\text{Score} = (\text{Citas Anuales} \times 0.45) + (\text{H5-Index} \times 0.35) + \text{Bonus Cuartil (Q1/Q2)}$$
  Automáticamente aparta y destaca **Joyas Emergentes** (artículos de 2025 o 2026 que tienen pocas o 0 citas por su recencia pero alta afinidad técnica).
* **Argumentos:**
  * `--input`: Archivo JSON con los artículos extraídos.
  * `--top`: Cantidad de artículos finales a retener en la tabla principal (por defecto `10`).
  * `--emerging`: Número de cupos reservados para Joyas Emergentes (por defecto `2`).
  * `--format`: Formato de salida (`markdown` para tablas legibles o `json` para pipelines).
  * `--output`: Ruta donde guardar el archivo (opcional).

* **Ejemplo de Uso:**
```bash
python skills/literature-harvester/scripts/rank_and_filter.py \
    --input investigations/mi_proyecto/raw/articles.json \
    --top 10 \
    --emerging 2 \
    --format markdown \
    --output investigations/mi_proyecto/summary_table.md
```

* **Salida Típica en Markdown:**
```markdown
| # | Título | Año | Journal / Venue | Cuartil | H5 | Citas (Anual.) | Tipo | Acceso | DOI |
|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Edge ML Technique for Smart Traffic... | 2024 | IEEE Access | Q2 | 95 | 88 (29.3) | SOTA Benchmark | 🔓 Open Access | [10.1109/...](...) |
| 2 | A Cascaded Framework for Vehicle...   | 2026 | Electronics | Q2 | 80 | 1 (1.0) | 💎 Joya Reciente | 🔒 Paywall (Univ) | [10.3390/...](...) |
```

---

### Funcionalidad 4: Orquestación Guiada del Estado del Arte (`systematic-slr`)

* **Propósito:** Orquesta el protocolo de 7 pasos a través del agente interactivo, evitando que se omitan pasos o se improvise con búsquedas superficiales.
* **Puntos de Control (*Checkpoints*):**
  * **Checkpoint 1:** El agente descompone la idea en términos atómicos en inglés y define los términos `NOT`. Te presenta la ecuación para que la valides antes de realizar la descarga.
  * **Checkpoint 2:** Tras el ranking, te muestra las Joyas Emergentes detectadas y te consulta si deseas inyectar manualmente algún paper o preprint reciente que conozcas.
* **Cómo Usarlo en el Chat del Agente:**
  Basta con pedirle al agente:
  > *"Quiero hacer el estado del arte sobre detección de vehículos orientados en edge computing para una revista Q3"*.
  El agente activará automáticamente `skills/systematic-slr/SKILL.md` y te guiará paso a paso.

---

### Funcionalidad 5: Entrevista de Admisión Crítica (*Grill the Idea*)

* **Propósito:** Antes de evaluar una idea de paper, el arnés somete al investigador a un interrogatorio estructurado en **6 dimensiones críticas** basado en [`intake_rubric.md`](skills/paper-validator/references/intake_rubric.md):
  1. **Delta Metodológico:** ¿Qué modificación técnica o matemática real se propone frente a la librería estándar?
  2. **Datasets y Disponibilidad:** ¿Son benchmarks públicos estándar o datos privados? ¿Habrá código abierto?
  3. **Baselines del SOTA (2024–2026):** ¿Contra qué modelos recientes se compara? (Prohibido comparar solo contra algoritmos de hace 5+ años).
  4. **Hipótesis Mecanicista:** ¿Por qué teóricamente este método debería superar a los existentes?
  5. **Ablaciones y Significancia:** ¿Se medirá el impacto de cada módulo y pruebas estadísticas ($p < 0.05$)?
  6. **Venue Objetivo:** ¿Revista JCR/Scopus Q1, Q2, Q3 o Conferencia CORE A*/A/B?

* **Cómo Usarlo en el Chat del Agente:**
  Comparte tu idea o abstract preliminar y el agente activará la entrevista de admisión:
  > *"Valida esta idea de paper: [pega tu abstract o idea]"*.

---

### Funcionalidad 6: Validador Adversarial & Estimador de Cuartil (`assess_novelty.py`)

* **Propósito:** Compara la idea del investigador frente al corpus recopilado de artículos del estado del arte. Realiza tokenización y normalización bilingüe (ES $\leftrightarrow$ EN), calcula el solapamiento conceptual, detecta obras competidoras (*Prior Art*), estima las probabilidades de aceptación en revistas Q1 vs Q2 vs Q3 y formula **3 planes de pivote estratégico**.
* **Argumentos:**
  * `--idea`: Texto de la idea, abstract o ruta a un archivo `.txt`/`.md`/`.tex`.
  * `--literature`: Archivo JSON con los artículos del estado del arte recopilados.
  * `--output`: Ruta donde guardar el reporte formal en Markdown.

* **Ejemplo de Uso:**
```bash
python skills/paper-validator/scripts/assess_novelty.py \
    --idea "Fine-Tuning YOLO11n-OBB for Oriented Vehicle Detection in Peruvian Traffic Scenes: Data Scaling and Edge Benchmarking on Raspberry Pi 4" \
    --literature investigations/mi_proyecto/raw/articles.json \
    --output investigations/mi_proyecto/paper_validation_dictamen.md
```

* **Salida Generada:**
  * **Diagnóstico Global:** `Viable para Revista Q2 / Q3`
  * **Probabilidades Estimadas:** Q1: 45% | Q2: 75% | Q3: 90%
  * **Prior Art Crítico:** Lista de los papers más cercanos con porcentaje de solapamiento.
  * **Venues Recomendados:** Revistas específicas que publican artículos en esa misma línea temática.
  * **Planes de Pivote:** Recomendaciones para superar la barrera del *Reviewer 2* (Pivote de Baselines, Estudio de Ablación o Frontera de Pareto/Eficiencia).

---

## Estructura de Carpetas de una Investigación

Cada proyecto de investigación vive de forma autocontenida y reproducible dentro de `investigations/<nombre_proyecto>/`:

```text
investigations/mi_proyecto/
├── raw/
│   ├── articles.json                 # Corpus de artículos descargados (OpenAlex o Scopus)
│   └── scopus_export.csv             # (Opcional) Exportación institucional
├── summary_table.md                  # Tabla Top 10 con H5-index y Joyas Emergentes
├── paper_validation_dictamen.md      # Dictamen adversarial y clasificación de cuartiles
└── report.md                         # Estado del arte y reporte final sintetizado
```
