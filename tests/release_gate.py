"""Vérifie deux campagnes complètes et leurs artefacts sur le même commit."""
import argparse
import hashlib
import json
from pathlib import Path
import campaign
import suites
from providers import Completion
from providers import ApiCallError
import claude_cli
import native_runtime
import arbitration


def check_codex_trace(path, expected_sha, expected, *, judge=False):
    try:
        data=path.read_bytes()
        if not expected_sha or hashlib.sha256(data).hexdigest()!=expected_sha:
            return ['trace Codex absente ou altérée']
        events=[json.loads(line) for line in data.decode('utf8').splitlines() if line.strip()]
        if not any(e.get('type')=='turn.completed' for e in events):
            return ['trace Codex sans tour final complet']
        if any(e.get('type') in ('turn.failed','error') for e in events):
            return ['trace Codex en erreur']
        items=[e['item'] for e in events if e.get('type')=='item.completed']
        if any(i.get('type') not in ('reasoning','agent_message') for i in items):
            return ['trace Codex contenant un outil']
        messages=[i['text'] for i in items if i.get('type')=='agent_message']
        actual=messages[-1]
        if judge:
            parsed=campaign.parse_judge_completion(Completion(actual,False,{},'trace',0))
            actual={k:v for k,v in parsed.items() if k!='metriques'}
            expected={k:v for k,v in expected.items() if k!='metriques'}
        return [] if actual==expected else ['artefact différent du message final Codex']
    except (OSError,ValueError,KeyError,IndexError,AttributeError,TypeError):
        return ['trace Codex illisible ou mal formée']


def compare_provenances(integration, degraded, expected_commit):
    problems=[]
    if integration.get('mode')!='integration' or degraded.get('mode')!='degraded':
        problems.append('modes integration/degraded attendus')
    for mode,p in [('integration',integration),('degraded',degraded)]:
        drh=p.get('drh_fpt') or {}
        if drh.get('commit')!=expected_commit or drh.get('dirty') is not False:
            problems.append(mode+' : commit différent ou dépôt non propre')
    for field in ['sha256_cas']:
        if not integration.get(field) or integration.get(field)!=degraded.get(field):
            problems.append(field+' différent ou absent entre campagnes')
    for field in ['suite','suite_registry_sha256','suite_seal_sha256','execution_profile',
                  'provider_repondant','modele_repondant','effort_repondant',
                  'provider_juge','modele_juge','effort_juge','context_mode']:
        if integration.get(field)!=degraded.get(field):problems.append(field+' différent entre modes')
    left=integration.get('drh_fpt') or {};right=degraded.get('drh_fpt') or {}
    if not left.get('sha256_bundle') or left.get('sha256_bundle')!=right.get('sha256_bundle'):
        problems.append('bundle différent ou absent entre campagnes')
    return problems


def check_claude_trace(path,expected_sha,expected,model,*,judge=False,runtime=None):
    try:
        if not expected_sha or hashlib.sha256(path.read_bytes()).hexdigest()!=expected_sha:
            return None,['trace Claude absente ou altérée']
        completion=claude_cli.parse_stream(path.read_text(encoding='utf8'),model,runtime=runtime)
        actual=completion.text
        if judge:
            actual={k:v for k,v in campaign.parse_judge_completion(completion).items() if k!='metriques'}
            expected={k:v for k,v in expected.items() if k!='metriques'}
        return completion,([] if actual==expected else ['artefact différent du message final Claude'])
    except (OSError,ValueError,ApiCallError):return None,['trace Claude invalide']


