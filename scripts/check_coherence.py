#!/usr/bin/env python3
"""
Vérifie la cohérence du dépôt drh-fpt (version, fraîcheur du bundle,
CHANGELOG, renvois de fichiers, arbre README, contenu du noyau versionné).
Sans dépendance externe.

Utilisable en CI ou en pre-commit :
    python3 scripts/check_coherence.py

Code de sortie : 0 si tout est cohérent (avertissements tolérés),
1 si au moins une erreur bloquante est détectée.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bundle as bb  # noqa: E402

SKILL_MD = ROOT / "SKILL.md"
README_MD = ROOT / "README.md"
CHANGELOG_MD = ROOT / "CHANGELOG.md"
BUNDLE = ROOT / "drh-fpt-bundle-pour-LLM.md"

# Fichiers dont une modification change le comportement du skill chargé.
# Le bundle en est dérivé : il est exclu (contrôlé séparément en 2).
NOYAU = ("SKILL.md", "references", "assets")

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# --- 1. Version unique -------------------------------------------------

def check_version_unique() -> None:
    skill_text = SKILL_MD.read_text(encoding="utf-8")

    m_yaml = re.search(r"^\s*version:\s*(\S+)\s*$", skill_text, re.MULTILINE)
    if not m_yaml:
        error("SKILL.md : version introuvable dans le YAML (clé 'version:').")
        return
    v_yaml = m_yaml.group(1)

    m_title = re.search(r"^# Skill : drh-fpt \(v([\d.]+)\)\s*$", skill_text, re.MULTILINE)
    if not m_title:
        error("SKILL.md : titre '# Skill : drh-fpt (vX.Y.Z)' introuvable.")
        return
    v_title = m_title.group(1)

    if v_yaml != v_title:
        error(
            f"Version incohérente dans SKILL.md : YAML={v_yaml} vs titre={v_title}."
        )

    if not BUNDLE.exists():
        error(f"{BUNDLE.name} introuvable : impossible de vérifier sa version.")
        return
    bundle_text = BUNDLE.read_text(encoding="utf-8")

    m_header = re.search(
        r"^# \(portage du skill Claude « drh-fpt » v([\d.]+)\)\s*$", bundle_text, re.MULTILINE
    )
    if not m_header:
        error("Bundle : en-tête 'portage du skill Claude « drh-fpt » vX.Y.Z' introuvable.")
    else:
        v_header = m_header.group(1)
        if v_header != v_yaml:
            error(
                f"Version incohérente : en-tête du bundle={v_header} vs YAML SKILL.md={v_yaml}."
            )

    m_yaml_in_bundle = re.search(r"^\s*version:\s*(\S+)\s*$", bundle_text, re.MULTILINE)
    if not m_yaml_in_bundle:
        error("Bundle : YAML de SKILL.md (avec 'version:') introuvable dans le bundle.")
    elif m_yaml_in_bundle.group(1) != v_yaml:
        error(
            f"Version incohérente : YAML dans le bundle={m_yaml_in_bundle.group(1)} "
            f"vs YAML SKILL.md={v_yaml}."
        )

    m_title_in_bundle = re.search(
        r"^# Skill : drh-fpt \(v([\d.]+)\)\s*$", bundle_text, re.MULTILINE
    )
    if not m_title_in_bundle:
        error("Bundle : titre '# Skill : drh-fpt (vX.Y.Z)' introuvable dans le bundle.")
    elif m_title_in_bundle.group(1) != v_yaml:
        error(
            f"Version incohérente : titre dans le bundle={m_title_in_bundle.group(1)} "
            f"vs YAML SKILL.md={v_yaml}."
        )

    if not errors:
        print(f"[OK] Version unique et cohérente partout : v{v_yaml}")


# --- 2. Fraîcheur du bundle ---------------------------------------------

def check_bundle_freshness() -> None:
    version = bb.read_version()
    regenerated = bb.build_bundle_text(version)
    if not BUNDLE.exists():
        error(f"{BUNDLE.name} introuvable.")
        return
    current = BUNDLE.read_text(encoding="utf-8")
    if current != regenerated:
        error(
            f"{BUNDLE.name} est périmé par rapport aux sources "
            "(voir 'python3 scripts/build_bundle.py --check' pour le diff)."
        )
    else:
        print("[OK] Bundle à jour par rapport aux sources.")


# --- 3. CHANGELOG --------------------------------------------------------

def check_changelog() -> None:
    version = bb.read_version()
    if not CHANGELOG_MD.exists():
        error("CHANGELOG.md introuvable.")
        return
    text = CHANGELOG_MD.read_text(encoding="utf-8")
    pattern = r"^## \[" + re.escape(version) + r"\]"
    if not re.search(pattern, text, re.MULTILINE):
        error(f"CHANGELOG.md : aucune entrée '## [{version}]' pour la version courante.")
    else:
        print(f"[OK] CHANGELOG.md contient une entrée pour v{version}.")


# --- 4. Renvois (references/xxx.md, assets/xxx.md) ----------------------

def check_references() -> None:
    pattern = re.compile(r"`((?:references|assets)/[A-Za-z0-9_.\-]+\.md)`")
    missing = []
    checked = 0
    for src in (SKILL_MD, README_MD):
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        for m in pattern.finditer(text):
            rel = m.group(1)
            checked += 1
            if not (ROOT / rel).exists():
                missing.append(f"{src.name} référence '{rel}' introuvable sur disque.")
    if missing:
        for msg in missing:
            error(msg)
    else:
        print(f"[OK] Tous les renvois references/assets vérifiés existent ({checked} occurrences).")


# --- 5. Arbre README (avertissement seulement) ---------------------------

def check_readme_tree() -> None:
    if not README_MD.exists():
        warn("README.md introuvable : impossible de vérifier l'arbre de structure.")
        return
    readme_text = README_MD.read_text(encoding="utf-8")

    m = re.search(r"## Structure\s*```(.*?)```", readme_text, re.DOTALL)
    if not m:
        warn("README.md : bloc 'Structure' introuvable, vérification de l'arbre ignorée.")
        return
    tree_block = m.group(1)

    excluded_dirs = {"dist", "resultats"}
    tracked = []
    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(ROOT)
        parts = rel.parts
        if any(p in excluded_dirs for p in parts) or ".git" in parts:
            continue
        if f.suffix == ".md" or f.name == "LICENSE":
            tracked.append(rel.as_posix())

    missing_from_tree = [p for p in tracked if Path(p).name not in tree_block]
    if missing_from_tree:
        for p in sorted(missing_from_tree):
            warn(f"README.md : '{p}' n'apparaît pas dans le bloc Structure.")
    else:
        print(f"[OK] Tous les fichiers .md/LICENSE suivis apparaissent dans le bloc Structure du README ({len(tracked)} fichiers).")


# --- 6. Noyau modifié ⇒ version incrémentée ------------------------------

def _git(*args: str) -> str | None:
    """Renvoie la sortie standard de la commande git, ou None si elle échoue."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _parse_version(raw: str) -> tuple[int, ...] | None:
    parts = raw.split(".")
    if not all(p.isdigit() for p in parts):
        return None
    return tuple(int(p) for p in parts)


