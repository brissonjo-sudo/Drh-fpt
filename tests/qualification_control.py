"""Gel humain et abandon technique explicites ; aucun appel de modèle."""
import argparse
import json
from pathlib import Path
import campaign
import suites


def main(argv=None):
    parser=argparse.ArgumentParser();commands=parser.add_subparsers(dest='command',required=True)
    seal=commands.add_parser('freeze');seal.add_argument('--suite',required=True);seal.add_argument('--approval',required=True)
    abort=commands.add_parser('abandon');abort.add_argument('--suite',required=True)
    abort.add_argument('--kind',choices=['interruption','execution_error','runtime_changed'],required=True)
    abort.add_argument('--reason',required=True)
    args=parser.parse_args(argv)
    if args.command=='freeze':
        registry=json.loads((suites.HERE/'suites.json').read_text(encoding='utf8'))['suites']
        spec=registry.get(args.suite,{})
        if not spec.get('qualification'):raise SystemExit('Suite de qualification attendue')
        approval=json.loads(Path(args.approval).read_text(encoding='utf8'))
        state=campaign.git_provenance(campaign.ROOT)
        if state.get('dirty') is not False or state.get('commit')!=approval.get('runtime_commit'):
            raise SystemExit('Commit candidat propre différent de l’approbation')
        if any(x.get('cli_versions')!=suites.cli_versions() for x in approval.get('profiles',{}).values()):
            raise SystemExit('Versions CLI différentes de l’approbation')
        suites.freeze(suites.HERE/spec['path'],approval,suites.HERE/spec['seal'])
        print('Jeu gelé après approbation explicite de Jo : '+args.suite)
    else:
        suite=suites.load_suite(args.suite)
        suites.abandon_game(suite,campaign.RESULTS/'qualification-launches.json',campaign.RESULTS,
            args.kind,args.reason,new_commit=campaign.git_provenance(campaign.ROOT).get('commit'))
        print('Jeu consommé, non qualifié ; preuves conservées : '+args.suite)
    return 0


if __name__=='__main__':raise SystemExit(main())
