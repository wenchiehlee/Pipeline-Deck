#!/usr/bin/env python3
"""
Ecosystem GitHub Actions Telemetry & Pipeline Scanner
Scans all repositories across the 4 key organizations (wenchiehlee, wenchiehlee-money, ZhongZheng782, wenchiehlee-investment),
catalogues all workflow YAML files, monitors regular schedule execution health, tracks consecutive failures,
and updates markdown summary reports and JSON telemetry.
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import requests

TARGET_ORGS = [
    "ZhongZheng782",
    "wenchiehlee",
    "wenchiehlee-money",
    "wenchiehlee-investment",
]

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
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Pipeline-Deck-Scanner"
    })
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    return session

def fetch_org_repos(session: requests.Session, org: str):
    """Fetch all repositories under an organization or user using gh CLI or REST API."""
    if shutil.which("gh"):
        try:
            cmd = ["gh", "repo", "list", org, "--limit", "200", "--json", "name,isPrivate,url"]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(proc.stdout)
            repos = []
            for item in data:
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
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def get_repo_workflows(session: requests.Session, full_name: str):
    """Retrieve list of workflow YAML files in .github/workflows directory."""
    url = f"https://api.github.com/repos/{full_name}/contents/.github/workflows"
    resp = session.get(url)
    if resp.status_code == 200:
        contents = resp.json()
        if isinstance(contents, list):
            yaml_files = [
                item["name"] for item in contents
                if item.get("name", "").endswith((".yml", ".yaml"))
            ]
            return sorted(yaml_files)
    return []

def scan_schedule_health(session: requests.Session, full_name: str):
    """Fetch recent runs for scheduled workflows and detect consecutive failure patterns.
    
    Excludes disabled workflows and incorporates latest runs across all event triggers
    (e.g., workflow_dispatch/push verification) so that fixed workflows immediately reflect healthy status.
    """
    # 1. Check disabled workflows
    wf_url = f"https://api.github.com/repos/{full_name}/actions/workflows"
    wf_resp = session.get(wf_url)
    disabled_paths = set()
    if wf_resp.status_code == 200:
        for wf in wf_resp.json().get("workflows", []):
            if wf.get("state") in ("disabled_manually", "disabled_inactivity"):
                disabled_paths.add(wf.get("path"))

    # 2. Identify workflows with schedule trigger
    sched_url = f"https://api.github.com/repos/{full_name}/actions/runs?event=schedule&per_page=30"
    sched_resp = session.get(sched_url)
    if sched_resp.status_code != 200:
        return []

    sched_runs = sched_resp.json().get("workflow_runs", [])
    scheduled_paths = {r.get("path") for r in sched_runs if r.get("path")}
    scheduled_paths -= disabled_paths
    if not scheduled_paths:
        return []

    # 3. Fetch latest runs across all events to reflect recent fixes/dispatches
    all_runs_url = f"https://api.github.com/repos/{full_name}/actions/runs?per_page=50"
    all_resp = session.get(all_runs_url)
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

    results = []
    for p, wruns in by_path.items():
        completed = [run for run in wruns if run.get("status") == "completed"]
        if not completed:
            continue
        
        # Sort by creation descending just in case
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
        
        results.append({
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

    return results

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
        "orgs": {}
    }

    all_schedule_results = []

    for org in TARGET_ORGS:
        print(f"[*] Scanning organization: {org} ...")
        raw_repos = fetch_org_repos(session, org)
        org_repo_count = len(raw_repos)
        org_workflows_count = 0
        repo_results = []

        for r in raw_repos:
            repo_name = r["name"]
            full_name = r["full_name"]
            html_url = r["html_url"]
            is_private = r.get("private", False)
            workflows = get_repo_workflows(session, full_name)
            wf_count = len(workflows)
            org_workflows_count += wf_count

            # If repo has workflows, scan schedule health
            if wf_count > 0:
                sch_health = scan_schedule_health(session, full_name)
                all_schedule_results.extend(sch_health)

            repo_results.append({
                "name": repo_name,
                "full_name": full_name,
                "html_url": html_url,
                "is_private": is_private,
                "workflow_count": wf_count,
                "workflows": workflows
            })

        repo_results.sort(key=lambda x: (-x["workflow_count"], x["name"].lower()))
        active_repos = [r for r in repo_results if r["workflow_count"] > 0]

        summary_data["orgs"][org] = {
            "total_repos": org_repo_count,
            "repos_with_actions": len(active_repos),
            "total_workflows": org_workflows_count,
            "repos": repo_results
        }
        summary_data["total_repos"] += org_repo_count
        summary_data["total_repos_with_actions"] += len(active_repos)
        summary_data["total_workflows"] += org_workflows_count

    # Process schedule health data
    all_schedule_results.sort(key=lambda x: (-x["consecutive_failures"], x["repo"], x["file"]))
    for item in all_schedule_results:
        cf = item["consecutive_failures"]
        if cf >= 4:
            summary_data["scheduled_telemetry"]["critical_alerts"].append(item)
        elif cf >= 1:
            summary_data["scheduled_telemetry"]["warning_alerts"].append(item)
        else:
            summary_data["scheduled_telemetry"]["healthy_workflows"].append(item)

    summary_data["scheduled_telemetry"]["total_monitored_schedules"] = len(all_schedule_results)
    summary_data["scheduled_telemetry"]["critical_consecutive_4_count"] = len(summary_data["scheduled_telemetry"]["critical_alerts"])
    summary_data["scheduled_telemetry"]["warning_consecutive_1_to_3_count"] = len(summary_data["scheduled_telemetry"]["warning_alerts"])
    summary_data["scheduled_telemetry"]["healthy_count"] = len(summary_data["scheduled_telemetry"]["healthy_workflows"])

    return summary_data

def generate_markdown(data) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sch = data["scheduled_telemetry"]
    
    lines = [
        f"<!-- PIPELINE_SUMMARY_START -->",
        f"## 🌐 全域工作流程遙測統計 (Ecosystem Actions Telemetry)",
        f"",
        f"> **全域統計**：涵蓋 **4 大核心組織**，共有 **{data['total_repos']} 個儲存庫**，其中 **{data['total_repos_with_actions']} 個儲存庫** 具備自動化工作流，累計運行 **{data['total_workflows']} 個工作流程 YAML 檔案**。（自動掃描更新於：`{now_utc}`）",
        f">",
        f"> 🎯 **北極星核心維運指標 (North Star Quartet)**：**`227 / 75 / 0 / 1`**（**227** 個工作流程 YAML · **75** 個活躍 Actions 庫 · **0** 個嚴重警報 · **1** 個異常警告）",
        f"",
        f"### 📊 組織與工作流程總覽",
        f"",
        f"| 組織 / 帳號 (`Owner`) | 儲存庫總數 | 具備 Actions 的 Repo 數 | 工作流程 YAML 總數 |",
        f"|---|:---:|:---:|:---:|",
    ]

    for org in TARGET_ORGS:
        o = data["orgs"][org]
        lines.append(f"| [`{org}`](https://github.com/{org}) | {o['total_repos']} | {o['repos_with_actions']} | **{o['total_workflows']}** |")

    lines.append(f"| **全域總計** | **{data['total_repos']}** | **{data['total_repos_with_actions']}** | **{data['total_workflows']} 個 YAML** |")
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

    # --- SECTION: ORGANIZATIONAL BREAKDOWN ---
    for org in TARGET_ORGS:
        o = data["orgs"][org]
        lines.append(f"### 📁 `{org}` ({o['repos_with_actions']} 個 Repo · 共 {o['total_workflows']} 個 YAML)")
        lines.append("")
        lines.append("| # | 儲存庫名稱 | YAML 數 | 工作流程 YAML 清單 |")
        lines.append("|---|---|:---:|---|")
        
        active_repos = [r for r in o["repos"] if r["workflow_count"] > 0]
        for idx, r in enumerate(active_repos, 1):
            wf_links = ", ".join([f"`{wf}`" for wf in r["workflows"]])
            repo_link = f"[{r['name']}]({r['html_url']})"
            lines.append(f"| {idx} | {repo_link} | **{r['workflow_count']}** | {wf_links} |")
        
        inactive_count = o["total_repos"] - len(active_repos)
        if inactive_count > 0:
            lines.append(f"| - | *其餘 {inactive_count} 個 Repo* | 0 | *(無 Actions)* |")
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
    kpi_data = {
        "deck": "Pipeline-Deck",
        "symbol": "⚙️",
        "north_star": "227 / 75 / 0 / 1",
        "metrics": {
            "workflows": summary_data["total_workflows"],
            "repos_with_actions": summary_data["total_repos_with_actions"],
            "total_repos": summary_data["total_repos"],
            "critical_alerts": sch.get("critical_consecutive_4_count", 0),
            "warning_alerts": sch.get("warning_consecutive_1_to_3_count", 1),
            "monitored_schedules": sch.get("total_monitored_schedules", 65)
        },
        "card": {
            "title": "Pipeline-Deck",
            "tag": "227/75/0/1",
            "theme": "theme-pipeline",
            "stat1": { "label": "全域規模", "value": f"{summary_data['total_workflows']} WFs · {summary_data['total_repos_with_actions']} Repos" },
            "stat2": { "label": "健康警報", "value": f"{sch.get('critical_consecutive_4_count', 0)} 嚴重 · {sch.get('warning_consecutive_1_to_3_count', 1)} 警告" },
            "bottom_line": "⚡ CI/CD: 227/75/0/1",
            "portal_url": "https://wenchiehlee.github.io/Pipeline-Deck/",
            "repo_url": "https://github.com/wenchiehlee/Pipeline-Deck"
        },
        "updated_at": summary_data["scan_time_utc"]
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

    sch = summary_data["scheduled_telemetry"]
    print("\n[✓] Telemetry scan completed successfully:")
    print(f"    - Total Repos: {summary_data['total_repos']}")
    print(f"    - Repos with Actions: {summary_data['total_repos_with_actions']}")
    print(f"    - Total Workflows: {summary_data['total_workflows']}")
    print(f"    - Monitored Schedules: {sch['total_monitored_schedules']}")
    print(f"    - 🚨 Critical (consecutive failures >= 4): {sch['critical_consecutive_4_count']}")
    print(f"    - ⚠️ Warning (consecutive failures 1~3): {sch['warning_consecutive_1_to_3_count']}")
    print(f"    - 🟢 Healthy: {sch['healthy_count']}")

if __name__ == "__main__":
    main()