def check_noyau_versionne() -> None:
    """Interdit de livrer un noyau modifié sous un numéro de version déjà publié.

    Le contrôle 1 garantit que la version est la même partout ; il ne dit rien
    du fait qu'elle ait été incrémentée quand le contenu a changé. Sans ce
    garde-fou, un skill au comportement modifié continue de se déclarer sous
    l'ancien numéro, et les campagnes de test ne sont plus datables.
    """
    version = bb.read_version()

    if _git("rev-parse", "--git-dir") is None:
        warn(
            "Dépôt Git indisponible : contrôle « noyau modifié ⇒ version "
            "incrémentée » ignoré."
        )
        return

    tag = next(
        (
            candidate
            for candidate in (f"v{version}", version)
            if _git("rev-parse", "--verify", "--quiet", f"refs/tags/{candidate}^{{}}")
            is not None
        ),
        None,
    )
    if tag is None:
        warn(
            f"Aucun tag 'v{version}' trouvé : contrôle « noyau modifié ⇒ version "
            "incrémentée » ignoré (clone superficiel ou version jamais publiée)."
        )
        return

    # Tag comparé à l'arbre de travail : les modifications non encore
    # committées comptent autant que les autres.
    diff = _git("diff", "--name-only", tag, "--", *NOYAU)
    untracked = _git("ls-files", "--others", "--exclude-standard", "--", *NOYAU)
    if diff is None or untracked is None:
        warn(f"Comparaison avec le tag {tag} impossible : contrôle ignoré.")
        return

    changed = sorted(
        {line for line in (diff + untracked).splitlines() if line.strip()}
    )
    if not changed:
        print(f"[OK] Noyau identique au tag {tag} : version v{version} légitime.")
        return

    text = CHANGELOG_MD.read_text(encoding="utf-8") if CHANGELOG_MD.exists() else ""
    m = re.search(r"^## \[Non publié\](?:\s*—\s*v([\d.]+))?", text, re.MULTILINE)
    if not m:
        apercu = ", ".join(changed[:5]) + (" …" if len(changed) > 5 else "")
        error(
            f"Noyau modifié depuis le tag {tag} ({len(changed)} fichier(s) : "
            f"{apercu}) alors que SKILL.md déclare toujours v{version}. "
            "Incrémenter la version ou ouvrir une entrée '## [Non publié]' "
            "dans CHANGELOG.md qui décrive ces modifications."
        )
        return

    prochaine = m.group(1)
    if prochaine is None:
        warn(
            "CHANGELOG.md : l'entrée '## [Non publié]' ne précise pas la version "
            "cible ; préférer '## [Non publié] — vX.Y.Z'."
        )
    else:
        v_courante = _parse_version(version)
        v_prochaine = _parse_version(prochaine)
        if v_courante is None or v_prochaine is None:
            warn(
                f"Version non numérique (courante={version}, non publiée="
                f"{prochaine}) : comparaison ignorée."
            )
        elif v_prochaine <= v_courante:
            error(
                f"CHANGELOG.md : l'entrée non publiée vise v{prochaine}, qui n'est "
                f"pas postérieure à la version déclarée v{version}."
            )
    print(
        f"[OK] Noyau modifié depuis {tag} ({len(changed)} fichier(s)), couvert "
        "par une entrée '## [Non publié]' du CHANGELOG."
    )


def main() -> int:
    check_version_unique()
    check_bundle_freshness()
    check_changelog()
    check_references()
    check_readme_tree()
    check_noyau_versionne()

    print()
    if warnings:
        print(f"AVERTISSEMENTS ({len(warnings)}) :")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\nERREURS ({len(errors)}) :")
        for e in errors:
            print(f"  - {e}")
        print("\nÉCHEC : incohérences bloquantes détectées.")
        return 1

    print("\nOK : aucune incohérence bloquante" + (f" ({len(warnings)} avertissement(s))." if warnings else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
