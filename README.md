# Pipeline-Deck

跨生態系 GitHub Actions 排程、數據萃取管道、GitOps 同步任務與雲端自動化引擎觀測中樞。

- 🌐 **線上門戶 (Live Portal)**: [https://wenchiehlee.github.io/Pipeline-Deck/](https://wenchiehlee.github.io/Pipeline-Deck/)

---

## Deck Family

- 🦌 **UX-Deck** ([Portal](https://wenchiehlee-ux.github.io/UX-Deck/) · [Repo](https://github.com/wenchiehlee-ux/UX-Deck)) — UX resources and presentation.
- 🐇 **Skill-Deck** ([Portal](https://wenchiehlee.github.io/skills/) · [Repo](https://github.com/wenchiehlee/skills)) — skills and related resources.
- 📊 **Analytics-Deck** ([Portal](https://wenchiehlee.github.io/Analytics-Deck/) · [Repo](https://github.com/wenchiehlee/Analytics-Deck)) — telemetry and analytics observability hub across ecosystem endpoints.
- ⚙️ **Pipeline-Deck** ([Portal](https://wenchiehlee.github.io/Pipeline-Deck/) · [Repo](https://github.com/wenchiehlee/Pipeline-Deck)) — pipeline workflows and automation resources.
- 📈 **Data-Deck** ([Portal](https://wenchiehlee-money.github.io/biztrends.TW/) · [Repo](https://github.com/wenchiehlee-money/biztrends.TW)) — Taiwan industry cycles, market trends, and data resources.
- 🧠 **Llm-Deck** ([Portal](https://wenchiehlee.github.io/llm/) · [Repo](https://github.com/wenchiehlee/llm)) — unified LLM client library, multi-provider fallback & smart routing.
- 🐳 **Docker-Deck** ([Portal](https://wenchiehlee.github.io/dockers/) · [Repo](https://github.com/wenchiehlee/dockers)) — Docker image discovery and usage.

---

<!-- PIPELINE_SUMMARY_START -->
## 🌐 全域工作流程、發布門戶與資安遙測統計 (Ecosystem Telemetry)

> **全域統計**：涵蓋 **7 大核心組織**，共有 **77 個活躍儲存庫**（排除已封存庫），其中 **57 個儲存庫** 具備自動化工作流，累計運行 **138 個工作流程 YAML 檔案**、**17 個 GitHub Pages 線上門戶**，以及 **0 個啟用全方位資安防護庫**。（自動掃描更新於：`2026-11-10 10:32:04 UTC`）
>
> 🎯 **北極星核心維運指標 (North Star Quartet)**：**`138 / 57 / 0 / 0`**（**138** 個工作流程 YAML · **57** 個活躍 Actions 庫 · **0** 個嚴重警報 · **0** 個異常警告）

### 📊 組織工作流程、Pages 與資安分佈總覽

| 組織 / 帳號 (`Owner`) | 活躍儲存庫數 | 具備 Actions 的 Repo | 工作流程 YAML 數 | Pages 發布站點 | 資安防護啟用庫 | 待處置警報總數 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| [`ZhongZheng782`](https://github.com/ZhongZheng782) | 5 | 5 | **14** | 2 | 0 | 0 |
| [`wenchiehlee`](https://github.com/wenchiehlee) | 30 | 29 | **66** | 8 | 0 | 0 |
| [`wenchiehlee-money`](https://github.com/wenchiehlee-money) | 24 | 10 | **28** | 4 | 0 | 0 |
| [`wenchiehlee-investment`](https://github.com/wenchiehlee-investment) | 16 | 12 | **29** | 1 | 0 | 0 |
| [`wenchiehlee-ux`](https://github.com/wenchiehlee-ux) | 1 | 1 | **1** | 1 | 0 | 0 |
| [`wenchiehlee-alert`](https://github.com/wenchiehlee-alert) | 0 | 0 | **0** | 0 | 0 | 0 |
| [`wenchiehlee-life`](https://github.com/wenchiehlee-life) | 1 | 0 | **0** | 1 | 0 | 0 |
| **全域總計** | **77** | **57** | **138 個 YAML** | **17 站點** | **0 庫** | **0 處** |

---

### 🚨 常態排程健康度與連續失敗監測 (Scheduled Consecutive Failures)

- **常態排程監測總數**：`46` 個工作流程
- **🚨 嚴重警報（連續失敗 ≥ 4 次）**：`0` 個
- **⚠️ 異常警告（連續失敗 1~3 次）**：`0` 個
- **🟢 正常運行（最新一次執行成功）**：`46` 個

> ✅ **目前全域常態排程工作流程運作狀態良好，無任何連續失敗管道。**

---

### 🌐 GitHub Pages 線上發布門戶觀測 (GitHub Pages Deployments)

- **Pages 發布站點總數**：`17` 個站點
- **🟢 正常發布 (`built`)**：`16` 個
- **🔴 建置異常 (`errored`)**：`1` 個
- **⚪ 其他/初始待命中 (`other`)**：`0` 個

| # | 組織 / 儲存庫 | UX 意象與定位 (UX-Deck) | Pages 線上網址 | 建置狀態 | 建置管道 | 可見性 |
|---|---|---|---|:---:|:---:|:---:|
| 1 | [wenchiehlee-money/My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | 🦉 拍拍翅萌萌鴞 (`台股個股深度調研`) | [https://wenchiehlee-money.github.io/My-TW-Coverage/](https://wenchiehlee-money.github.io/My-TW-Coverage/) | 🔴 異常 (errored) | `workflow` | 🌍 公開 |
| 2 | [wenchiehlee-investment/wenchiehlee-investment.github.io](https://github.com/wenchiehlee-investment/wenchiehlee-investment.github.io) | 💼 投資機構 (`投資組織官方入口`) | [https://wenchiehlee-investment.github.io/](https://wenchiehlee-investment.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 3 | [wenchiehlee-life/wenchiehlee-life.github.io](https://github.com/wenchiehlee-life/wenchiehlee-life.github.io) | 🌱 人文生活 (`生活組織官方門戶`) | [https://wenchiehlee-life.github.io/](https://wenchiehlee-life.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 4 | [wenchiehlee-money/GoogleAlertManager](https://github.com/wenchiehlee-money/GoogleAlertManager) | 🐦 破曉警報鳥 (`SaaS 情報過濾雷達`) | [https://wenchiehlee-money.github.io/GoogleAlertManager/](https://wenchiehlee-money.github.io/GoogleAlertManager/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 5 | [wenchiehlee-money/InvestorConference](https://github.com/wenchiehlee-money/InvestorConference) | 🦅 領航雄鷹 (`法人說明會與 IR 庫`) | [https://wenchiehlee-money.github.io/InvestorConference/](https://wenchiehlee-money.github.io/InvestorConference/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 6 | [wenchiehlee-money/VIX](https://github.com/wenchiehlee-money/VIX) | 🦢 幾何黑天鵝 (`全球波動率黑天鵝雷達`) | [https://wenchiehlee-money.github.io/VIX/](https://wenchiehlee-money.github.io/VIX/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 7 | [wenchiehlee-ux/UX-Deck](https://github.com/wenchiehlee-ux/UX-Deck) | 🦌 幾何靈鹿 (`UX 設計系統中樞`) | [https://wenchiehlee-ux.github.io/UX-Deck/](https://wenchiehlee-ux.github.io/UX-Deck/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 8 | [wenchiehlee/Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | 📊 觀測航線 (`全端點流量遙測中樞`) | [https://wenchiehlee.github.io/Analytics-Deck/](https://wenchiehlee.github.io/Analytics-Deck/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 9 | [wenchiehlee/dockers](https://github.com/wenchiehlee/dockers) | 🐳 貨櫃藍鯨 (`Docker 映像目錄與部署`) | [https://wenchiehlee.github.io/dockers/](https://wenchiehlee.github.io/dockers/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 10 | [wenchiehlee/mkdocs](https://github.com/wenchiehlee/mkdocs) | 📚 知識基底 (`工程技術文件中心`) | [https://wenchiehlee.github.io/mkdocs/](https://wenchiehlee.github.io/mkdocs/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 11 | [wenchiehlee/mkdocs-investment](https://github.com/wenchiehlee/mkdocs-investment) | 🐂🐻 幾何狂牛/守護熊 (`大盤資產配置與避險`) | [https://wenchiehlee.github.io/mkdocs-investment/](https://wenchiehlee.github.io/mkdocs-investment/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 12 | [wenchiehlee/mkdocs-life](https://github.com/wenchiehlee/mkdocs-life) | 🦌 幾何林鹿 (`溫潤人文生活誌`) | [https://wenchiehlee.github.io/mkdocs-life/](https://wenchiehlee.github.io/mkdocs-life/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 13 | [wenchiehlee/Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | ⚙️ 齒輪引擎 (`CI/CD 與自動化管道中樞`) | [https://wenchiehlee.github.io/Pipeline-Deck/](https://wenchiehlee.github.io/Pipeline-Deck/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 14 | [wenchiehlee/skills](https://github.com/wenchiehlee/skills) | 🐇 敏捷白兔 (`共享技能登錄庫`) | [https://wenchiehlee.github.io/skills/](https://wenchiehlee.github.io/skills/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 15 | [wenchiehlee/wenchiehlee.github.io](https://github.com/wenchiehlee/wenchiehlee.github.io) | 👤 個人旗艦 (`個人官方主站門戶`) | [https://wenchiehlee.github.io/](https://wenchiehlee.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 16 | [ZhongZheng782/Synology-Photo-Tagger](https://github.com/ZhongZheng782/Synology-Photo-Tagger) | 🐿️ 採集松鼠 (`AI 相片智慧標籤`) | [https://zhongzheng782.github.io/Synology-Photo-Tagger/](https://zhongzheng782.github.io/Synology-Photo-Tagger/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 17 | [ZhongZheng782/YoutubeAudio.Fetch](https://github.com/ZhongZheng782/YoutubeAudio.Fetch) | 🐋 聲波座頭鯨 (`影音 Podcast 萃取`) | [https://zhongzheng782.github.io/YoutubeAudio.Fetch/](https://zhongzheng782.github.io/YoutubeAudio.Fetch/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |

---

### 🛡️ 全域資安防護、Dependabot 與代碼品質觀測 (Security Posture & Code Quality)

- **秘密掃描防護 (Secret Scanning)**：`0` 個儲存庫啟用
- **阻擋推送防護 (Push Protection)**：`0` 個儲存庫啟用
- **Dependabot 自動安全修正**：`0` 個儲存庫啟用
- **Dependabot 待修復警報**：`0` 處（🔴 0 嚴重 · 🟠 0 高度 · 🟡 0 中度 · 🔵 0 低度）
- **CodeQL 代碼品質與安全漏洞**：`0` 處（🔴 0 嚴重 · 🟠 0 高度 · 🟡 0 中度 · 🔵 0 低度）
- **惡意代碼與外洩警報 (Malware / Leaks)**：`0` 處

> ✅ **目前全域所有活躍儲存庫無任何待處置安全漏洞或品質警報。**

---

### 📁 `ZhongZheng782` (5 個 Repo · 共 14 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [Synology-Photo-Tagger](https://github.com/ZhongZheng782/Synology-Photo-Tagger) | **4** | [🟢 built](https://zhongzheng782.github.io/Synology-Photo-Tagger/) | ⚪ 預設 | 0 | `probe-synology-photos-api.yml`, `probe-tailnet-mlx.yml`, `publish-image.yml`, `scout-image.yml` |
| 2 | [Yahoo.Finance](https://github.com/ZhongZheng782/Yahoo.Finance) | **4** | - | ⚪ 預設 | 0 | `Actions-fetch-wayback.yaml`, `Actions-fetch.yaml`, `Actions-update-lists.yaml`, `sync-up-forecast.yml` |
| 3 | [YoutubeAudio.Fetch](https://github.com/ZhongZheng782/YoutubeAudio.Fetch) | **3** | [🟢 built](https://zhongzheng782.github.io/YoutubeAudio.Fetch/) | ⚪ 預設 | 0 | `daily-channel-fetch.yml`, `sync-to-biztrends.yml`, `update-readme-index.yml` |
| 4 | [Win11](https://github.com/ZhongZheng782/Win11) | **2** | - | ⚪ 預設 | 0 | `action-runner.yml`, `powershell.yml` |
| 5 | [GoPublic](https://github.com/ZhongZheng782/GoPublic) | **1** | - | ⚪ 預設 | 0 | `sync-up.yml` |

### 📁 `wenchiehlee` (29 個 Repo · 共 66 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [GoogleSearch.Factset](https://github.com/wenchiehlee/GoogleSearch.Factset) | **7** | - | ⚪ 預設 | 0 | `Actions-process.yaml`, `Actions-quarantine-files.yaml`, `Actions-search.yaml`, `Actions-update-lists.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 2 | [gsheet.action](https://github.com/wenchiehlee/gsheet.action) | **3** | - | ⚪ 預設 | 0 | `e2e.yml`, `semantic-release.yml`, `test-and-release.yml` |
| 3 | [mcp-cli](https://github.com/wenchiehlee/mcp-cli) | **3** | - | ⚪ 預設 | 0 | `ci.yml`, `npm-publish.yml`, `release.yml` |
| 4 | [mkdocs](https://github.com/wenchiehlee/mkdocs) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs/) | ⚪ 預設 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 5 | [mkdocs-investment](https://github.com/wenchiehlee/mkdocs-investment) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs-investment/) | ⚪ 預設 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 6 | [mkdocs-life](https://github.com/wenchiehlee/mkdocs-life) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs-life/) | ⚪ 預設 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 7 | [Python-Actions.FinMind](https://github.com/wenchiehlee/Python-Actions.FinMind) | **3** | - | ⚪ 預設 | 0 | `daily-finmind-status.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 8 | [Python-Actions.OpenAI](https://github.com/wenchiehlee/Python-Actions.OpenAI) | **3** | - | ⚪ 預設 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 9 | [Python-Actions.OpenAPI](https://github.com/wenchiehlee/Python-Actions.OpenAPI) | **3** | - | ⚪ 預設 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 10 | [Python-Actions.PER](https://github.com/wenchiehlee/Python-Actions.PER) | **3** | - | ⚪ 預設 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 11 | [rss2md](https://github.com/wenchiehlee/rss2md) | **3** | - | ⚪ 預設 | 0 | `rss2md.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 12 | [Selenium-Actions.Auction](https://github.com/wenchiehlee/Selenium-Actions.Auction) | **3** | - | ⚪ 預設 | 0 | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 13 | [Selenium-Actions.IPO](https://github.com/wenchiehlee/Selenium-Actions.IPO) | **3** | - | ⚪ 預設 | 0 | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 14 | [skills](https://github.com/wenchiehlee/skills) | **3** | [🟢 built](https://wenchiehlee.github.io/skills/) | ⚪ 預設 | 0 | `deploy-pages.yml`, `publish-scribd-pdf-fetch.yml`, `update-skills-index.yml` |
| 15 | [twstock](https://github.com/wenchiehlee/twstock) | **3** | - | ⚪ 預設 | 0 | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml`, `twstock-Action.yaml` |
| 16 | [GoPublic](https://github.com/wenchiehlee/GoPublic) | **2** | - | ⚪ 預設 | 0 | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 17 | [whisper](https://github.com/wenchiehlee/whisper) | **2** | - | ⚪ 預設 | 0 | `python-publish.yml`, `test.yml` |
| 18 | [wjlee-barco](https://github.com/wenchiehlee/wjlee-barco) | **2** | - | ⚪ 預設 | 0 | `WP-post-workflow.yml`, `blog-post-workflow.yml` |
| 19 | [AI-Benchmark](https://github.com/wenchiehlee/AI-Benchmark) | **1** | - | ⚪ 預設 | 0 | `benchmark.yml` |
| 20 | [Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | **1** | [🟢 built](https://wenchiehlee.github.io/Analytics-Deck/) | ⚪ 預設 | 0 | `renew-analytics.yml` |
| 21 | [chromium](https://github.com/wenchiehlee/chromium) | **1** | - | ⚪ 預設 | 0 | `docker-publish.yml` |
| 22 | [dockers](https://github.com/wenchiehlee/dockers) | **1** | [🟢 built](https://wenchiehlee.github.io/dockers/) | ⚪ 預設 | 0 | `deploy-pages.yml` |
| 23 | [influxdb-action](https://github.com/wenchiehlee/influxdb-action) | **1** | - | ⚪ 預設 | 0 | `action.yml` |
| 24 | [llm](https://github.com/wenchiehlee/llm) | **1** | - | ⚪ 預設 | 0 | `update-stats.yml` |
| 25 | [Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | **1** | [🟢 built](https://wenchiehlee.github.io/Pipeline-Deck/) | ⚪ 預設 | 0 | `renew-pipeline-telemetry.yml` |
| 26 | [Python-Actions.ChatGPTAutomation](https://github.com/wenchiehlee/Python-Actions.ChatGPTAutomation) | **1** | - | ⚪ 預設 | 0 | `Actions.yaml` |
| 27 | [Python.TWSE-History](https://github.com/wenchiehlee/Python.TWSE-History) | **1** | - | ⚪ 預設 | 0 | `TWSE-API-Action.yaml` |
| 28 | [shell_gpt](https://github.com/wenchiehlee/shell_gpt) | **1** | - | ⚪ 預設 | 0 | `lint_test.yml` |
| 29 | [wenchiehlee.github.io](https://github.com/wenchiehlee/wenchiehlee.github.io) | **1** | [🟢 built](https://wenchiehlee.github.io/) | ⚪ 預設 | 0 | `jekyll.yml` |
| - | *其餘 1 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-money` (10 個 Repo · 共 28 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [InvestorConference](https://github.com/wenchiehlee-money/InvestorConference) | **7** | [🟢 built](https://wenchiehlee-money.github.io/InvestorConference/) | ⚪ 預設 | 0 | `daily-ingest.yml`, `deploy-web.yml`, `ingest.yml`, `sync-gt-to-mac-mini.yml`, `sync-to-downstream.yml`, `sync-yahoo-finance-consensus.yml`, `test-fin-issues.yml` |
| 2 | [GoogleAlertManager](https://github.com/wenchiehlee-money/GoogleAlertManager) | **5** | [🟢 built](https://wenchiehlee-money.github.io/GoogleAlertManager/) | ⚪ 預設 | 0 | `analyze.yml`, `fetch.yml`, `issue-feedback.yml`, `sync-to-downstream.yml`, `test.yml` |
| 3 | [Facebook.Fetch](https://github.com/wenchiehlee-money/Facebook.Fetch) | **4** | - | ⚪ 預設 | 0 | `add-group-handler.yml`, `daily_fetch.yml`, `sync-to-biztrends.yml`, `tag-link-injector.yml` |
| 4 | [diagram-design](https://github.com/wenchiehlee-money/diagram-design) | **3** | - | ⚪ 預設 | 0 | `auto-bump.yml`, `ci.yml`, `pages.yml` |
| 5 | [My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | **3** | [🔴 errored](https://wenchiehlee-money.github.io/My-TW-Coverage/) | ⚪ 預設 | 0 | `daily_update.yml`, `pages.yml`, `sync_to_googlealertmanager.yml` |
| 6 | [VIX](https://github.com/wenchiehlee-money/VIX) | **2** | [🟢 built](https://wenchiehlee-money.github.io/VIX/) | ⚪ 預設 | 0 | `sync.yml`, `update-vix-data.yml` |
| 7 | [AI-Benchmark](https://github.com/wenchiehlee-money/AI-Benchmark) | **1** | - | ⚪ 預設 | 0 | `benchmark.yml` |
| 8 | [local-workspace-mcp](https://github.com/wenchiehlee-money/local-workspace-mcp) | **1** | - | ⚪ 預設 | 0 | `test.yml` |
| 9 | [skills](https://github.com/wenchiehlee-money/skills) | **1** | - | ⚪ 預設 | 0 | `update-skills-index.yml` |
| 10 | [TaiwanLifeInsurance](https://github.com/wenchiehlee-money/TaiwanLifeInsurance) | **1** | - | ⚪ 預設 | 0 | `sync-to-biztrends.yml` |
| - | *其餘 14 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-investment` (12 個 Repo · 共 29 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [InvestorEvents](https://github.com/wenchiehlee-investment/InvestorEvents) | **5** | - | ⚪ 預設 | 0 | `monthly-event-catalogs.yml`, `sync-to-Downstream.yml`, `sync-to-biztrends.yml`, `weekly-dividends.yml`, `weekly-earnings.yml` |
| 2 | [ConceptStocks](https://github.com/wenchiehlee-investment/ConceptStocks) | **4** | - | ⚪ 預設 | 0 | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update_company_financials.yml`, `update_conceptstocks.yml` |
| 3 | [Gemini-CLI](https://github.com/wenchiehlee-investment/Gemini-CLI) | **3** | - | ⚪ 預設 | 0 | `check_quota.yml`, `manual_scripts.yml`, `stock_events.yml` |
| 4 | [ic.tpex.org.tw](https://github.com/wenchiehlee-investment/ic.tpex.org.tw) | **3** | - | ⚪ 預設 | 0 | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update-supply-chain.yml` |
| 5 | [MOPS](https://github.com/wenchiehlee-investment/MOPS) | **3** | - | ⚪ 預設 | 0 | `Download.yaml`, `EarlyFilerDownload.yaml`, `sync-to-Downstream.yml` |
| 6 | [Python-Actions.GoodInfo.CompanyInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo) | **3** | - | ⚪ 預設 | 0 | `Actions.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml` |
| 7 | [GoodInfo.Test](https://github.com/wenchiehlee-investment/GoodInfo.Test) | **2** | - | ⚪ 預設 | 0 | `hybrid-cdp-pipeline.yml`, `test-actions-cdp.yml` |
| 8 | [TaiwanHouse](https://github.com/wenchiehlee-investment/TaiwanHouse) | **2** | - | ⚪ 預設 | 0 | `monthly_update.yml`, `sync-to-biztrends.yml` |
| 9 | [MarketCostDistribution](https://github.com/wenchiehlee-investment/MarketCostDistribution) | **1** | - | ⚪ 預設 | 0 | `sync-outputs.yml` |
| 10 | [poorstock](https://github.com/wenchiehlee-investment/poorstock) | **1** | - | ⚪ 預設 | 0 | `Actions.yaml` |
| 11 | [TAIFEX](https://github.com/wenchiehlee-investment/TAIFEX) | **1** | - | ⚪ 預設 | 0 | `fetch-taifex.yml` |
| 12 | [TaiwanLoanInterest](https://github.com/wenchiehlee-investment/TaiwanLoanInterest) | **1** | - | ⚪ 預設 | 0 | `monthly-cbc-update.yaml` |
| - | *其餘 4 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-ux` (1 個 Repo · 共 1 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [UX-Deck](https://github.com/wenchiehlee-ux/UX-Deck) | **1** | [🟢 built](https://wenchiehlee-ux.github.io/UX-Deck/) | ⚪ 預設 | 0 | `deploy-pages.yml` |

### 📁 `wenchiehlee-alert` (0 個 Repo · 共 0 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| - | *(目前尚無儲存庫)* | 0 | - | - | - | - |

### 📁 `wenchiehlee-life` (0 個 Repo · 共 0 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| - | *其餘 1 個 Repo* | 0 | - | - | - | *(無 Actions)* |

<!-- PIPELINE_SUMMARY_END -->
