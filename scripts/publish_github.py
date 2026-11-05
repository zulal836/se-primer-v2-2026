"""Yeni proje deposu + GitHub Pages. Mevcut başka depoları değiştirmez."""
import argparse
import csv
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ENV={**os.environ,'GIT_TERMINAL_PROMPT':'0','GCM_INTERACTIVE':'Never'}

def git(*args, capture=False):
    return subprocess.run(['git',*args],cwd=ROOT,env=ENV,check=True,text=True,capture_output=capture)

def main():
    p=argparse.ArgumentParser();p.add_argument('--name',default='se-primer-v2-2026');p.add_argument('--push',action='store_true');args=p.parse_args()
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        c=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,env=ENV,timeout=20)
        token=dict(line.split('=',1) for line in c.stdout.splitlines() if '=' in line).get('password')
    if not token:raise ValueError('GitHub CLI/API kimliği yok; git credential manager veya GH_TOKEN ile giriş gerekli')
    def api(path,method='GET',data=None):
        req=urllib.request.Request('https://api.github.com'+path,method=method,data=None if data is None else json.dumps(data).encode(),headers={'Authorization':f'Bearer {token}','User-Agent':'se-primer-v2','Accept':'application/vnd.github+json','Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=60) as r:
            content=r.read()
            return json.loads(content) if content else {}
    who=api('/user');owner=who['login'];repo=f'{owner}/{args.name}'
    print(f'Hedef yeni public depo: {repo}; Pages: GitHub Actions; ücretli servis yok.')
    if not args.push:return
    try:
        api(f'/repos/{repo}')
    except urllib.error.HTTPError as e:
        if e.code!=404:raise
    else:raise ValueError('Bu depo zaten var; mevcut depoyu değiştirmemek için duruldu')
    if not (ROOT/'dist/index.html').exists():raise ValueError('Önce build ve testleri çalıştırın')
    # Ham gerçek veri public commit'e girmez.
    api('/user/repos','POST',{'name':args.name,'private':False,'description':'Türkçe yazılım mühendisliği oyunu · ONNX davranış modeli · sentetik geliştirme demosu'})
    if not (ROOT/'.git').exists():git('init','-b','main')
    git('config','user.name',owner)
    git('config','user.email',f'{who["id"]}+{owner}@users.noreply.github.com')
    git('add','.')
    staged=git('diff','--cached','--name-only',capture=True).stdout.splitlines()
    if any(x.startswith('private-data/') or x=='data/oturumlar.csv' or x=='.env' for x in staged):
        raise ValueError('Özel veri staged; yayın durduruldu')
    git('commit','-m','Build SE Primer v2 with consent collection, ONNX demo and verified tests')
    git('remote','add','origin',f'https://github.com/{repo}.git')
    git('push','-u','origin','main')
    try:
        pages=api(f'/repos/{repo}/pages','POST',{'build_type':'workflow'})
        print('Pages etkin:',pages.get('html_url','Yayın workflow sonucu bekleniyor'))
    except urllib.error.HTTPError as e:
        print(f'Pages API HTTP {e.code}; Settings > Pages > GitHub Actions seçin.')
    result={'github':f'https://github.com/{repo}','expected_app':f'https://{owner}.github.io/{args.name}/','commit':git('rev-parse','HEAD',capture=True).stdout.strip(),'status':'pushed; Pages workflow completion not yet verified'}
    (ROOT/'publication.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:sys.exit(f'GitHub yayın durdu: {e}')
