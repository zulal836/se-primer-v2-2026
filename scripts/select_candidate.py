"""Dış test verisini almayan, yalnız eğitim gruplarında iki sabit aday seçimi."""
import json
from pathlib import Path
import numpy as np
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import balanced_accuracy_score, recall_score

PROTOCOL='group-cv-two-fixed-candidates-v1'

def candidates():
    return {
        'weighted_logistic':make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',C=1,max_iter=1000,random_state=42)),
        'small_tree':DecisionTreeClassifier(max_depth=3,min_samples_leaf=3,class_weight='balanced',random_state=42),
    }

def select(x,y,groups,report_path,data_sha256):
    report_path=Path(report_path)
    if report_path.exists():
        previous=json.loads(report_path.read_text(encoding='utf-8'))
        if previous.get('data_sha256')==data_sha256 and previous.get('protocol')==PROTOCOL:
            raise ValueError('Bu veri/protokol zaten çalıştırıldı; dış test yeniden değerlendirilmez. Mevcut raporu kullanın.')
    splits=list(StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=42).split(x,y,groups))
    scores={}
    for name,estimator in candidates().items():
        folds=[]
        for index,(tr,va) in enumerate(splits,1):
            assert not set(groups[tr])&set(groups[va]),'CV oturum sızıntısı'
            if len(set(y[tr]))<2 or len(set(y[va]))<2:
                raise ValueError('Önceden sabitlenen CV katında iki sınıf yok; protokol değiştirilmeden duruldu')
            model=clone(estimator).fit(x[tr],y[tr])
            assert model.classes_.tolist()==[0,1]
            pred=(model.predict_proba(x[va])[:,1]>=.5).astype(int)
            folds.append(dict(fold=index,train_sessions=len(set(groups[tr])),validation_sessions=len(set(groups[va])),validation_class_counts=np.bincount(y[va],minlength=2).tolist(),session_overlap=0,balanced_accuracy=float(balanced_accuracy_score(y[va],pred)),recall_ayrintili=float(recall_score(y[va],pred,zero_division=0))))
        scores[name]=dict(folds=folds,mean_balanced_accuracy=float(np.mean([f['balanced_accuracy'] for f in folds])),mean_recall_ayrintili=float(np.mean([f['recall_ayrintili'] for f in folds])))
    selected=max(scores,key=lambda name:(scores[name]['mean_balanced_accuracy'],scores[name]['mean_recall_ayrintili'],name=='weighted_logistic'))
    report=dict(protocol=PROTOCOL,data_sha256=data_sha256,seed=42,cv='StratifiedGroupKFold(5, shuffle=True, random_state=42)',selection_rule='mean balanced accuracy, then mean recall, then logistic',candidates=scores,selected=selected,test_evaluations=0,holdout_previously_seen_by_baseline=True)
    report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return clone(candidates()[selected]).fit(x,y),report
