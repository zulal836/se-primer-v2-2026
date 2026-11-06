import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.select_candidate import select,PROTOCOL,candidates

class FinalProtocolTests(unittest.TestCase):
    def test_selected_by_cv_only_and_single_holdout_evaluation(self):
        r=json.loads((ROOT/'test-results/final-model-selection.json').read_text(encoding='utf-8'))
        expected=max(r['candidates'],key=lambda n:(r['candidates'][n]['mean_balanced_accuracy'],r['candidates'][n]['mean_recall_ayrintili'],n=='weighted_logistic'))
        self.assertEqual(r['selected'],expected)
        self.assertEqual(r['test_evaluations'],1)
        self.assertEqual(r['outer_session_overlap'],0)
        audit=json.loads((ROOT/'test-results/real-data-audit.json').read_text(encoding='utf-8'))
        self.assertEqual(r['data_sha256'],audit['merged_sha256'])
        for c in r['candidates'].values():
            self.assertEqual(len(c['folds']),5)
            self.assertTrue(all(f['session_overlap']==0 for f in c['folds']))

    def test_repeat_blocked_before_fitting(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            path=Path(tmp)/'report.json'
            path.write_text(json.dumps(dict(data_sha256='same',protocol=PROTOCOL)),encoding='utf-8')
            before=path.read_bytes()
            with self.assertRaisesRegex(ValueError,'yeniden değerlendirilmez'):
                select(np.empty((0,3)),np.array([]),np.array([]),path,'same')
            self.assertEqual(path.read_bytes(),before)

    def test_fixed_candidate_parameters(self):
        models=candidates()
        self.assertEqual(set(models),{'weighted_logistic','small_tree'})
        self.assertEqual(models['weighted_logistic'][-1].class_weight,'balanced')
        self.assertEqual(models['small_tree'].class_weight,'balanced')
        self.assertEqual(models['small_tree'].max_depth,3)
        self.assertEqual(models['small_tree'].min_samples_leaf,3)

if __name__=='__main__':unittest.main()
