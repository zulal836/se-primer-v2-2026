"""Yalnız kapıyı geçen gerçek veri modelini, iki dosyayı aynı HF commit'ine yükler."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download
from jsonschema import validate

ROOT=Path(__file__).resolve().parents[1]

def check():
    c=json.loads((ROOT/'model/config.json').read_text(encoding='utf-8'))
    validate(c,json.loads((ROOT/'model/config.schema.json').read_text(encoding='utf-8')))
    if not c['publishable'] or c['data_source']!='gerçek':
        raise ValueError('Nihai yayın reddedildi: en az 15 gerçek tamamlanmış oturumla eğitilmiş, kapıyı geçen model gerekli')
    if c['metrics']['balanced_accuracy']<.70 or c['metrics']['recall_ayrintili']<.65:
        raise ValueError('Eval kapısı geçilmemiş')
    if set(c['split']['train_sessions'])&set(c['split']['test_sessions']):
        raise ValueError('Split sızıntısı')
    if hashlib.sha256((ROOT/'model/model.onnx').read_bytes()).hexdigest()!=c['model_sha256']:
        raise ValueError('Model hash uyuşmazlığı')
    return c

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('repo',help='HF kullanıcı/yeni-proje-adı');p.add_argument('--push',action='store_true');args=p.parse_args()
    try:
        c=check()
        if not args.push:
            print('Ön kontrol geçti. Yüklemek için --push ekleyin.');sys.exit(0)
        api=HfApi();api.whoami()
        api.create_repo(args.repo,repo_type='model',private=False,exist_ok=False)
        commit=api.upload_folder(repo_id=args.repo,folder_path=ROOT/'model',commit_message='Primer v2: gerçek veri, eval kapısını geçen model')
        sha=commit.oid
        for name in ['model.onnx','config.json']:
            downloaded=Path(hf_hub_download(args.repo,name,revision=sha))
            if downloaded.read_bytes()!=(ROOT/'model'/name).read_bytes():
                raise ValueError('Yüklenen dosya uyuşmuyor')
        manifest={'repo':args.repo,'commit':sha,'mode':'hf-pinned'}
        (ROOT/'public/model/source.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
        (ROOT/'release-model.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
        print(f'https://huggingface.co/{args.repo}/resolve/{sha}/model.onnx')
        print('Web manifesti güncellendi; build ve pariteyi tekrar çalıştırıp yayınlayın.')
    except Exception as e:
        sys.exit(f'Yayın durduruldu: {e}')
