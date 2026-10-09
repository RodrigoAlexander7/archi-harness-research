# Archi Research Harness

Harness agéntico para revisión sistemática de literatura y validación estratégica de ideas de investigación enfocadas en **revistas indexadas JCR / Scopus (Q1/Q2)** en ingeniería y ciencias.

---

## Características Principales

1. **Protocolo SLR Sistematizado en 7 Pasos:** Metodología estandarizada para filtrado booleano, eliminación de ruido (`NOT`), ranking por H-index y citas anualizadas.
2. **Consultas a Repositorios Abiertos:** Búsqueda y reconstrucción de abstracts vía OpenAlex (IEEE, ACM, Springer, Elsevier) sin necesidad de API keys de pago.
3. **Integración con Acceso Universitario:** Ingesta y normalización de archivos CSV/BibTeX exportados desde Scopus y Web of Science.
4. **Validador de Ideas y Reviewer Adversarial:** Diagnóstico transparente de novedades, brechas de baselines y cálculo de probabilidades de aceptación en revistas Q1/Q2.
5. **Catálogo de Venues y H5-Index:** Calibración automática con Google Scholar Metrics y cuartiles Scimago/JCR.

---

## Instalación y Configuración

```bash
# Clonar y entrar al repositorio
cd ~/Documents/PROFESIONAL/archi

# Crear entorno virtual con uv e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## Uso Rápido

### 1. Búsqueda de Estado del Arte
```bash
python skills/literature-harvester/scripts/search_openalex.py \
    --include quantum graph \
    --exclude mechanics optics \
    --years 3 \
    --max 30 \
    --output investigations/2026-10-09_quantum_graphs/raw/articles.json
```

### 2. Filtrado y Ranking Multidimensional
```bash
python skills/literature-harvester/scripts/rank_and_filter.py \
    --input investigations/2026-10-09_quantum_graphs/raw/articles.json \
    --top 10 \
    --format markdown
```
