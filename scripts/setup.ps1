$ErrorActionPreference = 'Stop'
function Check-Exit { if ($LASTEXITCODE -ne 0) { throw "Komut başarısız: $LASTEXITCODE" } }
if (!(Test-Path data/oturumlar.csv)) { Copy-Item data/oturumlar.example.csv data/oturumlar.csv }
if (!(Test-Path .venv/Scripts/python.exe)) { python -m venv .venv; Check-Exit }
& .venv/Scripts/python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt
Check-Exit
npm ci
Check-Exit
node scripts/copy_runtime.mjs
Check-Exit
if (!(Test-Path model/model.onnx)) {
    & .venv/Scripts/python.exe scripts/generate_demo.py
    Check-Exit
    & .venv/Scripts/python.exe train.py --demo
    Check-Exit
}
Write-Output 'Hazır. npm run dev ile açın. Model sentetik demo olarak işaretlidir.'
