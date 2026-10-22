#!/usr/bin/env python3
"""Reconcile the accepted Türkiye in Japan SSOT v1 fixture against staged research.
Usage: python reconcile.py --canonical-dir /path/to/ssot-v1-fixture --intake-dir /path/to/data/intake --output-dir /path/to/results

Produces a REVIEW crosswalk only: it never changes canonical identifiers, Claims, or published site data.
"""
import argparse, csv, json, re, unicodedata, collections
from pathlib import Path
from urllib.parse import urlparse
from difflib import SequenceMatcher

# Editorial review of identity, scope, and granularity. These are NOT approvals to merge.
MANUAL = {
 'W001-E001': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT025','none','大阪と芝大門は別の施設・別公式ドメイン。名称の共通語だけでは同一性を認めない。'),
 'W001-E002': ('OPERATOR_RELATION_REVIEW','','','大阪トルコ文化センター等との運営・連携関係を確認。法人と講座提供施設は別の粒度。'),
 'W001-E003': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT029','none','京都の団体と既存の日本トルコ文化交流会は表記が近いが公式情報・所在地が異なる。別主体性を確認。'),
 'W001-E004': ('INTRA_INTAKE_RELATION_REVIEW','','','同一公式サイトのW001-E005串本町トルコ文化センターと、団体・施設の実体を確認。'),
 'W001-E005': ('INTRA_INTAKE_RELATION_REVIEW','','','W001-E004と同一公式サイト。施設・Offeringにすべきか検討。芝大門ENT025とは別。'),
 'W001-E008': ('INTRA_INTAKE_RELATION_REVIEW','','','W001-E009タイヨウのカフェとの主体・店舗の位置付けを確認。'),
 'W001-E009': ('INTRA_INTAKE_RELATION_REVIEW','','','W001-E008 KCRの公式サイトを共有。店舗ブランド/Location/Offeringの切り分けを確認。'),
 'W001-E016': ('DIPLOMATIC_OFFICE_REVIEW','ENT030','separate_office','名古屋総領事館は東京の大使館と異なる公館。所属関係と一般来訪可否を別途確認。'),
 'W001-E017': ('DIPLOMATIC_OFFICE_REVIEW','ENT030','separate_office','在大阪名誉総領事館は独立窓口候補。W001-E018/019と同一の外務省一覧URLは同一主体の証拠でない。'),
 'W001-E018': ('DIPLOMATIC_OFFICE_REVIEW','ENT030','separate_office','在和歌山名誉総領事館は独立窓口候補。共通一覧URLのみで統合しない。'),
 'W001-E019': ('DIPLOMATIC_OFFICE_REVIEW','ENT030','separate_office','在福岡名誉総領事館は独立窓口候補。共通一覧URLのみで統合しない。'),
 'W001-E020': ('ENTITY_OR_OFFERING_REVIEW','','','大阪大学トルコ語専攻は大学の教育Offeringか独立して識別する学科組織か粒度判定。'),
 'W001-E022': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT006','none','キリムアナトリア京都とANATOLIA飲食店は名称中のAnatoliaが共通するだけ。'),
 'W001-E023': ('BRAND_IDENTITY_REVIEW','ENT001','none','名古屋イスタンブールバザールと既存イスタンブール飲食店は同一主体の根拠なし。別に犬山の同名系ECが存在。'),
 'W002-E001': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT026','none','九州・トルコ協会と一般社団法人日本・トルコ協会は公式ドメインが違う。地域団体の同一性未確認。'),
 'W002-E002': ('NON_CANONICAL_PARENT_REVIEW','ENT033','none','中近東文化センターはアナトリア考古学研究所の親財団。既存ENT033三笠宮記念財団と同一法人ではない。'),
 'W002-E003': ('FOREIGN_LOCATION_SCOPE_REVIEW','ENT033','related_not_same','アナトリア考古学研究所は中近東文化センター附属で主たる研究拠点はトルコ。東京連絡先・国内講座の切り分け要。既存ENT033は支援財団で別。'),
 'W002-E004': ('ENTITY_OR_OFFERING_REVIEW','','','東京外国語大学のトルコ語教育はOffering。全大学を代表Entityとするか学科・授業を中心にするか整理。'),
 'W002-E005': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT035','none','日本トルコモザイクランプ協会は既存モザイクランプ★まむとは同一主体の証拠なし。'),
 'W002-E011': ('CANONICAL_PARENT_RELATION_REVIEW','ENT030','part_of_review','文化広報参事官室は公式に大使館の部門を名乗る。ENT030の別Entityとして所属関係を設けるかOffering/Channelで扱うか判定。'),
 'W002-E012': ('HISTORICAL_ONLY_IDENTITY_REVIEW','','','過去の催事情報でブランド名の根拠はあるが現在の事業主体・継続性は未確認。'),
 'W003-E001': ('ENTITY_OR_OFFERING_REVIEW','','','慶應外語は大学内プログラム。トルコ語講座はOfferingとして登録し、運営主体Entity粒度を確認。'),
 'W003-E002': ('ENTITY_OR_OFFERING_REVIEW','','','慶應義塾大学言語文化研究所の単発・特別講座はOffering/Event。独立部局Entityの要否を整理。'),
 'W003-E003': ('ENTITY_OR_OFFERING_REVIEW','','','朝日カルチャーセンター横浜教室の恒常教室とトルコ関連講座を分離。'),
 'W003-E004': ('ENTITY_OR_OFFERING_REVIEW','','','NHK文化センター梅田教室の施設とトルコ語Offeringを分離。'),
 'W003-E005': ('ENTITY_OR_OFFERING_REVIEW','','','ヨークカルチャーセンター大船の施設とトルコ語Offeringを分離。'),
 'W003-E006': ('ENTITY_OR_OFFERING_REVIEW','','','自由が丘産経学園の教室とトルコ関連講座を分離。W003-E005と同じドメインでも別の教室。'),
 'W003-E009': ('NAME_LOOKALIKE_DISTINCT_REVIEW','ENT006','none','ANATOLIAN RUGS（絨毯）とANATOLIA（レストラン）は別の公式ドメイン・業態。名称類似で統合しない。'),
}

