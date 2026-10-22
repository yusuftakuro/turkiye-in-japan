#!/usr/bin/env python3
"""Offline lookup for the staged research registry. Usage: python3 scripts/query_registry.py キリム"""
from pathlib import Path
import sqlite3, sys
root=Path(__file__).resolve().parent.parent
path=root/'integrated'/'research_registry.sqlite3'
if not path.exists():
 print('First run: python3 scripts/consolidate.py');sys.exit(2)
q=' '.join(sys.argv[1:]).strip()
if not q:print('Usage: python3 scripts/query_registry.py <日本語・トルコ語・英語の検索語>');sys.exit(2)
with sqlite3.connect(path) as c:
 rows=c.execute('SELECT candidate_id,name,region,kind,source_url FROM candidates WHERE name LIKE ? OR region LIKE ? OR kind LIKE ? ORDER BY wave,name LIMIT 40',(f'%{q}%',)*3).fetchall()
for id,name,region,kind,url in rows:print(f'{id}\t{name}\t{region}\t{kind}\n  {url}')
print(f'{len(rows)} matches (staging candidates; not canonical or live availability).')
