#!/usr/bin/env python3
"""Reproducible Türkiye in Japan research intake. Never silently merge into SSOT v1."""
import csv, json, io, re, sqlite3, unicodedata, zipfile
from pathlib import Path
from collections import Counter
from datetime import date
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent.parent
STAGE=ROOT/'data'/'intake'/'wave003'; OUT=ROOT/'integrated'
STAGE.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
CHECKED='2026-10-22'
# Official/first-party pages were researched individually; status of a website != current activity.
# source title and claim quote are distilled propositions, not copied passages.
CANDIDATES=[
# id, name, kind, subtype, region, official_url, supporting_url, source type, fact, offer labels, channel type, location tuples, review
('慶應外語（慶應義塾大学外国語教育研究センター）','cultural_institution','education_program','東京都','https://www.fls.keio.ac.jp/levelall-10aki/levelall-trk.html','https://www.fls.keio.ac.jp/levelall-10aki/levelall-trk.html','official_website','2026年度秋学期のトルコ語入門・初級講座が案内されている',['トルコ語入門（2026年秋）','トルコ語初級（2026年秋）'],None,[], 'provisional'),
('慶應義塾大学言語文化研究所','cultural_institution','research_and_education','東京都','https://www.icl.keio.ac.jp/tokushukouza.html','https://www.icl.keio.ac.jp/tokushukouza.html','official_website','言語文化研究所特殊講座にトルコ語初級・中級の案内がある',['トルコ語初級特殊講座','トルコ語中級特殊講座'],None,[], 'provisional'),
('朝日カルチャーセンター横浜教室','business','learning_center','神奈川県','https://www.asahiculture.com/','https://www.asahiculture.com/asahiculture/asp-webapp/web/WKozaKensaku.do?kensakuKubun=0&kyoshitsuId=&shishaId=9100&wbKozaKensakuJoken.chikuId=0&wbKozaKensakuJoken.chujanruId=8607&wbKozaKensakuJoken.daijanruId=09&wbKozaKensakuJoken.keyWord=&wbKozaKensakuJoken.shobunruiId=1291','official_website','横浜教室の2026年秋期トルコ語入門・初級・中級が掲載されている',['トルコ語・入門Ⅰ','トルコ語・初級Ⅰ','トルコ語・中級'],None,[], 'provisional'),
('NHK文化センター梅田教室','business','learning_center','大阪府','https://www.nhk-cul.co.jp/','https://www.nhk-cul.co.jp/programs/program_1108931.html','official_website','梅田教室にトルコの伝統手芸イーネオヤ講座の案内がある',['イーネオヤ講座（2026年10月〜）'],None,[], 'provisional'),
('ヨークカルチャーセンター大船','business','learning_center','神奈川県','https://www.culture.gr.jp/detail/oofuna/1953602','https://www.culture.gr.jp/detail/oofuna/1953602','official_website','トルコのオヤ講座に2026年10・11・12月の予定が掲載されている',['トルコのオヤ（レース編み）講座'],None,[], 'provisional'),
('自由が丘産経学園','business','learning_center','東京都','https://www.culture.gr.jp/detail/sk.jiyugaoka/4559366','https://www.culture.gr.jp/detail/sk.jiyugaoka/4559366','official_website','メキキオヤ講座の2026年秋期予定が掲載されている',['メキキオヤ講座','イーネオヤ講座'],None,[], 'provisional'),
('WASABI-Elisi（ワサビ・エリシ）','business','craft_workshop','地域要確認','https://wasabielisi.com/','https://wasabielisi.com/?cbid=2172835&csid=16&mode=cate','official_website','イーネオヤ教室について2026年10月25日・11月22日の案内がある',['イーネオヤ教室'],None,[], 'provisional'),
('ROGOBA（ロゴバ）','business','kilim_brand','東京都／大阪府','https://rogobakilim.com/','https://rogobakilim.com/shop/','official_website','東京と大阪の店舗およびキリム通販の案内がある',['ロゴバキリム・インテリア販売'],'online_shop',[('ROGOBA東京店','store','東京都','千代田区','東京都千代田区神田美土代町1 WORK VILLA MITOSHIRO 1階','unknown'),('ROGOBA大阪店','store','大阪府','大阪市中央区','大阪府大阪市中央区谷町3-1-24 エルデ大手前1F','unknown')], 'provisional'),
('ANATOLIAN RUGS','business','kilim_retailer','地域要確認','https://anatolianrugs.net/','https://anatolianrugs.net/','official_website','トルコ産キリム・絨毯の専門オンライン店舗が掲載されている',['トルコキリム・絨毯販売'],'online_shop',[], 'provisional'),
('ARTLINE（アートライン）','business','kilim_retailer','静岡県','https://www.artlinekilim.com/','https://www.artlinekilim.com/','official_website','静岡を拠点としてトルコ工房製キリム等の販売を案内している',['トルコキリム・絨毯販売'],None,[('ARTLINE事業所在地','office','静岡県','静岡市駿河区','静岡県静岡市駿河区東新田2丁目16-25','unknown')], 'provisional'),
('ZAKUROらんぷ家','business','lamp_workshop','東京都','https://zakuro-lampya.com/','https://zakuro-lampya.com/','official_website','谷中銀座でトルコモザイクランプの販売・制作体験を案内している',['モザイクランプ制作体験','トルコランプ販売'],None,[('ZAKUROらんぷ家','store','東京都','荒川区','東京都荒川区西日暮里3-15-5','yes')], 'provisional'),
('クリムゾン・ジャパン','business','translation_service','東京都','https://www.crimsonjapan.co.jp/','https://www.crimsonjapan.co.jp/translation/lang/turkish.html','official_website','日本語とトルコ語間の翻訳サービスの案内がある',['トルコ語翻訳サービス'],None,[], 'provisional'),
('トルコ雑貨＆カフェ ぎゃるぎゃる','business','turkish_goods_and_cafe','岡山県','https://www.gelgel.jp/','https://www.gelgel.jp/','official_website','倉敷美観地区でトルコ直輸入雑貨を扱いネットショップも案内している',['トルコ雑貨販売','カフェ'], 'online_shop',[('ぎゃるぎゃる実店舗','store','岡山県','倉敷市','岡山県倉敷市本町','yes')], 'provisional'),
('ESMA（トルコ雑貨）','business','online_retailer','所在地要確認','https://esma1210.thebase.in/','https://esma1210.thebase.in/about','official_website','トルコからの直輸入雑貨を通販で提供する旨が掲載されている',['トルコ雑貨通販'],'online_shop',[], 'provisional'),
('NOVAROMA','business','online_retailer','所在地要確認','https://www.novaromashop.com/','https://www.novaromashop.com/','official_website','イーネオヤ・アクセサリー・トルコ織物の通販と2026年10月の入荷情報が掲載されている',['オヤ・トルコ雑貨通販'],'online_shop',[], 'provisional'),
('ブルーコテージ（ぬくもりの森）','business','turkish_goods_store','静岡県','https://toruko.crayonsite.com/','https://toruko.crayonsite.com/','official_website','浜松市ぬくもりの森敷地内のトルコ直輸入雑貨店と案内されている',['トルコタイル・ランプ・雑貨販売'],None,[('ブルーコテージ','store','静岡県','浜松市','静岡県浜松市','unknown')], 'provisional'),
('ミフリ＆アクチェ','business','cross_border_retailer','トルコ／対日通販要確認','https://mihri.ocnk.net/','https://mihri.ocnk.net/','official_website','アンタルヤ発のトルコ手工芸品オンライン販売が案内されている',['キリム・イーネオヤ通販'],'online_shop',[], 'needs_review'),
('C-BOW（トルコのオヤ雑貨）','business','cross_border_retailer','発送元要確認','https://c-bow.ocnk.net/','https://c-bow.ocnk.net/info','official_website','トルコ発のオヤスカーフ・糸・手芸道具の通販を案内している',['トルコのオヤ用品通販'],'online_shop',[], 'needs_review'),
]
# Extra pages represent actual separate atomic facts for already known Entities or sourced future Events.
SOURCES_EXTRA=[
('https://clover.co.jp/workshop/oya2026','official_website','クロバー 2026年10月24日〜11月6日オヤ展・ワークショップ','2026-10-14'),
('https://amimono.me/news/detail.html?id=548','media','トルコの伝統手芸・オヤ 作品展＆ワークショップ',''),
('https://www.tkjts.jp/turkish_lecture/2026/08/14/7357/','official_website','第105回 秋期トルコ語講座','2026-08-14'),
('https://sevinc8.com/','official_website','セヴィンチエイト 店舗出店情報',''),
('https://istanbulbazar.ocnk.net/','official_website','イスタンブールバザール 犬山の実店舗・通販',''),
('https://www.turkeycenter.co.jp/cooking/','official_website','トルコ文化センター 2026年10月料理教室',''),
('https://www.culture.gr.jp/detail/sk.jiyugaoka/4559538','official_website','自由が丘産経学園 イーネオヤ講座',''),
('https://www.nhk-cul.co.jp/programs/program_1108931.html','official_website','NHK文化センター梅田 イーネオヤ',''),
]

