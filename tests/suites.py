"""Suites nommées et gel humain préalable, indépendants des scores modèles."""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
SLOTS={'codex:integration','codex:degraded','claude-native:integration','claude-native:degraded'}
THRESHOLD={'mandatory':1.0,'confirmed_legal_errors':0,'style':'indicative',
           'unresolved_disputes':'block','arbitrator':'Jo'}


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_suite(name='developpement', *, registry=None) -> dict:
    registry=Path(registry or HERE/'suites.json')
    data=json.loads(registry.read_text(encoding='utf8'))
    if data.get('schema_version')!=1 or name not in data.get('suites',{}):
        raise ValueError('Suite inconnue ou registre incompatible')
    spec=data['suites'][name]
    path=registry.parent/spec['path']
    seal=None
    if spec.get('qualification'):
        seal_path=registry.parent/spec['seal']
        if spec.get('state') not in {'frozen','pending-human-approval'} or not seal_path.exists():
            raise ValueError('Barèmes concrets non approuvés par Jo puis gelés')
        seal=json.loads(seal_path.read_text(encoding='utf8'))
        if seal.get('state')!='frozen' or seal.get('threshold')!=THRESHOLD:
            raise ValueError('Gel ou seuil incompatible')
        if seal.get('cases_sha256')!=file_sha(path):
            raise ValueError('Barèmes modifiés après gel')
        approval=seal.get('approval') or {}
        validate_approval(approval,path)
    cases=json.loads(path.read_text(encoding='utf8'))
    if spec.get('prefixes'):
        chosen=[]
        for prefix in spec['prefixes']:
            matches=[x for x in cases if x['id']==prefix or x['id'].startswith(prefix+'-')]
            if len(matches)!=1:raise ValueError('ID ciblé absent ou ambigu : '+prefix)
            chosen.extend(matches)
        cases=chosen
    ids=[x['id'] for x in cases]
    if len(ids)!=len(set(ids)):raise ValueError('Cas dupliqués')
    for mode in ['integration','degraded']:
        if sum(mode in x.get('modes',['integration','degraded']) for x in cases)!=spec['expected_per_mode']:
            raise ValueError('Nombre de cas incompatible avec la suite')
    return {'name':name,**spec,'cases':cases,'cases_path':str(path),
            'sha256':file_sha(path),'registry_sha256':file_sha(registry),
            'seal_sha256':file_sha(seal_path) if seal else None,
            'runtime_commit':seal.get('runtime_commit') if seal else None,
            'profiles':seal.get('approval',{}).get('profiles') if seal else None}


def validate_approval(approval: dict, path: Path) -> None:
    if approval.get('reviewer')!='Jo' or approval.get('decision')!='approved':
        raise ValueError('Approbation explicite de Jo requise')
    if not isinstance(approval.get('evidence'),str) or not approval['evidence'].strip():
        raise ValueError('Trace de la décision humaine absente')
    at=datetime.fromisoformat(approval.get('approved_at',''))
    if at.tzinfo is None:raise ValueError('Date humaine sans fuseau')
    if approval.get('cases_sha256')!=file_sha(path):
        raise ValueError('Approbation portant sur des barèmes différents')
    commit=approval.get('runtime_commit','')
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):
        raise ValueError('Commit de runtime exact requis')
    if set(approval.get('profiles',{}))!=SLOTS:
        raise ValueError('Les quatre profils exacts doivent être approuvés')
    for slot,profile in approval['profiles'].items():
        validate_profile({'profiles':approval['profiles']},slot,profile)
        native=slot.startswith('claude-native')
        if profile['provider_repondant']!=('claude-cli' if native else 'codex') or profile['provider_juge']!=('codex' if native else 'claude-cli'):
            raise ValueError('Familles croisées requises')
        if profile['execution_profile']!=('claude-native' if native else 'assembled'):
            raise ValueError('Profil d’exécution incompatible')
        if set(profile['cli_versions'])!={'codex','claude-cli'} or not all(profile['cli_versions'].values()):
            raise ValueError('Versions CLI exactes requises')
        for role in ['repondant','juge']:
            model=profile['modele_'+role]
            prefix='claude-' if profile['provider_'+role]=='claude-cli' else 'gpt-'
            if not isinstance(model,str) or not model.startswith(prefix):raise ValueError('Modèle exact requis')


