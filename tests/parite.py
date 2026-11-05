import hashlib
import json
from pathlib import Path
import numpy as np
import onnxruntime as ort

ROOT=Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    refs=json.loads((ROOT/'tests/parite.json').read_text())
    assert hashlib.sha256((ROOT/'model/model.onnx').read_bytes()).hexdigest()==refs['model_sha256'], 'Oracle model hash uyuşmazlığı'
    session=ort.InferenceSession(str(ROOT/'model/model.onnx'),providers=['CPUExecutionProvider'])
    for case in refs['cases']:
        p=float(session.run(None,{'features':np.array([case['input']],dtype=np.float32)})[1][0,1])
        assert abs(p-case['probability'])<refs['tolerance']
        print(case['input'], p)
    print('5 Python ONNX parite kontrolü geçti.')
