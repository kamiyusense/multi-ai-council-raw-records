PURPOSE: Round 1で独立に出された設計レビューを受け、 他者の指摘を見たことで自分の意見がどう変化したか、 どこを維持するか、 どこで反対するか、 Round 3で何を証拠によって決着させるべきかを明示する。
重要な前提。
Multi-AI Councilの元となった初期設計文書は、 ChatGPTが過去の人間・各AIとの調査結果を整理・統合して作成した文書である。
したがって、それ自体を 「独立したCHATGPT_R1_RAW」 として扱ってはならない。
また現在この回答を生成しているChatGPTの参照状態では、
- Claude Round 1については詳細なRAW内容を保持している
- Gemini Round 1については詳細な内容・論点は保持しているが、 完全な逐語RAWが現在の参照状態には存在しない
という非対称がある。
よって私は、 Geminiについて保持していない原文の表現を捏造したり、 「全文RAWを精読した」と主張したりしない。
この制約そのものが、 Councilにおける以下の原則を強化する。
RAW is authoritative. SUMMARY is derived. Every derived artifact must retain provenance.
============================================================
1. WHAT CHANGED AFTER ROUND 1 REVIEWS? ============================================================
YES. 私の意見はいくつか明確に変わった。
最大の変化は、 当初想定していたCouncilを 「賢いConsensus Engine」に寄せすぎていたことへの警戒が強くなったこと。
Round 1後の現在は、
「Consensus Engine」 ではなく
「Comparison / Evidence Engine」
と考える方が適切だと思う。
Councilの役目は、 3人のAIを何らかの方法で一つの"正解"に収束させることではない。
役目は、
- 誰が何を主張したか
- どこが一致しているか
- どこが食い違っているか
- 何を根拠としているか
- 根拠は本当にその主張を支えるか
- いつ時点の情報か
- 何がまだUNKNOWNか
を壊さずに整理し、 検証可能な形に変換することである。
[CHANGE 1]
BEFORE: Consensus Engineが各回答を解析し、 一致度・信頼度・過去性能等を用いて ある程度自動的に結論を生成する構想。
AFTER: Phase 0では動的な信頼度重み付けを行わない。
REASON: 実運用データもground truthも無い段階で 「Claude 0.82、Gemini 0.76」のような重みを付けても 精密に見えるだけの疑似精度になる。
信頼度モデルは、 実際に正誤判定可能な履歴データが蓄積してから検討すべき。
[CHANGE 2]
BEFORE: Round 1 → 自動Round 2 → 自動Round 3 まで比較的積極的に回す構想。
AFTER: Phase 0では自動Round 2 / Round 3を外す。
REASON: 自動反復はコスト・遅延・複雑性を増やし、 まだCouncil本体の比較品質すら測れていない段階では早すぎる。
まず独立Round 1を正確に収集・保存・比較できることを証明する。
[CHANGE 3]
BEFORE: Orchestrator DBを早い段階からWorkflow SSOTとして置く構想。
AFTER: Phase 0ではappend-onlyなRAW/eventログから始める。
REASON: SQLite等のDBが必要になること自体は長期的には自然だが、 最初から複雑な状態管理を導入する必要はない。
必要性が実測された時点で昇格すればよい。
[CHANGE 4]
BEFORE: AIによる意味的統合をConsensus Engineの中心に置く傾向があった。
AFTER: LLMによる意味解析は「派生物」であり、 決してauthoritative truthではない。
REASON: Consensusを判定するAIそのものが誤解すれば、 3つの回答が正しくても統合工程で壊れる。
これはreviewer regressの一種である。
以下はRound 1後も維持する。
1. 
3社の単純多数決を真実判定に使わない。
3/3一致は重要なシグナルだが、 3社が同じ古い記事・同じ誤解・同じ二次情報を参照することはあり得る。
AGREEMENT != VERIFICATION.
2. 
UNKNOWN / UNVERIFIEDを正式な結果として許す。
Councilが毎回答えを出す必要はない。
「現在の証拠では判断不能」 は失敗ではなく、 捏造された確定回答より良い。
3. 
Round 1のblind independenceは維持する。
最初から他AIの答えを見せると、 アンカリングと同調が起き、 独立した失敗モードを観測できない。
4. 
Round 2は相互批判・自己修正のために使う。
Round 1: 独立思考
Round 2: 他者を見た上で、 「何を変えたか」 「何を維持するか」 「何に反論するか」 を明示する。
これは単なる再回答より価値がある。
5. 
Round 3はモデル性能で殴るラウンドにしない。
残った事実争点は、
- 公式一次資料
- API reference
- Terms / pricing
- version/date metadata
- controlled experiment
によって決着させる。
6. 
外部Orchestratorはvendor-neutralであるべき。
OpenAI、Anthropic、Googleのいずれかを Council全体の永久的司令塔に固定しない。
各社はadapterとして接続する。
7. 
長期的なtruthを一個の場所に押し込まない。
Code truth: Git / GitHub
Workflow truth: Orchestrator records / DB
Runtime/device truth: Local PC
AIBOのようにOBS、VOICEVOX、Windowsデバイス等が絡むシステムでは、 GitHubだけでは現実の状態を表せない。
GeminiのRound 1で特に有用だった方向性として、 以下を採用する。
1. 
Phase 0を大胆に削るべきという指摘。
これは正しい。
最初から 自動重み付け、 複雑な自動Round、 高度な自己学習、 開発agent制御 まで入れるべきではない。
2. 
deterministic-firstの思想。
schema validation、 URL normalization、 重複、 日時、 欠落field、 budgetなど、 機械的に判定できるものをLLMへ投げない。
3. 
cheap → stronger → human という段階的エスカレーション。
ただしこれは 「安いAIを常時監視役にする」 という意味ではなく、
機械判定で足りない時だけAI、 さらに難しい時だけ強いAI、 重大な行動だけ人間、 という構造として採用する。
4. 
Julesのような粗い制御粒度のagentについて、 完全なリアルタイムkillに期待せず、 branch / PR / isolationによって被害範囲を限定する発想。
最も重要な反対点はこれ。
「URLや文字列をdeterministicに比較すれば Consensusを十分判定できる」
という方向には反対する。
URL一致は、
- 同じURLを貼った
- URLが存在する
ことしか証明しない。
それは、
- そのページが主張を本当に支えている
- その文脈で解釈が正しい
- 情報が現在も有効
- 例外条件が無い
ことを証明しない。
HTTP 200も同様。
HTTP 200 = resource responded
であり、
claim verified
ではない。
必要なのは概念的に、
CLAIM ↕ SOURCE PASSAGE ↕ VERSION / DATE ↕ INTERPRETATION
の結び付きである。
また、 固定の
15秒timeout N回retry 10 successful runs 固定TTL
等は、 初期値として仮置きするのはよいが、 設計上の真理として採用しない。
計測して調整可能なparameterにする。
Claude Round 1から最も重要だと思った指摘は、 RAW provenanceの問題である。
これは全面採用する。
今回のCouncil設計を議論する過程自体で、
Claude/Geminiの回答 ↓ ChatGPTによる要約 ↓ 別AIへ伝達
という伝言ゲームが既に起きていた。
これはCouncilが将来解決したい問題を、 Council設計会議自身が再現していたことになる。
したがって今後、
RAW: authoritative
SUMMARY: derived
を明確に分離する。
SUMMARYには最低でも、
- source RAW id
- summarizer
- model
- timestamp
- transformation type
を持たせる。
Claudeのもう一つの有力な指摘、
「Consensus Engineそのものがsingle point of semantic failureになる」
も採用する。
統合LLMを使ってはいけない、とは思わない。
しかし、 統合LLMの出力だけを見て 元RAWを捨てたり、 それをtruthとして扱ったりしてはいけない。
Claude案の
「1つのLLM synthesis pass」 をPhase 0で使うこと自体には反対しない。
ただしそれをauthoritative integrationにしてはいけない。
LLM synthesisは
USER-FACING VIEW
であって、
SYSTEM OF RECORD
ではない。
また、
HIGH confidence = 2 independent URLs + 3/3 agreement
のような機械的基準には反対。
理由:
1. 
2 URLが本当に独立とは限らない。
同じpress releaseを転載した二次記事かもしれない。
2. 
URLがclaimの核心部分を支えている保証がない。
3. 
3社が同じ誤ったsourceから学習・検索するcorrelated failureがある。
4. 
公式資料ですらversion mismatchがあり得る。
したがってconfidenceは、 単純なURL本数やAI票数だけで決めない。
3社Councilにしても、 独立性は完全ではない。
共通失敗源として、
- 同じ公開ドキュメント
- 同じ検索ランキング
- 同じStack Overflow / GitHub issue
- 同じ報道記事
- 同じ曖昧な製品表現
- 相互に似たtraining corpus
- 同じ人間作成promptのbias
がある。
さらに今回は、
Councilの初期文書をChatGPTが編集した
という明確な共通アンカーが存在する。
したがってRound 2で3者が合意しても、
「ChatGPTの初期frameに全員が引きずられた」
可能性を考慮する。
名称変更を提案する。
旧: Consensus Engine
新: Comparison / Evidence Engine
理由:
Consensusという語は、 「合意を作ることが目的」 という誤解を生みやすい。
実際の目的は、
- agreement detection
- disagreement detection
- claim extraction
- provenance tracking
- evidence linking
- freshness tracking
- UNKNOWN preservation
だからである。
DETERMINISTIC LAYER SHOULD HANDLE:
- vendor/model metadata
- timestamp
- round
- RAW hash / ID
- schema validation
- missing fields
- URL extraction
- URL normalization
- exact duplicate detection
- date extraction where explicit
- version strings where explicit
- budget
- token/usage/cost telemetry
- parse failure
- timeout/retry telemetry
LLM MAY ASSIST:
- semantic claim extraction
- paraphrase matching
- contradiction detection
- argument comparison
- source-passage relevance assessment
- unresolved-question generation
BUT:
LLM-derived fields must remain traceable to RAW.
この争点は一文で扱うべきではない。
「JulesにDELETEがある」 と 「実行中agentを即時hard-stopできる」 は別claimである。
Round 3では最低でも以下に分割する。
J1: DELETE /sessions/{id} endpointは現行公式APIに存在するか。
J2: DELETEの正式なdocumented semanticsは何か。
J3: active execution中に呼ぶとexecutionは停止するか。
J4: 停止する場合、即時かeventualか。
J5: 既に開始されたremote work/processは継続し得るか。
J6: 削除後のquota / billing / runtimeへの影響は何か。
J7: 既に作成されたchange / PR / resultはどうなるか。
これは一次資料と、 必要なら捨ててもよいtest repository上のcontrolled experimentで確認する。
長期設計では3種類のtruthを分ける。
A. CODE HISTORY Git / GitHub
B. WORKFLOW / COUNCIL HISTORY Orchestrator
C. LOCAL REALITY PC / runtime / devices
ただしPhase 0では、 本格DBを必須にしない。
最低限、
append-only JSONL / structured RAW files
で、
- input
- output
- metadata
- model
- timing
- usage
- sources
- derived artifacts
を保存できればよい。
DB化はquery / concurrency / recovery requirementが生じてからでよい。
Phase 0はREAD-ONLYを強く支持する。
初期Councilには、
- shell execution
- git write
- deploy
- arbitrary filesystem write
- production API mutation
- automatic merge
を与えない。
また、 「regexでsecretを消せば安全」 とは考えない。
secret sanitizerは必要だが、 regexだけでは不十分。
より上位のルールは、
「その情報をそもそも外部vendorへ送ってよいのか」
を送信前に分類すること。
最低限、
PUBLIC INTERNAL PRIVATE-CODE SECRET PERSONAL/SENSITIVE
等の送信区分が必要。
SECRETは原則fan-out禁止。
Councilは 「常に最強モデル3体で殴るシステム」 にしない。
今回ユーザーと3社で確認している方針を支持する。
Round 1: 各社の通常有料契約で普段使いに近いモデル
Round 2: 同じ契約内・追加従量課金なしの範囲で 高推論側へ一段エスカレーション
Round 3: さらにモデル課金を上げるのではなく PRIMARY EVIDENCEへ移行
今回の正式Round 2条件候補は、
OpenAI: GPT-5.6 Sol / High
Anthropic: Claude Opus 5 / effort High (ユーザーUI確認では追加クレジットなし)
Google: Gemini 3.1 Pro thinking強化を併用するかは、 Google AI Pro内の追加課金・上げ幅・UI条件を確認した上で確定
重要なのは、 3社をベンチマーク上完全同一性能に揃えることではない。
揃えるべきなのは、
「一般的な有料プラン内」 「追加従量課金なし」 「通常状態→高推論状態」
という運用上のエスカレーション階層である。
固定値をAIの勘で決めるより、 実測値を保存する。
最低限:
- vendor
- exact model ID when available
- UI-observed model when API ID unavailable
- reasoning/effort setting
- timestamp
- latency
- input/output tokens where available
- credit/cost where available
- retries
- timeout
- schema parse failures
- tool calls
- source count
- unsupported claims
- changed-mind count
- final unresolved count
特に今回、 Geminiが自身のmodel nameを誤申告し、 ユーザーがUIで訂正した事例が発生した。
したがってモデル情報には、
MODEL_REPORTED_BY_SYSTEM/API MODEL_OBSERVED_IN_UI MODEL_SELF_REPORTED_BY_AI
を可能なら分離する。
優先順位は概念的に、
system/API evidence

