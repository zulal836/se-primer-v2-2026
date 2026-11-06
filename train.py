"""Tekrarlanabilir eğitim: gerçek veri varsayılan; --demo sentetik geliştirme."""
import argparse
import csv
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
import numpy as np
import onnxruntime as ort
from jsonschema import validate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, recall_score, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

ROOT = Path(__file__).parent.resolve()
FEATURES = ['bekleme_sn','degistirme_sayisi','ipucu_sayisi']
THRESHOLDS = {'balanced_accuracy': .70, 'recall_ayrintili': .65, 'onnx_max_abs_diff': 1e-4}
REFERENCE = [[2,0,0],[100,5,3],[30,1,0],[65,2,1],[15,0,2]]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_data(path, source):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    if any(r['kaynak'] != source for r in rows):
        raise ValueError('Kaynaklar karışık veya beklenen kaynakla uyuşmuyor')
    sessions = {}
    seen = set()
    for r in rows:
        key = (r['oturum_id'], int(r['karar_no']))
        if not key[0] or key[1] not in (1,2,3) or key in seen:
            raise ValueError('Geçersiz veya yinelenen oturum/karar')
        seen.add(key)
        if r['tamamlandi'] not in ('0','1') or r['ayrinti_istegi'] not in ('','0','1'):
            raise ValueError('Tamamlanma veya etiket geçersiz')
        values = [float(r[k]) for k in FEATURES]
        if any(not np.isfinite(v) or v < 0 or v > cap for v, cap in zip(values,[300,20,10])):
            raise ValueError('Özellik sınırı aşıldı')
        if any(v != int(v) for v in values[1:]):
            raise ValueError('Davranış sayımları tam sayı olmalı')
        sessions.setdefault(key[0], []).append(r)
    complete = {k:v for k,v in sessions.items() if len(v)==3 and all(r['tamamlandi']=='1' for r in v)}
    if len(complete) < 15:
        raise ValueError(f'En az 15 tamamlanmış {source} oturum gerekli; bulunan: {len(complete)}')
    labeled = [r for group in complete.values() for r in group if r['ayrinti_istegi']!='']
    x = np.array([[float(r[k]) for k in FEATURES] for r in labeled], dtype=np.float32)
    y = np.array([int(r['ayrinti_istegi']) for r in labeled])
    groups = np.array([r['oturum_id'] for r in labeled])
    if len(y)==0 or min(np.bincount(y, minlength=2)) < 10:
        raise ValueError('Her sınıfta en az 10 etiketli karar gerekli')
    return x,y,groups

