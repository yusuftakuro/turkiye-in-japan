#!/usr/bin/env python3
"""Build reproducible (not canonical) research registry + SQLite search DB from sourced wave CSVs."""
import csv, sqlite3, re, io, json, unicodedata, difflib, sys
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
INDIR=ROOT/'data'/'intake';OUT=ROOT/'integrated';OUT.mkdir(exist_ok=True)

def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows,cols):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(s):return re.sub(r'[\s\-‐‑–—・･·_()（）「」【】\[\]。、]+','',unicodedata.normalize('NFKC',s or '')).casefold()
def domain(s):return (urlsplit(s).hostname or '').lower().removeprefix('www.')

candidates=[];sources=[];claims=[];reviews=[];status=[]
for wave in ('wave001','wave002','wave003'):
 folder=INDIR/wave
 entities=load(folder/'entities.csv');srcs=load(folder/'sources.csv');cls=load(folder/'claims.csv');cs=load(folder/'claim_sources.csv')
 sources.extend(dict(x,wave=wave) for x in srcs)
 claims.extend(dict(x,wave=wave) for x in cls)
 source_by_id={s['source_id']:s for s in srcs}
 mapping={x['claim_id']:x['source_id'] for x in cs if x['support_type']=='supports'}
 # The wave003 ClaimEntity typed junction is authoritative; wave001/2 use summary identity claim ID by position.
 claims_by_entity={}
 if (folder/'claim_entities.csv').exists():
  for x in load(folder/'claim_entities.csv'):claims_by_entity.setdefault(x['entity_id'],[]).append(x['claim_id'])
 for idx,ent in enumerate(entities,1):
  eid=ent['staged_entity_id']
  if claims_by_entity:
   claim_ids=claims_by_entity.get(eid,[])
  else:
   claim_ids=[f'W{wave[-3:]}-CL{idx:03d}']
  # Prior waves did not guarantee one-to-one row order; fallback exact official URL source.
  source_urls=[source_by_id[mapping[claim_id]]['url'] for claim_id in claim_ids if claim_id in mapping and mapping[claim_id] in source_by_id]
  if not source_urls:
   named=ent.get('official_url','')
   source_urls=[x['url'] for x in srcs if x['url']==named] or [named]
  u=ent.get('official_url') or source_urls[0]
  candidates.append(dict(candidate_id=eid,wave=wave[-3:],name=ent['public_name'],kind=ent.get('entity_kind',''),subtype=ent.get('entity_subtype',''),region=ent.get('region_hint',''),official_url=u,source_url=source_urls[0],verification_status=ent.get('verification_status',''),identity_review_status=ent.get('identity_review_status',''),status=ent.get('status','unknown'),merge_state='NOT_MERGED',canonical_id='',source_count=len(set(source_urls)),review_note=ent.get('note','')))
 if (folder/'review_queue.csv').exists():
  reviews.extend(dict(wave=wave, **r) for r in load(folder/'review_queue.csv'))
 status.append((wave,len(entities),len(srcs),len(cls)))
assert len(candidates)==54 and len({x['candidate_id'] for x in candidates})==54
names=[norm(x['name']) for x in candidates]
assert len(set(names))==54, 'Normalized exact duplication across waves'
assert all(x['source_url'].startswith(('https://','http://')) for x in candidates),'Missing sources'
# Conservatively log near matches without auto-merging names, domains or brands.
flags=[]
for i,a in enumerate(candidates):
 for b in candidates[:i]:
  if a['official_url'] and b['official_url'] and a['official_url']==b['official_url']:
   flags.append(dict(id_a=a['candidate_id'],id_b=b['candidate_id'],reason='same_official_url',score='1.00',resolution='needs_review'))
  elif norm(a['name'])==norm(b['name']):
   flags.append(dict(id_a=a['candidate_id'],id_b=b['candidate_id'],reason='exact_normalized_name',score='1.00',resolution='needs_review'))
  else:
   ratio=difflib.SequenceMatcher(None,norm(a['name']),norm(b['name'])).ratio()
   if ratio>=0.83:flags.append(dict(id_a=a['candidate_id'],id_b=b['candidate_id'],reason='similar_name',score=f'{ratio:.3f}',resolution='needs_review'))
# If the first 60-pilot reference is present locally, use only as a blocker for human review.
pilot_path=INDIR/'pilot_identity_index.csv';pilot=load(pilot_path) if pilot_path.exists() else []
for a in candidates:
 for b in pilot:
  nm=norm(b['raw_name']);ratio=difflib.SequenceMatcher(None,norm(a['name']),nm).ratio()
  if nm and (norm(a['name'])==nm or ratio>=0.90):
   flags.append(dict(id_a=a['candidate_id'],id_b=b['pilot_id'],reason='pilot_name_collision',score=f'{ratio:.3f}',resolution='needs_review'))
