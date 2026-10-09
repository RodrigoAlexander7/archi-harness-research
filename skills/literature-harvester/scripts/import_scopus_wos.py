#!/usr/bin/env python3
"""
import_scopus_wos.py
Importador y normalizador de archivos exportados desde Scopus o Web of Science (CSV / BibTeX).
Permite integrar los resultados obtenidos con acceso universitario al arnés de investigación.
"""

import sys
import json
import csv
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

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
        return {"quartile": "Desc", "h5_index": 25, "publisher": "Desc"}
    low_venue = venue_name.lower().strip()
    for name, data in venues_db.items():
        if name in low_venue or low_venue in name:
            return data
    return {"quartile": "No rankeado en DB local", "h5_index": 25, "publisher": "N/A"}

def parse_csv_export(file_path: Path, venues_db: Dict[str, Any]) -> List[Dict[str, Any]]:
    articles = []
    current_year = datetime.now().year

    # Detectar encoding común en exportaciones (UTF-8 con BOM o Latin-1)
    encoding = "utf-8-sig"
    try:
        with open(file_path, "r", encoding=encoding) as f:
            f.read(1024)
    except UnicodeDecodeError:
        encoding = "latin-1"

    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return []

        # Normalizar nombres de columnas a minúsculas
        field_map = {fn.strip().lower(): fn for fn in reader.fieldnames}

        # Helper para obtener valor con varios posibles encabezados
        def get_val(row, candidates):
            for cand in candidates:
                for k, orig in field_map.items():
                    if cand in k:
                        return row.get(orig, "").strip()
            return ""

        for idx, row in enumerate(reader):
            title = get_val(row, ["title", "document title", "article title"])
            if not title:
                continue

            abstract = get_val(row, ["abstract"]) or "No abstract provided in export."
            venue = get_val(row, ["source title", "journal", "publication name", "conference"]) or "Unknown Venue"
            
            # Año
            year_str = get_val(row, ["year", "publication year"])
            try:
                year = int(re.sub(r"\D", "", year_str)[:4])
            except Exception:
                year = current_year

            # Citas
            cite_str = get_val(row, ["cited by", "times cited", "citations"])
            try:
                citations = int(re.sub(r"\D", "", cite_str) or 0)
            except Exception:
                citations = 0

            doi = get_val(row, ["doi"])
            authors = get_val(row, ["authors", "author names"])
            oa_str = get_val(row, ["open access"]).lower()
            is_oa = "open" in oa_str or "all open" in oa_str or "oa" in oa_str

            venue_info = lookup_venue_info(venue, venues_db)
            age = max(1, current_year - year + 1)
            annual_citations = round(citations / age, 2)
            h5 = venue_info.get("h5_index", 25)
            score = round((annual_citations * 0.5) + (h5 * 0.3) + (10 if year >= current_year - 1 else 0), 2)

            articles.append({
                "id": f"inst_export_{idx+1}",
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "venue": venue,
                "publisher": venue_info.get("publisher", "N/A"),
                "quartile": venue_info.get("quartile", "Desc"),
                "h5_index": h5,
                "citations": citations,
                "annual_citations": annual_citations,
                "is_open_access": is_oa,
                "doi": f"https://doi.org/{doi}" if doi and not doi.startswith("http") else doi,
                "score": score
            })

    return articles

def parse_bibtex_export(file_path: Path, venues_db: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Parser simple y robusto de BibTeX sin dependencias externas pesadas
    articles = []
    current_year = datetime.now().year
    content = file_path.read_text(encoding="utf-8", errors="replace")

    entries = re.split(r"@\w+\s*\{", content)[1:]
    for idx, entry in enumerate(entries):
        fields = {}
        for line in entry.splitlines():
            m = re.match(r"\s*([a-zA-Z_]+)\s*=\s*[\"{](.*?)[\"}],?\s*$", line.strip())
            if m:
                fields[m.group(1).lower()] = m.group(2).strip()

        title = fields.get("title", "")
        if not title:
            continue

        abstract = fields.get("abstract", "No abstract available.")
        venue = fields.get("journal") or fields.get("booktitle") or "Unknown Venue"
        try:
            year = int(fields.get("year", current_year))
        except Exception:
            year = current_year

        doi = fields.get("doi", "")
        authors = fields.get("author", "")
        venue_info = lookup_venue_info(venue, venues_db)
        h5 = venue_info.get("h5_index", 25)

        articles.append({
            "id": f"bib_entry_{idx+1}",
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "year": year,
            "venue": venue,
            "publisher": venue_info.get("publisher", "N/A"),
            "quartile": venue_info.get("quartile", "Desc"),
            "h5_index": h5,
            "citations": 0,
            "annual_citations": 0.0,
            "is_open_access": False,
            "doi": f"https://doi.org/{doi}" if doi and not doi.startswith("http") else doi,
            "score": round(h5 * 0.3 + (10 if year >= current_year - 1 else 0), 2)
        })

    return articles

def main():
    parser = argparse.ArgumentParser(description="Importar exportaciones de Scopus / Web of Science (CSV o BibTeX)")
    parser.add_argument("--input", required=True, help="Ruta al archivo CSV o .bib exportado")
    parser.add_argument("--output", required=True, help="Ruta del archivo JSON resultante normalizado")

    args = parser.parse_args()
    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"[ERROR] Archivo no encontrado: {in_path}", file=sys.stderr)
        sys.exit(1)

    venues_db = load_venues_db()

    if in_path.suffix.lower() == ".bib":
        articles = parse_bibtex_export(in_path, venues_db)
    else:
        articles = parse_csv_export(in_path, venues_db)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"[EXITO] Importados {len(articles)} artículos normalizados en: {out_path}")

if __name__ == "__main__":
    main()
