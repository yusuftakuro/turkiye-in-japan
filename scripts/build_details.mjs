import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'data/canonical/v1.2-proposed');
const correction = JSON.parse(readFileSync(path.join(root, 'data/review/issue-26/dogal-online-sales-correction.json'), 'utf8'));
const dateJa = value => { const [year,month,day]=value.split('-'); return `${year}年${Number(month)}月${Number(day)}日`; };
function csv(text) {
  let rows = [], row = [], field = '', inside = false;
  text = text.replace(/^\uFEFF/, '');
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inside) {
      if (c === '"' && text[i+1] === '"') { field += '"'; i++; }
      else if (c === '"') inside = false;
      else field += c;
    } else if (c === '"') inside = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field.replace(/\r$/, '')); field = ''; if (row.some(x=>x)) rows.push(row); row = []; }
    else field += c;
  }
  row.push(field.replace(/\r$/, '')); if (row.some(x=>x)) rows.push(row);
  if (inside) throw new Error('Unclosed CSV string');
  const header = rows.shift();
  return rows.map(r => { if (r.length !== header.length) throw new Error('Invalid row width'); return Object.fromEntries(header.map((k,i)=>[k,r[i]])); });
}
const records = n => csv(readFileSync(path.join(source,n+'.csv'), 'utf8'));
const entities = records('entities'), offerings = records('offerings'), channels = records('channels'),
  places = records('locations'), locJoins = records('location_entities'), claims = records('new_claim_evidence'),
  relations = records('entity_relations'), channelOfferings = records('channel_offerings');
if (entities.length!==92 || offerings.length!==115 || places.length!==38) throw new Error('Unexpected data counts');
const byId = new Map(entities.map(e=>[e.entity_id,e]));
const locById = new Map(places.map(l=>[l.location_id,l]));
const offerId = new Set(offerings.map(o=>o.offering_id));
const channelId = new Set(channels.map(c=>c.channel_id));
if (byId.size!==92 || offerings.some(o=>!byId.has(o.entity_id)) || channels.some(c=>!byId.has(c.entity_id)) ||
    locJoins.some(j=>!locById.has(j.location_id) || !byId.has(j.entity_id)) ||
    channelOfferings.some(x=>!offerId.has(x.offering_id)||!channelId.has(x.channel_id))) throw new Error('Invalid dataset relationships');
