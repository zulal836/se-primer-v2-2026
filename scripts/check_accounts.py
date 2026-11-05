"""Yalnız mevcut oturumları kontrol eder; token değerlerini asla yazdırmaz."""
import json
import os
import subprocess
import urllib.request

env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'Never'}
token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
if not token:
    try:
        p=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,env=env,timeout=20)
        values=dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
        token=values.get('password')
    except subprocess.TimeoutExpired:
        pass
if token:
    try:
        req=urllib.request.Request('https://api.github.com/user',headers={'Authorization':f'Bearer {token}','User-Agent':'se-primer-v2'})
        with urllib.request.urlopen(req,timeout=30) as r:
            print('GitHub CLI/API oturumu:',json.load(r)['login'])
    except Exception:
        print('GitHub CLI/API oturumu doğrulanamadı')
else:
    print('GitHub CLI/API kimliği yok (connector oturumu bundan bağımsızdır)')
try:
    from huggingface_hub import get_token, HfApi
    if get_token():
        print('Hugging Face:',HfApi().whoami()['name'])
    else:
        print('Hugging Face girişi yok')
except Exception:
    print('Hugging Face oturumu doğrulanamadı')
