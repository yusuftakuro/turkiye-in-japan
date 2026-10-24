# START — 00/01/02 continuation (2026-10-24)

This is a copy-ready manual restart sheet. Writing an Issue does not automatically launch Work/Chat.

## 00 — Coordinator (this existing Chat)
```text
Türkiye in Japan｜00 統括を引き継いでください。
GitHub: https://github.com/yusuftakuro/turkiye-in-japan
main の AGENTS.md、docs/ops/CURRENT.md、Issue #23、PR #25、Issue #26、#27、#22を最新状態で確認してください。
01の制作候補PRと02の独立QAを統合し、重要な正本・主体・プライバシー・公開判断だけOwnerに確認してください。
```

## 01 — Producer (Work; next: Issue #26)
```text
Türkiye in Japan｜01 制作を継続してください。
Repo: https://github.com/yusuftakuro/turkiye-in-japan
main の AGENTS.md、docs/ops/CURRENT.md、Issue #26、既存Draft PR #25、Issue #22のQA結果を確認してください。
今回はP1：Dogal（ENT010）のオンライン販売終了（2026-05-31）と、OFF011/CH002の古いavailable表示、検索一覧・詳細ページの誤認を防ぐ修正候補です。
公式根拠を再確認し、フルSSOT（私有）と公開用投影の違いを維持し、変更範囲を最小化してください。
新規ブランチでDraft PRを作り、関連するテストと生成済みHTMLの差分を検査してください。
カフェ・旧実店舗を勝手に同一扱いしないこと。正式DB、main、本番サイトの変更・マージ・公開は行わないこと。
結果はIssue #26と00へ、PR URL・head SHA・根拠・未確認事項・テスト結果を返してください。
```

## 02 — Independent QA (separate Chat; READ_ONLY)
```text
Türkiye in Japan｜02 独立QAを継続してください。
Repo: https://github.com/yusuftakuro/turkiye-in-japan
AGENTS.md、docs/ops/CURRENT.md、Issue #22、Issue #26、Draft PR #25を確認してください。
以前のPR #25の判定は総合HOLDです。未実行だった個別検査の実施可否・結果を明示してください。
01がIssue #26の新Draft PRを作成済みならhead SHAを固定し、Dogalオンライン販売終了と公開DB・検索一覧・詳細表示の整合性を独立に検証してください。
PASS/FAIL/INCONCLUSIVEと出典、未検証箇所、修正要否を00へ報告してください。
READ_ONLY厳守。GitHub書き込み、PRコメント、DB・コード・サイト変更、マージ、公開は禁止です。
```

## Later
Issue #27 (Keio autumn Turkish course) is queued until #26 review. Do not launch simultaneous workers editing the same generator or public data. 00 will authorize next stage after the P1 correction is reviewed.
