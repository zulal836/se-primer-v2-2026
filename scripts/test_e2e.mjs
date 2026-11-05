import {spawn} from 'node:child_process';
const port=process.env.PRIMER_TEST_PORT||'5180';
const url=`http://127.0.0.1:${port}`;
const server=spawn(process.execPath,['node_modules/vite/bin/vite.js','--host','127.0.0.1','--port',port,'--strictPort'],{stdio:'inherit'});
let serverFailed=false;
server.on('exit',()=>{serverFailed=true});
async function waitForServer(){
 for(let i=0;i<120;i++){
  if(serverFailed)throw Error('Test sunucusu başlatılamadı');
  try{const r=await fetch(url,{signal:AbortSignal.timeout(1000)});if(r.ok)return;}catch{}
  await new Promise(resolve=>setTimeout(resolve,500));
 }
 throw Error('Test sunucusu zaman aşımı');
}
let code=1;
try{
 await waitForServer();
 const test=spawn(process.execPath,['node_modules/cypress/bin/cypress','run','--browser','electron'],{stdio:'inherit',env:{...process.env,CYPRESS_BASE_URL:url}});
 code=await new Promise((resolve,reject)=>{test.on('exit',resolve);test.on('error',reject)});
}catch(e){console.error(e.message);}finally{server.kill();}
process.exit(code??1);
