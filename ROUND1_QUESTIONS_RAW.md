# AI開発司令塔 / Multi-AI Council
## 設計レビュー依頼 v0.1

あなたは、このシステムを今後実際に構成する協力AIの一員として、
以下の経緯・調査結果・現在案をすべて読んだうえで設計レビューしてください。

これは「どのAIが一番優秀か」を決める企画ではありません。

最終目的は、

「技術知識の少ない人間ユーザーが、複数AIの間でプロンプト・調査結果・コード・レビュー結果を手作業でコピペしたり、どのAIが正しいかを毎回自力で裁定したりしなくても、安全に複数AIを利用できるシステム」

を作ることです。

現在ユーザーはChatGPT、Claude、Gemini/Julesを利用しています。

重要：
まだ実装を開始しません。
今回はアーキテクチャ合意形成フェーズです。

あなた自身の会社・製品に有利な方向へ寄せず、
事実誤認、危険な仮定、不要な複雑化、コスト増大も含めて遠慮なく批判してください。


==================================================
1. この調査を始めた理由
==================================================

ユーザーは現在AIBO Mk-IIというWindows上のゲーム配信用AI相棒を開発しています。

開発では、

・ChatGPT
・OpenAI Codex
・Claude Code
・Google Jules

などを使っています。

しかし現在、人間ユーザー自身が、

1. ChatGPTに相談
2. 指示文をコピー
3. Claude/Jules/Codexを開く
4. 貼り付け
5. 作業完了を待つ
6. 結果をコピー
7. ChatGPTへ戻す
8. 複数AIの回答を人間が比較
9. 次の指示をまたコピー

という「AI間通信係」になっています。

ユーザーは仕事があり、開発時間も限られているため、
この人力部分を可能な限り削減したいと考えています。

さらに今回、

「AIは間違えることがある」
「各AIは持っている情報・検索結果・推論傾向・得意領域が異なる」
「単一AIだけでは知り得ない仕様や見落としが存在する」

ことを実際に確認しました。

そこで単に1つのAIを自動化するのではなく、

複数AIを独立して調査・開発・監査させ、
最後に自動で比較・検証・合議する仕組み

を作る方針を検討しています。


==================================================
2. 最初に各AIへ行った調査
==================================================

Google/Geminiには主に以下を質問しました。

1. Julesを外部司令塔から操作する最適な公式手段
2. Jules APIで可能なこと
   - task/session作成
   - 指示送信
   - plan取得/承認
   - progress/activity取得
   - diff/code changes取得
   - test/bash output取得
   - completion取得
   - 追加指示
   - 中断/停止
3. Jules開発中または完了時にGeminiを監視AIとして使えるか
4. Gemini API Free Tierを監視・レビュー用途に使えるか
5. Gemini Chat無料枠とGemini API無料Tierの違い
6. 一般向けGemini Chatの未使用無料枠を自作プログラムから正式利用できるか
7. Jules定額/無料利用枠とJules API利用量の関係
8. Jules APIとWeb UIの利用枠共有
9. Gemini API Free Tierのrate/token/daily limit
10. private repoをFree Tierへ送る際のデータ利用・privacy
11. GitHub経由でCodex/Claude Code/Julesを協調させる方法
12. Julesの変更を別AIが監視する方法
13. 危険変更時の停止/人間承認
14. deterministic rules → cheap AI → strong AI → human の段階監視
15. Google側で見落としているSDK/API/service

さらにGoogle/Gemini視点で、
ベンダーニュートラルな推奨アーキテクチャを求めました。


Anthropic/Claudeには主に以下を質問しました。

1. Claude Codeを外部司令塔から操作する最適な公式手段
2. Agent SDK / Claude Code CLI / Hooks / MCPの役割
3. 外部から
   - task開始
   - prompt
   - repo read
   - edit
   - bash/test
   - progress
   - result
   - session continuation
   - stop/block
   - human approval
   をどこまで自動化可能か
4. PreToolUse/PostToolUse/Stop/Subagentによる監視
5. HookからGemini/OpenAI等を監視役として呼べるか
6. ClaudeをJules/Codexの監視役にできるか
7. Claude.ai Chat枠とAPI枠
8. Chat未使用枠を自作監視へ正式利用可能か
9. Claude API監視の最小コスト構成
10. Claude Code定額枠を司令塔から使える範囲
11. GitHub経由の三社協調
12. 他AIのdiffをClaudeが自動レビューする方法
13. deterministic-first設計
14. WARN/BLOCK時の差戻し/停止/人間承認
15. Anthropic側の見落としている機能

