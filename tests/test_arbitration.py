import copy
import hashlib
import json
import unittest
import arbitration
import campaign
from test_harness import successful_result


class ArbitrationTests(unittest.TestCase):
    def setUp(self):
        self.case={'id':'A01','attendus':[{'id':'c1','texte':'critère obligatoire'}]}
        self.judge=successful_result(self.case['attendus'])
        self.binding={'suite_sha256':'a'*64,'answer_sha256':'b'*64,'judge_sha256':'c'*64}

    def decision(self,target,value):
        return {**self.binding,'case_id':'A01','target':target,'decision':value,
                'reviewer':'Jo','confirmed':True,'decided_at':'2026-10-12T12:00:00+02:00',
                'reason':'Motif métier explicite','sources':['https://www.legifrance.gouv.fr/codes/article_lc/id'],
                'evidence':'message humain confirmé'}

    def test_raw_fail_can_be_arbitrated_without_rewriting_original(self):
        self.judge['criteres'][0]['statut']='PARTIEL'
        original=copy.deepcopy(self.judge)
        result=arbitration.assess(self.judge,self.case,self.binding,[self.decision('criterion:c1','satisfied')])
        self.assertFalse(result['raw_pass'])
        self.assertTrue(result['arbitrated_pass'])
        self.assertEqual(original,self.judge)

    def test_absent_pending_or_wrong_binding_cannot_clear_failure(self):
        self.judge['criteres'][0]['statut']='ABSENT'
        for decisions in [[],[{**self.decision('criterion:c1','satisfied'),'confirmed':False}],
                          [{**self.decision('criterion:c1','satisfied'),'answer_sha256':'z'*64}]]:
            self.assertFalse(arbitration.assess(self.judge,self.case,self.binding,decisions)['arbitrated_pass'])

    def test_human_cannot_clear_invalid_structure_or_truncation(self):
        for field,value in [('tronque',True),('criteres',[]),('score_sur_5',99)]:
            broken={**self.judge,field:value}
            result=arbitration.assess(broken,self.case,self.binding,[self.decision('criterion:c1','satisfied')])
            self.assertFalse(result['integrity_pass'])
            self.assertFalse(result['arbitrated_pass'])

    def test_legal_error_requires_individual_human_resolution(self):
        self.judge.update({'erreurs':['Règle potentiellement fausse'],'verdict':'ECHEC',
                           'verdict_fiabilite_juridique':'ECHEC'})
        unresolved=arbitration.assess(self.judge,self.case,self.binding,[])
        self.assertFalse(unresolved['arbitrated_pass'])
        resolved=[self.decision('error:0','false_positive'),
                  self.decision('verdict','satisfied'),self.decision('legal_verdict','satisfied')]
        self.assertTrue(arbitration.assess(self.judge,self.case,self.binding,resolved)['arbitrated_pass'])
        resolved[0]['decision']='confirmed_error'
        self.assertFalse(arbitration.assess(self.judge,self.case,self.binding,resolved)['arbitrated_pass'])

    def test_style_scores_indicative_when_obligations_satisfied(self):
        self.judge['score_sur_5']=1
        self.assertTrue(arbitration.assess(self.judge,self.case,self.binding,[])['raw_pass'])

    def test_legal_doubt_blocks_until_human_resolution(self):
        self.judge['incertitudes']=['Portée FPT incertaine']
        self.assertFalse(arbitration.assess(self.judge,self.case,self.binding,[])['arbitrated_pass'])
        self.assertTrue(arbitration.assess(self.judge,self.case,self.binding,[self.decision('doubt:0','false_positive')])['arbitrated_pass'])


if __name__=='__main__':unittest.main()
