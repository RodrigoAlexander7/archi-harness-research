# Auditoría Profunda y Dictamen de Viabilidad de Manuscrito (Reviewer 2 Suite)

**Manuscrito / Propuesta Auditada:** `Neuro-Symbolic Generative Machine Translation for Quechua-Spanish: Deterministic Morphotactic Slot Segmentation Combined with LLM Semantic Scaffolding and Native Speaker Evaluation`
**Diagnóstico Estratégico:** `Scopus Q3 (Garantía Alta) / Scopus Q2 (Con Baselines)`

### Probabilidades Estimadas de Aceptación por Nivel:
- 🎯 **Revista Scopus Q3 (ej. IJACSA, IJCDS):** **85%** (Recomendada para publicación rápida y segura)
- 📈 **Revista Scopus Q2 (ej. IEEE Access, MDPI Sensors):** **55%** (Viable si se incorporan baselines)
- 🏛️ **Revista JCR / Scopus Q1 (ej. Scientific Reports):** **20%** (Exige innovación arquitectónica formal)

---

## 1. Verificación de Evidencia y Brecha de Promesas (Claim-Evidence Alignment)
Esta auditoría identifica discrepancias entre las afirmaciones del abstract y el respaldo experimental en los datos:

| Afirmación / Promesa Auditada | Evidencia Empírica Detectada | Nivel de Soporte | Problema de Alineamiento | Acción Correctiva Recomendada |
|---|---|:---:|---|---|

---

## 2. Obras Más Cercanas en el Estado del Arte (Prior Art & Preprints)
| # | Título | Año | Venue | Indexación | Solapamiento | Citas | Fuente | Enlace |
|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | AI-Driven Generation of Old English: A Framework for Lo... | 2026 | Big Data and Cognitive Co | No rankeado en DB local | 16.7% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.3390/bdcc10050145) |
| 2 | M-GATE: Multilingual Grammar, Accuracy in Translation, ... | 2026 | arXiv (Cornell University | No rankeado en DB local | 11.1% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.48550/arxiv.2608.03803) |
| 3 | NooJ as a Symbolic Interface: Recursive Grammars and Fo... | 2026 | ARCA (Università Ca' Fosc | No rankeado en DB local | 11.1% | 0 | OpenAlex | N/A |
| 4 | QueEn: A Large Language Model for Quechua-English Trans... | 2024 | arXiv (Cornell University | No rankeado en DB local | 11.1% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.48550/arxiv.2412.05184) |
| 5 | Foundation Models for Low-Resource Language Education (... | 2025 | Qeios | No rankeado en DB local | 5.6% | 2 | OpenAlex | [DOI/URL](https://doi.org/10.32388/iqu339) |
| 6 | Quantifying the Gaps: A Systematic Taxonomy of Bias and... | 2026 | HAL (Le Centre pour la Co | No rankeado en DB local | 5.6% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.13140/rg.2.2.27046.59201) |

---

## 3. Radar de Trampas Técnicas y Desafíos de la Comunidad (Known Pitfalls)

---

## 4. Matriz de Delta Experimental Mínimo para Asegurar Publicación

| Cuartil Objetivo | Requisitos Mínimos para Aceptación | Tiempos Típicos | Revistas Recomendadas |
|:---:|---|:---:|---|
| **Scopus Q3** | • Dataset empírico regional (Perú) bien documentado.<br>• Estudio de data scaling (1,000–2,500 imgs).<br>• Benchmark honesto en edge (explicar que 2.5–3.3 FPS es monitoreo, no video continuo). | 4 – 8 semanas | **IJACSA** (H5: 63)<br>**IJCDS** (H5: 40) |
| **Scopus Q2** | • Añadir baseline comparativo: YOLOv8n-OBB vs YOLO11n-OBB.<br>• Cuantización INT8 con `ncnn2table` alcanzando >=8 FPS.<br>• Prueba de aumentación Copy-Paste para balancear mototaxis. | 3 – 5 meses | **IEEE Access** (H5: 95)<br>**Sensors** (MDPI) |
| **JCR / Scopus Q1** | • Introducir módulo de atención liviano propio (ej. Dynamic Head o CSP-DMS).<br>• Validación en benchmark público internacional (ej. VisDrone o DOTA) además del dataset peruano.<br>• Análisis formal de gradientes y significancia estadística ($p < 0.05$). | 6 – 12 meses | **Scientific Reports** (Nature)<br>**Artificial Intelligence Review** |

---

## 5. Recomendación Ejecutiva Final
Para el estado actual del manuscrito, la ruta óptima para **garantizar una publicación indexada exitosa sin meses de retraso** es enviar a **IJACSA (Scopus Q3)** o **IJCDS (Scopus Q3)**, ajustando la redacción del abstract para reflejar que la inferencia en Raspberry Pi es para *monitoreo periódico de flujo y conteo*, no para *tracking continuo en tiempo real* a 30 FPS.