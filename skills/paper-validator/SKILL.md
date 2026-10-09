---
name: paper-validator
description: Validador y auditor adversarial de ideas de papers. Realiza una entrevista técnica exhaustiva para comprender a fondo la propuesta, detecta solapamiento con el estado del arte (prior art), clasifica su potencial en cuartiles de revistas (JCR/Scopus Q1-Q4) o conferencias (CORE A*-B), y formula pivotes estratégicos para maximizar su aceptación.
---

# Paper Validator Skill (Auditor Adversarial de Ideas)

Esta habilidad actúa como un **Comité de Admisión y Revisor 2 Implacable** (*Reviewer 2 Adversarial*). Su propósito es evitar que un investigador invierta meses en una investigación que será rechazada por falta de novedad, baselines obsoletos o diseño experimental débil, guiándolo hacia un nivel publicable en **revistas JCR/Scopus Q1 o Q2**.

---

## Flujo de Trabajo en 4 Etapas

```mermaid
flowchart TD
    Idea[Propuesta o Hipótesis Inicial] --> Stage1[Etapa 1: Entrevista de Admisión Técnica]
    Stage1 --> UserAnswers[Respuestas y Aclaraciones del Investigador]
    UserAnswers --> Stage2[Etapa 2: Búsqueda Semántica de Prior Art en OpenAlex]
    Stage2 --> Stage3[Etapa 3: Dictamen Adversarial Implacable y Clasificación de Cuartil]
    Stage3 --> Stage4[Etapa 4: Plan de Pivote Estratégico para Elevar a Q1]
```

---

## Etapa 1: La Entrevista de Admisión Crítica (*Grill the Idea*)

**Regla de Oro:** NUNCA emitas un veredicto apresurado ante una idea de una sola línea. Una idea como *"quiero usar transformers para predecir fallas en turbinas"* es demasiado ambigua para saber si es un trabajo Q1 o un rechazo inmediato.

Al recibir una idea, analiza qué información falta y formula **entre 3 y 5 preguntas incisivas y contextualizadas** seleccionadas de estas 6 dimensiones críticas:

1. **El Delta Metodológico Real:**
   * *"¿Cuál es la modificación técnica específica? ¿Estás diseñando una nueva arquitectura, modificando la función de pérdida/atención, o aplicando una librería estándar tal cual?"*
2. **Datasets y Disponibilidad:**
   * *"¿Qué datasets utilizarás para validar la propuesta? ¿Son benchmarks públicos estándar de la comunidad o datos propios/privados? ¿El código y datos serán de acceso abierto?"*
3. **Baselines del SOTA Reciente (2024–2026):**
   * *"¿Contra qué modelos o algoritmos publicados en los últimos 2 años te vas a comparar? (Los revisores de Q1 rechazan automáticamente artículos que solo comparan contra modelos clásicos de 2018–2022)."*
4. **Hipótesis Mecanicista / Explicativa:**
   * *"¿Por qué razón teórica o estructural debería este enfoque superar al estado del arte en este problema específico?"*
5. **Ablaciones y Validación Estadística:**
   * *"¿Qué estudios de ablación se planifican para demostrar qué componente aporta la ganancia? ¿Se harán pruebas de significancia (Wilcoxon / t-test con p < 0.05) sobre múltiples semillas?"*
6. **Objetivo de Publicación:**
   * *"¿Apuntas prioritariamente a una Revista Indexada (JCR/Scopus Q1 o Q2) o a una Conferencia Internacional (CORE A*, A, B)?"*

---

## Etapa 2: Búsqueda de Solapamiento con el Estado del Arte (*Prior Art*)

Una vez clarificada la idea:
1. Extrae los términos técnicos precisos.
2. Consulta el corpus del estado del arte recopilado o ejecuta `search_openalex.py` para verificar si existen trabajos con títulos o abstracts similares en los últimos 24 meses.
3. Ejecuta la auditoría semántica:
```bash
python skills/paper-validator/scripts/assess_novelty.py \
    --idea "<Descripción detallada refinada tras la entrevista>" \
    --literature investigations/<tema>/raw/articles.json \
    --output investigations/<tema>/paper_validation_dictamen.md
```

---

## Etapa 3: Dictamen Transparente y Clasificación de Cuartil

El dictamen generado debe ser **frontal, transparente y sin filtros condescendientes**:

### Clasificación Categórica:
* **Apta para Revista Q1 / Conferencia CORE A* (Probabilidad > 70%):** Novedad conceptual clara, evaluación en benchmarks estándar reconocidos, ablaciones completas y justificación matemática/estructural.
* **Apta para Revista Q2 / Conferencia CORE A (Probabilidad > 70%):** Aplicación rigurosa a problemas complejos con novedad incremental o en nicho específico.
* **Nivel Q3 - Q4 / CORE B (Requiere Pivote Urgente):** Aplicación directa de técnicas conocidas sin modificación metodológica relevante o con datasets muy pequeños.
* **Desk Reject Inmediato (Riesgo Crítico):** Idea ya resuelta en la literatura reciente (solapamiento > 60%), o carente de novedad técnica ("unir A + B sin adaptación").

---

## Etapa 4: Plan de Pivote Estratégico (*Level-Up to Q1*)

Si la idea cae en Q3 o tiene alto riesgo de rechazo, formula **3 alternativas de pivote concretas**:

1. **Pivote de Escala y Benchmarks:** Qué datasets estándar más exigentes o qué baselines de 2024–2026 elevarían el trabajo a Q1.
2. **Pivote Teórico o Mecanicista:** Qué demostración formal, análisis de complejidad computacional o estudio de interpretabilidad puede añadirse.
3. **Pivote de Frontera de Pareto / Eficiencia:** Cómo enfocar la contribución hacia la optimización de latencia, memoria o costo energético si no es posible batir al SOTA en métricas absolutas.