const esc = x=>String(x??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const http = s=>/^https?:\/\/[a-z0-9][a-z0-9.-]*(?::[0-9]+)?(?:[\/?#]|$)/i.test(String(s||'').trim())?String(s).trim():'';
const categories={business:'店舗・事業者',nonprofit:'団体',public_body:'公的機関',cultural_institution:'文化施設・団体',religious_institution:'宗教・文化施設',community:'コミュニティ',media:'メディア',other:'団体・その他'};
const channelNames={online_shop:'オンラインショップ',in_person:'店頭・対面',online:'オンライン',website:'Webサイト',phone:'電話',reservation:'予約',registration:'申し込み'};
const relationshipNames={operated_by:'運営元',part_of:'所属先',brand_of:'ブランドの運営者',affiliated_with:'関連先',successor_of:'前身',predecessor_of:'後継先'};
const list = contents => `<ul class="profile-list">${contents.join('')}</ul>`;
function profile(e){
 const eo=offerings.filter(x=>x.entity_id===e.entity_id), ec=channels.filter(x=>x.entity_id===e.entity_id);
 const els=locJoins.filter(x=>x.entity_id===e.entity_id).map(x=>locById.get(x.location_id)).filter(l=>l?.public_access==='yes');
 const evidence=claims.filter(x=>x.object_type==='entity'&&x.object_id===e.entity_id);
 const official=http(e.official_url);const state=e.identity_review_status==='clear'?'情報を確認済み':'主体情報は暫定登録';
 const links=[official,...ec.map(x=>http(x.url)),...evidence.map(x=>http(x.source_url))].filter(Boolean);
 const uniqueLinks=[...new Set(links)].slice(0,7);
 const category=categories[e.entity_kind]||'団体・その他';
 const available=eo.length?eo.map(o=>{
   const applicableIds=new Set(channelOfferings.filter(x=>x.offering_id===o.offering_id).map(x=>x.channel_id));
   const linkedChannels=ec.filter(c=>applicableIds.has(c.channel_id) && c.availability_status !== 'unavailable');
   const how=linkedChannels.length?`<small>関連する経路：${esc([...new Set(linkedChannels.map(c=>channelNames[c.channel_type]||'その他'))].join('、'))}</small>`:'';
   return `<li><span>${esc(o.name)}</span>${o.availability_status==='unavailable'?'<small>（利用不可）</small>':''}${how}</li>`;
 }):['<li>提供内容は公開データに登録されていません。</li>'];
 const locs=els.length?els.map(l=>{
   const area=[l.prefecture,l.city].filter(Boolean).join('');
   const historical=['closed','inactive'].includes(l.operational_status);
   return `<li><span><strong>${esc(l.name)}</strong>${area?' · '+esc(area):''}</span><small>${historical?'閉店・終了の記録':'現在の来訪可否は未確認'}</small></li>`;
 }):['<li>公開可能な拠点情報は登録されていません。</li>'];
 const routes=ec.length?ec.map(c=>{
   const ended=c.availability_status==='unavailable';
   const label=(channelNames[c.channel_type]||'利用経路')+(ended?'（終了した記録）':'');const url=http(c.url);
   return `<li><span>${esc(label)}</span>${ended?'<small>現在は利用できません</small>':url?`<a target="_blank" rel="noopener noreferrer" href="${esc(url)}">該当する案内を見る ↗</a>`:'<small>リンク未登録</small>'}</li>`;
 }):['<li>利用経路は公開データに未登録です。</li>'];
 const relationLines=[];
 for (const r of relations){if(r.verification_status!=='verified')continue;
   if(r.subject_entity_id===e.entity_id&&byId.has(r.object_entity_id))relationLines.push(`<li><span>${esc(relationshipNames[r.relation_type]||'関係先')}</span><a href="${esc(r.object_entity_id)}.html">${esc(byId.get(r.object_entity_id).public_name)}</a></li>`);
   if(r.object_entity_id===e.entity_id&&byId.has(r.subject_entity_id))relationLines.push(`<li><span>関連する主体</span><a href="${esc(r.subject_entity_id)}.html">${esc(byId.get(r.subject_entity_id).public_name)}</a></li>`);
 }
 const bibliography=uniqueLinks.length?uniqueLinks.map((url,i)=>`<li><span>情報源 ${i+1}</span><a target="_blank" rel="noopener noreferrer" href="${esc(url)}">${esc(new URL(url).hostname)} ↗</a></li>`):['<li>公開データに情報源URLは登録されていません。</li>'];
 const summary=e.entity_id===correction.entity_id?`オンライン販売終了（${dateJa(correction.closure_date)}）`:eo.slice(0,2).map(o=>o.name).filter(Boolean).join('／')||category;
 const closureNote=e.entity_id===correction.entity_id?`<p class="detail-explain">オンライン販売は${dateJa(correction.closure_date)}に終了しました。カフェの営業とは別の情報です。 <a target="_blank" rel="noopener noreferrer" href="${esc(correction.source_url)}">公式のお知らせ ↗</a><br><small>公式ページ確認日：${dateJa(correction.checked_date_jst)}。</small></p>`:'';
 const body=`<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f7f5f0"><meta name="robots" content="noindex,nofollow"><meta name="description" content="${esc(e.public_name)}の掲載情報、提供内容、利用経路、確認日"><title>${esc(e.public_name)} | Türkiye in Japan</title><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/detail.css"><script src="../assets/i18n.js" defer></script></head><body><a class="skip" href="#main">本文へ移動</a><div class="topstrip"><div class="layout"><span>日本のトルコ関連情報を集めたディレクトリ</span><a href="../index.html#about">掲載情報について ↗</a></div></div><header class="header"><div class="layout header-inner"><a class="brand" href="../index.html"><span class="mark">T</span><span class="brand-name">Türkiye in Japan<small>DIRECTORY / JAPAN</small></span></a><nav class="nav"><a href="../explore.html" class="nav-cta">一覧から探す ↗</a></nav></div></header><main id="main" class="layout detail-shell"><nav class="detail-crumb" aria-label="現在の位置"><a href="../index.html">ホーム</a> / <a href="../explore.html">一覧</a> / ${esc(e.public_name)}</nav><div class="detail-columns"><article class="detail-main"><div class="eyebrow">${esc(category)} / ${esc(e.entity_id)}</div><h1>${esc(e.public_name)}</h1><p class="detail-summary">${esc(summary)}</p><div class="detail-state"><strong>利用前に最新情報をご確認ください</strong><p>${state}。最終確認：${esc(e.verified_at||'日付未登録')}。現在の営業・受付・訪問状況はこのページでは確認していません。</p></div>${closureNote}<section class="detail-section" aria-labelledby="offers"><span class="eyebrow">ACTIVITIES</span><h2 id="offers">提供内容</h2>${list(available)}</section><section class="detail-section" aria-labelledby="places"><span class="eyebrow">LOCATIONS</span><h2 id="places">登録されている場所</h2><p class="detail-explain">公開可能な拠点のみ記載しています。来訪可否や住所の詳細は公式情報でご確認ください。</p>${list(locs)}</section><section class="detail-section" aria-labelledby="channels"><span class="eyebrow">CHANNELS</span><h2 id="channels">利用方法・案内</h2><p class="detail-explain">調査時点で確認した利用経路です。現在の利用可否は未確認です。</p>${list(routes)}</section>${relationLines.length?`<section class="detail-section" aria-labelledby="organizations"><h2 id="organizations">関連する団体・事業者</h2>${list(relationLines)}</section>`:''}<section class="detail-section" aria-labelledby="sources"><span class="eyebrow">SOURCES</span><h2 id="sources">情報源</h2><p class="detail-explain">最終確認：${esc(e.verified_at||'日付未登録')}。リンク先の情報は更新される場合があります。</p>${list(bibliography)}</section></article><aside class="detail-aside"><div class="detail-box"><span class="eyebrow">PROFILE</span><h2>基本情報</h2><dl><dt>分類</dt><dd>${esc(category)}</dd><dt>登録状態</dt><dd>${esc(state)}</dd><dt>確認日</dt><dd>${esc(e.verified_at||'未登録')}</dd><dt>管理番号</dt><dd>${esc(e.entity_id)}</dd></dl>${official?`<a class="detail-official" target="_blank" rel="noopener noreferrer" href="${esc(official)}">公式情報を見る ↗</a>`:'<p class="detail-explain">公式リンクは未登録です。</p>'}</div></aside></div><div class="detail-return"><a href="../explore.html">← 一覧へ戻る</a></div></main><footer class="foot"><div class="layout footer-line"><span>Türkiye in Japan — 日本のトルコ関連情報</span><span>SSOT v1.2 暫定版／現在の状況は各情報源でご確認ください</span></div></footer></body></html>`;
 return body;
}
const out=path.join(root,'places');mkdirSync(out,{recursive:true});
let errors=[];const checking=process.argv.includes('--check');
for(const e of entities){const target=path.join(out,e.entity_id+'.html'),html=profile(e);if(checking){if(!existsSync(target)||readFileSync(target,'utf8')!==html)errors.push(e.entity_id);}else writeFileSync(target,html,'utf8');}
if(errors.length){console.error('Outdated pages: '+errors.join(', '));process.exit(1)}
console.log('PASS: '+entities.length+' entity detail pages '+(checking?'match public-safe source CSV':'generated'));
