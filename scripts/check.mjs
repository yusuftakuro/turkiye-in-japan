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
const dogalCorrection=JSON.parse(read('data/review/issue-26/dogal-online-sales-correction.json'));
const offering=read('data/canonical/v1.2-proposed/offerings.csv').split(/\r?\n/).find(x=>x.startsWith('OFF011,'));
const channel=read('data/canonical/v1.2-proposed/channels.csv').split(/\r?\n/).find(x=>x.startsWith('CH002,'));
if(!offering?.includes(',unavailable,verified,2026-10-25'))failures.push('Dogal online Offering is not marked unavailable at the source check date');
if(!channel?.includes(',unavailable,verified,2026-10-25,https://dogal.jp/'))failures.push('Dogal online Channel is not marked unavailable at the source check date');
if(dogalCorrection.entity_id!=='ENT010'||dogalCorrection.offering_id!=='OFF011'||dogalCorrection.channel_id!=='CH002'||dogalCorrection.candidate_status!=='unavailable'||dogalCorrection.closure_date!=='2026-05-31'||dogalCorrection.source_url!=='https://dogal.jp/')failures.push('Dogal correction evidence does not match the scoped official closure notice');
const listing=read('explore.html').match(/<article class="card directory-card" data-card data-entity="ENT010"[\s\S]*?<\/article>/)?.[0]||'';
if(!listing||/data-activity="[^"]*shop/.test(listing)||!listing.includes('オンライン販売は2026年5月31日に終了しました。カフェの営業とは別の情報です。'))failures.push('Dogal listing still implies online shopping is current or lacks its dated notice');
if(!read('explore.html').match(/<article class="card directory-card" data-card data-entity="ENT044" data-activity="shop"/))failures.push('Unknown retail Offering was hidden from shopping discovery');
const dogalProfile=read('places/ENT010.html');
if(!dogalProfile.includes('オンライン販売は2026年5月31日に終了しました。カフェの営業とは別の情報です。')||!dogalProfile.includes('href="https://dogal.jp/"')||!dogalProfile.includes('オンラインショップ（終了した記録）'))failures.push('Dogal profile does not distinguish and source the closed online channel');
const locale=read('assets/i18n.js');
for(const phrase of ['Online sales ended on 31 May 2026.','Çevrimiçi satışlar 31 Mayıs 2026\'da sona erdi.','only to online sales, not the café.','yalnızca çevrimiçi satışlarla ilgilidir','Official page checked on 25 October 2026.','Resmî sayfa 25 Ekim 2026 tarihinde kontrol edildi.'])if(!locale.includes(phrase))failures.push(`missing Dogal EN/TR correction translation: ${phrase}`);
if((read('data/canonical/v1.2-proposed/entities.csv').trim().split(/\r?\n/).length-1)!==92||(read('data/canonical/v1.2-proposed/offerings.csv').trim().split(/\r?\n/).length-1)!==115||(read('data/canonical/v1.2-proposed/locations.csv').trim().split(/\r?\n/).length-1)!==38)failures.push('Dogal correction changed protected projection counts');
const home=read('index.html');
for(const s of ['食べる','買う','学ぶ','体験する'])if(!home.includes(s))failures.push(`missing primary action ${s}`);
for(const f of ['assets/site.css','assets/site.js','.nojekyll'])if(!existsSync(new URL(f,base)))failures.push(`missing asset ${f}`);
if(failures.length){console.error(`FAILED ${failures.length} checks:\n${failures.join('\n')}`);process.exit(1)}
console.log(`PASS: ${pages.length} HTML pages, non-empty server-delivered main content, internal hrefs, CSS/JS assets, Dogal status, action entry points`);
