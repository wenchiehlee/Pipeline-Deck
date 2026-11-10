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
    pg = data.get("pages_telemetry", {})
    sec = data.get("security_telemetry", {})
    orgs = data["orgs"]
    total_orgs_count = len(orgs)

    crit_count = sch.get("critical_consecutive_4_count", 0)
    warn_count = sch.get("warning_consecutive_1_to_3_count", 0)
    healthy_count = sch.get("healthy_count", 0)
    monitored_schedules = sch.get("total_monitored_schedules", 0)

    total_sites = pg.get("total_sites", 0)
    built_sites = pg.get("built_sites", 0)
    errored_sites = pg.get("errored_sites", 0)
    other_sites = pg.get("other_sites", 0)

    sec_repos = sec.get("secret_scanning_enabled_count", 0)
    push_repos = sec.get("push_protection_enabled_count", 0)
    dep_alerts_total = sec.get("total_open_dependabot_alerts", 0)
    codeql_alerts_total = sec.get("total_open_codeql_alerts", 0)
    malware_alerts_total = sec.get("total_malware_alerts", 0)
    total_alerts = dep_alerts_total + codeql_alerts_total + malware_alerts_total

    dep_bd = sec.get("dependabot_breakdown", {})
    code_bd = sec.get("codeql_breakdown", {})

    ns_quartet = f"{data['total_workflows']} / {data['total_repos_with_actions']} / {crit_count} / {warn_count}"

    # Build Org Overview Rows
    org_rows_html = ""
    for org_name, org_info in orgs.items():
        avatar = ORG_AVATARS.get(org_name, "📁")
        t_repos = org_info["total_repos"]
        w_repos = org_info["repos_with_actions"]
        t_wfs = org_info["total_workflows"]
        pct = round(w_repos / t_repos * 100, 1) if t_repos > 0 else 0.0

        org_p = sum(1 for r in org_info["repos"] if r.get("pages", {}).get("enabled"))
        org_s = sum(1 for r in org_info["repos"] if r.get("security", {}).get("secret_scanning") == "enabled")
        org_a = sum(
            r.get("alerts", {}).get("dependabot", {}).get("total", 0) +
            r.get("alerts", {}).get("code_scanning", {}).get("total", 0)
            for r in org_info["repos"]
        )
        alert_cell = f'<span class="badge-status-warn">{org_a}</span>' if org_a > 0 else '<span style="color:#94a3b8;">0</span>'
        
        org_rows_html += f"""              <tr>
                <td>
                  <a href="https://github.com/{org_name}" target="_blank" rel="noopener noreferrer" class="table-org-link">
                    <span class="org-avatar">{avatar}</span> <strong>{org_name}</strong>
                  </a>
                </td>
                <td style="text-align: center;">{t_repos}</td>
                <td style="text-align: center;"><span class="badge-repo-count">{w_repos}</span></td>
                <td style="text-align: center;"><strong class="text-accent">{t_wfs}</strong></td>
                <td style="text-align: center;"><span class="badge-pages-count">{org_p}</span></td>
                <td style="text-align: center;"><span class="badge-sec-count">{org_s}</span></td>
                <td style="text-align: center;">{alert_cell}</td>
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

    # Build Pages Sites Rows
    pages_rows = ""
    for idx, s in enumerate(pg.get("sites", []), 1):
        st = s.get("status")
        if st == "built":
            st_pill = '<span class="badge-status-ok">🟢 正常發布 (built)</span>'
        elif st == "errored":
            st_pill = '<span class="badge-status-crit">🔴 建置異常 (errored)</span>'
        else:
            st_pill = f'<span class="badge-status-pending">⚪ {st or "待命"}</span>'

        url = s.get("url")
        url_link = f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="live-url-pill-sm"><span>🌐 訪問題站 ↗</span></a>' if url else '<span style="color:#94a3b8;">未生成</span>'
        vis_pill = '<span class="badge-vis private">🔒 私有</span>' if s.get("is_private") else '<span class="badge-vis public">🌍 公開</span>'
        build_type = s.get("build_type") or "legacy"

        pages_rows += f"""                <tr>
                  <td>{idx}</td>
                  <td><a href="https://github.com/{s['repo']}" target="_blank" rel="noopener noreferrer" class="repo-inline-link"><strong>{s['repo']}</strong></a></td>
                  <td>{url_link}</td>
                  <td style="text-align: center;">{st_pill}</td>
                  <td style="text-align: center;"><code>{build_type}</code></td>
                  <td style="text-align: center;">{vis_pill}</td>
                </tr>
