"""Admission Claude avant chaque appel, sans relance d'une réponse qualifiée.

Les diagnostics OK sont archivés séparément. Une attente conserve le processus
de campagne et ses réponses ; elle ne reprend aucune session du fournisseur.
"""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
import errno
import json
import math
import os
from pathlib import Path
import time
import uuid
from providers import ApiCallError

POLICY = {'five_hour_max': .5, 'seven_day_max': .85,
          'serialize_claude': True, 'probe': 'fresh-tool-less-OK',
          'retry_qualification_response': False}


def snapshot(raw):
    events = []
    for line in (raw or '').splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError('Trace de quota illisible') from exc
        if row.get('type') == 'rate_limit_event':
            events.append(row.get('rate_limit_info'))
    if not events or not isinstance(events[-1], dict):
        raise ValueError('Informations de quota absentes')
    info = events[-1]
    if info.get('status') not in {'allowed', 'allowed_warning', 'rejected'}:
        raise ValueError('État de quota inconnu')
    windows = info.get('unifiedWindows', {})
    result = {'status': info['status']}
    for name in ['five_hour', 'seven_day']:
        window = windows.get(name, {})
        usage, reset = window.get('utilization'), window.get('resetsAt')
        if (type(usage) not in {int, float} or not math.isfinite(usage) or usage < 0
            or type(reset) not in {int, float} or not math.isfinite(reset) or reset < 0):
            raise ValueError('Fenêtre de quota absente ou mal formée')
        result[name] = {'utilization': usage, 'resetsAt': reset}
    return result


class Controller:
    def __init__(self, root, *, probe=None, now=time.time, sleep=time.sleep, emit=None, validate=None):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.probe = probe or self._probe
        self.now, self.sleep = now, sleep
        self.emit = emit or (lambda message: print(message, flush=True))
        self.notice = None
        self.validate = validate or (lambda: None)

    @staticmethod
    def _probe(model, effort):
        import claude_cli
        return claude_cli.complete_cli(model, 'Réponds uniquement OK. Aucun outil.',
            'Réponds uniquement OK.', 64, effort)

    def _say(self, message):
        if message != self.notice:
            self.emit(message)
            self.notice = message

    @contextmanager
    def _lease(self):
        lock = self.root / 'admission.lock'
        # Le verrou est porté par l'OS : la mort d'un processus le libère.
        # Ne pas supprimer ce fichier alors que d'autres processus l'attendent.
        with lock.open('a+b') as stream:
            if not os.fstat(stream.fileno()).st_size:
                stream.write(b'\0')
                stream.flush()
            if os.name == 'nt':
                import msvcrt
                def acquire():
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                def release():
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                def acquire():
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                def release():
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            while True:
                try:
                    acquire()
                    break
                except OSError as exc:
                    if exc.errno not in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                        raise
                    self._say('Admission Claude : attente de la fin de l’appel déjà en cours.')
                    self.sleep(1)
            try:
                yield
            finally:
                release()

    def _delay(self, state):
        deadlines = [state[name]['resetsAt'] + 1 for name, limit in
                     [('five_hour', POLICY['five_hour_max']), ('seven_day', POLICY['seven_day_max'])]
                     if state[name]['utilization'] >= limit and state[name]['resetsAt'] >= self.now()]
        return max(deadlines, default=self.now()) - self.now()

    def _archive(self, raw, model):
        probes = self.root / 'probes'
        probes.mkdir(exist_ok=True)
        ident = str(int(self.now())) + '-' + uuid.uuid4().hex
        (probes / (ident + '.jsonl')).write_text(raw, encoding='utf8')
        (probes / (ident + '.json')).write_text(json.dumps({
            'model': model, 'observed_at_unix': self.now(),
            'diagnostic_only': True}, ensure_ascii=False, indent=2), encoding='utf8')

    def _save(self, state):
        temporary = self.root / 'state.tmp'
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf8')
        temporary.replace(self.root / 'state.json')

    def _wait(self, model, effort):
        state_path = self.root / 'state.json'
        state = json.loads(state_path.read_text(encoding='utf8')) if state_path.exists() else None
        while True:
            self.validate()
            delay = self._delay(state) if state else 0
            if delay > 0:
                deadline = self.now() + delay
                when = datetime.fromtimestamp(deadline, timezone.utc).isoformat()
                self._say('Admission Claude suspendue avant réponse : réserve de quota ; prochain contrôle après ' + when + '.')
                self.sleep(min(30, delay))
                continue
            try:
                completion = self.probe(model, effort)
                raw = completion.provider_trace
            except ApiCallError as exc:
                if not exc.provider_trace:
                    if str(exc).startswith(('Reconnecte Claude Code', 'Authentification OAuth locale indisponible')):
                        self._say('Admission Claude suspendue avant réponse : connexion normale à renouveler.')
                        self.sleep(30)
                        continue
                    raise
                raw = exc.provider_trace
                self._archive(raw, model)
                candidate = snapshot(raw)
                if candidate['status'] != 'rejected':
                    raise
                state = candidate
            else:
                self._archive(raw or '', model)
                state = snapshot(raw)
            self._save(state)
            if self._delay(state) > 0:
                continue
            if state['status'] == 'rejected':
                raise ValueError('Refus de quota sans fenêtre future connue')
            self.notice = None
            return

    def wait(self, model, effort):
        with self._lease():
            self._wait(model, effort)
            self.validate()

    def call(self, model, effort, target):
        with self._lease():
            self._wait(model, effort)
            self.validate()
            # Un échec de target est définitif : aucun retry ni nouvelle réponse.
            return target()
