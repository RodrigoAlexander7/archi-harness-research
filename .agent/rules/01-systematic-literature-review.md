# Regla 01: Guardrail de Estado del Arte Sistematizado (SLR)

Esta regla define los **guardrails inviolables** para cualquier tarea de revisión bibliográfica, búsqueda de estado del arte o síntesis de literatura en este repositorio.

---

## Mandatos Inviolables

1. **PROHIBIDO el uso de lenguaje natural en consultas:**
   - NUNCA introduzcas frases conversacionales o redactadas en buscadores o APIs (ej. NO buscar: *"métodos recientes para optimizar el tráfico con grafos"*).
   - Transforma SIEMPRE la intención en **términos atómicos booleanos** (ej. `traffic AND optimization AND graph`).

2. **PROHIBIDA la búsqueda superficial o no estructurada:**
   - NUNCA respondas un estado del arte con resultados de búsquedas web estándar sin metadatos cuantitativos.
   - Toda revisión debe registrar: DOI, año, citas anuales, revista/venue y estatus de acceso (Open Access vs Paywall).

3. **ACTIVACIÓN OBLIGATORIA DEL MOTOR AGÉNTICO ITERATIVO (`iterative_harvest.py`):**
   - Ante cualquier solicitud de "investiga", "revisa la literatura" o "busca el estado del arte", el agente debe ejecutar obligatoriamente el motor iterativo autónomo:
     ```bash
     uv run python skills/literature-harvester/scripts/iterative_harvest.py \
         --idea "<ruta_a_manuscrito_o_descripcion>" \
         --seed "<doi_o_url_semilla_opcional>" \
         --target-pool 20 \
         --final-top 10 \
         --output-dir outputs/<nombre_de_propuesta>
     ```
   - Si el usuario proporciona un artículo base o de referencia, debe inyectarse SIEMPRE mediante el argumento `--seed`.

4. **FILTRO MULTI-FACETAS Y PURGA DE RUIDO DINÁMICO (ANTI-DRIFT):**
   - El motor evalúa automáticamente la coexistencia de Entidad Núcleo ($E$) con Método ($M$) y Contexto ($C$).
   - Protege las raíces léxicas de la propuesta mediante lematización (`PorterStemmer`) y expulsa aplicaciones *off-target* (e.g. baches, códigos de barra, señales, telas) añadiendo sus sustantivos al filtro `NOT`.

5. **TRAZABILIDAD EN DOS NIVELES Y RANKING CALIBRADO:**
   - **Artefacto de Trazabilidad 1:** Genera obligatoriamente `outputs/<tema>/top20_candidatos_revisados.md` como evidencia del pool de 20 artículos auditados 1 a 1.
   - **Artefacto Final 2:** Aplica el ranking multicriterio (cupo máximo de 1 survey, anclaje de semilla, cuota de Joyas Emergentes 2025/2026 y bonificación empírica) para generar `outputs/<tema>/summary_table.md` (Top 10 ordenado) y `outputs/<tema>/references.bib` verificado vía Crossref.