"""

    # Build Security Alerts Rows
    sec_alert_rows = ""
    for idx, ra in enumerate(sec.get("repos_with_alerts", []), 1):
        dep_c = ra.get("dependabot_total", 0)
        code_c = ra.get("codeql_total", 0)
        mal_c = ra.get("malware_total", 0)
        tot = dep_c + code_c + mal_c

        crit_tot = ra["dependabot_breakdown"].get("critical", 0) + ra["codeql_breakdown"].get("critical", 0)
        high_tot = ra["dependabot_breakdown"].get("high", 0) + ra["codeql_breakdown"].get("high", 0)
        med_tot = ra["dependabot_breakdown"].get("medium", 0) + ra["codeql_breakdown"].get("medium", 0)
        low_tot = ra["dependabot_breakdown"].get("low", 0) + ra["codeql_breakdown"].get("low", 0)

        bd_badges = ""
        if crit_tot > 0:
            bd_badges += f'<span class="badge-sev crit">🔴 {crit_tot} Crit</span> '
        if high_tot > 0:
            bd_badges += f'<span class="badge-sev high">🟠 {high_tot} High</span> '
        if med_tot > 0:
            bd_badges += f'<span class="badge-sev med">🟡 {med_tot} Med</span> '
        if low_tot > 0:
            bd_badges += f'<span class="badge-sev low">🔵 {low_tot} Low</span> '

        sec_link = f'<a href="https://github.com/{ra["repo"]}/security" target="_blank" rel="noopener noreferrer" class="btn-table-action">Security ↗</a>'

        sec_alert_rows += f"""                <tr>
                  <td>{idx}</td>
                  <td><a href="https://github.com/{ra['repo']}" target="_blank" rel="noopener noreferrer" class="repo-inline-link"><strong>{ra['repo']}</strong></a></td>
                  <td style="text-align: center;"><span class="badge-total-alert"><strong>{tot}</strong> 處</span></td>
                  <td style="text-align: center;">{dep_c} 處</td>
                  <td style="text-align: center;">{code_c} 處</td>
                  <td style="text-align: center;">{mal_c} 處</td>
                  <td>{bd_badges}</td>
                  <td style="text-align: center;">{sec_link}</td>
                </tr>
