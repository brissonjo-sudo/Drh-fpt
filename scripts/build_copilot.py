#!/usr/bin/env python3
"""
Prépare l'agent Microsoft 365 Copilot (Agent Builder) à partir des sources
du skill : convertit les références Markdown en fiches .docx numérotées
(Agent Builder n'accepte pas le .md en fichier de connaissance) et contrôle
la limite de 8 000 caractères des instructions.

Usage :
    python scripts/build_copilot.py           # génère copilot/connaissances/*.docx
    python scripts/build_copilot.py --check   # contrôle seulement (instructions, sources, résidus)

Dépendance : python-docx.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPILOT = ROOT / "copilot"
OUT = COPILOT / "connaissances"
MAX_INSTRUCTIONS = 8000
MAX_FILES = 20

# (numéro, titre, sources concaténées dans l'ordre, nom de fichier)
FICHES = [
    ("01", "Contrat d'exécution", ["references/contrat-execution.md"], "contrat-execution"),
    ("02", "Sources et vérification", ["references/socle-sources-verification.md"], "sources-verification"),
    ("03", "Paramètres de la collectivité et fiche profil",
     ["references/parametres-collectivite.md", "assets/fiche-profil-collectivite.md"], "parametres-collectivite"),
    ("04", "Gabarits de livrables",
     ["assets/decision-modele.md", "assets/deliberation-modele.md", "assets/courrier-modele.md",
      "assets/note-modele.md", "assets/procedure-modele.md"], "gabarits-livrables"),
    ("05", "Carrière et paie : règles communes", ["references/carriere-paie.md"], "carriere-paie-regles-communes"),
    ("06", "Carrière : statut, carrière et discipline",
     ["references/carriere-paie/statut-discipline.md"], "carriere-statut-discipline"),
    ("07", "Carrière : rémunération, régime indemnitaire et paie",
     ["references/carriere-paie/remuneration-paie.md"], "carriere-remuneration-paie"),
    ("08", "Carrière : temps de travail et fin de fonctions",
     ["references/carriere-paie/temps-fin-fonctions.md"], "carriere-temps-fin-fonctions"),
    ("09", "QVT et santé", ["references/qvt-sante.md"], "qvt-sante"),
    ("10", "Recrutement et formation", ["references/recrutement-formation.md"], "recrutement-formation"),
    ("11", "CST et dialogue social", ["references/cst-dialogue-social.md"], "cst-dialogue-social"),
    ("12", "SI RH et masse salariale", ["references/si-rh-masse-salariale.md"], "si-rh-masse-salariale"),
    ("13", "Communication interne", ["references/communication-interne.md"], "communication-interne"),
    ("14", "Agents contractuels", ["references/contractuels.md"], "contractuels"),
    ("15", "Statut : garanties, déontologie et signalements", ["references/statut-garanties.md"], "statut-garanties"),
    ("16", "Restitution proportionnée", ["references/restitution-proportionnee.md"], "restitution-proportionnee"),
]
# Exclus, comme dans le bundle : méta-gabarit _gabarit-branche.md, registre de
# maintenance cache-plafonds-regime-indemnitaire.md, assets/README.md.

PATH_TO_FICHE = {src: f"{num} ({title})" for num, title, srcs, _ in FICHES for src in srcs}

# Remplacements textuels pour retirer la mécanique propre à Claude.
# Ordre : du plus spécifique au plus général.
SUBSTITUTIONS = [
    (r"du skill(\s*(?:\n>\s*)?)`recherche-juridique`", r"de la\1recherche sur les sites officiels"),
    (r"`recherche-juridique(?:\s*>=\s*[\d.]+)?`", "la recherche sur les sites officiels"),
    (r"recherche-juridique", "la recherche sur les sites officiels"),
    (r"Si le compagnon est absent ou indisponible", "Si la recherche sur les sites officiels est impossible"),
    (r"Dans la co-activation, le compagnon", "Lors de la vérification, la recherche officielle"),
    (r"La demande de clarification du compagnon", "Une demande de clarification liée à la recherche"),
    (r"\bdu compagnon\b", "de la recherche officielle"),
    (r"\ble compagnon\b", "la recherche officielle"),
    (r"\bLe compagnon\b", "La recherche officielle"),
    # « l'agent » désigne le fonctionnaire en FPT : l'outil est « l'assistant ».
    (r"la matrice du `SKILL\.md`", "la matrice de vérification des instructions de l'assistant"),
    (r"\(matrice §2\.2 du SKILL\.md\)", "(matrice de vérification des instructions de l'assistant)"),
    (r"\(SKILL\.md §2\.2\)", "(instructions de l'assistant)"),
    (r"SKILL\.md §6\.1", "instructions de l'assistant, profil de la collectivité"),
    (r"`?SKILL\.md`?", "instructions de l'assistant"),
    (r"\bPérimètre du skill\b", "Périmètre de l'assistant"),
    (r"\bdu skill\b", "de l'assistant"),
    (r"\bce skill\b", "cet assistant"),
    (r"\ble skill\b", "l'assistant"),
    (r"\bLe skill\b", "L'assistant"),
    (r"PROFIL COLLECTIVITÉ — drh-fpt", "PROFIL COLLECTIVITÉ"),
    (r"`assets/`", "la fiche DRH-FPT 04 (Gabarits de livrables)"),
    (r"`references/cache-plafonds-regime-indemnitaire\.md`", "le registre de maintenance (non fourni à l'assistant)"),
]

PERSISTANCE_COPILOT = """## Modes de persistance

