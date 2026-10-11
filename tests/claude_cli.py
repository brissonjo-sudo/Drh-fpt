"""Claude Code 2.1.277 : sessions OAuth isolées et traces contrôlées.

Ces contrôles prouvent la cohérence des artefacts, pas l'authenticité
cryptographique d'un appel fournisseur. Aucun secret n'entre dans le runtime.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from providers import ApiCallError, Completion

READ_TOOLS={'Read','Glob','Grep','Skill'}


def file_sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def executable():
    found=shutil.which('claude.exe') or shutil.which('claude.cmd') or shutil.which('claude')
    if found and Path(found).suffix.lower() in {'.cmd','.ps1'}:
        native=Path(found).parent/'node_modules/@anthropic-ai/claude-code/bin/claude.exe'
        if native.is_file():return str(native)
    return found or 'claude'


def command(model,system,*,native=False,effort=None,system_file=None):
    args=[executable(),'--print','--verbose','--output-format','stream-json',
          '--include-hook-events',
          '--no-session-persistence','--restricted','--strict-mcp-config',
          '--mcp-config','{"mcpServers":{}}','--no-chrome',
          '--permission-mode','dontAsk','--permission-prompts','none',
          '--settings','{"disableAllHooks":true,"autoMemoryEnabled":false,"enabledPlugins":{}}',
          '--model',model,'--tools','Read,Glob,Grep,Skill' if native else '']
    if native:args.extend(['--allowedTools','Read,Glob,Grep,Skill'])
    else:
        args.append('--safe-mode')
        if system_file:args.extend(['--system-prompt-file',str(system_file)])
        else:args.extend(['--system-prompt',system or 'Réponds uniquement à la demande.'])
    if effort:args.extend(['--effort',effort])
    return args


def confined_path(value,runtime):
    root=Path(runtime['root']).resolve()
    execution_root=Path(runtime.get('execution_root',runtime['root'])).resolve()
    path=Path(value)
    path=(execution_root/path).resolve() if not path.is_absolute() else path.resolve()
    try:relative=path.relative_to(execution_root).as_posix()
    except ValueError as exc:raise ApiCallError('Lecture hors runtime autorisé') from exc
    return root/relative,relative


def parse_stream(raw,model,*,runtime=None,duration_ms=0):
    try:
        events=[json.loads(line) for line in raw.splitlines() if line.strip()]
        init=[x for x in events if x.get('type')=='system' and x.get('subtype')=='init']
        final=[x for x in events if x.get('type')=='result']
        if len(init)!=1 or len(final)!=1:raise ValueError('init/result absent ou dupliqué')
        start,result=init[0],final[0]
        if any(x.get('type')=='error' or str(x.get('subtype','')).startswith('hook_') for x in events):
            raise ValueError('événement externe ou en erreur')
        if start.get('model')!=model or not model.startswith('claude-'):raise ValueError('modèle substitué')
        if start.get('mcp_servers') or start.get('plugins'):raise ValueError('configuration externe chargée')
        if result.get('subtype')!='success' or result.get('is_error') or result.get('permission_denials'):
            raise ValueError('session en erreur ou permission refusée')
        if result.get('stop_reason') in {'max_tokens','max_output_tokens'}:raise ValueError('réponse tronquée')
        if not isinstance(result.get('result'),str) or not result['result'].strip():raise ValueError('réponse vide')
        allowed=READ_TOOLS if runtime else set()
        if set(start.get('tools',[]))-allowed:raise ValueError('outils disponibles inattendus')
        loaded={}; calls={};results={}
        for event in events:
            message=event.get('message') or {}
            if event.get('type')=='assistant' and message.get('model',model)!=model:
                raise ValueError('modèle assistant différent')
            for block in message.get('content',[]) if isinstance(message.get('content'),list) else []:
                if block.get('type')=='tool_result':
                    if block.get('is_error'):raise ValueError('lecture en erreur')
                    results[block.get('tool_use_id')]=block
                if block.get('type')!='tool_use':continue
                name=block.get('name');inputs=block.get('input') or {}
                if name not in allowed:raise ValueError('outil non autorisé : '+str(name))
                calls[block['id']]=block
                if name=='Read':
                    path,rel=confined_path(inputs['file_path'],runtime)
                    if rel not in runtime['files'] or file_sha(path)!=runtime['files'][rel]:
                        raise ValueError('fichier absent ou altéré')
                    lines=len(path.read_text(encoding='utf8').splitlines())
                    offset=inputs.get('offset',1);limit=inputs.get('limit',2000)
                    full=offset in {None,1} and (limit is None or limit>=lines)
                    loaded[rel]={'path':rel,'sha256':runtime['files'][rel],'tool':'Read','full':full or loaded.get(rel,{}).get('full',False)}
                elif name in {'Glob','Grep'}:
                    path,rel=confined_path(inputs.get('path','.'),runtime)
                    # Toute surface recherchée est journalisée ; une recherche ne
                    # remplace pas la lecture des fichiers obligatoires.
                    if not path.exists():raise ValueError('surface de recherche absente')
                    glob=inputs.get('pattern','') if name=='Glob' else inputs.get('glob','')
                    if '..' in glob.replace('\\','/').split('/') or Path(glob).is_absolute():
                        raise ValueError('motif de recherche hors runtime')
                    if inputs.get('output_mode') not in {None,'content','files_with_matches','count'}:
                        raise ValueError('mode de recherche inattendu')
                else:
                    skill=inputs.get('skill','').lstrip('/')
                    rel=runtime.get('skills',{}).get(skill)
                    if not rel or inputs.get('args'):raise ValueError('skill externe ou arguments inattendus')
                    path,_=confined_path(rel,runtime)
                    if file_sha(path)!=runtime['files'][rel]:raise ValueError('skill altéré')
                    loaded[rel]={'path':rel,'sha256':runtime['files'][rel],'tool':'Skill','full':True}
        # Certains CLI émettent le résultat d'un Skill comme un message utilisateur.
        # Toute invocation doit néanmoins avoir un résultat d'outil associé.
        if set(calls)-set(results):raise ValueError('résultat de lecture absent')
        usage=dict(result.get('usage') or {})
        model_usage=result.get('modelUsage') or {}
        if set(model_usage)-{model}:raise ValueError('usage d’un autre modèle')
        usage.update({'resolved_model':model,'loaded_files':list(loaded.values()),
                      'tool_calls':[{'name':x['name'],'input':x['input']} for x in calls.values()]})
        return Completion(result['result'],False,usage,result.get('session_id'),duration_ms,raw)
    except (ValueError,KeyError,TypeError,AttributeError,OSError) as exc:
        raise ApiCallError('Trace Claude invalide : '+str(exc),provider_trace=raw) from exc


def isolated_environment(config):
    """Réutilise uniquement l'auth OAuth ; aucune configuration utilisateur copiée."""
    env=dict(os.environ)
    original=Path(env.get('CLAUDE_CONFIG_DIR',str(Path.home()/'.claude')))
    for key in list(env):
        if key.startswith(('ANTHROPIC_','CLAUDE_')):
            env.pop(key,None)
    credentials=original/'.credentials.json'
    if not credentials.exists():raise ApiCallError('Authentification OAuth locale indisponible')
    try:
        expires=json.loads(credentials.read_text(encoding='utf8'))['claudeAiOauth']['expiresAt']
        if not isinstance(expires,(int,float)) or expires/1000<time.time()+3600:
            raise ValueError('expiration proche ou passée')
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise ApiCallError('Reconnecte Claude Code par son flux normal avant la campagne (OAuth expiré ou moins d’une heure restante)') from exc
    # Temporaire hors cwd du modèle ; jamais archivé ni envoyé au modèle.
    shutil.copyfile(credentials,Path(config)/'.credentials.json')
    env['CLAUDE_CONFIG_DIR']=str(config)
    env['CLAUDE_CODE_DISABLE_AUTO_MEMORY']='1'
    return env


