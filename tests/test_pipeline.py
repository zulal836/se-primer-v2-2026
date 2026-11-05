import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
os.environ['PYTHONUTF8']='1'
sys.path.insert(0,str(ROOT))
import train
from scripts.merge_csv import merge
from scripts.generate_demo import COLUMNS

class PipelineTests(unittest.TestCase):
    def test_real_data_empty_rejects_without_modifying_artifact(self):
        before=train.digest(ROOT/'model/model.onnx')
        p=subprocess.run([sys.executable,str(ROOT/'train.py')],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0)
        self.assertIn('15',p.stderr)
        self.assertEqual(before,train.digest(ROOT/'model/model.onnx'))

    def test_publication_rejects_synthetic(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/publish_model.py'),'unused/unused'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0)
        self.assertIn('Nihai',p.stderr)

    def test_split_has_no_session_overlap_and_metrics_pass(self):
        c=json.loads((ROOT/'model/config.json').read_text(encoding='utf-8'))
        self.assertFalse(set(c['split']['train_sessions'])&set(c['split']['test_sessions']))
        self.assertGreaterEqual(c['metrics']['balanced_accuracy'],.70)
        self.assertGreaterEqual(c['metrics']['recall_ayrintili'],.65)
        self.assertLessEqual(c['metrics']['onnx_max_abs_diff'],1e-4)
        self.assertEqual(c['data_source'],'sentetik')
        self.assertFalse(c['publishable'])

    def test_low_quality_labels_fail_eval_without_modifying_artifact(self):
        import random
        rng=random.Random(17)
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            path=Path(temp)/'noise.csv'
            with (ROOT/'data/sentetik.csv').open(encoding='utf-8') as f:
                rows=list(csv.DictReader(f))
            for r in rows:
                r['ayrinti_istegi']=str(rng.randrange(2))
            with path.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows(rows)
            before=train.digest(ROOT/'model/model.onnx')
            p=subprocess.run([sys.executable,str(ROOT/'train.py'),'--demo','--data',str(path)],capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(p.returncode,0)
            self.assertIn('Eval',p.stderr)
            self.assertEqual(before,train.digest(ROOT/'model/model.onnx'))

    def test_merge_deduplicates_upgrades_and_rejects_conflict(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            folder=Path(temp);out=folder/'out.csv';incoming=folder/'in.csv'
            row=dict(zip(COLUMNS,['random-test-session',1,10,0,0,1,0,'yeni','Geliştirici','Test stratejisi','gerçek',0]))
            def write(path,items):
                with path.open('w',encoding='utf-8',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows(items)
            write(out,[row]);row['tamamlandi']=1;write(incoming,[row]);merge([incoming],out)
            with out.open(encoding='utf-8') as f:
                result=list(csv.DictReader(f))
            self.assertEqual(len(result),1);self.assertEqual(result[0]['tamamlandi'],'1')
            row['secim']=1;write(incoming,[row])
            with self.assertRaises(ValueError):merge([incoming],out)

    def test_constant_class_and_mixed_source_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            path=Path(temp)/'bad.csv'
            with (ROOT/'data/sentetik.csv').open(encoding='utf-8') as f:
                rows=list(csv.DictReader(f))
            for r in rows:r['ayrinti_istegi']='0'
            def write():
                with path.open('w',encoding='utf-8',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows(rows)
            write()
            with self.assertRaisesRegex(ValueError,'sınıfta'):train.load_data(path,'sentetik')
            rows[0]['kaynak']='gerçek';write()
            with self.assertRaisesRegex(ValueError,'Kaynak'):train.load_data(path,'sentetik')

if __name__=='__main__':unittest.main()
