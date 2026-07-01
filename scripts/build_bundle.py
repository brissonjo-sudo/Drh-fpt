#!/usr/bin/env python3
"""
Régénère drh-fpt-bundle-pour-LLM.md à partir des sources du dépôt
(SKILL.md + references/ + assets/fiche-profil-collectivite.md).

Le bundle est un fichier consolidé destiné au portage sur d'autres LLM
(instructions système en un seul bloc). Il était auparavant maintenu à la
main en parallèle des sources et avait déjà divergé deux fois : ce script
est la source unique de régénération.

Usage :
    python3 scripts/build_bundle.py            # régénère le bundle sur disque
    python3 scripts/build_bundle.py --check    # vérifie la fraîcheur (exit 1 si divergent)
    python3 scripts/build_bundle.py --package  # régénère + produit dist/*.skill et dist/*.md

Sans dépendance externe (bibliothèque standard uniquement).
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SKILL_MD = ROOT / "SKILL.md"
BUNDLE_PATH = ROOT / "drh-fpt-bundle-pour-LLM.md"
PREAMBLE_TEMPLATE = SCRIPTS / "bundle-preambule.md"
DIST = ROOT / "dist"

SEP = "=" * 80

# Ordre exact des sections du bundle, tel qu'observé dans
# drh-fpt-bundle-pour-LLM.md : SKILL.md, socle, paramètres, fiche profil,
# puis les huit branches (routeur §7 de SKILL.md).
SECTIONS = [
    ("RÈGLES DE CONDUITE (SKILL)", SKILL_MD),
    ("SOCLE — SOURCES & VÉRIFICATION", ROOT / "references/socle-sources-verification.md"),
    ("PARAMÈTRES & STATUTS PARTICULIERS", ROOT / "references/parametres-collectivite.md"),
    ("FICHE PROFIL (cadrage d'ouverture)", ROOT / "assets/fiche-profil-collectivite.md"),
    ("BRANCHE — Carrière & paie", ROOT / "references/carriere-paie.md"),
    ("BRANCHE — QVT & santé", ROOT / "references/qvt-sante.md"),
    ("BRANCHE — Recrutement & formation", ROOT / "references/recrutement-formation.md"),
    ("BRANCHE — CST & dialogue social", ROOT / "references/cst-dialogue-social.md"),
    ("BRANCHE — SI RH & masse salariale", ROOT / "references/si-rh-masse-salariale.md"),
    ("BRANCHE — Communication interne", ROOT / "references/communication-interne.md"),
    ("BRANCHE — Agents contractuels", ROOT / "references/contractuels.md"),
    ("BRANCHE — Statut : garanties, déontologie & signalements", ROOT / "references/statut-garanties.md"),
]

# Exclu du bundle (documenté dans le préambule) : gabarits de livrables
# assets/*-modele.md, méta-gabarit references/_gabarit-branche.md, tests/.


def read_version() -> str:
    """Lit la version dans le YAML d'en-tête de SKILL.md (source de vérité)."""
    text = SKILL_MD.read_text(encoding="utf-8")
    m = re.search(r"^\s*version:\s*(\S+)\s*$", text, re.MULTILINE)
    if not m:
        sys.exit("Version introuvable dans le YAML de SKILL.md (clé 'version:').")
    return m.group(1)


def build_bundle_text(version: str) -> str:
    preamble = PREAMBLE_TEMPLATE.read_text(encoding="utf-8").replace("{{VERSION}}", version)

    parts = [preamble, "\n", SEP, "\n"]
    for label, path in SECTIONS:
        content = path.read_text(encoding="utf-8")
        parts.append("\n")
        parts.append(SEP)
        parts.append(f"\n### SOURCE : {label}\n")
        parts.append(SEP)
        parts.append("\n\n")
        parts.append(content)

    return "".join(parts)


def do_check(bundle_text: str) -> int:
    if not BUNDLE_PATH.exists():
        print(f"ERREUR : {BUNDLE_PATH} n'existe pas.")
        return 1
    current = BUNDLE_PATH.read_text(encoding="utf-8")
    if current == bundle_text:
        print("OK : le bundle est à jour (identique aux sources).")
        return 0
    diff = difflib.unified_diff(
        current.splitlines(keepends=True),
        bundle_text.splitlines(keepends=True),
        fromfile="drh-fpt-bundle-pour-LLM.md (disque)",
        tofile="drh-fpt-bundle-pour-LLM.md (régénéré)",
    )
    diff_lines = list(diff)
    print("ERREUR : le bundle est PÉRIMÉ par rapport aux sources. Diff résumé :\n")
    for line in diff_lines[:200]:
        sys.stdout.write(line)
    if len(diff_lines) > 200:
        print(f"\n... ({len(diff_lines) - 200} lignes de diff supplémentaires tronquées)")
    print(
        "\nRégénère avec : python3 scripts/build_bundle.py"
    )
    return 1


def do_package(version: str, bundle_text: str) -> None:
    DIST.mkdir(exist_ok=True)

    # dist/drh-fpt-bundle-v{version}.md — copie du bundle
    bundle_copy = DIST / f"drh-fpt-bundle-v{version}.md"
    bundle_copy.write_text(bundle_text, encoding="utf-8")

    # dist/drh-fpt-v{version}.skill — archive zip d'un dossier drh-fpt/
    skill_archive = DIST / f"drh-fpt-v{version}.skill"
    top_level_files = ["SKILL.md", "README.md", "CHANGELOG.md", "JOURNAL.md", "LICENSE"]
    dirs_to_include = ["references", "assets"]

    with zipfile.ZipFile(skill_archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in top_level_files:
            src = ROOT / name
            if src.exists():
                zf.write(src, arcname=f"drh-fpt/{name}")
        for dirname in dirs_to_include:
            src_dir = ROOT / dirname
            for f in sorted(src_dir.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(ROOT)
                    zf.write(f, arcname=f"drh-fpt/{rel.as_posix()}")

    print(f"Package produit : {skill_archive.relative_to(ROOT)}")
    print(f"Bundle copié     : {bundle_copy.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check", action="store_true",
        help="ne réécrit pas le bundle ; compare au bundle sur disque et sort en erreur (1) s'ils diffèrent",
    )
    ap.add_argument(
        "--package", action="store_true",
        help="régénère le bundle puis produit dist/drh-fpt-v{version}.skill et dist/drh-fpt-bundle-v{version}.md",
    )
    args = ap.parse_args()

    version = read_version()
    bundle_text = build_bundle_text(version)

    if args.check:
        return do_check(bundle_text)

    BUNDLE_PATH.write_text(bundle_text, encoding="utf-8")
    print(f"Bundle régénéré : {BUNDLE_PATH.relative_to(ROOT)} (v{version})")

    if args.package:
        do_package(version, bundle_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