def complete_cli(model,system,user,max_tokens,effort=None,*,runtime=None):
    if not model.startswith('claude-'):raise ApiCallError('Identifiant Claude exact requis, aucun alias')
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='drh-claude-auth-') as config:
        env=isolated_environment(config)
        with tempfile.TemporaryDirectory(prefix='drh-claude-judge-') as empty:
            cwd=runtime['root'] if runtime else empty
            prompt=user if runtime else f'{user}\n\nLimite indicative : {max_tokens} tokens.'
            system_file=None
            if not runtime:
                system_file=Path(config)/'system-prompt.txt'
                system_file.write_text(system or 'Réponds uniquement à la demande.',encoding='utf8')
            try:
                response=subprocess.run(command(model,'',native=bool(runtime),effort=effort,system_file=system_file),
                    cwd=cwd,env=env,input=prompt,capture_output=True,text=True,
                    encoding='utf8',errors='strict',timeout=1800 if max_tokens>4000 else 600,check=False)
            except subprocess.TimeoutExpired as exc:
                partial=exc.stdout or ''
                if isinstance(partial,bytes):partial=partial.decode('utf8',errors='replace')
                raise ApiCallError('Exécution Claude impossible : TimeoutExpired',provider_trace=partial) from exc
            except OSError as exc:
                raise ApiCallError('Exécution Claude impossible : '+type(exc).__name__) from exc
            if response.returncode:raise ApiCallError(f'Claude a échoué (code {response.returncode})',provider_trace=response.stdout)
            return parse_stream(response.stdout,model,runtime=runtime,
                                duration_ms=round((time.monotonic()-started)*1000))
