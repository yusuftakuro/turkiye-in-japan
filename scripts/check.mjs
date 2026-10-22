import {readFileSync, existsSync} from 'node:fs';
import path from 'node:path';
const base=new URL('../', import.meta.url);
const read=f=>readFileSync(new URL(f,base),'utf8');
const pages=['index.html','explore.html','dogal.html','tokyo-camii.html','events.html'];
const failures=[];
for(const f of pages){
 const html=read(f);
 for(const pattern of [/<main\b[^>]*id="main"/,/<h1\b/,/<link rel="stylesheet" href="assets\/site.css"/,/<meta name="viewport"/])if(!pattern.test(html))failures.push(`${f}: missing ${pattern}`);
 if(/<main[^>]*>\s*<\/main>/.test(html))failures.push(`${f}: empty main`);
 for(const m of html.matchAll(/\bhref="([^"]+)"/g)){
  const href=m[1]; if(href.startsWith('https:')||href.startsWith('http:')||href.startsWith('#')||href.startsWith('mailto:'))continue;
  const file=href.split(/[?#]/)[0]; if(file&&!existsSync(new URL(file,base)))failures.push(`${f}: broken local link ${href}`);
 }
}
const dogal=read('dogal.html');
if(!dogal.includes('2025年3月23日')||!dogal.includes('オンライン'))failures.push('Dogal status split missing');
const home=read('index.html');
for(const s of ['食べる','買う','学ぶ','体験する'])if(!home.includes(s))failures.push(`missing primary action ${s}`);
for(const f of ['assets/site.css','assets/site.js','.nojekyll'])if(!existsSync(new URL(f,base)))failures.push(`missing asset ${f}`);
if(failures.length){console.error(`FAILED ${failures.length} checks:\n${failures.join('\n')}`);process.exit(1)}
console.log(`PASS: ${pages.length} HTML pages, non-empty server-delivered main content, internal hrefs, CSS/JS assets, Dogal status, action entry points`);