#!/usr/bin/env python3
"""
search_openalex.py
Búsqueda sistematizada de literatura científica en OpenAlex (IEEE, ACM, Springer, Elsevier).
Implementa filtros booleanos, ventana temporal, palabras negativas de exclusión y ranking inicial.
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
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

def search_openalex(
    include_keywords: List[str],
    exclude_keywords: List[str],
    years_back: int = 3,
    max_results: int = 50,
    email: str = "researcher@university.edu"
) -> List[Dict[str, Any]]:
    current_year = datetime.now().year
    from_year = current_year - years_back

    # Construir query de OpenAlex
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
        return []

    venues_db = load_venues_db()
    raw_results = data.get("results", [])
    filtered_articles = []

    low_excludes = [w.lower().strip() for w in exclude_keywords if w.strip()]

    for item in raw_results:
        title = item.get("title") or ""
        abstract = reconstruct_abstract(item.get("abstract_inverted_index"))
        pub_year = item.get("publication_year") or current_year
        citations = item.get("cited_by_count", 0)
        
        # Filtro de exclusión negativa (NOT)
        text_to_check = (title + " " + abstract).lower()
        if any(exc in text_to_check for exc in low_excludes):
            continue

        doi = item.get("doi") or ""
        primary_loc = item.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        venue_name = source.get("display_name") or "Desconocido"
        is_oa = primary_loc.get("is_oa", False)

        venue_info = lookup_venue_info(venue_name, venues_db)
        
        # Citas anualizadas
        age = max(1, current_year - pub_year + 1)
        annual_citations = round(citations / age, 2)
        
        # Puntaje compuesto para ranking inicial
        h5 = venue_info.get("h5_index", 25)
        score = round((annual_citations * 0.5) + (h5 * 0.3) + (10 if pub_year >= current_year - 1 else 0), 2)

        # Autores principales
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
        filtered_articles.append(article)

    # Ordenar por score compuesto descendente
    filtered_articles.sort(key=lambda x: x["score"], reverse=True)
    return filtered_articles[:max_results]

def main():
    parser = argparse.ArgumentParser(description="Búsqueda avanzada de literatura en OpenAlex con filtro booleano")
    parser.add_argument("--include", nargs="+", required=True, help="Palabras clave a incluir (ej: quantum graphs)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Palabras a excluir (ej: mechanics optics)")
    parser.add_argument("--years", type=int, default=3, help="Años hacia atrás (default: 3)")
    parser.add_argument("--max", type=int, default=30, help="Máximo de artículos en la salida")
    parser.add_argument("--output", type=str, default="", help="Ruta del archivo JSON de salida")

    args = parser.parse_args()

    results = search_openalex(
        include_keywords=args.include,
        exclude_keywords=args.exclude,
        years_back=args.years,
        max_results=args.max
    )

    print(f"[INFO] Búsqueda completada. Artículos retenidos tras filtros: {len(results)}")

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Resultados guardados en: {out_p}")
    else:
        print(json.dumps(results[:5], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