"""

    # Build Org Nav Tabs
    org_nav_tabs_html = f'<button class="org-tab active" data-org="all">全部組織 ({data["total_repos_with_actions"]} Repos · {data["total_workflows"]} YAMLs)</button>\n'
    for org_name, org_info in orgs.items():
        org_nav_tabs_html += f'        <button class="org-tab" data-org="{org_name}">{org_name} ({org_info["repos_with_actions"]} Repos · {org_info["total_workflows"]} YAMLs)</button>\n'

    # Build Org Repo Cards
    repo_cards_html = ""
    for org_name, org_info in orgs.items():
        for r in org_info["repos"]:
            repo_name = r["name"]
            full_name = r["full_name"]
            html_url = r["html_url"]
            wf_count = r["workflow_count"]
            wfs = r["workflows"]

            # Badges
            pg_badge = ""
            if r.get("pages", {}).get("enabled"):
                pst = r.get("pages", {}).get("status")
                purl = r.get("pages", {}).get("url")
                if pst == "built":
                    pg_badge = f'<a href="{purl}" target="_blank" rel="noopener noreferrer" class="card-pill pages-built" title="點擊直接訪問 Pages 線上網站">🌐 Pages: Built ↗</a>'
                elif pst == "errored":
                    pg_badge = f'<a href="{purl}" target="_blank" rel="noopener noreferrer" class="card-pill pages-errored" title="Pages 建置異常">🔴 Pages: Errored ↗</a>'
                else:
                    pg_badge = f'<span class="card-pill pages-other" title="Pages 待命中">⚪ Pages: {pst or "On"}</span>'

            sec_badge = ""
            if r.get("security", {}).get("secret_scanning") == "enabled":
                sec_badge = '<span class="card-pill sec-active" title="Secret Scanning & Push Protection 啟用">🛡️ Sec: Active</span>'

            alert_badge = ""
            dep_c = r.get("alerts", {}).get("dependabot", {}).get("total", 0)
            code_c = r.get("alerts", {}).get("code_scanning", {}).get("total", 0)
            tot_a = dep_c + code_c
            if tot_a > 0:
                alert_badge = f'<a href="{html_url}/security" target="_blank" rel="noopener noreferrer" class="card-pill alert-active" title="點擊查看待修復安全警報">⚠️ {tot_a} Alerts</a>'

            tags_html = ""
            for wf in wfs:
                wf_url = f"{html_url}/blob/main/.github/workflows/{wf}"
                tags_html += f'<a href="{wf_url}" target="_blank" rel="noopener noreferrer" class="workflow-tag"><span>📄</span> {wf}</a>\n'

            has_pages_attr = "true" if r.get("pages", {}).get("enabled") else "false"
            has_alerts_attr = "true" if tot_a > 0 else "false"
            has_actions_attr = "true" if wf_count > 0 else "false"

            wf_count_badge = f'<span class="org-repo-badge">{wf_count} YAML</span>' if wf_count > 0 else '<span class="org-repo-badge no-wf">0 YAML</span>'

            repo_cards_html += f"""        <div class="org-repo-card" data-org="{org_name}" data-repo="{repo_name.lower()}" data-workflows="{','.join(wfs).lower()}" data-has-pages="{has_pages_attr}" data-has-alerts="{has_alerts_attr}" data-has-actions="{has_actions_attr}">
          <div class="org-repo-header">
            <a href="{html_url}" target="_blank" rel="noopener noreferrer" class="org-repo-title">
              <span>📦</span> {full_name}
            </a>
            {wf_count_badge}
          </div>
          <div class="repo-meta-badges">
            {pg_badge}
            {sec_badge}
            {alert_badge}
          </div>
          <div class="org-workflow-tags">
            {tags_html if tags_html else '<span class="no-workflows-hint">無工作流程 YAML 檔案</span>'}
          </div>
        </div>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pipeline-Deck · 全域自動化管道、發布門戶與資安遙測中樞 ({ns_quartet})</title>
  
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
      max-width: 950px;
      line-height: 1.6;
      margin-bottom: 1.25rem;
    }}

    .telemetry-nav-strip {{
      display: flex;
      gap: 10px;
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
    .section-badge.badge-pages {{
      color: var(--accent-blue);
    }}
    .section-badge.badge-sec {{
      color: #059669;
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
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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
      font-size: 1.75rem;
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

    .badge-pages-count {{
      display: inline-block;
      background: #eff6ff;
      color: #2563eb;
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid #bfdbfe;
    }}

    .badge-sec-count {{
      display: inline-block;
      background: #ecfdf5;
      color: #059669;
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid #a7f3d0;
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

    .badge-status-pending {{
      background: #f8fafc;
      color: #64748b;
      border: 1px solid #e2e8f0;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.75rem;
    }}

    .badge-vis {{
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .badge-vis.public {{
      background: #f0fdf4;
      color: #166534;
      border: 1px solid #bbf7d0;
    }}
    .badge-vis.private {{
      background: #fef2f2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }}

    .badge-total-alert {{
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.78rem;
    }}

    .badge-sev {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      margin-right: 4px;
      display: inline-block;
    }}
    .badge-sev.crit {{
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fecaca;
    }}
    .badge-sev.high {{
      background: #fff7ed;
      color: #c2410c;
      border: 1px solid #ffedd5;
    }}
    .badge-sev.med {{
      background: #fffbeb;
      color: #b45309;
      border: 1px solid #fef3c7;
    }}
    .badge-sev.low {{
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #dbeafe;
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

    .live-url-pill-sm {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 10px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 999px;
      color: #1d4ed8;
      font-size: 0.78rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.15s ease;
    }}
    .live-url-pill-sm:hover {{
      background: #dbeafe;
      transform: translateY(-1px);
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
      transition: all 0.2s ease;
    }}

    .org-tab:hover {{
      background: #f8fafc;
      border-color: #94a3b8;
    }}

    .org-tab.active {{
      background: var(--accent-violet);
      color: #ffffff;
      border-color: var(--accent-violet);
      box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
    }}

    .org-filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 1rem;
      align-items: center;
    }}

    .filter-pill {{
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid #e2e8f0;
      background: #f8fafc;
      color: #64748b;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .filter-pill:hover {{
      background: #e2e8f0;
      color: #1e293b;
    }}

    .filter-pill.active {{
      background: #334155;
      color: #ffffff;
      border-color: #334155;
    }}

    .org-search-wrap {{
      display: flex;
      gap: 12px;
      align-items: center;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
    }}

    .search-box {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 8px 12px;
      flex: 1;
      max-width: 480px;
      transition: border-color 0.2s ease;
    }}

    .search-box:focus-within {{
      border-color: var(--accent-violet);
      box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15);
    }}

    .search-box input {{
      border: none;
      outline: none;
      font-size: 0.88rem;
      width: 100%;
      color: #0f172a;
    }}

    .org-search-stats {{
      font-size: 0.85rem;
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
      padding: 1.15rem;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.2s ease;
    }}

    .org-repo-card:hover {{
      border-color: #cbd5e1;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
      transform: translateY(-2px);
    }}

    .org-repo-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }}

    .org-repo-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #0f172a;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      word-break: break-all;
    }}

    .org-repo-title:hover {{
      color: var(--accent-violet);
    }}

    .org-repo-badge {{
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
      padding: 2px 8px;
      border-radius: 999px;
      background: var(--accent-violet-light);
      color: var(--accent-violet);
      border: 1px solid #ddd6fe;
      white-space: nowrap;
    }}

    .org-repo-badge.no-wf {{
      background: #f8fafc;
      color: #94a3b8;
      border-color: #e2e8f0;
    }}

    .repo-meta-badges {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .card-pill {{
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}

    .card-pill.pages-built {{
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }}
    .card-pill.pages-built:hover {{
      background: #d1fae5;
    }}

    .card-pill.pages-errored {{
      background: #fef2f2;
      color: #991b1b;
      border: 1px solid #fecaca;
    }}
    .card-pill.pages-errored:hover {{
      background: #fee2e2;
    }}

    .card-pill.pages-other {{
      background: #f8fafc;
      color: #64748b;
      border: 1px solid #e2e8f0;
    }}

    .card-pill.sec-active {{
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
    }}

    .card-pill.alert-active {{
      background: #fffbeb;
      color: #b45309;
      border: 1px solid #fde68a;
    }}
    .card-pill.alert-active:hover {{
      background: #fef3c7;
    }}

    .org-workflow-tags {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 4px;
    }}

    .workflow-tag {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      color: #334155;
      font-size: 0.75rem;
      padding: 3px 8px;
      border-radius: 6px;
      text-decoration: none;
      font-family: var(--font-mono);
      transition: all 0.15s ease;
    }}

    .workflow-tag:hover {{
      background: #eff6ff;
      border-color: #bfdbfe;
      color: #1d4ed8;
    }}

    .no-workflows-hint {{
      font-size: 0.78rem;
      color: #94a3b8;
      font-style: italic;
    }}

    /* DECK FAMILY FOOTER */
    .deck-family-footer {{
      margin-top: 4rem;
      border-top: 2px solid #e2e8f0;
      padding-top: 2rem;
    }}

    .deck-family-header-strip {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .deck-family-title-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 1.15rem;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.01em;
    }}

    .deck-family-header-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8rem;
      color: #475569;
      background: #f8fafc;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid #e2e8f0;
      font-family: var(--font-mono);
    }}

    .deck-cards-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      margin-bottom: 1.5rem;
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
        跨生態系 {total_orgs_count} 大核心組織、{data['total_repos_with_actions']} 個活躍儲存庫、{data['total_workflows']} 個工作流程 YAML、{total_sites} 個 GitHub Pages 發布門戶，以及 {sec_repos} 庫全方位資安防護之全域觀測中樞。
      </div>

      <div class="telemetry-nav-strip">
        <span class="live-url-pill" style="border-color: #c4b5fd; background: #faf5ff; color: #5b21b6; font-weight: 700;">
          <span class="pill-pulse"></span> 北極星核心指標 (North Star)：{ns_quartet}
        </span>
        <a href="#ecosystem-telemetry" class="live-url-pill" title="查看全域遙測統計">
          📊 全域統計 ⬇
        </a>
        <a href="#schedule-health" class="live-url-pill" title="查看常態排程健康度監控">
          🚨 排程健康 ⬇
        </a>
        <a href="#pages-deployments" class="live-url-pill" title="查看 GitHub Pages 發布門戶">
          🌐 Pages 門戶 ({total_sites}) ⬇
        </a>
        <a href="#security-posture" class="live-url-pill" title="查看資安防護與代碼品質">
          🛡️ 資安與品質 ({total_alerts} 警報) ⬇
        </a>
        <a href="#org-explorer" class="live-url-pill" title="查看 {total_orgs_count} 大組織工作流探索">
          📁 組織探索 ⬇
        </a>
        <a href="#deck-family" class="live-url-pill" style="border-color: #c4b5fd; background: #faf5ff; color: #6d28d9;" title="前往底部 7 大 Deck 家族導航卡片 ⬇">
          🦌🐇📊⚙️📈🧠🐳 7 大 Deck ⬇
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
        全域統計涵蓋 <strong>{total_orgs_count} 大核心組織</strong>，共有 <strong>{data['total_repos']} 個活躍儲存庫</strong>，其中 <strong>{data['total_repos_with_actions']} 個儲存庫</strong> 具備自動化工作流，累計運行 <strong>{data['total_workflows']} 個工作流程 YAML 檔案</strong>、<strong>{total_sites} 個 GitHub Pages 發布門戶</strong> 與 <strong>{sec_repos} 個資安防護啟用庫</strong>。
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
            <div class="kpi-sub">北極星指標 ① · 跨 {total_orgs_count} 組織 {data['total_repos_with_actions']} 庫</div>
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
        <div class="kpi-card">
          <div class="kpi-icon-wrap" style="background: #eff6ff; color: #2563eb;">
            <span>🌐</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">GitHub Pages 線上發布門戶</div>
            <div class="kpi-value" style="color: #2563eb;">{total_sites} <span class="kpi-unit">個站點</span></div>
            <div class="kpi-sub">🟢 <strong>{built_sites}</strong> 正常 · 🔴 <strong>{errored_sites}</strong> 異常</div>
          </div>
        </div>
        <div class="kpi-card" style="border-color: {'#a7f3d0' if total_alerts == 0 else '#fde68a'};">
          <div class="kpi-icon-wrap" style="background: {'#ecfdf5' if total_alerts == 0 else '#fffbeb'}; color: {'#059669' if total_alerts == 0 else '#d97706'};">
            <span>🛡️</span>
          </div>
          <div class="kpi-body">
            <div class="kpi-label">資安防護與待處置警報</div>
            <div class="kpi-value" style="color: {'#059669' if total_alerts == 0 else '#d97706'};">{sec_repos} <span class="kpi-unit">庫啟用</span></div>
            <div class="kpi-sub">⚠️ <strong>{total_alerts}</strong> 處待修復 (0 惡意代碼)</div>
          </div>
        </div>
      </div>

      <!-- ORGANIZATIONS BREAKDOWN TABLE -->
      <div class="table-card">
        <div class="table-card-head">
          <div class="table-card-title">📊 組織工作流程、Pages 與資安分佈總覽</div>
          <span class="table-hint">同源於 README.md 全域遙測統計表</span>
        </div>
        <div class="table-responsive">
          <table class="telemetry-table" id="org-overview-table">
            <thead>
              <tr>
                <th>組織 / 帳號 (<code>Owner</code>)</th>
                <th style="text-align: center;">儲存庫總數</th>
                <th style="text-align: center;">具備 Actions 庫</th>
                <th style="text-align: center;">工作流程 YAML</th>
                <th style="text-align: center;">Pages 站點</th>
                <th style="text-align: center;">資安防護庫</th>
                <th style="text-align: center;">待處置警報</th>
                <th style="text-align: center;">Actions 覆蓋率</th>
              </tr>
            </thead>
            <tbody>
{org_rows_html}              <tr class="table-total-row">
                <td><strong>全域總計</strong></td>
                <td style="text-align: center;"><strong>{data['total_repos']}</strong></td>
                <td style="text-align: center;"><strong>{data['total_repos_with_actions']}</strong></td>
                <td style="text-align: center;"><strong>{data['total_workflows']} 個 YAML</strong></td>
                <td style="text-align: center;"><strong>{total_sites} 個</strong></td>
                <td style="text-align: center;"><strong>{sec_repos} 庫</strong></td>
                <td style="text-align: center;"><strong>{total_alerts} 處</strong></td>
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

    <!-- SECTION 3: 🌐 GitHub Pages 線上發布門戶觀測 -->
    <section id="pages-deployments" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge badge-pages">PAGES OBSERVABILITY · {total_sites} SITES</div>
          <h2 class="section-heading">🌐 GitHub Pages 線上發布門戶觀測 (GitHub Pages Deployments)</h2>
        </div>
        <div class="health-summary-pill-group">
          <span class="health-pill pill-total">Pages 站點總數：<strong>{total_sites}</strong></span>
          <span class="health-pill pill-ok">🟢 正常發布：<strong>{built_sites}</strong></span>
          <span class="health-pill pill-crit" style="color: {'#059669' if errored_sites == 0 else '#dc2626'}; background: {'#ecfdf5' if errored_sites == 0 else '#fef2f2'};">🔴 建置異常：<strong>{errored_sites}</strong></span>
          <span class="health-pill pill-total">⚪ 待命/初始：<strong>{other_sites}</strong></span>
        </div>
      </div>
      <p class="section-desc">
        全域跨組織即時監控 GitHub Pages 站點之部署健康狀態、線上公開網址以及建置引擎類型。
      </p>

      <div class="table-card">
        <div class="table-card-head">
          <div class="table-card-title">🌐 GitHub Pages 線上發布站點清單</div>
          <span class="table-hint">包含 Deck Family 與各專案即時門戶</span>
        </div>
        <div class="table-responsive">
          <table class="telemetry-table" id="pages-table">
            <thead>
              <tr>
                <th>#</th>
                <th>組織 / 儲存庫</th>
                <th>線上訪問題站</th>
                <th style="text-align: center;">建置狀態</th>
                <th style="text-align: center;">建置管道</th>
                <th style="text-align: center;">可見性</th>
              </tr>
            </thead>
            <tbody>
{pages_rows}            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SECTION 4: 🛡️ 全域資安防護、Dependabot 與代碼品質觀測 -->
    <section id="security-posture" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge badge-sec">SECURITY & CODE QUALITY · {total_alerts} ALERTS</div>
          <h2 class="section-heading">🛡️ 全域資安防護、Dependabot 與代碼品質觀測 (Security & Quality Posture)</h2>
        </div>
        <div class="health-summary-pill-group">
          <span class="health-pill pill-ok">🛡️ 防護啟用：<strong>{sec_repos}</strong> 庫</span>
          <span class="health-pill pill-warn">📦 Dependabot 警報：<strong>{dep_alerts_total}</strong> 處</span>
          <span class="health-pill pill-crit">🔍 CodeQL 漏洞：<strong>{codeql_alerts_total}</strong> 處</span>
          <span class="health-pill pill-ok">☣️ 惡意代碼：<strong>{malware_alerts_total}</strong> 處</span>
        </div>
      </div>
      <p class="section-desc">
        全面觀測 GitHub 秘密掃描 (Secret Scanning)、阻擋推送保護 (Push Protection)、Dependabot 自動安全更新與 CodeQL 靜態代碼分析 (SAST) 之落實情況。
      </p>

      <div class="table-card">
        <div class="table-card-head">
          <div class="table-card-title">⚠️ 待處置資安警報與代碼品質儲存庫清單 ({len(sec.get("repos_with_alerts", []))} 庫)</div>
          <span class="table-hint">點擊右側 Security ↗ 可直達 GitHub 官方安全面板</span>
        </div>
        <div class="table-responsive">
          <table class="telemetry-table" id="security-alerts-table">
            <thead>
              <tr>
                <th>#</th>
                <th>組織 / 儲存庫</th>
                <th style="text-align: center;">待處置總數</th>
                <th style="text-align: center;">Dependabot</th>
                <th style="text-align: center;">CodeQL</th>
                <th style="text-align: center;">惡意代碼</th>
                <th>嚴重等級分佈</th>
                <th style="text-align: center;">安全儀表板</th>
              </tr>
            </thead>
            <tbody>
{sec_alert_rows if sec_alert_rows else '<tr><td colspan="8" style="text-align:center; padding: 20px; color:#059669;">✅ 目前全域所有儲存庫無任何待處置安全漏洞！</td></tr>'}            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SECTION 5: 📁 組織工作流清單探索 (Organization Workflows Explorer) -->
    <section id="org-explorer" class="section-block">
      <div class="section-header">
        <div class="section-title-wrap">
          <div class="section-badge">WORKFLOWS & REPO EXPLORER</div>
          <h2 class="section-heading">📁 {total_orgs_count} 大組織儲存庫、Pages 與工作流程探索 (Organization Explorer)</h2>
        </div>
      </div>
      <p class="section-desc">
        依組織或自訂條件切換檢視個別儲存庫的所有 GitHub Actions 工作流程、Pages 站點與資安防護標記。
      </p>

      <div class="org-nav-tabs">
        {org_nav_tabs_html}      </div>

      <div class="org-filter-pills">
        <span style="font-size: 0.78rem; font-weight: 700; color: #475569; margin-right: 4px;">快篩模式：</span>
        <button class="filter-pill active" data-filter="all">全部 ({data['total_repos']})</button>
        <button class="filter-pill" data-filter="has-actions">具備 Actions ({data['total_repos_with_actions']})</button>
        <button class="filter-pill" data-filter="has-pages">具備 Pages ({total_sites})</button>
        <button class="filter-pill" data-filter="has-alerts">具備資安警報 ({len(sec.get("repos_with_alerts", []))})</button>
      </div>

      <div class="org-search-wrap">
        <div class="search-box">
          <span>🔍</span>
          <input type="text" id="org-workflow-search" placeholder="在 {data['total_repos']} 個儲存庫與 {data['total_workflows']} 個工作流中搜尋 (例如：GoodInfo, docker, sync)...">
        </div>
        <div class="org-search-stats" id="org-filter-stats">顯示 {data['total_repos']} 個儲存庫</div>
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
            <span class="deck-tag">CI/CD & Sec</span>
          </div>
          <div class="deck-numbers-compact">
            <div class="stat-line">
              <span class="stat-lbl">工作流程</span>
              <span class="stat-val">{data['total_workflows']} WFs · {total_sites} Pages</span>
            </div>
            <div class="stat-line">
              <span class="stat-lbl">資安防護</span>
              <span class="stat-val">{sec_repos} 庫 · {total_alerts} 警報</span>
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
      <div>Pipeline-Deck · 跨生態系 GitHub Actions 排程、發布門戶與資安遙測中樞</div>
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
    const filterPills = document.querySelectorAll('.filter-pill');
    const orgRepoCards = document.querySelectorAll('.org-repo-card');
    const orgSearchInput = document.getElementById('org-workflow-search');
    const orgFilterStats = document.getElementById('org-filter-stats');

    let currentOrg = 'all';
    let currentQuickFilter = 'all';
    let currentOrgSearch = '';

    function applyOrgFilterAndSearch() {
      let visibleCount = 0;
      orgRepoCards.forEach(card => {
        const org = card.dataset.org;
        const repoName = card.dataset.repo || '';
        const workflows = card.dataset.workflows || '';
        const hasPages = card.dataset.hasPages === 'true';
        const hasAlerts = card.dataset.hasAlerts === 'true';
        const hasActions = card.dataset.hasActions === 'true';

        const matchesOrg = (currentOrg === 'all' || org === currentOrg);
        const matchesSearch = (!currentOrgSearch || repoName.includes(currentOrgSearch) || workflows.includes(currentOrgSearch));

        let matchesFilter = true;
        if (currentQuickFilter === 'has-actions') matchesFilter = hasActions;
        else if (currentQuickFilter === 'has-pages') matchesFilter = hasPages;
        else if (currentQuickFilter === 'has-alerts') matchesFilter = hasAlerts;

        if (matchesOrg && matchesSearch && matchesFilter) {
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

    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentQuickFilter = pill.dataset.filter;
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
