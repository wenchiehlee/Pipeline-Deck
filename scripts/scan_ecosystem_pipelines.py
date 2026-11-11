#!/usr/bin/env python3
"""
Ecosystem GitHub Actions Telemetry, Pages & Security Scanner
Scans all repositories across the 7 key organizations:
(ZhongZheng782, wenchiehlee, wenchiehlee-money, wenchiehlee-investment, wenchiehlee-ux, wenchiehlee-alert, wenchiehlee-life)
Catalogues:
  1. Workflows & Schedules (Schedule health, consecutive failures, recent run history)
  2. GitHub Pages (Enabled status, live deployment URL, build status)
  3. Security Posture (Secret scanning, push protection, dependabot alerts, CodeQL code quality, malware alerts)
Outputs:
  - data/pipeline_summary.json (Full telemetry)
  - data/kpi.json (Card KPI for Deck Family)
  - docs/ecosystem_pipeline_summary.md (Markdown report)
  - README.md (In-place telemetry update)
  - index.html (Responsive Portal)
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

TARGET_ORGS = [
    "ZhongZheng782",
    "wenchiehlee",
    "wenchiehlee-money",
    "wenchiehlee-investment",
    "wenchiehlee-ux",
    "wenchiehlee-alert",
    "wenchiehlee-life",
]

# Consistent UX-Deck Design & Mascot Registry (aligned with UX-Deck 13 Mascots Matrix)
UX_DECK_REGISTRY = {
    "wenchiehlee-ux/UX-Deck": {"symbol": "🦌", "name": "幾何靈鹿", "role": "UX 設計系統中樞"},
    "wenchiehlee/skills": {"symbol": "🐇", "name": "敏捷白兔", "role": "共享技能登錄庫"},
    "wenchiehlee/Analytics-Deck": {"symbol": "📊", "name": "觀測航線", "role": "全端點流量遙測中樞"},
    "wenchiehlee/Pipeline-Deck": {"symbol": "⚙️", "name": "齒輪引擎", "role": "CI/CD 與自動化管道中樞"},
    "wenchiehlee-money/biztrends.TW": {"symbol": "📈", "name": "市場趨勢", "role": "產業週期與金融雷達"},
    "wenchiehlee/llm": {"symbol": "🧠", "name": "智慧大腦", "role": "LLM 多模型智能路由庫"},
    "wenchiehlee/dockers": {"symbol": "🐳", "name": "貨櫃藍鯨", "role": "Docker 映像目錄與部署"},
    "wenchiehlee/mkdocs-life": {"symbol": "🦌", "name": "幾何林鹿", "role": "溫潤人文生活誌"},
    "wenchiehlee-money/GoogleAlertManager": {"symbol": "🐦", "name": "破曉警報鳥", "role": "SaaS 情報過濾雷達"},
    "ZhongZheng782/YoutubeAudio.Fetch": {"symbol": "🐋", "name": "聲波座頭鯨", "role": "影音 Podcast 萃取"},
    "wenchiehlee/mkdocs-investment": {"symbol": "🐂🐻", "name": "幾何狂牛/守護熊", "role": "大盤資產配置與避險"},
    "wenchiehlee-money/My-TW-Coverage": {"symbol": "🦉", "name": "拍拍翅萌萌鴞", "role": "台股個股深度調研"},
    "wenchiehlee-money/InvestorConference": {"symbol": "🦅", "name": "領航雄鷹", "role": "法人說明會與 IR 庫"},
    "wenchiehlee-money/VIX": {"symbol": "🦢", "name": "幾何黑天鵝", "role": "全球波動率黑天鵝雷達"},
    "ZhongZheng782/Synology-Photo-Tagger": {"symbol": "🐿️", "name": "採集松鼠", "role": "AI 相片智慧標籤"},
    "wenchiehlee/wenchiehlee.github.io": {"symbol": "👤", "name": "個人旗艦", "role": "個人官方主站門戶"},
    "wenchiehlee-investment/wenchiehlee-investment.github.io": {"symbol": "💼", "name": "投資機構", "role": "投資組織官方入口"},
    "wenchiehlee-life/wenchiehlee-life.github.io": {"symbol": "🌱", "name": "人文生活", "role": "生活組織官方門戶"},
    "wenchiehlee/mkdocs": {"symbol": "📚", "name": "知識基底", "role": "工程技術文件中心"},
    "wenchiehlee/mkdocs-demo": {"symbol": "🧪", "name": "介面範本", "role": "互動展示模版"},
    "wenchiehlee/mkdocs-material": {"symbol": "📐", "name": "架構樣板", "role": "Material 主題範本"},
}

def load_env_file():
    """Load key-value pairs from .env if present."""
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                if key and key not in os.environ:
                    os.environ[key] = val

def get_github_token() -> str:
    """Retrieve token from env GITHUB_TOKEN / GH_TOKEN or local gh CLI."""
    load_env_file()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True
        )
        return proc.stdout.strip()
    except Exception:
        return ""

def create_session(token: str) -> requests.Session:
    from urllib3.util import Retry
    from requests.adapters import HTTPAdapter

    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Pipeline-Deck-Scanner"
    })
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=25, pool_maxsize=25)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_org_repos(session: requests.Session, org: str):
    """Fetch all active (non-archived) repositories under an organization or user using gh CLI or REST API."""
    if shutil.which("gh"):
        try:
            cmd = ["gh", "repo", "list", org, "--no-archived", "--limit", "200", "--json", "name,isPrivate,url,isArchived"]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(proc.stdout)
            repos = []
            for item in data:
                if item.get("isArchived", False):
                    continue
                repos.append({
                    "name": item["name"],
                    "full_name": f"{org}/{item['name']}",
                    "html_url": item.get("url") or f"https://github.com/{org}/{item['name']}",
                    "private": item.get("isPrivate", False)
                })
            return repos
        except Exception as e:
            print(f"Notice: gh repo list failed for {org} ({e}), falling back to REST API...", file=sys.stderr)

    repos = []
    page = 1
    while True:
        if org == "wenchiehlee":
            url = f"https://api.github.com/user/repos?affiliation=owner&per_page=100&page={page}"
        else:
            url = f"https://api.github.com/orgs/{org}/repos?type=all&per_page=100&page={page}"
            
        resp = session.get(url)
        if resp.status_code != 200:
            url = f"https://api.github.com/users/{org}/repos?per_page=100&page={page}"
            resp = session.get(url)
            
        if resp.status_code != 200:
            print(f"Warning: Failed to fetch repos for {org} (HTTP {resp.status_code}): {resp.text}", file=sys.stderr)
            break
            
        data = resp.json()
        if not data:
            break
        for r in data:
            if r.get("archived", False):
                continue
            repos.append({
                "name": r["name"],
                "full_name": r.get("full_name", f"{org}/{r['name']}"),
                "html_url": r.get("html_url", f"https://github.com/{org}/{r['name']}"),
                "private": r.get("private", False)
            })
        if len(data) < 100:
            break
        page += 1
    return repos

def scan_single_repo(session: requests.Session, org: str, repo_basic: dict) -> dict:
    """Perform comprehensive inspection of a single repository:
    1. Base metadata (has_pages, security_and_analysis)
    2. GitHub Pages live status
    3. Security posture (Secret scanning, Push protection, Dependabot updates)
    4. Dependabot open alerts
    5. Code scanning (CodeQL) open alerts
    6. Secret scanning (Malware / Leaks) alerts
    7. Workflows list
    8. Schedule health & consecutive failures
    """
    full_name = repo_basic["full_name"]
    name = repo_basic["name"]
    repo_url = f"https://api.github.com/repos/{full_name}"

    # 1. Base repo info
    r_resp = session.get(repo_url)
    if r_resp.status_code == 200:
        r_data = r_resp.json()
        is_private = r_data.get("private", repo_basic.get("private", False))
        has_pages = r_data.get("has_pages", False)
        sec_analysis = r_data.get("security_and_analysis") or {}
        html_url = r_data.get("html_url", repo_basic["html_url"])
    else:
        is_private = repo_basic.get("private", False)
        has_pages = False
        sec_analysis = {}
        html_url = repo_basic["html_url"]

    # 2. Pages
    pages_info = {"enabled": False, "url": None, "status": None, "build_type": None}
    if has_pages:
        p_resp = session.get(f"{repo_url}/pages")
        if p_resp.status_code == 200:
            p_data = p_resp.json()
            pg_status = p_data.get("status")
            pg_btype = p_data.get("build_type")
            # Workflow-based Pages deployments are authoritative. The /pages status
            # can retain a stale legacy build error after a successful Actions deploy.
            if pg_btype == "workflow":
                try:
                    d_resp = session.get(f"{repo_url}/deployments?environment=github-pages&per_page=1", timeout=8)
                    if d_resp.status_code == 200 and d_resp.json():
                        st_url = d_resp.json()[0].get("statuses_url")
                        if st_url:
                            st_resp = session.get(st_url, timeout=8)
                            if st_resp.status_code == 200 and st_resp.json():
                                d_state = st_resp.json()[0].get("state")
                                if d_state == "success":
                                    pg_status = "built"
                                elif d_state in ("failure", "error"):
                                    pg_status = "errored"
                except Exception:
                    pass
            pages_info = {
                "enabled": True,
                "url": p_data.get("html_url"),
                "status": pg_status,
                "build_type": pg_btype
            }
        else:
            pages_info["enabled"] = True

    # 3. Security features
    def parse_sec(key):
        val = sec_analysis.get(key, {})
        if isinstance(val, dict):
            return val.get("status", "disabled")
        return "disabled"

    security_info = {
        "secret_scanning": parse_sec("secret_scanning"),
        "push_protection": parse_sec("secret_scanning_push_protection"),
        "dependabot_updates": parse_sec("dependabot_security_updates")
    }

    # 4. Dependabot alerts
    dep_alerts_data = {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "items": []}
    dep_resp = session.get(f"{repo_url}/dependabot/alerts?state=open&per_page=100")
    if dep_resp.status_code == 200:
        alerts = dep_resp.json()
        if isinstance(alerts, list):
            dep_alerts_data["total"] = len(alerts)
            for a in alerts:
                sev = a.get("security_advisory", {}).get("severity", "low").lower()
                if sev in dep_alerts_data:
                    dep_alerts_data[sev] += 1
                dep_alerts_data["items"].append({
                    "number": a.get("number"),
                    "package": a.get("dependency", {}).get("package", {}).get("name"),
                    "severity": sev,
                    "summary": a.get("security_advisory", {}).get("summary"),
                    "html_url": a.get("html_url")
                })

    # 5. Code scanning (CodeQL) alerts
    code_alerts_data = {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "items": []}
    code_resp = session.get(f"{repo_url}/code-scanning/alerts?state=open&per_page=100")
    if code_resp.status_code == 200:
        c_alerts = code_resp.json()
        if isinstance(c_alerts, list):
            code_alerts_data["total"] = len(c_alerts)
            for ca in c_alerts:
                rule = ca.get("rule", {})
                sev = rule.get("security_severity_level") or rule.get("severity", "low")
                sev = sev.lower()
                if sev in code_alerts_data:
                    code_alerts_data[sev] += 1
                elif sev == "error":
                    code_alerts_data["high"] += 1
                elif sev == "warning":
                    code_alerts_data["medium"] += 1
                elif sev == "note":
                    code_alerts_data["low"] += 1
                code_alerts_data["items"].append({
                    "number": ca.get("number"),
                    "rule_id": rule.get("id"),
                    "description": rule.get("description"),
                    "severity": sev,
                    "tool": ca.get("tool", {}).get("name"),
                    "html_url": ca.get("html_url")
                })

    # 6. Secret scanning alerts (malware / leaks)
    secret_alerts_data = {"total": 0, "items": []}
    sec_resp = session.get(f"{repo_url}/secret-scanning/alerts?state=open&per_page=100")
    if sec_resp.status_code == 200:
        s_alerts = sec_resp.json()
        if isinstance(s_alerts, list):
            secret_alerts_data["total"] = len(s_alerts)
            for sa in s_alerts:
                secret_alerts_data["items"].append({
                    "number": sa.get("number"),
                    "secret_type": sa.get("secret_type_display_name", sa.get("secret_type")),
                    "html_url": sa.get("html_url")
                })

    # 7. Workflows list
    workflows = []
    wf_resp = session.get(f"{repo_url}/contents/.github/workflows")
    if wf_resp.status_code == 200:
        contents = wf_resp.json()
        if isinstance(contents, list):
            workflows = sorted([
                item["name"] for item in contents
                if item.get("name", "").endswith((".yml", ".yaml"))
            ])

    # 8. Schedule health (if workflows exist)
    schedules = []
    if workflows:
        # Check disabled workflows
        wf_list_resp = session.get(f"{repo_url}/actions/workflows")
        disabled_paths = set()
        if wf_list_resp.status_code == 200:
            for wf in wf_list_resp.json().get("workflows", []):
                if wf.get("state") in ("disabled_manually", "disabled_inactivity"):
                    disabled_paths.add(wf.get("path"))

        sched_resp = session.get(f"{repo_url}/actions/runs?event=schedule&per_page=30")
        if sched_resp.status_code == 200:
            sched_runs = sched_resp.json().get("workflow_runs", [])
            scheduled_paths = {r.get("path") for r in sched_runs if r.get("path")}
            scheduled_paths -= disabled_paths

            if scheduled_paths:
                all_resp = session.get(f"{repo_url}/actions/runs?per_page=50")
                all_runs = all_resp.json().get("workflow_runs", []) if all_resp.status_code == 200 else sched_runs
                
                by_path = {}
                for r in all_runs:
                    p = r.get("path")
                    if p and p in scheduled_paths:
                        by_path.setdefault(p, []).append(r)
                for r in sched_runs:
                    p = r.get("path")
                    if p and p in scheduled_paths and p not in by_path:
                        by_path.setdefault(p, []).append(r)

                for p, wruns in by_path.items():
                    completed = [run for run in wruns if run.get("status") == "completed"]
                    if not completed:
                        continue
                    completed.sort(key=lambda x: x.get("created_at", ""), reverse=True)
                    recent_4 = completed[:4]
                    consecutive_failures = 0
                    for run in completed:
                        if run.get("conclusion") == "failure":
                            consecutive_failures += 1
                        else:
                            break
                    run_icons = ["❌" if x.get("conclusion") == "failure" else "✅" for x in recent_4]
                    file_name = p.split("/")[-1] if "/" in p else p
                    schedules.append({
                        "repo": full_name,
                        "workflow_name": completed[0].get("name", file_name),
                        "file": file_name,
                        "path": p,
                        "consecutive_failures": consecutive_failures,
                        "recent_4_icons": "".join(run_icons),
                        "latest_conclusion": completed[0].get("conclusion"),
                        "latest_run_at": completed[0].get("created_at"),
                        "latest_run_url": completed[0].get("html_url")
                    })

    return {
        "org": org,
        "name": name,
        "full_name": full_name,
        "html_url": html_url,
        "is_private": is_private,
        "workflow_count": len(workflows),
        "workflows": workflows,
        "schedules": schedules,
        "pages": pages_info,
        "security": security_info,
        "alerts": {
            "dependabot": dep_alerts_data,
            "code_scanning": code_alerts_data,
            "malware": secret_alerts_data
        }
    }

def scan_ecosystem():
    token = get_github_token()
    session = create_session(token)

    summary_data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_repos": 0,
        "total_repos_with_actions": 0,
        "total_workflows": 0,
        "scheduled_telemetry": {
            "total_monitored_schedules": 0,
            "critical_consecutive_4_count": 0,
            "warning_consecutive_1_to_3_count": 0,
            "healthy_count": 0,
            "critical_alerts": [],
            "warning_alerts": [],
            "healthy_workflows": []
        },
        "pages_telemetry": {
            "total_sites": 0,
            "built_sites": 0,
            "errored_sites": 0,
            "other_sites": 0,
            "sites": []
        },
        "security_telemetry": {
            "secret_scanning_enabled_count": 0,
            "push_protection_enabled_count": 0,
            "dependabot_updates_enabled_count": 0,
            "total_open_dependabot_alerts": 0,
            "dependabot_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "total_open_codeql_alerts": 0,
            "codeql_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "total_malware_alerts": 0,
            "repos_with_alerts": []
        },
        "orgs": {}
    }

    # Step 1: Collect non-archived repos across all organizations
    all_repo_targets = []
    print("[*] Fetching active repository manifests across 7 organizations...")
    for org in TARGET_ORGS:
        repos = fetch_org_repos(session, org)
        for r in repos:
            all_repo_targets.append((org, r))
        summary_data["orgs"][org] = {
            "total_repos": len(repos),
            "repos_with_actions": 0,
            "total_workflows": 0,
            "repos": []
        }
        summary_data["total_repos"] += len(repos)

    print(f"[*] Total active repositories to scan concurrently: {len(all_repo_targets)}")

    # Step 2: Parallel execution across all repos using ThreadPoolExecutor
    all_repo_results = []
    all_schedules = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_map = {
            executor.submit(scan_single_repo, session, org, repo): (org, repo["full_name"])
            for org, repo in all_repo_targets
        }
        for future in as_completed(future_map):
            org, full_name = future_map[future]
            try:
                res = future.result()
                if res:
                    all_repo_results.append(res)
            except Exception as e:
                print(f"Warning: Failed scanning {full_name}: {e}", file=sys.stderr)

    # Step 3: Aggregate into summary structures
    for r in all_repo_results:
        org = r["org"]
        wf_count = r["workflow_count"]
        summary_data["total_workflows"] += wf_count
        summary_data["orgs"][org]["total_workflows"] += wf_count
        if wf_count > 0:
            summary_data["total_repos_with_actions"] += 1
            summary_data["orgs"][org]["repos_with_actions"] += 1

        all_schedules.extend(r.get("schedules", []))

        # Pages telemetry aggregation
        pg = r.get("pages", {})
        if pg.get("enabled"):
            st = pg.get("status")
            if st == "built":
                summary_data["pages_telemetry"]["built_sites"] += 1
            elif st == "errored":
                summary_data["pages_telemetry"]["errored_sites"] += 1
            else:
                summary_data["pages_telemetry"]["other_sites"] += 1

            summary_data["pages_telemetry"]["sites"].append({
                "org": org,
                "name": r["name"],
                "repo": r["full_name"],
                "url": pg.get("url"),
                "status": st,
                "build_type": pg.get("build_type"),
                "is_private": r.get("is_private", False)
            })

        # Security posture aggregation
        sec = r.get("security", {})
        if sec.get("secret_scanning") == "enabled":
            summary_data["security_telemetry"]["secret_scanning_enabled_count"] += 1
        if sec.get("push_protection") == "enabled":
            summary_data["security_telemetry"]["push_protection_enabled_count"] += 1
        if sec.get("dependabot_updates") == "enabled":
            summary_data["security_telemetry"]["dependabot_updates_enabled_count"] += 1

        # Alerts aggregation
        alerts = r.get("alerts", {})
        dep = alerts.get("dependabot", {})
        code = alerts.get("code_scanning", {})
        mal = alerts.get("malware", {})

        dep_tot = dep.get("total", 0)
        code_tot = code.get("total", 0)
        mal_tot = mal.get("total", 0)

        if dep_tot > 0:
            summary_data["security_telemetry"]["total_open_dependabot_alerts"] += dep_tot
            for k in ["critical", "high", "medium", "low"]:
                summary_data["security_telemetry"]["dependabot_breakdown"][k] += dep.get(k, 0)

        if code_tot > 0:
            summary_data["security_telemetry"]["total_open_codeql_alerts"] += code_tot
            for k in ["critical", "high", "medium", "low"]:
                summary_data["security_telemetry"]["codeql_breakdown"][k] += code.get(k, 0)

        if mal_tot > 0:
            summary_data["security_telemetry"]["total_malware_alerts"] += mal_tot

        if dep_tot > 0 or code_tot > 0 or mal_tot > 0:
            summary_data["security_telemetry"]["repos_with_alerts"].append({
                "repo": r["full_name"],
                "org": org,
                "is_private": r.get("is_private", False),
                "dependabot_total": dep_tot,
                "dependabot_breakdown": {k: dep.get(k, 0) for k in ["critical", "high", "medium", "low"]},
                "dependabot_items": dep.get("items", []),
                "codeql_total": code_tot,
                "codeql_breakdown": {k: code.get(k, 0) for k in ["critical", "high", "medium", "low"]},
                "codeql_items": code.get("items", []),
                "malware_total": mal_tot,
                "malware_items": mal.get("items", [])
            })

        # Insert repo into org list
        summary_data["orgs"][org]["repos"].append(r)

    # Sort repos within each org by workflow count descending
    for org in TARGET_ORGS:
        summary_data["orgs"][org]["repos"].sort(key=lambda x: (-x["workflow_count"], x["name"].lower()))

    # Sort Pages sites by status then repo name
    summary_data["pages_telemetry"]["sites"].sort(key=lambda x: (0 if x["status"] == "errored" else (1 if x["status"] == "built" else 2), x["repo"].lower()))
    summary_data["pages_telemetry"]["total_sites"] = len(summary_data["pages_telemetry"]["sites"])

    # Sort repos with alerts by total alerts descending
    summary_data["security_telemetry"]["repos_with_alerts"].sort(
        key=lambda x: (-(x["dependabot_total"] + x["codeql_total"] + x["malware_total"]), x["repo"].lower())
    )

    # Process schedule health data
    all_schedules.sort(key=lambda x: (-x["consecutive_failures"], x["repo"], x["file"]))
    for item in all_schedules:
        cf = item["consecutive_failures"]
        if cf >= 4:
            summary_data["scheduled_telemetry"]["critical_alerts"].append(item)
        elif cf >= 1:
            summary_data["scheduled_telemetry"]["warning_alerts"].append(item)
        else:
            summary_data["scheduled_telemetry"]["healthy_workflows"].append(item)

    summary_data["scheduled_telemetry"]["total_monitored_schedules"] = len(all_schedules)
    summary_data["scheduled_telemetry"]["critical_consecutive_4_count"] = len(summary_data["scheduled_telemetry"]["critical_alerts"])
    summary_data["scheduled_telemetry"]["warning_consecutive_1_to_3_count"] = len(summary_data["scheduled_telemetry"]["warning_alerts"])
    summary_data["scheduled_telemetry"]["healthy_count"] = len(summary_data["scheduled_telemetry"]["healthy_workflows"])

    return summary_data

def generate_markdown(data) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sch = data["scheduled_telemetry"]
    pg = data.get("pages_telemetry", {})
    sec = data.get("security_telemetry", {})
    ns_quartet = f"{data['total_workflows']} / {data['total_repos_with_actions']} / {sch['critical_consecutive_4_count']} / {sch['warning_consecutive_1_to_3_count']}"
    
    lines = [
        f"<!-- PIPELINE_SUMMARY_START -->",
        f"## 🌐 全域工作流程、發布門戶與資安遙測統計 (Ecosystem Telemetry)",
        f"",
        f"> **全域統計**：涵蓋 **{len(TARGET_ORGS)} 大核心組織**，共有 **{data['total_repos']} 個活躍儲存庫**（排除已封存庫），其中 **{data['total_repos_with_actions']} 個儲存庫** 具備自動化工作流，累計運行 **{data['total_workflows']} 個工作流程 YAML 檔案**、**{pg.get('total_sites', 0)} 個 GitHub Pages 線上門戶**，以及 **{sec.get('secret_scanning_enabled_count', 0)} 個啟用全方位資安防護庫**。（自動掃描更新於：`{now_utc}`）",
        f">",
        f"> 🎯 **北極星核心維運指標 (North Star Quartet)**：**`{ns_quartet}`**（**{data['total_workflows']}** 個工作流程 YAML · **{data['total_repos_with_actions']}** 個活躍 Actions 庫 · **{sch['critical_consecutive_4_count']}** 個嚴重警報 · **{sch['warning_consecutive_1_to_3_count']}** 個異常警告）",
        f"",
        f"### 📊 組織工作流程、Pages 與資安分佈總覽",
        f"",
        f"| 組織 / 帳號 (`Owner`) | 活躍儲存庫數 | 具備 Actions 的 Repo | 工作流程 YAML 數 | Pages 發布站點 | 資安防護啟用庫 | 待處置警報總數 |",
        f"|---|:---:|:---:|:---:|:---:|:---:|:---:|",
    ]

    for org in TARGET_ORGS:
        o = data["orgs"][org]
        # Count pages & security for org
        org_pages = sum(1 for r in o["repos"] if r.get("pages", {}).get("enabled"))
        org_sec = sum(1 for r in o["repos"] if r.get("security", {}).get("secret_scanning") == "enabled")
        org_alerts = sum(r.get("alerts", {}).get("dependabot", {}).get("total", 0) + r.get("alerts", {}).get("code_scanning", {}).get("total", 0) for r in o["repos"])
        alert_str = f"**{org_alerts}**" if org_alerts > 0 else "0"
        lines.append(f"| [`{org}`](https://github.com/{org}) | {o['total_repos']} | {o['repos_with_actions']} | **{o['total_workflows']}** | {org_pages} | {org_sec} | {alert_str} |")

    tot_alerts = sec.get("total_open_dependabot_alerts", 0) + sec.get("total_open_codeql_alerts", 0)
    lines.append(f"| **全域總計** | **{data['total_repos']}** | **{data['total_repos_with_actions']}** | **{data['total_workflows']} 個 YAML** | **{pg.get('total_sites', 0)} 站點** | **{sec.get('secret_scanning_enabled_count', 0)} 庫** | **{tot_alerts} 處** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- SECTION: SCHEDULED CONSECUTIVE FAILURES ---
    lines.append(f"### 🚨 常態排程健康度與連續失敗監測 (Scheduled Consecutive Failures)")
    lines.append("")
    lines.append(f"- **常態排程監測總數**：`{sch['total_monitored_schedules']}` 個工作流程")
    lines.append(f"- **🚨 嚴重警報（連續失敗 ≥ 4 次）**：`{sch['critical_consecutive_4_count']}` 個")
    lines.append(f"- **⚠️ 異常警告（連續失敗 1~3 次）**：`{sch['warning_consecutive_1_to_3_count']}` 個")
    lines.append(f"- **🟢 正常運行（最新一次執行成功）**：`{sch['healthy_count']}` 個")
    lines.append("")

    if sch["critical_consecutive_4_count"] > 0:
        lines.append("#### 🔴 嚴重警報：常態排程連續失敗 ≥ 4 次清單")
        lines.append("")
        lines.append("| # | 儲存庫 | 工作流程名稱 | YAML 檔案 | 連續失敗次數 | 最近 4 次狀態 | 最新失敗時間 | 執行日誌 |")
        lines.append("|---|---|---|---|:---:|:---:|---|:---:|")
        for idx, item in enumerate(sch["critical_alerts"], 1):
            repo_link = f"[{item['repo']}](https://github.com/{item['repo']})"
            run_link = f"[Run ↗]({item['latest_run_url']})" if item.get("latest_run_url") else "-"
            lines.append(f"| {idx} | {repo_link} | {item['workflow_name']} | `{item['file']}` | **{item['consecutive_failures']} 次** | `{item['recent_4_icons']}` | `{item['latest_run_at'][:19]}` | {run_link} |")
        lines.append("")

    if sch["warning_consecutive_1_to_3_count"] > 0:
        lines.append("#### 🟡 異常警告：常態排程最新一次失敗（連續失敗 1~3 次）")
        lines.append("")
        lines.append("| # | 儲存庫 | 工作流程名稱 | YAML 檔案 | 連續失敗次數 | 最近 4 次狀態 | 最新失敗時間 | 執行日誌 |")
        lines.append("|---|---|---|---|:---:|:---:|---|:---:|")
        for idx, item in enumerate(sch["warning_alerts"], 1):
            repo_link = f"[{item['repo']}](https://github.com/{item['repo']})"
            run_link = f"[Run ↗]({item['latest_run_url']})" if item.get("latest_run_url") else "-"
            lines.append(f"| {idx} | {repo_link} | {item['workflow_name']} | `{item['file']}` | **{item['consecutive_failures']} 次** | `{item['recent_4_icons']}` | `{item['latest_run_at'][:19]}` | {run_link} |")
        lines.append("")

    if sch["critical_consecutive_4_count"] == 0 and sch["warning_consecutive_1_to_3_count"] == 0:
        lines.append("> ✅ **目前全域常態排程工作流程運作狀態良好，無任何連續失敗管道。**")
        lines.append("")

    lines.append("---")
    lines.append("")

    # --- SECTION: GITHUB PAGES DEPLOYMENTS ---
    lines.append(f"### 🌐 GitHub Pages 線上發布門戶觀測 (GitHub Pages Deployments)")
    lines.append("")
    lines.append(f"- **Pages 發布站點總數**：`{pg.get('total_sites', 0)}` 個站點")
    lines.append(f"- **🟢 正常發布 (`built`)**：`{pg.get('built_sites', 0)}` 個")
    lines.append(f"- **🔴 建置異常 (`errored`)**：`{pg.get('errored_sites', 0)}` 個")
    lines.append(f"- **⚪ 其他/初始待命中 (`other`)**：`{pg.get('other_sites', 0)}` 個")
    lines.append("")
    lines.append("| # | 組織 / 儲存庫 | UX 意象與定位 (UX-Deck) | Pages 線上網址 | 建置狀態 | 建置管道 | 可見性 |")
    lines.append("|---|---|---|---|:---:|:---:|:---:|")

    status_icon_map = {"built": "🟢 正常 (built)", "errored": "🔴 異常 (errored)"}
    for idx, s in enumerate(pg.get("sites", []), 1):
        st_icon = status_icon_map.get(s["status"], f"⚪ {s['status']}")
        url_link = f"[{s['url']}]({s['url']})" if s.get("url") else "*(未生成網址)*"
        repo_link = f"[{s['repo']}](https://github.com/{s['repo']})"
        vis = "🔒 私有" if s.get("is_private") else "🌍 公開"
        ux_meta = UX_DECK_REGISTRY.get(s["repo"], {"symbol": "🌐", "name": "線上站點", "role": "GitHub Pages 門戶"})
        ux_display = f"{ux_meta['symbol']} {ux_meta['name']} (`{ux_meta['role']}`)"
        lines.append(f"| {idx} | {repo_link} | {ux_display} | {url_link} | {st_icon} | `{s.get('build_type', 'legacy')}` | {vis} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # --- SECTION: SECURITY POSTURE, DEPENDABOT & CODE QUALITY ---
    dep_bd = sec.get("dependabot_breakdown", {})
    code_bd = sec.get("codeql_breakdown", {})
    lines.append(f"### 🛡️ 全域資安防護、Dependabot 與代碼品質觀測 (Security Posture & Code Quality)")
    lines.append("")
    lines.append(f"- **秘密掃描防護 (Secret Scanning)**：`{sec.get('secret_scanning_enabled_count', 0)}` 個儲存庫啟用")
    lines.append(f"- **阻擋推送防護 (Push Protection)**：`{sec.get('push_protection_enabled_count', 0)}` 個儲存庫啟用")
    lines.append(f"- **Dependabot 自動安全修正**：`{sec.get('dependabot_updates_enabled_count', 0)}` 個儲存庫啟用")
    lines.append(f"- **Dependabot 待修復警報**：`{sec.get('total_open_dependabot_alerts', 0)}` 處（🔴 {dep_bd.get('critical', 0)} 嚴重 · 🟠 {dep_bd.get('high', 0)} 高度 · 🟡 {dep_bd.get('medium', 0)} 中度 · 🔵 {dep_bd.get('low', 0)} 低度）")
    lines.append(f"- **CodeQL 代碼品質與安全漏洞**：`{sec.get('total_open_codeql_alerts', 0)}` 處（🔴 {code_bd.get('critical', 0)} 嚴重 · 🟠 {code_bd.get('high', 0)} 高度 · 🟡 {code_bd.get('medium', 0)} 中度 · 🔵 {code_bd.get('low', 0)} 低度）")
    lines.append(f"- **惡意代碼與外洩警報 (Malware / Leaks)**：`{sec.get('total_malware_alerts', 0)}` 處")
    lines.append("")

    repos_with_alerts = sec.get("repos_with_alerts", [])
    if repos_with_alerts:
        lines.append("#### ⚠️ 待處置資安警報與代碼品質儲存庫清單")
        lines.append("")
        lines.append("| # | 組織 / 儲存庫 | Dependabot 警報 | CodeQL 漏洞 | 惡意代碼 | 嚴重等級分佈 (Crit/High/Med/Low) | 安全儀表板直達 |")
        lines.append("|---|---|:---:|:---:|:---:|---|:---:|")
        for idx, ra in enumerate(repos_with_alerts, 1):
            repo_link = f"[{ra['repo']}](https://github.com/{ra['repo']})"
            dep_cnt = f"**{ra['dependabot_total']}**" if ra['dependabot_total'] > 0 else "0"
            code_cnt = f"**{ra['codeql_total']}**" if ra['codeql_total'] > 0 else "0"
            mal_cnt = f"**{ra['malware_total']}**" if ra['malware_total'] > 0 else "0"
            
            # Combine breakdown
            crit_tot = ra["dependabot_breakdown"].get("critical", 0) + ra["codeql_breakdown"].get("critical", 0)
            high_tot = ra["dependabot_breakdown"].get("high", 0) + ra["codeql_breakdown"].get("high", 0)
            med_tot = ra["dependabot_breakdown"].get("medium", 0) + ra["codeql_breakdown"].get("medium", 0)
            low_tot = ra["dependabot_breakdown"].get("low", 0) + ra["codeql_breakdown"].get("low", 0)
            breakdown_str = f"🔴 {crit_tot} · 🟠 {high_tot} · 🟡 {med_tot} · 🔵 {low_tot}"
            
            sec_url = f"[Security ↗](https://github.com/{ra['repo']}/security)"
            lines.append(f"| {idx} | {repo_link} | {dep_cnt} | {code_cnt} | {mal_cnt} | `{breakdown_str}` | {sec_url} |")
        lines.append("")
    else:
        lines.append("> ✅ **目前全域所有活躍儲存庫無任何待處置安全漏洞或品質警報。**")
        lines.append("")

    lines.append("---")
    lines.append("")

    # --- SECTION: ORGANIZATIONAL BREAKDOWN ---
    for org in TARGET_ORGS:
        o = data["orgs"][org]
        lines.append(f"### 📁 `{org}` ({o['repos_with_actions']} 個 Repo · 共 {o['total_workflows']} 個 YAML)")
        lines.append("")
        lines.append("| # | 儲存庫名稱 | YAML 數 | Pages 狀態 | 資安防護 | 待處置警報 | 工作流程 YAML 清單 |")
        lines.append("|---|---|:---:|:---:|:---:|:---:|---|")
        
        active_repos = [r for r in o["repos"] if r["workflow_count"] > 0]
        for idx, r in enumerate(active_repos, 1):
            wf_links = ", ".join([f"`{wf}`" for wf in r["workflows"]])
            repo_link = f"[{r['name']}]({r['html_url']})"
            
            pg_status = "-"
            if r.get("pages", {}).get("enabled"):
                st = r.get("pages", {}).get("status", "enabled")
                pg_url = r.get("pages", {}).get("url")
                pg_status = f"[🟢 {st}]({pg_url})" if (pg_url and st == "built") else (f"[🔴 {st}]({pg_url})" if pg_url else f"⚪ {st}")
                
            sec_status = "🛡️ 啟用" if r.get("security", {}).get("secret_scanning") == "enabled" else "⚪ 預設"
            
            dep_cnt = r.get("alerts", {}).get("dependabot", {}).get("total", 0)
            code_cnt = r.get("alerts", {}).get("code_scanning", {}).get("total", 0)
            tot_a = dep_cnt + code_cnt
            alert_badge = f"⚠️ **{tot_a}**" if tot_a > 0 else "0"
            
            lines.append(f"| {idx} | {repo_link} | **{r['workflow_count']}** | {pg_status} | {sec_status} | {alert_badge} | {wf_links} |")
        
        inactive_count = o["total_repos"] - len(active_repos)
        if inactive_count > 0:
            lines.append(f"| - | *其餘 {inactive_count} 個 Repo* | 0 | - | - | - | *(無 Actions)* |")
        elif o["total_repos"] == 0:
            lines.append(f"| - | *(目前尚無儲存庫)* | 0 | - | - | - | - |")
        lines.append("")

    lines.append("<!-- PIPELINE_SUMMARY_END -->")
    return "\n".join(lines)

def update_readme(md_content: str, readme_path: Path):
    if not readme_path.exists():
        return
    text = readme_path.read_text(encoding="utf-8")
    start_tag = "<!-- PIPELINE_SUMMARY_START -->"
    end_tag = "<!-- PIPELINE_SUMMARY_END -->"
    
    if start_tag in text and end_tag in text:
        parts = text.split(start_tag)
        before = parts[0]
        after = parts[1].split(end_tag)[1]
        new_text = f"{before}{md_content}{after}"
    else:
        new_text = f"{text.strip()}\n\n---\n\n{md_content}\n"
        
    readme_path.write_text(new_text, encoding="utf-8")
    print(f"[+] Updated {readme_path}")

def update_github_step_summary(md_content: str):
    """Write summary to GitHub Actions Step Summary if running in Actions environment."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write(md_content)
            print(f"[+] Appended telemetry report to GITHUB_STEP_SUMMARY")
        except Exception as e:
            print(f"Warning: Failed to write to GITHUB_STEP_SUMMARY: {e}", file=sys.stderr)

