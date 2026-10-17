#!/usr/bin/env python3
"""Mesure la taille des contextes DRH complets et sélectifs par cas."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import context_loader


ROOT = Path(__file__).resolve().parent.parent


def measure(mode: str) -> dict:
    bundle = (ROOT / "drh-fpt-bundle-pour-LLM.md").read_text(encoding="utf-8")
    full_bytes = len(bundle.encode("utf-8"))
    cases = json.loads((ROOT / "tests/cas-de-test.json").read_text(encoding="utf-8"))
    active = [case for case in cases if mode in case.get("modes", ["integration", "degraded"])]
    rows = []
    for case in active:
        text, files = context_loader.build_case_context(case)
        selective = len(text.encode("utf-8"))
        rows.append(
            {
                "id": case["id"], "full_bytes": full_bytes,
                "selective_bytes": selective,
                "reduction_percent": round((1 - selective / full_bytes) * 100, 1),
                "files": files,
            }
        )
    return {
        "mode": mode, "cases": rows, "full_bytes": full_bytes,
        "mean_selective_bytes": round(statistics.mean(row["selective_bytes"] for row in rows)),
        "median_selective_bytes": round(statistics.median(row["selective_bytes"] for row in rows)),
        "mean_reduction_percent": round(statistics.mean(row["reduction_percent"] for row in rows), 1),
    }


def markdown(report: dict) -> str:
    lines = [
        "# Mesure déterministe des contextes DRH-FPT\n",
        f"Mode : `{report['mode']}`. Cette mesure porte sur les octets UTF-8 du contexte DRH, pas sur les tokens facturés par un fournisseur.\n",
        f"- Bundle complet : **{report['full_bytes']} octets**",
        f"- Contexte sélectif moyen : **{report['mean_selective_bytes']} octets**",
        f"- Contexte sélectif médian : **{report['median_selective_bytes']} octets**",
        f"- Réduction moyenne : **{report['mean_reduction_percent']} %**\n",
        "| Cas | Complet | Sélectif | Réduction |",
        "|---|---:|---:|---:|",
    ]
    for row in report["cases"]:
        lines.append(
            f"| {row['id']} | {row['full_bytes']} | {row['selective_bytes']} | {row['reduction_percent']} % |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("integration", "degraded"), default="integration")
    parser.add_argument("--json")
    parser.add_argument("--markdown")
    args = parser.parse_args()
    report = measure(args.mode)
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown:
        Path(args.markdown).write_text(markdown(report), encoding="utf-8")
    if not args.json and not args.markdown:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
