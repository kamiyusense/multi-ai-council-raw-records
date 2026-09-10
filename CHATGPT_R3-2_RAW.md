## Round 3-2：3社R3回答のソース突き合わせ結果

指定された4つのRAWは**すべて全文取得できました**。読めなかったファイルはありません。

- `ROUND3-2_QUESTIONS_RAW.md`：4分類、UNKNOWNの扱い、実測検討など今回の要件を確認しました。
- `CHATGPT_R3_RAW.md`：全文取得済み。
- `GEMINI_R3_RAW.md`：全文取得済み。
- `CLAUDE_R3_RAW.md`：全文取得済み。

今回はR3の原文と現在の公式一次資料だけで主要争点を確認できたため、R1/R2を正本の代わりには使用していません。

**公式資料の確認日：2026年9月11日（JST）**

3社なので、一つの項目の中でも「ChatGPT↔Claudeは(1)、Gemini↔2社は(4)」のような混在が起こります。無理に1項目1分類には押し込みません。

---

# 1. 項目ごとの結論・ソース突き合わせ

| 項目 | R3での3社の結論 | 分類 | Round 3-2判定 |
|---|---|---|---|
| **a 月額契約だけで司令塔** | ChatGPT＝限定YES、Claude＝条件付き可能、Gemini＝UNKNOWN | C↔Cl **(2)**、G↔他 **(4)** | **限定YESを維持**。Codex・Claude Agent SDK・Julesという公式automation surfaceを自分用に操作する経路は存在。ただし通常APIを月額契約だけで自由に叩けるという意味ではない。 |
| **b API 1回費用** | ChatGPT約34.5円、Gemini約4.25円（一覧では1.5～3円）、Claude約11～200円 | **(4)** | 前提token数・モデルが違うので数値比較自体が不適切。ChatGPTの10k入力+2k出力という条件は現行価格でも計算一致。 |
| **c 自動追加課金OFF** | ChatGPT＝月額枠は概ね可、API厳密0円保証なし。Gemini＝3社完全停止可能。Claude＝Anthropicのみ確認 | C↔Cl Anthropic部分は概ね **(1)/(2)**、G↔他 **(4)** | **Geminiの「3社とも完全停止」は強すぎる。** OpenAIもGoogleも処理遅延・実行中処理等で設定額超過の可能性を公式記載。 |
| **d コスト削減** | 3社とも小型モデル、cache、Batch等を認める | **(2)** | **結論一致。確定してよい。** |
| **e 月額自動化＝規約違反か** | ChatGPT/Claude＝「3社全部違反」は誤り。Gemini＝全体UNKNOWNだがブラウザUI自動化は3社違反と断定 | C↔Cl **(2)**、G↔他 **(4)** | **公式CLI/SDK/APIまで一括で規約違反扱いするのは誤り。** 非公式UI操作とは分離必須。 |
| **f-1 枠構造** | ChatGPT＝各社で異なる。Claude＝Claude 5h+weekly。Gemini＝Googleは回数非公開/動的 | Claude部分C↔Cl **(2)**、Google部分C↔G **(4)** | GeminiのGoogle情報が古い。現在Gemini Appsは**5時間+週間のcompute-based枠**を公式公開。Julesは別に100 tasks/rolling 24h。 |
| **f-2 枠共有** | ChatGPT＝OpenAI Work+Codex、Claude各surface共有、Googleはproduct別。Claude＝Claude共有。Gemini＝Gemini App+Workspace共有 | Claude部分 **(2)**、Google部分 **(4)** | **GeminiのGoogle一般化は誤り。** Googleは「各productに独自AI usage limit」と明記。Workspace公式もGemini AppsとWorkspace内Geminiは別上限。 |
| **f-3 月額内機能** | ChatGPT＝agent系は含むが通常API別。Claude＝Claude/Code/Cowork等、API別。Gemini＝AI Studio/API/Vertexは全部月額外 | C↔Cl **(2)**、Google部分は **(4)** | 「Gemini Developer API Paid Tierが別課金」は正しいが、**Google AI StudioそのものまでGoogle AI Pro外とするのは現行資料と不整合**。 |
| **f-4 使用量確認** | ChatGPT/Claude＝画面確認可、programmatic remaining quota APIはUNKNOWN。Gemini＝画面でも確認機能なし | C↔Cl **(2)**、G↔他 **(4)** | Geminiは誤り。現在Gemini Appsに **Settings → Usage Limits** がある。ただし**司令塔から取得する公式APIは3社とも依然UNKNOWN**。 |
| **f-5 誤従量課金** | ChatGPT/Claude＝認証方式により事故はあり得る。Gemini＝Googleでは構造上起こらない | C↔Cl **(2)**、G↔他 **(4)** | 「絶対起こらない」は強すぎる。ただしJules API keyとGemini Developer API keyを同一課金経路とみなすのも誤り。 |
| **f-6-a 上限到達** | 3社概ね「追加課金を有効にしなければ停止/待機」 | **(2)** | **概ね一致**。ただしGoogle Gemini AppsではFlash-Liteへ継続可能。 |
| **f-6-b 実行途中の境界挙動** | ChatGPT＝UNKNOWN。Claude＝途中停止・手動再開等を記述。Gemini＝利用制限エラー | **(4)** | Claude自身がその細部について一次資料を見つけていないと明記しているため、**厳密なagent transaction semanticsはUNKNOWNへ戻すべき**。 |
| **f-6-c 超過分持越し** | ChatGPT＝UNKNOWN、Claude＝ユーザー実測でAnthropicのみ解決、Gemini＝概念なし | **(4)** | **Claude Proについてのみ実測で解決。** OpenAI/Google月額枠へ一般化不可。 |
| **f-6-d 未使用分繰越** | ChatGPT＝bank制度を確認できず、Claude＝UNKNOWN、Gemini＝概念なし | **(4)** | 週間枠は新cycleでfull allowance/refreshする資料があるが、全surface・全windowについて厳密な繰越仕様を一般化しない。 |
| **f-6-e モデルと枠** | ChatGPT/Claude＝modelにより消費差あり。Gemini＝下位モデル手動切替なし | C↔Cl **(2)**、G↔他 **(4)** | Gemini部分は現在明確に誤り。Gemini公式はモデル選択・thinkingで消費差があり、上限後Flash-Liteへ継続可能。 |
| **f-7 他社枠換算** | 3社ともUNKNOWN | **(2)** | **UNKNOWN維持。** 公式換算係数なし。 |
| **① Jules DELETE** | ChatGPT/Claude＝endpoint有、hard cancel不明。Gemini＝公開REST API自体なし | C↔Cl **(1)**、G↔他 **(4)** | **DELETE存在は確定。hard-stopはUNKNOWN。** |
| **② Codex外部操作** | ChatGPT/Claude＝可能。Gemini＝Codexは2023年廃止 | C↔Cl **(2)**、G↔他 **(4)** | **Geminiは旧Codex modelと現在のCodex製品を混同。現在も公式SDK/App Server等が存在。** |
| **③ Codex監視・中断** | ChatGPT＝hooks等YES、SDK hard interrupt UNKNOWN。Claude＝hooks/App Server YES。Gemini＝途中approval hookなし | C↔Cl **(2)**、G↔他 **(4)** | **現在はさらに進んで、App Serverに `turn/interrupt` が公式記載。広義の外部中断＝YES。** |
| **④ Claude Agent SDK課金** | ChatGPT＝subscription枠。Claude＝同結論だが二次情報。Gemini＝UNKNOWN | C↔Cl **(2)**、G↔他 **(4)** | 現行Anthropic公式で直接確認できた。**subscription usageを消費する。UNKNOWN撤回可能。** |
| **⑤ Gemini無料APIデータ利用** | ChatGPT/Gemini＝改善利用・human reviewあり。Claude＝UNKNOWN | C↔G **(1)**、Cl↔他 **(4)** | **YESで確定。ClaudeのUNKNOWNは撤回可能。** |

