"""Claude Code 2.1.277 : sessions OAuth isolées et traces contrôlées.

Ces contrôles prouvent la cohérence des artefacts, pas l'authenticité
cryptographique d'un appel fournisseur. Aucun secret n'entre dans le runtime.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
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


def command(model,system,*,native=False,effort=None,system_file=None,plugin_root=None):
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
    if native and plugin_root:args.extend(['--plugin-dir',str(plugin_root)])
    return args


def confined_path(value,runtime):
    root=Path(runtime['root']).resolve()
    execution_root=Path(runtime.get('execution_root',runtime['root'])).resolve()
    path=Path(value)
    path=(execution_root/path).resolve() if not path.is_absolute() else path.resolve()
    try:relative=path.relative_to(execution_root).as_posix()
    except ValueError as exc:raise ApiCallError('Lecture hors runtime autorisé') from exc
    return root/relative,relative


def normalized_newlines(text):
    return text.replace('\r\n','\n').replace('\r','\n')


def verified_read_lines(path,inputs,result):
    """Prouve les lignes reçues, jamais la seule étendue demandée."""
    text=normalized_newlines(path.read_text(encoding='utf8'))
    lines=text.split('\n');count=len(lines)-(1 if text.endswith('\n') else 0)
    offset=inputs.get('offset') or 1;limit=inputs.get('limit') or 2000
    if type(offset) is not int or type(limit) is not int or offset<1 or limit<1:
        raise ValueError('étendue Read invalide')
    content=result.get('content')
    if isinstance(content,list) and len(content)==1 and content[0].get('type')=='text':content=content[0].get('text')
    if not isinstance(content,str) or not content:raise ValueError('contenu Read vide ou inconnu')
    received=set()
    for line in normalized_newlines(content).splitlines():
        match=re.fullmatch(r'[ ]*(\d+)\t(.*)',line)
        if not match:raise ValueError('contenu Read non numéroté ou tronqué')
        number=int(match[1])
        if number in received or not offset<=number<offset+limit or not 1<=number<=len(lines):
            raise ValueError('numérotation Read incohérente')
        if match[2]!=lines[number-1]:raise ValueError('contenu Read différent de l’archive')
        received.add(number)
    expected=set(range(offset,min(count+1,offset+limit)))
    if not expected<=received:raise ValueError('contenu Read incomplet ou tronqué')
    # La dernière ligne vide est facultative dans la restitution du CLI.
    optional={count+1} if text.endswith('\n') else set()
    if received-expected-optional:raise ValueError('lignes Read supplémentaires')
    return received & set(range(1,count+1)),count


def verified_skill_expansion(text,runtime,pending):
    text=normalized_newlines(text);head,separator,body=text.partition('\n')
    if not separator:raise ValueError('expansion Skill vide')
    base=head.removeprefix('Base directory for this skill: ')
    path,rel=confined_path(str(Path(base)/'SKILL.md'),runtime)
    matches=[i for i,item in enumerate(pending) if item['rel']==rel]
    if not matches or rel not in runtime['files'] or file_sha(path)!=runtime['files'][rel]:
        raise ValueError('expansion Skill orpheline ou hors runtime')
    index=matches[0];arguments=normalized_newlines(pending[index]['args']).strip('\n')
    if arguments:
        suffix='\n\nARGUMENTS: '+arguments
        body=body.strip('\n')
        if not body.endswith(suffix):raise ValueError('arguments de l’expansion Skill absents ou différents')
        body=body[:-len(suffix)]
    expected=normalized_newlines(path.read_text(encoding='utf8'))
    expected=re.sub(r'^---\n.*?\n---(?:\n|$)','',expected,count=1,flags=re.S)
    if body.strip('\n')!=expected.strip('\n'):raise ValueError('corps Skill absent, tronqué ou différent')
    pending.pop(index)
    return rel


def parse_stream(raw,model,*,runtime=None,duration_ms=0):
    try:
        events=[json.loads(line) for line in raw.splitlines() if line.strip()]
        init=[x for x in events if x.get('type')=='system' and x.get('subtype')=='init']
        final=[x for x in events if x.get('type')=='result']
        if len(init)!=1 or len(final)!=1:raise ValueError('init/result absent ou dupliqué')
        start,result=init[0],final[0]
        if any(x.get('type')=='error' or str(x.get('subtype','')).startswith('hook_') for x in events):
            raise ValueError('événement externe ou en erreur')
        if any(x.get('type')=='system' and x.get('subtype')=='compact_boundary' for x in events):
            raise ValueError('compaction automatique interdite')
        if start.get('model')!=model or not model.startswith('claude-'):raise ValueError('modèle substitué')
        if start.get('mcp_servers'):raise ValueError('configuration MCP externe chargée')
        plugins=start.get('plugins') or []
        expected_plugin=runtime.get('plugin',{}).get('name') if runtime else None
        names=[x.get('name') if isinstance(x,dict) else x for x in plugins]
        if expected_plugin:
            if names!=[expected_plugin]:raise ValueError('plugin candidat absent ou plugin externe chargé')
            if set(runtime.get('expected_skills',[]))-set(start.get('skills',[])):
                raise ValueError('skills candidats absents du catalogue natif')
        elif plugins:raise ValueError('configuration externe chargée')
        if result.get('subtype')!='success' or result.get('is_error') or result.get('permission_denials'):
            raise ValueError('session en erreur ou permission refusée')
        if result.get('stop_reason') in {'max_tokens','max_output_tokens'}:raise ValueError('réponse tronquée')
        if not isinstance(result.get('result'),str) or not result['result'].strip():raise ValueError('réponse vide')
        allowed=READ_TOOLS if runtime else set()
        if set(start.get('tools',[]))-allowed:raise ValueError('outils disponibles inattendus')
        loaded={}; calls={};results={};read_requests={};coverage={};pending_skills=[]
        for event in events:
            message=event.get('message') or {}
            content=message.get('content',[])
            if isinstance(content,str):content=[{'type':'text','text':content}]
            if event.get('type')=='user' and (not isinstance(content,list) or not content or
                any(not isinstance(b,dict) or b.get('type') not in {'text','tool_result'} for b in content)):
                raise ValueError('message utilisateur supplémentaire mal formé')
            if event.get('type')=='assistant' and message.get('model',model)!=model:
                raise ValueError('modèle assistant différent')
            for block in content if isinstance(content,list) else []:
                if event.get('type')=='user' and block.get('type')=='text':
                    # L'expansion native d'un Skill est attendue. Une consigne
                    # de continuation ou un résumé ajouté par le CLI ne l'est pas.
                    if not runtime or not str(block.get('text','')).startswith('Base directory for this skill: '):
                        raise ValueError('continuation, résumé ou message utilisateur supplémentaire')
                    rel=verified_skill_expansion(block['text'],runtime,pending_skills)
                    loaded[rel]={'path':rel,'sha256':runtime['files'][rel],'tool':'Skill','full':True}
                if block.get('type')=='tool_result':
                    if block.get('is_error'):raise ValueError('lecture en erreur')
                    identifier=block.get('tool_use_id')
                    if identifier not in calls or identifier in results:raise ValueError('résultat orphelin ou dupliqué')
                    results[identifier]=block
                    if identifier in read_requests:
                        path,rel,inputs=read_requests[identifier]
                        received,count=verified_read_lines(path,inputs,block)
                        coverage.setdefault(rel,set()).update(received)
                        full=set(range(1,count+1))<=coverage[rel]
                        loaded[rel]={'path':rel,'sha256':runtime['files'][rel],'tool':'Read',
                                     'full':full or loaded.get(rel,{}).get('full',False)}
                if block.get('type')!='tool_use':continue
                name=block.get('name');inputs=block.get('input') or {}
                if name not in allowed:raise ValueError('outil non autorisé : '+str(name))
                if not isinstance(block.get('id'),str) or not block['id'] or block['id'] in calls:
                    raise ValueError('identifiant d’outil absent ou dupliqué')
                calls[block['id']]=block
                if name=='Read':
                    path,rel=confined_path(inputs['file_path'],runtime)
                    if rel not in runtime['files'] or file_sha(path)!=runtime['files'][rel]:
                        raise ValueError('fichier absent ou altéré')
                    read_requests[block['id']]=(path,rel,inputs)
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
                    # Skill transmet normalement la question en argument texte.
                    # Cela n'ajoute ni outil ni surface de lecture au runtime.
                    if not rel or not isinstance(inputs.get('args',''),str):
                        raise ValueError('skill externe ou arguments mal formés')
                    path,_=confined_path(rel,runtime)
                    if file_sha(path)!=runtime['files'][rel]:raise ValueError('skill altéré')
                    pending_skills.append({'rel':rel,'args':inputs.get('args','')})
        # Certains CLI émettent le résultat d'un Skill comme un message utilisateur.
        # Toute invocation doit néanmoins avoir un résultat d'outil associé.
        if set(calls)-set(results):raise ValueError('résultat de lecture absent')
        if pending_skills:raise ValueError('expansion native Skill absente')
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
                response=subprocess.run(command(model,'',native=bool(runtime),effort=effort,system_file=system_file,
                    plugin_root=runtime['root'] if runtime else None),
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
