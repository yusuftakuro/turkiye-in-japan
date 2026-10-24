# Start / resume the three-lane pilot

These are **launch instructions**, not agents already running. Chats and Work tasks cannot be created automatically by writing GitHub files.

## 00 — Coordination (existing Chat)
Use the existing Türkiye in Japan conversation. Reference Issue [#23](https://github.com/yusuftakuro/turkiye-in-japan/issues/23).

### Minimal new-conversation prompt if restarting 00
```text
Türkiye in Japan｜00 統括を引き継いでください。
最初に yusuftakuro/turkiye-in-japan の main から AGENTS.md と docs/ops/CURRENT.md、Issue #23 を読み、GitHubの最新HEAD・PR・CIを再確認してください。
01のIssue #21と02のIssue #22を管理し、制作・独立QAを統合してください。
作業状態は旧Chatから推測せず、根拠のあるRESULTだけで更新してください。
OWNER確認は仕様・正本・機密・大きな公開変更などの重要判断に限定してください。
```

## 01 — Content/Data production (new Work)
Choose **Work**, create a new task/chat and send:

```text
Türkiye in Japan｜01 制作として開始してください。
Repo: https://github.com/yusuftakuro/turkiye-in-japan
まず main の AGENTS.md、docs/ops/CURRENT.md、Issue #21 を取得し、HEADと既存PRを確認してください。
対象は ENT001 / ENT010 / ENT042 / ENT070 / ENT086 の5件だけ。
公式ソースを再確認し、状態・出典・差分・確認日時を記録した公開可能な候補資料を作ってください。
canonical CSV、ライブサイト、main は変更せず、専用branchに候補ファイルと短い検証結果を作成し、Draft PRまで進めてください。
独立QAと00の判断を待つ状態で完了し、勝手にmerge/publishしないでください。
```

## 02 — Independent QA (new separate Chat)
Create a new ordinary **Chat** first; Work can be added only if interactive browser execution is genuinely necessary:

```text
Türkiye in Japan｜02 独立QAとして開始してください。
Repo: https://github.com/yusuftakuro/turkiye-in-japan
main の AGENTS.md、docs/ops/CURRENT.md、Issue #22 と、制作Issue #21を確認してください。
作業はREAD_ONLYです。最初に現在の main SHA を固定し、対象 ENT001 / ENT010 / ENT042 / ENT070 / ENT086 の出典・状態・表示上のリスクを独立に検査してください。
制作01のPRが存在すればそのhead SHAを固定して再検証し、PASS/FAIL/INCONCLUSIVE・根拠URL・問題箇所・優先度をまとめて00に返してください。
IssueやPRの完了を仮定せず、canonical/main/siteに書き込まないでください。
```

## Rules for both new sessions
- Work/Chat are not necessarily continuous background workers. On each restart, reconstruct status from GitHub; do not promise autonomous scheduled delivery.
- Read only task-specific docs and minimal evidence. Do not copy whole history, or pay for multiple standing Workers without a proven throughput benefit.
- The pilot is read-only/candidate-only until new sources, QA and owner gates permit subsequent canonical/live changes.
