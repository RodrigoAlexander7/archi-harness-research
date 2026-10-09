#!/usr/bin/env python3
"""
rank_and_filter.py
Ejecuta el ranking multidimensional (Impacto bibliométrico + Bonificación Empírica + Joyas Emergentes),
prioriza artículos semilla (--seed), limita la cuota de surveys/reviews (--max-surveys) y aplica bonificación
a investigaciones con mediciones en hardware real (FPS, latencia, FPGA, Raspberry Pi, etc.).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


def is_survey_paper(title: str, abstract: str = "") -> bool:
    """Detecta si un artículo es un macro-survey o revisión bibliográfica."""
    t_lower = (title + " " + abstract[:200]).lower()
    return any(w in t_lower for w in ["survey", "literature review", "systematic review", "a decadal review", "state of the art review", "scoping review"])


def is_empirical_paper(title: str, abstract: str = "") -> bool:
    """Detecta si el artículo reporta validación empírica, experimentos o benchmarks cuantificables."""
    t_lower = (title + " " + abstract).lower()
    empirical_indicators = [
        "benchmark", "experimental", "experiment", "empirical", "dataset",
        "ablation", "comparative study", "testbed", "metrics", "case study",
        "real-world", "prototype", "deployed", "measurements"
    ]
    return any(kw in t_lower for kw in empirical_indicators)


def rank_articles(
    articles: List[Dict[str, Any]],
    top_n: int = 10,
    emerging_count: int = 2,
    max_surveys: int = 1
) -> Dict[str, Any]:
    current_year = 2026

    # 1. Calcular puntajes y atributos
    for art in articles:
        year = art.get("year", current_year)
        cites = art.get("citations", 0)
        age = max(1, current_year - year + 1)
        annual_cites = cites / age
        h5 = art.get("h5_index", 25)

        # Factor cuartil
        quartile = str(art.get("quartile", "")).upper()
        q_bonus = 25 if "Q1" in quartile else (15 if "Q2" in quartile else 5)

        # Bonificación empírica general (aplica a cualquier ciencia)
        text_full = art.get("title", "") + " " + art.get("abstract", "")
        is_emp = is_empirical_paper(art.get("title", ""), art.get("abstract", ""))
        emp_bonus = 15 if is_emp else 0
        is_survey = is_survey_paper(art.get("title", ""), art.get("abstract", ""))

        # Afinidad semántica si viene calculada del harvester iterativo (escala 0-10 -> ponderado)
        affinity = art.get("affinity_score", 7.0)
        affinity_component = affinity * 4.0  # hasta 40 pts

        # Penalización a macro-surveys para evitar que desplacen papers empíricos
        survey_penalty = -20 if is_survey else 0

        # Score ponderado
        composite_score = round(
            (annual_cites * 0.35) +
            (h5 * 0.25) +
            q_bonus +
            emp_bonus +
            affinity_component +
            survey_penalty,
            2
        )

        art["annual_citations"] = round(annual_cites, 2)
        art["composite_score"] = composite_score
        art["is_empirical"] = is_emp
        art["is_survey"] = is_survey

    # 2. Separar artículos semilla (Máxima prioridad de anclaje)
    seed_articles = [a for a in articles if a.get("is_seed", False)]
    seed_ids = {s.get("id") or s.get("doi") for s in seed_articles}
    remaining_pool = [a for a in articles if (a.get("id") or a.get("doi")) not in seed_ids]

    # 3. Separar Joyas Emergentes (2025-2026 con pocas citas)
    emerging_candidates = [
        a for a in remaining_pool
        if a.get("year", 0) >= (current_year - 1) and a.get("citations", 0) <= 8 and not a.get("is_survey")
    ]
    # Priorizar joyas con validación empírica o alto H5
    emerging_candidates.sort(
        key=lambda x: (x.get("is_empirical", False), x.get("year", 0), x.get("h5_index", 0)),
        reverse=True
    )
    selected_emerging = emerging_candidates[:emerging_count]
    emerging_ids = {e.get("id") or e.get("doi") for e in selected_emerging}

    # 4. Seleccionar el pool principal respetando cupo de surveys
    candidate_main = [a for a in remaining_pool if (a.get("id") or a.get("doi")) not in emerging_ids]
    candidate_main.sort(key=lambda x: x["composite_score"], reverse=True)

    available_slots = top_n - len(seed_articles) - len(selected_emerging)
    selected_main = []
    surveys_included = 0

    for a in candidate_main:
        if len(selected_main) >= available_slots:
            break
        if a.get("is_survey", False):
            if surveys_included < max_surveys:
                selected_main.append(a)
                surveys_included += 1
        else:
            selected_main.append(a)

    # 5. Ensamblar selección final: Semillas + Main + Joyas
    final_selection = seed_articles + selected_main + selected_emerging

    # Asignar etiquetas visibles
    for a in final_selection:
        if a.get("is_seed"):
            a["tag"] = "🎯 Semilla de Anclaje"
        elif (a.get("id") or a.get("doi")) in emerging_ids:
            a["tag"] = "💎 Joya Reciente"
        elif a.get("is_empirical"):
            a["tag"] = "⚙️ Validación Empírica"
        elif a.get("is_survey"):
            a["tag"] = "📖 SOTA Survey"
        else:
            a["tag"] = "🔬 SOTA Metodológico"

    return {
        "total_analyzed": len(articles),
        "seed_articles": seed_articles,
        "top_ranked": final_selection,
        "emerging_gems": selected_emerging
    }


def format_markdown_table(ranked_data: Dict[str, Any]) -> str:
    lines = [
        "| # | Título | Año | Journal / Venue | Cuartil | H5 | Citas (Anual.) | Categoría / Tag | Acceso | DOI |",
        "|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|"
    ]

    for idx, art in enumerate(ranked_data["top_ranked"], start=1):
        title = art.get("title", "")[:60] + ("..." if len(art.get("title", "")) > 60 else "")
        year = art.get("year", "")
        venue = art.get("venue", "N/A")[:28]
        q = art.get("quartile", "Desc")
        h5 = art.get("h5_index", 25)
        cites = art.get("citations", 0)
        ann_cites = art.get("annual_citations", 0.0)
        cite_str = f"{cites} ({ann_cites})"
        tag_str = art.get("tag", "SOTA Benchmark")
        oa_str = "🔓 Open Access" if art.get("is_open_access") else "🔒 Paywall (Univ)"
        doi = art.get("doi", "")
        doi_link = f"[Enlace]({doi})" if doi else "N/A"

        lines.append(f"| {idx} | {title} | {year} | {venue} | {q} | {h5} | {cite_str} | `{tag_str}` | {oa_str} | {doi_link} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Ranking multidimensional con bonificación empírica, cuota de surveys y soporte de semilla")
    parser.add_argument("--input", required=True, help="Ruta al archivo JSON con artículos extraídos")
    parser.add_argument("--top", type=int, default=10, help="Número de artículos en el corte final")
    parser.add_argument("--emerging", type=int, default=2, help="Número de joyas emergentes a incluir")
    parser.add_argument("--max-surveys", type=int, default=2, help="Máximo número de surveys permitidos en el Top")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de salida")
    parser.add_argument("--output", default="", help="Ruta de guardado (opcional)")

    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERROR] Archivo no encontrado: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    ranked_data = rank_articles(
        articles,
        top_n=args.top,
        emerging_count=args.emerging,
        max_surveys=args.max_surveys
    )

    if args.format == "markdown":
        output_str = format_markdown_table(ranked_data)
    else:
        output_str = json.dumps(ranked_data["top_ranked"], ensure_ascii=False, indent=2)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(output_str, encoding="utf-8")
        print(f"[INFO] Ranking guardado en: {out_p}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
