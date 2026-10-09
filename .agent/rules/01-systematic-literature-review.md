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

3. **ACTIVACIÓN OBLIGATORIA DE LA SKILL `systematic-slr`:**
   - Ante cualquier solicitud de revisión de literatura, activa inmediatamente el flujo de la skill `skills/systematic-slr/SKILL.md`.
   - Sigue sus 5 fases operativas y respeta los dos puntos de control (*Checkpoints*) con el investigador (confirmación de términos atómicos y de joyas emergentes).

4. **FILTRO TEMPORAL Y EXCLUSIONES (`NOT`):**
   - La ventana base es de **3 años** (ampliable a 5 únicamente si hay escasez comprobada de artículos).
   - Siempre define términos de exclusión negativa para purgar disciplinas adyacentes no deseadas.

5. **CRITERIO DE RANKING Q1/Q2 Y JOYAS EMERGENTES:**
   - Los artículos no se ordenan únicamente por número bruto de citas. Se ordenan ponderando la tasa de citas por año con el **H5-index** del journal y el cuartil JCR/SJR.
   - Es obligatorio reservar cupos para **Joyas Emergentes** de 2025/2026 (artículos con pocas o cero citas pero que representan el estado del arte metodológico más reciente).
