import tempfile
import unittest
from pathlib import Path
import native_runtime
import claude_cli
import json


class NativeRuntimeTests(unittest.TestCase):
    def test_explicit_organizational_exemption_has_no_fabricated_source_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);drh=base/'drh';drh.mkdir();(drh/'SKILL.md').write_text('DRH')
            companion=base/'companion';companion.mkdir();(companion/'SKILL.md').write_text('LEGAL')
            with self.assertRaises(ValueError):
                native_runtime.stage(base/'required',drh,'integration','A01',[],companion)
            runtime=native_runtime.stage(base/'exempt',drh,'integration','A01',[],companion,proof_required=False)
            self.assertNotIn('sources/official.md',runtime['files'])
            self.assertIn('.claude/skills/recherche-juridique/SKILL.md',runtime['files'])
            case={'prompt':'Préparer un échange interne','contextes':['communication-interne'],'preuve_requise':False}
            self.assertNotIn('sources/official.md',native_runtime.prompt(case,'integration'))
            import release_gate
            required=release_gate.native_required_files(case,'integration')
            self.assertIn('.claude/skills/drh-fpt/references/contrat-execution.md',required)
            self.assertNotIn('sources/official.md',required)
            self.assertIn('sources/official.md',release_gate.native_required_files({**case,'preuve_requise':True},'integration'))
    def test_stage_only_runtime_and_current_case_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);drh=base/'drh';drh.mkdir()
            (drh/'SKILL.md').write_text('DRH')
            (drh/'references').mkdir();(drh/'references'/'legal.md').write_text('règle')
            (drh/'tests').mkdir();(drh/'tests'/'cases.json').write_text('secret-barème')
            (drh/'.env').write_text('secret-auth')
            companion=base/'companion';companion.mkdir();(companion/'SKILL.md').write_text('LEGAL')
            trace={'case_id':'A01','source_id':'id','source_title':'Titre',
                   'source_url':'https://www.legifrance.gouv.fr/ceta/id/id',
                   'consulted_at':'2026-10-12T00:00:00+00:00','reference_date':'2026-10-12',
                   'version_or_date':'2024','supporting_excerpt':'source',
                   'conclusion_supported':'à confronter'}
            runtime=native_runtime.stage(base/'native',drh,'integration','A01',[trace],companion)
            files=runtime['files']
            self.assertIn('.claude/skills/drh-fpt/SKILL.md',files)
            self.assertIn('.claude/skills/recherche-juridique/SKILL.md',files)
            self.assertFalse(any('cases.json' in x or '.env' in x for x in files))
            self.assertIn('sources/official.md',files)
            self.assertIn('.claude-plugin/plugin.json',files)
            self.assertEqual(runtime['plugin']['name'],'drh-eval')
            self.assertIn('drh-eval:drh-fpt',runtime['skills'])
            with self.assertRaises(ValueError):
                native_runtime.stage(base/'wrong',drh,'integration','A02',[trace],companion)

    def test_degraded_no_companion_no_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);drh=base/'drh';drh.mkdir();(drh/'SKILL.md').write_text('DRH')
            runtime=native_runtime.stage(base/'native',drh,'degraded','A01',[])
            self.assertNotIn('recherche-juridique',runtime['skills'])
            self.assertNotIn('sources/official.md',runtime['files'])

    def test_native_prompt_does_not_inject_contract_or_rubrics(self):
        case={'id':'x','prompt':'Question RH','attendus':['SECRET']}
        prompt=native_runtime.prompt(case,'integration')
        self.assertIn('drh-eval:drh-fpt',prompt)
        self.assertFalse(prompt.startswith('/'))
        self.assertNotIn('SECRET',prompt)
        self.assertNotIn('Rappel final',prompt)
        self.assertNotIn('qualifier →',prompt)
        self.assertIn('Utilise aussi le skill drh-eval:recherche-juridique',prompt)

    def test_archive_keeps_signature_and_replays_old_absolute_read_paths(self):
        from test_claude_cli import stream, MODEL
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);drh=base/'drh';drh.mkdir();(drh/'SKILL.md').write_text('DRH')
            runtime=native_runtime.stage(base/'native',drh,'degraded','A01',[])
            archived=native_runtime.archive(runtime,base/'archive')
            self.assertEqual(native_runtime.signature(runtime),native_runtime.signature(archived))
            raw=stream({'type':'tool_use','id':'r','name':'Read','input':{'file_path':str(base/'native/.claude/skills/drh-fpt/SKILL.md')}},plugins=[{'name':'drh-eval'}],skills=['drh-eval:drh-fpt'])
            self.assertEqual(claude_cli.parse_stream(raw,MODEL,runtime=archived).usage['loaded_files'][0]['path'],'.claude/skills/drh-fpt/SKILL.md')


if __name__=='__main__':unittest.main()
