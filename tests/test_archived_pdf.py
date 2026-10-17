"""Le PDF exact est accepté sans transformer sa lecture en consultation primaire fraîche."""
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import archived_pdf
import live_sources
import campaign


class ArchivedPDFTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = Path(__file__).parent / 'rapports/rgpd-2026-10-14'
        self.pdf = 'CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf'
        self.index = 'articles-rgpd.json'
        shutil.copy2(source / self.pdf, self.root / self.pdf)
        shutil.copy2(source / self.index, self.root / self.index)
        self.traces = archived_pdf.archived_pdf_consultations(
            self.root, self.pdf, self.index,
            ['A-06', 'B-05', 'B-06', 'B-09', 'B-11'], '2026-10-12')

    def test_exact_pdf_accepted_for_all_five_rgpd_case_links(self):
        self.assertEqual(len(self.traces), 5)
        for trace in self.traces:
            self.assertEqual(live_sources.verify_trace(trace, self.root), [])
            case = {'id': trace['case_id'], 'required_source_ids': [archived_pdf.SOURCE_ID]}
            self.assertEqual(campaign.validate_evidence([trace], [case], 'integration', 'live', self.root), [])

    def test_modified_pdf_rejected_even_when_declared_hash_is_recomputed(self):
        p = self.root / self.pdf
        p.write_bytes(p.read_bytes() + b'altered')
        trace = self.traces[0]
        self.assertTrue(live_sources.verify_trace(trace, self.root))
        tampered = {**trace, 'raw_response_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        self.assertTrue(any('empreinte PDF' in p for p in live_sources.verify_trace(tampered, self.root)))

    def test_modified_index_rejected_even_with_updated_declared_hash(self):
        p = self.root / self.index
        p.write_bytes(p.read_bytes() + b' ')
        trace = {**self.traces[0], 'excerpt_index_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        self.assertTrue(live_sources.verify_trace(trace, self.root))

    def test_wrong_celex_url_endpoint_and_version_rejected(self):
        for field, value in [('source_id', 'CELEX:wrong'), ('source_url', 'https://eur-lex.europa.eu/wrong'),
                             ('source_url', archived_pdf.SOURCE_URL.replace('https:', 'http:')),
                             ('endpoint', 'https'), ('version_or_date', 'Consultation primaire actuelle')]:
            with self.subTest(field=field, value=value):
                self.assertTrue(live_sources.verify_trace({**self.traces[0], field: value}, self.root))

    def test_unapproved_case_and_incomplete_or_forged_excerpts_rejected(self):
        for field, value in [('case_id', 'A-01'), ('case_id', []), ('article_numbers', [5]),
                             ('supporting_excerpt', 'Inventé'), ('article_number', '5')]:
            with self.subTest(field=field):
                self.assertTrue(live_sources.verify_trace({**self.traces[0], field: value}, self.root))

    def test_rejects_pdf_and_index_paths_outside_evidence_root(self):
        for field in ['raw_response_file', 'excerpt_index_file']:
            self.assertTrue(live_sources.verify_trace({**self.traces[0], field: '../outside'}, self.root))
            self.assertTrue(live_sources.verify_trace({**self.traces[0], field: str((self.root / self.pdf).resolve())}, self.root))

    def test_rejects_claim_of_fresh_primary_download_or_invented_hour(self):
        for field, value in [('consultation_scope', 'fresh-primary-download'),
                             ('primary_consulted_on', '2026-10-16'),
                             ('primary_consulted_at', self.traces[0]['consulted_at']),
                             ('primary_provenance', 'verified-primary-today')]:
            self.assertTrue(live_sources.verify_trace({**self.traces[0], field: value}, self.root))

    def test_local_read_timestamp_still_obeys_age_limit(self):
        trace = self.traces[0]
        at = datetime.fromisoformat(trace['consulted_at'])
        self.assertEqual(live_sources.verify_trace(trace, self.root, as_of=at + timedelta(hours=1)), [])
        self.assertTrue(any('périmée' in p for p in live_sources.verify_trace(trace, self.root, as_of=at + timedelta(hours=25))))
        self.assertTrue(any('future' in p for p in live_sources.verify_trace(trace, self.root, as_of=at - timedelta(hours=1))))

    def test_context_exposes_archive_read_and_unknown_primary_hour(self):
        text = live_sources.source_context([self.traces[0]])
        self.assertIn('Lecture locale d’un PDF archivé', text)
        self.assertIn('2026-10-14, heure inconnue', text)
        self.assertIn('aucun nouveau téléchargement ni contrôle de vigueur actuelle', text)

    def test_evidence_schema_declares_pdf_metadata(self):
        schema = json.loads((Path(__file__).parent / 'evidence.schema.json').read_text(encoding='utf-8'))
        props = schema['properties']['consultations']['items']['properties']
        self.assertIn('archived_pdf', props['kind']['enum'])
        self.assertIn('archive/pdf', props['endpoint']['enum'])
        self.assertEqual(set(self.traces[0]) - set(props), set())
