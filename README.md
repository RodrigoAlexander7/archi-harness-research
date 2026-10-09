# 🏛️ Archi Research Harness

**Suite agéntica de aceleración científica para investigadores, tesistas y autores que publican en revistas indexadas JCR / Scopus (Q1, Q2 y Q3) y conferencias internacionales.**

Diseñado para transformar borradores, tesis e hipótesis en manuscritos de alto impacto científico, automatizando desde la revisión sistemática de literatura hasta la auditoría adversarial previa al envío.

---

## ✨ Características Finales (Suite de Capacidades)

El harness resuelve los 6 cuellos de botella más críticos en la investigación científica:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      SUITE DE CAPACIDADES FINALES                      │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. 🎓 Estado del Arte (SLR)       │ Reportes PRISMA y Joyas 2025/2026  │
│ 2. ⚖️ Reviewer 2 & Cuartiles      │ Predicción Q1/Q2/Q3 y Claim Gap    │
│ 3. 🌐 Buscador Global (18 DBs)    │ Búsqueda multi-fuente sin API keys │
│ 4. 📚 Gestor de Citas & BibTeX    │ De DOIs a .bib validado para LaTeX │
│ 5. 📊 Estudio Gráfico Editorial   │ Figuras publicables IEEE/Springer  │
│ 6. 📡 Radar de Comunidad (30 días)│ Pulso técnico reciente y trampas   │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

### 1. 🎓 Generador Automatizado de Estado del Arte (SLR con PRISMA)
* **Qué resuelve:** Ahorra semanas de lectura desorganizada y búsquedas manuales.
* **Qué obtienes:** Introduces un tema o ecuación booleana y el arnés genera un informe completo y formal con las obras nucleares de los últimos 3 años, ordenadas por el prestigio de la revista (H5-index y citas anualizadas).
* **Trazabilidad 100% Transparente:** Genera de forma explícita el registro de identificación cruda (`fase1_identificacion_sin_filtrar.md`) y el cribado de exclusiones negativas (`fase2_cribado_exclusiones.md`), eliminando el sesgo de "caja negra".
* **Rescate de Joyas Emergentes:** Detecta y destaca automáticamente artículos recién publicados en **2025 o 2026** que aún no acumulan citas masivas pero marcan el límite del conocimiento.

### 2. ⚖️ Auditor Adversarial de Ideas y Predicción de Cuartiles (Reviewer 2 Suite)
* **Qué resuelve:** Evita el rechazo editorial (*Desk Reject*) antes de que envíes tu manuscrito a una revista.
* **Qué obtienes:** Presentas tu borrador, abstract o código y recibes un diagnóstico transparente e implacable:
  * **Predicción Cuantitativa de Cuartiles:** Probabilidad estimada de aceptación en **Scopus Q3**, **Scopus Q2** y **JCR/Scopus Q1**.
  * **Verificación de Evidencia (*Claim-Evidence Gap*):** Detecta promesas en el texto que no cuentan con respaldo en las tablas (ej. prometer "video en tiempo real" con solo 3 FPS, o alegar robustez en clases minoritarias con $N < 50$).
  * **Radar de Trampas Técnicas (*Known Pitfalls*):** Alerta sobre discontinuidades angulares, degradación por cuantización INT8, o calentamiento térmico acumulativo en microcomputadores.
  * **Matriz de Delta Experimental Mínimo:** Te indica los experimentos exactos necesarios para asegurar publicación en Q3 o ascender a Q2/Q1.

### 3. 🌐 Buscador Académico Global Multi-Fuente (18 Bases de Datos)
* **Qué resuelve:** Rompe las barreras de dispersión bibliográfica y muros de pago.
* **Qué obtienes:** Localización instantánea de metadatos, resúmenes completos y enlaces directos a PDFs en acceso abierto a través de **OpenAlex, arXiv, Semantic Scholar, PubMed, Crossref** y más, **sin costo de licencias ni API keys**.
* **Integración Universitaria:** Permite importar directamente archivos `.csv` o `.bib` exportados con tu cuenta institucional de **Scopus** o **Web of Science**.

### 4. 📚 Gestor Automatizado de Referencias y BibTeX
* **Qué resuelve:** Errores de sintaxis en LaTeX, nombres de autores corruptos o citas fantasma generadas por LLMs.
* **Qué obtienes:** A partir de los DOIs y artículos seleccionados, genera automáticamente un archivo `references.bib` estandarizado y libre de caracteres inválidos, listo para compilar con `pdflatex`, `xelatex` o en Overleaf.

