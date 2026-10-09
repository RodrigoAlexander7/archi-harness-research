# Rúbrica de Clasificación de Venues y Cuestionario de Admisión (Intake Rubric)

Esta rúbrica estandariza los criterios que separan un paper rechazable de uno publicable en revistas **JCR/Scopus Q1/Q2** o conferencias **CORE A*/A/B**.

---

## 1. Cuestionario de Entrevista de Admisión (Las 6 Preguntas Críticas)

Cuando el investigador propone una idea embrionaria, el agente debe formular estas preguntas adaptándolas al contexto técnico:

1. **Delta Metodológico Real:**
   * *Pregunta:* "¿Cuál es la contribución técnica exacta? ¿Es un nuevo algoritmo, una modificación matemática/arquitectónica de una técnica existente, o es la aplicación directa de una librería/modelo estándar a un caso de estudio?"
   * *Criterio de Alerta:* Si la respuesta es *"apliqué el modelo estándar X al dataset Y"*, es un **Desk Reject casi seguro en Q1** (salvo en revistas de aplicación de nicho Q3/Q4).

2. **Naturaleza y Disponibilidad de Datos:**
   * *Pregunta:* "¿Qué datasets o bancos de prueba se utilizarán? ¿Son datasets públicos estándar del área o datos privados/propios? Si son propios, ¿se publicarán en acceso abierto para garantizar reproducibilidad?"
   * *Criterio de Alerta:* Datasets propios pequeños sin justificación o sin disponibilidad de código son penalizados severamente en Q1.

3. **Baselines del Estado del Arte Reciente:**
   * *Pregunta:* "¿Contra qué modelos o algoritmos de referencia (2024–2026) se comparará el rendimiento? ¿Se incluirá el SOTA actual o solo algoritmos tradicionales/canónicos?"
   * *Criterio de Alerta:* Comparar contra baselines de hace 5 o 10 años garantiza una crítica destructiva de los revisores.

4. **Falsabilidad y Mecanismo Explicativo:**
   * *Pregunta:* "¿Cuál es la hipótesis mecanicista? Es decir, ¿por qué razón teórica o computacional se espera que este enfoque supere a las soluciones existentes?"
   * *Criterio de Alerta:* "Para ver qué pasa" o "porque nadie lo ha probado antes" no son argumentos válidos para Q1.

5. **Ablaciones y Validación Estadística:**
   * *Pregunta:* "¿Qué estudios de ablación se planifican para demostrar qué módulo específico aporta la ganancia? ¿Se realizarán pruebas de significancia estadística (e.g. Wilcoxon, t-test, intervalos de confianza) con múltiples semillas?"
   * *Criterio de Alerta:* Reportar solo métricas puntuales (ej. solo accuracy) sin varianza ni significancia.

6. **Target y Expectativa de Publicación:**
   * *Pregunta:* "¿El objetivo primario es una Revista Indexada (JCR Q1, Q2) o una Conferencia Internacional (CORE A*, A, B)? ¿Qué horizonte temporal de publicación se contempla?"

---

## 2. Matriz de Clasificación de Venues

| Nivel / Cuartil | Características Requeridas | Ejemplos Representativos |
| :--- | :--- | :--- |
| **Revista JCR / Scopus Q1** | Novedad metodológica genuina, evaluación en múltiples benchmarks estándar, comparación contra 4+ baselines recientes (últimos 2-3 años), ablaciones completas y pruebas estadísticas. | IEEE Transactions, Nature Machine Intelligence, Expert Systems with Applications, Information Sciences, ACM Computing Surveys. |
| **Revista JCR / Scopus Q2** | Metodología sólida y rigurosa, aplicación profunda a un problema complejo del mundo real, comparación con el SOTA suficiente, aunque la novedad algorítmica sea moderada/incremental. | IEEE Access, Neurocomputing, Sensors, Applied Soft Computing, Computer Communications. |
| **Revista JCR / Scopus Q3 - Q4** | Aplicaciones directas de técnicas conocidas a casos de estudio locales o con datasets limitados sin aportes teóricos novedosos. | IJACSA, revistas locales o temáticas de menor factor de impacto. |
| **Conferencia CORE A* / A** | Novedad de alto impacto, conceptos disruptivos, relevancia inmediata para la comunidad, código abierto con reproducibilidad inmediata. | NeurIPS, ICML, ICLR, CVPR, ACL, KDD, IEEE INFOCOM. |
| **Conferencia CORE B / C** | Trabajos preliminares sólidos, ideas con evaluación preliminar prometedora o estudios de caso específicos. | Simposios regionales, CLEI, conferencias de sociedad temática. |
