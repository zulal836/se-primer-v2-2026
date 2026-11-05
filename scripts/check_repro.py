import json
import os
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from train import digest
paths=['model/model.onnx','model/config.json','tests/parite.json']
before={p:digest(ROOT/p) for p in paths}
subprocess.run([sys.executable,'train.py','--demo'],cwd=ROOT,check=True,env={**os.environ,'PYTHONUTF8':'1'})
after={p:digest(ROOT/p) for p in paths}
assert before==after,'Tekrarlanabilirlik uyuşmazlığı'
(ROOT/'test-results').mkdir(exist_ok=True)
(ROOT/'test-results/reproducibility.json').write_text(json.dumps({'identical':True,'before':before,'after':after},indent=2),encoding='utf-8')
print('İkinci eğitimde model, config ve oracle dosyaları bayt düzeyinde aynı.')