def write(name,rows,columns):
 with (STAGE/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader();w.writerows(rows)

def add_source(url,typ,title='',published=''):
 if url in source_id_by_url:return source_id_by_url[url]
 sid=f'W003-S{len(sources)+1:03d}';source_id_by_url[url]=sid
 sources.append(dict(source_id=sid,url=url,canonical_url=url,source_type=typ,page_title=title,published_at=published,retrieved_at=CHECKED,note='Public page inspected during 2026-10-22 research; evidence does not establish open-now status.'))
 return sid

def add_claim(value,target_type,target_id,sid,claim_type='source_statement',note='This states what the cited page publishes, not live availability.',valid_from='',valid_to=''):
 cid=f'W003-CL{len(claims)+1:03d}';claims.append(dict(claim_id=cid,claim_type=claim_type,claim_value=value,verification_status='verified',valid_from=valid_from,valid_to=valid_to,checked_at=CHECKED,supersedes_claim_id='',note=note)); claim_sources.append(dict(claim_id=cid,source_id=sid,support_type='supports'))
 link=dict(claim_id=cid, **{('entity_id' if target_type=='entity' else target_type+'_id'):target_id})
 claim_subjects[target_type].append(link);return cid

sources=[];source_id_by_url={};claims=[];claim_sources=[]
claim_subjects={k:[] for k in ['entity','location','channel','offering','event']}
entities=[];offerings=[];channels=[];locations=[];location_entities=[];channel_offerings=[];channel_locations=[];events=[];relation_tags=[];reviews=[];existing_updates=[]
for ix,row in enumerate(CANDIDATES,1):
 name,kind,subtype,region,official_url,support_url,source_type,fact,offer_labels,channel_type,locs,review=row
 eid=f'W003-E{ix:03d}';sid=add_source(support_url,source_type, name+' の公式案内')
 entities.append(dict(staged_entity_id=eid,public_name=name,entity_kind=kind,entity_subtype=subtype,status='unknown',identity_review_status=review,verification_status='verified',verified_at=CHECKED,official_url=official_url,intake_state='candidate_sourced_unmerged',canonical_entity_id='',region_hint=region,note='Source supports identity/activity but not legal identity or current opening status.'))
 add_claim(f'{name}：{fact}', 'entity', eid, sid,'identity_or_turkey_relation')
 relation=('turkish_language' if any(s in fact for s in ('トルコ語','翻訳')) else 'turkish_culture')
 if any(s in subtype for s in ('retailer','kilim','online','goods')):relation='turkish_products'
 relation_tags.append(dict(entity_id=eid,relation_tag=relation,source_id=sid))
 for label in offer_labels:
  oid=f'W003-O{len(offerings)+1:03d}'
  otype='class' if any(w in label for w in ['講座','教室','制作体験']) else ('translation' if '翻訳' in label else ('food_service' if label=='カフェ' else 'retail'))
  offerings.append(dict(offering_id=oid,entity_id=eid,offering_type=otype,name=label,availability_status='unknown',verification_status='verified',verified_at=CHECKED,note='Presence shown on source page, current eligibility/availability not asserted.'))
  add_claim(f'{name}は「{label}」を案内している','offering',oid,sid,'offering_listed')
  if channel_type:
   # add channel once, link all eligible retail offerings
   pass
 if channel_type:
  cid=f'W003-C{len(channels)+1:03d}'
  # URL only store landing for products; product listings on actual shop pages count as transaction path.
  channels.append(dict(channel_id=cid,entity_id=eid,channel_type=channel_type,availability_status='unknown',verification_status='verified',verified_at=CHECKED,url=official_url,note='Site advertises products; checkout was not independently exercised.'))
  for offer in offerings:
   if offer['entity_id']==eid and offer['offering_type']=='retail':channel_offerings.append(dict(channel_id=cid,offering_id=offer['offering_id']))
  add_claim(f'{name}のサイトには商品購入に向けた通販案内がある','channel',cid,sid,'sales_channel_listed')
 for loc in locs:
  locname,lk,pref,city,address,access=loc
  lid=f'W003-L{len(locations)+1:03d}'
  loc_kind=lk if lk in ('store','restaurant','office','other','classroom') else 'other'
  locations.append(dict(location_id=lid,name=locname,location_kind=loc_kind,operational_status='unknown',verification_status='verified',verified_at=CHECKED,prefecture=pref,city=city,address=address,nearest_station='',public_access=access,visibility=('internal_only' if lk=='office' else 'public'),opened_at='',closed_at='',note='Do not equate published location with confirmed open-now availability; some locations have incomplete address.'))
  location_entities.append(dict(location_id=lid,entity_id=eid,relation_type=('based_at' if lk=='office' else 'operates_at'),valid_from='',valid_to=''))
  add_claim(f'{name}が「{locname}」の所在地を掲載している','location',lid,sid,'location_published')
  for channel in channels:
   if channel['entity_id']==eid and channel['channel_type']=='in_person':channel_locations.append(dict(channel_id=channel['channel_id'],location_id=lid))
 if review=='needs_review':reviews.append(dict(object_id=eid,severity='high',issue='Japan-facing fulfillment eligibility/local presence needs evidence; do not publish as domestic store.'))
# Additional offering source for second class at Jiyugaoka (not new Entity)
jiy=entities[5]['staged_entity_id'];sid=add_source('https://www.culture.gr.jp/detail/sk.jiyugaoka/4559538','official_website','イーネオヤ（第1土）')
for o in offerings:
 if o['entity_id']==jiy and o['name']=='イーネオヤ講座':
  add_claim('自由が丘産経学園でイーネオヤ（第1土）の2026年秋期案内がある','offering',o['offering_id'],sid,'offering_listed')
# Dated events from first-party calendars; keep historical events.
event_specs=[
('トルコの伝統手芸・オヤ 新刊作品展＆ワークショップ','exhibition_and_workshop','scheduled','2026-10-24','2026-11-06','date','https://clover.co.jp/workshop/oya2026','TOHO BEADS STYLE Tokyo Gallery t','東京都','台東区','東京都台東区柳橋1-9-11',''),
('WASABI-Elisi イーネオヤ教室（2026年10月25日）','handicraft_workshop','scheduled','2026-10-25T11:00','2026-10-25T13:00','minute','https://wasabielisi.com/?cbid=2172835&csid=16&mode=cate','','','','','W003-E007'),
('WASABI-Elisi イーネオヤ教室（2026年11月22日）','handicraft_workshop','scheduled','2026-11-22T11:00','2026-11-22T13:00','minute','https://wasabielisi.com/?cbid=2172835&csid=16&mode=cate','','','','','W003-E007'),
('トルコの伝統手芸・オヤ 作品展（2026年9月）','exhibition','completed','2026-09-03','2026-09-12','date','https://amimono.me/news/detail.html?id=548','ユヌス・エムレ（トルコ文化センター）','東京都','渋谷区','東京都渋谷区大山町1-19',''),
]
for name,evtype,status,start,end,precision,url,place,pref,city,address,org in event_specs:
 sid=add_source(url,'official_website' if 'wasabielisi' in url or 'clover.co' in url else 'media',name)
 lid=''
 if place:
  lid=f'W003-L{len(locations)+1:03d}'
  locations.append(dict(location_id=lid,name=place,location_kind='venue',operational_status='unknown',verification_status='verified',verified_at=CHECKED,prefecture=pref,city=city,address=address,nearest_station='',public_access='unknown',visibility='public',opened_at='',closed_at='',note='Third-party event venue; not owned by organizer.'))
 eid=f'W003-EV{len(events)+1:03d}'
 events.append(dict(event_id=eid,name=name,event_type=evtype,status=status,starts_at=start,ends_at=end,time_precision=precision,location_id=lid,organizer_entity_id=org,parent_event_id='',verification_status='verified',verified_at=CHECKED,note='Exact times/dates as displayed; confirm cancellations and remaining capacity at official source.'))
 add_claim(f'掲載された開催期間：{start}〜{end}','event',eid,sid,'event_dated',valid_from=start[:10],valid_to=end[:10])
# Two sources supporting the same exhibition, without duplicating Event.
for url in ['https://amimono.me/news/detail.html?id=548']:
 sid=add_source(url,'media','2026年10月オヤ展告知')
 add_claim('2026年10月24日〜11月6日のオヤ作品展・ワークショップが案内されている','event','W003-EV001',sid,'event_dated')
# Updates against known pilot ids and prior intake only. No canonically assumed mapping.
for legacy,category,summary,url,implication in [
 ('P048','offering','日本・トルコ協会 第105回秋期オンライン講座（2026年10月〜2027年2月）','https://www.tkjts.jp/turkish_lecture/2026/08/14/7357/','Existing P047 organization; update Offering P048 and dated term information, not new Entity'),
 ('P025/P026','channel','セヴィンチエイト イクスピアリ/アトレ竹芝 2026-27年の出店案内','https://sevinc8.com/','Existing branded business; events/pop-ups need venue and timing reconciliation'),
 ('P040/P042','event','トルコ文化センター 2026年10月26日料理教室','https://www.turkeycenter.co.jp/cooking/','Wave002 EV002 already exists: update its citations, do not duplicate Event'),
 ('W001-E023','identity','犬山市トルコ芸術専門店イスタンブールバザール','https://istanbulbazar.ocnk.net/','Possible relation to Wave001 Nagoya Istanbul Bazaar; verify same brand before Entity creation'),
 ('W001-E021','offering','hand craft shop kinari 名古屋 トルコランプ制作メニュー','https://handcraft-nagoya.com/menu','Add activity/Offering to existing wave001 candidate, no new Entity'),
]:
 existing_updates.append(dict(existing_ref=legacy,object_type=category,proposal=summary,evidence_url=url,action=implication,checked_at=CHECKED,merge_status='NOT_MERGED'))
# Write all normalized tables without string-encoded FK arrays.
tables={
 'entities.csv':(entities,['staged_entity_id','public_name','entity_kind','entity_subtype','status','identity_review_status','verification_status','verified_at','official_url','intake_state','canonical_entity_id','region_hint','note']),
 'locations.csv':(locations,['location_id','name','location_kind','operational_status','verification_status','verified_at','prefecture','city','address','nearest_station','public_access','visibility','opened_at','closed_at','note']),
 'location_entities.csv':(location_entities,['location_id','entity_id','relation_type','valid_from','valid_to']),
 'channels.csv':(channels,['channel_id','entity_id','channel_type','availability_status','verification_status','verified_at','url','note']),
 'channel_offerings.csv':(channel_offerings,['channel_id','offering_id']),
 'channel_locations.csv':(channel_locations,['channel_id','location_id']),
 'offerings.csv':(offerings,['offering_id','entity_id','offering_type','name','availability_status','verification_status','verified_at','note']),
 'events.csv':(events,['event_id','name','event_type','status','starts_at','ends_at','time_precision','location_id','organizer_entity_id','parent_event_id','verification_status','verified_at','note']),
 'sources.csv':(sources,['source_id','url','canonical_url','source_type','page_title','published_at','retrieved_at','note']),
 'claims.csv':(claims,['claim_id','claim_type','claim_value','verification_status','valid_from','valid_to','checked_at','supersedes_claim_id','note']),
 'claim_sources.csv':(claim_sources,['claim_id','source_id','support_type']),
 'claim_entities.csv':(claim_subjects['entity'],['claim_id','entity_id']),
 'claim_locations.csv':(claim_subjects['location'],['claim_id','location_id']),
 'claim_channels.csv':(claim_subjects['channel'],['claim_id','channel_id']),
 'claim_offerings.csv':(claim_subjects['offering'],['claim_id','offering_id']),
 'claim_events.csv':(claim_subjects['event'],['claim_id','event_id']),
 'entity_relation_tags.csv':(relation_tags,['entity_id','relation_tag','source_id']),
 'review_queue.csv':(reviews,['object_id','severity','issue']),
 'existing_update_proposals.csv':(existing_updates,['existing_ref','object_type','proposal','evidence_url','action','checked_at','merge_status']),
}
for name,(rows,cols) in tables.items():write(name,rows,cols)
counts={name.removesuffix('.csv'):len(rows) for name,(rows,_) in tables.items()}
manifest={'date':CHECKED,'state':'staging_candidate_not_canonical','counts':counts,'existing_updates':len(existing_updates),'baseline':{'canonical_v1_entity_count_reported':41,'canonical_v1_fixture_available':False,'pilot_records':60,'prior_staged_candidate_entities':36},'notes':['SSOT v1.0 unchanged','Events classified on 2026-10-22','All availability statuses unknown except dated events','Historical events preserved','Proposed updates not duplicated as new Entities']}
(STAGE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
