# Multi-AI Council — Round 3 事実確認ラウンド  
**ChatGPT / OpenAI側提出回答**  
**調査基準日：2026-09-11（日本時間）**

前回の中断前に確認した内容を保持し、未確認項目を追加調査しました。今回は指定どおり**設計提案は行わず、公式一次資料で確認できた事実とUNKNOWNだけ**を記載します。

なお、私自身のRound 2ではRound 3を「公式一次資料・API reference・Terms/Pricing・version/date等で決着させる」と定義していました。

## 結果一覧

| 項目 | 判定 | 結論 |
|---|---|---|
| a 月額契約だけで司令塔 | **確認できた** | **限定的にYES**。3社とも公式の自動化手段があり、少なくともCodex / Claude Agent SDK / Julesを月額契約側から利用できる |
| b API 1回費用 | **確認できた** | トークン量次第。例示条件なら3社合計 **約35円/回（高性能構成）** |
| c 自動追加課金OFF | **一部確認** | 月額枠側は概ね可能。API側の「厳密な0円超過保証」は3社共通ではない |
| d コスト削減 | **確認できた** | 小型モデル、キャッシュ、Batch/Flex、月額枠優先等あり |
| e A/B/Cの規約・課金 | **確認できた** | 「3社とも従量API必須」は**誤り** |
| f-1 枠構造 | **概ね確認** | OpenAI/Claude/Googleで構造が異なる |
| f-2 枠共有 | **確認できた部分あり** | OpenAI Work+Codex共有、Chatは別。Claudeは各surface共有。Googleはサービス別枠 |
| f-3 月額内機能 | **概ね確認** | 各社とも開発・agent機能を含む。ただしAPI本体は別扱いの場合あり |
| f-4 使用量自動取得 | **UNKNOWN含む** | UI/CLI確認はあるが、個人月額枠を司令塔から取得する正式APIは確認できず |
| f-5 誤従量課金 | **確認できた** | OpenAI/Claudeとも認証方式で課金先が変わる。GoogleもAPI課金系は別 |
| f-6 上限後 | **一部UNKNOWN** | 追加課金を無効なら基本停止。ただし「実行途中」の細部は未文書化が多い |
| f-7 他社比較 | **UNKNOWN** | 83%というOpenAI実測を他社枠へ換算する公式換算率なし |
| ① Jules DELETE | **部分確認** | DELETE存在。ただしhard-cancel/quota停止はUNKNOWN |
| ② Codex外部操作 | **確認できた** | CLI exec / SDK / MCP / App Server等あり |
| ③ Codex監視・中断 | **部分確認** | approval/hooks等あり。SDKのhard interrupt詳細はUNKNOWN |
| ④ Claude Agent SDK課金 | **確認できた** | **現在はサブスク枠を消費**。6月変更案は一時停止 |
| ⑤ Gemini無料APIデータ | **確認できた** | **YES**。改善利用・人手レビューの可能性あり |

---

# a. 現在の月額プランだけで3社連携司令塔を作れるか

## 結論：限定的に **YES**

「3社すべて従量APIを契約しなければ自作プログラムから操作できない」は成立しません。

### OpenAI

Codexは公式に、

- Codex CLI
- `codex exec`
- Codex SDK
- MCP Server
- App Server

などを提供しています。

Codex SDK公式ページは明確に **“Programmatically control local Codex agents”** とし、自作アプリや内部workflowへの組み込みを用途として列挙しています。

さらに認証には、

- ChatGPTログイン → **subscription access**
- API key → **usage-based access**

という2方式があります。