def freeze(path: Path, approval: dict, output: Path) -> dict:
    validate_approval(approval,path)
    cases=json.loads(path.read_text(encoding='utf8'))
    if len(cases)!=12 or len({x['id'] for x in cases})!=12:
        raise ValueError('12 cas neufs exacts requis')
    for case in cases:
        if not isinstance(case.get('preuve_requise',True),bool):
            raise ValueError('Toute exemption de source exige preuve_requise=false explicite')
        required=case.get('required_source_ids')
        if not isinstance(required,list) or any(not isinstance(x,str) or not x.strip() for x in required):
            raise ValueError('Sources primaires requises à identifier avant gel')
        if case.get('preuve_requise',True) and not required:
            raise ValueError('Source requise absente ; toute exemption doit être explicite et revue')
        for field in ['attendus','attendus_degraded']:
            criteria=case.get(field)
            if not isinstance(criteria,list) or not criteria:
                raise ValueError('Barème requis dans les deux modes')
            if len({x['id'] for x in criteria})!=len(criteria):raise ValueError('Critères dupliqués')
            if any(not x.get('texte','').strip() for x in criteria):raise ValueError('Critère vide')
    sealed={'schema_version':1,'state':'frozen','cases_sha256':file_sha(path),
            'runtime_commit':approval['runtime_commit'],'approval':approval,'threshold':THRESHOLD}
    with output.open('x',encoding='utf8') as stream:
        json.dump(sealed,stream,ensure_ascii=False,indent=2)
    return sealed


def cli_versions() -> dict:
    result={}
    for provider,binary in [('codex','codex'),('claude-cli','claude')]:
        executable=shutil.which(binary+'.exe') or shutil.which(binary+'.cmd') or shutil.which(binary)
        if provider=='claude-cli':
            from claude_cli import executable as claude_executable
            executable=claude_executable()
        if not executable:raise ValueError('CLI absent : '+binary)
        response=subprocess.run([executable,'--version'],capture_output=True,text=True,encoding='utf8',timeout=30)
        if response.returncode or not response.stdout.strip():raise ValueError('Version CLI inconnue')
        result[provider]=response.stdout.strip()
    return result


def validate_profile(suite: dict, slot: str, actual: dict) -> None:
    """Les modèles/efforts/CLI sont approuvés avant le premier cas, sans fallback."""
    profiles=suite.get('profiles') or {}
    expected=profiles.get(slot)
    if not isinstance(expected,dict) or not expected:raise ValueError('Profil exact non approuvé')
    required={'provider_repondant','modele_repondant','effort_repondant','provider_juge',
              'modele_juge','effort_juge','execution_profile','context_mode','cli_versions'}
    if set(expected)!=required or any(actual.get(key)!=expected[key] for key in required):
        raise ValueError('Profil différent des modèles/efforts/CLI approuvés')


def claim_launch(suite: dict, state: Path, slot: str, run_id: str, commit: str) -> None:
    """Réserver avant appel : une réponse ouverte ne peut pas devenir un nouveau jeu."""
    if not suite.get('qualification'):return
    if not suite.get('reserve_for') and commit!=suite.get('runtime_commit'):raise ValueError('Runtime différent du commit gelé')
    if slot not in SLOTS:raise ValueError('Configuration de qualification inconnue')
    state.parent.mkdir(parents=True,exist_ok=True)
    lock=state.with_suffix('.lock')
    descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    try:
        os.close(descriptor)
        data=json.loads(state.read_text(encoding='utf8')) if state.exists() else {}
        game=data.setdefault(suite['name'],{'seal_sha256':suite['seal_sha256'],'runtime_commit':commit,'runs':{}})
        if game.get('outcome'):raise ValueError('Jeu clos et consommé : tout nouveau créneau est interdit')
        if game['runtime_commit']!=commit:raise ValueError('Runtime différent du commit de ce jeu consommé')
        if game['seal_sha256']!=suite['seal_sha256']:raise ValueError('Jeu consommé avec un autre gel')
        if slot in game['runs']:raise ValueError('Créneau déjà consommé ; aucune relance de score')
        if suite.get('reserve_for') and data.get(suite['reserve_for'],{}).get('outcome')!='failed':
            raise ValueError('Réserve disponible uniquement après échec du jeu A')
        game['runs'][slot]=run_id
        temporary=state.with_suffix('.tmp')
        temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
        temporary.replace(state)
    finally:
        lock.unlink()