さらに、
同一ベンダー開発+監視と
異ベンダー開発+監視の長短を比較し、
ベンダーニュートラルな推奨構成を求めました。


==================================================
3. ChatGPTが他2社の回答を見る前に行った独立調査 v0
==================================================

他AIの意見によるアンカリングを避けるため、
ChatGPTはGemini/Claudeの回答を見る前に独立して調査しました。

ChatGPT v0の主要結論：

A.
「AI三人を常時互いに監視させる」のではなく、

司令塔
→ deterministic監視
→ 必要時のみ安価AI
→ 必要時のみ強AI
→ 最後だけ人間

という段階制が本命。

B.
Julesは公式REST APIから、

・GitHub Source指定
・Session作成
・追加message
・Plan approval
・Session/Activity取得

などが可能。

Activityから進捗・bash結果・code changes等を司令塔が取得し、
外部監査AIへ渡す方式が適する。

Jules内部に監査AIを埋め込む必要はない。

Jules
→ Jules API
→ Orchestrator
→ Reviewer AI

と分離する。

C.
Claude CodeはAgent SDK / CLI / Hooks / Subagent / MCP等があり、
外部制御能力が非常に高い。

特にPreToolUseで操作実行前に判定できるため、

Claude Code
→ toolを使おうとする
→ deterministic check
→ 必要なら外部AI
→ allow/deny

という細粒度安全制御が可能。

D.
Gemini Developer API Free Tierは
一般向けGemini Chatとは別物。

無料APIを軽量監査に利用する案は有力だが、
Free Tierでは入力データの利用条件に注意が必要。

private code全文を常時送るのではなく、

・sanitized diff
・test result
・file list
・task specification
・static analysis result

など必要最小限の「監査packet」を送る案を推奨。

E.
Claude.ai Chatの未使用無料枠を
自作プログラムから正式なAPI資源として消費することは想定しない。

Web UI automation / Cookie流用 / scraping等も採用しない。

F.
GitHubだけをシステム全体のSingle Source of Truthにはしない。

ChatGPT v0では、

GitHub = code成果物
Local PC = 実機/未commit/runtime環境
Orchestrator DB = task/agent/approval/audit/workflow state

という三層構造を提案。

G.
通常はdeveloper AI 1名 + reviewer AI最大1名程度。

全AIを毎操作で呼ぶと、
コスト・latency・意見衝突が増え、
人間が結局裁判官になるため避ける。

H.
最終目標：

User
→ ChatGPT/Hub
→ Task Router
→ Codex / Claude Code / Jules
→ deterministic guard
→ cheap reviewer
→ strong reviewer when needed
→ human only for dangerous/ambiguous approval


==================================================
4. Geminiから得た回答
==================================================

Gemini調査の主要結果：

・Julesの外部操作は公式Jules REST APIが最適。
・sessions.create可能。
・sendMessage可能。
・plan取得/approvePlan可能。
・activities取得可能。
・diffはActivity metadataでも部分取得できるが、
  完全なGit diffはGitHub branch/PR側から取得する方が確実。
・test/bash outputはActivity log経由。
・completion検知可能。
・追加指示可能。
・明示的abort/cancel APIは確認できず、
  実行途中の細粒度停止能力は限定的。
・requirePlanApproval=trueで計画段階のgateは可能。

Gemini監視：
Jules activitiesをOrchestratorが取得し、
Gemini APIへ送る構成は可能。

Gemini API Free Tier：
軽量監視/一次reviewに利用可能。

Gemini ChatとDeveloper APIは別。

一般向けGemini Chatの無料枠を
自作プログラムから正式利用する方法はない。

Jules API/Web UIは同一Jules service quotaを共有するという見解。

Gemini Free Tierにはrate limitsがあり、
細粒度ログ全件を無加工で送る設計は避ける。

Free Tierへprivate codeを送る場合、
データ利用/privacyに注意。
有料Tier/Vertex AIの方がprivate code用途には適する。

Gemini推奨監視：

Stage 1:
deterministic rules
(secret/rm -rf/許可path外変更等)

Stage 2:
Gemini lightweight model
(diff summary / specification deviation)

Stage 3:
strong model
(architecture/security)

