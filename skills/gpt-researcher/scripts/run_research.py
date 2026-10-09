#!/usr/bin/env python3
"""
run_research.py
Wrapper para ejecutar investigaciones web autónomas usando el motor gpt-researcher.
Soporta búsqueda con DuckDuckGo (gratuita), Tavily, y genera reportes con citas web.
"""

import sys
import asyncio
import argparse
from pathlib import Path
from gpt_researcher import GPTResearcher

async def run_gpt_research(query: str, report_type: str = "research_report") -> str:
    researcher = GPTResearcher(query=query, report_type=report_type)
    await researcher.conduct_research()
    report = await researcher.write_report()
    return report

def main():
    parser = argparse.ArgumentParser(description="Ejecutar investigación web profunda con gpt-researcher")
    parser.add_argument("--query", required=True, help="Consulta u objetivo de investigación")
    parser.add_argument("--type", default="research_report", choices=["research_report", "detailed_report", "outline_report"], help="Tipo de reporte")
    parser.add_argument("--output", default="", help="Ruta para guardar el informe en Markdown")

    args = parser.parse_args()

    print(f"[INFO] Iniciando investigación web para: {args.query}")
    try:
        report = asyncio.run(run_gpt_research(args.query, args.type))
        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(report, encoding="utf-8")
            print(f"[EXITO] Reporte guardado en: {out_p}")
        else:
            print(report)
    except Exception as e:
        print(f"[ERROR] Error durante la investigación: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
