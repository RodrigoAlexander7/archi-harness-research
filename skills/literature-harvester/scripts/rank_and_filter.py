#!/usr/bin/env python3
"""
rank_and_filter.py
Ejecuta el ranking multidimensional (Impacto de citas anualizadas + Prestigio H5-index / Cuartil),
aplica el corte a Top N artículos y detecta Joyas Emergentes (papers 2025-2026).
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

def rank_articles(
    articles: List[Dict[str, Any]],
    top_n: int = 10,
    emerging_count: int = 2
) -> Dict[str, Any]:
    current_year = 2026

    # Calcular puntajes detallados
    for art in articles:
        year = art.get("year", current_year)
        cites = art.get("citations", 0)
        age = max(1, current_year - year + 1)
        annual_cites = cites / age
        h5 = art.get("h5_index", 25)

        # Factor cuartil
        quartile = str(art.get("quartile", "")).upper()
        q_bonus = 25 if "Q1" in quartile else (15 if "Q2" in quartile else 5)

        # Score ponderado
        composite_score = round(
            (annual_cites * 0.45) + 
            (h5 * 0.35) + 
            q_bonus, 
            2
        )
        art["annual_citations"] = round(annual_cites, 2)
        art["composite_score"] = composite_score

    # Separar candidatos a joyas emergentes (año >= current_year - 1 y pocas citas)
    emerging_candidates = [
        a for a in articles 
        if a.get("year", 0) >= (current_year - 1) and a.get("citations", 0) <= 5
    ]
    # Ordenar joyas emergentes por H5 del venue o por recencia
    emerging_candidates.sort(key=lambda x: (x.get("year", 0), x.get("h5_index", 0)), reverse=True)
    selected_emerging = emerging_candidates[:emerging_count]
    emerging_ids = {e.get("id") for e in selected_emerging}

    # Ordenar el resto por composite_score
    main_pool = [a for a in articles if a.get("id") not in emerging_ids]
    main_pool.sort(key=lambda x: x["composite_score"], reverse=True)

    top_main = main_pool[:(top_n - len(selected_emerging))]

    final_selection = top_main + selected_emerging
    # Marcar joyas emergentes en los metadatos
    for a in final_selection:
        a["is_emerging_gem"] = a.get("id") in emerging_ids

    return {
        "total_analyzed": len(articles),
        "top_ranked": final_selection,
        "emerging_gems": selected_emerging
    }

def format_markdown_table(ranked_data: Dict[str, Any]) -> str:
    lines = [
        "| # | Título | Año | Journal / Venue | Cuartil | H5 | Citas (Anual.) | Tipo | Acceso | DOI |",
        "|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|"
    ]

    for idx, art in enumerate(ranked_data["top_ranked"], start=1):
        title = art.get("title", "")[:65] + ("..." if len(art.get("title", "")) > 65 else "")
        year = art.get("year", "")
        venue = art.get("venue", "N/A")[:30]
        q = art.get("quartile", "Desc")
        h5 = art.get("h5_index", 25)
        cites = art.get("citations", 0)
        ann_cites = art.get("annual_citations", 0.0)
        cite_str = f"{cites} ({ann_cites})"
        gem_str = "💎 Joya Reciente" if art.get("is_emerging_gem") else "SOTA Benchmark"
        oa_str = "🔓 Open Access" if art.get("is_open_access") else "🔒 Paywall (Univ)"
        doi = art.get("doi", "")
        doi_link = f"[Enlace]({doi})" if doi else "N/A"

        lines.append(f"| {idx} | {title} | {year} | {venue} | {q} | {h5} | {cite_str} | {gem_str} | {oa_str} | {doi_link} |")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Ranking multidimensional y selección de Joyas Emergentes")
    parser.add_argument("--input", required=True, help="Ruta al archivo JSON con artículos extraídos")
    parser.add_argument("--top", type=int, default=10, help="Número de artículos en el corte final")
    parser.add_argument("--emerging", type=int, default=2, help="Número de joyas emergentes a incluir")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de salida")
    parser.add_argument("--output", default="", help="Ruta de guardado (opcional)")

    args = parser.parse_args()
    in_path = Path(args.input)

    if not in_path.exists():
        print(f"[ERROR] Archivo no encontrado: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    ranked_data = rank_articles(articles, top_n=args.top, emerging_count=args.emerging)

    if args.format == "markdown":
        output_text = format_markdown_table(ranked_data)
    else:
        output_text = json.dumps(ranked_data, ensure_ascii=False, indent=2)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(output_text, encoding="utf-8")
        print(f"[EXITO] Resultados guardados en: {out_p}")
    else:
        print(output_text)

if __name__ == "__main__":
    main()
