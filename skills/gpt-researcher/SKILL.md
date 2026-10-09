---
name: gpt-researcher
description: Agente de investigación web autónomo basado en gpt-researcher (~30k estrellas). Rastrea múltiples fuentes en Internet (blogs, documentación técnica, noticias, páginas corporativas), filtra sesgos y genera reportes extensos estructurados con citas.
---

# GPT Researcher Skill

Esta habilidad dota al arnés de un **motor de investigación web profunda** para temas que van más allá de artículos científicos de revistas (documentación oficial de librerías, casos de uso en la industria, reportes de empresas, noticias tecnológicas y benchmarks comunitarios).

## Características

* **Búsqueda autónoma multietapa:** Planifica consultas, recopila más de 20 fuentes web, filtra información irrelevante y sintetiza.
* **Citas web y enlaces directos:** Todas las afirmaciones incluyen referencias y URLs de origen.
* **Soporte de motores de búsqueda:** Compatible con DuckDuckGo (gratuito) y Tavily.

## Uso Rápido

```bash
python skills/gpt-researcher/scripts/run_research.py \
    --query "YOLO11 performance benchmarks on Raspberry Pi ARM devices NCNN vs ONNX" \
    --type research_report \
    --output investigations/yolo_benchmarks/web_report.md
```
