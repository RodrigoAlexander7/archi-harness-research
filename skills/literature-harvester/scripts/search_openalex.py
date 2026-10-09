#!/usr/bin/env python3
"""
search_openalex.py
Búsqueda sistematizada de literatura científica en OpenAlex (IEEE, ACM, Springer, Elsevier).
Implementa trazabilidad formal en fases:
  - Fase 1: Identificación inicial sin filtrar (raw pool).
  - Fase 2: Registro de cribado y exclusiones negativas (screening log).
  - Fase 3: Artículos retenidos listos para ranking.
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import urllib.parse
import requests

def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstruye el texto plano del abstract a partir del índice invertido de OpenAlex."""
    if not inverted_index:
        return "No abstract available."
    position_word_map = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            position_word_map[pos] = word
    if not position_word_map:
        return "No abstract available."
    max_pos = max(position_word_map.keys())
    words = [position_word_map.get(i, "") for i in range(max_pos + 1)]
    return " ".join(words).strip()

def load_venues_db() -> Dict[str, Any]:
    db_path = Path(__file__).resolve().parent.parent.parent / "data" / "venues_hindex.json"
    if db_path.exists():
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def lookup_venue_info(venue_name: str, venues_db: Dict[str, Any]) -> Dict[str, Any]:
    if not venue_name:
        return {"quartile": "Desc", "h5_index": 20, "publisher": "Desc"}
    low_venue = venue_name.lower().strip()
    for name, data in venues_db.items():
        if name in low_venue or low_venue in name:
            return data
    return {"quartile": "No rankeado en DB local", "h5_index": 25, "publisher": "N/A"}

def search_openalex_with_traceability(
    include_keywords: List[str],
    exclude_keywords: List[str],
    years_back: int = 3,
    max_results: int = 50,
    email: str = "researcher@university.edu"
) -> Dict[str, Any]:
    current_year = datetime.now().year
    from_year = current_year - years_back

    query_str = " ".join(include_keywords)
    encoded_query = urllib.parse.quote(query_str)
    
    url = (
        f"https://api.openalex.org/works"
        f"?search={encoded_query}"
        f"&filter=from_publication_date:{from_year}-01-01"
        f"&per-page={min(max_results * 2, 100)}"
        f"&mailto={email}"
    )

    headers = {
        "User-Agent": f"ResearchHarness/0.1 ({email})"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] Falló la consulta a OpenAlex: {e}", file=sys.stderr)
        return {"raw_pool": [], "screening_log": [], "retained_articles": []}

    venues_db = load_venues_db()
    raw_results = data.get("results", [])
    
    raw_pool = []
    screening_log = []
    retained_articles = []

    low_excludes = [w.lower().strip() for w in exclude_keywords if w.strip()]

    for item in raw_results:
        title = item.get("title") or ""
        abstract = reconstruct_abstract(item.get("abstract_inverted_index"))
        pub_year = item.get("publication_year") or current_year
        citations = item.get("cited_by_count", 0)
        doi = item.get("doi") or ""
        primary_loc = item.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        venue_name = source.get("display_name") or "Desconocido"
        is_oa = primary_loc.get("is_oa", False)

        venue_info = lookup_venue_info(venue_name, venues_db)
        age = max(1, current_year - pub_year + 1)
        annual_citations = round(citations / age, 2)
        h5 = venue_info.get("h5_index", 25)
        score = round((annual_citations * 0.5) + (h5 * 0.3) + (10 if pub_year >= current_year - 1 else 0), 2)

        authorships = item.get("authorships", [])
        author_names = [a.get("author", {}).get("display_name", "") for a in authorships[:3]]
        authors_str = ", ".join(author_names) + (" et al." if len(authorships) > 3 else "")

        article = {
            "id": item.get("id"),
            "title": title,
            "abstract": abstract,
            "authors": authors_str,
            "year": pub_year,
            "venue": venue_name,
            "publisher": venue_info.get("publisher", "N/A"),
            "quartile": venue_info.get("quartile", "Desc"),
            "h5_index": h5,
            "citations": citations,
            "annual_citations": annual_citations,
            "is_open_access": is_oa,
            "doi": doi,
            "score": score
        }
        raw_pool.append(article)

        # Evaluar filtro de exclusión negativa (NOT)
        text_to_check = (title + " " + abstract).lower()
        matched_exclusion = None
        for exc in low_excludes:
            if exc in text_to_check:
                matched_exclusion = exc
                break

        if matched_exclusion:
            screening_log.append({
                "article": article,
                "status": "EXCLUDED",
                "reason": f"Coincidencia con término de exclusión: '{matched_exclusion}'"
            })
        else:
            screening_log.append({
                "article": article,
                "status": "RETAINED",
                "reason": "Superó todos los criterios de cribado"
            })
            retained_articles.append(article)

    retained_articles.sort(key=lambda x: x["score"], reverse=True)
    return {
        "query": query_str,
        "from_year": from_year,
        "current_year": current_year,
        "exclude_keywords": exclude_keywords,
        "raw_pool": raw_pool,
        "screening_log": screening_log,
        "retained_articles": retained_articles[:max_results]
    }

