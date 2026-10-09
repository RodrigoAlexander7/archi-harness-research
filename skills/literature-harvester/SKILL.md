---
name: literature-harvester
description: Extrae, filtra por operadores booleanos y palabras negativas, y clasifica literatura científica de OpenAlex, Scopus y Web of Science con métricas H5 y cuartiles Q1/Q2.
---

# Literature Harvester Skill

Esta habilidad automatiza la fase empírica del Estado del Arte Sistematizado (SLR) siguiendo el protocolo de 7 pasos:

1. **Búsqueda Booleana Avanzada:** Usa `scripts/search_openalex.py` con términos atómicos (`--include`).
2. **Exclusiones Negativas (`NOT`):** Usa `--exclude` para eliminar disciplinas adyacentes no deseadas.
3. **Ventana Temporal:** Por defecto 3 años (`--years 3`), expandible a 5.
4. **Ingesta Institucional:** Si el usuario tiene exportaciones de Scopus o WoS en CSV/BibTeX, usa `scripts/import_scopus_wos.py`.
5. **Ranking y Joyas Emergentes:** Usa `scripts/rank_and_filter.py` para generar la tabla top con cálculo de citas anuales, H5-index y rescate de artículos clave del año en curso.

## Comandos Clave

```bash
# Búsqueda en OpenAlex
python skills/literature-harvester/scripts/search_openalex.py \
    --include quantum graph \
    --exclude mechanics optics \
    --years 3 \
    --max 30 \
    --output investigations/<tema>/raw/articles.json

# Importar CSV de Scopus institucional
python skills/literature-harvester/scripts/import_scopus_wos.py \
    --input investigations/<tema>/raw/scopus_export.csv \
    --output investigations/<tema>/raw/articles.json

# Generar Tabla Top 10 con Joyas Emergentes
python skills/literature-harvester/scripts/rank_and_filter.py \
    --input investigations/<tema>/raw/articles.json \
    --top 10 \
    --emerging 2 \
    --format markdown \
    --output investigations/<tema>/summary_table.md
```
