#!/usr/bin/env python3
"""
search_openalex.py
Búsqueda sistematizada de literatura científica en OpenAlex (IEEE, ACM, Springer, Elsevier).
Implementa trazabilidad formal en fases PRISMA 2020:
  - Fase 1: Identificación inicial sin filtrar (raw pool), incluyendo artículos semilla y similares.
  - Fase 2: Registro de cribado con exclusiones negativas (filtro NOT) y compuerta de afinidad de dominio.
  - Fase 3: Artículos retenidos listos para ranking multidimensional.

Nuevas capacidades:
  - Soporte de Artículo Semilla (--seed): Ingesta un DOI/título y busca artículos similares y relacionados.
  - Búsqueda Facetada Multi-Eje (--axes): Ejecuta múltiples consultas temáticas y las fusiona sin duplicados.
  - Compuerta de Afinidad de Dominio (--domain-must): Purga artículos que no pertenezcan al dominio temático.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
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
    db_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "venues_hindex.json"
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


def resolve_seed_work(seed_input: str, email: str = "researcher@university.edu") -> Optional[Dict[str, Any]]:
    """Resuelve un artículo semilla a partir de un DOI, URL de IEEE/OpenAlex o título."""
    seed_str = seed_input.strip()
    headers = {"User-Agent": f"ResearchHarness/0.2 ({email})"}

    # 1. Detectar DOI
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", seed_str)
    if doi_match:
        clean_doi = doi_match.group(0).rstrip(".")
        url = f"https://api.openalex.org/works/https://doi.org/{clean_doi}?mailto={email}"
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

    # 2. Detectar ID de OpenAlex (W\d+)
    openalex_match = re.search(r"W\d{8,12}", seed_str)
    if openalex_match:
        url = f"https://api.openalex.org/works/{openalex_match.group(0)}?mailto={email}"
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

    # 3. Búsqueda por título en OpenAlex
    clean_title = re.sub(r"https?://\S+", "", seed_str).strip()
    if len(clean_title) > 8:
        encoded = urllib.parse.quote(clean_title)
        url = f"https://api.openalex.org/works?search={encoded}&per-page=1&mailto={email}"
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200 and resp.json().get("results"):
                return resp.json()["results"][0]
        except Exception:
            pass

    return None


def fetch_similar_to_seed(
    seed_work: Dict[str, Any],
    years_back: int = 3,
    max_similar: int = 15,
    email: str = "researcher@university.edu"
) -> List[Dict[str, Any]]:
    """Busca artículos estrechamente relacionados con la semilla en OpenAlex."""
    current_year = datetime.now().year
    from_year = current_year - years_back
    headers = {"User-Agent": f"ResearchHarness/0.2 ({email})"}
    seed_title = seed_work.get("title") or ""
    
    similar_works = []
    if seed_title:
        # Búsqueda semántica usando el título de la semilla
        encoded_title = urllib.parse.quote(seed_title)
        url = (
            f"https://api.openalex.org/works"
            f"?search={encoded_title}"
            f"&filter=from_publication_date:{from_year}-01-01"
            f"&per-page={max_similar}"
            f"&mailto={email}"
        )
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                for r in results:
                    # Evitar duplicar la semilla exacta
                    if r.get("id") != seed_work.get("id"):
                        r["_source_tag"] = "Similitud Semántica con Semilla"
                        similar_works.append(r)
        except Exception as e:
            print(f"[WARN] No se pudo buscar similares a la semilla: {e}", file=sys.stderr)

    return similar_works


def parse_openalex_item(item: Dict[str, Any], venues_db: Dict[str, Any], current_year: int) -> Dict[str, Any]:
    title = item.get("title") or ""
    abstract = reconstruct_abstract(item.get("abstract_inverted_index")) if "abstract_inverted_index" in item else item.get("abstract", "")
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
    score = round((annual_citations * 0.45) + (h5 * 0.35) + (10 if pub_year >= current_year - 1 else 0), 2)

    authorships = item.get("authorships", [])
    author_names = [a.get("author", {}).get("display_name", "") for a in authorships[:3]]
    authors_str = ", ".join(author_names) + (" et al." if len(authorships) > 3 else "")

    return {
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
        "score": score,
        "is_seed": item.get("_is_seed", False),
        "source_tag": item.get("_source_tag", "Búsqueda Abierta")
    }


def search_openalex_with_traceability(
    include_keywords: List[str],
    exclude_keywords: List[str],
    domain_must: List[str] = None,
    axes_queries: List[str] = None,
    seed_input: str = "",
    seed_similarity_count: int = 15,
    years_back: int = 3,
    max_results: int = 50,
    email: str = "researcher@university.edu"
) -> Dict[str, Any]:
    current_year = datetime.now().year
    from_year = current_year - years_back
    venues_db = load_venues_db()
    headers = {"User-Agent": f"ResearchHarness/0.2 ({email})"}

    raw_candidates_map: Dict[str, Dict[str, Any]] = {}
    seed_article = None

    # 1. Ingesta del Artículo Semilla si fue provisto
    if seed_input:
        print(f"[INFO] Resolviendo artículo semilla: {seed_input}...")
        seed_raw = resolve_seed_work(seed_input, email=email)
        if seed_raw:
            seed_raw["_is_seed"] = True
            seed_raw["_source_tag"] = "🎯 Artículo Semilla (Referencia de Anclaje)"
            seed_parsed = parse_openalex_item(seed_raw, venues_db, current_year)
            seed_article = seed_parsed
            raw_candidates_map[seed_parsed["id"] or seed_parsed["doi"]] = seed_parsed
            print(f"[EXITO] Semilla anclada: {seed_parsed['title']} ({seed_parsed['year']})")

            # Buscar artículos similares a la semilla
            print(f"[INFO] Buscando obras similares a la semilla en OpenAlex...")
            similar_raws = fetch_similar_to_seed(seed_raw, years_back=years_back, max_similar=seed_similarity_count, email=email)
            for sr in similar_raws:
                parsed_sim = parse_openalex_item(sr, venues_db, current_year)
                ident = parsed_sim["id"] or parsed_sim["doi"]
                if ident and ident not in raw_candidates_map:
                    raw_candidates_map[ident] = parsed_sim
            print(f"[INFO] {len(similar_raws)} artículos similares a la semilla incorporados al pool.")
        else:
            print(f"[WARN] No se pudo resolver automáticamente la semilla: {seed_input}", file=sys.stderr)

    # 2. Ejecución de Búsquedas (Multi-Eje o Consulta Simple)
    queries_to_run = axes_queries if axes_queries else [" ".join(include_keywords)]
    
    for q_idx, q_str in enumerate(queries_to_run, start=1):
        if not q_str.strip():
            continue
        encoded_query = urllib.parse.quote(q_str.strip())
        url = (
            f"https://api.openalex.org/works"
            f"?search={encoded_query}"
            f"&filter=from_publication_date:{from_year}-01-01"
            f"&per-page={min(max_results * 2, 80)}"
            f"&mailto={email}"
        )
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            if resp.status_code == 200:
                items = resp.json().get("results", [])
                for item in items:
                    item["_source_tag"] = f"Eje {q_idx}: {q_str[:35]}..." if len(queries_to_run) > 1 else "Búsqueda Abierta"
                    parsed = parse_openalex_item(item, venues_db, current_year)
                    ident = parsed["id"] or parsed["doi"] or parsed["title"]
                    if ident and ident not in raw_candidates_map:
                        raw_candidates_map[ident] = parsed
        except Exception as e:
            print(f"[ERROR] Error al consultar eje '{q_str}': {e}", file=sys.stderr)

    raw_pool = list(raw_candidates_map.values())

    # 3. Cribado (Fase 2 PRISMA): Exclusiones NOT y Compuerta de Dominio
    screening_log = []
    retained_articles = []

    low_excludes = [w.lower().strip() for w in exclude_keywords if w.strip()]
    low_domain_must = [w.lower().strip() for w in (domain_must or []) if w.strip()]

    for article in raw_pool:
        # La semilla de anclaje es inmune al descarte
        if article.get("is_seed"):
            screening_log.append({
                "article": article,
                "status": "RETAINED",
                "reason": "🎯 Artículo Semilla Inyectado (Anclaje Metodológico)"
            })
            retained_articles.append(article)
            continue

        text_to_check = (article.get("title", "") + " " + article.get("abstract", "")).lower()

        # Chequeo 1: Filtro negativo explícito (NOT)
        matched_exclusion = None
        for exc in low_excludes:
            if exc in text_to_check:
                matched_exclusion = exc
                break

        if matched_exclusion:
            screening_log.append({
                "article": article,
                "status": "EXCLUDED",
                "reason": f"Filtro NOT de exclusión: coincidencia con '{matched_exclusion}'"
            })
            continue

        # Chequeo 2: Compuerta de afinidad obligatoria de dominio (Domain Must)
        if low_domain_must:
            has_domain_affinity = any(d_word in text_to_check for d_word in low_domain_must)
            if not has_domain_affinity:
                screening_log.append({
                    "article": article,
                    "status": "EXCLUDED",
                    "reason": f"Falta de afinidad con dominio obligatorio (no menciona {', '.join(low_domain_must[:4])})"
                })
                continue

        # Retenido
        screening_log.append({
            "article": article,
            "status": "RETAINED",
            "reason": "Cumple criterios temáticos de inclusión y supera compuerta de dominio"
        })
        retained_articles.append(article)

    return {
        "raw_pool": raw_pool,
        "screening_log": screening_log,
        "retained_articles": retained_articles,
        "seed_article": seed_article,
        "include_keywords": include_keywords,
        "exclude_keywords": exclude_keywords,
        "domain_must": domain_must or []
    }


def generate_phase1_markdown(data: Dict[str, Any]) -> str:
    raw_pool = data.get("raw_pool", [])
    seed = data.get("seed_article")
    lines = [
        "# Fase 1: Identificación Inicial de Literatura (Pool Crudo sin Filtrar)",
        "",
        f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Total Artículos Recuperados:** {len(raw_pool)}  ",
    ]
    if seed:
        lines.append(f"**Artículo Semilla de Referencia:** *{seed.get('title')}* ({seed.get('year')}) | [DOI]({seed.get('doi')})")

    lines.extend([
        "",
        "> [!NOTE] Criterio PRISMA de Identificación",
        "> Esta lista reúne todos los artículos devueltos por OpenAlex (búsquedas por ejes, artículos semilla y obras con alta similitud conceptual) antes de aplicar filtros negativos o compuertas temáticas.",
        "",
        "---",
        "",
        "| # | Título | Año | Venue | Origen / Tag | Citaciones | DOI |",
        "|---|---|:---:|---|---|:---:|:---:|"
    ])

    for idx, art in enumerate(raw_pool, start=1):
        title = art.get("title", "")[:65] + ("..." if len(art.get("title", "")) > 65 else "")
        doi = f"[Link]({art.get('doi')})" if art.get("doi") else "N/A"
        tag = "🎯 Semilla" if art.get("is_seed") else art.get("source_tag", "Búsqueda")
        lines.append(
            f"| {idx} | {title} | {art.get('year')} | {art.get('venue')[:25]} | `{tag}` | {art.get('citations')} | {doi} |"
        )

    return "\n".join(lines)


def generate_phase2_markdown(data: Dict[str, Any]) -> str:
    screening_log = data.get("screening_log", [])
    excludes = data.get("exclude_keywords", [])
    domain_must = data.get("domain_must", [])
    retained_count = sum(1 for item in screening_log if item["status"] == "RETAINED")
    excluded_count = sum(1 for item in screening_log if item["status"] == "EXCLUDED")

    lines = [
        "# Fase 2: Registro de Cribado, Exclusiones Negativas y Compuerta de Dominio",
        "",
        f"**Términos de Exclusión (NOT):** `{', '.join(excludes) if excludes else 'Ninguno'}`  ",
        f"**Compuerta de Dominio Obligatoria:** `{', '.join(domain_must) if domain_must else 'Ninguna'}`  ",
        f"**Total Artículos Evaluados:** {len(screening_log)}  ",
        f"**Artículos Retenidos:** {retained_count}  ",
        f"**Artículos Descartados:** {excluded_count}  ",
        "",
        "> [!IMPORTANT] Trazabilidad del Filtro PRISMA",
        "> Cada descarte se fundamenta en la presencia de términos no deseados (NOT) o en la ausencia total de vocabulario del dominio obligatorio.",
        "",
        "---",
        "",
        "| # | Título | Año | Estado | Motivo / Criterio de Decisión |",
        "|---|---|:---:|---|---|"
    ]

    for idx, item in enumerate(screening_log, start=1):
        art = item["article"]
        title = art.get("title", "")[:65] + ("..." if len(art.get("title", "")) > 65 else "")
        year = art.get("year", "")
        status = "✅ Retenido" if item["status"] == "RETAINED" else "❌ Excluido"
        reason = item["reason"]
        lines.append(f"| {idx} | {title} | {year} | {status} | {reason} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Búsqueda avanzada de literatura en OpenAlex con trazabilidad en fases y soporte de semilla")
    parser.add_argument("--include", nargs="*", default=[], help="Palabras clave a incluir")
    parser.add_argument("--exclude", nargs="*", default=[], help="Palabras a excluir (filtro NOT)")
    parser.add_argument("--domain-must", nargs="*", default=[], help="Palabras clave obligatorias de dominio (al menos una debe estar presente)")
    parser.add_argument("--axes", nargs="*", default=[], help="Múltiples consultas de ejes temáticos para búsqueda facetada")
    parser.add_argument("--seed", type=str, default="", help="Artículo semilla (DOI, URL o título) para anclaje y búsqueda de similares")
    parser.add_argument("--seed-similar-count", type=int, default=15, help="Cantidad de artículos similares a la semilla a recuperar")
    parser.add_argument("--years", type=int, default=3, help="Años hacia atrás (default: 3)")
    parser.add_argument("--max", type=int, default=35, help="Máximo de artículos retenidos")
    parser.add_argument("--output", type=str, default="", help="Ruta del archivo JSON limpio")
    parser.add_argument("--phase1-out", type=str, default="", help="Ruta para guardar Fase 1")
    parser.add_argument("--phase2-out", type=str, default="", help="Ruta para guardar Fase 2")

    args = parser.parse_args()

    results = search_openalex_with_traceability(
        include_keywords=args.include,
        exclude_keywords=args.exclude,
        domain_must=args.domain_must,
        axes_queries=args.axes,
        seed_input=args.seed,
        seed_similarity_count=args.seed_similar_count,
        years_back=args.years,
        max_results=args.max
    )

    retained = results.get("retained_articles", [])
    raw_pool = results.get("raw_pool", [])
    print(f"[INFO] Búsqueda completada.")
    print(f"       - Candidatos crudos identificados (Fase 1): {len(raw_pool)}")
    print(f"       - Artículos retenidos tras cribado (Fase 2): {len(retained)}")

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(retained, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Dataset retenido guardado en: {out_p}")

        base_dir = out_p.parent.parent if out_p.parent.name == "raw" else out_p.parent
        p1_path = Path(args.phase1_out) if args.phase1_out else (base_dir / "fase1_identificacion_sin_filtrar.md")
        p2_path = Path(args.phase2_out) if args.phase2_out else (base_dir / "fase2_cribado_exclusiones.md")

        p1_path.parent.mkdir(parents=True, exist_ok=True)
        p1_path.write_text(generate_phase1_markdown(results), encoding="utf-8")
        print(f"[INFO] Reporte Fase 1 guardado en: {p1_path}")

        p2_path.parent.mkdir(parents=True, exist_ok=True)
        p2_path.write_text(generate_phase2_markdown(results), encoding="utf-8")
        print(f"[INFO] Reporte Fase 2 guardado en: {p2_path}")
    else:
        print(json.dumps(retained[:5], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