def rows(path):
 with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(x):
 return re.sub(r'[\s\-‐‑–—・･_()（）「」【】\[\].,:：]+','',unicodedata.normalize('NFKC',x or '')).casefold()
def host(x):
 return (urlparse(x or '').hostname or '').lower().removeprefix('www.')
def writecsv(path, data, fields):
 with open(path,'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)

def main():
 p=argparse.ArgumentParser();p.add_argument('--canonical-dir',type=Path,required=True);p.add_argument('--intake-dir',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
 a.output_dir.mkdir(parents=True,exist_ok=True)
 canon=rows(a.canonical_dir/'entities.csv');candidates=rows(a.intake_dir/'candidate_catalog.csv');aliases=rows(a.canonical_dir/'entity_aliases.csv');oldpilot=rows(a.canonical_dir/'pilot_record_mapping.csv'); sources=rows(a.canonical_dir/'sources.csv')
 assert len(canon)==41 and len(candidates)==54 and len(oldpilot)==60, 'unexpected baseline dimensions'
 assert len({x['candidate_id'] for x in candidates})==54, 'candidate IDs not unique'
 amap=collections.defaultdict(list)
 for x in aliases:amap[x['entity_id']].append(x['alias'])
 match_rows=[];seen=collections.Counter();identical_urls=[]
 for n in candidates:
  possible=[]
  for c in canon:
   names=[c['public_name']]+amap[c['entity_id']]
   sc=max(SequenceMatcher(None,norm(n['name']),norm(name)).ratio() for name in names)
   exact=any(norm(n['name'])==norm(name) for name in names)
   same_official=bool(host(n['official_url']) and host(n['official_url'])==host(c['official_url']))
   if exact or same_official:identical_urls.append((n['candidate_id'],c['entity_id'],exact,same_official))
   possible.append((int(sc*100),c,exact,same_official))
  possible.sort(key=lambda x:x[0],reverse=True)
  lead=possible[0];typ,related_id,relation,note=MANUAL.get(n['candidate_id'],('NO_CANONICAL_COLLISION_DETECTED','','','公式URL・名称の厳密一致なし。正式追加前に本人性・地域・現況を最終確認。'))
  if related_id and related_id not in {c['entity_id'] for c in canon}:raise ValueError('invalid manually assigned canonical relation')
  # Fuzzy comparison is triage metadata, NEVER a relation assertion.
  x={
   'candidate_id':n['candidate_id'],'candidate_name':n['name'],'wave':n['candidate_id'].split('-')[0],
   'disposition':typ,'confirmed_same_canonical_entity_id':'',
   'related_canonical_entity_id_for_review':related_id,'relation_hypothesis':relation,
   'nearest_canonical_name':lead[1]['public_name'],'nearest_canonical_id':lead[1]['entity_id'],'fuzzy_name_score_0_100':lead[0],
   'candidate_official_url':n['official_url'],'review_reason':note,'canonical_merge_status':'NOT_MERGED',
   'review_status':'MANUAL_REVIEW_REQUIRED' if typ!='NO_CANONICAL_COLLISION_DETECTED' else 'PRELIMINARY_NO_COLLISION'
  }
  seen[typ]+=1;match_rows.append(x)
 assert not identical_urls, f'Exact identity/host matches: {identical_urls}'
 fields=list(match_rows[0]);writecsv(a.output_dir/'candidate_crosswalk.csv',match_rows,fields)
 dup_path=a.intake_dir.parent.parent/'integrated/possible_duplicates.csv'
 dup=rows(dup_path) if dup_path.exists() else []
 source_hosts={host(x['url']) for x in sources if host(x['url'])}
 overlap=[r['candidate_id'] for r in candidates if host(r['official_url']) in source_hosts and host(r['official_url'])!='mofa.go.jp']
 assert not overlap, 'Shared unrelated canonical source domain requires review'
 previous=rows(a.canonical_dir/'acceptance-test-results.csv');assert len(previous)==46 and all(r['result']=='PASS' for r in previous)
 report={
  'canonical_reference':'SSOT v1.0 accepted archive',
  'canonical_entities':len(canon),'canonical_locations':len(rows(a.canonical_dir/'locations.csv')),
  'canonical_channels':len(rows(a.canonical_dir/'channels.csv')),
  'canonical_offerings':len(rows(a.canonical_dir/'offerings.csv')),
  'canonical_events':len(rows(a.canonical_dir/'events.csv')),
  'canonical_sources':len(sources),'canonical_claims':len(rows(a.canonical_dir/'claims.csv')),
  'canonical_pilot_mapping':len(oldpilot),'legacy_evidence_unique_ids':len({r['v02_evidence_id'] for r in rows(a.canonical_dir/'legacy_evidence_to_v1_mapping.csv')}),
  'canonical_original_acceptance_tests_pass':46,
  'research_candidates':len(candidates),'confirmed_exact_existing_entity':len(identical_urls),
  'staged_no_canonical_collision_detected':seen['NO_CANONICAL_COLLISION_DETECTED'],
  'staged_requires_identity_scope_grain_or_relationship_review':len(candidates)-seen['NO_CANONICAL_COLLISION_DETECTED'],
  'classifications':dict(sorted(seen.items())),'canonical_new_entities_merged':0,
  'distinct_candidate_official_domains_matching_canonical_official_domains':0,
  'unresolved_same_source_not_same_subject_pairs_in_staging':len(dup),
  'methodology':'Exact normalized names and direct alias matches, official domain comparisons, editorial crosswalk, no automatic merge. Source page directory domain reuse is not entity proof.',
  'limitations':['Cannot prove entity identity from absence of a fuzzy/name/domain collision','Some staged Entity objects likely better represented as Offering or parent-child departments','Parent association and consular offices must not be merged because of shared URLs','No live business-availability assertion from identity verification.']
 }
 (a.output_dir/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=[
 '# SSOT v1.0 × 調査候補54件 照合レポート','',
 '基準日：2026-10-22。照合資料：確定版SSOT v1.0の実体ZIP、調査Wave001–003。',
 '', '## 数量と結論',
 f"- 確定版: Entity {report['canonical_entities']}、Location {report['canonical_locations']}、Channel {report['canonical_channels']}、Offering {report['canonical_offerings']}、Event {report['canonical_events']}。",
 f"- 元Pilot {len(oldpilot)}件、旧Evidence {report['legacy_evidence_unique_ids']} IDsを実ファイルで確認。",
 f"- 新規調査候補 {len(candidates)}件: **正本との同名/別名の完全一致・公式ドメイン一致は 0件**。ただし同一主体が存在しないとの断定ではない。",
 f"- 自動照合で明らかな衝突が見えない候補 {report['staged_no_canonical_collision_detected']}件、要精査{report['staged_requires_identity_scope_grain_or_relationship_review']}件。",
 '- 既存正本の書き換え・新規採用は **0件**。新しい「41 + 54 = 95 Entity」は確定値ではない。',
 '- 54件は3つの独立した研究候補で、専攻・授業・公館内の部門を含む。独立Entityへの昇格はObject定義に沿って判断する。',
 '', '## 重要な判定',
 '- **W002-E011 大使館文化広報参事官室**: ENT030 駐日大使館に属すると公式が自己紹介している。同一Entityか別部門Entityか判定し、誤って新しい独立公館として数えない。',
 '- **W002-E003 アナトリア考古学研究所**: 公益財団法人中近東文化センター附属。研究拠点はトルコ、国内での講座・事務窓口もあり。ENT033三笠宮記念財団は別の支援者。研究所を日本国内Entityとして新規追加するかはScopeを先に決める。',
 '- **W001-E001 大阪トルコ文化センター** と **ENT025 芝大門トルコ文化センター**: 一般名詞が同じだけで混同禁止。',
 '- **W001-E022 キリムアナトリア京都** と **ENT006 ANATOLIAレストラン**、**W003-E009 ANATOLIAN RUGS** とENT006も名称が似るが別の公式ドメイン・業態。自動統合禁止。',
 '- **W001-E017〜019 名誉総領事館**: 同じ外務省公館一覧URLに掲載されていても別地域・別オフィス。来訪可能性も未確認。',
 '- **W003-E003〜006 カルチャースクール/講座**: 施設/教室の主体はEntity、トルコ語や文化講座はOffering、特定日程はEventに分ける。',
 '- **W002-E012 ラビレント**: 過去の百貨店催事を根拠に、現時点の店舗や営業中Entityとしない。',
 '', '## 既存Entityへの追加提案（新規Entityではない）',
 '- P048→ENT026 日本・トルコ協会 / OFF035 トルコ語講座。2026年度講座はOfferingの開催期情報として追加提案。',
 '- P040/P042→ENT025 トルコ文化センター / OFF030 料理教室。日付のある開催回はEventで接続し、同一開催回を重複作成しない。',
 '- P025/P026→ENT017 と ENT041 セヴィンチエイト。同一事業者と決めつけず、2つの既存Entityを維持して変化を追う。',
 '', '## 回帰テスト',
 '- ZIP同梱の受入結果46件PASSを確認。実行スクリプトはv03/v02_evidence_map.csvを相対パス参照するがZIPに同ファイルがないため、そのまま再実行するとFileNotFoundErrorとなる。',
 '- 同梱legacy_v02_evidence.csv（222行）を検査用の相対パスへ複写する互換処理で46件を再実行し、46/46 PASS。**元アーカイブは変更していない**。',
 '', '## 正式統合ゲート',
 '1. このcrosswalk内の要精査項目を同一主体/別主体/Offering/国外拠点の観点で確定。',
 '2. 新しいEntityのみ正本IDを採番。親組織・ブランドや既存のProgramに接続するものはEntity件数に加算しない。',
 '3. stagingデータのClaim（特にWave001の一行集約）をatomicに分割、Source、ClaimSource、型別ClaimSubjectを検査。',
 '4. Entity関係、Location、Channel、Offering、Event、TopicのFKとstatusを再検証し、旧Evidenceの追跡関係を保持。',
 '5. 新規正本として採用した別PRで改めて全46テストを実行する。',
 '', '実ファイルでの判定内訳は `candidate_crosswalk.csv` を参照。'
 ]
 (a.output_dir/'reconciliation-report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()