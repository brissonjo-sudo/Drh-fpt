"""Consultation locale du PDF RGPD figé, distincte d'un téléchargement primaire."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SOURCE_ID = 'CELEX:02016R0679-20160504'
SOURCE_URL = 'https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:02016R0679-20160504'
PDF_SHA256 = 'e5984442f70f842034f9b5cb39bf3d6137630252260830c07b0449f354faa718'
INDEX_SHA256 = 'e38cac70ace13cc3e2eaada83a7bc731a81615c6236710a43983ec39ab627a21'
VERSION = 'Consolidation du 2016-05-04 (PDF archivé)'


def confined_file(root: Path, relative: str) -> Path:
    """Refuser un chemin absolu ou résolu hors du dossier de preuve."""
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError('chemin de preuve PDF invalide')
    path = Path(relative)
    resolved = (root / path).resolve()
    if path.is_absolute() or not resolved.is_relative_to(root.resolve()):
        raise ValueError('preuve PDF hors du dossier de preuve')
    return resolved


def checked_index(root: Path, relative: str) -> dict:
    """Lier les extraits historiques à l'index immuable déjà relu, sans extraction nouvelle."""
    data = confined_file(root, relative).read_bytes()
    if hashlib.sha256(data).hexdigest() != INDEX_SHA256:
        raise ValueError('empreinte de l’index PDF différente de la référence figée')
    index = json.loads(data)
    if index.get('source_id') != SOURCE_ID:
        raise ValueError('identifiant de l’index PDF incohérent')
    return index


def case_excerpt(index: dict, case_id: str) -> tuple[list[int], str]:
    """Restituer tous les articles prévus pour ce cas, avec leurs empreintes propres."""
    numbers = index['case_articles'].get(case_id)
    if not numbers:
        raise ValueError('cas sans liaison PDF RGPD autorisée')
    texts = []
    for number in numbers:
        article = index['articles'][str(number)]
        text = article['text']
        if hashlib.sha256(text.encode('utf-8')).hexdigest() != article['text_sha256']:
            raise ValueError('empreinte d’extrait PDF différente')
        texts.append(text)
    return numbers, '\n\n'.join(texts)


def verify_pdf_trace(trace: dict, root: Path, data: bytes) -> None:
    """Vérifier l'identité PDF/index et le cas, sans certifier la vigueur actuelle."""
    if hashlib.sha256(data).hexdigest() != PDF_SHA256 or trace.get('raw_response_sha256') != PDF_SHA256:
        raise ValueError('empreinte PDF différente de la référence figée')
    if trace.get('source_id') != SOURCE_ID or trace.get('source_url') != SOURCE_URL:
        raise ValueError('identifiant ou URL PDF incohérent')
    if trace.get('consultation_scope') != 'local-archive-read':
        raise ValueError('portée de consultation PDF absente ou trompeuse')
    if (trace.get('primary_consulted_on') != '2026-10-14'
            or trace.get('primary_consulted_at') is not None
            or 'primary_consulted_at' not in trace
            or trace.get('primary_provenance') != 'reported-by-Claude'):
        raise ValueError('provenance primaire PDF différente ou heure inventée')
    case_id = trace.get('case_id')
    if not isinstance(case_id, str):
        raise ValueError('identifiant de cas PDF invalide')
    if trace.get('endpoint') != 'archive/pdf' or trace.get('request') != {
            'source_id': SOURCE_ID, 'pdf_sha256': PDF_SHA256, 'case_id': case_id}:
        raise ValueError('requête de lecture PDF incohérente')
    if trace.get('version_or_date') != VERSION:
        raise ValueError('version du PDF archivé incohérente')
    reference = trace.get('reference_date')
    if not isinstance(reference, str) or datetime.fromisoformat(reference).date().isoformat() != reference:
        raise ValueError('date de référence PDF invalide')
    index = checked_index(root, trace.get('excerpt_index_file'))
    if trace.get('excerpt_index_sha256') != INDEX_SHA256:
        raise ValueError('empreinte déclarée de l’index PDF incohérente')
    numbers, text = case_excerpt(index, case_id)
    if trace.get('article_numbers') != numbers or trace.get('supporting_excerpt') != text:
        raise ValueError('articles ou extrait différents du PDF indexé pour le cas')


def archived_pdf_consultations(root: Path, pdf_file: str, index_file: str,
                               case_ids: list[str], reference_date: str) -> list[dict]:
    """Lire l'archive maintenant ; conserver la provenance primaire rapportée et sa limite."""
    data = confined_file(root, pdf_file).read_bytes()
    index = checked_index(root, index_file)
    at = datetime.now(timezone.utc).isoformat()
    traces = []
    for case_id in case_ids:
        numbers, text = case_excerpt(index, case_id)
        trace = {'kind': 'archived_pdf', 'case_id': case_id, 'source_id': SOURCE_ID,
                 'source_title': 'RGPD — dispositif consolidé EUR-Lex archivé',
                 'source_url': SOURCE_URL, 'consulted_at': at,
                 'consultation_scope': 'local-archive-read',
                 'primary_consulted_on': '2026-10-14', 'primary_consulted_at': None,
                 'primary_provenance': 'reported-by-Claude', 'reference_date': reference_date,
                 'version_or_date': VERSION, 'supporting_excerpt': text,
                 'conclusion_supported': 'Dispositif archivé à analyser dans son champ ; vigueur actuelle non certifiée par cette lecture locale',
                 'endpoint': 'archive/pdf',
                 'request': {'source_id': SOURCE_ID, 'pdf_sha256': PDF_SHA256, 'case_id': case_id},
                 'raw_response_file': pdf_file, 'raw_response_sha256': PDF_SHA256,
                 'excerpt_index_file': index_file, 'excerpt_index_sha256': INDEX_SHA256,
                 'article_numbers': numbers}
        verify_pdf_trace(trace, root, data)
        traces.append(trace)
    return traces
