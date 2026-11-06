"""Mevcut train.py sonucunu ve artefakt korumasını kaydeder; kapı değiştirmez."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
paths=['model/model.onnx','model/config.json','model/README.md',
       'public/model/model.onnx','public/model/config.json','public/model/source.json','tests/parite.json','public/demo.mp4']
def snapshot():
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
before=snapshot()
result=subprocess.run([sys.executable,'train.py'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONUTF8':'1'})
after=snapshot()
report={'date':'2026-11-06','command':'python train.py','exit_code':result.returncode,
        'stdout':result.stdout.strip(),'stderr':result.stderr.strip(),
        'artifacts_unchanged':before==after,'before':before,'after':after}
(ROOT/'test-results/real-training-attempt.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('before','after')},indent=2,ensure_ascii=False))
if result.returncode and before!=after:
    sys.exit('HATA: başarısız eğitim artefakt değiştirdi')