Stage 4:
human approval

Julesで危険変更が起きた場合は、
Julesをkillするより
isolated branch/PRを閉じる・保護する方式を推奨。

AI監査は毎操作ではなくcommit/diff単位にまとめることで
quota/costを節約。

Google側の追加候補：

・Cloud Run Functions / Eventarc
・Gemini Context Caching
・Secret Manager

Geminiの役割分担提案：

local implementation = Claude Code
async cloud development = Jules
large-context monitoring = Gemini
hub = GitHub Actions + lightweight Python/Node orchestrator

GitHub PR/Issue/Reviewを共通言語として利用。


==================================================
5. Claudeから得た回答
==================================================

Claude調査の主要結果：

Claude Codeの外部制御は
公式機能でほぼ完全にカバーされている。

第一候補：
Claude Agent SDK (Python/TS)

補助：
Claude Code CLI headless (`claude -p`)
Hooks
MCP
GitHub Actions/GitLab CI

Agent SDK/CLIから、

・task
・prompt
・repo read
・file edit
・bash/test
・progress stream
・result
・session continuation
・stop/block
・human approval

を自動化可能。

Claude CodeはPreToolUse Hookによって
tool execution前にdeny/block可能。

PostToolUseで実行後結果を監視可能。

PermissionRequestでhuman approval queueへ送れる。

Stopで「終了しようとしたが未解決なら継続」を実装可能。

SubagentStop等も利用可能。

Hooksは外部processとのJSON I/Oなので、
Hook内部からGemini API/OpenAI API等を呼ぶことも可能。

Claude Code自身については
他AIによるtool-call単位のリアルタイム監視が可能。

一方Jules/Codexは同じ粒度の公開Hookが確認できないため、
基本的にactivity/diff/PR境界の監査になる。

Claude.ai subscriptionとClaude Platform APIは別会計。

ただしClaudeの調査では、
2026年6月にAgent SDK/headless利用をsubscription poolから
別creditへ分離する変更が予告された後pauseされ、
現時点ではAgent SDK/headless等がsubscription shared limitsを
消費する状態だという報告があった。

これは時事的仕様なので、
実装前に公式資料で再確認する必要がある。

Claude Chatの未使用枠を
一般Web UI automationで消費する方式は採用しない。

Claude監査をAPI従量課金で行う場合は、

deterministic
→ lightweight model
→ strong model only when necessary

が最小コスト。

GitHubは三者が共有できる最も現実的なintegration boundary。

Claude:
GitHub Action / Agent SDK

Codex:
CLI / automation

Jules:
REST API / automatic PR

Claudeの提案ではGitHubを共通言語・状態境界として使用。

他AIのdiffをClaudeが自動reviewすることも可能。

Claudeが追加で指摘した機能：

・GitHub Code Review
・GitLab integration
・Bedrock / Vertex AI / Microsoft Foundry routing
・Claude Code Plugins
・`claude mcp serve`

監視AIについて：

同一vendor：
integration/cost/authが単純だが
同じblind spotを共有する危険。

異vendor：
integration complexity/costは増えるが、
model biasやvendor outage/specification changeに強い。

特に最終high-risk gateでは
異vendor reviewerを使う価値がある。


==================================================
6. 三者を比較した結果
==================================================

ChatGPT/Gemini/Claudeは独立調査にもかかわらず、
以下でほぼ一致しました。

1. 人間のAI間コピペをなくすべき。
2. 外部Orchestratorを置く。
3. 全AIを常時監視には使わない。
4. deterministic rulesを最初に置く。
5. 安価AI→強AI→人間の段階制。
6. Jules REST APIは有力。
7. Claude Codeは外部制御に強い。
8. GitHubは重要な共通境界。
9. high-risk時の異vendor reviewには価値がある。
10. consumer Chat無料枠を非公式自動化しない。
11. 人間は最終的な危険/曖昧な判断にだけ関与する。

意見差：

A.
Gemini/ClaudeはGitHubをかなり中心に置く。

ChatGPTは、
GitHubをCode SSOTにはするが、
Workflow全体のSSOTにはしない案。

理由：
local PCの未commit状態、
OBS/VOICEVOX/Windows/device/runtime等はGitHubに存在しない。

したがって現案では、

GitHub = Code SSOT
Orchestrator DB = Workflow SSOT
Local host = Runtime/Device state

とする。