def run(args):
    source = 'sentetik' if args.demo else 'gerçek'
    data = args.data or ROOT / ('data/sentetik.csv' if args.demo else 'data/oturumlar.csv')
    x,y,groups = load_data(data, source)
    train,test = next(GroupShuffleSplit(n_splits=1, test_size=.25, random_state=42).split(x,y,groups))
    if set(groups[train]) & set(groups[test]):
        raise ValueError('Oturum sızıntısı')
    if min(np.bincount(y[test], minlength=2)) < 5 or len(set(y[train])) != 2:
        raise ValueError('Sabit split sınıf sayıları yetersiz; daha fazla gerçek veri toplayın')
    selection_report=None
    if getattr(args,'compare',False):
        if args.demo:
            raise ValueError('Son karşılaştırma yalnız gerçek veri içindir')
        from scripts.select_candidate import select
        model,selection_report=select(x[train],y[train],groups[train],ROOT/'test-results/final-model-selection.json',digest(data))
    else:
        model = make_pipeline(StandardScaler(), LogisticRegression(random_state=42, max_iter=1000))
        model.fit(x[train],y[train])
    assert model.classes_.tolist()==[0,1], 'Sınıf sırası uyuşmazlığı'
    pred = (model.predict_proba(x[test])[:,1] >= .5).astype(int)
    metrics = {'balanced_accuracy':float(balanced_accuracy_score(y[test],pred)), 'recall_ayrintili':float(recall_score(y[test],pred)), 'confusion_matrix':confusion_matrix(y[test],pred).tolist()}
    if selection_report is not None:
        selection_report.update(test_evaluations=1,test_metrics=metrics,train_sessions=len(set(groups[train])),test_sessions=len(set(groups[test])),train_class_counts=np.bincount(y[train],minlength=2).tolist(),test_class_counts=np.bincount(y[test],minlength=2).tolist(),outer_session_overlap=0,gate_passed=metrics['balanced_accuracy']>=.70 and metrics['recall_ayrintili']>=.65)
        (ROOT/'test-results/final-model-selection.json').write_text(json.dumps(selection_report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(metrics, indent=2))
    if metrics['balanced_accuracy'] < .70 or metrics['recall_ayrintili'] < .65:
        raise ValueError('Eval kapısı geçilemedi; mevcut artefaktlar korunuyor')
    classifier=model[-1] if hasattr(model,'steps') else model
    onnx = convert_sklearn(model, name='primer_help_v1', initial_types=[('features',FloatTensorType([None,3]))], options={id(classifier):{'zipmap':False}}, target_opset=17)
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        stage = Path(temp)
        (stage/'model.onnx').write_bytes(onnx.SerializeToString())
        session = ort.InferenceSession(str(stage/'model.onnx'), providers=['CPUExecutionProvider'])
        actual = session.run(None, {'features':x})[1]
        metrics['onnx_max_abs_diff'] = float(np.max(np.abs(actual-model.predict_proba(x))))
        if metrics['onnx_max_abs_diff'] > 1e-4:
            raise ValueError('ONNX parite kapısı geçilemedi')
        config = dict(version='0.1.0-demo' if args.demo else '2.0.0', data_source=source, input_name='features', features=[dict(name=n,dtype='float32',min=0,max=cap) for n,cap in zip(FEATURES,[300,20,10])], classes=['kisa','ayrintili'], metrics=metrics, thresholds=THRESHOLDS, decision_threshold=.5, split=dict(seed=42,train_sessions=sorted(set(groups[train])),test_sessions=sorted(set(groups[test])),test_class_counts=np.bincount(y[test],minlength=2).tolist()),model_sha256=digest(stage/'model.onnx'),data_sha256=digest(data),publishable=not args.demo)
        validate(config,json.loads((ROOT/'model/config.schema.json').read_text(encoding='utf-8')))
        # Oturum kimlikleri sadece rastgele/sentetik teknik kimliklerdir; kişi bilgisi değildir.
        (stage/'config.json').write_text(json.dumps(config,indent=2,ensure_ascii=False),encoding='utf-8')
        card = f'''---
license: mit
library_name: sklearn
tags: [onnx, education, tabular-classification]
---
# Son Boş Randevu model kartı

Amaç: üç davranış girdisinden kısa/ayrıntılı açıklama seçmek; klinik karar veya öğrenci notu değildir.

Sürüm: {config['version']}. Kaynak: **{source}**. {'SENTETİK DEMO: gerçek insan ihtiyacıyla doğrulanmamıştır; nihai yayına uygun değildir.' if args.demo else 'Oyuncuların yardım öncesi gönüllü öz bildirimi; öğrenme etkisi henüz ölçülmedi.'}

Değerlendirme: oturum bazlı %25 holdout, seed=42; {len(set(groups[train]))} eğitim / {len(set(groups[test]))} test oturumu. Balanced accuracy={metrics['balanced_accuracy']:.6f}, ayrıntılı recall={metrics['recall_ayrintili']:.6f}. ONNX maksimum fark={metrics['onnx_max_abs_diff']:.10g}.

Kabul eşiği: balanced accuracy >=0.70 ve recall >=0.65. Eşik önceden spec.md'de tanımlıdır. Olasılık eşiği 0.5; kalibrasyon garantisi yoktur. Kural tabanlı yedek kullanılabilir.

Sınırlar: öz bildirim yanlılığı, küçük örneklem, farklı cihazların süre ölçümü ve tekrar oynama etkisi. Sentetik veri üreticisi davranış ile etiket ilişkisini kurgular; yüksek puan insan genellemesini göstermez. Oturum ayrımı kişi ayrımı değildir, aynı insan iki split'te bulunabilir. Arayüz beklenti etkisi yaratabilir. İnsan öğrenme çıktısını ayrıca ölçmek gerekir.

Kullanılmaması gereken durumlar: sağlık/klinik karar, kişilik çıkarımı, sınav puanlama, öğrenci eleme, hassas veri işleme. Model ve eğitim kodu public olabilir; kişiler hakkında hüküm verilemez.

Özellik sırası/tipi, sınıflar ve veri/model hash'leri config.json sözleşmesindedir. JSON şeması eğitimde doğrulanır. Kaynak yaklaşım: https://github.com/seyyah/huggingface-hello-web ; yeni oyun ve eğitim bağımsız hazırlanmıştır.
'''
        (stage/'README.md').write_text(card, encoding='utf-8')
        target=ROOT/'model'
        for name in ['model.onnx','config.json','README.md']:
            shutil.copy2(stage/name,target/name)
        public=ROOT/'public/model'
        public.mkdir(parents=True,exist_ok=True)
        for name in ['model.onnx','config.json']:
            shutil.copy2(stage/name,public/name)
        (public/'source.json').write_text(json.dumps({'repo':None,'commit':None,'mode':'local-demo' if args.demo else 'local-candidate'}),encoding='utf-8')
        probabilities = session.run(None,{'features':np.array(REFERENCE,dtype=np.float32)})[1][:,1]
        (ROOT/'tests/parite.json').write_text(json.dumps({'model_sha256':config['model_sha256'],'tolerance':1e-4,'cases':[{'input':v,'probability':float(p)} for v,p in zip(REFERENCE,probabilities)]},indent=2),encoding='utf-8')
    print('Eval ve ONNX kapısı geçti. ' + ('Yalnız yerel SENTETİK DEMO.' if args.demo else 'Gerçek veri adayı hazır; yayın ayrı komutla yapılır.'))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--demo',action='store_true')
    parser.add_argument('--data',type=Path)
    parser.add_argument('--compare',action='store_true',help='Yalnız eğitim oturumlarında önceden sabitlenmiş iki aday CV seçimi')
    args=parser.parse_args()
    try:
        run(args)
    except (ValueError,FileNotFoundError,KeyError) as exc:
        sys.exit(f'Eğitim durduruldu: {exc}')
