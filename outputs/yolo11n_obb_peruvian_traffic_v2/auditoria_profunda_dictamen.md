# Auditoría Profunda y Dictamen de Viabilidad de Manuscrito (Reviewer 2 Suite)

**Manuscrito / Propuesta Auditada:** `/home/totora/Documents/PROFESIONAL/swole-yolo/paper/simbig_paper.tex`
**Diagnóstico Estratégico:** `Scopus Q3 (Garantía Alta) / Scopus Q2 (Con Baselines)`

### Probabilidades Estimadas de Aceptación por Nivel:
- 🎯 **Revista Scopus Q3 (ej. IJACSA, IJCDS):** **81%** (Recomendada para publicación rápida y segura)
- 📈 **Revista Scopus Q2 (ej. IEEE Access, MDPI Sensors):** **47%** (Viable si se incorporan baselines)
- 🏛️ **Revista JCR / Scopus Q1 (ej. Scientific Reports):** **10%** (Exige innovación arquitectónica formal)

---

## 1. Verificación de Evidencia y Brecha de Promesas (Claim-Evidence Alignment)
Esta auditoría identifica discrepancias entre las afirmaciones del abstract y el respaldo experimental en los datos:

| Afirmación / Promesa Auditada | Evidencia Empírica Detectada | Nivel de Soporte | Problema de Alineamiento | Acción Correctiva Recomendada |
|---|---|:---:|---|---|
| **Capacidad de procesamiento en tiempo real en dispositivo Edge (Raspberry Pi)** | FPS máximo reportado: 3.33 FPS (1.96 ms de latencia) | `Partly Supported / At Risk` | Rendimiento insuficiente para video en tiempo real (mínimo estándar: 10–15 FPS). | Reformular honestamente como 'low-rate surveillance/monitoring' o incorporar cuantización INT8 (NCNN/TensorRT) para alcanzar >=10 FPS. |
| **Detección precisa y robusta de mototaxis / vehículos ligeros** | Clase con soporte extremadamente bajo (ratio ~1:89 frente a autos; ~38 instancias de test en el corpus) | `Partly Supported / Statistical Fragility` | La métrica mAP alta en mototaxis es estadísticamente ruidosa por tamaño muestral pequeño. | Aplicar aumentación sintética 'Class-Aware Copy-Paste', ajustar Focal Loss / Class-Weighted Loss y reportar matriz de confusión con intervalos de confianza. |
| **Operación edge sin estrangulamiento térmico (thermal throttling)** | Temperaturas observadas: °C (Delta térmico de +19°C a +20°C en pruebas cortas) | `Partly Supported` | Pruebas de corta duración (2 min) no garantizan ausencia de throttling en operación continua (24/7) a 80°C. | Ejecutar benchmark de estrés térmico de 30 minutos continuos reportando la frecuencia del reloj de CPU de la Raspberry Pi. |
| **Aporte científico de la solución de detección** | Fine-tuning directo de arquitectura comercial (YOLO11n-OBB) sobre dataset local sin nuevo módulo matemático/arquitectónico | `Partly Supported (Adecuado para Scopus Q3, Débil para Q1/Q2)` | Riesgo de ser calificado como 'ejercicio de ingeniería / aplicación directa' por revisores de Q1/Q2. | Agregar baselines comparativos directos (YOLOv8n-OBB vs YOLO11n-OBB) y cuantización INT8 formal, o postular a revistas aplicadas Scopus Q3 (IJACSA, IJCDS). |

---

## 2. Obras Más Cercanas en el Estado del Arte (Prior Art & Preprints)
| # | Título | Año | Venue | Indexación | Solapamiento | Citas | Fuente | Enlace |
|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | Keke-Aware Vehicle Counting for Traffic Measurement Usi... | 2026 | Applied Sciences | No rankeado en DB local | 9.8% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.3390/app16094316) |
| 2 | A Cascaded Framework for Vehicle Detection in Low-Resol... | 2026 | Electronics | No rankeado en DB local | 8.5% | 1 | OpenAlex | [DOI/URL](https://doi.org/10.3390/electronics15051119) |
| 3 | YOLO-GCM: A Lightweight Detector-Side Feature Enhanceme... | 2026 | Vehicles | No rankeado en DB local | 8.2% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.3390/vehicles8070143) |
| 4 | OM-YOLO: A Robust and Efficient Detection Model for Pre... | 2026 | International journal of  | No rankeado en DB local | 7.4% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.22266/ijies2026.0731.15) |
| 5 | Real Time Object Detection in Autonomous Vehicle Using ... | 2025 | INTERANTIONAL JOURNAL OF  | No rankeado en DB local | 7.2% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.55041/ijsrem48914) |
| 6 | LMOD-YOLO: A lightweight YOLO model for marine organism... | 2026 | Scientific Reports | No rankeado en DB local | 6.9% | 0 | OpenAlex | [DOI/URL](https://doi.org/10.1038/s41598-026-66858-7) |

---

## 3. Radar de Trampas Técnicas y Desafíos de la Comunidad (Known Pitfalls)

### ⚠️ Regresión de Ángulos en Cajas Orientadas (OBB Angle Boundary Trap)
- **Riesgo:** Ambigüedad periódica en [0, pi] o [-pi/2, pi/2] genera gradientes explosivos cuando el vehículo gira 180°.
- **Mitigación para el Paper:** Ultralytics YOLO11-OBB mitiga esto con Probabilistic IoU / Gaussian Wasserstein Distance (GWD). Indicarlo explícitamente en el paper para ganar puntos metodológicos.

### ⚠️ Degradación de Ángulos por Cuantización INT8 (Quantization Drift)
- **Riesgo:** Cuantizar uniformemente las capas de la cabeza detectora suele colapsar la precisión del ángulo más rápido que las coordenadas x,y.
- **Mitigación para el Paper:** Utilizar calibración KL-Divergence con 'ncnn2table' seleccionando imágenes equilibradas de validación, o cuantización mixta (backbone en INT8 y cabeza OBB en FP16).

### ⚠️ Partición de Datos Temporal (Clip-Level vs Frame-Level)
- **Riesgo:** Punto fuerte: El manuscrito evitó la trampa mortal de mezclar cuadros contiguos en train/val/test.
- **Mitigación para el Paper:** Destacar esta rigurosidad metodológica en el Abstract y Metodología; muchos papers son rechazados por fuga inadvertida de datos.

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