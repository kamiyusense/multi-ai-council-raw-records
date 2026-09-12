# GEMINI_FEATURE_VERIFICATION_SUMMARY

このファイルは人間向けの要約であり、Multi-AI Councilで他AIへ判断材料として渡す場合は GEMINI_FEATURE_VERIFICATION_RAW.md を正とする。要約とRAWが食い違う場合はRAWおよび実機確認結果を優先する。

最終更新: 2026年9月12日
状態: 継続検証中

## 1. 通常Gemini

GitHubのblob/raw URLを一般チャットから直接取得する経路は、今回の会話では失敗した。一方、既存Notebookに登録済みのGitHub由来資料を一般Geminiチャットから参照することは成功した。

## 2. Google AI Studio

URL Contextを有効にしたAI Studioで、GitHubのRAW URLからINDEX.mdを取得し、更新日・Round 3-2の3ファイル・設問・進行表の4ファイルを回答できた。Gemini 3.1 Pro Previewでは成功画面を確認した。Gemini 2.5 FlashはURL ContextがOFFの状態で失敗し、ONにした後も今回のGitHub RAW取得では失敗を確認した。

## 3. Gemini Notebook

GitHubのblob URLをWebソースとして追加できた。INDEX.mdの内容について、GitHubの現行内容と一致する回答を得た。INDEX記載のMarkdownファイル群をソースへ追加した画面では22個のソースを確認した。

## 4. 一般GeminiとNotebookの連携

一般Geminiチャットから既存Notebookを参照できた。また、一般GeminiにJulestest.txtのGitHub blob URLを新しいNotebookソースとして追加するよう依頼し、追加後に本文の「テスト」を読み取った回答を確認した。

## 5. Gemini in Chrome（補足・実機未検証）

ユーザー環境のChrome設定にはGemini in Chromeの項目が表示されず、実機検証は未実施。候補として調査したが、現時点の結果を機能確認済みとは扱わない。

## 6. 現時点のCouncilでの利用候補

現時点の実機結果だけからは、GitHubを正本とし、Geminiは通常GeminiとGemini Notebookを組み合わせて使う運用が候補になる。AI StudioはURL Context・モデル比較・Thinking調整などの検証環境として残す。これは現時点の運用候補であり、将来の機能変更や追加検証で更新する。

## 7. 注意事項

・GeminiがNotebookのソース数を一度誤って自己申告したため、件数や追加結果はNotebookの表示と照合する。
・Notebookへ登録したGitHubソースが、GitHub更新時に自動同期されることは今回実測していない。
・「直接GitHub取得の成功」「Notebook経由のソース追加・参照」「公式資料上の対応」は別々の主張として扱う。
・無料枠、料金、提供状況などは変わり得るため、必要時は公式資料と実機で再確認する。

## 8. 参照したGoogle公式URL

・Gemini Notebook / Geminiアプリ連携: https://support.google.com/gemini/answer/16972047?hl=ja
・Gemini Notebookの基本仕様: https://support.google.com/gemininotebook/answer/16206563?hl=ja
・Gemini in Chrome: https://support.google.com/gemini/answer/16283624?hl=ja-JP
・Gemini in Chromeの利用可否・提供: https://support.google.com/gemini/answer/17140089?hl=ja
・Gemini API URL Context: https://ai.google.dev/gemini-api/docs/url-context
・Gemini API Thinking: https://ai.google.dev/gemini-api/docs/thinking
・Gemini API料金: https://ai.google.dev/gemini-api/docs/pricing?hl=ja
・Gemini APIデータ利用条件: https://ai.google.dev/gemini-api/terms?hl=ja
・Gemini APIモデル一覧: https://ai.google.dev/gemini-api/docs/models?hl=ja
・Gemini APIモデル廃止情報: https://ai.google.dev/gemini-api/docs/deprecations?hl=ja

============================================================
END
