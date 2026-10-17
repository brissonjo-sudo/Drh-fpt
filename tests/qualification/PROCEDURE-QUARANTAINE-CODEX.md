# Quarantaine temporaire du skill global Codex

**Préparée le 15/10/2026. Non exécutée.** Décision de Jo : cette opération
sera autorisée explicitement au moment de la campagne uniquement. La décision
de méthode ne vaut pas autorisation de déplacer maintenant le dossier.

## Périmètre et conditions d'entrée

Source unique : `C:\Users\Krn\.agents\skills\recherche-juridique`.
Destination : `C:\Users\Krn\.agents-quarantaine\<horodatage-UTC>-<UUID>\recherche-juridique`,
hors de `.agents\skills`. Aucun contenu, frontmatter ou réglage utilisateur
n'est modifié. Le déplacement concerne un dossier ordinaire (constaté à la
préparation : 7 fichiers, pas de lien à la racine) ; tout lien/reparse point
rencontré lors de l'exécution impose un nouvel examen, sans déplacement.

Avant la fenêtre : accord explicite de Jo consigné, checkout/runtime propre
et gelé approuvé, versions CLI recontrôlées, OAuth valide, commandes exactes de
campagne validées, absence d'autre tâche dépendant de ce skill pendant la
fenêtre. Ne tuer aucun processus pour libérer le dossier ; différer si nécessaire.
Sans ces prérequis, ne pas ouvrir la fenêtre. Toute correction après ouverture
d'un jeu suit les règles de consommation de A/B ; ne pas relancer un créneau.

La sonde triviale appartient au précontrôle de cette fenêtre autorisée. Elle
n'appelle ni `campaign.main` ni `suites.claim_launch`, ne charge aucun cas A/B,
et ne consomme pas de tentative de qualification. La campagne réelle requiert
son autorisation distincte et ses autres conditions de gel ; elles ne sont pas
accordées par ce document.

## 1. Préparer les chemins et les preuves (après l'accord de Jo)

Utiliser PowerShell 7, depuis le checkout gelé approuvé. Les variables sont
locales à la tâche ; aucun changement de HOME, USERPROFILE ou CODEX_HOME.

```powershell
$ErrorActionPreference = 'Stop'
$taskRepo = (Get-Location).Path
$taskPython = 'C:\Users\Krn\AppData\Local\Programs\Python\Python313\python.exe'
$taskSource = [IO.Path]::GetFullPath('C:\Users\Krn\.agents\skills\recherche-juridique')
$taskQuarantineRoot = [IO.Path]::GetFullPath('C:\Users\Krn\.agents-quarantaine')
$taskStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [Guid]::NewGuid().ToString('N')
$taskWindow = [IO.Path]::GetFullPath((Join-Path $taskQuarantineRoot $taskStamp))
$taskQuarantine = [IO.Path]::GetFullPath((Join-Path $taskWindow 'recherche-juridique'))
$taskEvidence = Join-Path 'C:\Users\Krn\Documents\Codex\repo-recovery\2026-10-12\instantane-r1' ('campagne-quarantaine-' + $taskStamp)
if ($taskSource -ne 'C:\Users\Krn\.agents\skills\recherche-juridique') { throw 'Source inattendue' }
if (-not $taskQuarantine.StartsWith($taskQuarantineRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Destination hors quarantaine' }
if ($taskQuarantine.StartsWith('C:\Users\Krn\.agents\skills\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Destination encore découvrable' }
if (-not (Test-Path -LiteralPath $taskSource -PathType Container)) { throw 'Source absente' }
if (Test-Path -LiteralPath $taskWindow) { throw 'Destination déjà présente : ne pas écraser' }
if (-not (Test-Path -LiteralPath (Join-Path $taskRepo 'tests\providers.py'))) { throw 'Mauvais checkout' }
New-Item -ItemType Directory -Path $taskWindow | Out-Null
New-Item -ItemType Directory -Path $taskEvidence | Out-Null
```

Consigner dans ce dossier de preuves l'accord de Jo, le SHA du runtime, les
versions effectives, et les chemins absolus. Recalculer les empreintes à cet
instant ; le relevé des 7 fichiers de préparation ne remplace pas ce nouveau relevé.