def record_outcome(suite: dict,state: Path,reports: dict,result: dict) -> None:
    """Clôture après contrôle commun ; les disputes pendantes restent à Jo."""
    if set(reports)!=SLOTS:raise ValueError('Les quatre rapports sont requis')
    assessments=result.get('qualification_assessments',{})
    if any(item.get('unresolved') or item.get('invalid_decisions')
           for mode in assessments.values() for item in mode.values()):
        raise ValueError('Arbitrage humain encore requis avant clôture')
    data=json.loads(state.read_text(encoding='utf8'))
    game=data.get(suite['name'])
    if not game or set(game['runs'])!=SLOTS:raise ValueError('Quatre créneaux consommés requis')
    if game['seal_sha256']!=suite['seal_sha256']:raise ValueError('Gel différent')
    if 'outcome' in game:raise ValueError('Jeu déjà clos')
    proofs={}
    for slot,path in reports.items():
        report=json.loads(path.read_text(encoding='utf8'))
        p=report.get('provenance_evaluation',{})
        if p.get('campagne_id')!=game['runs'][slot] or p.get('suite')!=suite['name'] or p.get('drh_fpt',{}).get('commit')!=game['runtime_commit']:
            raise ValueError('Rapport différent du lancement réservé')
        proofs[slot]={'report_sha256':file_sha(path),'path':str(path)}
    game.update({'outcome':'passed' if result['reussite'] else 'failed',
                 'reports':proofs,'issues':result['motifs_echec']})
    temporary=state.with_suffix('.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');temporary.replace(state)


def validate_launch(suite: dict,state: Path,provenance: dict,report: Path) -> None:
    data=json.loads(state.read_text(encoding='utf8'));game=data.get(suite['name'])
    if not game or game.get('seal_sha256')!=suite['seal_sha256']:
        raise ValueError('Registre de lancement absent ou gel différent')
    if game.get('outcome')=='failed':raise ValueError('Jeu clos en échec : qualification définitivement refusée')
    slot=('claude-native' if provenance.get('execution_profile')=='claude-native' else provenance.get('provider_repondant',''))+':'+provenance.get('mode','')
    if game.get('runs',{}).get(slot)!=provenance.get('campagne_id') or game.get('runtime_commit')!=provenance.get('drh_fpt',{}).get('commit'):
        raise ValueError('Rapport sans créneau réservé sur ce commit')
    if game.get('outcome')=='passed' and game.get('reports',{}).get(slot,{}).get('report_sha256')!=file_sha(report):
        raise ValueError('Rapport différent de la clôture réussie')


def abandon_game(suite: dict,state: Path,results_root: Path,kind: str,reason: str,*,new_commit=None) -> None:
    """Consommer un jeu interrompu/invalide sans fabriquer de bilan ni rejouer."""
    if kind not in {'interruption','execution_error','runtime_changed'} or not reason.strip():
        raise ValueError('Motif technique explicite requis')
    data=json.loads(state.read_text(encoding='utf8'));game=data.get(suite['name'])
    if not game or not game.get('runs') or game.get('outcome'):raise ValueError('Jeu non lancé ou déjà clos')
    if game.get('seal_sha256')!=suite['seal_sha256']:raise ValueError('Gel différent')
    root=results_root.resolve();proofs={};interrupted=False;execution_error=False
    for slot,run_id in game['runs'].items():
        folder=(root/run_id).resolve()
        folder.relative_to(root)
        path=folder/'_provenance.json'
        if not path.is_file():raise ValueError('Provenance du lancement absente')
        p=json.loads(path.read_text(encoding='utf8'))
        if p.get('campagne_id')!=run_id or p.get('suite')!=suite['name'] or p.get('drh_fpt',{}).get('commit')!=game['runtime_commit']:
            raise ValueError('Provenance différente du lancement')
        reports=list(folder.rglob('_bilan.json'))
        interrupted |= not reports
        execution_error |= any(any(x.get('statut')!='ok' for x in json.loads(report.read_text(encoding='utf8')).get('cas',[])) for report in reports)
        proofs[slot]={f.relative_to(folder).as_posix():file_sha(f) for f in folder.rglob('*') if f.is_file()}
    if kind=='interruption' and not interrupted:raise ValueError('Aucune interruption constatée')
    if kind=='execution_error' and not execution_error:raise ValueError('Aucune erreur d’exécution constatée')
    if kind=='runtime_changed' and (not new_commit or new_commit==game['runtime_commit']):raise ValueError('Aucun nouveau commit constaté')
    game.update({'outcome':'failed','abandonment':{'kind':kind,'reason':reason,
        'at':datetime.now(timezone.utc).isoformat(),'new_commit':new_commit,'proofs':proofs,
        'business_score':'not-qualified','human_decision':None}})
    temporary=state.with_suffix('.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');temporary.replace(state)