B.
Julesは実行中kill/block能力が弱いため、
「止める」より
「isolated branch/worktree/sandboxから本体へ届かせない」
安全モデルが重要。

C.
Claude Codeだけはtool-call単位のHookを持つため、
他2者と完全に同じ監視方式へ統一しない。

Claude Code:
fine-grained pre-execution supervision

Jules/Codex:
activity/diff/commit/PR boundary supervision

という非対称性を受け入れる。


==================================================
7. この比較後に変更したChatGPT案
==================================================

ChatGPTは当初、
Jules単独automationを最初のprototypeにする案でした。

しかしClaude調査後、

最初のdevelopment-agent automation prototypeは
Claude Codeの方が適している

と変更しました。

理由：

・Agent SDK
・headless CLI
・structured output
・session continuation
・streaming
・Hooks
・interrupt
・permissions

が揃っており、
「外部司令塔→agent→監視→test→result」
の一連の自動化を検証しやすいため。

ただしClaudeを司令塔そのものにはしません。

Orchestrator本体はvendor-neutralな
Python等の通常プログラムにする。

各社はAdapterとして接続する。

例：

Orchestrator
├ ClaudeAdapter
├ JulesAdapter
├ CodexAdapter
├ GeminiReviewerAdapter
└ OpenAIReviewerAdapter

vendorが落ちても
他vendorが使える構造を維持する。


==================================================
8. 新しく追加したい最重要機能
==================================================

ここまでの調査を行う過程で、
さらに重要な問題が判明しました。

今回、人間ユーザー自身が、

ChatGPTへ質問
→ Geminiへ同じ質問をcopy
→ Claudeへ同じ質問をcopy
→ Gemini回答をChatGPTへcopy
→ Claude回答をChatGPTへcopy
→ ChatGPTが比較

という作業を行いました。

しかし、この「独立調査→比較」そのものが
非常に価値のある安全機構でした。

各AIは実際に、

・ChatGPTだけが拾った情報
・Geminiだけが拾った情報
・Claudeだけが拾った情報

を持っていました。

また、一社だけで調査すると
誤情報や古い情報を自信を持って提示する可能性があります。

そこで開発agent automationより先に、

==================================================
Phase 0:
Multi-AI Research Council
==================================================

を構築したいと考えています。


==================================================
9. Multi-AI Research Councilの目的
==================================================

ユーザーが例えば、

「このAPI仕様を調べて」
「この設計は可能？」
「三社比較して」
「このバグの原因を考えて」

と一度だけ依頼すると、

Orchestratorが同一問題を、

・ChatGPT/OpenAI
・Gemini
・Claude

へ独立に送る。

重要：
最初の回答生成時には、
他AIの回答を互いに見せない。

理由：
anchoring / conformity / groupthinkを避けるため。

その後、三者の回答を収集し、

Consensus Engineが、

・三者一致
・二者一致
・三者不一致
・一社だけが主張
・数字/料金/利用枠等のtime-sensitive claim
・vendor-specific claim
・根拠の有無

に分解する。

単純多数決はしない。


==================================================
10. Councilの合議ルール案
==================================================

暫定案：

A. 三者一致
→ confidenceを上げる。
ただし三者が同じ二次情報を参照している可能性があるため、
重要事項ではsource independenceも考慮。

B. 二者一致
→ 残り1者の反論理由を分析。
必要なら一次資料を再確認。

C. 三者不一致
→ 自動で第二調査round。

D. vendor-specific claim
例：
Jules仕様 → Google公式一次資料を優先。
Claude Code仕様 → Anthropic公式一次資料。
Codex/OpenAI仕様 → OpenAI公式一次資料。

ただし「自社AIがそう言ったから正しい」ではなく、
primary sourceによるverificationを要求。

E. 数字・料金・quota・version・availability
→ 必ず最新primary sourceで再確認。

F. primary sourceでも不明
→ 無理に結論を作らず
UNKNOWN / UNVERIFIEDとして残す。

G. source conflict
→ source date/version/authorityを比較。

H. AI間で意見が割れ、
実験で確認可能
→ safe sandbox testを提案/自動実行。

I. それでも解決不能
→ 初めてhumanへ質問。


==================================================
11. Councilの第二ラウンド
==================================================

Round 1:
三AI完全独立回答。

Round 2:
Consensus Engineが
争点だけ抽出。

各AIへ、

