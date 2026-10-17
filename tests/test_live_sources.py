"""Preuves officielles : lecture effective, version et intégrité du corpus."""
import json
import tempfile
import unittest
from pathlib import Path
import live_sources
from datetime import datetime,timezone,timedelta


class LiveSourceTests(unittest.TestCase):
    def test_primary_title_matching_accepts_uppercase_law_and_deduplicates_same_cid(self):
        title={'title':'LOI n° 2010-1330 du 9 novembre 2010 portant réforme des retraites','cid':'LEGITEXT-fixture'}
        search={'results':[{'titles':[title,title,{'title':'LOI n° 2010-13301 du 9 novembre 2010','cid':'wrong'}]}]}
        self.assertEqual(live_sources.matching_text_ids({'query':'2010-1330'},search),['LEGITEXT-fixture'])

    def test_partial_collection_checkpoints_decision_and_structure_before_next_failure(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        import sys
        for kind in ['decision','consolidated_structure']:
            decision={'text':{'id':'CETATEXT-fixture','titre':'Décision','texte':'Motifs officiels','dateTexte':0}}
            structure={'cid':'LEGITEXT-fixture','title':'Structure','dateDebutVersion':0,'dateFinVersion':32472144000000,'sections':[]}
            def api(endpoint,request,token):
                if request.get('textId')=='BROKEN':raise ValueError('fixture interruption')
                return decision if endpoint=='/consult/juri' else structure
            fake=SimpleNamespace(load_dotenv=lambda:None,get_token=lambda:'fixture',api_call=api,LegifranceError=RuntimeError,
                                 _epoch_ms=lambda d:int(datetime.fromisoformat(d).replace(tzinfo=timezone.utc).timestamp()*1000))
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp)
                manifest={'reference_date':'2026-10-12','sources':[
                    {'key':'first','kind':kind,'text_id':'CETATEXT-fixture' if kind=='decision' else 'LEGITEXT-fixture','cases':{'A01':[]}},
                    {'key':'broken','text_id':'BROKEN','cases':{'A01':['1']}}]}
                with patch.dict(sys.modules,{'legifrance':fake}):
                    with self.assertRaisesRegex(ValueError,'fixture interruption'):
                        live_sources.collect(manifest,root/'legal',root/'out')
                path=root/'out/evidence.json'
                self.assertTrue(path.exists(),'consultation réussie non enregistrée avant échec suivant')
                self.assertEqual(len(json.loads(path.read_text(encoding='utf8'))['consultations']),1)
    def test_primary_european_publication_host_is_allowed_for_rgpd(self):
        self.assertIn('eur-lex.europa.eu',live_sources.OFFICIAL_PAGE_HOSTS)
    def test_structure_preserves_an_article_with_no_reported_number(self):
        raw={'title':'Décret CST','articles':[{'num':None,'id':'LEGIARTI-fixture','etat':'ABROGE',
              'dateDebut':None,'dateFin':None}]}
        text=live_sources.structure_text(raw)
        self.assertIn('numéro non renseigné',text)
        self.assertIn('LEGIARTI-fixture',text)
        self.assertIn('ABROGE',text)
    def test_numeric_dates_before_1970_are_portable(self):
        instant=datetime(1962,7,11,tzinfo=timezone.utc)
        epoch=datetime(1970,1,1,tzinfo=timezone.utc)
        self.assertEqual(live_sources.date_value((instant-epoch).total_seconds()*1000),instant)

    def test_structure_preserves_unreported_section_dates_without_inventing_them(self):
        raw={'title':'Décret','sections':[{'title':'Chapitre abrogé','etat':'ABROGE',
            'dateDebut':None,'dateFin':None}]}
        self.assertIn('non renseigné',live_sources.structure_text(raw))

    def test_consolidated_structure_proves_repeal_and_checks_archive(self):
        raw={'cid':'LEGITEXT123','title':'Décret disciplinaire','dateDebutVersion':0,
            'dateFinVersion':32472144000000,'sections':[{'title':'Conseils de recours',
            'etat':'ABROGE','dateDebut':0,'dateFin':1607558400000,'articles':[]}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            trace=live_sources.archive_structure_consultation(root,'structure',
                {'textId':'LEGITEXT123','date':1791676800000},raw,['29'],'2026-10-11')[0]
            self.assertIn('ABROGE',trace['supporting_excerpt'])
            self.assertIn('2020-12-10',trace['supporting_excerpt'])
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            self.assertTrue(live_sources.verify_trace({**trace,'supporting_excerpt':'Inventé'},root))
            self.assertTrue(live_sources.verify_trace({**trace,'request':{'textId':'LEGITEXT123','date':0}},root))

    def test_official_html_keeps_visible_law_and_removes_script_style_head(self):
        body='<html><head><style>.cache{}</style><title>Navigation</title></head><body><script>secret()</script><p>Règle &amp; condition</p><p>Exception importante</p></body></html>'
        self.assertEqual(live_sources.official_page_text(body),'Règle & condition Exception importante')
        self.assertEqual(live_sources.official_page_text('<nav>Menu</nav><main><p>Règle</p><p>Exception</p></main><footer>Liens</footer>'),'Règle Exception')

    def test_official_html_trace_rejects_unknown_extractor(self):
        import gzip,hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);at=datetime.now(timezone.utc).isoformat();url='https://www.cnil.fr/fr/texte'
            raw={'url':url,'status':200,'body':'<style>inutile</style><p>Texte officiel</p>','consulted_at':at}
            archive=root/'raw.gz';archive.write_bytes(gzip.compress(json.dumps(raw).encode()))
            trace={'kind':'official_page','source_url':url,'source_id':url,'consulted_at':at,
                'version_or_date':'Page consultée le '+at,'supporting_excerpt':'Texte officiel',
                'raw_response_file':archive.name,'raw_response_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                'endpoint':'https','request':{'url':url},'excerpt_extractor':'visible-html-v1'}
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            self.assertTrue(live_sources.verify_trace({**trace,'excerpt_extractor':'unknown'},root))
            self.assertTrue(live_sources.verify_trace({**trace,'supporting_excerpt':'Faux'},root))

    def test_source_specific_date_preserves_historical_comparison(self):
        manifest={'reference_date':'2026-10-11'}
        self.assertEqual(live_sources.reference_date_for_source(manifest,{}),'2026-10-11')
        self.assertEqual(live_sources.reference_date_for_source(manifest,{'reference_date':'2004-01-01'}),'2004-01-01')
        with self.assertRaises(ValueError):
            live_sources.reference_date_for_source(manifest,{'reference_date':'bad'})

    def test_official_page_requires_allowed_host_and_https(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); import gzip,hashlib
            at=datetime.now(timezone.utc).isoformat(); url='https://www.cnil.fr/fr/texte'
            raw={'url':url,'status':200,'body':'Texte officiel','consulted_at':at}
            path=root/'raw.json.gz';path.write_bytes(gzip.compress(json.dumps(raw).encode()))
            trace={'kind':'official_page','source_url':url,'source_id':url,'consulted_at':at,
                   'version_or_date':'Page consultée le '+at,'supporting_excerpt':'Texte officiel',
                   'raw_response_file':path.name,'raw_response_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                   'endpoint':'https','request':{'url':url}}
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            self.assertTrue(live_sources.verify_trace({**trace,'source_url':url.replace('https:','http:')},root))
            self.assertTrue(live_sources.verify_trace({**trace,'source_url':'https://example.com/texte'},root))

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


    def test_article_number_is_preserved_verified_and_rendered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            raw={'title':'Code officiel','articles':[{'id':'LEGIARTI123','num':'L714-13',
                'etat':'VIGUEUR','content':'Texte officiel','dateDebut':0,
                'dateFin':32472144000000}]}
            trace=live_sources.archive_consultation(root,'number','/consult/legiPart',
                {'textId':'CODE','date':1791676800000},raw,['L714-13'],['07'],'2026-10-11')[0]
            self.assertEqual(trace['article_number'],'L714-13')
            self.assertIn('Article L714-13',live_sources.source_context([trace]))
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            legacy={k:v for k,v in trace.items() if k!='article_number'}
            self.assertEqual(live_sources.verify_trace(legacy,root),[])
            for bad in ['L714-14','',42]:
                self.assertTrue(live_sources.verify_trace({**trace,'article_number':bad},root))

    def test_journal_article_number_is_checked_against_raw(self):
        import gzip,hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);at=datetime.now(timezone.utc).isoformat()
            raw={'cid':'JORFTEXT123','dateParution':1791676800000,
                'articles':[{'id':'JORFARTI123','num':'94','content':'Publication officielle'}]}
            archive=root/'journal.gz'
            archive.write_bytes(gzip.compress(json.dumps(raw).encode(),mtime=0))
            trace={'kind':'jorf','case_id':'29','source_id':'JORFARTI123',
                'source_url':'https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI123',
                'consulted_at':at,'reference_date':'2026-10-11',
                'version_or_date':'Publication au JORF le 2026-10-11',
                'supporting_excerpt':'Publication officielle','endpoint':'/consult/jorf',
                'request':{'textCid':'JORFTEXT123'},'raw_response_file':archive.name,
                'raw_response_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                'article_number':'94'}
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            self.assertTrue(live_sources.verify_trace({**trace,'article_number':'95'},root))
            legacy={k:v for k,v in trace.items() if k!='article_number'}
            self.assertEqual(live_sources.verify_trace(legacy,root),[])

    def test_non_article_trace_cannot_invent_article_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            raw={'cid':'LEGITEXT123','title':'Structure','dateDebutVersion':0,
                'dateFinVersion':32472144000000,'sections':[]}
            trace=live_sources.archive_structure_consultation(root,'structure',
                {'textId':'LEGITEXT123','date':1791676800000},raw,['29'],'2026-10-11')[0]
            self.assertEqual(live_sources.verify_trace(trace,root),[])
            self.assertTrue(live_sources.verify_trace({**trace,'article_number':'94'},root))


if __name__ == '__main__':
    unittest.main()
