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
   * *"¿Apuntas prioritariamente a una Revista Indexada (JCR/Scopus Q1, Q2 o Q3) o a una Conferencia Internacional (CORE A*, A, B)?"*

---

## Etapa 2: Búsqueda Multi-API de Prior Art y Preprints

Una vez clarificada la idea:
1. Extrae los términos técnicos precisos.
2. Consulta el corpus del estado del arte recopilado o activa la búsqueda Multi-API (OpenAlex + arXiv live feed) para no omitir preprints publicados recientemente.

---

## Etapa 3: Auditoría Profunda y Dictamen Adversarial (Reviewer 2 Suite)

El arnés ejecuta una evaluación multidimensional mediante `deep_audit.py` (o `assess_novelty.py`):
```bash
python skills/paper-validator/scripts/deep_audit.py \
    --idea "<Texto de la idea, borrador o ruta a archivo .tex/.md>" \
    --literature outputs/<propuesta>/raw/articles.json \
    --query-arxiv \
    --output outputs/<propuesta>/auditoria_profunda_dictamen.md
```

### Capacidades Evaluadas en el Dictamen:
1. **Verificación Claim-Evidence Gap (Inspirado en peer-review):**
   - Contrasta promesas ("real-time", "alta precisión en todas las clases", "operación sin sobrecalentamiento") contra los números empíricos reales (FPS reportados, tamaño de muestra $N$ por clase, temperaturas observadas).
2. **Radar de Trampas Técnicas y Desafíos Comunitarios (Inspirado en last30days):**
   - Detecta trampas comunes de la arquitectura (ambigüedad angular en cajas OBB, colapso de precisión en cuantización INT8, thermal throttling en micro-SoCs, fuga de datos temporal por splits a nivel de cuadro vs clip).
3. **Predicción Cuantitativa por Cuartiles (Q1, Q2 y Q3):**
   - **Scopus Q3 (ej. IJACSA, IJCDS):** Probabilidad alta para datasets empíricos regionales y estudios de data scaling.
   - **Scopus Q2 (ej. IEEE Access, Sensors):** Probabilidad sujeta a inclusión de baselines modernos y optimización de latencia.
   - **JCR / Scopus Q1 (ej. Scientific Reports):** Probabilidad sujeta a novedades arquitectónicas y ablaciones con significancia estadística.

---

## Etapa 4: Matriz de Delta Experimental Mínimo y Planes de Pivote

El dictamen entrega una tabla con las acciones experimentales exactas que el investigador debe ejecutar para garantizar aceptación en su cuartil objetivo:
1. **Ruta Q3 (Publicación Segura y Rápida en 4–8 semanas):** Ajustar el framing hacia monitoreo de baja tasa y documentar detalladamente el dataset regional.
2. **Ruta Q2 (Elevación de Impacto en 3–5 meses):** Añadir baselines contemporáneos (ej. YOLOv8n-OBB) y cuantización INT8 formal.
3. **Ruta Q1 (Excelencia Teórica en 6–12 meses):** Diseñar mecanismos de atención propios, verificar en benchmarks internacionales reconocidos y contrastar hipótesis con tests estadísticos.

