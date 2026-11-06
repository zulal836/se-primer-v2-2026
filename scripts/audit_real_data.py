"""Ham cevapları değiştirmeden denetler, mevcut birleştiriciyi kullanır.

Public rapora yalnız toplamlar yazılır; oturum kimliği ve satır içerikleri yazılmaz.
"""
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_demo import COLUMNS
from merge_csv import merge


def audit():
    paths = sorted((ROOT / 'private-data').glob('*.csv'))
    if not paths:
        raise ValueError('private-data içinde CSV bulunamadı')
    records = {}
    duplicate_rows = 0
    completion_updates = 0
    input_rows = 0
    private_keys = set()
    duplicates_within_inputs = 0
    originals = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    for path in [ROOT / 'data/oturumlar.csv', *paths]:
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != COLUMNS:
                raise ValueError(f'CSV başlığı uyuşmuyor: {path.name}')
            for line, row in enumerate(reader, 2):
                if path in paths:
                    input_rows += 1
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f'{path.name}:{line}: sütun sayısı geçersiz')
                if row['kaynak'] != 'gerçek' or not row['oturum_id']:
                    raise ValueError(f'{path.name}:{line}: gerçek kaynak/oturum kimliği gerekli')
                if row['karar_no'] not in ('1','2','3') or row['secim'] not in ('0','1'):
                    raise ValueError(f'{path.name}:{line}: karar veya seçim geçersiz')
                if row['ayrinti_istegi'] not in ('','0','1') or row['tamamlandi'] not in ('0','1'):
                    raise ValueError(f'{path.name}:{line}: etiket veya tamamlanma değeri geçersiz')
                for name, limit in [('bekleme_sn',300),('degistirme_sayisi',20),('ipucu_sayisi',10)]:
                    value = float(row[name])
                    if not math.isfinite(value) or not 0 <= value <= limit:
                        raise ValueError(f'{path.name}:{line}: {name} sınır dışında')
                    if name != 'bekleme_sn' and value != int(value):
                        raise ValueError(f'{path.name}:{line}: sayım tam sayı olmalı')
                key = row['oturum_id'], row['karar_no']
                if path in paths:
                    duplicates_within_inputs += int(key in private_keys)
                    private_keys.add(key)
                old = records.get(key)
                if old:
                    if any(old[k] != row[k] for k in COLUMNS if k != 'tamamlandi'):
                        raise ValueError(f'{path.name}:{line}: aynı oturum/karar için çelişen cevaplar; birleştirilmedi')
                    duplicate_rows += 1
                    if old['tamamlandi'] != row['tamamlandi']:
                        completion_updates += 1
                    row['tamamlandi'] = str(max(int(old['tamamlandi']), int(row['tamamlandi'])))
                records[key] = row
    merge(paths)
    groups = defaultdict(list)
    for row in records.values():
        groups[row['oturum_id']].append(row)
    complete = {key: rows for key,rows in groups.items()
                if {r['karar_no'] for r in rows} == {'1','2','3'}
                and all(r['tamamlandi'] == '1' for r in rows)}
    complete_rows = [r for rows in complete.values() for r in rows]
    labeled_session_count = sum(any(r['ayrinti_istegi'] != '' for r in rows) for rows in complete.values())
    def distribution(rows):
        counts = Counter(r['ayrinti_istegi'] for r in rows)
        return {'kisa_0': counts['0'], 'ayrintili_1': counts['1'], 'eksik': counts['']}
    report = {
        'date': '2026-11-06', 'source': 'gerçek', 'input_csv_count': len(paths),
        'input_rows': input_rows, 'unique_decisions': len(records),
        'duplicate_rows_within_input_csvs': duplicates_within_inputs,
        'duplicate_rows_not_counted_again': duplicate_rows,
        'completion_snapshot_differences': completion_updates,
        'unique_sessions': len(groups), 'completed_unique_sessions': len(complete),
        'incomplete_unique_sessions': len(groups) - len(complete),
        'all_unique_decisions_labels': distribution(records.values()),
        'completed_decisions': len(complete_rows),
        'completed_sessions_with_any_label': labeled_session_count,
        'completed_sessions_by_label_count': dict(sorted(Counter(sum(r['ayrinti_istegi'] != '' for r in rows) for rows in complete.values()).items())),
        'completed_decisions_labels': distribution(complete_rows),
        'raw_inputs_unchanged': all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p,h in originals.items()),
        'merged_sha256': hashlib.sha256((ROOT/'data/oturumlar.csv').read_bytes()).hexdigest(),
        'raw_data_is_public': False,
    }
    (ROOT/'test-results/real-data-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    try:
        audit()
    except (ValueError, KeyError, OSError) as error:
        sys.exit(f'Veri denetimi durdu: {error}')
