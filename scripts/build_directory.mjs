import {readFileSync,writeFileSync} from 'node:fs';
function csvParse(csv){
  const rows=[];let row=[],val="",quote=false;
  csv=csv.replace(/^\ufeff/,"");
  for(let i=0;i<csv.length;i++){
    const c=csv[i];
    if(quote){if(c==='"'&&csv[i+1]==='"'){val+='"';i++}else if(c==='"')quote=false;else val+=c;}
    else if(c==='"')quote=true;
    else if(c===','){row.push(val);val="";}
    else if(c==='\n'){row.push(val.replace(/\r$/,""));val="";if(row.some(x=>x!==""))rows.push(row);row=[];}
    else val+=c;
  }
  row.push(val.replace(/\r$/,""));if(row.some(x=>x!==""))rows.push(row);
  if(quote)throw Error("Unclosed CSV quoted field");
  const cols=rows.shift();
  return rows.map(r=>{if(r.length!==cols.length)throw Error("CSV field count mismatch");return Object.fromEntries(cols.map((c,i)=>[c,r[i]]))});
}
function escapeHtml(v){return String(v||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");}
function renderDirectory(shell,datasets){
  const entities=csvParse(datasets.entities),offerings=csvParse(datasets.offerings),locations=csvParse(datasets.locations),joins=csvParse(datasets.location_entities),tags=csvParse(datasets.entity_relation_tags);
  const correction=datasets.correction;
  if(entities.length!==92||offerings.length!==115||locations.length!==38)throw Error("Unexpected canonical projection counts");
  const ids=new Set(entities.map(e=>e.entity_id));
  if(ids.size!==92||offerings.some(o=>!ids.has(o.entity_id))||joins.some(o=>!ids.has(o.entity_id)))throw Error("Duplicate entity ID or FK mismatch");
  const offered={},linked={},tagged={},locBy=Object.fromEntries(locations.map(l=>[l.location_id,l]));
  for(const o of offerings)(offered[o.entity_id]??=[]).push(o);
  for(const j of joins)if(locBy[j.location_id]?.public_access==="yes")(linked[j.entity_id]??=[]).push(locBy[j.location_id]);
  for(const t of tags)(tagged[t.entity_id]??=[]).push(t.relation_tag_id);
  const actTypes={food_service:"eat",retail:"shop",class:"learn",lecture:"learn",workshop:"experience",museum_visit:"experience",visit:"experience"};
  const actNames={eat:"食べる",shop:"買う",learn:"学ぶ",experience:"体験する"};
  const kindLabels={business:"BUSINESS",nonprofit:"ORGANIZATION",cultural_institution:"CULTURE",religious_institution:"CULTURE",community:"COMMUNITY",public_body:"PUBLIC INSTITUTION",media:"MEDIA",other:"ORGANIZATION"};
  const cards=entities.map(e=>{
    const oo=offered[e.entity_id]||[],ll=linked[e.entity_id]||[];
    // Exclude only explicitly unavailable offerings. Unknown availability remains discoverable.
    const acts=[...new Set(oo.filter(o=>o.availability_status!=='unavailable').map(o=>actTypes[o.offering_type]).filter(Boolean))];
    const regions=[...new Set(ll.map(l=>(l.prefecture||"")+(l.city||"")).filter(Boolean))].slice(0,3).join("、");
    let kind=kindLabels[e.entity_kind]||"ORGANIZATION";
    if(acts.includes("eat"))kind="EAT / FOOD";
    else if(acts.includes("shop"))kind="SHOP / PRODUCTS";
    else if(acts.includes("learn"))kind="LEARN / CLASS";
    else if(acts.includes("experience"))kind="CULTURE / EXPERIENCE";
    const names=[...new Set(oo.map(o=>o.name).filter(Boolean))];
    const currentNames=[...new Set(oo.filter(o=>o.availability_status!=='unavailable').map(o=>o.name).filter(Boolean))];
    const desc=e.entity_id===correction.entity_id?`オンライン販売は${correction.closure_date.slice(0,4)}年${Number(correction.closure_date.slice(5,7))}月${Number(correction.closure_date.slice(8,10))}日に終了しました。カフェの営業とは別の情報です。`:(currentNames.slice(0,3).join("／")||"登録された団体・施設等の情報").slice(0,140);
    const key=[e.public_name,e.entity_id,regions,names.join(" "),(tagged[e.entity_id]||[]).join(" "),acts.map(a=>actNames[a]).join(" ")].filter(Boolean).join(" ");
    const provisional=e.identity_review_status!=="clear";
    const access=ll.length?ll.map(l=>`<li>${escapeHtml(l.name)}</li>`).join(""):"<li>公開可能な来訪先情報なし</li>";
    const offList=(oo.length?oo.map(o=>`<li>${escapeHtml(o.name)}${o.availability_status==='unavailable'?'<small>（利用不可）</small>':''}</li>`):["確認中"].map(n=>`<li>${escapeHtml(n)}</li>`)).join("");
    const validUrl=/^https?:\/\/[^\/\s:@]+(?:[\/?#]|$)/i.test(e.official_url||"");
    const link=validUrl?`<a class="card-link" href="${escapeHtml(e.official_url)}" target="_blank" rel="noopener noreferrer">公式情報を見る ↗</a>`:'<span class="muted">公式URLは調査中</span>';
    return `<article class="card directory-card" data-card data-entity="${escapeHtml(e.entity_id)}" data-activity="${escapeHtml(acts.join(" "))}" data-keywords="${escapeHtml(key)}"><div class="smallcaps">${escapeHtml(kind)} <span class="directory-id">${escapeHtml(e.entity_id)}</span></div><h2>${escapeHtml(e.public_name)}</h2><p>${escapeHtml(desc)}</p><div class="meta">${regions?`<span>${escapeHtml(regions)}</span>`:""}<span>${provisional?"暫定登録":"記録あり"}</span></div><details class="directory-details"><summary>提供内容・確認情報</summary><p>現在の営業・受付状況：未確認。${provisional?"主体情報も暫定登録。":""}<br>データ確認日：${escapeHtml(e.verified_at||"未確認")}</p><strong>関連する内容</strong><ul>${offList}</ul><strong>登録されている公開拠点</strong><ul>${access}</ul></details><div class="directory-links"><a class="detail-link" href="places/${escapeHtml(e.entity_id)}.html">詳細情報を見る →</a>${link}</div></article>`;
  });
  if(cards.length!==92)throw Error("Directory output incomplete");
  const marker="<!-- CARDS_GENERATED_HERE -->";
  if(shell.split(marker).length!==2)throw Error("Missing sole generation marker");
  return shell.replace(marker,cards.join("\n"));
}
const data=n=>readFileSync(new URL('../data/canonical/v1.2-proposed/'+n+'.csv',import.meta.url),'utf8');
const shell=readFileSync(new URL('../templates/explore-shell.html',import.meta.url),'utf8');
const correction=JSON.parse(readFileSync(new URL('../data/review/issue-26/dogal-online-sales-correction.json',import.meta.url),'utf8'));
const html=renderDirectory(shell,{entities:data('entities'),offerings:data('offerings'),locations:data('locations'),location_entities:data('location_entities'),entity_relation_tags:data('entity_relation_tags'),correction});
const path=new URL('../explore.html',import.meta.url);
if(process.argv.includes('--check')){if(readFileSync(path,'utf8')!==html){console.error('FAIL: directory HTML is out of sync');process.exit(1)}console.log('PASS: 92-card directory reproducibly generated')}
else{writeFileSync(path,html,'utf8');console.log('Generated 92 Entity directory cards')}
