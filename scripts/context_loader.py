#!/usr/bin/env python3
"""Construit un contexte DRH complet ou ciblé à partir des sources du dépôt."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEP = "=" * 80

CORE_FILES = (
    "SKILL.md",
    "references/contrat-execution.md",
    "references/socle-sources-verification.md",
    "references/parametres-collectivite.md",
    "references/restitution-proportionnee.md",
)

CONTEXT_FILES = {
    "parametres-collectivite": ("references/parametres-collectivite.md",),
    "carriere-paie": ("references/carriere-paie.md",),
    "carriere-statut-discipline": ("references/carriere-paie/statut-discipline.md",),
    "carriere-remuneration-paie": ("references/carriere-paie/remuneration-paie.md",),
    "carriere-temps-fin-fonctions": ("references/carriere-paie/temps-fin-fonctions.md",),
    "qvt-sante": ("references/qvt-sante.md",),
    "recrutement-formation": ("references/recrutement-formation.md",),
    "cst-dialogue-social": ("references/cst-dialogue-social.md",),
    "si-rh-masse-salariale": ("references/si-rh-masse-salariale.md",),
    "communication-interne": ("references/communication-interne.md",),
    "contractuels": ("references/contractuels.md",),
    "statut-garanties": ("references/statut-garanties.md",),
}

DELIVERABLE_ASSETS = {
    "decision": "assets/decision-modele.md",
    "décision": "assets/decision-modele.md",
    "délibération": "assets/deliberation-modele.md",
    "deliberation": "assets/deliberation-modele.md",
    "courrier": "assets/courrier-modele.md",
    "note": "assets/note-modele.md",
    "procédure": "assets/procedure-modele.md",
    "procedure": "assets/procedure-modele.md",
    "profil": "assets/fiche-profil-collectivite.md",
}


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def files_for_case(case: dict) -> list[str]:
    """Retourne les sources nécessaires à un cas en mode sélectif."""
    files = list(CORE_FILES)
    context_keys = case.get("contextes")
    if not isinstance(context_keys, list) or not context_keys:
        raise ValueError(f"{case.get('id', 'cas inconnu')} : champ contextes absent")
    for key in context_keys:
        if key not in CONTEXT_FILES:
            raise ValueError(f"{case.get('id', 'cas inconnu')} : contexte inconnu {key!r}")
        for rel in CONTEXT_FILES[key]:
            _append_unique(files, rel)

    requested = " ".join(
        str(case.get(field, "")) for field in ("prompt", "livrable")
    ).lower()
    for needle, rel in DELIVERABLE_ASSETS.items():
        if needle in requested:
            _append_unique(files, rel)
    return files


def build_context(files: list[str], root: Path = ROOT) -> str:
    """Assemble les fichiers en conservant leur provenance lisible."""
    chunks = []
    for rel in files:
        path = root / rel
        if not path.is_file():
            raise FileNotFoundError(f"Source de contexte introuvable : {rel}")
        chunks.extend(
            (
                f"\n{SEP}\n",
                f"### SOURCE DRH : {rel}\n",
                f"{SEP}\n\n",
                path.read_text(encoding="utf-8"),
            )
        )
    return "".join(chunks)


def build_case_context(case: dict, root: Path = ROOT) -> tuple[str, list[str]]:
    files = files_for_case(case)
    return build_context(files, root), files


def context_metrics(text: str, files: list[str]) -> dict:
    return {
        "fichiers": files,
        "octets_utf8": len(text.encode("utf-8")),
        "caracteres": len(text),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