「他AIの全文回答」

を丸ごと渡すのではなく、

・争点
・相反するclaim
・primary source
・不足情報

のみ渡し、

再評価させる。

これにより、
他AIの文章表現やconfidenceに引っ張られることを減らす。

Round 3:
まだ不一致なら、

・primary source verification
・sandbox experiment
・stronger model
・specialized agent

へescalate。

Humanは最後。


==================================================
12. Councilが返す最終結果
==================================================

ユーザーへ三人分の長文をそのまま返さない。

例：

CONCLUSION
Jules REST APIでsession作成とplan approvalは可能。

CONFIDENCE
HIGH

AGREEMENT
3/3

VERIFICATION
Google primary documentation confirmed.

DISAGREEMENTS
abort/cancel APIについて意見差あり。
公式資料では確認不能。

UNRESOLVED
実行中hard cancel capability.

ACTION
hard cancelを前提にせず、
isolated branch + protected mainを採用。

HUMAN ACTION
なし。

という形で、
「ユーザー自身がAI三人の裁判官になる」
状況をなくす。


==================================================
13. Development Orchestratorへの拡張計画
==================================================

Council完成後、

Phase 1:
Claude Code単独development automation

User
→ Orchestrator
→ Claude Code
→ Hooks
→ tests
→ result

Phase 2:
Safety / automatic correction

deterministic PreToolUse
→ cheap reviewer if uncertain
→ Claude correction
→ retry N times
→ human only if unresolved

Phase 3:
Jules Adapter

async/cloud/GitHub-oriented tasksを担当。

isolated branch
→ Jules
→ Activities
→ tests/diff
→ review
→ PR

Phase 4:
Codex Adapter

local/remote/agentic tasksへ追加。

Phase 5:
automatic routing

task characteristics,
cost,
quota,
privacy,
required environment,
agent availability,
historical success rate

等からdeveloper/reviewerを自動選択。


==================================================
14. 目標UX
==================================================

最終的にはユーザーが、

「AIBOのGAME_OVERバグ直して」

と一度言うだけ。

Orchestratorが、

1. task解析
2. developer選択
3. isolated branch/worktree作成
4. instruction送信
5. safety monitoring
6. implementation
7. test
8. diff
9. reviewer selection
10. independent review
11. 必要ならdeveloperへ自動差戻し
12. retest
13. high-riskなら異vendor second opinion
14. 結果統合
15. 必要な場合だけhuman approval

まで行う。

ユーザーへは、

「修正完了。
241 tests PASS。
3 reviewers PASS。
mainへのmergeだけ承認してください。」

程度を返す。

ユーザーは各AIサービスを開かず、
prompt/outputをcopyしない。


==================================================
15. 安全原則
==================================================

以下は現時点で必須と考えています。

・main直接編集禁止
・agentごとにbranch/worktree/sandbox分離
・API key/secretsをpromptへ入れない
・secret manager/local encrypted storage
・dangerous commands deterministic block
・dependency changeは追加gate
・test failure時auto merge禁止
・test count低下検知
・large deletion検知
・protected path
・max retry count
・max cost/token/request budget
・agent timeout
・audit log
・all agent outputs tagged with vendor/model/time
・primary-source citation保存
・unknownを許容
・AI多数決だけで危険操作を許可しない
・high-risk merge/deploy/deleteはhuman approval
・Web UI scraping/Cookie流用/非公式consumer quota automationは禁止


==================================================
16. 今回あなたにレビューしてほしいこと
==================================================

この設計にまだ同意しないでください。

まず批判してください。

以下を必ず回答してください。

1.
このPhase 0 → Phase 5の順序は適切か。

2.
特にPhase 0 Multi-AI Research Councilを
development automationより先に作る判断は妥当か。

3.
Councilの「独立Round 1 → dispute-only Round 2 → evidence/experiment Round 3」
は本当にbias低減に有効か。

4.
単純多数決を避ける現在のConsensus Rulesは妥当か。

5.
Consensus Engine自体が誤る問題をどう解決するか。

6.
三AIが同じ誤ったsourceを参照して
全員一致する「correlated failure」をどう検出するか。

7.
vendor-specific primary sourceを優先するルールに問題はないか。
vendor自身のdocumentationが古い/曖昧な場合はどうするか。

8.
AIが引用したsource自体を捏造する可能性への対策。

9.
time-sensitive情報をどうcacheし、
いつ再検証するか。

