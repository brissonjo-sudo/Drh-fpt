"""Preuves officielles : lecture effective, version et intégrité du corpus."""
import json
import tempfile
import unittest
from pathlib import Path
import live_sources
from datetime import datetime,timezone,timedelta


class LiveSourceTests(unittest.TestCase):
    def test_extracts_nested_current_articles_not_repealed_ones(self):
        raw = {'title': 'Texte officiel', 'articles': [], 'sections': [
            {'articles': [{'id': 'LEGIARTI123', 'num': '2', 'etat': 'VIGUEUR',
                           'content': '<p>Règle &amp; condition</p>',
                           'dateDebut': 1719619200000, 'dateFin': 32472144000000},
                          {'id': 'LEGIARTI456', 'num': '3', 'etat': 'ABROGE',
                           'content': 'Ancien texte', 'dateDebut': 0, 'dateFin': 1}]}]}
        records = live_sources.extract_articles(raw, ['2'], '2026-10-11')
        self.assertEqual(records[0]['text'], 'Règle & condition')
        self.assertEqual(records[0]['id'], 'LEGIARTI123')
        with self.assertRaises(ValueError):
            live_sources.extract_articles(raw, ['3'], '2026-10-11')

    def test_rejects_future_or_expired_article_even_if_label_says_vigueur(self):
        raw = {'articles': [{'id': 'LEGIARTI123', 'num': '2', 'etat': 'VIGUEUR',
                            'content': 'Texte', 'dateDebut': 1893456000000,
                            'dateFin': 32472144000000}]}
        with self.assertRaises(ValueError):
            live_sources.extract_articles(raw, ['2'], '2026-10-11')

    def test_archive_integrity_and_excerpt_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = {'title': 'Officiel', 'articles': [{'id': 'LEGIARTI123', 'num': '2',
                'etat': 'VIGUEUR', 'content': '<p>Règle officielle</p>',
                'dateDebut': 1719619200000, 'dateFin': 32472144000000}]}
            trace = live_sources.archive_consultation(root, 'source', '/consult/legiPart',
                {'textId': 'OFFICIAL', 'date': 1791676800000}, raw, ['2'], ['01'],
                '2026-10-11')[0]
            self.assertEqual(live_sources.verify_trace(trace, root), [])
            trace['supporting_excerpt'] = 'Texte inventé'
            self.assertTrue(live_sources.verify_trace(trace, root))
            (root / trace['raw_response_file']).write_bytes(b'{}')
            self.assertTrue(any('empreinte' in p for p in live_sources.verify_trace(trace, root)))

    def test_rejects_archive_path_outside_evidence_directory(self):
        problems = live_sources.verify_trace({'raw_response_file': '../secret.json'}, Path.cwd())
        self.assertTrue(problems)

    def test_malformed_url_and_timestamp_are_failures(self):
        for trace in ({'source_url': 42, 'consulted_at': 42}, {'consulted_at': 42}):
            self.assertTrue(live_sources.verify_trace(trace, Path.cwd()))

    def test_transitional_notes_are_preserved(self):
        raw = {'articles': [{'id': 'LEGIARTI123', 'num': '2', 'etat': 'VIGUEUR',
              'content': 'Règle', 'nota': '<p>Application différée en 2029</p>',
              'dateDebut': 0, 'dateFin': 32472144000000}]}
        self.assertIn('Application différée en 2029', live_sources.extract_articles(raw, ['2'], '2026-10-11')[0]['text'])

    def test_archival_review_uses_campaign_date_not_current_time(self):
        at=datetime(2020,1,1,tzinfo=timezone.utc)
        trace={'source_url':'https://www.legifrance.gouv.fr/x','consulted_at':at.isoformat()}
        self.assertFalse(any('périmée' in p for p in live_sources.verify_trace(trace,Path.cwd(),as_of=at+timedelta(hours=1))))
        self.assertTrue(any('périmée' in p for p in live_sources.verify_trace(trace,Path.cwd())))

    def test_respondent_sources_do_not_include_judge_conclusions(self):
        trace = {'source_url': 'https://www.legifrance.gouv.fr/x', 'source_id': 'LEGIARTI123',
            'version_or_date': '2026-10-11', 'consulted_at': '2026-10-11T10:00:00Z',
            'supporting_excerpt': 'Texte officiel', 'conclusion_supported': 'Réponse attendue secrète'}
        context = live_sources.source_context([trace])
        self.assertIn('Texte officiel', context)
        self.assertNotIn('Réponse attendue secrète', context)


if __name__ == '__main__':
    unittest.main()
