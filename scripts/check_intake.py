#!/usr/bin/env python3
"""Validate research intake schemas, staging foreign keys, URLs, and index, no dependencies."""
import csv, re, json, sys, unicodedata
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent.parent
WAVE=ROOT/'data'/'intake'/'wave003'

def load(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def require(test, msg):
 if not test:raise AssertionError(msg)
def distinct(rows,col):
 vals=[r[col] for r in rows];require(all(vals),f'empty {col}');require(len(vals)==len(set(vals)),f'duplicate {col}');return set(vals)

def norm(n):return re.sub(r'[\s\-‐‑–—・･·･_()（）「」【】\[\]]','',unicodedata.normalize('NFKC',n)).casefold()

def local_check():
 e=load(WAVE/'entities.csv');l=load(WAVE/'locations.csv');c=load(WAVE/'channels.csv');o=load(WAVE/'offerings.csv');s=load(WAVE/'sources.csv');cl=load(WAVE/'claims.csv');ev=load(WAVE/'events.csv')
 ids={'entity':distinct(e,'staged_entity_id'),'location':distinct(l,'location_id'),'channel':distinct(c,'channel_id'),'offering':distinct(o,'offering_id'),'source':distinct(s,'source_id'),'claim':distinct(cl,'claim_id'),'event':distinct(ev,'event_id')}
 for rowset,fk,dest in [(c,'entity_id','entity'),(o,'entity_id','entity')]:
  for r in rowset:require(r[fk] in ids[dest],f'invalid {fk}: {r}')
 for r in ev:
  if r['location_id']:require(r['location_id'] in ids['location'],'event location missing')
  if r['organizer_entity_id']:require(r['organizer_entity_id'] in ids['entity'],'event organizer missing')
  if r['parent_event_id']:require(r['parent_event_id'] in ids['event'],'parent event missing')
  require(r['status'] in {'scheduled','completed','cancelled','postponed','unknown'},'invalid event status')
  require(r['starts_at'] and r['ends_at'] and r['starts_at']<=r['ends_at'],'event date error')
 for r in e:
  require(r['status'] in ('active','inactive','unknown'),'bad entity status')
  require(r['identity_review_status'] in ('clear','provisional','needs_review'),'bad identity status')
  require(r['intake_state']=='candidate_sourced_unmerged' and not r['canonical_entity_id'],'unsafe merge state')
  require(r['official_url'].startswith('https://'),'no secure official url')
 for r in s:
  require(r['source_type'] in {'official_website','official_social','government','public_registry','media','directory','other'},'bad source type')
  require(urlsplit(r['url']).scheme in ('https','http') and urlsplit(r['url']).hostname,'bad url')
 for r in cl:require(r['verification_status'] in ('verified','unverified'),'bad verification')
 for table,src,dst in [('location_entities.csv','location_id','location'),('channel_locations.csv','channel_id','channel'),('channel_offerings.csv','channel_id','channel'),('claim_sources.csv','claim_id','claim'),('entity_relation_tags.csv','entity_id','entity')]:
  for row in load(WAVE/table):require(row[src] in ids[dst],f'FK {table}.{src}')
 for table,fks in [('location_entities.csv', [('entity_id','entity')]),('channel_locations.csv',[('location_id','location')]),('channel_offerings.csv',[('offering_id','offering')]),('claim_sources.csv',[('source_id','source')]),('entity_relation_tags.csv',[('source_id','source')])]:
  for row in load(WAVE/table):
   for field,dest in fks:require(row[field] in ids[dest],f'FK {table}.{field}')
 subjects=set()
 for table,fk,target in [('claim_entities.csv','entity_id','entity'),('claim_locations.csv','location_id','location'),('claim_channels.csv','channel_id','channel'),('claim_offerings.csv','offering_id','offering'),('claim_events.csv','event_id','event')]:
  for row in load(WAVE/table):
   require(row['claim_id'] in ids['claim'] and row[fk] in ids[target],f'bad ClaimSubject {table}')
   subjects.add(row['claim_id'])
 require(subjects==ids['claim'],'orphan claims detected')
 links=load(WAVE/'claim_sources.csv');supported={x['claim_id'] for x in links if x['support_type']=='supports'}
 require(supported==ids['claim'],'some Claims have no source support')
 require(all(x['support_type'] in ('supports','contradicts') for x in links),'invalid support type')
 require(len({norm(x['public_name']) for x in e})==len(e),'duplicate wave003 normalized names')
 # Only source-supported named entities, never numbers as merged canonical results.
 summary={'status':'PASS','wave003':{k:len(v) for k,v in ids.items()},'claim_source_support_coverage':f'{len(supported)}/{len(cl)}','claim_subject_coverage':f'{len(subjects)}/{len(cl)}','canonical_merged_count':0}
 return summary
if __name__=='__main__':
 try:
  print(json.dumps(local_check(),ensure_ascii=False,indent=2))
 except Exception as ex:
  print('FAIL:',str(ex),file=sys.stderr);sys.exit(1)
