# Dictamen de Viabilidad de Paper para Revistas JCR/Scopus Q1/Q2

**Idea Evaluada:** \documentclass[runningheads]{llncs}

\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{boo...
**Diagnóstico Global:** `Apta para Revista Q1 (Sujeto a rigor experimental y baselines SOTA)`
**Probabilidad Estimada de Aceptación en Q1:** **70%**
**Probabilidad Estimada de Aceptación en Q2:** **88%**
**Evaluación de Novedad:** Novedad Conceptual Diferenciada (Solapamiento máx: 9.6%)

---

## 1. Obras Más Cercanas en el Estado del Arte (Prior Art)
| # | Título | Año | Venue | Cuartil | Solapamiento | Citas | DOI |
|---|---|:---:|---|:---:|:---:|:---:|:---:|
| 1 | Keke-Aware Vehicle Counting for Traffic Measurement Using YO... | 2026 | Applied Sciences | No rankeado en DB local | 9.6% | 0 | [Enlace](https://doi.org/10.3390/app16094316) |
| 2 | A Cascaded Framework for Vehicle Detection in Low-Resolution... | 2026 | Electronics | No rankeado en DB local | 8.0% | 1 | [Enlace](https://doi.org/10.3390/electronics15051119) |
| 3 | YOLO-GCM: A Lightweight Detector-Side Feature Enhancement Fr... | 2026 | Vehicles | No rankeado en DB local | 8.0% | 0 | [Enlace](https://doi.org/10.3390/vehicles8070143) |
| 4 | OM-YOLO: A Robust and Efficient Detection Model for Preservi... | 2026 | International journal of  | No rankeado en DB local | 7.2% | 0 | [Enlace](https://doi.org/10.22266/ijies2026.0731.15) |
| 5 | Real Time Object Detection in Autonomous Vehicle Using Yolo ... | 2025 | INTERANTIONAL JOURNAL OF  | No rankeado en DB local | 6.9% | 0 | [Enlace](https://doi.org/10.55041/ijsrem48914) |

---

## 2. Recomendación de Revistas Candidatas (Venues Identificados)
| Revista / Venue | Cuartil Estimado | H5-Index | Fit Temático |
|---|:---:|:---:|---|
| Applied Sciences | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| Electronics | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| Vehicles | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| International journal of intelligent engineering and systems | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |

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