import hashlib
import json
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base='https://zulal836.github.io/se-primer-v2-2026/'
def get(path,method='GET'):
    req=urllib.request.Request(base+path,method=method,headers={'User-Agent':'se-primer-v2-public-check'})
    with urllib.request.urlopen(req,timeout=90) as r:
        return r.status,dict(r.headers),r.read()
status,_,html=get('')
assert status==200 and b'lang="tr"' in html
_,_,body=get('model/model.onnx')
sha=hashlib.sha256(body).hexdigest()
config=json.loads(get('model/config.json')[2])
assert sha==config['model_sha256']==hashlib.sha256((ROOT/'model/model.onnx').read_bytes()).hexdigest()
status,headers,_=get('demo.mp4','HEAD')
assert status==200 and headers.get('Content-Type','').startswith('video/mp4')
result={'app':base,'app_http':200,'demo':base+'demo.mp4','demo_http':status,'model_sha256':sha,'no_auth_headers_sent':True}
(ROOT/'test-results/public-http.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
