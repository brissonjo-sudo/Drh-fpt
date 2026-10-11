"""Évaluation brute et arbitrage humain séparés ; aucun jugement réécrit."""
from __future__ import annotations
from datetime import datetime
from urllib.parse import urlparse
import campaign


def assess(judge,case,binding,decisions):
    integrity=campaign.validate_judge_result(judge,case,semantic=False)
    errors=judge.get('erreurs',[])
    doubts=judge.get('incertitudes',[])
    if not isinstance(doubts,list) or any(not isinstance(x,str) or not x.strip() for x in doubts):
        integrity.append('incertitudes mal formées')
    if not isinstance(errors,list) or any(not isinstance(x,str) or not x.strip() for x in errors):
        integrity.append('erreurs mal formées')
    failures=[]
    for item in judge.get('criteres',[]) if isinstance(judge.get('criteres'),list) else []:
        if isinstance(item,dict) and item.get('statut')!='SATISFAIT':
            failures.append('criterion:'+str(item.get('id')))
    failures += ['error:'+str(i) for i in range(len(errors))] if isinstance(errors,list) else []
    failures += ['doubt:'+str(i) for i in range(len(doubts))] if isinstance(doubts,list) else []
    if judge.get('verdict')!='REUSSITE':failures.append('verdict')
    if judge.get('verdict_fiabilite_juridique')!='REUSSITE':failures.append('legal_verdict')
    if judge.get('verdict_architecture')=='ECHEC' or (case.get('type')=='architectural' and judge.get('verdict_architecture')!='REUSSITE'):
        failures.append('architecture_verdict')
    resolutions={};invalid=[]
    for entry in decisions:
        try:
            if not isinstance(entry,dict):raise ValueError('décision mal formée')
            if entry.get('case_id')!=case['id']:continue
            if any(entry.get(k)!=v for k,v in binding.items()):continue
            target=entry['target']
            if target not in failures or target in resolutions:raise ValueError('cible inconnue ou doublon')
            if entry.get('reviewer')!='Jo' or entry.get('confirmed') is not True:raise ValueError('arbitrage humain non confirmé')
            if datetime.fromisoformat(entry['decided_at']).tzinfo is None:raise ValueError('date sans fuseau')
            if not entry.get('reason','').strip() or not entry.get('evidence','').strip():raise ValueError('motif ou preuve humaine absent')
            sources=entry.get('sources')
            if not isinstance(sources,list) or not sources or any(urlparse(x).scheme!='https' for x in sources):
                raise ValueError('source absente')
            allowed={'false_positive','confirmed_error'} if target.startswith(('error:','doubt:')) else {'satisfied','unsatisfied'}
            if entry.get('decision') not in allowed:raise ValueError('décision incompatible')
            resolutions[target]=entry['decision']
        except (ValueError,KeyError,TypeError,AttributeError) as exc:
            invalid.append(str(exc))
    unresolved=[x for x in failures if x not in resolutions]
    confirmed=[x for x,v in resolutions.items() if v in {'confirmed_error','unsatisfied'}]
    return {'integrity_pass':not integrity,'integrity_issues':integrity,
            'raw_pass':not integrity and not failures,'raw_failures':failures,
            'arbitrated_pass':not integrity and not invalid and not unresolved and not confirmed,
            'unresolved':unresolved,'confirmed_failures':confirmed,'invalid_decisions':invalid,
            'human_resolutions':resolutions,'style_scores':'indicative'}


def validate_routing(decisions,bindings):
    issues=[]
    for entry in decisions:
        if not isinstance(entry,dict):issues.append('arbitrage mal formé');continue
        matches=[binding for binding in bindings if all(entry.get(k)==v for k,v in binding.items())]
        if len(matches)!=1:issues.append('arbitrage orphelin ou ambigu : '+str(entry.get('case_id','inconnu')))
    return issues
