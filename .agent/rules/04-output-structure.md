# Regla 04: Estructura y Organización de Salidas (Outputs Isolation)

Esta regla define el protocolo estricto para almacenar todos los entregables, reportes y datasets generados durante una investigación, asegurando la limpieza y trazabilidad del repositorio.

---

## 1. Mandato Inviolable de Aislamiento de Propuestas

1. **PROHIBIDO escribir directamente en la raíz de `outputs/`:**
   - Ninguna consulta, script o reporte debe escribirse como `outputs/report.md` o `outputs/raw/`.
   - Toda ejecución debe estar confinada a una subcarpeta con el nombre de la propuesta o tema:
     `outputs/[nombre_de_propuesta]/` (ejemplo: `outputs/yolo11n_obb_peruvian_traffic_v2/`).

2. **Nomenclatura de Carpetas:**
   - Usa nombres en minúsculas, separados por guiones bajos o medios, descriptivos y únicos:
     - `outputs/<tema_o_hipotesis>/`
     - Si es una nueva versión para comparar: `outputs/<tema_o_hipotesis>_v2/`

---

## 2. Estructura Interna Estándar de cada Propuesta

Cada subcarpeta `outputs/[nombre_de_propuesta]/` debe contener exclusivamente:

```text
outputs/[nombre_de_propuesta]/
├── raw/                                      # Datos crudos y fuentes descargadas
│   ├── articles.json                         # Corpus JSON normalizado de artículos recuperados
│   └── scopus_export.csv                     # (Opcional) Exportaciones institucionales
├── fase1_identificacion_sin_filtrar.md       # Fase 1: Lista completa sin filtrar (PRISMA Identification)
├── fase2_cribado_exclusiones.md              # Fase 2: Registro de exclusiones negativas (Filtro NOT)
├── summary_table.md                          # Fase 3: Matriz Top 10 por H5-index y Joyas Emergentes
├── paper_validation_dictamen.md              # Auditoría adversarial de Reviewer 2 y cuartiles Q1-Q3
├── references.bib                            # Archivo BibTeX limpio generado con citation-management
└── report.md                                 # Fase 4: Síntesis final formal del Estado del Arte
```

---

## 3. Preservación y No Destructividad

- **NUNCA sobreescribas ni borres ejecuciones previas** a menos que el usuario lo solicite explícitamente.
- Para comparar rendimiento, calidad o mejoras metodológicas entre diferentes runs, utiliza sufijos de versión (`_v1`, `_v2`, `_expanded`).
