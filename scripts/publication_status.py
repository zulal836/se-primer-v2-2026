import json
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
repo='zulal836/se-primer-v2-2026'
request=urllib.request.Request(f'https://api.github.com/repos/{repo}/actions/runs?branch=main&per_page=3',headers={'User-Agent':'se-primer-v2'})
with urllib.request.urlopen(request,timeout=30) as response:
    runs=json.load(response)['workflow_runs']
for run in runs:
    print(json.dumps({k:run.get(k) for k in ['id','head_sha','status','conclusion','html_url']},indent=2))
if runs:
    request=urllib.request.Request(runs[0]['jobs_url'],headers={'User-Agent':'se-primer-v2'})
    with urllib.request.urlopen(request,timeout=30) as response:
        for job in json.load(response)['jobs']:
            print(job['name'],job['status'],job['conclusion'])
            for step in job['steps']:
                print(' ',step['name'],step['status'],step['conclusion'])
