============================================================
MULTI-AI COUNCIL
ROUND 4 開始前 共通運用・参照環境ステータス
============================================================

最終更新: 2026年9月14日

【目的】

Round 4-A を開始する時点で、ChatGPT・Claude・Gemini が共通で参照する
現在の運用状態、参照経路、確認済みCapability、現在地を記録する。
これは議論の要約ではない。

【正本と現在の正式原則】

・GitHub repository が正本である。
・正式原則は COUNCIL_PRINCIPLES_RAW.md の原則1〜13である。
・個別RAWが一次記録であり、派生BundleやManifestは正本ではない。

【Gemini の正式参照経路】

GitHub正本
→ INDEX.md記載RAWを正規generatorで原文連結した GEMINI_NOTEBOOK_BUNDLE.md
→ --verify による順序・本文バイト列・SHA-256の検証
→ GitHub Actions
→ Apps Script
→ Google Drive上の同一 GEMINI_NOTEBOOK_BUNDLE.md
→ Gemini Notebook

GitHub SecretsおよびApps Scriptの秘密値は、repo本文に保存しない。

【確認済みCapability】

・BundleはINDEX記載RAWを順序どおり原文連結して生成される。
・--verifyで、対象RAWの順序、本文バイト列、SHA-256、およびGit index blobとの整合性を確認できる。
・GitHub ActionsからApps Scriptを経由し、Google Drive上のBundleを自動更新できる。
・Gemini NotebookにはGoogle Drive版Bundleを一度だけソース登録済みである。
・Drive更新後、Notebook側でソースの再登録、削除、手動更新を行わず、
  後から追加した未知値を読み取れた。Drive → Gemini Notebook の自動追従は実機確認済みである。
・ClaudeはGitHubのURLからRAW本文を取得できる。
・ただしURL取得経路で、現在mainではなく更新前の内容が返る事例が実測された。
  2026-09-14、新規Claudeチャットで確認したところ、
  COUNCIL_PRINCIPLES_RAW.md / CLAUDE_HANDOVER_RAW.md / ROUND4-5_PLAN_RAW.md の
  3ファイルで更新前の内容が返った。
  文書末尾まで取得できており、先頭や途中の内容も旧状態であったため、
  単純な末尾切り詰めでは説明できない。
  同日、一意なクエリを付けた再取得およびgit取得では現在版を確認できた。

【URL取得経路に関する未確定事項と運用】

未確定:
・古い内容が返る原因層が、GitHub/CDN側のキャッシュなのか、
  Claude/WebFetch等の中間取得層なのかは特定できていない。
  原因そのものはUNKNOWNとして扱う。

運用:
・Round開始前など重要な判断の前、またはRAW同士が食い違って見える場合は、
  1回のURL取得だけで断定せず、別経路でも確認する。
・?cachebust= を付けた再取得は、2026-09-14に有効だった具体例として記録する。
  固定手順ではない。原因が未確定であるため、この手段が今後も有効である保証はない。

【現在地】

・Round 1、Round 2、Round 3、Round 3-2は完了。
・次はRound 4-Aであり、開始準備段階である。
・各社固有の引き継ぎは、この共通情報がmainへ反映された後、
  HANDOVER_CHECKLIST_RAW.mdに従って各社自身が作成する。

【過去記録との関係】

GEMINI_FEATURE_VERIFICATION_RAW.md等に残る過去時点の記述は歴史記録である。
現在の運用状態・参照経路・確認済みCapabilityについては、
本ファイルを優先する。過去の実験RAWを現在の状態に合わせて遡及修正しない。

============================================================
END
============================================================
