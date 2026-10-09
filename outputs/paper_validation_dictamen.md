# Dictamen de Viabilidad de Paper para Revistas JCR/Scopus Q1/Q2

**Idea Evaluada:** \documentclass[runningheads]{llncs}

\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{boo...
**Diagnóstico Global:** `Apta para Revista Q1 (Sujeto a rigor experimental y baselines SOTA)`
**Probabilidad Estimada de Aceptación en Q1:** **70%**
**Probabilidad Estimada de Aceptación en Q2:** **88%**
**Evaluación de Novedad:** Novedad Conceptual Diferenciada (Solapamiento máx: 9.3%)

---

## 1. Obras Más Cercanas en el Estado del Arte (Prior Art)
| # | Título | Año | Venue | Cuartil | Solapamiento | Citas | DOI |
|---|---|:---:|---|:---:|:---:|:---:|:---:|
| 1 | A Lightweight End-to-End Framework for Real-Time Vehicle-Eje... | 2026 | Sensors | Q2 | 9.3% | 0 | [Enlace](https://doi.org/10.3390/s26144386) |
| 2 | An Automated Detection Method for Motor Vehicles Encroaching... | 2026 | Sensors | Q2 | 8.9% | 0 | [Enlace](https://doi.org/10.3390/s26072027) |
| 3 | Multi-View Vehicle Detection and Tracking for Smart City Tra... | 2026 | EAI Endorsed Transactions | No rankeado en DB local | 8.3% | 0 | [Enlace](https://doi.org/10.4108/eetiot.12412) |
| 4 | Real-Time Vehicle Detection and Location Tracking for Milita... | 2026 | ITEGAM- Journal of Engine | No rankeado en DB local | 8.3% | 0 | [Enlace](https://doi.org/10.5935/jetia.v12i59.3386) |
| 5 | Tunnel Traffic Enforcement Using Visual Computing and Field-... | 2025 | IEEE Eurasia Conference o | No rankeado en DB local | 8.1% | 0 | [Enlace](https://doi.org/10.3390/engproc2025092030) |

---

## 2. Recomendación de Revistas Candidatas (Venues Identificados)
| Revista / Venue | Cuartil Estimado | H5-Index | Fit Temático |
|---|:---:|:---:|---|
| Sensors | Q2 | 120 | Alto (Publica artículos similares del SOTA) |
| EAI Endorsed Transactions on Internet of Things | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| ITEGAM- Journal of Engineering and Technology for Industrial Applications (ITEGAM-JETIA) | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| IEEE Eurasia Conference on IOT, Communication and Engineering (ECICE) | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |

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