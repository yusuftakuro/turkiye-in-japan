import {readFileSync,existsSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const root=new URL('../',import.meta.url);
const read=p=>readFileSync(new URL(p,root),'utf8');
const top=['index.html','explore.html','events.html','dogal.html','tokyo-camii.html','templates/explore-shell.html'];
for(const p of top)if(!read(p).includes('src="assets/i18n.js"'))throw Error('Missing localization on '+p);
const names=read('data/canonical/v1.2-proposed/entities.csv').trim().split(/\r?\n/).length-1;
if(names!==92)throw Error('Expected 92 Entity profiles');
for(let i=1;i<=92;i++){const p='places/ENT'+String(i).padStart(3,'0')+'.html';
if(!existsSync(new URL(p,root))||!read(p).includes('src="../assets/i18n.js"'))throw Error('Missing localization script on '+p);}
const js=read('assets/i18n.js');
for(const x of ['ja','en','tr','Türkçe','display language','translateValue','tr\\u0000']){
 if(x==='tr\\u0000')continue;
 if(!js.toLowerCase().includes(x.toLowerCase()))throw Error('Missing language marker '+x);
}
execFileSync(process.execPath,['--check',new URL('assets/i18n.js',root).pathname],{stdio:'inherit'});
execFileSync(process.execPath,[new URL('build_directory.mjs',import.meta.url).pathname,'--check'],{stdio:'inherit'});
execFileSync(process.execPath,[new URL('build_details.mjs',import.meta.url).pathname,'--check'],{stdio:'inherit'});
console.log('PASS: 92 profiles and main pages linked to three-language UI');
