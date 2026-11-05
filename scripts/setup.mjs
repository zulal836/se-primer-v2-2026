import {spawnSync} from 'node:child_process';
import {existsSync,copyFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
process.chdir(resolve(dirname(fileURLToPath(import.meta.url)),'..'));
const win=process.platform==='win32';
const py=win?'.venv/Scripts/python.exe':'.venv/bin/python';
function run(command,args,shell=false){
 const result=spawnSync(command,args,{stdio:'inherit',shell,env:{...process.env,PYTHONUTF8:'1'}});
 if(result.error)throw result.error;
 if(result.status!==0)process.exit(result.status||1);
}
if(!existsSync('data/oturumlar.csv'))copyFileSync('data/oturumlar.example.csv','data/oturumlar.csv');
if(!existsSync(py))run(win?'python':'python3',['-m','venv','.venv']);
run(py,['-m','pip','install','--index-url','https://pypi.org/simple','--timeout','180','-r',existsSync('requirements-lock.txt')?'requirements-lock.txt':'requirements.txt']);
run('npm',['ci'],win);
if(!existsSync('model/model.onnx')){run(py,['scripts/generate_demo.py']);run(py,['train.py','--demo']);}
console.log('Hazır. npm run dev ile oyunu açın. Gerçek veri toplanana kadar model sentetik demodur.');