[OpenAI Codex SDK公式資料](https://developers.openai.com/codex/sdk?utm_source=chatgpt.com)  
[OpenAI Codex Authentication公式資料](https://developers.openai.com/codex/auth?utm_source=chatgpt.com)

したがって**ChatGPT Plusの枠で公式Codexを自動利用する道があります**。

### Anthropic

現在の公式Help Centerは、Claude Agent SDK、`claude -p`、Agent SDKベースの第三者アプリについて、**引き続きsubscription usage limitsから消費する**と明記しています。6月15日に予定されていた別クレジット方式への変更は停止されました。

[Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan?utm_source=chatgpt.com)

### Google

Jules REST APIは公式に、

> programmatically access Jules’s capabilities

するためのAPIと説明され、workflow自動化や自作ツールへの組込みが用途として明記されています。APIキーはJules自身のSettingsから発行します。

Google AI Proには**Jules in Pro**が含まれ、100 tasks / rolling 24h、同時15 tasksです。

[Jules REST API Quickstart](https://jules.google/docs/api/reference/?utm_source=chatgpt.com)  
[Jules Limits and Plans](https://jules.google/docs/usage-limits?utm_source=chatgpt.com)

### 重要な限界

これは「ChatGPT/Claude/Geminiの通常チャットを完全にAPI化できる」という意味ではありません。

**Codex・Agent SDK・Julesという、各社が公式に自動化を許可したsurfaceを連携できる**という意味です。

---

# b. 従量APIなら1質問いくらか

API料金は質問数ではなくトークン量なので、固定価格はありません。

比較用に、

**入力10,000 tokens + 出力2,000 tokens**

を「1回」と仮定します。為替は調査時点の **$1 ≒ ¥154** を使用します。

### 高性能構成

| 社 | モデル | Input / 1M | Output / 1M | 仮定1回 |
|---|---|---:|---:|---:|
| OpenAI | GPT-5.6 Sol | $4 | $20 | $0.080 ≒ **12.3円** |
| Anthropic | Claude Opus 5 | $5 | $25 | $0.100 ≒ **15.4円** |
| Google | Gemini 3.1 Pro Preview | $2 | $12 | $0.044 ≒ **6.8円** |
| **合計** | | | | **約34.5円/回** |

OpenAI公式料金：  
Anthropic公式料金：  
Google公式料金：

[OpenAI GPT-5.6 Sol料金](https://developers.openai.com/api/docs/models/gpt-5.6-sol?utm_source=chatgpt.com)  
[Anthropic API料金](https://platform.claude.com/docs/en/about-claude/pricing?utm_source=chatgpt.com)  
[Gemini Developer API料金](https://ai.google.dev/gemini-api/docs/pricing?utm_source=chatgpt.com)

### 安価モデルへの切替

OpenAIにはGPT-5.6 Terra $2/$12、Luna $0.20/$1.20があります。

AnthropicにはClaude Sonnet 5 $2/$10、Haiku 4.5 $1/$5等があります。

したがって同じ質問でもモデルroutingで数倍～十数倍変わります。

**約35円は固定価格ではなく、上記10k→2kという比較条件での値です。**

---

# c. 自動追加課金OFF＋上限で停止

### Claude Pro：YES

Usage creditsは任意です。無効化すると**included usageのみ**になります。

月間spending cap、auto-reload設定もあります。

### OpenAI ChatGPT Plus：YES（included枠）

追加Creditsはincluded usageを使い切った後に使用される追加機能です。

ただしOpenAI Platform APIはChatGPT Plusとは別会計です。

### Google AI Pro：サービス依存

Google AI Proでは各サービスに独自の枠があります。

Gemini API Prepayについては非常に明確で、残高0になるとAPI keyが停止します。ただし約10分のbilling pipeline latencyにより**negative balanceになる場合がある**とGoogle自身が明記しています。

したがって、

**「自動チャージOFF」は可能。  
「絶対1円も超えない」はGoogle Gemini APIでは保証されない。**

---

# d. 公式コスト削減

確認できた代表例です。

OpenAIはLuna/Terra等の小型モデル、cached input。AnthropicはHaiku/Sonnet、prompt caching、Batch API 50%引き。GoogleはBatch/FlexがStandardより安価で、Gemini 3.1 ProではStandard $2/$12に対しBatch/Flex $1/$6です。

---

# e. 「3社すべて月額枠自動利用は規約違反」の検証

## 判定：その一般化は **誤り**

ここはA/B/Cを分離します。

### A. ブラウザUIを非公式自動操作

OpenAIの利用規約には、サービスからデータ/Outputを**自動またはプログラムで抽出すること**を禁止する記載があります。

したがってCookie流用やスクレイピングを「公式CLIと同じ」と扱えません。

[OpenAI利用規約](https://openai.com/ja-JP/policies/terms-of-use/?utm_source=chatgpt.com)

Anthropic/Googleについて、今回の検索では同一条件を直接規定する最新一次資料を十分確認できなかったため、**UNKNOWN**とします。

### B. 公式CLI / SDK / REST API

これはAと全く違います。

OpenAI：ChatGPT subscription accessによるCodex CLIが公式。`codex exec`はStableで、scripted/CI-style run用です。

Anthropic：Claude Agent SDK / `claude -p`は現在subscription limitsを使用可能。

Google：Jules REST APIは公式programmatic interface。Jules in ProはGoogle AI Pro特典。

したがって、

> 「月額枠から自作プログラムがAIを呼ぶことは3社全部規約違反」

は**一次資料に反します**。

### C. 通常の従量API

これは別会計です。

OpenAIはAPI keyログインをするとstandard API pricingになります。

Claude ProもClaude Console API usageを含みません。

Gemini Developer APIにも独立したFree/Paid tierがあります。

### 個人利用 vs 他人へ配布

**個人PC上の自分用公式CLI/SDK利用：公式用途として確認。**

一方「他人のリクエストを自分の個人subscriptionへ通すサービス」の全面的許否は、3社について同一条件を明示した一次資料を今回確保できませんでした。

**UNKNOWN。**

不足証拠：各社consumer subscription termsにおけるthird-party serving/resaleの明示条項。

---

# f-1. 月額枠の構造

## ChatGPT Plus

WorkとCodexは**共通allowance**です。

5時間枠＋週間枠が適用される場合、**両方に残量が必要**です。

5時間枠は前window終了後、次にWork/Codexへmessageを送った時点から新window開始。

[Managing usage with GPT-6 Astra in Work and Codex](https://help.openai.com/en/articles/20001516?utm_source=chatgpt.com)

## Claude Pro

5時間session limit＋weekly limit。

週間枠はアカウントごとの固定日時にリセットされ、毎cycle full allowanceが与えられます。

## Google AI Pro

**1個の共通枠ではありません。**

Geminiアプリはcompute-based limitで、weekly limit到達まで5時間ごとにreset。

Jules in Proは、

**100 tasks / rolling 24 hours、15 concurrent tasks。** 

Antigravityにはsubscriptionに基づく**独自のtime-bound baseline quota**があります。

---

# f-2. 枠の共有関係

### OpenAI

**Work + Codex = 共通枠。**

Regular ChatはこのWork/Codex usage viewに含まれません。

したがって以前のユーザー記憶、

> Chatとエージェント枠は別。5時間/週間表示はエージェント側

は**概ね正しかった**です。

### Anthropic

Claude公式は、

> claude.ai / Claude Code / Claude Desktop 等のsurfaceは同じusage limit

と明記しています。

Coworkもstandard chatより多くusage allocationを消費すると公式説明されています。

### Google

各productに独自AI usage limitがある、とGoogle自身が明記しています。

つまりGemini App/Jules/Antigravityを一つの5時間枠として扱えません。

---

# f-3. 月額内で使える機能

### ChatGPT Plus

今回確認できた範囲：

ChatGPT Chat、Work、Codex CLI、Codex desktop/IDE、Codex cloud、Codex SDK経由のlocal Codex等。

通常OpenAI Platform APIは**別料金**。

### Claude Pro

Claude Chat、Claude Code、Claude Desktop、Cowork、現在のClaude Agent SDK / `claude -p`。

ただしClaude Console APIは別料金。

注意：Claude Fable 5/5.1は現在Pro included usageではなくusage creditsです。

### Google AI Pro

Gemini app、AI Studioのexpanded limits、Jules in Pro、Antigravity expanded limits、各種Google製品内Gemini等。

Gemini Developer API Paid Tierは別billing systemです。

---

# f-4. 使用量確認

### OpenAI

Settings → Usageで確認可能。

Codex TUIには現在正式に `/usage daily`、`/usage weekly`、`/usage cumulative` があります。

しかし**個人Plusの残り5時間/週間allowanceを任意プログラムから取得する公開API**は今回公式資料で発見できませんでした。

**Programmatic remaining-quota API = UNKNOWN。**

OpenAI Platform APIにはOrganization Usage APIがありますが、これはAPI usageであってPlus included Codex枠とは別です。

### Claude

Settings → Usageで5時間/weekly progress確認可能。

個人Pro included quotaをprogrammaticに取得する公式API：

**UNKNOWN。**

### Google

Jules APIはquota超過時429を返しますが、Google AI Pro全体/Jules残量を取得する正式quota endpointは今回確認できませんでした。

**UNKNOWN。**

したがって現時点では、**3社の月額残量を司令塔が正式APIで完全取得して「残り5%で停止」する構造は確認できません。**

---

# f-5. 意図しない従量課金

### OpenAI

Codex公式資料は非常に明確です。

ChatGPT login：

**subscription access**

API key：

**usage-based access**

API key認証時はstandard API pricing。

さらに、

`codex login status`

で現在の認証方式を確認できます。

管理設定には、

`forced_login_method = "chatgpt"`

も存在します。

ただし個人OpenAIアカウント全体について「API従量課金を絶対無効化するconsumer側kill switch」は今回確認できませんでした。

**メーカー側完全防止機能：UNKNOWN / 確認できず。**

最善策：CodexをChatGPT loginに固定し、`codex login status`を確認し、API key環境と分離。

### Claude

設問に記載された事実を公式資料で再確認できました。

`ANTHROPIC_API_KEY`が設定されているとClaude CodeはsubscriptionではなくAPI keyを使用し、API料金になります。

Usage credits自体はOFFにできます。OFFならincluded usageのみです。

### Google

Jules REST APIのキーは**Jules Settingsから生成するJules用キー**です。

Gemini Developer API billingとは同一物として扱えません。

Gemini API Prepayはbilling account単位で、残高0なら関連API keyが停止します。

---

# f-6. 枠を使い切った場合

## f-6-a

### OpenAI

included Work/Codex allowanceを使い切ると、追加Creditsがある場合はそれを利用できます。Creditsはincluded usageの後です。

追加Creditを購入しなければreset待ち。

### Claude

Usage credits OFFならincluded limit到達後は利用できずreset待ち。ON＋残高ありならstandard API rateで継続を選択できます。

### Google

Gemini appは上限到達後、対象上位modelはreset待ちで、Flash-Liteへ継続できる場合があります。

Julesはtask quota。

---

## f-6-b 「上限ちょうど」「途中停止」

ここは公式資料が不足しています。

**OpenAI/Claude/Julesとも、1つの長時間agent taskがincluded quota境界を跨いだ瞬間に内部のどのstepで停止するか、既消費分をどう扱うか、reset後に自動resumeするかを統一的に説明した一次資料を確認できませんでした。**

したがって：

**UNKNOWN。**

不足証拠：各サービスのquota enforcement transaction semantics。

なおGoogle Gemini API Prepayだけは例外的に詳細があり、約10分billing latencyによりlong-running agent/batchが残高を超えて進む場合があります。

---

## f-6-c 超過分

月額included quotaについて、OpenAI/Claude/Julesで「超過usageを次periodから差し引く」とする一次資料は確認できませんでした。

**UNKNOWN。**

Gemini API Prepayではnegative balanceが発生した場合、**次回credit purchaseから差し引かれる**と明記されています。

---

## f-6-d 未使用分

Claudeは各weekly cycleで**full weekly allowanceを受け取る**と明記。

OpenAIもCodex resetは5-hour/weekly windowをrefreshする仕組みです。

Google Gemini appも5時間/weeklyでreset。

**未使用included quotaの繰越制度は確認できませんでした。**

したがって通常枠については、**reset前に余った枠を次periodへbankする仕組みは公式資料上確認できない**、が正確です。

OpenAIの「banked reset」は別物で、未使用quotaの繰越ではなく、キャンペーン等で付与されたone-time resetです。

---

# f-6-e モデル選択

### OpenAI

明確に差があります。

Plusで5時間あたり推定local messages：

- GPT-6 Astra：5–45
- GPT-5.6 Sol：10–100
- GPT-5.6 Terra：25–200
- GPT-5.6 Luna：250–2,000

と公式例があります。

つまり軽量modelは同じallowanceで桁違いに多く処理できる場合があります。

### Claude

公式にmodel choice、effort level、tool usage等でusage consumptionが変わるとされています。

ただし「SonnetならOpusの正確にX倍」という固定換算は公開されていません。

### Google

Gemini appもmodel・feature・prompt complexity等を考慮したcompute-based usageです。

固定倍率はUNKNOWN。

---

# f-7. OpenAI実測83%との他社比較

## UNKNOWN

ChatGPT Plusで、

- weekly 83%
- 5h limit一度到達
- 約900追加credits

という実測値をClaude Pro / Google AI Proへ変換できる公式換算率は存在しません。

Claude自身もusageがconversation length、model、feature、effort等で変動するとしています。

Googleもcompute-basedでcomplexity/model/featuresを考慮します。

したがって数字を作ることはしません。

**Round 3指定どおり、実測比較実験まで保留するのが正しいです。**

---

# ① Jules DELETE

## Endpoint存在：確認できた

現行公式APIに、

`DELETE /v1alpha/sessions/{sessionId}`

があります。

公式説明は単に：

> Deletes a session.

成功時empty response。

[Jules Sessions API](https://jules.google/docs/api/reference/sessions?utm_source=chatgpt.com)

## 実行中agentをhard-stopするか

**UNKNOWN。**

公式ページは「sessionをdeleteする」としか書いておらず、

- active execution即時停止
- remote process停止
- quota消費停止時点
- eventual cancellation
- already-created PRへの影響

を説明していません。

したがって、

**DELETE endpoint存在 = 確定**  
**hard cancel = 未確定**

です。

これは私自身のRound 2で分離したJ1～J7と一致します。

---

# ② Codex/OpenAIの外部programmatic control

## 確認できた

現行Codexには少なくとも、

- `codex exec` — Stable、non-interactive/script/CI
- Codex SDK
- Codex MCP Server
- App Server
- Codex cloud CLI

があります。

特にSDKは、

> start, continue, and resume local Codex threads

を正式にサポートします。

つまりRound 2でUNKNOWNにしていた

**「Codexを外部programから公式に操作できるか」**

は現在 **YES** に更新できます。

---

# ③ Codex監視・approval・interrupt・hooks

## Approval：YES

`--ask-for-approval`

でhuman approval policyを制御できます。

## Hooks：YES

Lifecycle hooksがあり、`/hooks`でinspect/trust/disableできます。

## Sandbox：YES

read-only / workspace-write / danger-full-access等を指定できます。

## SDK hard interrupt

今回確認したCodex SDK一次資料には明示的なthread interrupt/cancel semanticsを発見できませんでした。

**UNKNOWN。**

API Responses側にはbackground responseをcancelするendpointがありますが、これはCodex SDK threadのhard killと同一とは扱いません。

---

# ④ Claude Agent SDK課金

## 確認できた

これはRound 3の大きな更新点です。

2026-06-15に、

Agent SDK / `claude -p`をsubscription枠から外してmonthly Agent SDK credit方式へ変更する予定でした。

しかしAnthropicはその変更を**pause**しました。

現在の公式ページ冒頭：

> For now, nothing has changed: Claude Agent SDK, `claude -p`, and third-party app usage still draw from your subscription's usage limits. 


したがって2026-09-11現在：

**Claude Agent SDK / `claude -p` = Claude Pro subscription usage limitから消費可能。**

「Agent SDKは必ずAPI従量課金」は**現時点では誤り**です。

---

# ⑤ Gemini API無料枠へprivate codeを送る場合

## 確認できた：YES、改善利用対象

現行Gemini API Additional Termsでは、Unpaid Services（Google AI StudioやGemini API unpaid quota）について、

Googleは入力と生成responseを製品・サービス・ML技術の提供・改善・開発に利用するとしています。

さらに、

**human reviewers may read, annotate, and process API input and output**

と明記されています。

[Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms?utm_source=chatgpt.com)

したがって、

**Gemini API無料枠へprivate source codeを送れば、改善利用および人手reviewの対象になり得ます。**

一方Paid Servicesでは、

**prompts/responsesをGoogle製品改善には使用しない**

と明記されています。

これはCouncilのprivacy gateに直接関係する確定事実です。

---

# サービス名称確認

Round 3の指示に従い名称も確認しました。

Googleの現行正式プラン名は **Google AI Pro** です。現在のGoogle One公式ページもこの名称を使用しています。

旧名称から現名称への**正確な改称日**について、今回確認した公式ページでは確定できませんでした。

**変更時期：UNKNOWN。**

OpenAIは現行 **ChatGPT Plus**、Anthropicは現行 **Claude Pro**。

開発surfaceの現行名称は、

**Codex / Claude Code / Claude Cowork / Claude Agent SDK / Jules / Google Antigravity**

を確認しました。

---

# Round 3で確定した重要事実

今回もっとも重要なのは、Round 2で争点になった主張がかなり整理できたことです。

**「3社とも月額プランを自作プログラムから使うことは規約違反で、従量API keyが絶対必要」**

という強い主張は、**採用できません。**

OpenAIはChatGPT subscription accessでCodexを公式に自動化でき、AnthropicはClaude Agent SDK / `claude -p`を現在subscription枠から正式に利用でき、GoogleはJules REST APIを公式programmatic interfaceとして提供し、Jules in ProをGoogle AI Proに含めています。

一方、

**非公式ブラウザ自動操作（A）  
公式CLI/SDK/REST（B）  
通常の従量API（C）**

は明確に別物として扱う必要があります。

また、Round 2で私自身がUNKNOWNとしていた「Codex exact external orchestration capability」「Claude subscription/Agent SDK billing semantics」「Gemini Free Tier privacy/data-use semantics」は、今回かなりの部分を一次資料で確定できました。

残った主なUNKNOWNは、**Jules DELETEのhard-cancel semantics、各社個人月額枠の残量を正式APIでprogrammatic取得する方法、quota境界に長時間agent taskが到達した瞬間の厳密なtransaction semantics、個人subscriptionを第三者向けサービスのbackendとして使う場合の3社横並びの明示規定**です。

以上を**ChatGPT Round 3公式回答**とします。Round 4のプレゼンにはまだ進みません。