Gemini R3の主要なGoogle主張は、f-1～f-6でこのように記載されています。 Claudeのf-6-c実測追記もRAWに明記されています。

なお、今回**純粋な(3)「同じ公式ページを読んで結論だけが逆」**に確定できる主要争点は見つかりませんでした。目立つ対立は、ほぼ「古い/異なる資料または資料未確認」による(4)です。

---

# 2. 公式資料で確定した重要な食い違い

## Gemini R3：①「Julesの一般公開APIリファレンスは存在しない」

これは**事実誤認**です。

Gemini R3は「一般公開されたAPIリファレンスが存在しない」として①をUNKNOWNにしています。

Google公式の **Quickstart | Jules** は、Jules REST APIがprogrammatic access、自動化、custom workflow、CI/CD等のためのAPIだと明記し、Jules SettingsからAPI keyを生成する手順まで公開しています。

[Quickstart | Jules](https://jules.google/docs/api/reference/?utm_source=chatgpt.com)

さらに **Sessions | Jules** には、

`DELETE /v1alpha/sessions/{sessionId}`

があり、説明は **“Deletes a session.”**、成功時empty responseです。

[Sessions | Jules](https://jules.google/docs/api/reference/sessions/?utm_source=chatgpt.com)

したがって、

**「DELETE endpointが存在する」＝確定**  
**「実行中agentを即座にhard-stopしquota消費も止める」＝UNKNOWN**

です。

ここはChatGPT R3とClaude R3の読み方が正しかったです。Claudeも同じSessions URLを使用しています。

---

## Gemini R3：②「Codexモデルは2023年廃止なので外部操作できない」

これも**現在の製品についての事実誤認**です。

Geminiは旧OpenAI Codexモデルの終了を、現在の「Codex」という開発agent製品に適用してしまっています。

現行OpenAI公式 **Codex SDK | ChatGPT Learn** はページ冒頭で、

> Programmatically control local Codex agents

と明記し、CI/CD、自作agent、内部workflow、アプリ統合を用途として列挙しています。

[Codex SDK | ChatGPT Learn](https://developers.openai.com/codex/sdk?utm_source=chatgpt.com)

したがって②は**YES**です。

---

## Gemini R3：③「Codexに途中承認・interrupt機構がない」

現在の公式仕様とは一致しません。

OpenAI公式 **Codex App Server | ChatGPT Learn** に、

`turn/interrupt`

が明記されており、成功するとturnのstatusが `interrupted` になります。

[Codex App Server | ChatGPT Learn](https://developers.openai.com/codex/app-server?utm_source=chatgpt.com)

またCodex SDKページ自身も、App Serverを「authentication、conversation history、approvals、streamed agent events」を扱うcustom client用と説明しています。

### ChatGPT自身のR3もここは更新します

R3では、

> SDK hard interrupt = UNKNOWN

としました。

これは**「SDKそのものに同等のcancel methodがあるか」**という狭い意味ではまだUNKNOWNで構いません。

しかしCouncilの広い設問である

**「外部司令塔からCodexを監視・中断できるか」**

については、App Serverの `turn/interrupt` が確認できたので、

**部分確認 → YESに引き上げます。**

---

## Gemini R3：f-1 使用枠

Geminiが証拠に挙げたURL自体が別内容です。

Gemini R3は

`support.google.com/gemini/answer/14579631`

を「Gemini Advanced FAQ」として、回数制限非公開の根拠にしています。

しかし現在そのURLのページタイトルは、

**「Gemini モバイルアプリを使ってできること」**

であり、利用枠の記事ではありません。

[Gemini モバイルアプリを使ってできること](https://support.google.com/gemini/answer/14579631?hl=ja&utm_source=chatgpt.com)

正しい現行資料 **Gemini Apps limits & upgrades for Google AI subscribers** は、

- compute-based usage
- prompt complexity/model/features/chat lengthで消費量が変化
- **5時間ごとにrefresh**
- **weekly limitあり**

と明記しています。

[Gemini Apps limits & upgrades for Google AI subscribers](https://support.google.com/gemini/answer/16275805?utm_source=chatgpt.com)

したがってf-1のGemini R3情報は更新が必要です。

---

## Gemini R3：f-2「GeminiアプリとWorkspaceが同じ枠」

これも現行公式資料と一致しません。

Google One公式 **Use Google AI Pro benefits** は冒頭で、

**Each product has its own AI usage limits.**

と明記しています。

[Use Google AI Pro benefits | Google One Help](https://support.google.com/googleone/answer/14534406?utm_source=chatgpt.com)

さらにWorkspaceアカウント向けGemini公式Helpには、

**Gemini AppsとWorkspace apps内Geminiにはseparate limitsがある**

と明記されています。

[Use Gemini Apps with a work or school Google Account](https://support.google.com/gemini/answer/14620100?utm_source=chatgpt.com)

したがって、

**「Google系AI機能は全部同一プール」ではありません。**

これはChatGPT R3側の「Googleはサービス別枠」が妥当でした。

---

## Gemini R3：f-4「使用量を画面から確認する公式機能なし」

**現在は明確に誤りです。**

Gemini公式は、

**Settings → Usage Limits**

からusage limitを確認できる手順を明記しています。また上限接近時・到達時には通知とrefresh時刻も表示します。

したがって、

- **人間が画面で確認** → YES
- **司令塔がAPIで残り%を取得** → UNKNOWN

です。

ここはChatGPTとClaudeの切り分けが正しかったです。

---

## Gemini R3：f-6-e「下位モデルへ切り替える機能なし」

これも現在は**誤り**です。

Gemini公式は、

- Flash-Lite / Flash / Pro等を用意
- higher model / higher thinking levelほどusageを多く消費
- 上限到達後も**Flash-Liteでconversationを継続可能**

としています。

したがってモデルroutingはGoogleでも利用枠節約の設計要素になります。

---

# 3. 「3社ともAPI上限を設定すれば絶対追加課金なし」は成立しない

これは特に重要です。

Gemini R3は「3社とも完全停止可能」としました。

しかし現在の一次資料では、**「limitを設定できる」ことと「1円も超過しない」ことは別**です。

Google Gemini APIはbilling data処理に最大約10分の遅延があり、project capを超えたoverageが発生し得ると公式記載されています。Prepayでもcut-off遅延によって**negative balance**になり、その分は次のcredit購入から差し引かれます。

[Billing | Gemini API | Google AI for Developers](https://ai.google.dev/gemini-api/docs/billing?utm_source=chatgpt.com)

通常のGoogle Cloud「budget alert」はそもそも支出を止めません。

[Create, edit, or delete budgets and budget alerts | Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/budgets?utm_source=chatgpt.com)

2026年のSpend Cap機能でも、

- enforcementはinstantではない
- **in-flight requestは完了まで処理**
- reporting latencyによるoverageは普通に請求

と明記されています。

[Manage spend cap budgets | Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps?utm_source=chatgpt.com)

OpenAI APIのhard spend limitsも、enforcementはinstantではなく**configured amountをわずかに超える可能性**を公式Helpが明記しています。

[Troubleshooting API usage and spend limits | OpenAI Help Center](https://help.openai.com/en/articles/6614457?utm_source=chatgpt.com)

したがってcの正しい表現は、

**「追加購入・auto-reloadをOFFにして、かなり強く出費を抑えることはできる。しかしAPI課金で厳密に¥0オーバーを3社共通で保証する、とは言えない」**

です。

---

# 4. a：月額プランだけでMulti-AI Councilを動かせるか

ここは今回さらに確度が上がりました。

### OpenAI

Codexはプログラム制御可能で、認証は明確に二系統です。

- ChatGPT sign-in → **subscription access**
- API key → **usage-based access** 


[Authentication | ChatGPT Learn](https://developers.openai.com/codex/auth?utm_source=chatgpt.com)

### Anthropic

Anthropic公式は2026年6月15日に予定していたAgent SDK課金変更を**pause**し、

> Agent SDK / `claude -p` / third-party app usage は引き続きsubscription usage limitsを消費

と現在も明記しています。

[Use the Claude Agent SDK with your Claude plan | Claude Help Center](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan?utm_source=chatgpt.com)

したがってClaude R3が「二次情報なのでまだ再確認」とした部分は、**現在は一次資料で直接解決できます**。

### Google

Jules公式は、paid Jules plansについて、

**paid plans are accessed through a Google One subscription**

とし、Jules in ProはGoogle AI Proのbenefit、100 daily tasks / rolling 24h・15 concurrentとしています。

[Limits and Plans | Jules](https://jules.google/docs/usage-limits?utm_source=chatgpt.com)

Jules REST API自体も公式のprogrammatic interfaceです。

したがってR3-2時点のaは、

**「3社の通常のmodel APIを月額契約だけで直接叩く」→ NO**

ではなく、

**「Codex / Claude Agent SDK / Julesという各社公式automation surfaceを、自分用の司令塔から利用する」→ 限定的YES**

とするのが最も根拠に忠実です。

ただし**第三者向けサービスとして他人のrequestを個人subscription経由で流すことまで許されるか**は別問題で、ここは引き続きUNKNOWNです。

---

# 5. b：料金についての再照合

Gemini R3は、現行モデルを公式サイトで確認したのではなく、

- GPT-4o
- Claude 3.5 Sonnet
- Gemini 1.5 Pro

を「私の知識ベース上の最新情報」として使用しています。さらに一覧は「約1.5～3円」としながら、本文計算では**4.25円**です。

これは今回の「2026年9月の公式情報で確認」という条件を満たしません。

一方ChatGPT R3の比較条件は、

**入力10,000 tokens + 出力2,000 tokens**

でした。

現行一次資料では、

- GPT-5.6 Sol = **$4 / $20 per MTok** 
- Claude Opus 5 = **$5 / $25 per MTok** 
- Gemini 3.1 Pro Preview（≤200k）= **$2 / $12 per MTok** 

です。

したがって同じ仮定なら、

| モデル | 10k input | 2k output | 合計 |
|---|---:|---:|---:|
| GPT-5.6 Sol | $0.040 | $0.040 | **$0.080** |
| Claude Opus 5 | $0.050 | $0.050 | **$0.100** |
| Gemini 3.1 Pro Preview | $0.020 | $0.024 | **$0.044** |
| **3社** | | | **$0.224** |

ChatGPT R3で置いた「1ドル=154円」という**比較用仮定**なら、

**$0.224 × ¥154 = ¥34.496 ≒ ¥34.5**

です。

つまりChatGPT R3の約35円は、**同じtoken条件については現行公式価格でも検算成立**します。

Claude R3の約200円とは入力3万+出力8千という別条件なので、矛盾ではありません。ただしClaude R3にあった「GPT-5.6 Sol $5/$30」は現行公式価格では誤りです。Claude自身が「全て二次情報」と注意書きしていた点は適切でした。

またClaude R3でUNKNOWNだったSonnet 5価格も現在は解決しています。

Anthropic公式は**$2/$10を恒久価格とし、予定されていた$3/$15への9月1日値上げは行わない**と明記しています。

[Pricing | Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/pricing?utm_source=chatgpt.com)

---

# 6. ChatGPT自身がUNKNOWNにした項目の再判定

| ChatGPT R3のUNKNOWN | 他社で解決できたか | R3-2判定 |
|---|---|---|
| **f-4 月額included quotaを司令塔が正式API取得** | いいえ | **UNKNOWN維持**。Claudeもprogrammatic取得を発見できず、Geminiの「ない」はそもそもUIの存在を見落としている。不存在証明にはならない。 |
| **f-6-b quota境界を長時間agentが跨ぐ瞬間の処理** | いいえ | **UNKNOWN維持**。Claudeは詳細を書いたが、本人が「公式記載を発見できなかった」と認めている。 |
| **f-6-c 超過分持越し** | Anthropicだけユーザー実測あり | **Claude ProだけUNKNOWN撤回**。OpenAI/Google monthly quotaには一般化しない。 |
| **f-7 OpenAIの83%をClaude/Googleへ換算** | いいえ | **UNKNOWN維持**。 |
| **Jules DELETEがhard cancelか** | いいえ | **UNKNOWN維持**。Claudeも同じ結論。 |
| **個人subscriptionを第三者向けサービスに中継可能か** | いいえ | **UNKNOWN維持**。ClaudeのR3も一次資料を直接確認できていない。 |
| **Codexの外部interrupt** | はい。ただしSDK限定ではなくApp Server | **広義のUNKNOWN撤回 → YES**。`turn/interrupt`確認済み。 |
| **Gemini無料APIのデータ利用** | Gemini回答＋Google公式で再確認 | これは元々ChatGPTはYESだったため維持。Claude側のUNKNOWNを撤回可能。 |

---

# 7. 3社でなお残るUNKNOWNと実験方法

厳密には「3社全員が同じ文言でUNKNOWN」としていないものもありますが、一次資料で決着していないものを残します。

| UNKNOWN | 実験可能か | 方法 | コスト | 設計優先度 |
|---|---|---|---|---|
| **月額枠の残量をprogrammaticに取得可能か** | 一部 | 公開API/公式CLIのdocumented outputだけを調査。非公開endpointのreverse engineeringやUI scrapingはしない。各社Support問い合わせも有効。 | 各社30～60分程度、prompt数回。金銭ほぼ不要 | **高**。quota-aware routingには重要。ただしローカル推定値で代替可能。 |
| **長時間agentが5h/weekly境界を跨いだときどのstepで止まるか** | YES | 枠が残り少ない状態で再現可能な長時間taskを開始し、event/log・状態・reset後のresumeを記録する。 | 1社1～2時間程度＋残り枠をかなり消費 | **中～高**。ただし最初から「途中失敗可能」と仮定したretry設計にすれば先に開発可能。 |
| **Jules DELETEのhard-stop性** | YES | 捨てrepo/branchで長時間session開始→DELETE→activities/state/commit/PR/task countを継続観測。 | **1～3 Jules tasks、10～30分程度** | **中**。比較的安く確認できるので実験価値が高い。 |
| **個人subscription認証を第三者向けサービスに使える法的範囲** | 技術実験ではNO | Termsだけで決着しなければ各社Support/契約窓口への問い合わせが必要。 | 金銭ほぼ0、回答待ち時間あり | **自分だけで使う現段階では低**。公開製品化時は高。 |
| **OpenAI/Claude/Googleの枠を相互換算する係数** | YES、ただし経験値のみ | 同一repo・同一prompt corpus・同一種類のtaskを10～20件ずつ流し、開始/終了usageを記録。 | 各社10～20 task、週間枠を相応に消費 | **中**。router最適化には有用だがMVPの必須条件ではない。 |

特に**Jules DELETE実験は安価で、Round 4以降の設計判断をかなり明確にできる**と思います。

---

# 8. ユーザーのClaude Pro実測データ

R3-2 RAWにある実測は、

1. セッション枠を使い切った後、reset後は**0% used**から開始し、超過分は持ち越されなかった
2. Round 3回答1回で週間枠が**21% → 23%**

です。

Claude RAWにも同じ観測結果が追記されています。

### f-6-cについて

これは**Anthropic Claude Proに関する直接観測として十分採用できます。**

しかもAnthropic公式は、

- 5h limit到達でblocking error
- usage creditsを無効化すればincluded usageのみ
- included usageは5hごとにreset

と説明しており、観測結果と矛盾しません。

したがってAnthropicについては、

**「今回観測したsessionでは、使い切った超過分が次windowへ借金として持ち越されなかった」**

をR3-2の実測事実として採用します。

ただし、これは**「未使用分が繰り越されるか」f-6-dの実験にはなっていません**。100%まで使い切ったためです。Claude RAW自身もそこを正しく分離しています。

---

## 21% → 23% の「約2%」について

これも**観測事実として有効**です。

しかし、

> 「Round 3級回答ならClaude Proで週50回答できる」

とは推定しません。

Anthropic公式はusageが、

- conversation length / complexity
- model
- features
- effort

で変化すると明記しています。

[How do usage and length limits work? | Claude Help Center](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work?utm_source=chatgpt.com)

したがって**2 percentage points consumed**は非常に価値のあるベンチマーク1点ですが、固定換算率ではありません。

f-7のUNKNOWNを完全解消するには、今後同じ種類のCouncil回答を数回測って中央値を見る必要があります。

---

# 9. OpenAIでもClaudeと同じ「超過持越しなし」になるか

ここは**完全なYESとは言いません。**

OpenAIのincluded Work/Codex allowanceは、

- 5時間window
- weekly window
- limit後はreset待ち、または追加credits

という構造です。

[Managing usage with GPT-6 Astra in Work and Codex | OpenAI Help Center](https://help.openai.com/en/articles/20001516?utm_source=chatgpt.com)

なので**追加creditsを使わない通常included枠だけなら、Claudeの実測と似た挙動になる可能性は高い**です。

しかし私はここを公式資料だけから、

**「境界を跨いだ超過計算が絶対に次windowへ持ち越されない」**

とは確定しません。

さらに現在のOpenAI Usage Creditsは別です。公式Helpは、task開始時にcredit balanceが正でも並行処理などでtask終了時に残高を使い切った場合、**credit balanceがnegativeになり、その後のcredit購入から差し引かれる場合がある**と明記しています。

[Using Credits for Flexible Usage in ChatGPT (Personal plans) | OpenAI Help Center](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro-sora?utm_source=chatgpt.com)

つまり、

**Claude Proの「included session枠で超過持越しなし」という実測を、OpenAIの購入Creditsにまで一般化するのは明確に不可**

です。

Google Gemini API Prepayもnegative balanceを次回credit purchaseから差し引く仕様なので、同様に一般化できません。

---

# 10. ⑤ Gemini無料APIのデータ利用

ここは3社間でかなり綺麗に決着します。

Google公式 **Gemini API Additional Terms of Service** はUnpaid Servicesについて、

- submitted content / generated responsesをGoogle products/services/ML technologiesの提供・改善・開発に利用
- **human reviewers may read, annotate, and process API input and output**
- sensitive/confidential/personal informationを送らないよう注意

と明記しています。

[Gemini API Additional Terms of Service | Google AI for Developers](https://ai.google.dev/gemini-api/terms?utm_source=chatgpt.com)

したがってChatGPT/Geminiの結論、

**「Gemini API無料枠へprivate source codeを送ると、改善利用・human reviewの対象となり得る」**

は確定してよいです。

Claudeの⑤ UNKNOWNは撤回できます。

なお「必ずモデル学習される」とまでは言い換えません。公式文言に忠実に**製品・サービス・ML技術の改善/開発、人手レビュー**と表現します。

---

# 11. 今回確認した主要公式一次資料

すべて**確認日 2026年9月11日（JST）**です。

| 会社 | ページタイトル / URL | 今回確認した内容 | 確認日 |
|---|---|---|---|
| OpenAI | [Codex SDK | ChatGPT Learn](https://developers.openai.com/codex/sdk?utm_source=chatgpt.com) | Codexのprogrammatic control、CI/CD・自作agent・内部workflow用途  | 2026-09-11 |
| OpenAI | [Authentication | ChatGPT Learn](https://developers.openai.com/codex/auth?utm_source=chatgpt.com) | ChatGPT＝subscription access、API key＝usage-based access  | 2026-09-11 |
| OpenAI | [Managing usage with GPT-6 Astra in Work and Codex](https://help.openai.com/en/articles/20001516?utm_source=chatgpt.com) | Work+Codex共有枠、5h+weekly、Settings Usage  | 2026-09-11 |
| OpenAI | [Codex App Server | ChatGPT Learn](https://developers.openai.com/codex/app-server?utm_source=chatgpt.com) | `turn/interrupt`、成功時interrupted  | 2026-09-11 |
| OpenAI | [GPT-5.6 Sol Model | OpenAI API](https://developers.openai.com/api/docs/models/gpt-5.6-sol?utm_source=chatgpt.com) | $4 input/$20 output per MTok  | 2026-09-11 |
| OpenAI | [Terms of Use | OpenAI](https://openai.com/policies/terms-of-use/?utm_source=chatgpt.com) | consumer serviceからdata/outputを自動・programmaticに抽出することの禁止  | 2026-09-11 |
| OpenAI | [Using Credits for Flexible Usage in ChatGPT](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro-sora?utm_source=chatgpt.com) | included後のCredits、auto reload、negative balance可能性  | 2026-09-11 |
| Anthropic | [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan?utm_source=chatgpt.com) | 6/15変更pause、Agent SDK等はsubscription usage継続  | 2026-09-11 |
| Anthropic | [What is the Pro plan?](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan?utm_source=chatgpt.com) | 5h session + weekly、full weekly allowance  | 2026-09-11 |
| Anthropic | [Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan?utm_source=chatgpt.com) | `ANTHROPIC_API_KEY`設定時はAPI料金へ切替  | 2026-09-11 |
| Anthropic | [Manage usage credits for paid Claude plans](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans?utm_source=chatgpt.com) | Creditsをdisableするとincluded usageのみ  | 2026-09-11 |
| Anthropic | [Pricing | Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/pricing?utm_source=chatgpt.com) | Opus 5 $5/$25、Sonnet 5 $2/$10確定  | 2026-09-11 |
| Google | [Quickstart | Jules](https://jules.google/docs/api/reference/?utm_source=chatgpt.com) | Jules REST API、programmatic automation、API key  | 2026-09-11 |
| Google | [Sessions | Jules](https://jules.google/docs/api/reference/sessions/?utm_source=chatgpt.com) | DELETE endpoint、説明はDeletes a sessionのみ  | 2026-09-11 |
| Google | [Limits and Plans | Jules](https://jules.google/docs/usage-limits?utm_source=chatgpt.com) | Pro=100 tasks/rolling 24h、15 concurrent、Google AI Pro benefit  | 2026-09-11 |
| Google | [Use Google AI Pro benefits](https://support.google.com/googleone/answer/14534406?utm_source=chatgpt.com) | 各product独自usage limit、AI Studio等を含む  | 2026-09-11 |
| Google | [Gemini Apps limits & upgrades](https://support.google.com/gemini/answer/16275805?utm_source=chatgpt.com) | compute-based、5h+weekly、Usage Limits画面、Flash-Lite継続  | 2026-09-11 |
| Google | [Gemini API Additional Terms of Service](https://ai.google.dev/gemini-api/terms?utm_source=chatgpt.com) | unpaid data改善利用、人手review  | 2026-09-11 |
| Google | [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing?utm_source=chatgpt.com) | 現行モデル単価・free/paidデータ利用差  | 2026-09-11 |
| Google | [Billing | Gemini API](https://ai.google.dev/gemini-api/docs/billing?utm_source=chatgpt.com) | billing latency、negative balance、spend cap  | 2026-09-11 |

---

## Round 3-2時点のChatGPT担当としての結論

今回かなり大きく整理できました。

**確定側へ動いたもの**は、Jules REST APIの存在、Jules DELETE endpoint、Codex外部操作、Codex App Serverからのinterrupt、Claude Agent SDKのsubscription利用、Gemini無料APIの改善利用・human review、Googleの5h+weekly利用構造とUsage Limits画面です。

一方で、**無理に確定しないもの**は、月額枠の残量を3社とも司令塔から公式API取得できるか、quota境界を長時間agentが跨いだ正確なtransaction semantics、Jules DELETEが実行中processまでhard-killするか、個人subscriptionを第三者向けサービスへ中継できる法的範囲、3社間のusage換算率です。

そしてユーザーのClaude Pro実測については、**Anthropicのf-6-c「使い切った超過分が次のsessionへ借金として持ち越されるか」について、今回観測した条件では「持ち越されなかった」と採用してよい**と判断します。ただしOpenAI・Googleへの横展開はしません。

以上を、ChatGPT側の**Round 3-2正式作業回答**とします。