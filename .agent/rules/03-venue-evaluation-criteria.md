# Regla 03: Criterios de Evaluación y Prestigio de Revistas (Venues)

Esta regla documenta los sistemas métricos de indexación académica y las fórmulas de calibración utilizadas por el arnés para evaluar revistas.

---

## 1. Métricas Primarias de Prestigio

### 1.1. JCR (Journal Citation Reports - Web of Science / Clarivate)
- **Impact Factor (JIF):** Citas promedio en el año actual a artículos publicados en los dos años previos.
- **Cuartiles JCR (Q1, Q2, Q3, Q4):** Posición porcentual de la revista dentro de su categoría temática en WoS (Science Citation Index Expanded / Social Sciences Citation Index).
  - **Q1:** Top 25% de la categoría temática (Máximo prestigio académico).
  - **Q2:** Percentil 25% - 50% (Sólido estándar internacional).
  - **Q3 / Q4:** Percentil 50% - 100%.

### 1.2. Scopus / Scimago Journal Rank (SJR)
- Pondera las citas recibidas según el prestigio de las fuentes citantes (similar a un algoritmo PageRank para revistas).
- Los cuartiles Scimago SJR (Q1 a Q4) reflejan el peso temático en la base de datos de Scopus.

### 1.3. Google Scholar Metrics (H5-Index y H5-Median)
- **H5-index:** El mayor número $h$ tal que $h$ artículos publicados en los últimos 5 años completos tienen al menos $h$ citas cada uno.
- **Escala de referencia rápida para ingeniería y ciencias de la computación:**
  - $H5 \ge 150$: Conferencias y revistas monstruosas (ej. CVPR, NeurIPS, Nature, IEEE TPAMI).
  - $60 \le H5 < 150$: Revistas consolidadas de primer orden (IEEE Transactions, ACM Transactions, Information Sciences, Expert Systems with Applications).
  - $30 \le H5 < 60$: Revistas especializadas sólidas (IEEE Access, Applied Soft Computing, Sensors).
  - $15 \le H5 < 30$: Revistas emergentes o conferencias regionales (CLEI, SIMBIG).
  - $H5 < 15$: Venues en consolidación o de bajo impacto.

---

## 2. Acceso Institucional y Estrategia con Paywalls

- Si un artículo pertenece a una editorial con suscripción (IEEE Xplore, Elsevier ScienceDirect, SpringerLink, Wiley, ACM DL):
  1. El arnés extrae primero el **Título, Abstract, DOI y Métricas de Citación** a través de APIs abiertas (OpenAlex, Crossref).
  2. Si el artículo es seleccionado en el Top 5-10:
     - El arnés verifica si existe una versión libre (*Open Access / Green OA* o preprint en arXiv).
     - Si está cerrado tras *paywall*, el investigador puede usar su **acceso universitario a Scopus / Web of Science** introduciendo el DOI en la biblioteca de su institución para descargar el PDF completo sin costo.
