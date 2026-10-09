---
name: literature-harvester
description: Extrae, filtra por operadores booleanos y palabras negativas, y clasifica literatura científica de OpenAlex, Scopus y Web of Science con métricas H5 y cuartiles Q1/Q2.
---

# Literature Harvester Skill

Esta habilidad automatiza la fase empírica del Estado del Arte Sistematizado (SLR) siguiendo el protocolo de 7 pasos:

1. **Búsqueda Agéntica e Iterativa (Recomendado):** Usa `scripts/iterative_harvest.py` con `--idea` y `--seed` opcional. Ejecuta un bucle reflexivo de refinamiento de ecuaciones, filtra ruido mediante un crítico semántico 1 a 1, produce el pool de 20 candidatos (`top20_candidatos_revisados.md`) y el Top 10 ordenado (`summary_table.md` + `references.bib`).
2. **Búsqueda Booleana Directa:** Usa `scripts/search_openalex.py` con términos atómicos (`--include`, `--exclude`, `--axes`, `--seed`).
3. **Ingesta Institucional:** Si el usuario tiene exportaciones de Scopus o WoS en CSV/BibTeX, usa `scripts/import_scopus_wos.py`.
4. **Ranking y Joyas Emergentes:** Usa `scripts/rank_and_filter.py` para generar la tabla top con cálculo de citas anuales, H5-index y rescate de artículos clave del año en curso.

## Comandos Clave

```bash
# 1. Búsqueda Agéntica e Iterativa (Bucle Inteligente -> Top 20 -> Top 10)
uv run python skills/literature-harvester/scripts/iterative_harvest.py \
    --idea "/ruta/al/manuscrito.tex o descripción textual de la idea" \
    --seed "10.1109/ELMAR66948.2025.11193980" \
    --target-pool 20 \
    --final-top 10 \
    --output-dir outputs/<nombre_de_propuesta>

# 2. Búsqueda Directa en OpenAlex
uv run python skills/literature-harvester/scripts/search_openalex.py \
    --include quantum graph \
    --exclude mechanics optics \
    --years 3 \
    --max 30 \
    --output outputs/<tema>/raw/articles.json

# 3. Importar CSV de Scopus institucional
uv run python skills/literature-harvester/scripts/import_scopus_wos.py \
    --input outputs/<tema>/raw/scopus_export.csv \
    --output outputs/<tema>/raw/articles.json

# 4. Generar Tabla Top 10 con Joyas Emergentes
uv run python skills/literature-harvester/scripts/rank_and_filter.py \
    --input outputs/<tema>/raw/articles.json \
    --top 10 \
    --emerging 2 \
    --format markdown \
    --output outputs/<tema>/summary_table.md
```

