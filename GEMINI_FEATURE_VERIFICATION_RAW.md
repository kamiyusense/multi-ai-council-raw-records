# GEMINI_FEATURE_VERIFICATION_RAW

最終更新: 2026年9月12日

このファイルは、ChatGPT会話「Gemini GitHub参照問題検証」から、Gemini関連の検証に関する実際のユーザー発言・画面確認報告・それに対する応答を、検証順に記録したRAWである。ここにない事実は補わない。要約・推測・公式仕様との解釈は別ファイルに分ける。

参照元会話: Gemini GitHub参照問題検証
対象リポジトリ: kamiyusense/multi-ai-council-raw-records

============================================================
1. Gemini in Chrome の実機確認
============================================================

ユーザー発言:
「出てる？」（Chrome設定の画面画像を添付）

応答:
「まだ出てないです。スクショ左の AI イノベーション を見ると、あるのは Chrome のスキル、Google 検索の AI モードと連携されたアプリ、オンデバイス AI で、Gemini in Chrome という項目は見当たりません。」

この会話では、ユーザー環境ではまだ利用できず実機未検証として扱った。

============================================================
2. Google AI Studio: GitHub RAW URL
============================================================

ユーザーがAI Studioへ入力した質問:
「このURLを直接取得して、書かれている内容を確認してください。
https://github.com/kamiyusense/multi-ai-council-raw-records/raw/refs/heads/main/INDEX.md
答えるときは、次の3つを書いてください。
1. 最終更新の日付
2. Round 3-2 のセクションに並んでいるファイル名（3つ）
3. 設問・進行表 のセクションに並んでいるファイル名（4つ）
URLから内容を取得できなかった場合は、取得できなかったと書いてください。
推測で埋めないでください。」

画面確認として記録された結果:
「スクショ左のAI Studioを見る限り、URL Context経由でちゃんと回答が返っています。」
「回答下部に raw.githubusercontent.com がソースとして表示されています。」
回答内にはINDEX.mdのセクション名とファイル名が表示されていた。

この時点の会話内の整理:
「Gemini通常チャット + GitHub URL → 失敗」
「Gemini通常チャット + RAW URL → 失敗」
「Gemini Import code → 圧縮データ展開不具合」
「Google AI Studio + URL Context + RAW URL → 成功」

============================================================
3. AI Studioでモデルを変えた比較
============================================================

ユーザー発言:
「モデル選択の候補　注目の　から　全て　にしたら出てきたわこれだね」
「2.5もうなくね？　ちょっと調べてきて」
「これさ、AIStudio上で使えるモデルに完全無料のものはないの？」

Gemini 2.5 Flash の最初の画面確認:
「URLから内容を取得できませんでした。」
「今回は 2.5 Flash + URL Context ONでもGitHub RAW取得に失敗」
「右側の設定を見ると今回はちゃんと Thinking mode ON / URL context ON」

その前段の画面確認:
「Enable URL Context」
「You provided URL(s), but the URL Context tool is required to access their content. Please enable the URL Context tool and try your request again.」
「右の設定を見ると、URL context のトグルがOFFになってる。」
この時点はURL Context未有効による失敗であり、2.5 Flashのモデル能力の判定前と記録された。

============================================================
4. Gemini Notebook: GitHub blob URL と INDEX.md
============================================================

ユーザーがNotebookのソース追加で入力したURL:
https://github.com/kamiyusense/multi-ai-council-raw-records/blob/main/INDEX.md

画面確認中の応答:
「追加自体はできてます。左の ソース にGitHubのURLが1件出ています。ただし右端に青いクルクルが出ているので、今はまだ取り込み／解析中っぽいです。」

その後、ユーザーがNotebookに質問した結果として記録した回答:
「最終更新の日付: 2026-09-12」
「Round 3-2: CHATGPT_R3-2_RAW.md / CLAUDE_R3-2_RAW.md / GEMINI_R3-2_RAW.md」
「設問・進行表: ROUND3_QUESTIONS_RAW.md / ROUND3-2_QUESTIONS_RAW.md / COUNCIL_PRINCIPLES_RAW.md / ROUND4-5_PLAN_RAW.md」

この回答をGitHubのINDEX.md原文と照合した応答:
「Notebookの回答と全部一致しています。」

============================================================
5. NotebookへのINDEX記載ファイル追加
============================================================

ユーザーがGeminiへ入力した依頼:
「INDEX.md に載っている全ファイルを、GitHub から取得してソースに追加してください。
リポジトリは kamiyusense/multi-ai-council-raw-records です。
Claudetest.txt と Julestest.txt は不要です。」

画面確認後の応答:
「左側の ソース 欄を見ると、CHATGPT_R1_RAW.md、CLAUDE_R1_RAW.md、GEMINI_R1_RAW.mdみたいな各社RAWがズラッと並んでいて、下部にも 22個のソース と出ています。」

Geminiの自己申告:
「現在、このNotebookには INDEX.md や各AIの回答記録、進行表といった20ファイルが登録されています。」

その後の照合:
「INDEX.md：1」
「GitHubから追加したMarkdown：20」
「Geminiチャット：1」
「合計：22ソース」

応答:
「Geminiの説明は、INDEX 1 ＋ 会話履歴 1 ＋ Markdown 19 ＝21なので、『19個』の部分が単純に1個足りないです。」

============================================================
6. 一般Geminiチャットから既存Notebookを参照
============================================================

ユーザーが一般GeminiチャットからNotebookを参照した際の回答:
「現在、Notebookには INDEX.md や各AIの回答記録（CLAUDE_R1_RAW.md や GEMINI_R2_RAW.md など）、進行表といった20ファイルが登録されています。」

応答:
「一般のGeminiチャット → 既存Notebookを参照 → Notebookに登録済みのGitHub由来ファイルを読む、これは成功です。」

============================================================
7. 一般Geminiチャットから Julestest.txt を追加
============================================================

一般Geminiチャットへ送った依頼:
「Julestest.txt を私が手動で追加するのではなく、あなた自身で Multi-AI Council Raw Records Index Notebookの新しいソースとして追加してください。
対象URL:
https://github.com/kamiyusense/multi-ai-council-raw-records/blob/main/Julestest.txt
追加後、その内容を読んで何と書かれているか答えてください。
Claudetest.txt や既存ソースには変更を加えないでください。」

ユーザーが確認したGeminiの回答:
「ご指示通り、既存のソース（Claudetest.txt など）には一切変更を加えず、Multi-AI Council Raw Records Index に新しいソースとして Julestest.txt を追加しました。
追加したファイルの内容を読み取ったところ、ファイルには以下の一言のみが書かれていました。
『テスト』」

この結果に対する応答:
「一般Geminiチャットからの迂回ルートが成立したと見ていいです。」
「一般Geminiチャット → Notebook操作 → GitHub URLをNotebookへ登録 → 内容参照 の経路が成立した。」

============================================================
8. 会話内で確認された注意事項
============================================================

・GeminiがNotebookのソース数を一度誤って自己申告した。実表示との照合が必要。
・GitHubをNotebookへ登録したソースが、GitHub更新時に自動同期されることは、この会話内では実測していない。
・Gemini in Chromeはユーザー環境に項目がなく、実機未検証。
・直接取得の成功、Notebook経由の取得、AI Studioのモデル仕様上の対応は、同じ主張として扱わない。

============================================================
END
