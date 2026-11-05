import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_demo import COLUMNS

def merge(paths, output=ROOT / 'data/oturumlar.csv'):
    records = {}
    for path in [output, *map(Path, paths)]:
        if not path.exists():
            raise ValueError(f'Dosya yok: {path}')
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != COLUMNS:
                raise ValueError(f'CSV başlığı uyuşmuyor: {path}')
            for row in reader:
                if row['kaynak'] != 'gerçek':
                    raise ValueError('Gerçek dosyasına sentetik kaynak eklenemez')
                key = row['oturum_id'], row['karar_no']
                old = records.get(key)
                if old and any(old[k] != row[k] for k in COLUMNS if k != 'tamamlandi'):
                    raise ValueError(f'Çelişen kayıt: {key}')
                row['tamamlandi'] = str(max(int(row['tamamlandi']), int(old['tamamlandi']) if old else 0))
                records[key] = row
    with output.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(records.values())
    print(f'{len(records)} benzersiz karar birleştirildi: {output}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Kullanım: python scripts/merge_csv.py dosya1.csv [dosya2.csv ...]')
    merge(sys.argv[1:])