- **Recoller (par défaut)** : copier le bloc ci-dessus et le coller au début de
  chaque nouvelle conversation avec l'assistant.
- **Mémoire Copilot** : si la mémoire de Microsoft 365 Copilot est activée,
  l'utilisateur peut demander de mémoriser le profil.

"""

RESIDUS = re.compile(r"\bskill\b|Claude|SKILL\.md|compagnon|recherche-juridique|references/|assets/", re.I)


def adapt(text: str, src: str) -> str:
    """Adapte une source Markdown au contexte Copilot."""
    if src == "assets/fiche-profil-collectivite.md":
        text = re.sub(r"## Modes de persistance.*?(?=## )", PERSISTANCE_COPILOT, text, flags=re.S)
    # Renvois vers d'autres fichiers → numéro de fiche.
    def repl_path(m: re.Match) -> str:
        path = m.group(1)
        if path in PATH_TO_FICHE:
            return f"la fiche DRH-FPT {PATH_TO_FICHE[path]}"
        return m.group(0)
    text = re.sub(r"`?((?:references|assets)/[\w/.-]+\.md)`?", repl_path, text)
    for pattern, new in SUBSTITUTIONS:
        text = re.sub(pattern, new, text)
    return text


# --- Rendu Markdown → docx (sous-ensemble utilisé par le dépôt) -------------

INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*\s][^*]*\*|\[[^\]]+\]\([^)]+\))")


def add_inline(par, text: str) -> None:
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            par.add_run(part[2:-2]).bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = par.add_run(part[1:-1])
            run.font.name = "Consolas"
        elif part.startswith("[") and "](" in part:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part).groups()
            par.add_run(f"{label} ({url})")
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            par.add_run(part[1:-1]).italic = True
        else:
            par.add_run(part)


def render(doc, md: str) -> None:
    from docx.shared import Pt

    lines = md.splitlines()
    i = 0
    para_buf: list[str] = []

    def flush():
        if para_buf:
            add_inline(doc.add_paragraph(), " ".join(s.strip() for s in para_buf))
            para_buf.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                p = doc.add_paragraph()
                run = p.add_run(lines[i])
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                p.paragraph_format.space_after = Pt(0)
                i += 1
            i += 1
            continue

        if not stripped or re.fullmatch(r"-{3,}|={3,}", stripped):
            flush()
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", stripped)
        if m:
            flush()
            level = min(len(m.group(1)) + 1, 4)  # le titre 1 est réservé au titre de la fiche
            doc.add_heading(re.sub(r"[*`]", "", m.group(2)), level=level)
            i += 1
            continue

        if stripped.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                table = doc.add_table(rows=len(rows), cols=ncol)
                table.style = "Table Grid"
                for r, cells in enumerate(rows):
                    for c, cell in enumerate(cells):
                        p = table.cell(r, c).paragraphs[0]
                        add_inline(p, cell)
                        if r == 0:
                            for run in p.runs:
                                run.bold = True
            continue

        if stripped.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            add_inline(doc.add_paragraph(style="Quote"), " ".join(q for q in quote if q))
            continue

        m = re.match(r"(\s*)([-*+]|\d+[.)])\s+(.*)", line)
        if m:
            flush()
            indent = len(m.group(1).replace("\t", "    "))
            numbered = m.group(2)[0].isdigit()
            item = [m.group(3)]
            i += 1
            # Lignes de continuation indentées.
            while i < len(lines) and lines[i].strip() and lines[i].startswith(" ") \
                    and not re.match(r"\s*([-*+]|\d+[.)])\s+", lines[i]):
                item.append(lines[i].strip())
                i += 1
            style = "List Number" if numbered else "List Bullet"
            if indent >= 2:
                style += " 2"
            text = " ".join(item)
            if numbered:
                text = f"{m.group(2)} {text}"
                style = "List Bullet 2" if indent >= 2 else "Normal"
            add_inline(doc.add_paragraph(style=style), text)
            continue

        para_buf.append(line)
        i += 1
    flush()


def build_fiche(num: str, title: str, sources: list[str], slug: str, version: str) -> Path:
    from docx import Document

    doc = Document()
    full_title = f"DRH-FPT {num} — {title}"
    doc.core_properties.title = full_title
    doc.core_properties.subject = f"Base de connaissance de l'assistant DRH-FPT (skill v{version})"
    doc.add_heading(full_title, level=1)
    doc.add_paragraph(
        f"Fiche de connaissance de l'assistant DRH-FPT, issue du skill v{version}. "
        "Les montants, délais et seuils sont des repères de recherche : "
        "les confirmer sur la source officielle avant usage."
    ).italic = True
    for src in sources:
        text = adapt((ROOT / src).read_text(encoding="utf-8"), src)
        render(doc, text)
    path = OUT / f"DRH-FPT-{num}-{slug}.docx"
    doc.save(path)
    return path


def read_version() -> str:
    m = re.search(r"^\s*version:\s*(\S+)\s*$", (ROOT / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "?"


def check() -> int:
    errors = 0
    # Version générale et variantes locales (copilot/<collectivité>/instructions.md).
    for path in sorted(COPILOT.rglob("instructions.md")):
        n = len(path.read_text(encoding="utf-8"))
        print(f"Instructions {path.relative_to(ROOT).as_posix()} : {n} / {MAX_INSTRUCTIONS} caractères")
        if n > MAX_INSTRUCTIONS:
            print("ERREUR : instructions trop longues pour Agent Builder.")
            errors += 1
    if len(FICHES) > MAX_FILES:
        print(f"ERREUR : {len(FICHES)} fiches, limite {MAX_FILES}.")
        errors += 1
    for num, _, sources, _ in FICHES:
        for src in sources:
            path = ROOT / src
            if not path.exists():
                print(f"ERREUR : source manquante {src}")
                errors += 1
                continue
            for ln, line in enumerate(adapt(path.read_text(encoding="utf-8"), src).splitlines(), 1):
                if RESIDUS.search(line):
                    print(f"RÉSIDU fiche {num} ({src}:{ln}) : {line.strip()[:110]}")
    print(f"Fiches : {len(FICHES)} / {MAX_FILES} (place libre pour {MAX_FILES - len(FICHES)} documents locaux)")
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="contrôle sans générer")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    status = check()
    if args.check or status:
        return status
    version = read_version()
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("DRH-FPT-*.docx"):
        old.unlink()
    for num, title, sources, slug in FICHES:
        path = build_fiche(num, title, sources, slug, version)
        print(f"Généré : {path.relative_to(ROOT)} ({path.stat().st_size // 1024} Ko)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
