<!-- PIPELINE_SUMMARY_START -->
## 🌐 全域工作流程、發布門戶與資安遙測統計 (Ecosystem Telemetry)

> **全域統計**：涵蓋 **7 大核心組織**，共有 **106 個活躍儲存庫**（排除已封存庫），其中 **74 個儲存庫** 具備自動化工作流，累計運行 **224 個工作流程 YAML 檔案**、**17 個 GitHub Pages 線上門戶**，以及 **77 個啟用全方位資安防護庫**。（自動掃描更新於：`2026-11-24 15:32:51 UTC`）
>
> 🎯 **北極星核心維運指標 (North Star Quartet)**：**`224 / 74 / 0 / 4`**（**224** 個工作流程 YAML · **74** 個活躍 Actions 庫 · **0** 個嚴重警報 · **4** 個異常警告）

### 📊 組織工作流程、Pages 與資安分佈總覽

| 組織 / 帳號 (`Owner`) | 活躍儲存庫數 | 具備 Actions 的 Repo | 工作流程 YAML 數 | Pages 發布站點 | 資安防護啟用庫 | 待處置警報總數 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| [`ZhongZheng782`](https://github.com/ZhongZheng782) | 31 | 20 | **92** | 2 | 5 | 0 |
| [`wenchiehlee`](https://github.com/wenchiehlee) | 32 | 30 | **67** | 8 | 30 | 0 |
| [`wenchiehlee-money`](https://github.com/wenchiehlee-money) | 25 | 11 | **35** | 4 | 24 | 0 |
| [`wenchiehlee-investment`](https://github.com/wenchiehlee-investment) | 16 | 12 | **29** | 1 | 16 | **2** |
| [`wenchiehlee-ux`](https://github.com/wenchiehlee-ux) | 1 | 1 | **1** | 1 | 1 | 0 |
| [`wenchiehlee-alert`](https://github.com/wenchiehlee-alert) | 0 | 0 | **0** | 0 | 0 | 0 |
| [`wenchiehlee-life`](https://github.com/wenchiehlee-life) | 1 | 0 | **0** | 1 | 1 | 0 |
| **全域總計** | **106** | **74** | **224 個 YAML** | **17 站點** | **77 庫** | **2 處** |

---

### 🚨 常態排程健康度與連續失敗監測 (Scheduled Consecutive Failures)

- **常態排程監測總數**：`65` 個工作流程
- **🚨 嚴重警報（連續失敗 ≥ 4 次）**：`0` 個
- **⚠️ 異常警告（連續失敗 1~3 次）**：`4` 個
- **🟢 正常運行（最新一次執行成功）**：`61` 個

#### 🟡 異常警告：常態排程最新一次失敗（連續失敗 1~3 次）

| # | 儲存庫 | 工作流程名稱 | YAML 檔案 | 連續失敗次數 | 最近 4 次狀態 | 最新失敗時間 | 執行日誌 |
|---|---|---|---|:---:|:---:|---|:---:|
| 1 | [wenchiehlee-money/biztrends.TW](https://github.com/wenchiehlee-money/biztrends.TW) | Check Data Health | `check-data-health.yml` | **3 次** | `❌❌❌` | `2026-11-24T14:04:56` | [Run ↗](https://github.com/wenchiehlee-money/biztrends.TW/actions/runs/45410132361) |
| 2 | [wenchiehlee/Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | 4-Times-Daily Analytics Telemetry Renew | `renew-analytics.yml` | **2 次** | `❌❌✅✅` | `2026-11-24T03:42:45` | [Run ↗](https://github.com/wenchiehlee/Analytics-Deck/actions/runs/45321389130) |
| 3 | [wenchiehlee-money/biztrends.TW](https://github.com/wenchiehlee-money/biztrends.TW) | Update Cycle Indices | `update_indices.yml` | **1 次** | `❌` | `2026-11-23T10:16:53` | [Run ↗](https://github.com/wenchiehlee-money/biztrends.TW/actions/runs/45154643866) |
| 4 | [wenchiehlee/Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | Daily Ecosystem Pipelines & Failure Telemetry Renew | `renew-pipeline-telemetry.yml` | **1 次** | `❌✅❌✅` | `2026-11-24T08:46:11` | [Run ↗](https://github.com/wenchiehlee/Pipeline-Deck/actions/runs/45359015460) |

#### ⚙️ Runner 環境告警（如 Node.js 版本棄用通知）

- **常態排程最新一次執行中偵測到的 Runner 告警**：`77` 筆，影響 `36` 個排程工作流程

| # | 告警等級 | 訊息內容 | 出現次數 | 受影響儲存庫數 |
|---|:---:|---|:---:|:---:|
| 1 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: BetaHuhn/repo-file-sync-action@latest. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 11 | 8 |
| 2 | ℹ️ notice | "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026. For more information, see https://github.com/actions/runner-images/issues/14748" | 5 | 4 |
| 3 | 🔴 failure | Process completed with exit code 1. | 4 | 3 |
| 4 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 3 | 3 |
| 5 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: BetaHuhn/repo-file-sync-action@v1. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 3 | 2 |
| 6 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: astral-sh/setup-uv@v5. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 3 | 3 |
| 7 | 🔴 failure | Nothing was fetched | 3 | 1 |
| 8 | 🔴 failure | The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings | 2 | 1 |
| 9 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/configure-pages@v5, actions/deploy-pages@v4, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 2 | 2 |
| 10 | 🔴 failure | Error: No artifacts named "github-pages" were found for this workflow run. Ensure artifacts are uploaded with actions/upload-artifact@v4 or later. | 2 | 2 |
| 11 | 🔴 failure | Error: No artifacts named "github-pages" were found for this workflow run. Ensure artifacts are uploaded with actions/upload-artifact@v4 or later.
    at getArtifactMetadata (/home/runner/work/_actions/actions/deploy-pages/v4/src/internal/api-client.js:85:1)
    at processTicksAndRejections (node:internal/process/task_queues:104:5)
    at Deployment.create (/home/runner/work/_actions/actions/deploy-pages/v4/src/internal/deployment.js:66:1)
    at main (/home/runner/work/_actions/actions/deploy-pages/v4/src/index.js:30:1) | 2 | 2 |
| 12 | 🔴 failure | Fetching artifact metadata failed. Is githubstatus.com reporting issues with API requests, Pages, or Actions? Please re-run the deployment at a later time. | 2 | 2 |
| 13 | ⚠️ warning | Source data/reports/wayback_yahoo_finance_consensus.csv not found | 2 | 1 |
| 14 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/upload-artifact@v5. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 2 | 2 |
| 15 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: tj-actions/changed-files@v45. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 2 | 2 |
| 16 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v2. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 2 | 1 |
| 17 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-python@v5, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 18 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/download-artifact@v4, actions/setup-python@v5, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 19 | ⚠️ warning | Source reports/dividends-report/dividends-report-2454.md not found | 1 | 1 |
| 20 | ⚠️ warning | Source reports/dividends-report/dividends-report-3034.md not found | 1 | 1 |
| 21 | ⚠️ warning | Source reports/dividends-report/dividends-report-2480.md not found | 1 | 1 |
| 22 | ⚠️ warning | Source reports/dividends-report/dividends-report-8299.md not found | 1 | 1 |
| 23 | ⚠️ warning | Source reports/dividends-report/dividends-report-2382.md not found | 1 | 1 |
| 24 | ⚠️ warning | Source reports/dividends-report/dividends-report-2412.md not found | 1 | 1 |
| 25 | ⚠️ warning | Source reports/market-analysis-pe-forward-return-report-tr-all.md not found | 1 | 1 |
| 26 | ⚠️ warning | Source reports/market-analysis-pe-forward-return-report not found | 1 | 1 |
| 27 | ⚠️ warning | Source reports/market-analysis-drawdown-report-all.md not found | 1 | 1 |
| 28 | ⚠️ warning | Source reports/market-analysis-drawdown-report not found | 1 | 1 |
| 29 | ⚠️ warning | Source reports/roa-roe-report-all.md not found | 1 | 1 |
| 30 | ⚠️ warning | Source reports/roa-roe-report not found | 1 | 1 |
| 31 | ⚠️ warning | Source reports/dividends-report-all.md not found | 1 | 1 |
| 32 | ⚠️ warning | Source reports/dividends-report not found | 1 | 1 |
| 33 | ⚠️ warning | The `python-version` input is not set.  The version of Python currently in `PATH` will be used. | 1 | 1 |
| 34 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: astral-sh/setup-uv@v5, BetaHuhn/repo-file-sync-action@v1. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 35 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: google-github-actions/auth@v2. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 36 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: astral-sh/setup-uv@v5, BetaHuhn/repo-file-sync-action@latest. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 37 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/configure-pages@v5, actions/setup-python@v5, actions/upload-artifact@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 38 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/deploy-pages@v4. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 39 | ⚠️ warning | Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: sarisia/actions-readme-feed@v1. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/ | 1 | 1 |
| 40 | 🔴 failure | [feed 1/1] max retry count exceeded. Abort. | 1 | 1 |
| 41 | 🔴 failure | [feed 1/1][try 3/3] failed to get feed: Error: Request timed out after 5000ms | 1 | 1 |
| 42 | 🔴 failure | [feed 1/1][try 2/3] failed to get feed: Error: Request timed out after 5000ms | 1 | 1 |
| 43 | 🔴 failure | [feed 1/1][try 1/3] failed to get feed: Error: Request timed out after 5000ms | 1 | 1 |

---

### 🌐 GitHub Pages 線上發布門戶觀測 (GitHub Pages Deployments)

- **Pages 發布站點總數**：`17` 個站點
- **🟢 正常發布 (`built`)**：`15` 個
- **🔴 建置異常 (`errored`)**：`2` 個
- **⚪ 其他/初始待命中 (`other`)**：`0` 個

| # | 組織 / 儲存庫 | UX 意象與定位 (UX-Deck) | Pages 線上網址 | 建置狀態 | 建置管道 | 可見性 |
|---|---|---|---|:---:|:---:|:---:|
| 1 | [wenchiehlee/Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | 📊 觀測航線 (`全端點流量遙測中樞`) | [https://wenchiehlee.github.io/Analytics-Deck/](https://wenchiehlee.github.io/Analytics-Deck/) | 🔴 異常 (errored) | `workflow` | 🌍 公開 |
| 2 | [wenchiehlee/Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | ⚙️ 齒輪引擎 (`CI/CD 與自動化管道中樞`) | [https://wenchiehlee.github.io/Pipeline-Deck/](https://wenchiehlee.github.io/Pipeline-Deck/) | 🔴 異常 (errored) | `workflow` | 🌍 公開 |
| 3 | [wenchiehlee-investment/wenchiehlee-investment.github.io](https://github.com/wenchiehlee-investment/wenchiehlee-investment.github.io) | 💼 投資機構 (`投資組織官方入口`) | [https://wenchiehlee-investment.github.io/](https://wenchiehlee-investment.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 4 | [wenchiehlee-life/wenchiehlee-life.github.io](https://github.com/wenchiehlee-life/wenchiehlee-life.github.io) | 🌱 人文生活 (`生活組織官方門戶`) | [https://wenchiehlee-life.github.io/](https://wenchiehlee-life.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 5 | [wenchiehlee-money/GoogleAlertManager](https://github.com/wenchiehlee-money/GoogleAlertManager) | 🐦 破曉警報鳥 (`SaaS 情報過濾雷達`) | [https://wenchiehlee-money.github.io/GoogleAlertManager/](https://wenchiehlee-money.github.io/GoogleAlertManager/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 6 | [wenchiehlee-money/InvestorConference](https://github.com/wenchiehlee-money/InvestorConference) | 🦅 領航雄鷹 (`法人說明會與 IR 庫`) | [https://wenchiehlee-money.github.io/InvestorConference/](https://wenchiehlee-money.github.io/InvestorConference/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 7 | [wenchiehlee-money/My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | 🦉 拍拍翅萌萌鴞 (`台股個股深度調研`) | [https://wenchiehlee-money.github.io/My-TW-Coverage/](https://wenchiehlee-money.github.io/My-TW-Coverage/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 8 | [wenchiehlee-money/VIX](https://github.com/wenchiehlee-money/VIX) | 🦢 幾何黑天鵝 (`全球波動率黑天鵝雷達`) | [https://wenchiehlee-money.github.io/VIX/](https://wenchiehlee-money.github.io/VIX/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 9 | [wenchiehlee-ux/UX-Deck](https://github.com/wenchiehlee-ux/UX-Deck) | 🦌 幾何靈鹿 (`UX 設計系統中樞`) | [https://wenchiehlee-ux.github.io/UX-Deck/](https://wenchiehlee-ux.github.io/UX-Deck/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 10 | [wenchiehlee/dockers](https://github.com/wenchiehlee/dockers) | 🐳 貨櫃藍鯨 (`Docker 映像目錄與部署`) | [https://wenchiehlee.github.io/dockers/](https://wenchiehlee.github.io/dockers/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 11 | [wenchiehlee/mkdocs](https://github.com/wenchiehlee/mkdocs) | 📚 知識基底 (`工程技術文件中心`) | [https://wenchiehlee.github.io/mkdocs/](https://wenchiehlee.github.io/mkdocs/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 12 | [wenchiehlee/mkdocs-investment](https://github.com/wenchiehlee/mkdocs-investment) | 🐂🐻 幾何狂牛/守護熊 (`大盤資產配置與避險`) | [https://wenchiehlee.github.io/mkdocs-investment/](https://wenchiehlee.github.io/mkdocs-investment/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 13 | [wenchiehlee/mkdocs-life](https://github.com/wenchiehlee/mkdocs-life) | 🦌 幾何林鹿 (`溫潤人文生活誌`) | [https://wenchiehlee.github.io/mkdocs-life/](https://wenchiehlee.github.io/mkdocs-life/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 14 | [wenchiehlee/skills](https://github.com/wenchiehlee/skills) | 🐇 敏捷白兔 (`共享技能登錄庫`) | [https://wenchiehlee.github.io/skills/](https://wenchiehlee.github.io/skills/) | 🟢 正常 (built) | `workflow` | 🌍 公開 |
| 15 | [wenchiehlee/wenchiehlee.github.io](https://github.com/wenchiehlee/wenchiehlee.github.io) | 👤 個人旗艦 (`個人官方主站門戶`) | [https://wenchiehlee.github.io/](https://wenchiehlee.github.io/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 16 | [ZhongZheng782/Synology-Photo-Tagger](https://github.com/ZhongZheng782/Synology-Photo-Tagger) | 🐿️ 採集松鼠 (`AI 相片智慧標籤`) | [https://zhongzheng782.github.io/Synology-Photo-Tagger/](https://zhongzheng782.github.io/Synology-Photo-Tagger/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |
| 17 | [ZhongZheng782/YoutubeAudio.Fetch](https://github.com/ZhongZheng782/YoutubeAudio.Fetch) | 🐋 聲波座頭鯨 (`影音 Podcast 萃取`) | [https://zhongzheng782.github.io/YoutubeAudio.Fetch/](https://zhongzheng782.github.io/YoutubeAudio.Fetch/) | 🟢 正常 (built) | `legacy` | 🌍 公開 |

---

### 🛡️ 全域資安防護、Dependabot 與代碼品質觀測 (Security Posture & Code Quality)

- **秘密掃描防護 (Secret Scanning)**：`77` 個儲存庫啟用
- **阻擋推送防護 (Push Protection)**：`77` 個儲存庫啟用
- **Dependabot 自動安全修正**：`49` 個儲存庫啟用
- **Dependabot 待修復警報**：`2` 處（🔴 2 嚴重 · 🟠 0 高度 · 🟡 0 中度 · 🔵 0 低度）
- **CodeQL 代碼品質與安全漏洞**：`0` 處（🔴 0 嚴重 · 🟠 0 高度 · 🟡 0 中度 · 🔵 0 低度）
- **惡意代碼與外洩警報 (Malware / Leaks)**：`0` 處

#### ⚠️ 待處置資安警報與代碼品質儲存庫清單

| # | 組織 / 儲存庫 | Dependabot 警報 | CodeQL 漏洞 | 惡意代碼 | 嚴重等級分佈 (Crit/High/Med/Low) | 安全儀表板直達 |
|---|---|:---:|:---:|:---:|---|:---:|
| 1 | [wenchiehlee-investment/ConceptStocks](https://github.com/wenchiehlee-investment/ConceptStocks) | **1** | 0 | 0 | `🔴 1 · 🟠 0 · 🟡 0 · 🔵 0` | [Security ↗](https://github.com/wenchiehlee-investment/ConceptStocks/security) |
| 2 | [wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo) | **1** | 0 | 0 | `🔴 1 · 🟠 0 · 🟡 0 · 🔵 0` | [Security ↗](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo/security) |

---

### 📁 `ZhongZheng782` (20 個 Repo · 共 92 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [NASearch](https://github.com/ZhongZheng782/NASearch) | **16** | - | ⚪ 預設 | 0 | `check-extracted.yml`, `check-index-paths.yml`, `check-pst-duplicates.yml`, `eml-to-md.yml`, `fast-diagnostic.yml`, `fast-find.yml`, `fetch-summary.yml`, `find-pst.yml`, `full-find.yml`, `list-paths.yml`, `move-pst.yml`, `pst-convert.yml`, `run-and-print-scan.yml`, `scan-backup.yml`, `sync-report.yml`, `verify-converted.yml` |
| 2 | [Mac-mini](https://github.com/ZhongZheng782/Mac-mini) | **13** | - | ⚪ 預設 | 0 | `bench-params.yml`, `check-log.yml`, `check-python-arch.yml`, `deploy-mlx-api.yml`, `diagnose-ocr-network.yml`, `download-mlx-model.yml`, `eval-sample.yml`, `health-mlx-api.yml`, `rebuild-global-leaderboard.yml`, `run-pipeline.yml`, `setup-tailscale.yml`, `sync-gt-srt.yml`, `test-qwen3-thinking.yml` |
| 3 | [andy](https://github.com/ZhongZheng782/andy) | **10** | - | ⚪ 預設 | 0 | `action-runner.yml`, `calibrate-esc.yml`, `car-test.yml`, `diagnose-reverse.yml`, `runner-monitor.yml`, `setup-donkeycar-env.yml`, `setup-nginx-proxy.yml`, `setup-tailscale-funnel.yml`, `shutdown.yml`, `start-driving.yml` |
| 4 | [HomeAssistant](https://github.com/ZhongZheng782/HomeAssistant) | **10** | - | ⚪ 預設 | 0 | `check-ha-logs.yml`, `check-timetree.yml`, `configure-ha-hacs-xiaomi.yml`, `deploy-homeassistant-synology.yml`, `diagnose-lg-thinq.yml`, `diagnose-timetree-notify.yml`, `diagnose-washer-events.yml`, `update-uptimerobot-readme.yml`, `update-washer-readme.yml`, `update-xiaomi-miot-readme.yml` |
| 5 | [wenchiehlee.quickconnect.to](https://github.com/ZhongZheng782/wenchiehlee.quickconnect.to) | **8** | - | ⚪ 預設 | 0 | `action-runner.yml`, `mkdocs-deploy-synology.yml`, `reboot.yml`, `setup-nas-reverse-proxy.yml`, `setup-tailscale-funnel.yml`, `sync-ddns-table.yml`, `sync-nginx-conf.yml`, `update-uptimerobot-readme.yml` |
| 6 | [wenchiehlee.quickconnect.to-Container.Manager](https://github.com/ZhongZheng782/wenchiehlee.quickconnect.to-Container.Manager) | **5** | - | ⚪ 預設 | 0 | `actions.yml`, `authorize-ssh-key.yml`, `connect-cdp-net.yml`, `deploy-on-change.yml`, `deploy.yml` |
| 7 | [Llm-Cli-APIServer](https://github.com/ZhongZheng782/Llm-Cli-APIServer) | **4** | - | ⚪ 預設 | 0 | `deploy-synology-nas.yml`, `docker-publish.yml`, `stop-nas.yml`, `update-stats.yml` |
| 8 | [Synology-Photo-Tagger](https://github.com/ZhongZheng782/Synology-Photo-Tagger) | **4** | [🟢 built](https://zhongzheng782.github.io/Synology-Photo-Tagger/) | 🛡️ 啟用 | 0 | `probe-synology-photos-api.yml`, `probe-tailnet-mlx.yml`, `publish-image.yml`, `scout-image.yml` |
| 9 | [Yahoo.Finance](https://github.com/ZhongZheng782/Yahoo.Finance) | **4** | - | 🛡️ 啟用 | 0 | `Actions-fetch-wayback.yaml`, `Actions-fetch.yaml`, `Actions-update-lists.yaml`, `sync-up-forecast.yml` |
| 10 | [YoutubeAudio.Fetch](https://github.com/ZhongZheng782/YoutubeAudio.Fetch) | **4** | [🟢 built](https://zhongzheng782.github.io/YoutubeAudio.Fetch/) | 🛡️ 啟用 | 0 | `daily-channel-fetch.yml`, `sync-to-biztrends.yml`, `update-readme-index.yml`, `update-source-settings.yml` |
| 11 | [LineMonitoring](https://github.com/ZhongZheng782/LineMonitoring) | **3** | - | ⚪ 預設 | 0 | `collect-line-bot-logs.yml`, `deploy-synology-nas.yml`, `mac-runner-smoke.yml` |
| 12 | [Python-Actions.GoodInfo.Analyzer](https://github.com/ZhongZheng782/Python-Actions.GoodInfo.Analyzer) | **2** | - | ⚪ 預設 | 0 | `hybrid-fetch-and-analyze.yml`, `sync.yaml` |
| 13 | [Win11](https://github.com/ZhongZheng782/Win11) | **2** | - | 🛡️ 啟用 | 0 | `action-runner.yml`, `powershell.yml` |
| 14 | [AI-Usage](https://github.com/ZhongZheng782/AI-Usage) | **1** | - | ⚪ 預設 | 0 | `update-usage.yml` |
| 15 | [FamilyHealthyCheck](https://github.com/ZhongZheng782/FamilyHealthyCheck) | **1** | - | ⚪ 預設 | 0 | `daily-health-check.yml` |
| 16 | [GoogleAnalytics](https://github.com/ZhongZheng782/GoogleAnalytics) | **1** | - | ⚪ 預設 | 0 | `daily-ga-monitor.yml` |
| 17 | [GoPublic](https://github.com/ZhongZheng782/GoPublic) | **1** | - | 🛡️ 啟用 | 0 | `sync-up.yml` |
| 18 | [Mail-Deck](https://github.com/ZhongZheng782/Mail-Deck) | **1** | - | ⚪ 預設 | 0 | `mail-portal-deploy-synology.yml` |
| 19 | [Photo-Deck](https://github.com/ZhongZheng782/Photo-Deck) | **1** | - | ⚪ 預設 | 0 | `photo-portal-deploy-synology.yml` |
| 20 | [TravelAPP](https://github.com/ZhongZheng782/TravelAPP) | **1** | - | ⚪ 預設 | 0 | `deploy-synology-nas.yml` |
| - | *其餘 11 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee` (30 個 Repo · 共 67 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [GoogleSearch.Factset](https://github.com/wenchiehlee/GoogleSearch.Factset) | **7** | - | 🛡️ 啟用 | 0 | `Actions-process.yaml`, `Actions-quarantine-files.yaml`, `Actions-search.yaml`, `Actions-update-lists.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 2 | [gsheet.action](https://github.com/wenchiehlee/gsheet.action) | **3** | - | 🛡️ 啟用 | 0 | `e2e.yml`, `semantic-release.yml`, `test-and-release.yml` |
| 3 | [mcp-cli](https://github.com/wenchiehlee/mcp-cli) | **3** | - | 🛡️ 啟用 | 0 | `ci.yml`, `npm-publish.yml`, `release.yml` |
| 4 | [mkdocs](https://github.com/wenchiehlee/mkdocs) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs/) | 🛡️ 啟用 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 5 | [mkdocs-investment](https://github.com/wenchiehlee/mkdocs-investment) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs-investment/) | 🛡️ 啟用 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 6 | [mkdocs-life](https://github.com/wenchiehlee/mkdocs-life) | **3** | [🟢 built](https://wenchiehlee.github.io/mkdocs-life/) | 🛡️ 啟用 | 0 | `mkdocs-deploy-gh-pages.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 7 | [Python-Actions.FinMind](https://github.com/wenchiehlee/Python-Actions.FinMind) | **3** | - | 🛡️ 啟用 | 0 | `daily-finmind-status.yml`, `sync-to-biztrends.yml`, `sync-up-配置檔案.yml` |
| 8 | [Python-Actions.OpenAI](https://github.com/wenchiehlee/Python-Actions.OpenAI) | **3** | - | 🛡️ 啟用 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 9 | [Python-Actions.OpenAPI](https://github.com/wenchiehlee/Python-Actions.OpenAPI) | **3** | - | 🛡️ 啟用 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 10 | [Python-Actions.PER](https://github.com/wenchiehlee/Python-Actions.PER) | **3** | - | 🛡️ 啟用 | 0 | `Actions.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 11 | [rss2md](https://github.com/wenchiehlee/rss2md) | **3** | - | 🛡️ 啟用 | 0 | `rss2md.yml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 12 | [Selenium-Actions.Auction](https://github.com/wenchiehlee/Selenium-Actions.Auction) | **3** | - | 🛡️ 啟用 | 0 | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 13 | [Selenium-Actions.IPO](https://github.com/wenchiehlee/Selenium-Actions.IPO) | **3** | - | 🛡️ 啟用 | 0 | `Selenium-Action.yaml`, `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 14 | [skills](https://github.com/wenchiehlee/skills) | **3** | [🟢 built](https://wenchiehlee.github.io/skills/) | 🛡️ 啟用 | 0 | `deploy-pages.yml`, `publish-scribd-pdf-fetch.yml`, `update-skills-index.yml` |
| 15 | [twstock](https://github.com/wenchiehlee/twstock) | **3** | - | 🛡️ 啟用 | 0 | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml`, `twstock-Action.yaml` |
| 16 | [GoPublic](https://github.com/wenchiehlee/GoPublic) | **2** | - | 🛡️ 啟用 | 0 | `sync-up-名單清單.yml`, `sync-up-配置檔案.yml` |
| 17 | [whisper](https://github.com/wenchiehlee/whisper) | **2** | - | 🛡️ 啟用 | 0 | `python-publish.yml`, `test.yml` |
| 18 | [wjlee-barco](https://github.com/wenchiehlee/wjlee-barco) | **2** | - | 🛡️ 啟用 | 0 | `WP-post-workflow.yml`, `blog-post-workflow.yml` |
| 19 | [AI-Benchmark](https://github.com/wenchiehlee/AI-Benchmark) | **1** | - | 🛡️ 啟用 | 0 | `benchmark.yml` |
| 20 | [Analytics-Deck](https://github.com/wenchiehlee/Analytics-Deck) | **1** | [🔴 errored](https://wenchiehlee.github.io/Analytics-Deck/) | 🛡️ 啟用 | 0 | `renew-analytics.yml` |
| 21 | [chromium](https://github.com/wenchiehlee/chromium) | **1** | - | 🛡️ 啟用 | 0 | `docker-publish.yml` |
| 22 | [dockers](https://github.com/wenchiehlee/dockers) | **1** | [🟢 built](https://wenchiehlee.github.io/dockers/) | 🛡️ 啟用 | 0 | `deploy-pages.yml` |
| 23 | [influxdb-action](https://github.com/wenchiehlee/influxdb-action) | **1** | - | 🛡️ 啟用 | 0 | `action.yml` |
| 24 | [llm](https://github.com/wenchiehlee/llm) | **1** | - | 🛡️ 啟用 | 0 | `update-stats.yml` |
| 25 | [Pipeline-Deck](https://github.com/wenchiehlee/Pipeline-Deck) | **1** | [🔴 errored](https://wenchiehlee.github.io/Pipeline-Deck/) | 🛡️ 啟用 | 0 | `renew-pipeline-telemetry.yml` |
| 26 | [Python-Actions.ChatGPTAutomation](https://github.com/wenchiehlee/Python-Actions.ChatGPTAutomation) | **1** | - | 🛡️ 啟用 | 0 | `Actions.yaml` |
| 27 | [Python.TWSE-History](https://github.com/wenchiehlee/Python.TWSE-History) | **1** | - | 🛡️ 啟用 | 0 | `TWSE-API-Action.yaml` |
| 28 | [Selenium-Action.Goodinfo-Weekly](https://github.com/wenchiehlee/Selenium-Action.Goodinfo-Weekly) | **1** | - | ⚪ 預設 | 0 | `Selenium-Action_Template.yaml` |
| 29 | [shell_gpt](https://github.com/wenchiehlee/shell_gpt) | **1** | - | 🛡️ 啟用 | 0 | `lint_test.yml` |
| 30 | [wenchiehlee.github.io](https://github.com/wenchiehlee/wenchiehlee.github.io) | **1** | [🟢 built](https://wenchiehlee.github.io/) | 🛡️ 啟用 | 0 | `jekyll.yml` |
| - | *其餘 2 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-money` (11 個 Repo · 共 35 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [biztrends.TW](https://github.com/wenchiehlee-money/biztrends.TW) | **7** | - | ⚪ 預設 | 0 | `check-data-health.yml`, `refresh-cycle-mapping-monthly.yml`, `sync_to_GoogleSheet.Banks.yml`, `sync_to_TAIEX_centralized.yml`, `sync_to_gopublic.yml`, `update_combined_dividends.yml`, `update_indices.yml` |
| 2 | [InvestorConference](https://github.com/wenchiehlee-money/InvestorConference) | **7** | [🟢 built](https://wenchiehlee-money.github.io/InvestorConference/) | 🛡️ 啟用 | 0 | `daily-ingest.yml`, `deploy-web.yml`, `ingest.yml`, `sync-gt-to-mac-mini.yml`, `sync-to-downstream.yml`, `sync-yahoo-finance-consensus.yml`, `test-fin-issues.yml` |
| 3 | [GoogleAlertManager](https://github.com/wenchiehlee-money/GoogleAlertManager) | **5** | [🟢 built](https://wenchiehlee-money.github.io/GoogleAlertManager/) | 🛡️ 啟用 | 0 | `analyze.yml`, `fetch.yml`, `issue-feedback.yml`, `sync-to-downstream.yml`, `test.yml` |
| 4 | [Facebook.Fetch](https://github.com/wenchiehlee-money/Facebook.Fetch) | **4** | - | 🛡️ 啟用 | 0 | `add-group-handler.yml`, `daily_fetch.yml`, `sync-to-biztrends.yml`, `tag-link-injector.yml` |
| 5 | [diagram-design](https://github.com/wenchiehlee-money/diagram-design) | **3** | - | 🛡️ 啟用 | 0 | `auto-bump.yml`, `ci.yml`, `pages.yml` |
| 6 | [My-TW-Coverage](https://github.com/wenchiehlee-money/My-TW-Coverage) | **3** | [🟢 built](https://wenchiehlee-money.github.io/My-TW-Coverage/) | 🛡️ 啟用 | 0 | `daily_update.yml`, `pages.yml`, `sync_to_googlealertmanager.yml` |
| 7 | [VIX](https://github.com/wenchiehlee-money/VIX) | **2** | [🟢 built](https://wenchiehlee-money.github.io/VIX/) | 🛡️ 啟用 | 0 | `sync.yml`, `update-vix-data.yml` |
| 8 | [AI-Benchmark](https://github.com/wenchiehlee-money/AI-Benchmark) | **1** | - | 🛡️ 啟用 | 0 | `benchmark.yml` |
| 9 | [local-workspace-mcp](https://github.com/wenchiehlee-money/local-workspace-mcp) | **1** | - | 🛡️ 啟用 | 0 | `test.yml` |
| 10 | [skills](https://github.com/wenchiehlee-money/skills) | **1** | - | 🛡️ 啟用 | 0 | `update-skills-index.yml` |
| 11 | [TaiwanLifeInsurance](https://github.com/wenchiehlee-money/TaiwanLifeInsurance) | **1** | - | 🛡️ 啟用 | 0 | `sync-to-biztrends.yml` |
| - | *其餘 14 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-investment` (12 個 Repo · 共 29 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [InvestorEvents](https://github.com/wenchiehlee-investment/InvestorEvents) | **5** | - | 🛡️ 啟用 | 0 | `monthly-event-catalogs.yml`, `sync-to-Downstream.yml`, `sync-to-biztrends.yml`, `weekly-dividends.yml`, `weekly-earnings.yml` |
| 2 | [ConceptStocks](https://github.com/wenchiehlee-investment/ConceptStocks) | **4** | - | 🛡️ 啟用 | ⚠️ **1** | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update_company_financials.yml`, `update_conceptstocks.yml` |
| 3 | [Gemini-CLI](https://github.com/wenchiehlee-investment/Gemini-CLI) | **3** | - | 🛡️ 啟用 | 0 | `check_quota.yml`, `manual_scripts.yml`, `stock_events.yml` |
| 4 | [ic.tpex.org.tw](https://github.com/wenchiehlee-investment/ic.tpex.org.tw) | **3** | - | 🛡️ 啟用 | 0 | `sync-to-Analyzer.yml`, `sync-to-biztrends.yml`, `update-supply-chain.yml` |
| 5 | [MOPS](https://github.com/wenchiehlee-investment/MOPS) | **3** | - | 🛡️ 啟用 | 0 | `Download.yaml`, `EarlyFilerDownload.yaml`, `sync-to-Downstream.yml` |
| 6 | [Python-Actions.GoodInfo.CompanyInfo](https://github.com/wenchiehlee-investment/Python-Actions.GoodInfo.CompanyInfo) | **3** | - | 🛡️ 啟用 | ⚠️ **1** | `Actions.yaml`, `sync-to-Analyzer.yml`, `sync-to-biztrends.yml` |
| 7 | [GoodInfo.Test](https://github.com/wenchiehlee-investment/GoodInfo.Test) | **2** | - | 🛡️ 啟用 | 0 | `hybrid-cdp-pipeline.yml`, `test-actions-cdp.yml` |
| 8 | [TaiwanHouse](https://github.com/wenchiehlee-investment/TaiwanHouse) | **2** | - | 🛡️ 啟用 | 0 | `monthly_update.yml`, `sync-to-biztrends.yml` |
| 9 | [MarketCostDistribution](https://github.com/wenchiehlee-investment/MarketCostDistribution) | **1** | - | 🛡️ 啟用 | 0 | `sync-outputs.yml` |
| 10 | [poorstock](https://github.com/wenchiehlee-investment/poorstock) | **1** | - | 🛡️ 啟用 | 0 | `Actions.yaml` |
| 11 | [TAIFEX](https://github.com/wenchiehlee-investment/TAIFEX) | **1** | - | 🛡️ 啟用 | 0 | `fetch-taifex.yml` |
| 12 | [TaiwanLoanInterest](https://github.com/wenchiehlee-investment/TaiwanLoanInterest) | **1** | - | 🛡️ 啟用 | 0 | `monthly-cbc-update.yaml` |
| - | *其餘 4 個 Repo* | 0 | - | - | - | *(無 Actions)* |

### 📁 `wenchiehlee-ux` (1 個 Repo · 共 1 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| 1 | [UX-Deck](https://github.com/wenchiehlee-ux/UX-Deck) | **1** | [🟢 built](https://wenchiehlee-ux.github.io/UX-Deck/) | 🛡️ 啟用 | 0 | `deploy-pages.yml` |

### 📁 `wenchiehlee-alert` (0 個 Repo · 共 0 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| - | *(目前尚無儲存庫)* | 0 | - | - | - | - |

### 📁 `wenchiehlee-life` (0 個 Repo · 共 0 個 YAML)

| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |
|---|---|:---:|:---:|:---:|:---:|---|
| - | *其餘 1 個 Repo* | 0 | - | - | - | *(無 Actions)* |

<!-- PIPELINE_SUMMARY_END -->