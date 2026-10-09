---
name: paper-validator
description: Evalúa ideas de papers de forma adversarial, detecta solapamientos con prior art y estima probabilidades de publicación en revistas indexadas JCR/Scopus Q1/Q2 formulando pivotes estratégicos.
---

# Paper Validator Skill

Esta habilidad somete cualquier propuesta de investigación o idea de paper al juicio de un **"Reviewer 2 Adversarial"**:

1. **Cálculo de Solapamiento con Prior Art:** Compara la idea con los artículos del estado del arte recopilados.
2. **Diagnóstico de Delta Real:** Identifica si la idea es una mera combinación trivial o si posee una novedad conceptual publicable.
3. **Probabilidad de Aceptación:** Estima probabilidades porcentuales de aceptación en revistas Q1 vs. Q2.
4. **Pivotes de Mejora:** Proporciona 3 alternativas concretas para elevar un paper de nivel Q3/rechazo hacia un estándar publicable en Q1.

## Ejemplo de Ejecución

```bash
python skills/paper-validator/scripts/assess_novelty.py \
    --idea "Proponemos un algoritmo híbrido de optimización cuántica aproximada (QAOA) para problemas de ruteo en grafos dinámicos utilizando descomposición espectral" \
    --literature investigations/<tema>/raw/articles.json \
    --output investigations/<tema>/paper_validation_dictamen.md
```