def check_report(path, evidence_file=None, decisions=None):
    report=json.loads(path.read_text(encoding='utf8'));p=report.get('provenance_evaluation') or {}
    problems=[]
    gate=report.get('gate_strict') or {}
    try:
        suite=suites.load_suite(p.get('suite','developpement'))
    except (OSError,ValueError) as exc:
        return p,['suite non approuvée ou invalide : '+str(exc)]
    cases=campaign.active_cases(suite['cases'],p.get('mode'),[])
    qualification=suite['qualification']
    if qualification:
        slot=('claude-native' if p.get('execution_profile')=='claude-native' else p.get('provider_repondant',''))+':'+p.get('mode','')
        try:suites.validate_profile(suite,slot,p)
        except ValueError as exc:problems.append(str(exc))
        if not suite.get('reserve_for') and p.get('drh_fpt',{}).get('commit')!=suite['runtime_commit']:
            problems.append('commit différent du candidat gelé')
        if p.get('suite_registry_sha256')!=suite['registry_sha256']:
            problems.append('empreinte du registre absente ou différente')
    if gate.get('active') is not True or (not qualification and (gate.get('reussite') is not True or gate.get('motifs_echec'))):
        problems.append('campagne stricte non validée')
    if p.get('suite_registry_sha256') and p['suite_registry_sha256']!=suite['registry_sha256']:
        problems.append('registre de suites modifié')
    if p.get('mode')=='integration':
        try:
            source_path=Path(evidence_file or p['evidence_file'])
            traces,sha=campaign.load_evidence(str(source_path))
            if not p.get('evidence_sha256') or sha!=p['evidence_sha256']:
                problems.append('dossier de sources différent de la campagne')
            at=campaign.datetime.fromisoformat(p['date_debut_utc'])
            problems+=campaign.validate_evidence(traces,cases,'integration','live',source_path.resolve().parent,as_of=at)
        except (OSError,ValueError,TypeError,KeyError,SystemExit):
            problems.append('dossier de sources absent ou invalide')
    if p.get('sha256_cas')!=campaign.sha256_text(Path(suite['cases_path']).read_text(encoding='utf-8')):
        problems.append('critères différents des cas courants')
    if p.get('case_ids')!=[c['id'] for c in cases] or p.get('selection_diagnostique'):
        problems.append('sélection incomplète ou diagnostique')
    entries=report.get('cas') or []
    problems+=campaign.validate_strict_campaign(p,cases,entries,semantic=not qualification)
    if {e.get('id') for e in entries}!={c['id'] for c in cases} or len(entries)!=suite['expected_per_mode']:
        problems.append(str(suite['expected_per_mode'])+' résultats exacts requis')
    folder=path.parent;root=folder.parent.parent
    assessments={}
    for c in cases:
        ident=c['id']
        try:
            answer,meta=campaign.read_answer(root,ident)
            if not answer.strip() or meta.get('truncated') or meta.get('legacy'):
                problems.append(ident+' : réponse absente, ancienne ou tronquée')
            judge=json.loads((folder/(ident+'-eval.json')).read_text(encoding='utf8'))
            problems += [ident+' : '+issue for issue in campaign.validate_judge_result(judge,c,semantic=not qualification)]
            if qualification:
                if 'incertitudes' not in judge:problems.append(ident+' : incertitudes non déclarées')
                binding={'suite_sha256':suite['sha256'],
                         'answer_sha256':hashlib.sha256(campaign.response_path(root,ident).read_bytes()).hexdigest(),
                         'judge_sha256':hashlib.sha256((folder/(ident+'-eval.json')).read_bytes()).hexdigest()}
                assessment=arbitration.assess(judge,c,binding,decisions or [])
                assessments[ident]=assessment
                if not assessment['arbitrated_pass']:problems.append(ident+' : qualification métier non validée ou arbitrage requis')
            if p.get('provider_repondant')=='codex':
                problems += [ident+' : '+issue for issue in check_codex_trace(root/(ident+'-respondant.jsonl'),meta.get('provider_trace_sha256'),answer)]
            elif p.get('provider_repondant')=='claude-cli':
                runtime=None
                if p.get('execution_profile')=='claude-native':
                    runtime=json.loads((root/'runtime'/ident/'_runtime.json').read_text(encoding='utf8'))
                    # Le chemin de l'archive est résolu localement, pas repris du fichier.
                    runtime['root']=str((root/'runtime'/ident).resolve())
                    for rel,sha in runtime['files'].items():
                        file,normalized=claude_cli.confined_path(rel,{**runtime,'execution_root':runtime['root']})
                        if native_runtime.file_sha(file)!=sha:problems.append(ident+' : runtime altéré')
                    expected_runtime=p.get('native_runtime_sha256_by_case',{}).get(ident)
                    if not expected_runtime or native_runtime.signature(runtime)!=expected_runtime or meta.get('native_runtime_sha256')!=expected_runtime:
                        problems.append(ident+' : empreinte native absente ou différente')
                completion,issues=check_claude_trace(root/(ident+'-respondant.jsonl'),meta.get('provider_trace_sha256'),answer,p['modele_repondant'],runtime=runtime)
                problems += [ident+' : '+issue for issue in issues]
                if runtime and completion:
                    loaded={x['path'] for x in completion.usage['loaded_files'] if x.get('full')}
                    required={'.claude/skills/drh-fpt/'+rel for rel in campaign.context_loader.files_for_case(c)}
                    if p['mode']=='integration':required|={'.claude/skills/recherche-juridique/SKILL.md','sources/official.md'}
                    if required-loaded:problems.append(ident+' : fichiers nécessaires non lus entièrement : '+', '.join(sorted(required-loaded)))
            elif meta.get('provider_trace_sha256'):
                actual=hashlib.sha256((root/(ident+'-respondant.jsonl')).read_bytes()).hexdigest()
                if actual!=meta['provider_trace_sha256']:problems.append(ident+' : trace répondant altérée')
            entry=next(e for e in entries if e.get('id')==ident)
            if p.get('provider_juge')=='codex':
                problems += [ident+' : '+issue for issue in check_codex_trace(folder/(ident+'-juge.jsonl'),entry.get('juge_trace_sha256'),judge,judge=True)]
            elif p.get('provider_juge')=='claude-cli':
                _,issues=check_claude_trace(folder/(ident+'-juge.jsonl'),entry.get('juge_trace_sha256'),judge,p['modele_juge'],judge=True)
                problems += [ident+' : '+issue for issue in issues]
            elif entry.get('juge_trace_sha256'):
                actual=hashlib.sha256((folder/(ident+'-juge.jsonl')).read_bytes()).hexdigest()
                if actual!=entry['juge_trace_sha256']:problems.append(ident+' : trace juge altérée')
            if not p.get('context_sha256_by_case',{}).get(ident):
                problems.append(ident+' : empreinte du contexte absente')
        except (OSError,KeyError,ValueError,StopIteration,TypeError,ApiCallError) as exc:
            problems.append(ident+' : artefact invalide ('+type(exc).__name__+')')
    p['_qualification_assessments']=assessments
    return p,problems


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--integration',required=True);parser.add_argument('--degraded',required=True)
    parser.add_argument('--claude-integration');parser.add_argument('--claude-degraded')
    parser.add_argument('--arbitrations')
    parser.add_argument('--close-game',action='store_true')
    parser.add_argument('--expected-commit');parser.add_argument('--output');parser.add_argument('--evidence-file')
    args=parser.parse_args();commit=args.expected_commit or campaign.git_provenance(campaign.ROOT)['commit']
    decisions=json.loads(Path(args.arbitrations).read_text(encoding='utf8')) if args.arbitrations else []
    if not isinstance(decisions,list):raise SystemExit('Arbitrages : liste de décisions attendue')
    left,a=check_report(Path(args.integration),args.evidence_file,decisions);right,b=check_report(Path(args.degraded),decisions=decisions)
    problems=a+b+compare_provenances(left,right,commit)
    assessments={'codex_integration':left.get('_qualification_assessments',{}),'codex_degraded':right.get('_qualification_assessments',{})}
    if left.get('suite','').startswith('qualification-'):
        if not args.claude_integration or not args.claude_degraded:
            problems.append('qualification commune : deux campagnes Claude natives requises')
        else:
            native_i,c=check_report(Path(args.claude_integration),decisions=decisions)
            native_d,d=check_report(Path(args.claude_degraded),decisions=decisions)
            problems+=c+d+compare_provenances(native_i,native_d,commit)
            for original,native in [(left,native_i),(right,native_d)]:
                for field in ['suite','sha256_cas','suite_seal_sha256','suite_registry_sha256']:
                    if original.get(field)!=native.get(field):problems.append('qualification commune : '+field+' différent')
                if original.get('provider_repondant')!='codex' or original.get('provider_juge')!='claude-cli':
                    problems.append('couple Codex/Claude attendu')
                if native.get('provider_repondant')!='claude-cli' or native.get('provider_juge')!='codex' or native.get('execution_profile')!='claude-native':
                    problems.append('couple Claude natif/Codex attendu')
            assessments.update({'claude_integration':native_i.get('_qualification_assessments',{}),'claude_degraded':native_d.get('_qualification_assessments',{})})
    result={'reussite':not problems,'commit_teste':commit,'integration':args.integration,'degraded':args.degraded,'motifs_echec':problems}
    if any(assessments.values()):result['qualification_assessments']=assessments
    if args.close_game:
        if not left.get('suite','').startswith('qualification-') or not args.claude_integration or not args.claude_degraded:
            raise SystemExit('Clôture : quatre campagnes de qualification requises')
        suites.record_outcome(suites.load_suite(left['suite']),campaign.RESULTS/'qualification-launches.json',
            {'codex:integration':Path(args.integration),'codex:degraded':Path(args.degraded),
             'claude-native:integration':Path(args.claude_integration),'claude-native:degraded':Path(args.claude_degraded)},result)
    if args.output:Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return int(bool(problems))

if __name__=='__main__':raise SystemExit(main())