10.
Research Councilで、
どの時点から3AI全部を呼ばず
1AI/2AIだけで済ませるべきか。

11.
Councilそのもののcost explosionを防ぐ方法。

12.
privacy-sensitiveな質問を
3vendorへ自動送信してしまう危険への対策。

13.
prompt injectionされたWeb page/repository/documentを
Councilが読んだ場合の対策。

14.
悪意ある/壊れた一つのagentが
Consensus Engineを誘導することへの対策。

15.
各AIのconfidence自己申告を信用すべきか。

16.
「3/3一致」をどの程度confidenceに反映すべきか。

17.
ChatGPT / Gemini / Claudeを
完全に対称な三票として扱うべきか。
それともdomainごとのweightを持たせるべきか。

18.
weightを持たせるなら、
固定weightではなく実績から更新すべきか。

19.
その実績評価自体をどうground truth化するか。

20.
CouncilがUNKNOWNを返す条件をどう定義するか。

21.
Human escalationの条件が多すぎて
結局人間が忙しくならないか。

22.
Claude Codeだけfine-grained Hook、
Jules/Codexはcoarser boundaryという
非対称監視をそのまま受け入れるべきか。

23.
GitHub = Code SSOT
Orchestrator DB = Workflow SSOT
Local Host = Runtime State
という三層モデルは妥当か。

24.
Orchestratorがsingle point of failureになる問題。

25.
API障害、quota exhaustion、vendor outage時のfallback。

26.
API key管理・権限分離について追加すべきこと。

27.
各agentに与えるfilesystem/network/GitHub権限を
どう最小化するべきか。

28.
auto-mergeを将来的に許す場合の条件。

29.
AIBOのように実機Windows/OBS/VOICEVOX等が必要なprojectを
cloud agentとどう分業するべきか。

30.
このシステムを作ることで、
逆にユーザーの管理負担が増える危険はないか。

31.
設計がoverengineeringになっている部分はどこか。

32.
Phase 0 MVPとして
「絶対必要」
「後回し」
に分けてほしい。

33.
Phase 0 MVPの最小構成を具体的に提示してほしい。

34.
最初のend-to-end testとして何を使うべきか。

35.
このシステムが「人間のコピペをなくしただけで、
AIの誤りを自動増幅する装置」にならないための条件。

36.
あなた自身の前回回答に誤り・過剰断定・古い情報が
含まれている可能性も考慮し、
今回の回答で自己監査してください。

37.
他2AIの調査結果について、
技術的に疑わしい点があれば具体的に指摘してください。

38.
現在案より安全・単純・安価な代案があれば提示してください。

39.
それでもこの構成を採用するなら、
「実装開始してよい最低条件」を定義してください。

40.
最終的に、
APPROVE
APPROVE WITH CHANGES
REJECT
のどれかを選び、
理由を示してください。


==================================================
17. 回答形式
==================================================

以下の順番で回答してください。

A. Verdict
APPROVE / APPROVE WITH CHANGES / REJECT

B. Critical Problems
実装前に直すべきもの。

C. Strong Parts
現在案で維持すべきもの。

D. Corrections
これまでのChatGPT/Gemini/Claude調査の
誤り・疑わしい点・要再確認点。

E. Phase 0 Revised Architecture
あなたが修正したMVP構成。

F. Consensus Algorithm
具体的な合議アルゴリズム。

G. Security Model
privacy / injection / secrets / permissions。

H. Cost Model
無駄な3AI呼び出しを防ぐ方法。

I. Failure Handling
vendor outage / timeout / bad agent / disagreement。

J. Human Escalation
人間を呼ぶ最小条件。

K. Implementation Gate
これを満たすまでコードを書き始めるな、
という条件。

L. Final Recommendation
理由を含む最終提案。


==================================================
18. 最重要方針
==================================================

このシステムの成功指標は
「AIをたくさん使ったこと」ではありません。

成功とは、

・ユーザーの操作回数が減る
・誤情報が減る
・危険操作が減る
・費用が予測可能
・不明なものをUNKNOWNと言える
・vendor一社に依存しない
・人間がAI同士の伝書鳩にならない

ことです。

複雑な方が格好いいという理由で
機能を増やさないでください。

必要なら現在案を大幅に削って構いません。

あなたはこの案を承認する役ではなく、
壊す役としてレビューしてください。
