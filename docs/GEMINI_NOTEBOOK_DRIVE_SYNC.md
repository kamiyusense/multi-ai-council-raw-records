# Google Drive 経由の Gemini Notebook 同期

GitHubのINDEX記載RAWが正本です。Driveの`GEMINI_NOTEBOOK_BUNDLE.md`は派生コピーで、GitHub ActionsがBundleを生成・検証した後にApps Script Web AppへPOSTして同じDriveファイルを上書きします。Gemini NotebookにはこのDriveファイルを一度だけソース登録します。

## 初回のGoogle側設定

1. Google Driveで空のテキストファイルを1つ作り、`GEMINI_NOTEBOOK_BUNDLE.md`と命名する。ファイルIDを控える。
2. Apps Scriptでスタンドアロンプロジェクトを作成し、`apps-script/GeminiNotebookDriveSync.gs`を貼り付けて保存する。
3. スクリプトプロパティに`DRIVE_FILE_ID`（手順1のID）と`SYNC_TOKEN`（32文字以上のランダムな秘密値）を追加する。
4. **デプロイ → 新しいデプロイ → ウェブアプリ**。実行ユーザーは自分、アクセスはGitHub Actionsから到達できる選択肢（通常は「全員」）でデプロイする。Drive書込みを承認し、`/exec` URLを控える。
5. Gemini Notebookに手順1のDriveファイルを一度だけ追加する。

個人アカウントで「全員」が選べない場合、この最小構成は使えません。認可回避や個人OAuthトークンのGitHub保存は行わず、匿名POSTを受けられる別の中継を検討してください。

## GitHub Secrets

**Settings → Secrets and variables → Actions** に登録します。

- `GEMINI_DRIVE_SYNC_URL`: Apps Scriptの`/exec` URL
- `GEMINI_DRIVE_SYNC_TOKEN`: Apps Scriptの`SYNC_TOKEN`と同じ値

両方が設定されるまで同期ステップは安全にスキップされ、秘密値はリポジトリへコミットされません。

## 検証

1. PRをmainへマージする。
2. Secrets設定後、mainで**Generate Gemini Notebook Bundle**を手動実行する。
3. ログで生成・`--verify`・`Sync bundle to Google Drive`が成功したことを確認する。
4. Driveファイルに更新済みSource commit SHAがあることを確認する。
5. Notebookのソースを再追加せず、新規RAWへ入れた固有文字列を質問する。正答できればDriveソースは自動追従している。

## セキュリティ

- URLだけでは書込みできないよう、長いランダムな`SYNC_TOKEN`を必須にする。
- tokenはHTTPSで送信される。Actionsログ、issue、PR本文へ出力しない。
- Apps Scriptは固定のDriveファイルIDだけを操作する。
- GitHubの書込み権限は既存の生成済みBundleコミット用の`contents: write`のみを維持する。
