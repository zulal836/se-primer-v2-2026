"""Yalnız sentetik geliştirme verisi; insan ihtiyacı veya gerçek oturum değildir."""
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ['oturum_id','karar_no','bekleme_sn','degistirme_sayisi','ipucu_sayisi','ayrinti_istegi','secim','seviye','rol','hedef','kaynak','tamamlandi']

def main():
    rng = random.Random(42)
    path = ROOT / 'data/sentetik.csv'
    path.parent.mkdir(exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for session in range(160):
            for scene in range(1, 4):
                wait = round(rng.uniform(1, 130), 3)
                changes = rng.randrange(7)
                hints = rng.randrange(4)
                # Gizli simülasyon tercihi ve %8 gürültü; gerçek insan etiketi değildir.
                score = wait / 65 + changes / 2 + hints * .9
                label = int(score > 3.8)
                if rng.random() < .08:
                    label = 1 - label
                writer.writerow(dict(zip(COLUMNS, [f'syn-{session:04}',scene,wait,changes,hints,label,rng.randrange(2),'yeni','Geliştirici','Test stratejisi','sentetik',1])))
    print(f'Sentetik veri: {path}, 160 oturum / 480 karar')

if __name__ == '__main__':
    main()