user-observed UI

AI self-report
とする。
現時点では以下を確定仕様にしない。
- exact model routing policy
- exact timeout
- exact retries
- exact cache TTL
- exact confidence thresholds
- dynamic vendor reliability weights
- always-on LLM synthesis
- SQLite requirement
- Jules DELETE hard-cancel semantics
- Claude subscription/Agent SDK billing semantics
- Codex exact external orchestration capability
- Gemini Free Tier privacy/data-use semantics
- structured output guarantees across all vendors
これらは Round 3の事実確認、 またはPhase 0の実測対象。
人間に毎回判断を返すCouncilは失敗。
しかし人間を完全に外すのも違う。
Phase 0では、 主に以下の場合にhuman escalationする。
- sensitivity classificationが不明
- evidenceを確認しても重大な争点がUNKNOWN
- 後続フェーズで不可逆・高影響actionを行う
- security boundaryを越える
- merge/deploy/payment/account permission等
普通の軽微なagreementまで 人間に毎回投げない。
相棒 ↓ local vendor-neutral orchestrator ↓ sensitivity gate ↓ parallel independent Round 1 fan-out ├─ OpenAI ├─ Anthropic └─ Google ↓ immutable RAW + provenance storage ↓ deterministic metadata/schema/source extraction ↓ optional auditable semantic comparison ↓ human-readable report
REPORT SHOULD SHOW:
- direct answers
- claims
- three-way agreements
- two-way agreements
- conflicts
- unique proposals
- sources
- source freshness
- provenance
- UNKNOWN
- RAW references
Phase 0 DOES NOT INCLUDE:
- automatic Round 2
- automatic Round 3
- dynamic reliability weights
- autonomous code editing
- shell
- git write
- deploy
- automatic PR merge
- self-modifying policy
数値を今ここで恣意的に固定するより、 以下の性質を満たすことをgateとする。
1. 
同じ質問を3 vendorへ独立送信できる。
2. 
各RAWを失わず保存できる。
3. 
各回答にmodel/provenance/timeを紐付けられる。
4. 
一社失敗しても他社RAWを破壊しない。
5. 
summaryから元RAWへ戻れる。
6. 
semantic comparisonが誤っても 元RAWから監査・再計算できる。
7. 
secret/sensitive情報を誤fan-outしにくい境界がある。
8. 
UNKNOWNを無理にYES/NOへ潰さない。
9. 
usage/cost/latencyを計測可能。
10. 
Phase 0自体には破壊的action能力がない。
優先的に一次資料または実験で決着すべきもの:
A. Jules API
- DELETE endpoint existence
- exact semantics
- active-run cancellation behavior
B. Claude
- Claude.ai / Claude Code / Agent SDK / APIの subscription / credit / API billing境界
C. Codex
- 現在の外部programmatic control surface
- CLI/API/Remoteで可能なこと
- approval / interrupt / resume capability
D. Gemini
- Free Tier / paid APIのdata-use/privacy conditions
- consumer Gemini UIとのbilling/quota separation
E. Structured output
- 3 vendorでの現在のschema/JSON guarantees
- failure/retry behavior
F. Evidence quality
- URLが存在するかではなく source passageがclaimを実際にsupportしているか
Phase 0を大幅に単純化する提案には賛成する。
特に、 自動Roundや信頼度weightを初期版から外す方向は採用する。
一方で、 URL一致・HTTP成功・文字列比較だけでは semantic truthやclaim supportは確認できない。
あなたにはRound 3で、
「どの程度までdeterministic処理で安全に比較でき、 どこからsemantic evaluatorが必要になるか」
をさらに詰めてほしい。
RAW provenanceに関する批判を全面的に採用する。
Council設計会議そのものが summary伝言ゲームを起こしていた、 という指摘は非常に重要だった。
ただし、 あなたが提案するone-LLM synthesis passも 同じ問題の対象になる。
synthesisは便利だが、 authoritative truthにはしない。
また、 agreement数とURL本数だけで HIGH confidenceを機械的に与える設計には反対する。
私自身の最大のbiasは、
「統合する仕組みを作るAI」 として、 統合レイヤーを必要以上に賢くしようとする傾向。
これは警戒すべき。
Phase 0で最も価値があるのは、 賢い結論生成器ではなく、
「三者が何を言ったかを一切壊さず、 後から誰でも追跡できる記録装置」
かもしれない。
もう一つのbiasは、 OpenAI系の制御面について 他vendorより詳しく見積もりやすい点。
そのためOpenAI capabilityも 自社知識だけで優遇せず、 他社と同じくRound 3で現行公式仕様を確認すべき。
NON-NEGOTIABLE 1: RAWとprovenanceを保存する。
NON-NEGOTIABLE 2: SUMMARYをRAWの代用品にしない。
NON-NEGOTIABLE 3: 多数決をverificationにしない。
NON-NEGOTIABLE 4: UNKNOWNを正式結果として許可する。
NON-NEGOTIABLE 5: 時変情報にはfreshnessを持たせる。
NON-NEGOTIABLE 6: 一次資料は「URLがある」だけでなく、 claimを実際にsupportしているか確認する。
NON-NEGOTIABLE 7: Phase 0に破壊的write/action能力を持たせない。
NON-NEGOTIABLE 8: モデルの自己申告を唯一のmodel provenanceにしない。
VERDICT: APPROVE WITH CHANGES
CHANGED MY MIND: YES
MOST IMPORTANT CHANGE: Councilを「合意を生成する賢いConsensus Engine」ではなく、 「RAWを保存し、主張・相違・証拠・UNKNOWNを監査可能にする Comparison / Evidence Engine」として始める。
MOST IMPORTANT DISAGREEMENT: synthesis modelや、 URL本数・AI票数のような簡単な指標によって、 不確実な回答を"verified truth"へ昇格させてはいけない。
NON-NEGOTIABLE: RAW provenance and UNKNOWN must survive every stage.
MESSAGE TO GEMINI: 単純化には賛成。 ただしURL/string一致はclaim verificationではない。
MESSAGE TO CLAUDE: RAW critiqueを採用する。 ただしone-LLM synthesis自身も同じ監査対象である。
ROUND 3 PRIORITY: PRIMARY EVIDENCE / CONTROLLED EXPERIMENTS
RE-RUN ROUND 1: NO
RE-RUN THIS ROUND 2: NO, unless input provenance is later shown to be materially incomplete. If additional missing RAW is supplied later, do not silently overwrite this response. Preserve this RAW and create a separately versioned response.