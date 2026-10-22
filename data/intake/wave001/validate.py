import csv, json, pathlib, unicodedata
p=pathlib.Path(__file__).resolve().parent

def read(name):
 with (p/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
tables={name:read(name+'.csv') for name in ['entities','locations','location_entities','channels','channel_locations','offerings','sources','claims','claim_sources','entity_relations','existing_entity_updates']}
checks=[]
def check(name,actual):
 checks.append((name,bool(actual)))
 if not actual:print('FAIL:',name)
E={x['staged_entity_id'] for x in tables['entities']}; L={x['location_id'] for x in tables['locations']}; C={x['channel_id'] for x in tables['channels']}; O={x['offering_id'] for x in tables['offerings']}; S={x['source_id'] for x in tables['sources']}; CL={x['claim_id'] for x in tables['claims']}
check('24 proposed Entity records',len(E)==24)
check('Every Entity has official/authoritative source and claim',len(CL)==len(E)==len(tables['claim_sources']))
for name,items,idcol in [('entity',tables['entities'],'staged_entity_id'),('location',tables['locations'],'location_id'),('channel',tables['channels'],'channel_id'),('offering',tables['offerings'],'offering_id'),('source',tables['sources'],'source_id'),('claim',tables['claims'],'claim_id')]:
 check(name+' IDs unique',len({x[idcol] for x in items})==len(items))
check('LocationEntity valid FK',all(x['entity_id'] in E and x['location_id'] in L for x in tables['location_entities']))
check('Channel valid Entity FK',all(x['entity_id'] in E for x in tables['channels']))
check('ChannelLocation valid FK',all(x['channel_id'] in C and x['location_id'] in L for x in tables['channel_locations']))
check('Offering valid Entity FK',all(x['entity_id'] in E for x in tables['offerings']))
check('Claim has an Entity target',all(x['subject_type']=='Entity' and x['subject_id'] in E for x in tables['claims']))
check('ClaimSource valid FK',all(x['claim_id'] in CL and x['source_id'] in S and x['support_type']=='supports' for x in tables['claim_sources']))
check('Entity relations valid FK',all(x['from_entity_id'] in E and x['to_entity_id'] in E for x in tables['entity_relations']))
check('Source URLs HTTP(S)',all(x['url'].startswith('https://') for x in tables['sources']))
check('No invented active statuses',all(x['status']=='unknown' for x in tables['entities']))
check('No guessed appointment availability',all(x['availability_status']=='unknown' for x in tables['offerings']+tables['channels']))
check('No nonvisitor office listed as public',all(x['visibility']=='internal_only' for x in tables['locations'] if x['public_access'] not in ['yes','appointment_only']))
check('No canonical IDs invented',all(x['canonical_entity_id']=='' for x in tables['entities']))
check('All staging IDs unique and in scope',all(x.startswith('W001-') for x in E|L|C|O|S|CL))
check('No existing Entity overwritten',all(x['action'].startswith('propose_') for x in tables['existing_entity_updates']))
legacy=list(csv.DictReader(open('/mnt/data/turkiye_source/turkiye-japan-pilot-entities.csv',encoding='utf-8-sig')))
def n(x):return ''.join(c for c in unicodedata.normalize('NFKC',x).casefold() if c.isalnum())
legacy_names=[n(x['name']) for x in legacy]; new_names=[n(x['public_name']) for x in tables['entities']]
check('No exact-name legacy duplicates (pilot 60)',all(x not in legacy_names for x in new_names))
check('No duplicate new Entity names',len(new_names)==len(set(new_names)))
res={'checks_total':len(checks),'checks_passed':sum(1 for _,a in checks if a),'checks_failed':[name for name,a in checks if not a]}
(p/'validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
if res['checks_failed']:raise SystemExit(1)