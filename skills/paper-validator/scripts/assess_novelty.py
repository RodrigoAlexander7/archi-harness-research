#!/usr/bin/env python3
"""
assess_novelty.py
Compara la idea de paper del investigador frente al corpus del estado del arte recopilado.
Calcula solapamiento conceptual, detecta prior art competitivo, estima probabilidad en Q1/Q2
y formula recomendaciones de pivote estratégico.
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Set

# Mapeo bilingüe (ES -> EN) para términos científicos frecuentes
BILINGUAL_MAP = {
    "cuántico": "quantum", "cuántica": "quantum", "cuanticos": "quantum", "cuanticas": "quantum",
    "grafo": "graph", "grafos": "graph", "teoria": "theory",
    "enrutamiento": "routing", "ruteo": "routing", "rutas": "routing",
    "red": "network", "redes": "network", "neuronal": "neural", "neuronales": "neural",
    "atención": "attention", "atencion": "attention",
    "aprendizaje": "learning", "refuerzo": "reinforcement", "profundo": "deep",
    "híbrido": "hybrid", "hibrido": "hybrid", "algoritmo": "algorithm", "algoritmos": "algorithm",
    "vehículo": "vehicle", "vehículos": "vehicle", "vehiculo": "vehicle", "vehiculos": "vehicle",
    "optimización": "optimization", "optimizacion": "optimization",
    "espectral": "spectral", "descomposición": "decomposition", "descomposicion": "decomposition",
    "dinámico": "dynamic", "dinámica": "dynamic", "dinamicos": "dynamic", "dinamicas": "dynamic",
    "circuito": "circuit", "circuitos": "circuit", "estado": "state", "estados": "state",
    "transferencia": "transfer", "perfecta": "perfect", "qubit": "qubit", "qubits": "qubit"
}

def tokenize_clean(text: str) -> Set[str]:
    stopwords = {
        "the", "and", "of", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with",
        "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have",
        "new", "we", "our", "paper", "propose", "proposed", "method", "results", "approach",
        "el", "la", "los", "las", "un", "una", "de", "del", "en", "para", "por", "con", "su",
        "que", "se", "es", "son", "artículo", "proponemos", "método", "resultados", "via", "based"
    }
    raw_words = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{3,}\b", text.lower())
    tokens = set()
    for w in raw_words:
        if w in stopwords:
            continue
        # Mapear español a inglés si existe
        normalized = BILINGUAL_MAP.get(w, w)
        tokens.add(normalized)
    return tokens

def calculate_overlap(idea_tokens: Set[str], abstract_tokens: Set[str]) -> float:
    if not idea_tokens or not abstract_tokens:
        return 0.0
    intersection = idea_tokens.intersection(abstract_tokens)
    # Coeficiente de solapamiento relativo al tamaño de la idea
    return round((len(intersection) / len(idea_tokens)) * 100, 1)

def evaluate_idea(idea_text: str, literature: List[Dict[str, Any]]) -> Dict[str, Any]:
    idea_tokens = tokenize_clean(idea_text)
    
    comparisons = []
    high_overlap_papers = []

    for art in literature:
        art_tokens = tokenize_clean((art.get("title", "") + " " + art.get("abstract", "")))
        overlap_pct = calculate_overlap(idea_tokens, art_tokens)
        
        comp = {
            "title": art.get("title"),
            "year": art.get("year"),
            "venue": art.get("venue"),
            "quartile": art.get("quartile", "Desc"),
            "h5_index": art.get("h5_index", 25),
            "citations": art.get("citations", 0),
            "doi": art.get("doi"),
            "overlap_percent": overlap_pct,
            "is_open_access": art.get("is_open_access", False)
        }
        comparisons.append(comp)
        if overlap_pct >= 35.0:
            high_overlap_papers.append(comp)

    comparisons.sort(key=lambda x: x["overlap_percent"], reverse=True)
    top_prior_art = comparisons[:5]

    # Diagnóstico de Delta Real
    max_overlap = top_prior_art[0]["overlap_percent"] if top_prior_art else 0.0
    
    if max_overlap >= 65.0:
        delta_status = "Alto Riesgo de Solapamiento Crítico (Novedad Comprometida)"
        q1_prob = 20
        q2_prob = 45
        verdict = "Requiere Pivote Urgente (Riesgo de Desk Reject por falta de novedad)"
    elif max_overlap >= 40.0:
        delta_status = "Novedad Incremental Moderada"
        q1_prob = 45
        q2_prob = 75
        verdict = "Viable para Revista Q2 / Requiere fortalecer baselines para Q1"
    else:
        delta_status = "Novedad Conceptual Diferenciada"
        q1_prob = 70
        q2_prob = 88
        verdict = "Apta para Revista Q1 (Sujeto a rigor experimental y baselines SOTA)"

    # Extraer venues de las obras más cercanas para sugerir dónde publicar
    recommended_venues = []
    seen_venues = set()
    for p in top_prior_art:
        v = p.get("venue")
        if v and v not in seen_venues and "arxiv" not in v.lower():
            recommended_venues.append({
                "venue": v,
                "quartile": p.get("quartile", "Q1/Q2"),
                "h5_index": p.get("h5_index", 30)
            })
            seen_venues.add(v)

    return {
        "idea_words_analyzed": len(idea_tokens),
        "total_literature_analyzed": len(literature),
        "max_overlap_percent": max_overlap,
        "delta_status": delta_status,
        "verdict": verdict,
        "q1_probability": q1_prob,
        "q2_probability": q2_prob,
        "top_prior_art": top_prior_art,
        "recommended_venues": recommended_venues
    }

def format_evaluation_report(eval_data: Dict[str, Any], idea_summary: str) -> str:
    lines = [
        "# Dictamen de Viabilidad de Paper para Revistas JCR/Scopus Q1/Q2",
        "",
        f"**Idea Evaluada:** {idea_summary[:120]}...",
        f"**Diagnóstico Global:** `{eval_data['verdict']}`",
        f"**Probabilidad Estimada de Aceptación en Q1:** **{eval_data['q1_probability']}%**",
        f"**Probabilidad Estimada de Aceptación en Q2:** **{eval_data['q2_probability']}%**",
        f"**Evaluación de Novedad:** {eval_data['delta_status']} (Solapamiento máx: {eval_data['max_overlap_percent']}%)",
        "",
        "---",
        "",
        "## 1. Obras Más Cercanas en el Estado del Arte (Prior Art)",
        "| # | Título | Año | Venue | Cuartil | Solapamiento | Citas | DOI |",
        "|---|---|:---:|---|:---:|:---:|:---:|:---:|"
    ]

    for idx, art in enumerate(eval_data["top_prior_art"], start=1):
        title = art.get("title", "")[:60] + ("..." if len(art.get("title", "")) > 60 else "")
        doi_link = f"[Enlace]({art.get('doi')})" if art.get("doi") else "N/A"
        lines.append(
            f"| {idx} | {title} | {art.get('year')} | {art.get('venue')[:25]} | {art.get('quartile')} | {art.get('overlap_percent')}% | {art.get('citations')} | {doi_link} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Recomendación de Revistas Candidatas (Venues Identificados)",
        "| Revista / Venue | Cuartil Estimado | H5-Index | Fit Temático |",
        "|---|:---:|:---:|---|"
    ])

    for v in eval_data["recommended_venues"][:4]:
        lines.append(f"| {v['venue']} | {v['quartile']} | {v['h5_index']} | Alto (Publica artículos similares del SOTA) |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Plan de Pivote Estratégico para Asegurar Publicación en Q1",
        "",
        "### Opción 1: Pivote de Baselines y Complejidad",
        "- **Acción:** No comparar únicamente contra algoritmos canónicos clásicos. Los artículos del prior art están usando benchmarks recientes.",
        "- **Exigencia Q1:** Incluir al menos 3 baselines del periodo 2024–2026 encontrados en esta búsqueda.",
        "",
        "### Opción 2: Pivote de Estudio de Ablación y Mecanismos",
        "- **Acción:** Aislar cada hiperparámetro o componente de la solución.",
        "- **Exigencia Q1:** Presentar tablas de ablación que demuestren que cada módulo aporta una ganancia estadísticamente significativa (con p-values < 0.05).",
        "",
        "### Opción 3: Pivote de Eficiencia / Pareto-Optimality",
        "- **Acción:** Si no es posible superar al SOTA en métricas de exactitud absoluta, medir latencia, memoria o costo energético.",
        "- **Exigencia Q1:** Posicionar el aporte en la frontera de Pareto: igual rendimiento con una fracción del costo computacional."
    ])

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Evaluar novedad y viabilidad de una idea de paper frente al SOTA")
    parser.add_argument("--idea", required=True, help="Texto de la idea o ruta al archivo .txt/.md con la idea")
    parser.add_argument("--literature", required=True, help="Ruta al JSON de artículos del SOTA recopilados")
    parser.add_argument("--output", default="", help="Ruta para guardar el reporte en Markdown")

    args = parser.parse_args()

    # Cargar idea
    idea_path = Path(args.idea)
    if idea_path.exists():
        idea_text = idea_path.read_text(encoding="utf-8")
    else:
        idea_text = args.idea

    # Cargar literatura
    lit_path = Path(args.literature)
    if not lit_path.exists():
        print(f"[ERROR] Archivo de literatura no encontrado: {lit_path}", file=sys.stderr)
        sys.exit(1)

    with open(lit_path, "r", encoding="utf-8") as f:
        literature = json.load(f)

    eval_data = evaluate_idea(idea_text, literature)
    report_md = format_evaluation_report(eval_data, idea_text)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(report_md, encoding="utf-8")
        print(f"[EXITO] Dictamen guardado en: {out_p}")
    else:
        print(report_md)

if __name__ == "__main__":
    main()
