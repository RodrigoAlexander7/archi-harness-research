# Dictamen de Viabilidad de Paper para Revistas JCR/Scopus Q1/Q2

**Idea Evaluada:** Proponemos un algoritmo híbrido de enrutamiento cuántico en grafos con redes neuronales de atención para problemas dinám...
**Diagnóstico Global:** `Requiere Pivote Urgente (Riesgo de Desk Reject por falta de novedad)`
**Probabilidad Estimada de Aceptación en Q1:** **20%**
**Probabilidad Estimada de Aceptación en Q2:** **45%**
**Evaluación de Novedad:** Alto Riesgo de Solapamiento Crítico (Novedad Comprometida) (Solapamiento máx: 72.7%)

---

## 1. Obras Más Cercanas en el Estado del Arte (Prior Art)
| # | Título | Año | Venue | Cuartil | Solapamiento | Citas | DOI |
|---|---|:---:|---|:---:|:---:|:---:|:---:|
| 1 | Vehicle Routing Problems via Quantum Graph Attention Network... | 2025 | arXiv (Cornell University | No rankeado en DB local | 72.7% | 0 | N/A |
| 2 | Vehicle Routing Problems via Quantum Graph Attention Network... | 2025 | arXiv (Cornell University | No rankeado en DB local | 72.7% | 0 | [Enlace](https://doi.org/10.48550/arxiv.2511.15175) |
| 3 | A Hybrid Quantum-Meta Reinforcement Learning and Graph Atten... | 2026 | IEEE Access | No rankeado en DB local | 63.6% | 2 | [Enlace](https://doi.org/10.1109/access.2026.3664972) |
| 4 | Vehicle Routing Problems via Quantum Graph Attention Network... | 2026 | Communications in compute | No rankeado en DB local | 54.5% | 1 | [Enlace](https://doi.org/10.1007/978-981-92-2584-2_44) |
| 5 | GNN-Guided Graph Coarsening and Adaptive QUBO Penalties for ... | 2026 | arXiv (Cornell University | No rankeado en DB local | 54.5% | 0 | [Enlace](https://doi.org/10.48550/arxiv.2609.04593) |

---

## 2. Recomendación de Revistas Candidatas (Venues Identificados)
| Revista / Venue | Cuartil Estimado | H5-Index | Fit Temático |
|---|:---:|:---:|---|
| IEEE Access | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |
| Communications in computer and information science | No rankeado en DB local | 25 | Alto (Publica artículos similares del SOTA) |

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