def generate_phase1_markdown(data: Dict[str, Any]) -> str:
    raw_pool = data.get("raw_pool", [])
    query = data.get("query", "")
    from_year = data.get("from_year", "")
    current_year = data.get("current_year", "")

    lines = [
        "# Fase 1: Identificación Inicial de Literatura (Lista Cruda Sin Filtrar)",
        "",
        f"**Ecuación Booleana de Entrada:** `{query}`  ",
        f"**Ventana Temporal:** {from_year} – {current_year}  ",
        f"**Total de Artículos Recuperados Inicialmente:** {len(raw_pool)} artículos  ",
        "",
        "> [!NOTE] Propósito Metodológico (Estándar PRISMA)",
        "> Esta lista documenta la totalidad de candidatos obtenidos tras la búsqueda con términos atómicos en repositorios abiertos antes de aplicar criterios de exclusión negativa.",
        "",
        "---",
        "",
        "| # | Título | Año | Journal / Conferencia | Citas | Acceso | DOI / Enlace |",
        "|---|---|:---:|---|:---:|:---:|:---:|"
    ]

    for idx, art in enumerate(raw_pool, start=1):
        title = art.get("title", "")[:75] + ("..." if len(art.get("title", "")) > 75 else "")
        year = art.get("year", "")
        venue = art.get("venue", "N/A")[:35]
        cites = art.get("citations", 0)
        oa = "🔓 Open Access" if art.get("is_open_access") else "🔒 Paywall"
        doi = art.get("doi", "")
        doi_link = f"[Enlace]({doi})" if doi else "N/A"
        lines.append(f"| {idx} | {title} | {year} | {venue} | {cites} | {oa} | {doi_link} |")

    return "\n".join(lines)

def generate_phase2_markdown(data: Dict[str, Any]) -> str:
    screening_log = data.get("screening_log", [])
    excludes = data.get("exclude_keywords", [])
    retained_count = sum(1 for item in screening_log if item["status"] == "RETAINED")
    excluded_count = sum(1 for item in screening_log if item["status"] == "EXCLUDED")

    lines = [
        "# Fase 2: Registro de Cribado y Exclusiones Negativas (Filtro NOT)",
        "",
        f"**Términos de Exclusión Aplicados:** `{', '.join(excludes) if excludes else 'Ninguno'}`  ",
        f"**Total Artículos Evaluados:** {len(screening_log)}  ",
        f"**Artículos Retenidos:** {retained_count}  ",
        f"**Artículos Descartados:** {excluded_count}  ",
        "",
        "> [!IMPORTANT] Trazabilidad del Filtro Negativo",
        "> Cada descarte se encuentra fundamentado por la presencia explícita de vocabulario que distorsiona el área de investigación o pertenece a disciplinas no deseadas.",
        "",
        "---",
        "",
        "| # | Título | Año | Estado | Motivo / Criterio de Decisión |",
        "|---|---|:---:|:---:|---|"
    ]

    for idx, item in enumerate(screening_log, start=1):
        art = item["article"]
        title = art.get("title", "")[:70] + ("..." if len(art.get("title", "")) > 70 else "")
        year = art.get("year", "")
        status = "✅ Retenido" if item["status"] == "RETAINED" else "❌ Excluido"
        reason = item["reason"]
        lines.append(f"| {idx} | {title} | {year} | {status} | {reason} |")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Búsqueda avanzada de literatura en OpenAlex con trazabilidad en fases")
    parser.add_argument("--include", nargs="+", required=True, help="Palabras clave a incluir (ej: quantum graphs)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Palabras a excluir (ej: mechanics optics)")
    parser.add_argument("--years", type=int, default=3, help="Años hacia atrás (default: 3)")
    parser.add_argument("--max", type=int, default=30, help="Máximo de artículos retenidos")
    parser.add_argument("--output", type=str, default="", help="Ruta del archivo JSON limpio")
    parser.add_argument("--phase1-out", type=str, default="", help="Ruta para guardar el reporte de Fase 1 (Lista Cruda)")
    parser.add_argument("--phase2-out", type=str, default="", help="Ruta para guardar el reporte de Fase 2 (Cribado)")

    args = parser.parse_args()

    results = search_openalex_with_traceability(
        include_keywords=args.include,
        exclude_keywords=args.exclude,
        years_back=args.years,
        max_results=args.max
    )

    retained = results.get("retained_articles", [])
    raw_pool = results.get("raw_pool", [])
    print(f"[INFO] Búsqueda completada.")
    print(f"       - Candidatos crudos identificados (Fase 1): {len(raw_pool)}")
    print(f"       - Artículos retenidos tras cribado (Fase 2): {len(retained)}")

    # Guardar JSON limpio
    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(retained, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Dataset retenido guardado en: {out_p}")

        # Si no se especificaron rutas para Fase 1 y 2, generarlas en el directorio padre por defecto
        base_dir = out_p.parent.parent if out_p.parent.name == "raw" else out_p.parent
        p1_path = Path(args.phase1_out) if args.phase1_out else (base_dir / "fase1_identificacion_sin_filtrar.md")
        p2_path = Path(args.phase2_out) if args.phase2_out else (base_dir / "fase2_cribado_exclusiones.md")

        p1_path.parent.mkdir(parents=True, exist_ok=True)
        p1_path.write_text(generate_phase1_markdown(results), encoding="utf-8")
        print(f"[INFO] Reporte Fase 1 (Lista Cruda) guardado en: {p1_path}")

        p2_path.parent.mkdir(parents=True, exist_ok=True)
        p2_path.write_text(generate_phase2_markdown(results), encoding="utf-8")
        print(f"[INFO] Reporte Fase 2 (Cribado de Exclusiones) guardado en: {p2_path}")
    else:
        print(json.dumps(retained[:5], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