def update_index_html(summary_data: dict, index_html_path: Path):
    try:
        from generate_portal_html import generate_portal_html
    except ImportError:
        try:
            from scripts.generate_portal_html import generate_portal_html
        except ImportError:
            generate_portal_html = None

    if generate_portal_html:
        generate_portal_html(summary_data, index_html_path)
        return

    if not index_html_path.exists():
        return
    text = index_html_path.read_text(encoding="utf-8")
    
    # Update embedded window.PIPELINE_TELEMETRY JSON
    json_start = "/* TELEMETRY_DATA_START */"
    json_end = "/* TELEMETRY_DATA_END */"
    if json_start in text and json_end in text:
        parts = text.split(json_start)
        before = parts[0]
        after = parts[1].split(json_end)[1]
        raw_json = json.dumps(summary_data, ensure_ascii=False)
        text = f"{before}{json_start}\n    window.PIPELINE_TELEMETRY = {raw_json};\n    {json_end}{after}"
    
    index_html_path.write_text(text, encoding="utf-8")
    print(f"[+] Updated {index_html_path}")

def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    docs_dir = base_dir / "docs"
    data_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    summary_data = scan_ecosystem()

    # 1. Save Full Telemetry JSON
    json_path = data_dir / "pipeline_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved telemetry JSON to {json_path}")

    # 1.1 Save Lightweight Card KPI JSON (for Deck Family Sync)
    sch = summary_data["scheduled_telemetry"]
    pg = summary_data.get("pages_telemetry", {})
    sec = summary_data.get("security_telemetry", {})
    ns_val = f"{summary_data['total_workflows']} / {summary_data['total_repos_with_actions']} / {sch.get('critical_consecutive_4_count', 0)} / {sch.get('warning_consecutive_1_to_3_count', 0)}"
    kpi_data = {
        "deck": "Pipeline-Deck",
        "symbol": "⚙️",
        "north_star": ns_val,
        "metrics": {
            "workflows": summary_data["total_workflows"],
            "repos_with_actions": summary_data["total_repos_with_actions"],
            "total_repos": summary_data["total_repos"],
            "critical_alerts": sch.get("critical_consecutive_4_count", 0),
            "warning_alerts": sch.get("warning_consecutive_1_to_3_count", 0),
            "monitored_schedules": sch.get("total_monitored_schedules", 0),
            "pages_sites": pg.get("total_sites", 0),
            "pages_built": pg.get("built_sites", 0),
            "pages_errored": pg.get("errored_sites", 0),
            "secret_scanning_repos": sec.get("secret_scanning_enabled_count", 0),
            "push_protection_repos": sec.get("push_protection_enabled_count", 0),
            "dependabot_alerts_total": sec.get("total_open_dependabot_alerts", 0),
            "codeql_alerts_total": sec.get("total_open_codeql_alerts", 0),
            "malware_alerts_total": sec.get("total_malware_alerts", 0)
        },
        "card": {
            "title": "Pipeline-Deck",
            "tag": "CI/CD & Sec",
            "theme": "theme-pipeline",
            "stat1": { "label": "工作流程 & 門戶", "value": f"{summary_data['total_workflows']} WFs · {pg.get('total_sites', 0)} Pages" },
            "stat2": { "label": "資安防護 & 警報", "value": f"{sec.get('secret_scanning_enabled_count', 0)} 庫防護 · {sec.get('total_open_dependabot_alerts', 0) + sec.get('total_open_codeql_alerts', 0)} 處待處置" },
            "bottom_line": f"⚡ CI/CD: {ns_val}",
            "portal_url": "https://wenchiehlee.github.io/Pipeline-Deck/",
            "repo_url": "https://github.com/wenchiehlee/Pipeline-Deck"
        },
        "updated_at": summary_data.get("generated_at", datetime.now(timezone.utc).isoformat())
    }
    kpi_path = data_dir / "kpi.json"
    with open(kpi_path, "w", encoding="utf-8") as f:
        json.dump(kpi_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved lightweight KPI JSON to {kpi_path}")

    # 2. Save Markdown Report
    md_content = generate_markdown(summary_data)
    md_path = docs_dir / "ecosystem_pipeline_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Saved markdown summary to {md_path}")

    # 3. Update README.md
    readme_path = base_dir / "README.md"
    update_readme(md_content, readme_path)

    # 4. GitHub Actions Step Summary
    update_github_step_summary(md_content)

    # 5. Update index.html
    index_html_path = base_dir / "index.html"
    update_index_html(summary_data, index_html_path)

    print("\n[✓] Ecosystem telemetry scan completed successfully:")
    print(f"    - Total Repositories: {summary_data['total_repos']}")
    print(f"    - Repos with Actions: {summary_data['total_repos_with_actions']}")
    print(f"    - Total Workflows: {summary_data['total_workflows']}")
    print(f"    - Monitored Schedules: {sch['total_monitored_schedules']} (🚨 {sch['critical_consecutive_4_count']} Crit | ⚠️ {sch['warning_consecutive_1_to_3_count']} Warn)")
    print(f"    - 🌐 GitHub Pages Sites: {pg.get('total_sites', 0)} (🟢 {pg.get('built_sites', 0)} Built | 🔴 {pg.get('errored_sites', 0)} Errored)")
    print(f"    - 🛡️ Secret Scanning Repos: {sec.get('secret_scanning_enabled_count', 0)}")
    print(f"    - 🛡️ Push Protection Repos: {sec.get('push_protection_enabled_count', 0)}")
    print(f"    - 📦 Dependabot Open Alerts: {sec.get('total_open_dependabot_alerts', 0)}")
    print(f"    - 🔍 CodeQL Open Alerts: {sec.get('total_open_codeql_alerts', 0)}")
    print(f"    - ☣️ Malware Alerts: {sec.get('total_malware_alerts', 0)}")

if __name__ == "__main__":
    main()
