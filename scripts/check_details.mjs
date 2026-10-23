import {existsSync,readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const root=new URL('../',import.meta.url);const read=n=>readFileSync(new URL(n,root),'utf8');
const exp=read('explore.html');const ids=[...exp.matchAll(/data-entity="(ENT\d{3})"/g)].map(x=>x[1]);
if(ids.length!==92||new Set(ids).size!==92)throw Error('Directory must have 92 unique entities');
for(const id of ids){const path='places/'+id+'.html';if(!exp.includes('href="'+path+'"'))throw Error('Missing detail link: '+id);if(!existsSync(new URL(path,root)))throw Error('Missing detail file '+id);const page=read(path);if(!page.includes('情報源')||!page.includes('現在の営業・受付・訪問状況')||!page.includes('<main id="main"'))throw Error('Missing required profile sections '+id);if(!page.includes('<h1>')||!page.includes('<section class="detail-section"'))throw Error('Profile must contain static content: '+id);}
execFileSync(process.execPath,[new URL('build_details.mjs',import.meta.url).pathname,'--check'],{stdio:'inherit'});
console.log('PASS: all 92 source-linked static detail profiles');