```powershell
function Get-TaskManifest([string]$Root) {
    $taskRootItem = Get-Item -LiteralPath $Root -Force
    if ($taskRootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Racine liée : arrêt' }
    @((Get-ChildItem -LiteralPath $Root -Force -Recurse | Sort-Object FullName) | ForEach-Object {
        if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Lien interne : arrêt' }
        $taskRelative = [IO.Path]::GetRelativePath($Root, $_.FullName)
        if ($_.PSIsContainer) {
            [pscustomobject][ordered]@{path=$taskRelative; kind='directory'; bytes=0; sha256=$null; lastWriteUtc=$_.LastWriteTimeUtc.Ticks}
        } else {
            $taskStream = [IO.File]::OpenRead($_.FullName)
            $taskHasher = [Security.Cryptography.SHA256]::Create()
            try { $taskHash = [BitConverter]::ToString($taskHasher.ComputeHash($taskStream)).Replace('-','').ToLowerInvariant() }
            finally { $taskStream.Dispose(); $taskHasher.Dispose() }
            [pscustomobject][ordered]@{path=$taskRelative; kind='file'; bytes=$_.Length; sha256=$taskHash; lastWriteUtc=$_.LastWriteTimeUtc.Ticks}
        }
    })
}
function Assert-TaskManifest($Expected, [string]$Root) {
    $taskActual = @(Get-TaskManifest $Root)
    if ((ConvertTo-Json -InputObject @($Expected) -Depth 5 -Compress) -ne
        (ConvertTo-Json -InputObject @($taskActual) -Depth 5 -Compress)) { throw 'Manifeste différent' }
}
$taskBefore = @(Get-TaskManifest $taskSource)
ConvertTo-Json -InputObject $taskBefore -Depth 5 | Set-Content -LiteralPath (Join-Path $taskEvidence 'manifest-avant.json') -Encoding utf8
[pscustomobject]@{source=$taskSource; quarantine=$taskQuarantine; evidence=$taskEvidence; state='restauration requise dès déplacement'} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskEvidence 'RESTAURATION-REQUISE.json') -Encoding utf8
```

## 2. Préparer la sonde sans l'exécuter hors fenêtre

Le code ci-dessous utilise le même adaptateur que la campagne. Il conserve la
trace annotée et stderr ; toute mention de skill dans stderr bloque. L'absence
de cette mention prouve seulement le critère de la sonde, pas une absence de
lecture système vérifiée par instrumentation OS. Registres comparés avant/après.

```powershell
$taskProbeCode = @'
import sys, json, subprocess, hashlib
from pathlib import Path
repo, evidence = map(Path, sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo/'tests'))
import providers, suites
def registry():
    files = list((repo/'tests').rglob('*.json'))
    files += [p for p in (repo/'tests/resultats').rglob('*') if p.is_file()]
    return {str(p.relative_to(repo)): [hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns] for p in files}
before = registry()
(evidence/'registres-avant-sonde.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
original = subprocess.run
captures = []
def observe(args, *pos, **kw):
    result = original(args, *pos, **kw)
    if isinstance(args, list) and args[:2] == ['codex', 'exec']:
        captures.append({'args': args, 'code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    return result
try:
    versions = suites.cli_versions()
    subprocess.run = observe
    completion = providers.complete('codex', '', 'gpt-6.1-sol', 'Réponds uniquement à la demande.', 'Réponds exactement OK.', 16, 'high')
    (evidence/'sonde-codex.jsonl').write_text(completion.provider_trace, encoding='utf-8', newline='\n')
    assert completion.text.strip() == 'OK'
finally:
    subprocess.run = original
    (evidence/'captures-cli-sonde.json').write_text(json.dumps(captures, ensure_ascii=False, indent=2), encoding='utf-8')
    after = registry()
    (evidence/'registres-apres-sonde.json').write_text(json.dumps(after, indent=2), encoding='utf-8')
    assert before == after, 'Registre modifié pendant la sonde'
assert len(captures) == 1 and captures[0]['code'] == 0
assert 'skill' not in captures[0]['stderr'].lower(), 'Chargement de skill encore signalé : arrêter'
print(json.dumps({'response': 'OK', 'versions': versions, 'identity': 'gpt-6.1-sol : modèle demandé, non attesté', 'no_skill_in_stderr': True, 'registry_unchanged': True}, ensure_ascii=False))
'@
```

