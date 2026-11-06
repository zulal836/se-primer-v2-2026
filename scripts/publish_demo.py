"""Yalnız açıkça işaretlenmiş 0.1.0-demo SENTETİK GELİŞTİRME DEMOSU yayını.

Gerçek model yayın kapısını veya config.publishable değerini değiştirmez.
"""
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from huggingface_hub import HfApi, get_token, hf_hub_download
from jsonschema import validate

ROOT=Path(__file__).resolve().parents[1]
FILES=['model.onnx','config.json','README.md','config.schema.json']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_demo(root=ROOT):
    folder=root/'model'
    config=json.loads((folder/'config.json').read_text(encoding='utf-8'))
    validate(config,json.loads((folder/'config.schema.json').read_text(encoding='utf-8')))
    if config['version']!='0.1.0-demo' or config['data_source']!='sentetik' or config['publishable'] is not False:
        raise ValueError('Bu komut yalnız publishable=false, sentetik 0.1.0-demo içindir; gerçek model yayımlayamaz.')
    if sha(folder/'model.onnx')!=config['model_sha256']:
        raise ValueError('Demo model hash uyuşmazlığı')
    for name in ['model.onnx','config.json']:
        if (folder/name).read_bytes()!=(root/'public/model'/name).read_bytes():
            raise ValueError(f'Paket/public demo dosyası uyuşmuyor: {name}')
    card=(folder/'README.md').read_text(encoding='utf-8')
    if 'SENTETİK GELİŞTİRME DEMOSU' not in card:
        raise ValueError('Model kartında açık SENTETİK GELİŞTİRME DEMOSU etiketi gerekli')
    return config

def publish(args):
    c=check_demo()
    before={name:sha(ROOT/'model'/name) for name in FILES}
    print('Yayın türü: SENTETİK GELİŞTİRME DEMOSU. Gerçek model kabul edilmedi; publishable=false korunacak.')
    print('Sentetik metrikler:',json.dumps(c['metrics'],ensure_ascii=False))
    if not args.push:
        print('Ön kontrol geçti. Yeni public demo deposuna yükleme için --push kullanın.')
        return
    if not get_token():
        raise ValueError('HF girişi yok. Proje terminalinde .venv/Scripts/hf.exe auth login çalıştırın; token sohbete yazılmaz.')
    api=HfApi()
    owner=api.whoami()['name']
    repo=args.repo or f'{owner}/se-primer-v2-synthetic-demo'
    if not repo.startswith(owner+'/') or 'demo' not in repo.split('/')[-1].lower():
        raise ValueError('Hedef kendi hesabınızda yeni ve adında demo geçen bir depo olmalı.')
    api.create_repo(repo,repo_type='model',private=False,exist_ok=False)
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        for name in FILES:
            shutil.copy2(ROOT/'model'/name,Path(temp)/name)
        commit=api.upload_folder(repo_id=repo,repo_type='model',folder_path=temp,commit_message='SYNTHETIC DEVELOPMENT DEMO 0.1.0-demo; not an accepted real-user model')
    revision=commit.oid
    receipt=dict(repo=repo,commit=revision,mode='hf-pinned-synthetic-demo',publication_kind='SENTETİK GELİŞTİRME DEMOSU',final_real_model_accepted=False,config_publishable=c['publishable'],files_sha256=before)
    # Yükleme başarılı ama anonim kontrol engellenirse gerçek commit kaybolmaz.
    (ROOT/'release-demo.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf-8')
    for name in FILES:
        downloaded=Path(hf_hub_download(repo,name,revision=revision,token=False,force_download=True))
        if sha(downloaded)!=before[name]:
            raise ValueError(f'Anonim indirilen demo dosyası uyuşmuyor: {name}')
    if {name:sha(ROOT/'model'/name) for name in FILES}!=before:
        raise ValueError('Yerel demo dosyası yayın sırasında değişti')
    manifest=dict(repo=repo,commit=revision,mode='hf-pinned-synthetic-demo')
    (ROOT/'public/model/source.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    receipt['anonymous_download_verified']=True
    (ROOT/'release-demo.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'https://huggingface.co/{repo}/resolve/{revision}/model.onnx')
    print('Demo/config/kart aynı commit’te; web sabit commit manifestine bağlandı. Gerçek yayın kapısı değiştirilmedi.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--push',action='store_true')
    p.add_argument('--repo',help='Yeni, kendi hesabınızdaki public demo deposu; verilmezse kullanıcı/se-primer-v2-synthetic-demo')
    try:
        publish(p.parse_args())
    except ValueError as error:
        sys.exit(str(error))
    except Exception as error:
        status=getattr(getattr(error,'response',None),'status_code',None)
        sys.exit(f'Demo yayını durdu: {type(error).__name__}, HTTP={status}. Erişim/giriş adımını kontrol edin; otomatik tekrar yapılmadı.')
