"""Vérifie deux campagnes complètes et leurs artefacts sur le même commit."""
import argparse
import hashlib
import json
from pathlib import Path
import campaign
from providers import Completion


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
    left=integration.get('drh_fpt') or {};right=degraded.get('drh_fpt') or {}
    if not left.get('sha256_bundle') or left.get('sha256_bundle')!=right.get('sha256_bundle'):
        problems.append('bundle différent ou absent entre campagnes')
    return problems


def check_report(path, evidence_file=None):
    report=json.loads(path.read_text(encoding='utf8'));p=report.get('provenance_evaluation') or {}
    problems=[]
    gate=report.get('gate_strict') or {}
    if gate.get('active') is not True or gate.get('reussite') is not True or gate.get('motifs_echec'):
        problems.append('campagne stricte non validée')
    cases=campaign.active_cases(json.loads((campaign.HERE/'cas-de-test.json').read_text(encoding='utf8')),p.get('mode'),[])
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
    if p.get('sha256_cas')!=campaign.sha256_text((campaign.HERE/'cas-de-test.json').read_text(encoding='utf-8')):
        problems.append('critères différents des cas courants')
    if p.get('case_ids')!=[c['id'] for c in cases] or p.get('selection_diagnostique'):
        problems.append('sélection incomplète ou diagnostique')
    entries=report.get('cas') or []
    problems+=campaign.validate_strict_campaign(p,cases,entries)
    if {e.get('id') for e in entries}!={c['id'] for c in cases} or len(entries)!=30:
        problems.append('30 résultats exacts requis')
    folder=path.parent;root=folder.parent.parent
    for c in cases:
        ident=c['id']
        try:
            answer,meta=campaign.read_answer(root,ident)
            if not answer.strip() or meta.get('truncated') or meta.get('legacy'):
                problems.append(ident+' : réponse absente, ancienne ou tronquée')
            judge=json.loads((folder/(ident+'-eval.json')).read_text(encoding='utf8'))
            problems += [ident+' : '+issue for issue in campaign.validate_judge_result(judge,c)]
            if p.get('provider_repondant')=='codex':
                problems += [ident+' : '+issue for issue in check_codex_trace(root/(ident+'-respondant.jsonl'),meta.get('provider_trace_sha256'),answer)]
            elif meta.get('provider_trace_sha256'):
                actual=hashlib.sha256((root/(ident+'-respondant.jsonl')).read_bytes()).hexdigest()
                if actual!=meta['provider_trace_sha256']:problems.append(ident+' : trace répondant altérée')
            entry=next(e for e in entries if e.get('id')==ident)
            if p.get('provider_juge')=='codex':
                problems += [ident+' : '+issue for issue in check_codex_trace(folder/(ident+'-juge.jsonl'),entry.get('juge_trace_sha256'),judge,judge=True)]
            elif entry.get('juge_trace_sha256'):
                actual=hashlib.sha256((folder/(ident+'-juge.jsonl')).read_bytes()).hexdigest()
                if actual!=entry['juge_trace_sha256']:problems.append(ident+' : trace juge altérée')
            if not p.get('context_sha256_by_case',{}).get(ident):
                problems.append(ident+' : empreinte du contexte absente')
        except (OSError,KeyError,ValueError,StopIteration,TypeError) as exc:
            problems.append(ident+' : artefact invalide ('+type(exc).__name__+')')
    return p,problems


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--integration',required=True);parser.add_argument('--degraded',required=True)
    parser.add_argument('--expected-commit');parser.add_argument('--output');parser.add_argument('--evidence-file')
    args=parser.parse_args();commit=args.expected_commit or campaign.git_provenance(campaign.ROOT)['commit']
    left,a=check_report(Path(args.integration),args.evidence_file);right,b=check_report(Path(args.degraded))
    problems=a+b+compare_provenances(left,right,commit)
    result={'reussite':not problems,'commit_teste':commit,'integration':args.integration,'degraded':args.degraded,'motifs_echec':problems}
    if args.output:Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return int(bool(problems))

if __name__=='__main__':raise SystemExit(main())