## 3. Déplacement, sonde, campagne autorisée et restauration

Avant exécution, renseigner `$taskCampaign` avec la commande **exactement revue
et autorisée par Jo** pour cette fenêtre. Le bloc ci-dessous échoue par défaut ;
il n'est pas une commande de campagne prête à lancer. Ne pas déduire une
autorisation de gel/campagne de l'accord sur la quarantaine.

```powershell
$taskCampaign = { throw 'Commande de campagne gelée et autorisée non renseignée' }
try {
    # Recontrôle immédiat et déplacement local unique, sans -Force.
    Assert-TaskManifest $taskBefore $taskSource
    Move-Item -LiteralPath $taskSource -Destination $taskQuarantine
    if (Test-Path -LiteralPath $taskSource) { throw 'Source encore présente' }
    Assert-TaskManifest $taskBefore $taskQuarantine
    ConvertTo-Json -InputObject @(Get-TaskManifest $taskQuarantine) -Depth 5 |
        Set-Content -LiteralPath (Join-Path $taskEvidence 'manifest-quarantaine.json') -Encoding utf8
    $taskProbeCode | & $taskPython - $taskRepo $taskEvidence
    if ($LASTEXITCODE -ne 0) { throw 'Sonde non concluante ; aucune campagne' }
    # La quarantaine reste active seulement pour la campagne explicitement autorisée.
    & $taskCampaign
    if ($LASTEXITCODE -ne 0) { throw 'Campagne interrompue : restaurer et appliquer les règles A/B' }
} finally {
    # Exécuté aussi si la sonde ou la campagne échoue.
    if (Test-Path -LiteralPath $taskQuarantine) {
        if (Test-Path -LiteralPath $taskSource) { throw 'Source recréée : ne pas écraser ; conserver quarantaine et alerter Jo' }
        Assert-TaskManifest $taskBefore $taskQuarantine
        Move-Item -LiteralPath $taskQuarantine -Destination $taskSource
        Assert-TaskManifest $taskBefore $taskSource
        if (Test-Path -LiteralPath $taskQuarantine) { throw 'Quarantaine encore occupée' }
        ConvertTo-Json -InputObject @(Get-TaskManifest $taskSource) -Depth 5 |
            Set-Content -LiteralPath (Join-Path $taskEvidence 'manifest-restaure.json') -Encoding utf8
        [pscustomobject]@{state='restaure et empreintes verifiees'; source=$taskSource; atUtc=[DateTime]::UtcNow.ToString('o')} |
            ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskEvidence 'RESTAURATION-VERIFIEE.json') -Encoding utf8
    }
}
```

Si la fenêtre est annulée après la sonde, restaurer immédiatement ; ne pas
conserver le skill en quarantaine pour un lancement ultérieur non autorisé.
En cas de fermeture de PowerShell ou panne, `finally` n'est pas garanti : reprendre
les chemins du marqueur `RESTAURATION-REQUISE.json`, contrôler le manifeste,
vérifier que la source est absente, puis effectuer le mouvement de restauration
ci-dessus. Si les deux chemins existent ou si une empreinte diffère : ne rien
écraser, conserver les preuves et demander à Jo de statuer sur la récupération.

## Critères de fin et journal

- Source restaurée à son chemin exact ; destination ne contient plus le skill.
- Inventaire, tailles, SHA-256 et horodatages identiques avant/après restauration.
- Sonde horodatée, trace conservée, aucun chargement de skill dans stderr ; sinon
  aucune campagne autorisée par cette procédure.
- Registres inchangés pendant la sonde. Les écritures de la campagne réelle sont
  ensuite attendues et suivent le registre A/B ; ne pas les confondre avec la sonde.
- Une ligne par déplacement, sonde, début/fin de campagne et restauration dans le
  journal unique, avec SHA runtime et chemins de preuves. En cas d'échec, le noter.
- Conserver les manifestes et marqueurs ; aucune suppression automatique de preuve.

**Statut de cette préparation : aucun dossier déplacé, aucune sonde exécutée
après déplacement, aucune restauration prétendue réalisée, aucun gel/campagne.**
