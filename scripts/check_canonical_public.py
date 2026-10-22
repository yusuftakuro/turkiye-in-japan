#!/usr/bin/env python3
"""No dependencies. Enforce public-safe proposed data export integrity."""
from pathlib import Path
import csv,json,collections
D=Path(__file__).resolve().parents[1]/'data/canonical/v1.1-proposed'
if not D.is_dir():raise SystemExit('Missing data/canonical/v1.1-proposed')
def records(n):
 with (D/(n+'.csv')).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def require(cond,msg):
 if not cond:raise AssertionError(msg)
entities=records('entities');off=records('offerings');loc=records('locations');chan=records('channels');proof=records('new_claim_evidence')
require(len(entities)==67, 'expected exactly 67 Entity records, of which 26 are provisional')
new=[r for r in entities if r['entity_id']>='ENT042']
require(len(new)==26, 'expected 26 new provisional entities')
require(all(r['status']=='unknown' and r['identity_review_status']=='provisional' for r in new),'new entities must not be shown as confirmed currently active')
require(len(off)==71 and len(chan)==58, 'expected Offering 71 and Channel 58')
require(len(loc)==35, 'expected 35 public visitor-oriented Locations')
require(all(r['location_kind'] not in {'registered_address','contact_address','office'} for r in loc),'non-visitor locations leaked')
require(not set(x['location_id'] for x in loc)&{'LOC024','LOC025','LOC026','LOC046'},'non-public locations leaked')
require(all(r['operational_status'] in {'open','temporarily_closed','closed','unknown'} for r in loc),'bad location operational status')
E={r['entity_id'] for r in entities};O={r['offering_id'] for r in off};L={r['location_id'] for r in loc};C={r['channel_id'] for r in chan}
for tab,refs in [('offerings',{'entity_id':E}),('channels',{'entity_id':E}),('location_entities',{'entity_id':E,'location_id':L}),('channel_locations',{'channel_id':C,'location_id':L}),('channel_offerings',{'channel_id':C,'offering_id':O}),('entity_relation_tags',{'entity_id':E}),('entity_relations',{'subject_entity_id':E,'object_entity_id':E}),('offering_topics',{'offering_id':O})]:
 for row in records(tab):
  for field,ok in refs.items():require(row[field] in ok,f'broken FK {tab}:{field}:{row[field]}')
proof_by=collections.defaultdict(list)
for r in proof:
 require(r['source_url'].startswith('http'),'proof without source URL')
 typ=r['object_type'];assert typ in {'entity','offering','channel'},typ
 ok={'entity':E,'offering':O,'channel':C}[typ]
 require(r['object_id'] in ok,'proof orphan '+r['object_id'])
 proof_by[r['object_id']].append(r)
require(all(r['entity_id'] in proof_by for r in new),'new Entity without public provenance')
require(not any(r['availability_status']=='available' for r in off if r['entity_id'] in {x['entity_id'] for x in new}), 'provisional offerings incorrectly advertised available')
print(json.dumps({'result':'PASS','entities':len(E),'new_provisional_entities':len(new),'offerings':len(O),'channels':len(C),'public_locations':len(L),'evidence_rows':len(proof)},ensure_ascii=False))
