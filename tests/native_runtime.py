"""Projet Claude éphémère : skill local et sources du cas, sans barèmes."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import live_sources

MAX_SOURCE_SEGMENT_BYTES=16000


def source_segments(text):
    """Borne octets et lignes sans perdre ni modifier un caractère source."""
    pieces=[];buffer=[];size=0;lines=0
    for char in text:
        width=len(char.encode('utf8'))
        if size+width>MAX_SOURCE_SEGMENT_BYTES or (char=='\n' and lines>=300):
            pieces.append(''.join(buffer));buffer=[];size=0;lines=0
        buffer.append(char);size+=width;lines+=char=='\n'
    if buffer:pieces.append(''.join(buffer))
    return pieces


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
          companion: Path|None=None,*,proof_required: bool=True) -> dict:
    if mode not in {'integration','degraded'}:raise ValueError('Mode invalide')
    if any(x.get('case_id')!=case_id for x in evidence):raise ValueError('Sources d’un autre cas')
    if mode=='integration' and (not companion or (proof_required and not evidence)):
        raise ValueError('Compagnon et sources requis sauf exemption explicite')
    if mode=='degraded' and (companion or evidence):raise ValueError('Dégradé sans compagnon ni sources')
    root.mkdir(parents=True,exist_ok=False)
    skills={'drh-fpt':'.claude/skills/drh-fpt/SKILL.md'}
    copy_skill(drh,root/'.claude/skills/drh-fpt')
    source_files=[]
    if mode=='integration':
        copy_skill(companion,root/'.claude/skills/recherche-juridique')
        skills['recherche-juridique']='.claude/skills/recherche-juridique/SKILL.md'
        if evidence:
            (root/'sources').mkdir()
            chunks=source_segments(live_sources.source_context(evidence))
            for number,chunk in enumerate(chunks,1):
                rel=f'sources/official-{number:03}.md';source_files.append(rel)
                (root/rel).write_text(chunk,encoding='utf8',newline='\n')
            index='# Documents officiels du cas\n\n'
            index+='Lire tous les fragments ci-dessous dans cet ordre avant de conclure. Leur concaténation restitue intégralement le dossier consulté ; une coupure peut se situer au milieu d’un passage.\n\n'
            index+='\n'.join(f'- `{rel}`' for rel in source_files)+'\n'
            (root/'sources/official.md').write_text(index,encoding='utf8',newline='\n')
    # --restricted ignore les sources de réglages projet, donc leur découverte
    # de skills. Un plugin local explicitement fourni est une voie native
    # documentée, sans ajouter de répertoire extérieur ni activer de réglages.
    (root/'.claude-plugin').mkdir()
    manifest={'name':'drh-eval','version':'0.7.0','skills':['./.claude/skills/']}
    (root/'.claude-plugin/plugin.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    namespaced={f'drh-eval:{name}':rel for name,rel in skills.items()}
    skills.update(namespaced)
    files={p.relative_to(root).as_posix():file_sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
    return {'schema_version':1,'profile':'claude-native','root':str(root.resolve()),
            'mode':mode,'case_id':case_id,'files':files,'skills':skills,
            'source_files':source_files,
            'plugin':{'name':'drh-eval','relative_root':'.'},'expected_skills':list(namespaced)}


def prompt(case: dict,mode: str) -> str:
    instruction='Utilise le skill drh-eval:drh-fpt pour répondre à la question suivante.\n'
    if mode=='integration':
        instruction+='Utilise aussi le skill drh-eval:recherche-juridique pour cette réponse.\n'
        if case.get('preuve_requise',case.get('type')!='echec_attendu'):
            instruction+='Les documents officiels de cette réponse sont dans sources/official.md ; consulte-les.\n'
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
