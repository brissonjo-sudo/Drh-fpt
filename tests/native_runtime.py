"""Projet Claude éphémère : skill local et sources du cas, sans barèmes."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import live_sources


def file_sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def signature(runtime):
    portable={k:v for k,v in runtime.items() if k not in {'root','execution_root'}}
    return hashlib.sha256(json.dumps(portable,sort_keys=True,ensure_ascii=False).encode('utf8')).hexdigest()


def copy_skill(source: Path,target: Path):
    if not (source/'SKILL.md').is_file():raise ValueError('SKILL.md absent')
    target.mkdir(parents=True,exist_ok=False)
    shutil.copyfile(source/'SKILL.md',target/'SKILL.md')
    for directory in ['references','assets']:
        base=source/directory
        if not base.exists():continue
        for path in sorted(base.rglob('*.md')):
            # Un lien ne peut pas ajouter un fichier extérieur au corpus prévu.
            if path.is_symlink():raise ValueError('Lien de runtime non autorisé')
            path.resolve().relative_to(source.resolve())
            output=target/directory/path.relative_to(base)
            output.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,output)


def stage(root: Path,drh: Path,mode: str,case_id: str,evidence: list,
          companion: Path|None=None) -> dict:
    if mode not in {'integration','degraded'}:raise ValueError('Mode invalide')
    if any(x.get('case_id')!=case_id for x in evidence):raise ValueError('Sources d’un autre cas')
    if mode=='integration' and (not companion or not evidence):raise ValueError('Compagnon et sources requis')
    if mode=='degraded' and (companion or evidence):raise ValueError('Dégradé sans compagnon ni sources')
    root.mkdir(parents=True,exist_ok=False)
    skills={'drh-fpt':'.claude/skills/drh-fpt/SKILL.md'}
    copy_skill(drh,root/'.claude/skills/drh-fpt')
    if mode=='integration':
        copy_skill(companion,root/'.claude/skills/recherche-juridique')
        skills['recherche-juridique']='.claude/skills/recherche-juridique/SKILL.md'
        (root/'sources').mkdir()
        (root/'sources/official.md').write_text(live_sources.source_context(evidence),encoding='utf8')
    files={p.relative_to(root).as_posix():file_sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
    return {'schema_version':1,'profile':'claude-native','root':str(root.resolve()),
            'mode':mode,'case_id':case_id,'files':files,'skills':skills}


def prompt(case: dict,mode: str) -> str:
    instruction='/drh-fpt\n'
    if mode=='integration':
        instruction+='Le compagnon recherche-juridique est installé. Les documents officiels de cette réponse sont dans sources/official.md ; consulte-les.\n'
    else:
        instruction+='Le compagnon recherche-juridique est indisponible pour cette réponse.\n'
    return instruction+'\n'+case['prompt']


def archive(runtime: dict,destination: Path) -> dict:
    """Copie exacte du corpus sans configuration d'authentification."""
    destination.mkdir(parents=True,exist_ok=False)
    root=Path(runtime['root'])
    for rel,expected in runtime['files'].items():
        path=root/rel
        if file_sha(path)!=expected:raise ValueError('Runtime modifié pendant l’exécution')
        output=destination/rel;output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,output)
    portable={**runtime,'execution_root':runtime['root'],'root':str(destination.resolve())}
    (destination/'_runtime.json').write_text(json.dumps(portable,ensure_ascii=False,indent=2),encoding='utf8')
    return portable
