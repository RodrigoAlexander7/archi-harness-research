# Dictamen de Viabilidad de Paper para Revistas JCR/Scopus Q1/Q2

**Idea Evaluada:** Fine-Tuning YOLO11n-OBB for Oriented Vehicle Detection in Peruvian Traffic Scenes: Data Scaling and Edge Benchmarking on...
**Diagnóstico Global:** `Viable para Revista Q2 / Requiere fortalecer baselines para Q1`
**Probabilidad Estimada de Aceptación en Q1:** **45%**
**Probabilidad Estimada de Aceptación en Q2:** **75%**
**Evaluación de Novedad:** Novedad Incremental Moderada (Solapamiento máx: 64.3%)

---

## 1. Obras Más Cercanas en el Estado del Arte (Prior Art)
| # | Título | Año | Venue | Cuartil | Solapamiento | Citas | DOI |
|---|---|:---:|---|:---:|:---:|:---:|:---:|
| 1 | HBB2OBB: Horizontal to Oriented Bounding Box Conversion and ... | 2026 | Zenodo (CERN European Org | No rankeado en DB local | 64.3% | 0 | [Enlace](https://doi.org/10.5281/zenodo.22817652) |
| 2 | HBB2OBB: Horizontal to Oriented Bounding Box Conversion and ... | 2026 | Zenodo (CERN European Org | No rankeado en DB local | 64.3% | 0 | [Enlace](https://doi.org/10.5281/zenodo.22714493) |
| 3 | HBB2OBB: Horizontal to Oriented Bounding Box Conversion and ... | 2026 | Zenodo (CERN European Org | No rankeado en DB local | 64.3% | 0 | [Enlace](https://doi.org/10.5281/zenodo.22774765) |
| 4 | HBB2OBB: Horizontal to Oriented Bounding Box Conversion and ... | 2026 | Zenodo (CERN European Org | No rankeado en DB local | 57.1% | 0 | [Enlace](https://doi.org/10.5281/zenodo.22261356) |
| 5 | A Cascaded Framework for Vehicle Detection in Low-Resolution... | 2026 | Electronics | No rankeado en DB local | 42.9% | 1 | [Enlace](https://doi.org/10.3390/electronics15051119) |

---

## 2. Recomendación de Revistas Candidatas (Venues Identificados)
| Revista / Venue | Cuartil Estimado | H5-Index | Fit Temático |
|---|:---:|:---:|---|
| Zenodo (CERN European Organization for Nuclear Research) | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| Electronics | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |

---

## 3. Plan de Pivote Estratégico para Asegurar Publicación en Q1

### Opción 1: Pivote de Baselines y Complejidad
- **Acción:** No comparar únicamente contra algoritmos canónicos clásicos. Los artículos del prior art están usando benchmarks recientes.
- **Exigencia Q1:** Incluir al menos 3 baselines del periodo 2024–2026 encontrados en esta búsqueda.

### Opción 2: Pivote de Estudio de Ablación y Mecanismos
- **Acción:** Aislar cada hiperparámetro o componente de la solución.
- **Exigencia Q1:** Presentar tablas de ablación que demuestren que cada módulo aporta una ganancia estadísticamente significativa (con p-values < 0.05).

### Opción 3: Pivote de Eficiencia / Pareto-Optimality
- **Acción:** Si no es posible superar al SOTA en métricas de exactitud absoluta, medir latencia, memoria o costo energético.
- **Exigencia Q1:** Posicionar el aporte en la frontera de Pareto: igual rendimiento con una fracción del costo computacional.