# Exact shared domains can be branch/partner sites. A warning, never a forced merge.
for i,a in enumerate(candidates):
 for b in candidates[:i]:
  if a['official_url'] and b['official_url'] and domain(a['official_url'])==domain(b['official_url']) and a['official_url']!=b['official_url']:
   flags.append(dict(id_a=a['candidate_id'],id_b=b['candidate_id'],reason='shared_domain',score='',resolution='needs_review'))
# De-dup warning rows only.
flags=list({(x['id_a'],x['id_b'],x['reason']):x for x in flags}.values())
write(INDIR/'candidate_catalog.csv',candidates,list(candidates[0]))
write(OUT/'possible_duplicates.csv',flags,['id_a','id_b','reason','score','resolution'])
# SQLite query/read-only research layer; do not use as SSOT canonical fixture.
db=OUT/'research_registry.sqlite3'
if db.exists():db.unlink()
conn=sqlite3.connect(db)
conn.executescript('''PRAGMA foreign_keys=ON;
CREATE TABLE candidates(candidate_id TEXT PRIMARY KEY, wave TEXT NOT NULL, name TEXT NOT NULL, kind TEXT, subtype TEXT, region TEXT, official_url TEXT, source_url TEXT NOT NULL, identity_review_status TEXT, status TEXT, merge_state TEXT CHECK(merge_state='NOT_MERGED'), canonical_id TEXT);
CREATE TABLE sources(source_id TEXT PRIMARY KEY,wave TEXT,url TEXT NOT NULL,page_title TEXT);
CREATE TABLE claims(claim_id TEXT PRIMARY KEY,wave TEXT,claim_type TEXT,claim_value TEXT,checked_at TEXT);
CREATE TABLE duplicates(id_a TEXT,id_b TEXT,reason TEXT,score TEXT,resolution TEXT);
CREATE INDEX idx_region ON candidates(region);CREATE INDEX idx_wave ON candidates(wave);
''')
conn.executemany('INSERT INTO candidates VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',[[x[k] for k in ('candidate_id','wave','name','kind','subtype','region','official_url','source_url','identity_review_status','status','merge_state','canonical_id')] for x in candidates])
conn.executemany('INSERT INTO sources VALUES(?,?,?,?)',[(s['source_id'],s['wave'],s['url'],s.get('page_title','')) for s in sources])
conn.executemany('INSERT INTO claims VALUES(?,?,?,?,?)',[(s['claim_id'],s['wave'],s.get('claim_type',''),s.get('claim_value',''),s.get('checked_at','')) for s in claims])
conn.executemany('INSERT INTO duplicates VALUES(?,?,?,?,?)',[(x['id_a'],x['id_b'],x['reason'],x['score'],x['resolution']) for x in flags])
try:
 conn.execute("CREATE VIRTUAL TABLE candidate_fts USING fts5(candidate_id UNINDEXED, name, kind, region)")
 conn.executemany('INSERT INTO candidate_fts VALUES(?,?,?,?)',[(x['candidate_id'],x['name'],x['kind'],x['region']) for x in candidates]);fts=True
except sqlite3.OperationalError:fts=False
conn.commit()
assert conn.execute('SELECT count(*) FROM candidates').fetchone()[0]==54
assert conn.execute("SELECT count(*) FROM candidates WHERE merge_state != 'NOT_MERGED'").fetchone()[0]==0
assert conn.execute('PRAGMA foreign_key_check').fetchall()==[]
conn.close()
summary={'status':'PASS','canonical_entity_fixture_loaded':False,'reported_existing_canonical_entities':41,'pilot_raw_rows':len(pilot),'staged_candidates':len(candidates),'wave_counts':{v[0]:{'entities':v[1],'sources':v[2],'claims':v[3]} for v in status},'total_staging_sources':len(sources),'total_staging_claims':len(claims),'candidate_coverage_source_url':sum(bool(x['source_url']) for x in candidates),'exact_normalized_duplicates':len(names)-len(set(names)),'potential_identity_matches':len(flags),'sqlite_fts5':fts,'canonical_merged_count':0,'scope_notes':['Names, entities and locations do not share a one-row = one-business assumption.','Prior 60 pilot records are separate from 41 canonical Entities.','P013 and P057 original pilot rows are not authoritative.','Source URL on a page does not confirm real-time operation or shop availability.']}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
