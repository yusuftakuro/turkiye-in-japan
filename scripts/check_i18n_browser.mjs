import {existsSync,readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';

const root = new URL('../', import.meta.url);
function findChrome() {
  for (const bin of ['google-chrome','google-chrome-stable','chromium','chromium-browser']) {
    try { execFileSync('which',[bin],{stdio:'ignore'}); return bin; } catch {}
  }
  throw new Error('Chrome or Chromium not available on CI image');
}
const chrome=findChrome();
function open(path,language) {
  const u=new URL(path,root);u.searchParams.set('lang',language);
  let html=execFileSync(chrome,
    ['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--virtual-time-budget=2500','--dump-dom',u.href],
    {encoding:'utf8',timeout:45000,maxBuffer:3000000,stdio:['ignore','pipe','ignore']});
  if(!html.includes('<html lang="'+language+'"'))throw new Error(path+': missing html lang '+language);
  if(!html.includes('site-language-bar'))throw new Error(path+': no language selector in DOM');
  return html;
}
const trHome=open('index.html','tr');
for (const s of ["Japonya'da","Ne yapmak istersiniz?","Görüntüleme dili"])if(!trHome.includes(s))throw new Error('TR home missing '+s);
const enHome=open('index.html','en');
for (const s of ['Find Türkiye','What would you like to do?','Display language'])if(!enHome.includes(s))throw new Error('EN home missing '+s);
const trListing=open('explore.html','tr');
for (const s of ['Kayıtlara göz at','Türk yemekleri','ENT092','href="/'])if(!trListing.includes(s))throw new Error('TR directory missing '+s);
const enDetail=open('places/ENT010.html','en');
for (const s of ['Products and services','Online sales of Turkish food and drinks','Last checked','Proper names and untranslated records remain in Japanese'])if(!enDetail.includes(s))throw new Error('EN Dogal profile missing '+s);
const trDetail=open('places/ENT010.html','tr');
for (const s of ['Ürünler ve hizmetler','Türk gıda ve içeceklerinin çevrimiçi satışı','Gitmeden veya başvurmadan önce'])if(!trDetail.includes(s))throw new Error('TR Dogal profile missing '+s);
console.log('PASS: JavaScript-rendered localization for JA source / EN & TR in homepage, explorer and Dogal profile');
