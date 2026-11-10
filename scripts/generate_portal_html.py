import json
from pathlib import Path
from datetime import datetime

ORG_AVATARS = {
    "ZhongZheng782": "🏛️",
    "wenchiehlee": "👤",
    "wenchiehlee-money": "📈",
    "wenchiehlee-investment": "💼",
    "wenchiehlee-ux": "🦌",
    "wenchiehlee-alert": "🚨",
    "wenchiehlee-life": "🌱",
}

def generate_portal_html(data: dict, index_html_path: Path):
    gen_dt = datetime.fromisoformat(data["generated_at"])
    utc_str = gen_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    taipei_hour = (gen_dt.hour + 8) % 24
    taipei_str = f"台北時間 {gen_dt.strftime('%Y-%m-%d')} {taipei_hour:02d}:{gen_dt.strftime('%M:%S')}"

    sch = data["scheduled_telemetry"]
    orgs = data["orgs"]
    total_orgs_count = len(orgs)

    crit_count = sch.get("critical_consecutive_4_count", 0)
    warn_count = sch.get("warning_consecutive_1_to_3_count", 0)
    healthy_count = sch.get("healthy_count", 0)
    monitored_schedules = sch.get("total_monitored_schedules", 0)

    ns_quartet = f"{data['total_workflows']} / {data['total_repos_with_actions']} / {crit_count} / {warn_count}"

    # Build Org Overview Rows
    org_rows_html = ""
    for org_name, org_info in orgs.items():
        avatar = ORG_AVATARS.get(org_name, "📁")
        t_repos = org_info["total_repos"]
        w_repos = org_info["repos_with_actions"]
        t_wfs = org_info["total_workflows"]
        pct = round(w_repos / t_repos * 100, 1) if t_repos > 0 else 0.0
        
        org_rows_html += f"""              <tr>
                <td>
                  <a href="https://github.com/{org_name}" target="_blank" rel="noopener noreferrer" class="table-org-link">
                    <span class="org-avatar">{avatar}</span> <strong>{org_name}</strong>
                  </a>
                </td>
                <td style="text-align: center;">{t_repos}</td>
                <td style="text-align: center;"><span class="badge-repo-count">{w_repos}</span></td>
                <td style="text-align: center;"><strong class="text-accent">{t_wfs}</strong></td>
                <td style="text-align: center;">
                  <div class="coverage-bar-wrap">
                    <div class="coverage-bar-track"><div class="coverage-bar-fill" style="width: {pct}%;"></div></div>
                    <span>{pct}%</span>
                  </div>
                </td>
              </tr>
"""

    total_pct = round(data['total_repos_with_actions'] / data['total_repos'] * 100, 1) if data['total_repos'] > 0 else 0.0

    # Build Critical Alerts Section if any
    crit_section_html = ""
    crit_list = sch.get("critical_alerts", [])
    if crit_list:
        crit_rows = ""
        for idx, item in enumerate(crit_list, 1):
            run_link = f'<a href="{item.get("latest_run_url")}" target="_blank" rel="noopener noreferrer" class="btn-table-action">Run ↗</a>' if item.get("latest_run_url") else "-"
            crit_rows += f"""                <tr>
                  <td>{idx}</td>
                  <td><a href="https://github.com/{item['repo']}" target="_blank" rel="noopener noreferrer" class="repo-inline-link">{item['repo']}</a></td>
                  <td><strong>{item['workflow_name']}</strong></td>
                  <td><code>{item['file']}</code></td>
                  <td style="text-align: center;"><span class="badge-status-crit">{item['consecutive_failures']} 次</span></td>
                  <td style="text-align: center;"><span class="status-run-icons">{item.get('recent_4_icons', '')}</span></td>
                  <td><code>{item.get('latest_run_at', '')[:19]}</code></td>
                  <td style="text-align: center;">{run_link}</td>
                </tr>
"""
        crit_section_html = f"""      <!-- CRITICAL ALERTS TABLE -->
      <div id="critical-alerts-container">
        <div class="table-card">
          <div class="table-card-head" style="background: #fef2f2; border-bottom: 1px solid #fecaca;">
            <div class="table-card-title" style="color: #991b1b;">🚨 嚴重警報：常態排程連續失敗 ≥ 4 次清單</div>
            <span class="table-hint">需優先介入排查修復</span>
          </div>
          <div class="table-responsive">
            <table class="telemetry-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>儲存庫</th>
                  <th>工作流程名稱</th>
                  <th>YAML 檔案</th>
                  <th style="text-align: center;">連續失敗次數</th>
                  <th style="text-align: center;">最近 4 次狀態</th>
                  <th>最新失敗時間 (UTC)</th>
                  <th style="text-align: center;">執行日誌</th>
                </tr>
              </thead>
              <tbody id="critical-alerts-tbody">
{crit_rows}              </tbody>
            </table>
          </div>
        </div>
      </div>
"""

    # Build Warning Alerts Section if any
    warn_section_html = ""
    warn_list = sch.get("warning_alerts", [])
    if warn_list:
        warn_rows = ""
        for idx, item in enumerate(warn_list, 1):
            run_link = f'<a href="{item.get("latest_run_url")}" target="_blank" rel="noopener noreferrer" class="btn-table-action">Run ↗</a>' if item.get("latest_run_url") else "-"
            warn_rows += f"""                <tr>
                  <td>{idx}</td>
                  <td><a href="https://github.com/{item['repo']}" target="_blank" rel="noopener noreferrer" class="repo-inline-link">{item['repo']}</a></td>
                  <td><strong>{item['workflow_name']}</strong></td>
                  <td><code>{item['file']}</code></td>
                  <td style="text-align: center;"><span class="badge-status-warn">{item['consecutive_failures']} 次</span></td>
                  <td style="text-align: center;"><span class="status-run-icons">{item.get('recent_4_icons', '')}</span></td>
                  <td><code>{item.get('latest_run_at', '')[:19]}</code></td>
                  <td style="text-align: center;">{run_link}</td>
                </tr>
"""
        warn_section_html = f"""      <!-- WARNING ALERTS TABLE -->
      <div id="warning-alerts-container">
        <div class="table-card">
          <div class="table-card-head warning-head">
            <div class="table-card-title">⚠️ 異常警告：常態排程最新一次失敗（連續失敗 1~3 次）</div>
            <span class="table-hint">可點擊右側 Run 連結查看詳細失敗日誌</span>
          </div>
          <div class="table-responsive">
            <table class="telemetry-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>儲存庫</th>
                  <th>工作流程名稱</th>
                  <th>YAML 檔案</th>
                  <th style="text-align: center;">連續失敗次數</th>
                  <th style="text-align: center;">最近 4 次狀態</th>
                  <th>最新失敗時間 (UTC)</th>
                  <th style="text-align: center;">執行日誌</th>
                </tr>
              </thead>
              <tbody id="warning-alerts-tbody">
{warn_rows}              </tbody>
            </table>
          </div>
        </div>
      </div>
"""
    else:
        warn_section_html = """      <!-- NO WARNING ALERTS BANNER -->
      <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 12px 18px; margin-bottom: 1.5rem; color: #065f46; font-size: 0.95rem; font-weight: 500; display: flex; align-items: center; gap: 8px;">
        <span>✅</span> <strong>目前全域常態排程運作狀態良好，無任何連續失敗管道。</strong>
      </div>
"""

    # Build Healthy Schedules Rows
    healthy_rows = ""
    for idx, item in enumerate(sch.get("healthy_workflows", []), 1):
        clean_time = item.get('latest_run_at', '').replace('Z', '')[:19]
        healthy_rows += f"""                <tr>
                  <td>{idx}</td>
                  <td><a href="https://github.com/{item['repo']}" target="_blank" rel="noopener noreferrer" class="repo-inline-link">{item['repo']}</a></td>
                  <td><strong>{item['workflow_name']}</strong></td>
                  <td><code>{item['file']}</code></td>
                  <td style="text-align: center;"><span class="badge-status-ok">🟢 正常</span></td>
                  <td style="text-align: center;"><span class="status-run-icons">{item.get('recent_4_icons', '')}</span></td>
                  <td><code>{clean_time}</code></td>
                  <td style="text-align: center;"><a href="{item.get('latest_run_url', '#')}" target="_blank" rel="noopener noreferrer" class="btn-table-action">Run ↗</a></td>
                </tr>
"""

    # Build Org Nav Tabs
    org_nav_tabs_html = f'<button class="org-tab active" data-org="all">全部組織 ({data["total_repos_with_actions"]} Repos · {data["total_workflows"]} YAMLs)</button>\n'
    for org_name, org_info in orgs.items():
        org_nav_tabs_html += f'        <button class="org-tab" data-org="{org_name}">{org_name} ({org_info["repos_with_actions"]} Repos · {org_info["total_workflows"]} YAMLs)</button>\n'

    # Build Org Repo Cards
    repo_cards_html = ""
    for org_name, org_info in orgs.items():
        active_repos = [r for r in org_info["repos"] if r["workflow_count"] > 0]
        for r in active_repos:
            repo_name = r["name"]
            full_name = r["full_name"]
            html_url = r["html_url"]
            wf_count = r["workflow_count"]
            wfs = r["workflows"]
            
            tags_html = ""
            for wf in wfs:
                wf_url = f"{html_url}/blob/main/.github/workflows/{wf}"
                tags_html += f'<a href="{wf_url}" target="_blank" rel="noopener noreferrer" class="workflow-tag"><span>📄</span> {wf}</a>\n'
            
            repo_cards_html += f"""        <div class="org-repo-card" data-org="{org_name}" data-repo="{repo_name.lower()}" data-workflows="{','.join(wfs).lower()}">
          <div class="org-repo-header">
            <a href="{html_url}" target="_blank" rel="noopener noreferrer" class="org-repo-title">
              <span>📦</span> {full_name}
            </a>
            <span class="org-repo-badge">{wf_count} YAML</span>
          </div>
          <div class="org-workflow-tags">
            {tags_html}
          </div>
        </div>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pipeline-Deck · 全域自動化管道與 GitOps 工作流中樞 ({ns_quartet})</title>
  
  <!-- Pipeline-Deck ⚙️ Tone-Matched Favicon -->
  <link rel="icon" type="image/svg+xml" href="./favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="./favicon.png">
  <link rel="shortcut icon" href="./favicon.ico">

  <!-- Google Fonts (Exact UX-Deck Typography Stack) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=LXGW+WenKai+TC:wght@300;400;700&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Quicksand:wght@500;600;700&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">

  <!-- Global site tag (gtag.js) - Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-913Z6DSVD2"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-913Z6DSVD2');
  </script>

  <style>
    :root {{
      --bg-studio: #ffffff;
      --bg-subtle: #fbfbfe;
      --bg-card: #ffffff;
      --border-light: #f1f1f5;
      --border-mid: #e5e7eb;
      --text-main: #1e1e2f;
      --text-muted: #4b5563;
      --text-dim: #6b7280;
      
      --accent-violet: #7c3aed;
      --accent-violet-light: #f5f3ff;
      --accent-blue: #2563eb;
      --accent-blue-light: #eff6ff;
      --accent-amber: #d97706;
      --accent-amber-light: #fffbeb;
      --accent-red: #dc2626;
      --accent-red-light: #fef2f2;
      --accent-emerald: #059669;
      --accent-emerald-light: #ecfdf5;

      --font-display: 'Plus Jakarta Sans', 'Noto Sans TC', sans-serif;
      --font-body: 'Inter', 'Noto Sans TC', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-studio);
      color: var(--text-main);
      font-family: var(--font-body);
      line-height: 1.55;
      padding: 2rem 1.25rem 4rem;
      -webkit-font-smoothing: antialiased;
    }}

    .container {{
      max-width: 1320px;
      margin: 0 auto;
    }}

    /* STUDIO HEADER */
    header {{
      margin-bottom: 2.5rem;
    }}

    .header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-violet);
      background: var(--accent-violet-light);
      border: 1px solid #ddd6fe;
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 0.85rem;
    }}

    h1 {{
      font-family: var(--font-display);
      font-size: 2.25rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: #0f172a;
      margin-bottom: 0.5rem;
    }}

    .subtitle {{
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 900px;
      line-height: 1.6;
      margin-bottom: 1.25rem;
    }}

    .telemetry-nav-strip {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
      margin-top: 1rem;
    }}

    .live-url-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent-blue);
      background: var(--accent-blue-light);
      border: 1px solid #bfdbfe;
      padding: 6px 14px;
      border-radius: 999px;
      text-decoration: none;
      transition: all 0.2s ease;
    }}

    .live-url-pill:hover {{
      background: #dbeafe;
      transform: translateY(-1px);
    }}

    .pill-pulse {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      display: inline-block;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
      70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    /* SECTION BLOCK */
    .section-block {{
      margin-bottom: 3.5rem;
    }}

    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid #f1f5f9;
      padding-bottom: 0.85rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .section-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .section-badge {{
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent-violet);
    }}

    .section-badge.badge-health {{
      color: var(--accent-red);
    }}

    .section-heading {{
      font-family: var(--font-display);
      font-size: 1.45rem;
      font-weight: 700;
      color: #0f172a;
    }}

    .telemetry-timestamp {{
      font-size: 0.82rem;
      font-family: var(--font-mono);
      color: var(--text-dim);
      background: #f8fafc;
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid #e2e8f0;
    }}

    .section-desc {{
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }}

    /* NORTH STAR HIGHLIGHT BANNER */
    .north-star-banner {{
      background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
      border: 1px solid #ddd6fe;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .north-star-title {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.05rem;
      font-weight: 700;
      color: #5b21b6;
    }}

    .north-star-values {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .north-star-chip {{
      background: #ffffff;
      border: 1px solid #c4b5fd;
      border-radius: 8px;
      padding: 6px 12px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .north-star-chip strong {{
      font-size: 1rem;
    }}

    /* KPI CARDS GRID */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }}

    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-mid);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      align-items: flex-start;
      gap: 14px;
      transition: all 0.2s ease;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
      border-color: #cbd5e1;
    }}

    .kpi-card.kpi-featured {{
      border-color: #c4b5fd;
      background: #fbfbfe;
    }}

    .kpi-icon-wrap {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.35rem;
      flex-shrink: 0;
    }}

    .kpi-body {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}

    .kpi-label {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .kpi-value {{
      font-family: var(--font-display);
      font-size: 1.85rem;
      font-weight: 800;
      line-height: 1.1;
      margin-top: 4px;
      letter-spacing: -0.02em;
    }}

    .kpi-unit {{
      font-size: 0.85rem;
      font-weight: 500;
      color: var(--text-dim);
      margin-left: 2px;
    }}

    .kpi-sub {{
      font-size: 0.78rem;
      color: var(--text-dim);
      margin-top: 4px;
    }}

    /* TABLES */
    .table-card {{
      background: #ffffff;
      border: 1px solid var(--border-mid);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1.75rem;
    }}

    .table-card-head {{
      background: #f8fafc;
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border-mid);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .table-card-head.warning-head {{
      background: #fffbeb;
      border-bottom: 1px solid #fde68a;
    }}

    .table-card-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .table-card-head.warning-head .table-card-title {{
      color: #92400e;
    }}

    .table-hint {{
      font-size: 0.78rem;
      color: var(--text-dim);
    }}

    .table-responsive {{
      overflow-x: auto;
    }}

    table.telemetry-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }}

    table.telemetry-table th {{
      background: #ffffff;
      color: var(--text-dim);
      font-weight: 600;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-mid);
      white-space: nowrap;
    }}

    table.telemetry-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }}

    table.telemetry-table tbody tr:hover {{
      background-color: #f8fafc;
    }}

    tr.table-total-row td {{
      background: #faf5ff;
      border-top: 2px solid #ddd6fe;
      border-bottom: none;
      font-weight: 700;
      color: #5b21b6;
    }}

    .table-org-link {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: #0f172a;
      text-decoration: none;
      font-weight: 600;
    }}

    .table-org-link:hover {{
      color: var(--accent-violet);
      text-decoration: underline;
    }}

    .org-avatar {{
      font-size: 1.1rem;
    }}

    .badge-repo-count {{
      display: inline-block;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid #dbeafe;
    }}

    .text-accent {{
      color: var(--accent-violet);
      font-family: var(--font-mono);
      font-weight: 700;
    }}

    .coverage-bar-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--text-dim);
    }}

    .coverage-bar-track {{
      flex: 1;
      height: 6px;
      background: #f1f5f9;
      border-radius: 999px;
      overflow: hidden;
      min-width: 60px;
    }}

    .coverage-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #7c3aed, #a855f7);
      border-radius: 999px;
    }}

    /* HEALTH BADGES & ICONS */
    .health-summary-pill-group {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .health-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid #e2e8f0;
      background: #ffffff;
    }}

    .health-pill.pill-total {{
      background: #f8fafc;
      color: #334155;
    }}

    .health-pill.pill-crit {{
      background: #fef2f2;
      border-color: #fecaca;
      color: #b91c1c;
    }}

    .health-pill.pill-warn {{
      background: #fffbeb;
      border-color: #fde68a;
      color: #b45309;
    }}

    .health-pill.pill-ok {{
      background: #ecfdf5;
      border-color: #a7f3d0;
      color: #047857;
    }}

    .badge-status-crit {{
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.75rem;
    }}

    .badge-status-warn {{
      background: #fffbeb;
      color: #d97706;
      border: 1px solid #fde68a;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.75rem;
    }}

    .badge-status-ok {{
      background: #ecfdf5;
      color: #059669;
      border: 1px solid #a7f3d0;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.75rem;
    }}

    .status-run-icons {{
      font-size: 0.95rem;
      letter-spacing: 2px;
    }}

    .repo-inline-link {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }}

    .repo-inline-link:hover {{
      text-decoration: underline;
    }}

    .btn-table-action {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      color: #334155;
      font-size: 0.75rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.15s ease;
    }}

    .btn-table-action:hover {{
      background: #e2e8f0;
      color: #0f172a;
    }}

    /* ACCORDION */
    details.healthy-accordion {{
      background: #ffffff;
      border: 1px solid var(--border-mid);
      border-radius: 12px;
      overflow: hidden;
    }}

    summary.healthy-summary {{
      padding: 1rem 1.25rem;
      background: #f8fafc;
      font-size: 0.92rem;
      font-weight: 700;
      color: #0f172a;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
      transition: background 0.2s ease;
    }}

    summary.healthy-summary:hover {{
      background: #f1f5f9;
    }}

    .badge-health-ok {{
      font-size: 0.75rem;
      background: #ecfdf5;
      color: #059669;
      border: 1px solid #a7f3d0;
      padding: 3px 10px;
      border-radius: 999px;
      font-weight: 700;
    }}

    .healthy-content {{
      border-top: 1px solid var(--border-mid);
    }}

    /* ORG EXPLORER & WORKFLOW TAGS */
    .org-nav-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 1.25rem;
    }}

    .org-tab {{
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      color: #475569;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .org-tab:hover {{
      background: #f8fafc;
      border-color: #94a3b8;
    }}

    .org-tab.active {{
      background: #7c3aed;
      border-color: #7c3aed;
      color: #ffffff;
    }}

    .org-search-wrap {{
      display: flex;
      gap: 12px;
      margin-bottom: 1.5rem;
      align-items: center;
    }}

    .search-box {{
      position: relative;
      display: flex;
      align-items: center;
    }}

    .search-box span {{
      position: absolute;
      left: 12px;
      color: #94a3b8;
      font-size: 0.9rem;
    }}

    .search-box input {{
      width: 100%;
      padding: 8px 12px 8px 36px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      font-size: 0.88rem;
      outline: none;
      transition: all 0.15s ease;
    }}

    .search-box input:focus {{
      border-color: #7c3aed;
      box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
    }}

    .org-search-stats {{
      font-size: 0.82rem;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }}

    .org-repos-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1.25rem;
    }}

    .org-repo-card {{
      background: #ffffff;
      border: 1px solid var(--border-mid);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.2s ease;
    }}

    .org-repo-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
      border-color: #cbd5e1;
    }}

    .org-repo-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }}

    .org-repo-title {{
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 700;
      color: #0f172a;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
      line-height: 1.3;
    }}

    .org-repo-title:hover {{
      color: #7c3aed;
      text-decoration: underline;
    }}

    .org-repo-badge {{
      background: #f5f3ff;
      border: 1px solid #ddd6fe;
      color: #6d28d9;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      flex-shrink: 0;
    }}

    .org-workflow-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .workflow-tag {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: 6px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      color: #475569;
      text-decoration: none;
      transition: all 0.15s ease;
    }}

    .workflow-tag:hover {{
      background: #ede9fe;
      border-color: #c4b5fd;
      color: #6d28d9;
    }}

    /* DECK FAMILY FOOTER */
    .deck-family-footer {{
      margin-top: 4rem;
      padding-top: 2.5rem;
      border-top: 1px solid #e2e8f0;
      background: #ffffff;
    }}

    .deck-family-header-strip {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .deck-family-title-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-display);
      font-weight: 800;
      font-size: 1.15rem;
      color: #0f172a;
    }}

    .deck-family-header-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: #6d28d9;
      background: #f5f3ff;
      border: 1px solid #ddd6fe;
      padding: 4px 12px;
      border-radius: 999px;
      font-family: var(--font-mono);
    }}

    .deck-cards-row {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 10px;
      margin-bottom: 2rem;
    }}

    @media (max-width: 1200px) {{
      .deck-cards-row {{
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      }}
    }}

    .deck-card {{
      background: #ffffff;
      border: 1px solid var(--border-mid);
      border-radius: 10px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .deck-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }}

    .deck-card-head {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .deck-avatar {{
      font-size: 1rem;
    }}

    .deck-card-title {{
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-weight: 700;
      color: #0f172a;
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .deck-tag {{
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 1px 5px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #475569;
    }}

    .deck-numbers-compact {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      padding: 6px;
      background: #f8fafc;
      border-radius: 6px;
      font-size: 0.72rem;
    }}

    .stat-line {{
      display: flex;
      justify-content: space-between;
      color: var(--text-dim);
    }}

    .stat-val {{
      font-weight: 600;
      color: #1e293b;
      font-family: var(--font-mono);
    }}

    .deck-actions-compact {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      margin-top: auto;
    }}

    .deck-btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 4px;
      border-radius: 4px;
      text-decoration: none;
      transition: all 0.15s ease;
    }}

    .deck-btn svg {{
      width: 10px;
      height: 10px;
    }}

    .deck-btn-portal {{
      background: #2563eb;
      color: #ffffff;
      border: 1px solid #2563eb;
    }}

    .deck-btn-portal:hover {{
      background: #1d4ed8;
    }}

    .deck-btn-repo {{
      background: #ffffff;
      color: #334155;
      border: 1px solid #cbd5e1;
    }}

    .deck-btn-repo:hover {{
      background: #f1f5f9;
      color: #0f172a;
    }}

    .deck-card-bottom-line {{
      font-size: 0.68rem;
      font-family: var(--font-mono);
      color: var(--text-dim);
      text-align: center;
      border-top: 1px dashed #e2e8f0;
      padding-top: 4px;
    }}

    .deck-family-bottom-bar {{
      text-align: center;
      font-size: 0.82rem;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .deck-family-bottom-bar code {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #7c3aed;
      background: #f5f3ff;
      border: 1px solid #ddd6fe;
      padding: 1px 5px;
      border-radius: 4px;
    }}

    /* Studio Footer */
    footer.studio-footer {{
      margin-top: 3.5rem;
      border-top: 1px solid var(--border-light);
      padding-top: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      color: var(--text-dim);
      font-size: 0.85rem;
    }}

    footer.studio-footer a {{
      color: var(--accent-violet);
      text-decoration: none;
      font-weight: 600;
    }}
    footer.studio-footer a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>

  <div class="container">
    
    <!-- STUDIO HEADER -->
    <header>
      <div class="header-badge">⚙️ PIPELINE-DECK UNIFIED AUTOMATION ENGINE · GITOPS & CI/CD</div>
      <h1>Pipeline-Deck</h1>
      <div class="subtitle">
        跨生態系 {total_orgs_count} 大核心組織、{data['total_repos_with_actions']} 個活躍儲存庫、{data['total_workflows']} 個工作流程 YAML 與 {monitored_schedules} 個常態排程之全域觀測中樞。落實全域自動化排程定時快照、連續失敗警示與零延遲靜態門戶部署。
      </div>

      <div class="telemetry-nav-strip">
        <span class="live-url-pill" style="border-color: #c4b5fd; background: #faf5ff; color: #5b21b6; font-weight: 700;">
          <span class="pill-pulse"></span> 北極星核心指標 (North Star)：{ns_quartet}
        </span>
        <a href="#ecosystem-telemetry" class="live-url-pill" title="查看全域遙測統計">
          📊 全域遙測統計 ⬇
        </a>
        <a href="#schedule-health" class="live-url-pill" title="查看常態排程健康度監控">
          🚨 排程健康監控 ⬇
        </a>
        <a href="#org-explorer" class="live-url-pill" title="查看 {total_orgs_count} 大組織工作流探索">
          📁 {total_orgs_count} 大組織工作流 ⬇
        </a>
        <a href="#deck-family" class="live-url-pill" style="border-color: #c4b5fd; background: #faf5ff; color: #6d28d9;" title="直接前往底部 7 大 Deck 家族導航卡片 ⬇">
          🦌🐇📊⚙️📈🧠🐳 7 大 Deck 家族 ⬇
        </a>
        <a href="https://github.com/wenchiehlee/Pipeline-Deck" target="_blank" rel="noopener noreferrer" class="live-url-pill" title="前往 GitHub 原始庫 ↗">
          📦 GitHub 原始庫 ↗
        </a>
      </div>
    </header>

    <!-- SECTION 1: 🌐 全域工作流程遙測統計 (Ecosystem Actions Telemetry) -->
    <section id="ecosystem-telemetry" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge">ECOSYSTEM TELEMETRY</div>
          <h2 class="section-heading">🌐 全域工作流程遙測統計 (Ecosystem Actions Telemetry)</h2>
        </div>
        <div class="telemetry-timestamp" id="telemetry-timestamp">
          🕒 自動掃描更新：{utc_str} ({taipei_str})
        </div>
      </div>
      <p class="section-desc">
        全域統計涵蓋 <strong>{total_orgs_count} 大核心組織</strong>，共有 <strong>{data['total_repos']} 個儲存庫</strong>，其中 <strong>{data['total_repos_with_actions']} 個儲存庫</strong> 具備自動化工作流，累計運行 <strong>{data['total_workflows']} 個工作流程 YAML 檔案</strong>。
      </p>

      <!-- NORTH STAR QUARTET HIGHLIGHT BANNER -->
      <div class="north-star-banner">
        <div class="north-star-title">
          <span>🎯</span> <strong>Pipeline-Deck 核心維運指標 (North Star Quartet: {ns_quartet})</strong>
        </div>
        <div class="north-star-values">
          <div class="north-star-chip"><span style="color: #7c3aed;">⚡ 工作流</span> <strong style="color: #7c3aed;">{data['total_workflows']}</strong> YAMLs</div>
          <div class="north-star-chip"><span style="color: #2563eb;">📦 活躍庫</span> <strong style="color: #2563eb;">{data['total_repos_with_actions']}</strong> Repos</div>
          <div class="north-star-chip" style="border-color: #a7f3d0; background: #ecfdf5;"><span style="color: #059669;">🚨 嚴重警報</span> <strong style="color: #059669;">{crit_count}</strong> 次 (≥4)</div>
          <div class="north-star-chip" style="border-color: #fde68a; background: #fffbeb;"><span style="color: #b45309;">⚠️ 異常警告</span> <strong style="color: #b45309;">{warn_count}</strong> 次 (1~3)</div>
        </div>
      </div>

      <!-- KPI METRICS GRID -->
      <div class="kpi-grid">
        <div class="kpi-card kpi-featured">
          <div class="kpi-icon-wrap" style="background: #f5f3ff; color: #7c3aed;">
            <span>⚡</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">全域工作流程 YAML (規模)</div>
            <div class="kpi-value" id="kpi-total-workflows" style="color: #7c3aed;">{data['total_workflows']} <span class="kpi-unit">個檔案</span></div>
            <div class="kpi-sub">北極星指標 ① · 跨 {total_orgs_count} 大組織 {data['total_repos_with_actions']} 個庫</div>
          </div>
        </div>
        <div class="kpi-card kpi-featured">
          <div class="kpi-icon-wrap" style="background: #eff6ff; color: #2563eb;">
            <span>📦</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">自動化儲存庫 (覆蓋率)</div>
            <div class="kpi-value" id="kpi-repo-coverage" style="color: #2563eb;">{data['total_repos_with_actions']} <span class="kpi-unit">/ {data['total_repos']} 庫</span></div>
            <div class="kpi-sub">全域自動化比例：<strong>{total_pct}%</strong></div>
          </div>
        </div>
        <div class="kpi-card" style="border-color: {'#a7f3d0' if crit_count == 0 else '#fecaca'};">
          <div class="kpi-icon-wrap" style="background: {'#ecfdf5' if crit_count == 0 else '#fef2f2'}; color: {'#059669' if crit_count == 0 else '#dc2626'};">
            <span>🚨</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">排程嚴重警報 (連續失敗≥4)</div>
            <div class="kpi-value" id="kpi-critical-failures" style="color: {'#059669' if crit_count == 0 else '#dc2626'};">{crit_count} <span class="kpi-unit">條管道</span></div>
            <div class="kpi-sub">{'常態健康無嚴重中斷' if crit_count == 0 else '需立即介入排查'}</div>
          </div>
        </div>
        <div class="kpi-card" style="border-color: {'#e2e8f0' if warn_count == 0 else '#fde68a'};">
          <div class="kpi-icon-wrap" style="background: {'#f8fafc' if warn_count == 0 else '#fffbeb'}; color: {'#64748b' if warn_count == 0 else '#d97706'};">
            <span>⚠️</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">排程異常警告 (連續失敗1~3)</div>
            <div class="kpi-value" id="kpi-warning-failures" style="color: {'#64748b' if warn_count == 0 else '#d97706'};">{warn_count} <span class="kpi-unit">條管道</span></div>
            <div class="kpi-sub">{'暫無早期失敗警示' if warn_count == 0 else '列入觀測持續追蹤'}</div>
          </div>
        </div>
      </div>

      <!-- ORGANIZATIONS BREAKDOWN TABLE -->
      <div class="table-card">
        <div class="table-card-head">
          <div class="table-card-title">📊 組織與工作流程總覽</div>
          <span class="table-hint">同源於 README.md 全域遙測統計表</span>
        </div>
        <div class="table-responsive">
          <table class="telemetry-table" id="org-overview-table">
            <thead>
              <tr>
                <th>組織 / 帳號 (<code>Owner</code>)</th>
                <th style="text-align: center;">儲存庫總數</th>
                <th style="text-align: center;">具備 Actions 庫數</th>
                <th style="text-align: center;">工作流程 YAML 總數</th>
                <th style="text-align: center;">Actions 覆蓋率</th>
              </tr>
            </thead>
            <tbody>
{org_rows_html}              <tr class="table-total-row">
                <td><strong>全域總計</strong></td>
                <td style="text-align: center;"><strong>{data['total_repos']}</strong></td>
                <td style="text-align: center;"><strong>{data['total_repos_with_actions']}</strong></td>
                <td style="text-align: center;"><strong>{data['total_workflows']} 個 YAML</strong></td>
                <td style="text-align: center;"><strong>{total_pct}%</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SECTION 2: 🚨 常態排程健康度與連續失敗監測 -->
    <section id="schedule-health" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge badge-health">SCHEDULE HEALTH MONITOR · {ns_quartet}</div>
          <h2 class="section-heading">🚨 常態排程健康度與連續失敗監測 (Scheduled Consecutive Failures)</h2>
        </div>
        <div class="health-summary-pill-group">
          <span class="health-pill pill-total">常態排程：<strong>{monitored_schedules}</strong></span>
          <span class="health-pill pill-crit" style="color: {'#059669' if crit_count == 0 else '#dc2626'}; background: {'#ecfdf5' if crit_count == 0 else '#fef2f2'}; border-color: {'#a7f3d0' if crit_count == 0 else '#fecaca'};">🚨 嚴重警報（≥4次）：<strong>{crit_count}</strong></span>
          <span class="health-pill pill-warn">⚠️ 異常警告（1~3次）：<strong>{warn_count}</strong></span>
          <span class="health-pill pill-ok">🟢 正常運行：<strong>{healthy_count}</strong></span>
        </div>
      </div>
      <p class="section-desc">
        針對生態系中配置有 <code>schedule: - cron:</code> 的常態工作流程，追蹤最新執行紀錄與連續失敗次數。連續失敗 ≥ 4 次標記為嚴重警報，連續失敗 1~3 次標記為異常警告。
      </p>

{crit_section_html}
{warn_section_html}
      <!-- HEALTHY WORKFLOWS ACCORDION -->
      <details class="healthy-accordion">
        <summary class="healthy-summary">
          <span>🟢 檢視全域 {healthy_count} 個正常運行排程工作流程清單 (點擊展開 / 收合)</span>
          <span class="badge-health-ok">{healthy_count} Healthy Schedules</span>
        </summary>
        <div class="healthy-content">
          <div class="table-responsive">
            <table class="telemetry-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>儲存庫</th>
                  <th>工作流程名稱</th>
                  <th>YAML 檔案</th>
                  <th style="text-align: center;">狀態</th>
                  <th style="text-align: center;">最近 4 次結論</th>
                  <th>最新成功時間 (UTC)</th>
                  <th style="text-align: center;">執行紀錄</th>
                </tr>
              </thead>
              <tbody id="healthy-schedules-tbody">
{healthy_rows}              </tbody>
            </table>
          </div>
        </div>
      </details>
    </section>

    <!-- SECTION 3: 📁 組織工作流清單探索 (Organization Workflows Explorer) -->
    <section id="org-explorer" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge">WORKFLOWS EXPLORER</div>
          <h2 class="section-heading">📁 {total_orgs_count} 大組織儲存庫與工作流程探索 (Organization Explorer)</h2>
        </div>
      </div>
      <p class="section-desc">
        依組織切換檢視個別儲存庫的所有 GitHub Actions 工作流程。點擊工作流程標籤可直接連往 GitHub 原始 YAML 代碼。
      </p>

      <div class="org-nav-tabs">
        {org_nav_tabs_html}      </div>

      <div class="org-search-wrap">
        <div class="search-box" style="flex: 1; max-width: 480px;">
          <span>🔍</span>
          <input type="text" id="org-workflow-search" placeholder="在 {data['total_repos_with_actions']} 個儲存庫與 {data['total_workflows']} 個工作流中搜尋 (例如：GoodInfo, docker, sync)...">
        </div>
        <div class="org-search-stats" id="org-filter-stats">顯示 {data['total_repos_with_actions']} 個儲存庫</div>
      </div>

      <!-- REPO CATALOG CARDS -->
      <div class="org-repos-grid" id="org-repos-grid">
{repo_cards_html}      </div>
    </section>

    <!-- DECK FAMILY FOOTER -->
    <footer id="deck-family" class="deck-family-footer">
      <div class="deck-family-header-strip">
        <div class="deck-family-title-wrap">
          <span>🦌🐇📊⚙️📈🧠🐳</span>
          <span>7 大 Deck 家族導航門戶</span>
        </div>
        <div class="deck-family-header-pill">
          <span>🌐</span>
          <span>Pipeline-Deck 全域維運指標：{ns_quartet}</span>
        </div>
      </div>

      <div class="deck-cards-row">
        <!-- 1. UX-Deck -->
        <article class="deck-card theme-ux">
          <div class="deck-card-head">
            <span class="deck-avatar">🦌</span>
            <span class="deck-card-title">UX-Deck</span>
            <span class="deck-tag">Design</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">吉祥物庫</span>
              <span class="stat-val">13 Mascots</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">中心端點</span>
              <span class="stat-val">9+ Hubs · AA</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee-ux.github.io/UX-Deck/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee-ux/UX-Deck" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 2. Skill-Deck -->
        <article class="deck-card theme-skill">
          <div class="deck-card-head">
            <span class="deck-avatar">🐇</span>
            <span class="deck-card-title">Skill-Deck</span>
            <span class="deck-tag">Registry</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">技能模組</span>
              <span class="stat-val">60+ Skills</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">即時索引</span>
              <span class="stat-val">Auto-Sync</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee.github.io/skills/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee/skills" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 3. Analytics-Deck -->
        <article class="deck-card theme-analytics">
          <div class="deck-card-head">
            <span class="deck-avatar">📊</span>
            <span class="deck-card-title">Analytics-Deck</span>
            <span class="deck-tag">Telemetry</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">總瀏覽量</span>
              <span class="stat-val">20.5k Views</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">觀測艙位</span>
              <span class="stat-val">13 Pods · 4x/D</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee.github.io/Analytics-Deck/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee/Analytics-Deck" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 4. Pipeline-Deck -->
        <article class="deck-card theme-pipeline" style="border-color: #c4b5fd; box-shadow: 0 0 0 1px #c4b5fd;">
          <div class="deck-card-head">
            <span class="deck-avatar">⚙️</span>
            <span class="deck-card-title">Pipeline-Deck</span>
            <span class="deck-tag">CI/CD</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">工作流程</span>
              <span class="stat-val">{data['total_workflows']} WFs · {data['total_repos_with_actions']} 庫</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">異常警報</span>
              <span class="stat-val">{crit_count} 嚴重 · {warn_count} 警告</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee.github.io/Pipeline-Deck/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal" style="background:#7c3aed; border-color:#7c3aed;">
              <span>Current</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="4"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee/Pipeline-Deck" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 5. Data-Deck -->
        <article class="deck-card theme-data">
          <div class="deck-card-head">
            <span class="deck-avatar">📈</span>
            <span class="deck-card-title">Data-Deck</span>
            <span class="deck-tag">Finance</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">市場產業</span>
              <span class="stat-val">34+ Sectors</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">數據管道</span>
              <span class="stat-val">FinMind & GoodInfo</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee-money.github.io/biztrends.TW/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee-money/biztrends.TW" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 6. Llm-Deck -->
        <article class="deck-card theme-llm">
          <div class="deck-card-head">
            <span class="deck-avatar">🧠</span>
            <span class="deck-card-title">Llm-Deck</span>
            <span class="deck-tag">Models</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">路由客戶端</span>
              <span class="stat-val">Multi-Provider</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">容錯機制</span>
              <span class="stat-val">Smart Fallback</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee.github.io/llm/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee/llm" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>

        <!-- 7. Docker-Deck -->
        <article class="deck-card theme-docker">
          <div class="deck-card-head">
            <span class="deck-avatar">🐳</span>
            <span class="deck-card-title">Docker-Deck</span>
            <span class="deck-tag">Images</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">容器鏡像</span>
              <span class="stat-val">Discovery Hub</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">部署引擎</span>
              <span class="stat-val">GHCR & Compose</span>
            </div>
          </div>
          <div class="deck-actions-compact">
            <a href="https://wenchiehlee.github.io/dockers/" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-portal">
              <span>Portal</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
            </a>
            <a href="https://github.com/wenchiehlee/dockers" target="_blank" rel="noopener noreferrer" class="deck-btn deck-btn-repo">
              <span>Repo</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
          </div>
          <div class="deck-card-bottom-line">
            <span>⚡ CI/CD:</span> <strong>{ns_quartet}</strong>
          </div>
        </article>
      </div>

      <div class="deck-family-bottom-bar">
        <span>⚙️ Pipeline-Deck 數據同步管道 · 定期全域快照：<code>0 0 * * * UTC</code> · 北極星核心指標：<code>{ns_quartet}</code></span>
      </div>
    </footer>

    <!-- STUDIO FOOTER -->
    <footer class="studio-footer">
      <div>Pipeline-Deck · 跨生態系 GitHub Actions 排程與自動化觀測中樞</div>
      <div>Designed with 💜 for Deck Family Observability · Powered by GitHub Pages</div>
    </footer>

  </div>

  <!-- EMBEDDED TELEMETRY & SCRIPTS -->
  <script>
    /* TELEMETRY_DATA_START */
    window.PIPELINE_TELEMETRY = """ + json.dumps(data, ensure_ascii=False) + """;
    /* TELEMETRY_DATA_END */

    // Org Explorer Filter & Search
    const orgTabs = document.querySelectorAll('.org-tab');
    const orgRepoCards = document.querySelectorAll('.org-repo-card');
    const orgSearchInput = document.getElementById('org-workflow-search');
    const orgFilterStats = document.getElementById('org-filter-stats');

    let currentOrg = 'all';
    let currentOrgSearch = '';

    function applyOrgFilterAndSearch() {
      let visibleCount = 0;
      orgRepoCards.forEach(card => {
        const org = card.dataset.org;
        const repoName = card.dataset.repo || '';
        const workflows = card.dataset.workflows || '';
        const matchesOrg = (currentOrg === 'all' || org === currentOrg);
        const matchesSearch = (!currentOrgSearch || repoName.includes(currentOrgSearch) || workflows.includes(currentOrgSearch));
        
        if (matchesOrg && matchesSearch) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });
      if (orgFilterStats) {
        orgFilterStats.textContent = `顯示 ${visibleCount} 個儲存庫`;
      }
    }

    orgTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        orgTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentOrg = tab.dataset.org;
        applyOrgFilterAndSearch();
      });
    });

    if (orgSearchInput) {
      orgSearchInput.addEventListener('input', (e) => {
        currentOrgSearch = e.target.value.trim().toLowerCase();
        applyOrgFilterAndSearch();
      });
    }

    // Dynamic Telemetry Fetch (real-time freshness sync)
    async function syncFreshTelemetry() {
      try {
        const resp = await fetch('data/pipeline_summary.json?t=' + Date.now());
        if (!resp.ok) return;
        const freshData = await resp.json();
        if (freshData && freshData.generated_at !== window.PIPELINE_TELEMETRY?.generated_at) {
          console.log("[Pipeline-Deck] Refreshed telemetry from data/pipeline_summary.json:", freshData.generated_at);
          window.PIPELINE_TELEMETRY = freshData;
        }
      } catch (err) {
        // Fallback gracefully to embedded data
      }
    }
    syncFreshTelemetry();
  </script>
</body>
</html>
"""
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Successfully generated portal HTML at {index_html_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    data_file = base_dir / "data" / "pipeline_summary.json"
    index_html = base_dir / "index.html"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            d = json.load(f)
        generate_portal_html(d, index_html)
