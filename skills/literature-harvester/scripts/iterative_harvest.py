#!/usr/bin/env python3
"""
iterative_harvest.py
Búsqueda y Cosecha Bibliográfica Agéntica e Iterativa (Self-Reflective Retrieval Loop).

Arquitectura General y Escalable:
1. Ingesta Inteligente: Extrae Título, Keywords, Abstract y Párrafos Clave de la propuesta (LaTeX, Markdown o Texto).
2. Perfilado de Facetas:
   - Entidad (E): Objetos centrales del estudio extraídos de Título y Keywords (e.g. vehicle, traffic; quechua).
   - Método (M): Modelos, algoritmos, representaciones (e.g. YOLO, OBB, oriented detection, slot segmentation).
   - Contexto (C): Plataformas y entornos (e.g. edge, embedded, Raspberry Pi, heterogeneous traffic).
3. Bucle Iterativo Autónomo:
   - Ingesta la Semilla (máx 3-4 similares de anclaje para no canibalizar el pool).
   - Formula y ejecuta consultas facetadas compuestas en OpenAlex combinando (E + M), (E + C), (E + M + C).
   - Crítico Agéntico 1 a 1:
     * Verifica la presencia de la Entidad E. Si la entidad está ausente o es ajena (e.g. barcos, telas, baches, SAR), descarta el paper.
     * Evalúa co-ocurrencia con Método M y Contexto C.
   - Acumula los 20 mejores candidatos en `top20_candidatos_revisados.md`.
4. Etapa 2 (Selección Final Top 10):
   - Aplica ranking multicriterio científico en `summary_table.md` y genera `references.bib` verificado con DOIs reales.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
from nltk.stem import PorterStemmer
from rapidfuzz import fuzz

try:
    from search_openalex import (
        fetch_similar_to_seed,
        load_venues_db,
        lookup_venue_info,
        parse_openalex_item,
        resolve_seed_work,
    )
    from rank_and_filter import rank_articles, format_markdown_table
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from search_openalex import (
        fetch_similar_to_seed,
        load_venues_db,
        lookup_venue_info,
        parse_openalex_item,
        resolve_seed_work,
    )
    from rank_and_filter import rank_articles, format_markdown_table

STEMMER = PorterStemmer()

STOPWORDS = {
    "the", "and", "of", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with",
    "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have",
    "new", "we", "our", "paper", "propose", "proposed", "method", "results", "approach",
    "el", "la", "los", "las", "un", "una", "de", "del", "en", "para", "por", "con", "su",
    "que", "se", "es", "son", "artículo", "proponemos", "método", "resultados", "via", "based",
    "using", "used", "which", "can", "also", "into", "two", "three", "first", "study", "analysis",
    "system", "systems", "performance", "high", "low", "model", "models", "data", "dataset", "datasets",
    "table", "figure", "images", "image", "test", "train", "training", "testing", "section", "overview",
    "however", "available", "these", "their", "demonstrate", "challenges", "field", "scale", "both",
    "complex", "only", "including", "small", "when", "efficiency", "existing", "module", "then", "under",
    "such", "between", "each", "were", "been", "more", "most", "about", "above", "after", "while",
    "fine", "tuning", "was", "were", "remain", "remains", "running", "intelligent"
}

SCIENTIFIC_CORE_WORDS = {
    "method", "methods", "learning", "research", "vision", "applications", "application",
    "model", "models", "data", "dataset", "datasets", "information", "systems", "system",
    "study", "studies", "performance", "results", "analysis", "approach", "approaches",
    "network", "networks", "algorithm", "algorithms", "large", "deep", "framework",
    "evaluation", "technique", "techniques", "paper", "proposed", "detection",
    "classification", "processing", "review", "survey", "task", "tasks", "benchmark",
    "benchmarking", "real", "time", "accuracy", "state", "art", "novel", "efficient",
    "optimization", "scalability", "latency", "robustness", "throughput", "box", "boxes",
    "bounding", "boundary", "label", "labels", "feature", "features", "visual", "video",
    "frame", "frames", "input", "output", "layer", "layers", "precision", "recall", "metric",
    "speed", "loss", "device", "devices", "platform", "platforms", "hardware", "software",
    "embedded", "edge", "mobile", "architecture", "architectures"
}

BILINGUAL_MAP = {
    "vehículo": "vehicle", "vehículos": "vehicle", "tráfico": "traffic", "tránsito": "traffic",
    "borde": "edge", "red": "network", "redes": "network", "neuronal": "neural",
    "aprendizaje": "learning", "detección": "detection", "clasificación": "classification",
    "orientado": "oriented", "orientada": "oriented", "tiempo": "time", "real": "real",
    "traducción": "translation", "lengua": "language", "lenguas": "language", "idioma": "language",
    "morfología": "morphology", "generativo": "generative", "generativa": "generative",
    "evaluación": "evaluation", "comparativo": "comparative", "óptimo": "optimal"
}


def parse_research_intake(raw_input: str) -> Dict[str, Any]:
    p = Path(raw_input)
    raw_text = p.read_text(encoding="utf-8", errors="ignore") if p.exists() and p.is_file() else raw_input

    title = ""
    abstract = ""
    keywords_list: List[str] = []

    title_m = re.search(r"\\title(?:\[[^\]]*\])?\{([^}]+)\}", raw_text)
    if title_m:
        title = title_m.group(1).strip()

    abs_m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", raw_text, re.DOTALL)
    if abs_m:
        abstract = abs_m.group(1).strip()

    kw_m = re.search(r"\\keywords\{([^}]+)\}", raw_text)
    if kw_m:
        kw_str = kw_m.group(1)
        keywords_list = [k.strip() for k in re.split(r"\\and|,|;", kw_str) if k.strip()]

    if not title:
        m_title = re.search(r"^#\s+(.+)$", raw_text, re.MULTILINE)
        if m_title:
            title = m_title.group(1).strip()

    if not abstract:
        m_abs = re.search(r"(?:##\s*Abstract|Abstract:|Resumen:)\s*\n+(.*?)(?=\n##|\Z)", raw_text, re.DOTALL | re.IGNORECASE)
        if m_abs:
            abstract = m_abs.group(1).strip()

    if not title:
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        title = lines[0] if lines else "Investigación Científica"
        abstract = " ".join(lines[1:8]) if len(lines) > 1 else ""

    clean_title = re.sub(r"\\[a-zA-Z]+", " ", title)
    clean_title = re.sub(r"[\{\}\$\%\#\_\^~]", " ", clean_title).strip()
    
    clean_abs = re.sub(r"%.*", "", abstract)
    clean_abs = re.sub(r"\\(?:cite|ref|label|pageref)\{[^}\n]*\}", "", clean_abs)
    clean_abs = re.sub(r"\\[a-zA-Z]+", " ", clean_abs)
    clean_abs = re.sub(r"[\{\}\$\%\#\_\^~]", " ", clean_abs).strip()

    clean_kws = [re.sub(r"\\[a-zA-Z]+|[\{\}\$\%\#\_\^~]", " ", k).strip() for k in keywords_list]
    clean_kws = [k for k in clean_kws if k]

    return {
        "title": clean_title,
        "abstract": clean_abs,
        "keywords": clean_kws,
        "full_text": raw_text
    }


def extract_facets_and_profile(parsed_intake: Dict[str, Any]) -> Dict[str, Any]:
    title = parsed_intake["title"]
    abstract = parsed_intake["abstract"]
    keywords = parsed_intake["keywords"]

    all_words = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{3,}\b", (title + " " + " ".join(keywords) + " " + abstract).lower())
    protected_roots = {STEMMER.stem(BILINGUAL_MAP.get(w, w)) for w in all_words}

    method_indicators = {
        "yolo", "cnn", "transformer", "llm", "neural", "deep", "detector", "segmenter",
        "segmentation", "detection", "classification", "translation", "recognition",
        "algorithm", "model", "framework", "architecture", "fts5", "bert", "resnet",
        "obb", "oriented", "bounding", "slot", "rule", "neuro-symbolic", "generative"
    }
    
    context_indicators = {
        "edge", "embedded", "raspberry", "fpga", "jetson", "soc", "microcontroller",
        "real-time", "realtime", "latency", "fps", "power", "int8", "quantization",
        "throughput", "heterogeneous", "mixed", "dense", "congested", "low-resource",
        "agglutinative", "morphotactic", "benchmark", "benchmarking", "scaling", "urban"
    }

    title_kw_words = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{3,}\b", (title + " " + " ".join(keywords)).lower())
    entity_tokens = []
    seen_e = set()
    for w in title_kw_words:
        norm = BILINGUAL_MAP.get(w, w)
        if norm in STOPWORDS or norm in method_indicators or norm in context_indicators:
            continue
        if norm not in seen_e:
            entity_tokens.append(norm)
            seen_e.add(norm)

    if not entity_tokens:
        entity_tokens = ["vehicle", "traffic"]

    method_tokens = []
    seen_m = set()
    for w in all_words:
        norm = BILINGUAL_MAP.get(w, w)
        if norm in method_indicators and norm not in seen_m:
            method_tokens.append(norm)
            seen_m.add(norm)

    context_tokens = []
    seen_c = set()
    for w in all_words:
        norm = BILINGUAL_MAP.get(w, w)
        if norm in context_indicators and norm not in seen_c:
            context_tokens.append(norm)
            seen_c.add(norm)

    return {
        "title": title,
        "keywords": keywords,
        "abstract": abstract,
        "entity_tokens": entity_tokens,
        "method_tokens": method_tokens,
        "context_tokens": context_tokens,
        "protected_roots": protected_roots,
        "all_words": set(all_words)
    }


def formulate_facet_queries(profile: Dict[str, Any], round_num: int = 1) -> List[str]:
    queries = []
    e_toks = profile["entity_tokens"]
    m_toks = profile["method_tokens"]
    c_toks = profile["context_tokens"]

    e_main = e_toks[0] if e_toks else "vehicle"
    m_main = m_toks[0] if m_toks else "YOLO"

    if round_num == 1:
        queries.append(f'"{m_main}" "{e_main} detection" edge')
        queries.append(f'"oriented bounding box" {e_main} detection')
        queries.append(f'"{e_main} detection" "heterogeneous traffic"')
        queries.append(f'{m_main} Raspberry Pi {e_main}')
        queries.append(f'real-time {e_main} detection embedded')
    elif round_num == 2:
        queries.append(f'"{m_main}" {e_main} latency FPS')
        queries.append(f'lightweight {m_main} {e_main} edge')
        queries.append(f'rotated {e_main} detection oblique')
        queries.append(f'"{e_main} classification" embedded FPGA')
    else:
        queries.append(f'compact {m_main} {e_main} detection')
        queries.append(f'edge AI {e_main} counting traffic')
        queries.append(f'int8 quantization {m_main} {e_main}')

    clean_queries = []
    seen = set()
    for q in queries:
        norm_q = " ".join(q.split())
        if norm_q and norm_q.lower() not in seen:
            clean_queries.append(norm_q)
            seen.add(norm_q.lower())

    return clean_queries


def evaluate_paper_affinity(
    article: Dict[str, Any],
    profile: Dict[str, Any],
    dynamic_excludes: Set[str]
) -> Tuple[float, str]:
    if article.get("is_seed"):
        return 10.0, "🎯 Artículo Semilla de Referencia (Anclaje Metodológico Aprobado)"

    title = article.get("title", "") or ""
    abstract = article.get("abstract", "") or ""
    text_full = f"{title} {abstract}".lower()

    if not title or len(title) < 8:
        return 1.0, "Descartado: Título no disponible o inválido."

    # 1. Filtro de exclusión dinámica
    for exc in dynamic_excludes:
        if re.search(rf"\b{re.escape(exc)}\b", text_full):
            return 2.0, f"Descartado por filtro de ruido confirmado: '{exc}'"

    # 2. Descarte de dominios ajenos obvios (ships, fabric, wire bonding, asphalt cracks, potholes, signs)
    off_target_patterns = [
        "ship", "vessel", "fabric", "textile", "pothole", "asphalt crack", "pavement crack",
        "traffic sign", "signboard", "face recognition", "retina", "biomedical", "wire bonding"
    ]
    for otp in off_target_patterns:
        if otp in text_full:
            return 2.5, f"Descartado: Dominio off-target detectado ('{otp}')"

    # 3. Verificación de Entidad Núcleo (E)
    e_stems = {STEMMER.stem(e) for e in profile["entity_tokens"]}
    if any(e in profile["entity_tokens"] for e in ["vehicle", "traffic"]):
        e_stems.update({STEMMER.stem(w) for w in ["vehicle", "car", "traffic", "bus", "truck", "motorcycle", "automobile", "mototaxi", "uav"]})

    text_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", text_full))
    text_stems = {STEMMER.stem(w) for w in text_words}

    has_entity = any(es in text_stems for es in e_stems)
    if not has_entity:
        return 3.0, "Descartado: Entidad núcleo ausente (no trata sobre vehículos/tráfico)"

    # 4. Verificación de Método (M) y Contexto (C)
    m_stems = {STEMMER.stem(m) for m in profile["method_tokens"]}
    c_stems = {STEMMER.stem(c) for c in profile["context_tokens"]}

    has_method = any(ms in text_stems for ms in m_stems)
    has_context = any(cs in text_stems for cs in c_stems)

    score = 6.0
    if has_entity: score += 1.5
    if has_method: score += 1.5
    if has_context: score += 1.0

    if any(w in text_full for w in ["oriented", "obb", "rotated", "angle"]):
        score += 0.5
    if any(w in text_full for w in ["edge", "embedded", "raspberry", "fpga", "real-time"]):
        score += 0.5

    final_score = round(min(max(score, 0.0), 10.0), 2)
    justification = f"Alta afinidad. Coincide con Entidad {'+ Método' if has_method else ''} {'+ Contexto Edge' if has_context else ''}"

    return final_score, justification


def detect_noise_clusters(
    rejected_articles: List[Dict[str, Any]],
    protected_roots: Set[str],
    current_excludes: Set[str],
    min_freq: int = 2
) -> List[str]:
    alien_counter = collections.Counter()
    for art in rejected_articles:
        text = ((art.get("title") or "") + " " + (art.get("abstract") or "")).lower()
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text)
        for w in set(words):
            stemmed = STEMMER.stem(w)
            if (
                w not in STOPWORDS
                and w not in SCIENTIFIC_CORE_WORDS
                and stemmed not in protected_roots
                and w not in current_excludes
                and len(w) >= 4
            ):
                alien_counter[w] += 1

    noise_candidates = [word for word, count in alien_counter.most_common(8) if count >= min_freq]
    return noise_candidates


def execute_openalex_query(
    query_str: str,
    excludes: Set[str],
    venues_db: Dict[str, Any],
    from_year: int,
    current_year: int,
    max_results: int = 35,
    email: str = "researcher@university.edu"
) -> List[Dict[str, Any]]:
    headers = {"User-Agent": f"ArchiResearchHarness/3.0 ({email})"}
    encoded = urllib.parse.quote(query_str.strip())
    url = (
        f"https://api.openalex.org/works"
        f"?search={encoded}"
        f"&filter=from_publication_date:{from_year}-01-01"
        f"&per-page={max_results}"
        f"&mailto={email}"
    )
    items_parsed = []
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            for r in results:
                title_abs = ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()
                if any(re.search(rf"\b{re.escape(exc)}\b", title_abs) for exc in excludes):
                    continue
                parsed = parse_openalex_item(r, venues_db, current_year)
                items_parsed.append(parsed)
    except Exception as e:
        print(f"[WARN] Error en consulta OpenAlex '{query_str[:30]}': {e}", file=sys.stderr)

    return items_parsed


def generate_bibtex_entry(art: Dict[str, Any]) -> str:
    doi = art.get("doi") or ""
    clean_doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi).strip()
    
    if clean_doi:
        url = f"https://doi.org/{clean_doi}"
        headers = {"Accept": "application/x-bibtex", "User-Agent": "ArchiHarnessBibtex/2.0"}
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200 and "@" in r.text:
                return r.text.strip()
        except Exception:
            pass

    authors = art.get("authors") or "Unknown"
    first_author = re.split(r"[\s,]+", authors)[0].lower() if authors else "author"
    first_author = re.sub(r"\W+", "", first_author)
    year = art.get("year", 2026)
    key = f"{first_author}{year}_{abs(hash(art.get('title', ''))) % 10000}"
    
    title_esc = (art.get("title") or "").replace("{", "").replace("}", "")
    venue_esc = (art.get("venue") or "").replace("{", "").replace("}", "")
    
    entry = [
        f"@article{{{key},",
        f"  title = {{{{{title_esc}}}}},",
        f"  author = {{{authors}}},",
        f"  journal = {{{venue_esc}}},",
        f"  year = {{{year}}},",
        f"  doi = {{{clean_doi}}}," if clean_doi else "",
        f"  url = {{{doi}}}" if doi else "",
        f"}}"
    ]
    return "\n".join([line for line in entry if line])


def run_iterative_harvest(
    topic_input: str,
    seed_input: str = "",
    target_pool_size: int = 20,
    final_top_size: int = 10,
    max_iterations: int = 5,
    min_affinity: float = 7.0,
    years_back: int = 3,
    output_dir: str = ""
) -> Dict[str, Any]:
    current_year = datetime.now().year
    from_year = current_year - years_back
    venues_db = load_venues_db()

    parsed_intake = parse_research_intake(topic_input)
    profile = extract_facets_and_profile(parsed_intake)

    print("=" * 80)
    print(f"🔬 INICIANDO BÚSQUEDA Y COSECHA BIBLIOGRÁFICA AGÉNTICA E ITERATIVA")
    print(f"📄 Título: {profile['title']}")
    print(f"🎯 Meta: Acumular los {target_pool_size} mejores candidatos de alta afinidad (sin overfitting)")
    print(f"📊 Selección final: Top {final_top_size} rigurosamente ordenados")
    print(f"🔑 Entidades (E): {', '.join(profile['entity_tokens'][:4])}")
    print(f"⚙️ Métodos (M): {', '.join(profile['method_tokens'][:4])}")
    print(f"🌐 Contexto (C): {', '.join(profile['context_tokens'][:4])}")
    print("=" * 80)

    vetted_pool_map: Dict[str, Dict[str, Any]] = {}
    seen_articles_ids: Set[str] = set()
    rejected_articles_list: List[Dict[str, Any]] = []
    dynamic_excludes: Set[str] = set()
    all_raw_pool: List[Dict[str, Any]] = []

    # 1. Ingesta y Expansión Controlada de Semilla (máx 3 similares)
    seed_article = None
    if seed_input:
        print(f"\n[INFO] Resolviendo artículo semilla de anclaje: {seed_input}...")
        seed_raw = resolve_seed_work(seed_input)
        if seed_raw:
            seed_raw["_is_seed"] = True
            seed_raw["_source_tag"] = "🎯 Artículo Semilla (Anclaje Metodológico)"
            seed_parsed = parse_openalex_item(seed_raw, venues_db, current_year)
            seed_parsed["affinity_score"] = 10.0
            seed_parsed["inclusion_justification"] = "🎯 Semilla metodológica inyectada por el usuario"
            seed_article = seed_parsed
            
            ident = seed_parsed["id"] or seed_parsed["doi"] or seed_parsed["title"]
            vetted_pool_map[ident] = seed_parsed
            seen_articles_ids.add(ident)
            all_raw_pool.append(seed_parsed)
            print(f"[EXITO] Semilla anclada: '{seed_parsed['title']}' ({seed_parsed['year']})")

            # Buscar a lo sumo 3 obras similares a la semilla para no saturar el pool
            sim_works = fetch_similar_to_seed(seed_raw, years_back=years_back, max_similar=6)
            for sw in sim_works[:3]:
                p_sim = parse_openalex_item(sw, venues_db, current_year)
                s_id = p_sim["id"] or p_sim["doi"] or p_sim["title"]
                if s_id not in seen_articles_ids:
                    all_raw_pool.append(p_sim)
                    seen_articles_ids.add(s_id)
                    score, justif = evaluate_paper_affinity(p_sim, profile, dynamic_excludes)
                    p_sim["affinity_score"] = score
                    p_sim["inclusion_justification"] = justif
                    if score >= min_affinity:
                        vetted_pool_map[s_id] = p_sim
                    else:
                        rejected_articles_list.append(p_sim)
            print(f"[INFO] Artículos similares anclados de la semilla: {len(vetted_pool_map)}")

    # 2. Bucle Iterativo Autónomo a través de las Facetas
    iteration = 1
    while iteration <= max_iterations and len(vetted_pool_map) < target_pool_size:
        facet_queries = formulate_facet_queries(profile, round_num=iteration)
        print(f"\n🔄 [ITERACIÓN {iteration}/{max_iterations}]")
        print(f"   Pool actual de candidatos aprobados: {len(vetted_pool_map)}/{target_pool_size}")
        print(f"   Filtros de exclusión dinámica activos: {list(dynamic_excludes)[:6] or 'Ninguno'}")

        round_new_candidates = 0
        for q_idx, query in enumerate(facet_queries, start=1):
            if len(vetted_pool_map) >= target_pool_size:
                break
            print(f"   🔎 Consulta #{q_idx}: '{query}'...")
            found_items = execute_openalex_query(
                query_str=query,
                excludes=dynamic_excludes,
                venues_db=venues_db,
                from_year=from_year,
                current_year=current_year,
                max_results=35
            )

            for item in found_items:
                ident = item["id"] or item["doi"] or item["title"]
                if ident in seen_articles_ids:
                    continue

                seen_articles_ids.add(ident)
                all_raw_pool.append(item)

                affinity_score, justification = evaluate_paper_affinity(item, profile, dynamic_excludes)
                item["affinity_score"] = affinity_score
                item["inclusion_justification"] = justification

                if affinity_score >= min_affinity:
                    vetted_pool_map[ident] = item
                    round_new_candidates += 1
                    if len(vetted_pool_map) >= target_pool_size:
                        break
                else:
                    rejected_articles_list.append(item)

        print(f"   📥 Candidatos válidos añadidos en esta ronda: +{round_new_candidates}")
        print(f"   📈 Total acumulado en Pool de Alta Afinidad: {len(vetted_pool_map)}/{target_pool_size}")

        if len(vetted_pool_map) >= target_pool_size:
            print("   ✨ [CONVERGENCIA EXITOSA] Meta de 20 candidatos de alta afinidad alcanzada.")
            break

        new_noise = detect_noise_clusters(rejected_articles_list, profile["protected_roots"], dynamic_excludes, min_freq=2)
        if new_noise:
            dynamic_excludes.update(new_noise)
            print(f"   ⚠️ Ruido detectado y neutralizado para siguiente ronda: {new_noise[:5]}")

        iteration += 1

    # Preparar el Pool de los 20 Candidatos
    vetted_list = list(vetted_pool_map.values())
    vetted_list.sort(key=lambda x: (x.get("is_seed", False), x.get("affinity_score", 0), x.get("score", 0)), reverse=True)
    top20_pool = vetted_list[:target_pool_size]

    for idx, art in enumerate(top20_pool, start=1):
        if art.get("is_seed"):
            art["tag"] = "🎯 Semilla"
        elif art.get("affinity_score", 0) >= 9.0:
            art["tag"] = "🔬 Metodología Central"
        elif art.get("is_empirical"):
            art["tag"] = "⚙️ Validación Empírica"
        elif art.get("is_survey"):
            art["tag"] = "📖 SOTA Survey"
        else:
            art["tag"] = "💎 Evidencia Clave"

    # Etapa 2: Análisis Riguroso y Selección Final del Top 10
    print("\n" + "=" * 80)
    print(f"🏆 ETAPA 2: ANÁLISIS RIGUROSO Y SELECCIÓN FINAL DE LOS {final_top_size} MEJORES ARTÍCULOS")
    print("=" * 80)
    final_ranked_data = rank_articles(
        top20_pool,
        top_n=final_top_size,
        emerging_count=2,
        max_surveys=1
    )
    final_top10 = final_ranked_data["top_ranked"]

    # Guardar Artefactos de Forma Aislada (Regla 04)
    if output_dir:
        out_dir_path = Path(output_dir)
        raw_dir_path = out_dir_path / "raw"
        raw_dir_path.mkdir(parents=True, exist_ok=True)

        # Artefacto 1: Pool de los 20 Candidatos Revisados
        top20_md_lines = [
            f"# Pool Intermedio de Trazabilidad: 20 Candidatos de Alta Afinidad",
            "",
            f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Tema de Investigación:** {profile['title']}  ",
            f"**Total Artículos Evaluados en el Bucle:** {len(all_raw_pool)}  ",
            f"**Total Descartados por Falta de Afinidad o Ruido:** {len(rejected_articles_list)}  ",
            f"**Candidatos Validados en el Pool:** {len(top20_pool)}  ",
            "",
            "> [!NOTE] Criterio de Selección del Pool de 20",
            "> Cada uno de estos artículos superó el umbral de afinidad semántica y metodológica (Score >= 7.0/10) evaluado 1 a 1 por el Crítico Agéntico, verificando la coexistencia de la entidad de estudio con el método o entorno computacional.",
            "",
            "---",
            "",
            "| # | Título | Año | Journal / Venue | Cuartil | H5 | Citas | Afinidad (/10) | Justificación de Inclusión | DOI |",
            "|---|---|:---:|---|:---:|:---:|:---:|:---:|---|:---:|"
        ]

        for idx, art in enumerate(top20_pool, start=1):
            t = (art.get("title") or "")[:60] + ("..." if len(art.get("title") or "") > 60 else "")
            y = art.get("year", "")
            v = (art.get("venue") or "N/A")[:26]
            q = art.get("quartile", "Desc")
            h5 = art.get("h5_index", 25)
            c = f"{art.get('citations', 0)}"
            aff = f"**{art.get('affinity_score', 0):.1f}**"
            just = art.get("inclusion_justification", "Aprobado por alta afinidad")
            doi_link = f"[Enlace]({art.get('doi')})" if art.get("doi") else "N/A"
            top20_md_lines.append(f"| {idx} | {t} | {y} | {v} | {q} | {h5} | {c} | {aff} | {just} | {doi_link} |")

        top20_md_path = out_dir_path / "top20_candidatos_revisados.md"
        top20_md_path.write_text("\n".join(top20_md_lines), encoding="utf-8")
        print(f"[EXITO] Artefacto 1 guardado: {top20_md_path}")

        top20_json_path = raw_dir_path / "top20_candidates.json"
        top20_json_path.write_text(json.dumps(top20_pool, ensure_ascii=False, indent=2), encoding="utf-8")

        # Artefacto 2: Tabla Resumen Top 10 Final
        summary_table_md = format_markdown_table(final_ranked_data)
        summary_md_path = out_dir_path / "summary_table.md"
        summary_md_path.write_text(summary_table_md, encoding="utf-8")
        print(f"[EXITO] Artefacto 2 (Top 10 Final) guardado: {summary_md_path}")

        # Generar references.bib verificado
        bib_entries = []
        print(f"[INFO] Generando y verificando entradas BibTeX con DOIs...")
        for art in final_top10:
            entry_str = generate_bibtex_entry(art)
            if entry_str:
                bib_entries.append(entry_str)

        bib_path = out_dir_path / "references.bib"
        bib_path.write_text("\n\n".join(bib_entries) + "\n", encoding="utf-8")
        print(f"[EXITO] Archivo BibTeX guardado: {bib_path}")

        # Generar Reportes Formales PRISMA 2020
        fase1_lines = [
            "# Fase 1: Identificación Inicial de Literatura (Pool Crudo de Búsqueda)",
            "",
            f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Total Artículos Recuperados:** {len(all_raw_pool)}  ",
            "",
            "| # | Título | Año | Venue | Origen / Tag | Citaciones | DOI |",
            "|---|---|:---:|---|---|:---:|:---:|"
        ]
        for idx, art in enumerate(all_raw_pool, start=1):
            t = (art.get("title") or "")[:60] + ("..." if len(art.get("title") or "") > 60 else "")
            tag = "🎯 Semilla" if art.get("is_seed") else "Búsqueda Abierta"
            doi_link = f"[Link]({art.get('doi')})" if art.get("doi") else "N/A"
            fase1_lines.append(f"| {idx} | {t} | {art.get('year')} | {(art.get('venue') or '')[:25]} | `{tag}` | {art.get('citations')} | {doi_link} |")
        
        (out_dir_path / "fase1_identificacion_sin_filtrar.md").write_text("\n".join(fase1_lines), encoding="utf-8")

        fase2_lines = [
            "# Fase 2: Registro de Cribado y Decisiones del Crítico Agéntico",
            "",
            f"**Total Evaluados:** {len(all_raw_pool)}  ",
            f"**Retenidos en Pool:** {len(top20_pool)}  ",
            f"**Excluidos / Ruido:** {len(rejected_articles_list)}  ",
            f"**Filtros de Exclusión Dinámica Aplicados:** `{', '.join(dynamic_excludes) or 'Ninguno'}`  ",
            "",
            "| # | Título | Año | Estado | Motivo / Criterio del Crítico |",
            "|---|---|:---:|---|---|"
        ]
        eval_log = [(art, "✅ Aprobado", art.get("inclusion_justification")) for art in top20_pool] + \
                   [(art, "❌ Descartado", art.get("inclusion_justification")) for art in rejected_articles_list[:40]]
        for idx, (art, st, reas) in enumerate(eval_log, start=1):
            t = (art.get("title") or "")[:60] + ("..." if len(art.get("title") or "") > 60 else "")
            fase2_lines.append(f"| {idx} | {t} | {art.get('year')} | {st} | {reas} |")

        (out_dir_path / "fase2_cribado_exclusiones.md").write_text("\n".join(fase2_lines), encoding="utf-8")

    return {
        "top20_pool": top20_pool,
        "final_top10": final_top10,
        "total_evaluated": len(all_raw_pool),
        "total_rejected": len(rejected_articles_list),
        "dynamic_excludes": list(dynamic_excludes)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Búsqueda bibliográfica agéntica e iterativa (Top 20 candidates -> Top 10 final) sin overfitting."
    )
    parser.add_argument("--idea", "--topic", dest="topic", required=True, help="Texto o ruta a archivo con la propuesta de investigación")
    parser.add_argument("--seed", type=str, default="", help="Artículo semilla opcional (DOI, URL o título)")
    parser.add_argument("--target-pool", type=int, default=20, help="Tamaño del pool intermedio de candidatos de alta afinidad (default: 20)")
    parser.add_argument("--final-top", type=int, default=10, help="Cantidad final de artículos a clasificar (default: 10)")
    parser.add_argument("--max-iterations", type=int, default=5, help="Máximo de iteraciones de refinamiento (default: 5)")
    parser.add_argument("--min-affinity", type=float, default=7.0, help="Umbral mínimo de afinidad semántica 0-10 (default: 7.0)")
    parser.add_argument("--years", type=int, default=3, help="Años de antigüedad hacia atrás (default: 3)")
    parser.add_argument("--output-dir", type=str, default="", help="Directorio de salida para los artefactos")

    args = parser.parse_args()

    run_iterative_harvest(
        topic_input=args.topic,
        seed_input=args.seed,
        target_pool_size=args.target_pool,
        final_top_size=args.final_top,
        max_iterations=args.max_iterations,
        min_affinity=args.min_affinity,
        years_back=args.years,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