### 5. 📊 Estudio Editorial de Gráficos Científicos
* **Qué resuelve:** Figuras rechazadas por los comités de revistas debido a baja resolución (DPI), fuentes ilegibles o formatos no vectoriales.
* **Qué obtienes:** Scripts en Python listos para generar curvas de pérdida, matrices de confusión, diagramas de compensación latencia vs. exactitud y distribuciones de datos con la paleta de colores, tipografías y proporciones exigidas por **IEEE, Springer Nature y Elsevier**.

### 6. 📡 Radar de Tendencias y Consenso Comunitario (Últimos 30 Días)
* **Qué resuelve:** Empezar a programar con una librería o modelo que la comunidad técnica ya demostró que falla o está roto en producción.
* **Qué obtienes:** Rastreo ágil en foros técnicos (Reddit, Hacker News, X) sobre el rendimiento real, problemas de memoria, cuellos de botella y compatibilidad de modelos o herramientas recién lanzados al mercado.

---

## 📁 Aislamiento y Organización Limpia (Regla 04)

Toda consulta o análisis vive en una subcarpeta dedicada y autocontenida dentro de `outputs/[nombre_de_propuesta]/`. Ninguna ejecución ensucia la raíz del repositorio ni sobreescribe experimentos anteriores:

```text
outputs/yolo11n_obb_peruvian_traffic_v2/
├── raw/
│   └── articles.json                         # Corpus JSON normalizado de artículos
├── fase1_identificacion_sin_filtrar.md       # Fase 1: Pool de candidatos crudos (PRISMA)
├── fase2_cribado_exclusiones.md              # Fase 2: Registro explícito de descartes (Filtro NOT)
├── summary_table.md                          # Fase 3: Tabla Top 10 por H5-index y Joyas 2026
├── auditoria_profunda_dictamen.md            # Fase 4: Dictamen Reviewer 2, Claim Gap y Cuartiles
├── references.bib                            # Archivo BibTeX estandarizado para LaTeX
└── report.md                                 # Reporte formal exhaustivo del Estado del Arte
```

---

## 🚀 Inicio Rápido (Quickstart)

### 1. Instalación
El repositorio utiliza [`uv`](https://github.com/astral-sh/uv) para una gestión de paquetes ultrarrápida:

```bash
# Clonar y entrar al repositorio
cd ~/Documents/PROFESIONAL/archi-harness

# Crear entorno virtual e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 2. Comandos Principales

#### 🔍 Generar Estado del Arte (SLR)
```bash
uv run python skills/literature-harvester/scripts/search_openalex.py \
    --include "oriented bounding box" vehicle detection traffic edge YOLO \
    --exclude satellite remote_sensing maritime ships \
    --years 3 \
    --max 35 \
    --output outputs/mi_propuesta/raw/articles.json

# Clasificar por H5-index y detectar Joyas Emergentes
uv run python skills/literature-harvester/scripts/rank_and_filter.py \
    --input outputs/mi_propuesta/raw/articles.json \
    --top 10 \
    --emerging 2 \
    --format markdown \
    --output outputs/mi_propuesta/summary_table.md
```

#### ⚖️ Auditar Manuscrito o Propuesta (Reviewer 2 Suite)
```bash
uv run python skills/paper-validator/scripts/deep_audit.py \
    --idea "/ruta/al/manuscrito.tex" \
    --literature outputs/mi_propuesta/raw/articles.json \
    --query-arxiv \
    --output outputs/mi_propuesta/auditoria_profunda_dictamen.md
```

#### 🌐 Búsqueda en arXiv y Bases de Datos Especializadas
```bash
# Consultar preprints en arXiv directamente
curl -s "https://export.arxiv.org/api/query?search_query=all:oriented+vehicle+detection&max_results=5" | \
    uv run python skills/paper-lookup/scripts/arxiv_atom.py -
```

---

## 🤖 Interacción Conversacional con el Agente

No necesitas memorizar comandos. Puedes interactuar en lenguaje natural con el agente dentro de este entorno:

* **Para una revisión de literatura:**  
  > *"Quiero hacer el estado del arte sobre detección orientada de vehículos en microcontroladores para una revista Scopus Q3."*
* **Para auditar tu borrador:**  
  > *"Audita este manuscrito en LaTeX y dime qué experimentos mínimos me faltan para asegurar aceptación sin desk reject."*
* **Para resolver un problema metodológico:**  
  > *"Tengo un desbalance de 1 a 80 en mototaxis, ¿qué técnicas recientes de 2025/2026 recomienda el estado del arte?"*

---

## 📜 Licencia y Buenas Prácticas
Diseñado bajo estándares de investigación abierta, reproducibilidad computacional y adherencia estricta a las directrices de integridad científica de **COPE** (Committee on Publication Ethics).
