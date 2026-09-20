# R5B PRIVATE EVIDENCE HANDOVER

状態: PRIVATE / R5-B独立回答回収前は非公開
作成日: 2026-09-20

## 目的

この文書は、現在のChatが長文化・終了しても、R5-B後に使用する先駆者調査資料と運用判断を新しいChatへ確実に引き継ぐための非公開メモである。

## 主要資料

- `COUNCIL_CLI_BROWSER_RESEARCH_PRIVATE_DRAFT.md`
- 用途: Multi-AI CouncilのR5-B前後で比較に使う先駆者・外部調査資料
- 内容: 三社公式CLI、Browser方式、既存LLM Council実装、deterministic Orchestrator、RAW保存、timeout/retry、subscription認証、課金・権限・隔離等の比較
- R5-A回答の事後改変には使用しない

## R5-B前の扱い

1. この先駆者資料はR5-Bの三社独立回答が回収・凍結されるまでラウンド担当へ開示しない。
2. R5-Bでは、設問で明示したR5-Aまでの許可RAWのみを参照対象とする。
3. 先駆者資料、外部証拠一覧、関連する非公開メモはR5-B独立回答の根拠に含めない。
4. 一社だけに先に見せない。
5. R5-A回答を書き換えたり、後から内容を混ぜたりしない。

## 公開GitHubに関する注意

公開Council repoの以下は非開示保管場所として扱わない。

- main
- branch
- Draft PR
- Issue
- Discussion
- 公開commit

公開repoへ置けば、未Mergeでも第三者・ラウンド担当が発見可能である。
R5-B独立回答凍結前の保管はLibrary/ローカル等の非公開領域を使う。

## R5-B後の予定

1. ChatGPT / Claude / Gemini のR5-B独立回答を回収する。
2. 各回答を凍結し、参照時点と必要なhashを記録する。
3. その後、先駆者資料を公開または三社へ同時開示する。
4. 必要なら「R5-A/R5-B後に開示された追加証拠」と明示して追加比較・再評価を行う。
5. 先駆者資料を理由にR5-Aの過去回答を事後改変しない。

## 先駆者資料の当時の主要整理

当時の第一候補:
- 三社公式CLI + 判断を行わないvendor-neutral / deterministic Orchestrator

補助:
- 公式ブラウザAgentを一次資料取得や人間確認に限定

注意:
- CLIは監査・隔離・機械可読性で有利だが、実機試験合格までは本番採用を保証しない。
- Browserは限定bridgeとして残すが、三社共通の主経路にはしない。

## 新しいChatでの復帰手順

新しいChatでは最初に次のように依頼する。

「R5B_PRIVATE_EVIDENCE_HANDOVER.md と COUNCIL_CLI_BROWSER_RESEARCH_PRIVATE_DRAFT.md を読んで、Multi-AI Council R5-Bの非公開証拠運用を引き継いで。GitHub mainを正本とし、R5-B独立回答が凍結するまでは先駆者資料をラウンド担当へ見せないで。」

その後:
1. GitHub mainの現在状態を確認
2. R5-B設問と参照許可RAWを確認
3. R5-B独立回答回収前か後かを確認
4. 回収前なら先駆者資料を非開示のまま維持
5. 回収後なら先駆者資料の同時開示・比較へ進む

## 禁止

- R5-B前に先駆者資料を一社だけへ見せる
- 公開GitHub branch/PRを「非公開だから安全」とみなす
- 先駆者資料を使ってR5-A回答を書き換える
- API key / Billing / Credits / permission変更を独断で行う
- UNKNOWNを推測で埋める
