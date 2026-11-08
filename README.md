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
## 🌐 全域工作流程遙測統計 (Ecosystem Actions Telemetry)

> **全域統計**：涵蓋 **4 大核心組織**，共有 **93 個儲存庫**，其中 **58 個儲存庫** 具備自動化工作流，累計運行 **141 個工作流程 YAML 檔案**。（自動掃描更新於：`2026-11-08 09:34:06 UTC`）

### 📊 組織與工作流程總覽

| 組織 / 帳號 (`Owner`) | 儲存庫總數 | 具備 Actions 的 Repo 數 | 工作流程 YAML 總數 |
|---|:---:|:---:|:---:|
| [`ZhongZheng782`](https://github.com/ZhongZheng782) | 5 | 5 | **14** |
| [`wenchiehlee`](https://github.com/wenchiehlee) | 46 | 30 | **67** |
| [`wenchiehlee-money`](https://github.com/wenchiehlee-money) | 24 | 10 | **28** |
| [`wenchiehlee-investment`](https://github.com/wenchiehlee-investment) | 18 | 13 | **32** |
| **全域總計** | **93** | **58** | **141 個 YAML** |

---

### 🚨 常態排程健康度與連續失敗監測 (Scheduled Consecutive Failures)

- **常態排程監測總數**：`48` 個工作流程
- **🚨 嚴重警報（連續失敗 ≥ 4 次）**：`9` 個
- **⚠️ 異常警告（連續失敗 1~3 次）**：`3` 個
- **🟢 正常運行（最新一次執行成功）**：`36` 個

#### 🔴 嚴重警報：常態排程連續失敗 ≥ 4 次清單

| # | 儲存庫 | 工作流程名稱 | YAML 檔案 | 連續失敗次數 | 最近 4 次狀態 | 最新失敗時間 | 執行日誌 |
|---|---|---|---|:---:|:---:|---|:---:|
| 1 | [wenchiehlee/Python.TWSE-History](https://github.com/wenchiehlee/Python.TWSE-History) | TWSE API On GitHub Actions | `TWSE-API-Action.yaml` | **30 次** | `❌❌❌❌` | `2026-11-08T08:53:14` | [Run ↗](https://github.com/wenchiehlee/Python.TWSE-History/actions/runs/42464814342) |
| 2 | [wenchiehlee/Selenium-Actions.Auction](https://github.com/wenchiehlee/Selenium-Actions.Auction) | Run Selenium On GitHub Action | `Selenium-Action.yaml` | **30 次** | `❌❌❌❌` | `2026-11-08T08:52:41` | [Run ↗](https://github.com/wenchiehlee/Selenium-Actions.Auction/actions/runs/42464775091) |
| 3 | [wenchiehlee/Selenium-Actions.IPO](https://github.com/wenchiehlee/Selenium-Actions.IPO) | Run Selenium On GitHub Action | `Selenium-Action.yaml` | **30 次** | `❌❌❌❌` | `2026-11-07T13:42:22` | [Run ↗](https://github.com/wenchiehlee/Selenium-Actions.IPO/actions/runs/42378180085) |
| 4 | [wenchiehlee/Python-Actions.OpenAI](https://github.com/wenchiehlee/Python-Actions.OpenAI) | API On GitHub Actions | `Actions.yaml` | **20 次** | `❌❌❌❌` | `2026-11-08T08:54:36` | [Run ↗](https://github.com/wenchiehlee/Python-Actions.OpenAI/actions/runs/42464907072) |
| 5 | [wenchiehlee-investment/MOPS](https://github.com/wenchiehlee-investment/MOPS) | Sync to Downstream | `sync-to-Downstream.yml` | **19 次** | `❌❌❌❌` | `2026-11-08T05:17:25` | [Run ↗](https://github.com/wenchiehlee-investment/MOPS/actions/runs/42450183427) |
| 6 | [wenchiehlee/Python-Actions.OpenAPI](https://github.com/wenchiehlee/Python-Actions.OpenAPI) | OpenAPI On GitHub Actions | `Actions.yaml` | **19 次** | `❌❌❌❌` | `2026-11-07T13:36:53` | [Run ↗](https://github.com/wenchiehlee/Python-Actions.OpenAPI/actions/runs/42377769801) |
| 7 | [wenchiehlee/Python-Actions.PER](https://github.com/wenchiehlee/Python-Actions.PER) | OpenAPI On GitHub Actions | `Actions.yaml` | **19 次** | `❌❌❌❌` | `2026-11-07T13:49:47` | [Run ↗](https://github.com/wenchiehlee/Python-Actions.PER/actions/runs/42378735586) |
| 8 | [wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo) | Sync to Analyzer | `sync-to-Analyzer.yml` | **15 次** | `❌❌❌❌` | `2026-11-07T15:17:28` | [Run ↗](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo/actions/runs/42385652367) |
| 9 | [wenchiehlee/GoogleSearch.Factset](https://github.com/wenchiehlee/GoogleSearch.Factset) | Sync to Analyzer | `sync-to-Analyzer.yml` | **15 次** | `❌❌❌❌` | `2026-11-07T22:27:47` | [Run ↗](https://github.com/wenchiehlee/GoogleSearch.Factset/actions/runs/42420718685) |

#### 🟡 異常警告：常態排程最新一次失敗（連續失敗 1~3 次）

| # | 儲存庫 | 工作流程名稱 | YAML 檔案 | 連續失敗次數 | 最近 4 次狀態 | 最新失敗時間 | 執行日誌 |
|---|---|---|---|:---:|:---:|---|:---:|
| 1 | [ZhongZheng782/Win11](https://github.com/ZhongZheng782/Win11) | Powershell | `powershell.yml` | **1 次** | `❌` | `2026-11-02T21:34:57` | [Run ↗](https://github.com/ZhongZheng782/Win11/actions/runs/41529645966) |
| 2 | [ZhongZheng782/Yahoo.Finance](https://github.com/ZhongZheng782/Yahoo.Finance) | Daily Yahoo Finance Wayback Fetch | `Actions-fetch-wayback.yaml` | **1 次** | `❌✅✅✅` | `2026-11-08T06:28:31` | [Run ↗](https://github.com/ZhongZheng782/Yahoo.Finance/actions/runs/42454889835) |
| 3 | [wenchiehlee-money/My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | Daily Update Financials & Valuation | `daily_update.yml` | **1 次** | `❌✅✅✅` | `2026-11-08T08:27:37` | [Run ↗](https://github.com/wenchiehlee-money/My-TW-Coverage/actions/runs/42463027112) |

---

### 📁 `ZhongZheng782` (5 個 Repo · 共 14 個 YAML)

| # | 儲存庫名稱 | YAML 數 | 工作流程 YAML 清單 |
|---|---|:---:|---|
| 1 | [Synology-Photo-Tagger](https://github.com/ZhongZheng782/Synology-Photo-Tagger) | **4** | `probe-synology-photos-api.yml`, `probe-tailnet-mlx.yml`, `publish-image.yml`, `scout-image.yml` |
| 2 | [Yahoo.Finance](https://github.com/ZhongZheng782/Yahoo.Finance) | **4** | `Actions-fetch-wayback.yaml`, `Actions-fetch.yaml`, `Actions-update-lists.yaml`, `sync-up-forecast.yml` |
| 3 | [YoutubeAudio.Fetch](https://github.com/ZhongZheng782/YoutubeAudio.Fetch) | **3** | `daily-channel-fetch.yml`, `sync-to-biztrends.yml`, `update-readme-index.yml` |
| 4 | [Win11](https://github.com/ZhongZheng782/Win11) | **2** | `action-runner.yml`, `powershell.yml` |
| 5 | [GoPublic](https://github.com/ZhongZheng782/GoPublic) | **1** | `sync-up.yml` |

### 📁 `wenchiehlee` (30 個 Repo · 共 67 個 YAML)

| # | 儲存庫名稱 | YAML 數 | 工作流程 YAML 清單 |
|---|---|:---:|---|
| 1 | [GoogleSearch.Factset](https://github.com/wenchiehlee/GoogleSearch.Factset) | **7** | `Actions-process.yaml`, `Actions-quarantine-files.yaml`, `Actions-search.yaml`, `Actions-update-lists.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 2 | [gsheet.action](https://github.com/wenchiehlee/gsheet.action) | **3** | `e2e.yml`, `semantic-release.yml`, `test-and-release.yml` |
| 3 | [mcp-cli](https://github.com/wenchiehlee/mcp-cli) | **3** | `ci.yml`, `npm-publish.yml`, `release.yml` |
| 4 | [mkdocs](https://github.com/wenchiehlee/mkdocs) | **3** | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 5 | [mkdocs-investment](https://github.com/wenchiehlee/mkdocs-investment) | **3** | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 6 | [mkdocs-life](https://github.com/wenchiehlee/mkdocs-life) | **3** | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 7 | [Python-Actions.FinMind](https://github.com/wenchiehlee/Python-Actions.FinMind) | **3** | `daily-finmind-status.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 8 | [Python-Actions.OpenAI](https://github.com/wenchiehlee/Python-Actions.OpenAI) | **3** | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 9 | [Python-Actions.OpenAPI](https://github.com/wenchiehlee/Python-Actions.OpenAPI) | **3** | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 10 | [Python-Actions.PER](https://github.com/wenchiehlee/Python-Actions.PER) | **3** | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 11 | [rss2md](https://github.com/wenchiehlee/rss2md) | **3** | `rss2md.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 12 | [Selenium-Actions.Auction](https://github.com/wenchiehlee/Selenium-Actions.Auction) | **3** | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 13 | [Selenium-Actions.IPO](https://github.com/wenchiehlee/Selenium-Actions.IPO) | **3** | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 14 | [twstock](https://github.com/wenchiehlee/twstock) | **3** | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml`, `twstock-Action.yaml` |
| 15 | [GoPublic](https://github.com/wenchiehlee/GoPublic) | **2** | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 16 | [mkdocs-material](https://github.com/wenchiehlee/mkdocs-material) | **2** | `build.yml`, `documentation.yml` |
| 17 | [skills](https://github.com/wenchiehlee/skills) | **2** | `publish-scribd-pdf-fetch.yml`, `update-skills-index.yml` |
| 18 | [whisper](https://github.com/wenchiehlee/whisper) | **2** | `python-publish.yml`, `test.yml` |
| 19 | [wjlee-barco](https://github.com/wenchiehlee/wjlee-barco) | **2** | `WP-post-workflow.yml`, `blog-post-workflow.yml` |
| 20 | [AI-Benchmark](https://github.com/wenchiehlee/AI-Benchmark) | **1** | `benchmark.yml` |
| 21 | [Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | **1** | `renew-analytics.yml` |
| 22 | [chromium](https://github.com/wenchiehlee/chromium) | **1** | `docker-publish.yml` |
| 23 | [influxdb-action](https://github.com/wenchiehlee/influxdb-action) | **1** | `action.yml` |
| 24 | [llm](https://github.com/wenchiehlee/llm) | **1** | `update-stats.yml` |
| 25 | [mkdocs-demo](https://github.com/wenchiehlee/mkdocs-demo) | **1** | `deploy.yml` |
| 26 | [Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | **1** | `renew-pipeline-telemetry.yml` |
| 27 | [Python-Actions.ChatGPTAutomation](https://github.com/wenchiehlee/Python-Actions.ChatGPTAutomation) | **1** | `Actions.yaml` |
| 28 | [Python.TWSE-History](https://github.com/wenchiehlee/Python.TWSE-History) | **1** | `TWSE-API-Action.yaml` |
| 29 | [shell_gpt](https://github.com/wenchiehlee/shell_gpt) | **1** | `lint_test.yml` |
| 30 | [wenchiehlee.github.io](https://github.com/wenchiehlee/wenchiehlee.github.io) | **1** | `jekyll.yml` |
| - | *其餘 16 個 Repo* | 0 | *(無 Actions)* |

### 📁 `wenchiehlee-money` (10 個 Repo · 共 28 個 YAML)

| # | 儲存庫名稱 | YAML 數 | 工作流程 YAML 清單 |
|---|---|:---:|---|
| 1 | [InvestorConference](https://github.com/wenchiehlee-money/InvestorConference) | **7** | `daily-ingest.yml`, `deploy-web.yml`, `ingest.yml`, `sync-gt-to-mac-mini.yml`, `sync-to-downstream.yml`, `sync-yahoo-finance-consensus.yml`, `test-fin-issues.yml` |
| 2 | [GoogleAlertManager](https://github.com/wenchiehlee-money/GoogleAlertManager) | **5** | `analyze.yml`, `fetch.yml`, `issue-feedback.yml`, `sync-to-downstream.yml`, `test.yml` |
| 3 | [Facebook.Fetch](https://github.com/wenchiehlee-money/Facebook.Fetch) | **4** | `add-group-handler.yml`, `daily_fetch.yml`, `sync-to-biztrends.yml`, `tag-link-injector.yml` |
| 4 | [diagram-design](https://github.com/wenchiehlee-money/diagram-design) | **3** | `auto-bump.yml`, `ci.yml`, `pages.yml` |
| 5 | [My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | **3** | `daily_update.yml`, `pages.yml`, `sync_to_googlealertmanager.yml` |
| 6 | [VIX](https://github.com/wenchiehlee-money/VIX) | **2** | `sync.yml`, `update-vix-data.yml` |
| 7 | [AI-Benchmark](https://github.com/wenchiehlee-money/AI-Benchmark) | **1** | `benchmark.yml` |
| 8 | [local-workspace-mcp](https://github.com/wenchiehlee-money/local-workspace-mcp) | **1** | `test.yml` |
| 9 | [skills](https://github.com/wenchiehlee-money/skills) | **1** | `update-skills-index.yml` |
| 10 | [TaiwanLifeInsurance](https://github.com/wenchiehlee-money/TaiwanLifeInsurance) | **1** | `sync-to-biztrends.yml` |
| - | *其餘 14 個 Repo* | 0 | *(無 Actions)* |

### 📁 `wenchiehlee-investment` (13 個 Repo · 共 32 個 YAML)

| # | 儲存庫名稱 | YAML 數 | 工作流程 YAML 清單 |
|---|---|:---:|---|
| 1 | [InvestorEvents](https://github.com/wenchiehlee-investment/InvestorEvents) | **5** | `monthly-event-catalogs.yml`, `sync-to-Downstream.yml`, `sync-to-biztrends.yml`, `weekly-dividends.yml`, `weekly-earnings.yml` |
| 2 | [ConceptStocks](https://github.com/wenchiehlee-investment/ConceptStocks) | **4** | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update_company_financials.yml`, `update_conceptstocks.yml` |
| 3 | [Gemini-CLI](https://github.com/wenchiehlee-investment/Gemini-CLI) | **3** | `check_quota.yml`, `manual_scripts.yml`, `stock_events.yml` |
| 4 | [ic.tpex.org.tw](https://github.com/wenchiehlee-investment/ic.tpex.org.tw) | **3** | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update-supply-chain.yml` |
| 5 | [MOPS](https://github.com/wenchiehlee-investment/MOPS) | **3** | `Download.yaml`, `EarlyFilerDownload.yaml`, `sync-to-Downstream.yml` |
| 6 | [Python-Actions.GoodInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo) | **3** | `Actions.yaml`, `Dispatcher.yaml`, `sync-to-Analyzer.yml` |
| 7 | [Python-Actions.GoodInfo.CompanyInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo) | **3** | `Actions.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml` |
| 8 | [GoodInfo.Test](https://github.com/wenchiehlee-investment/GoodInfo.Test) | **2** | `hybrid-cdp-pipeline.yml`, `test-actions-cdp.yml` |
| 9 | [TaiwanHouse](https://github.com/wenchiehlee-investment/TaiwanHouse) | **2** | `monthly_update.yml`, `sync-to-biztrends.yml` |
| 10 | [MarketCostDistribution](https://github.com/wenchiehlee-investment/MarketCostDistribution) | **1** | `sync-outputs.yml` |
| 11 | [poorstock](https://github.com/wenchiehlee-investment/poorstock) | **1** | `Actions.yaml` |
| 12 | [TAIFEX](https://github.com/wenchiehlee-investment/TAIFEX) | **1** | `fetch-taifex.yml` |
| 13 | [TaiwanLoanInterest](https://github.com/wenchiehlee-investment/TaiwanLoanInterest) | **1** | `monthly-cbc-update.yaml` |
| - | *其餘 5 個 Repo* | 0 | *(無 Actions)* |

<!-- PIPELINE_SUMMARY_END -->
