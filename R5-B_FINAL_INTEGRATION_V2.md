# Multi-AI Council Round 5-B 最終統合記録 v2

日付: 2026-09-21  
状態: R5-B三社RAW、ユーザー最終判断、3社最終承認を固定する統合記録  
外部model実行: なし  
既存R5-B RAW: 変更なし

## 1. 正本と構成

本記録は、main上の次の三社RAWを入力として作成した。本文の詳細な独立回答は各RAWを正本として参照する。

- `CHATGPT_R5-B_RAW.md`
- `CLAUDE_R5-B_RAW.md`
- `GEMINI_R5-B_RAW.md`

三社RAWのSHA-256は作業時点で次のとおり。

| ファイル | SHA-256 |
|---|---|
| CHATGPT_R5-B_RAW.md | 79C38353C23B1DB1B56EEE8D0B73465030386C406F0F0339A4B83ADDBCB0B403 |
| CLAUDE_R5-B_RAW.md | F8867B817160ED7DA63AFE4CAB813CA4E31612A20210F4D0142A4905FCA8BDEF |
| GEMINI_R5-B_RAW.md | 83FF18C6B23AEA40E9D2D522A42E3AFBE01A11667F2941F2988AD8B756C3B235 |

## 2. ユーザー最終判断

ユーザーは、R5-B三社RAW・ユーザー判断・v2について、重大な問題なしとして最終比較へ進むことを承認した。特に次を承認済みとする。

- 原則8のCLI限定例外は、許可範囲・禁止範囲・失敗時の縮退・最初の5案件checkpointを含む。
- fan-outは秘密情報、認証情報、個人情報、非公開コード等を含む、または安全に否定できない場合に送信せず、人間確認まで停止する。
- 保存と外部送信を別の安全境界として扱う。
- 2/3一致を初期状態で正式合意にしない。
- 安全警告、追加課金、Merge、最終採用は人間へ返す。
- baselineを取得しない場合、厳密な改善率比較はできない。
- agyの当時の能力はR5-A/B時点ではUNKNOWNとし、後発の実機証拠とは分離する。
- Round 5-Cは不要とする。

## 3. 三社最終承認

三社の最終確認は次のとおり。

- ChatGPT: A. 承認
- Claude: A. 承認
- agy / Gemini: A. 承認

任意改善として、model情報を `requested/configured model`、外部検証済みの `executed model`、検証不能時の `UNKNOWN` に分離すること、および実行中の停止手段をfixture/mockで検証することを採用する。

## 4. 統合案 v2 の決定事項

### 4.1 原則8の限定変更

Phase 0 CLI例外は、read-only原則を全面解除しない限定変更とする。許可対象は、固定されたCLI adapterによるサブスクリプション経路の起動、ローカルRAW保存、ログ・ハッシュ・比較レポート生成に限る。任意shell、ユーザー入力やAI出力から組み立てたコマンド、Git write、API key、従量課金fallback、デプロイ、自動Merge、重要データの上書き・削除は引き続き禁止する。

失敗時はCLI adapterを停止し、L1（手動貼り付け支援）またはL0（完全手動）へ縮退する。試用期間は最初の5案件とし、各案件で安全性・課金経路・停止手段・操作負担・エラー・RAW保存をcheckpoint記録する。問題があれば5案件を待たずに停止し、原則8の変更を再評価する。

### 4.2 fan-out境界

外部Providerへ送信するデータについて、秘密情報、認証情報、個人情報、非公開コード等を含むことを安全に否定できない場合は送信しない。判定不能はfail-closedとし、人間確認まで停止する。ローカル保存は外部送信とは別の安全境界として扱う。

### 4.3 baselineの扱い

baselineを測定しない場合、改善率を厳密な絶対値として比較しない。操作回数、拘束時間、エラー回数、人間確認回数などを測定できた場合のみ、その測定範囲を明記して比較する。

### 4.4 safety preflight

preflightは静的検査と、live AI実行を伴わないmock/fixture検査に分ける。preflightという名称だけを理由に、新しいlive model実行、追加課金、外部送信を自動開始しない。課金経路、入力境界、保存先、adapter、停止フラグ、retry=0、fallback禁止を確認する。

### 4.5 停止手段

CLI自動実行前に、実行中の子プロセスを停止する手段と、新規dispatchを止める停止フラグを用意する。停止中は別Providerへの新規dispatch、自動retry、fallbackを開始しない。まずmock/fixtureで停止機能を検証し、合格までCLI自動実行へ進まない。

### 4.6 agyの位置づけ

R5-A/R5-B時点のagy capabilityは、当時の証拠がなければUNKNOWNとする。後発の実機証拠は後発証拠として別に記録し、過去RAWを遡及修正しない。

### 4.7 model情報区分

ログとpreflightでは、(1) requested/configured model、(2) AIの自己申告ではなく外部ログ・実行記録・公式UI等で検証済みの executed model、(3)検証不能時のUNKNOWNを分ける。自己申告だけでは実行modelを確定しない。

## 5. 未解決・非公開資料

指定された `R5B_PRIVATE_EVIDENCE_HANDOVER.md` と `COUNCIL_CLI_BROWSER_RESEARCH_PRIVATE_DRAFT.md` は、現在のmain、取得できた全リモートbranch履歴、作業ツリーのいずれにも存在しなかった。内容が提供されるまで、追加証拠としての開示はUNKNOWNとし、推測で作成・公開しない。

## 6. 検証記録

- 取得元: `origin/main` のclone
- 既存R5-B三社RAW: 存在確認済み、変更対象外
- 外部model実行: なし
- API key / Billing / permission変更: なし
- 自動retry: なし
- 欠落封印資料: 上記2ファイル、UNKNOWN

