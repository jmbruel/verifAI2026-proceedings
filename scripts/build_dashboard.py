#!/usr/bin/env python3
"""
Generate a self-contained, offline HTML proceedings status dashboard
(tracking/dashboard.html) directly from repository source files:
  - tracking/paper-tracking.md
  - submission/toc.csv
  - submission/springer-checklist.md
  - tracking/author-emails.md (optional: deadline & Cc lines)
  - tracking/drafts/*.eml (optional: existing Apple Mail drafts)
  - proceedings.pdf (optional: total compiled page count via pdfinfo)

Usage:
  python3 scripts/build_dashboard.py [--output tracking/dashboard.html]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def parse_paper_tracking(path: Path) -> list[dict]:
    papers: list[dict] = []
    if not path.exists():
        return papers

    lines = path.read_text(encoding="utf-8").splitlines()
    current: dict | None = None

    for raw in lines:
        line = raw.strip()
        if line.startswith("|") and line.endswith("|"):
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 10 and cols[0].isdigit():
                page_str = cols[6]
                pages = int(page_str) if page_str.isdigit() else 0
                current = {
                    "num": int(cols[0]),
                    "id": cols[1],
                    "title": cols[2],
                    "authors": cols[3],
                    "received": cols[4],
                    "sources": cols[5],
                    "pages": pages,
                    "ltp": cols[7],
                    "status": cols[8],
                    "build": cols[9],
                    "notes": [],
                    "corr": "",
                    "email": "",
                    "cc": "",
                    "part": "",
                    "startPage": "",
                    "folderNum": "",
                    "draft": None,
                }
                papers.append(current)
            continue

        if line.startswith(">") and current is not None:
            cleaned = re.sub(r"^>\s*", "", line)
            cleaned = re.sub(r"\*\*(?:Failure note|Note)\s*\(#\d+\):\*\*\s*", "", cleaned)
            cleaned = cleaned.replace("`", "")
            current["notes"].append(cleaned)

    return papers


def merge_toc_csv(papers: list[dict], path: Path) -> None:
    if not path.exists():
        return

    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    by_title = {r.get("Paper Title", "").strip().lower(): r for r in rows}

    for idx, p in enumerate(papers):
        row = by_title.get(p["title"].strip().lower())
        if row is None and idx < len(rows):
            row = rows[idx]
        if row:
            p["part"] = (row.get("Part Titles") or "").strip()
            p["startPage"] = (row.get("Starting Page") or "").strip()
            p["corr"] = (row.get("Corresponding Author Name") or "").strip()
            p["email"] = (row.get("Corresponding Author Email") or "").strip()
            p["folderNum"] = (row.get("Submission Folder Number") or "").strip()


def merge_author_emails(papers: list[dict], path: Path) -> str:
    deadline = ""
    if not path.exists():
        return deadline

    text = path.read_text(encoding="utf-8")
    m = re.search(r"Deadline across all emails:\s*\*\*([^*]+)\*\*", text)
    if m:
        deadline = m.group(1).strip()

    # Extract Cc: lines per paper section
    sections = re.split(r"^###\s+Paper\s+#(\d+)\s+\(`?(\d+)`?\)", text, flags=re.M)
    # sections = [preamble, num1, id1, body1, num2, id2, body2, ...]
    by_id = {p["id"]: p for p in papers}
    for i in range(1, len(sections) - 2, 3):
        sub_id = sections[i + 1]
        body = sections[i + 2]
        cc_m = re.search(r"^Cc:\s*(.+)$", body, flags=re.M)
        if cc_m and sub_id in by_id:
            by_id[sub_id]["cc"] = cc_m.group(1).strip()

    return deadline


def merge_drafts(papers: list[dict], drafts_dir: Path) -> None:
    if not drafts_dir.is_dir():
        return
    emls = sorted(p.name for p in drafts_dir.glob("*.eml"))
    for p in papers:
        needle = f"-{p['id']}-"
        for fn in emls:
            if needle in fn or fn.startswith(f"{p['id']}-"):
                p["draft"] = fn
                break


def enrich_rules(papers: list[dict]) -> None:
    for p in papers:
        note = " ".join(p["notes"]).strip()
        p["note"] = note
        del p["notes"]

        low = note.lower()
        status = p["status"]
        received_ok = p["received"] not in ("No", "Pending", "—", "")
        ltp_ok = p["ltp"] not in ("No", "Pending", "—", "")

        cr1 = "cr-1" not in low and (p["pages"] == 0 or 6 <= p["pages"] <= 20)
        cr2 = "cr-2" not in low
        cr3 = "cr-3" not in low
        cr4 = "cr-4" not in low and ltp_ok
        cr5 = "cr-5" not in low

        if status == "Pending" or not received_ok:
            cr1 = cr2 = cr3 = cr4 = cr5 = False

        p["rules"] = {"cr1": cr1, "cr2": cr2, "cr3": cr3, "cr4": cr4, "cr5": cr5}

        if not ltp_ok:
            p["ltpStatus"] = "unsigned" if "unsigned" in low else "missing"
        elif ".docx" in low:
            p["ltpStatus"] = "docx"
        else:
            p["ltpStatus"] = "ok"

        if status == "Pass":
            p["category"] = "pass"
        elif status == "Pending" or not received_ok:
            p["category"] = "missing"
        elif not cr4:
            p["category"] = "ltp"
        else:
            p["category"] = "cr5"


def parse_checklist(path: Path) -> list[dict]:
    groups: list[dict] = []
    if not path.exists():
        return groups

    current_group: dict | None = None
    idx = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current_group = {"group": line[3:].strip(), "items": []}
            groups.append(current_group)
            continue
        m = re.match(r"^-\s*\[([ xX])\]\s*\*\*(.+?)\*\*\s*(?:[—-]\s*(.*))?$", line)
        if m and current_group is not None:
            idx += 1
            current_group["items"].append(
                {
                    "id": f"chk-{idx}",
                    "done": m.group(1).lower() == "x",
                    "label": m.group(2).strip(),
                    "meta": (m.group(3) or "").strip(),
                }
            )
    return groups


def parse_volume_number(checklist_path: Path) -> str:
    if not checklist_path.exists():
        return ""
    m = re.search(r"Assigned:\s*(LNCS\s+\d+)", checklist_path.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def get_pdf_pages(pdf_path: Path) -> int | None:
    if not pdf_path.exists():
        return None
    try:
        out = subprocess.check_output(["pdfinfo", str(pdf_path)], text=True, stderr=subprocess.DEVNULL)
        m = re.search(r"^Pages:\s*(\d+)", out, flags=re.M)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def build_html(payload: dict) -> str:
    data_json = json.dumps(payload, ensure_ascii=False)
    # Prevent closing </script> inside JSON strings
    data_json = data_json.replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VERIF-AI 2026 — Proceedings Dashboard</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --card: #ffffff;
      --content: #f1f3f6;
      --border: #dfe3ea;
      --divider: #e8ebf0;
      --fg: #141923;
      --muted: #5c6678;
      --primary: #2563eb;
      --primary-fg: #ffffff;
      --link: #1d4ed8;
      --code: #0f4c81;
      --success: #15803d;
      --success-bg: rgba(21, 128, 61, 0.12);
      --warning: #b45309;
      --warning-bg: rgba(180, 83, 9, 0.14);
      --error: #b91c1c;
      --error-bg: rgba(185, 28, 28, 0.12);
      --chart-1: #2563eb;
      --chart-2: #0284c7;
      --shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }}
    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --bg: #0e1116;
        --card: #161b22;
        --content: #1d232c;
        --border: #2c3543;
        --divider: #242c38;
        --fg: #e6edf3;
        --muted: #919ba8;
        --primary: #3b82f6;
        --primary-fg: #ffffff;
        --link: #60a5fa;
        --code: #93c5fd;
        --success: #4ade80;
        --success-bg: rgba(74, 222, 128, 0.14);
        --warning: #fbbf24;
        --warning-bg: rgba(251, 191, 36, 0.15);
        --error: #f87171;
        --error-bg: rgba(248, 113, 113, 0.15);
        --chart-1: #60a5fa;
        --chart-2: #38bdf8;
        --shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
      }}
    }}
    :root[data-theme="dark"] {{
      --bg: #0e1116;
      --card: #161b22;
      --content: #1d232c;
      --border: #2c3543;
      --divider: #242c38;
      --fg: #e6edf3;
      --muted: #919ba8;
      --primary: #3b82f6;
      --primary-fg: #ffffff;
      --link: #60a5fa;
      --code: #93c5fd;
      --success: #4ade80;
      --success-bg: rgba(74, 222, 128, 0.14);
      --warning: #fbbf24;
      --warning-bg: rgba(251, 191, 36, 0.15);
      --error: #f87171;
      --error-bg: rgba(248, 113, 113, 0.15);
      --chart-1: #60a5fa;
      --chart-2: #38bdf8;
      --shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 20px;
      background: var(--bg);
      color: var(--fg);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
    }}
    .wrap {{ max-width: 1280px; margin: 0 auto; display: flex; flex-direction: column; gap: 18px; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: var(--shadow);
    }}
    .header {{
      display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px;
    }}
    h1 {{ margin: 4px 0 2px; font-size: 20px; font-weight: 650; letter-spacing: -0.01em; }}
    h2 {{ margin: 0 0 2px; font-size: 14px; font-weight: 650; }}
    h3 {{ margin: 0; font-size: 13.5px; font-weight: 650; }}
    .muted {{ color: var(--muted); font-size: 12px; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .tabular {{ font-variant-numeric: tabular-nums; }}
    .row {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }}
    .between {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; }}
    .badge {{
      display: inline-flex; align-items: center; padding: 2px 9px; border-radius: 999px;
      font-size: 12px; font-weight: 550; white-space: nowrap; border: 1px solid transparent;
    }}
    .b-neutral {{ background: var(--content); color: var(--muted); border-color: var(--border); }}
    .b-success {{ background: var(--success-bg); color: var(--success); }}
    .b-warning {{ background: var(--warning-bg); color: var(--warning); }}
    .b-error {{ background: var(--error-bg); color: var(--error); }}
    .btn {{
      appearance: none; border: 1px solid var(--border); background: var(--content); color: var(--fg);
      border-radius: 8px; padding: 6px 12px; font-size: 12px; font-weight: 550; cursor: pointer;
      transition: opacity 0.15s, background 0.15s, border-color 0.15s;
    }}
    .btn:hover {{ opacity: 0.88; }}
    .btn-primary, .btn[aria-selected="true"], .btn[aria-pressed="true"] {{
      background: var(--primary); color: var(--primary-fg); border-color: var(--primary);
    }}
    .kpis {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }}
    @media (max-width: 1024px) {{ .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 560px) {{ .kpis {{ grid-template-columns: 1fr; }} }}
    .kpi-val {{ font-size: 24px; font-weight: 700; margin-top: 4px; display: flex; align-items: baseline; gap: 8px; }}
    .track {{ height: 6px; border-radius: 999px; background: var(--content); overflow: hidden; margin: 9px 0 6px; }}
    .fill {{ height: 100%; border-radius: 999px; }}
    .charts-grid {{ display: grid; grid-template-columns: 7fr 5fr; gap: 14px; }}
    @media (max-width: 980px) {{ .charts-grid {{ grid-template-columns: 1fr; }} }}
    .legend {{ display: flex; gap: 12px; font-size: 12px; color: var(--muted); flex-wrap: wrap; }}
    .dot {{ width: 9px; height: 9px; border-radius: 2px; display: inline-block; margin-right: 4px; }}
    .donut-wrap {{ display: flex; align-items: center; gap: 20px; margin: 10px 0; flex-wrap: wrap; }}
    .rule-list {{ flex: 1; min-width: 210px; display: flex; flex-direction: column; gap: 10px; }}
    .rule-btn {{ background: none; border: none; padding: 0; text-align: left; width: 100%; color: inherit; cursor: pointer; }}
    .rule-btn:hover .rule-name {{ text-decoration: underline; }}
    .controls {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; margin-bottom: 12px; }}
    .input, .select {{
      border: 1px solid var(--border); background: var(--content); color: var(--fg);
      border-radius: 8px; padding: 6px 10px; font-size: 12px; outline: none;
    }}
    .input {{ min-width: 240px; }}
    .input:focus, .select:focus {{ border-color: var(--primary); }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--divider); border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left; }}
    thead tr {{ background: var(--content); color: var(--muted); border-bottom: 1px solid var(--divider); }}
    th, td {{ padding: 9px 11px; vertical-align: middle; }}
    tbody tr {{ border-bottom: 1px solid var(--divider); }}
    tbody tr:last-child {{ border-bottom: none; }}
    tbody tr.paper-row {{ cursor: pointer; }}
    tbody tr.paper-row:hover, tbody tr.paper-row.open {{ background: var(--content); }}
    .title-cell {{ font-weight: 560; }}
    .authors-sub {{ color: var(--muted); font-size: 12px; margin-top: 2px; max-width: 560px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .detail-row td {{ background: var(--content); padding: 12px 16px; }}
    .detail-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 14px; }}
    @media (max-width: 780px) {{ .detail-grid {{ grid-template-columns: 1fr; }} }}
    .note-box {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; font-size: 12px; }}
    .cards-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    @media (max-width: 820px) {{ .cards-2 {{ grid-template-columns: 1fr; }} }}
    .action-card {{ display: flex; flex-direction: column; justify-content: space-between; gap: 12px; }}
    .chk-item {{ display: flex; align-items: flex-start; gap: 9px; cursor: pointer; font-size: 12.5px; }}
    .chk-item input {{ margin-top: 3px; accent-color: var(--primary); cursor: pointer; }}
    .done-text {{ text-decoration: line-through; color: var(--muted); }}
    .hidden {{ display: none !important; }}
    .bar-g {{ cursor: pointer; }}
    .bar-g:hover rect {{ opacity: 0.82; }}
    .toast {{
      position: fixed; right: 18px; bottom: 18px; padding: 8px 14px; border-radius: 8px;
      background: var(--card); color: var(--fg); border: 1px solid var(--border);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18); font-size: 12px; opacity: 0;
      pointer-events: none; transition: opacity 0.2s;
    }}
    .toast.show {{ opacity: 1; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="card header">
      <div>
        <div class="row" id="header-badges"></div>
        <h1>VERIF-AI 2026 — Proceedings Production Dashboard</h1>
        <div class="muted" id="header-sub"></div>
      </div>
      <div class="row">
        <nav class="row" role="tablist" aria-label="Dashboard tabs">
          <button class="btn" role="tab" aria-selected="true" data-tab="overview" id="tab-btn-overview">Overview &amp; Papers</button>
          <button class="btn" role="tab" aria-selected="false" data-tab="actions" id="tab-btn-actions">Action Queue</button>
          <button class="btn" role="tab" aria-selected="false" data-tab="checklist">Springer Checklist</button>
        </nav>
        <button class="btn" id="theme-toggle" title="Toggle light/dark theme">Theme</button>
      </div>
    </header>

    <section class="kpis" id="kpi-strip"></section>

    <div id="tab-overview" class="wrap" style="gap: 16px;">
      <section class="charts-grid">
        <div class="card">
          <div class="between" style="margin-bottom: 10px;">
            <div>
              <h2>Page Counts by Paper (click a bar to inspect)</h2>
              <div class="muted">Guides: 6 pp short-paper · 12 pp full-paper · 20 pp soft cap</div>
            </div>
            <div class="legend">
              <span><span class="dot" style="background:var(--success)"></span>Pass</span>
              <span><span class="dot" style="background:var(--warning)"></span>CR-5 / Minor</span>
              <span><span class="dot" style="background:var(--error)"></span>LTP / Missing</span>
            </div>
          </div>
          <div id="page-chart" style="overflow-x:auto;"></div>
        </div>

        <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <h2>Compliance Rule Breakdown</h2>
            <div class="muted">Click any rule with failures to filter the table</div>
          </div>
          <div class="donut-wrap">
            <div id="donut-chart"></div>
            <div id="rule-bars" class="rule-list"></div>
          </div>
          <div class="between muted" style="border-top:1px solid var(--divider); padding-top:10px;" id="length-stats"></div>
        </div>
      </section>

      <section class="card">
        <div class="controls">
          <div class="row" id="filter-pills"></div>
          <div class="row">
            <input id="search-input" class="input" type="search" placeholder="Filter by #, ID, title, author, email..." />
            <select id="sort-select" class="select">
              <option value="num">Sort: Paper #</option>
              <option value="status">Sort: Fails first</option>
              <option value="pages-desc">Sort: Pages (high→low)</option>
              <option value="pages-asc">Sort: Pages (low→high)</option>
              <option value="id">Sort: Sub. ID</option>
            </select>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="width:46px">#</th>
                <th style="width:62px">ID</th>
                <th>Title &amp; Authors</th>
                <th style="width:64px; text-align:right;">Pages</th>
                <th style="width:118px">LTP</th>
                <th style="width:94px">Status</th>
                <th style="width:66px; text-align:center;">Build</th>
              </tr>
            </thead>
            <tbody id="papers-tbody"></tbody>
          </table>
        </div>
        <div class="between muted" style="margin-top:10px;" id="table-footer"></div>
      </section>
    </div>

    <div id="tab-actions" class="hidden wrap" style="gap: 14px;">
      <div class="card between">
        <div>
          <h2 id="actions-title">Pending Author Follow-Ups</h2>
          <div class="muted">Draft emails live in <code>tracking/drafts/</code> (open in Apple Mail and press ⇧⌘D to send).</div>
        </div>
        <button class="btn btn-primary" id="copy-all-emails">Copy All Pending Emails</button>
      </div>
      <div id="action-cards" class="wrap" style="gap: 16px;"></div>
    </div>

    <div id="tab-checklist" class="hidden wrap" style="gap: 14px;">
      <div class="card between">
        <div>
          <h2>Springer Submission Checklist</h2>
          <div class="muted">Parsed live from <code>submission/springer-checklist.md</code>. Local clicks persist in browser storage.</div>
        </div>
        <div class="row">
          <span id="checklist-progress" class="mono tabular" style="font-weight:650; font-size:13px;"></span>
          <button class="btn" id="reset-checklist">Reset to Markdown</button>
        </div>
      </div>
      <div id="checklist-grid" class="cards-2"></div>
    </div>
  </div>

  <div id="toast" class="toast"></div>

  <script>
    const DATA = {data_json};
    const PAPERS = DATA.papers;
    const CHECKLIST = DATA.checklist;
    const STORAGE_KEY = "verifai2026_repo_checklist_v1";

    let activeFilter = "all";
    let searchQuery = "";
    let sortBy = "num";
    let expandedId = null;
    let chkState = loadChk();

    function loadChk() {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) return JSON.parse(raw);
      }} catch (e) {{}}
      const s = {{}};
      CHECKLIST.forEach(g => g.items.forEach(i => {{ s[i.id] = i.done; }}));
      return s;
    }}

    function saveChk() {{
      try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(chkState)); }} catch (e) {{}}
    }}

    function esc(str) {{
      return String(str || "").replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));
    }}

    function badge(text, cls) {{
      return `<span class="badge b-${{cls}}">${{esc(text)}}</span>`;
    }}

    function showToast(msg) {{
      const el = document.getElementById("toast");
      el.textContent = msg;
      el.classList.add("show");
      clearTimeout(window.__t);
      window.__t = setTimeout(() => el.classList.remove("show"), 2100);
    }}

    function copyText(text, label) {{
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => showToast("Copied: " + label)).catch(() => fallbackCopy(text, label));
      }} else {{
        fallbackCopy(text, label);
      }}
    }}

    function fallbackCopy(text, label) {{
      const ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try {{ document.execCommand("copy"); showToast("Copied: " + label); }} catch (e) {{}}
      document.body.removeChild(ta);
    }}

    // Theme toggle
    document.getElementById("theme-toggle").addEventListener("click", () => {{
      const root = document.documentElement;
      const cur = root.getAttribute("data-theme");
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const next = cur ? (cur === "dark" ? "light" : "dark") : (prefersDark ? "light" : "dark");
      root.setAttribute("data-theme", next);
    }});

    // Tabs
    document.querySelectorAll('[role="tab"]').forEach(btn => {{
      btn.addEventListener("click", () => {{
        const target = btn.dataset.tab;
        document.querySelectorAll('[role="tab"]').forEach(b => b.setAttribute("aria-selected", b === btn ? "true" : "false"));
        ["overview", "actions", "checklist"].forEach(id => {{
          document.getElementById("tab-" + id).classList.toggle("hidden", id !== target);
        }});
      }});
    }});

    function renderHeaderAndKPIs() {{
      const total = PAPERS.length;
      const received = PAPERS.filter(p => p.received !== "No" && p.received !== "Pending" && p.received !== "—").length;
      const buildsOk = PAPERS.filter(p => p.build === "OK").length;
      const passed = PAPERS.filter(p => p.status === "Pass").length;
      const failed = PAPERS.filter(p => p.status !== "Pass").length;
      const wetLtp = PAPERS.filter(p => p.rules.cr4).length;
      const ltpBlockers = PAPERS.filter(p => p.category === "ltp" || p.category === "missing").length;
      const paperPages = PAPERS.reduce((s, p) => s + p.pages, 0);
      const volPages = DATA.proceedingsPages || paperPages;
      const fullCount = PAPERS.filter(p => p.pages >= 12).length;
      const fullPct = total ? ((fullCount / total) * 100).toFixed(1) : "0.0";
      const passPct = total ? ((passed / total) * 100).toFixed(1) : "0.0";
      const recPct = total ? Math.round((received / total) * 100) : 0;
      const volPct = Math.min(100, Math.round((volPages / 700) * 100));

      document.getElementById("header-badges").innerHTML =
        badge(DATA.volumeNumber ? "Springer " + DATA.volumeNumber : "Springer LNCS", "neutral") +
        badge("Generated: " + DATA.generatedAt, "neutral") +
        (DATA.deadline ? badge("Author Deadline: " + DATA.deadline, "warning") : "");

      document.getElementById("header-sub").textContent =
        `Volume Editors: Jean-Michel Bruel & Bertrand Meyer · ${{total}} Accepted Papers · Live view from tracking/paper-tracking.md & submission/toc.csv`;

      document.getElementById("tab-btn-overview").textContent = `Overview & Papers (${{total}})`;
      document.getElementById("tab-btn-actions").textContent = `Action Queue (${{failed}})`;

      document.getElementById("kpi-strip").innerHTML = `
        <div class="card">
          <div class="muted">Submissions Received</div>
          <div class="kpi-val tabular">${{received}} / ${{total}} <span style="font-size:12px; color:var(--success)">${{recPct}}%</span></div>
          <div class="track"><div class="fill" style="width:${{recPct}}%; background:var(--success)"></div></div>
          <div class="muted">${{buildsOk}} / ${{total}} LaTeX builds OK</div>
        </div>
        <div class="card">
          <div class="muted">Compliance Ready</div>
          <div class="kpi-val tabular">${{passed}} / ${{total}} <span style="font-size:12px; color:${{failed ? 'var(--warning)' : 'var(--success)'}}">${{passPct}}%</span></div>
          <div class="track"><div class="fill" style="width:${{passPct}}%; background:var(--success)"></div></div>
          <div class="muted">${{failed}} paper${{failed === 1 ? '' : 's'}} needing follow-up</div>
        </div>
        <div class="card">
          <div class="muted">Wet-Signed LTPs</div>
          <div class="kpi-val tabular">${{wetLtp}} / ${{total}} <span style="font-size:12px; color:${{ltpBlockers ? 'var(--error)' : 'var(--success)'}}">${{ltpBlockers}} blocker${{ltpBlockers === 1 ? '' : 's'}}</span></div>
          <div class="track"><div class="fill" style="width:${{total ? Math.round((wetLtp/total)*100) : 0}}%; background:var(--chart-1)"></div></div>
          <div class="muted">${{PAPERS.filter(p => !p.rules.cr4).map(p => '#' + p.num + ' ' + p.ltpStatus).join(' · ') || 'All wet-signed LTPs received'}}</div>
        </div>
        <div class="card">
          <div class="muted">Total Volume Size</div>
          <div class="kpi-val tabular">${{volPages}} pp <span class="muted">/ 700 max</span></div>
          <div class="track"><div class="fill" style="width:${{volPct}}%; background:${{volPages > 700 ? 'var(--error)' : 'var(--chart-2)'}}"></div></div>
          <div class="muted">${{paperPages}} paper pp${{DATA.proceedingsPages ? ' + ' + (volPages - paperPages) + ' front/parts' : ''}}</div>
        </div>
        <div class="card">
          <div class="muted">Full-Paper Ratio (≥12p)</div>
          <div class="kpi-val tabular">${{fullPct}}% <span style="font-size:12px; color:${{Number(fullPct) >= 66.7 ? 'var(--success)' : 'var(--error)'}}">${{fullCount}} / ${{total}}</span></div>
          <div class="track"><div class="fill" style="width:${{fullPct}}%; background:${{Number(fullPct) >= 66.7 ? 'var(--success)' : 'var(--error)'}}"></div></div>
          <div class="muted">Springer floor: ≥ 66.7% (2/3)</div>
        </div>`;

      const counts = PAPERS.map(p => p.pages).filter(n => n > 0).sort((a, b) => a - b);
      const avg = counts.length ? (counts.reduce((a, b) => a + b, 0) / counts.length).toFixed(1) : "—";
      const med = counts.length ? counts[Math.floor(counts.length / 2)] : "—";
      const rng = counts.length ? `${{counts[0]}} – ${{counts[counts.length - 1]}} pp` : "—";
      document.getElementById("length-stats").innerHTML =
        `<span>Avg length: <strong style="color:var(--fg)" class="tabular">${{avg}} pp</strong></span>
         <span>Median: <strong style="color:var(--fg)" class="tabular">${{med}} pp</strong></span>
         <span>Range: <strong style="color:var(--fg)" class="tabular">${{rng}}</strong></span>`;

      const cr5Fails = PAPERS.filter(p => !p.rules.cr5).length;
      const shorts = PAPERS.filter(p => p.pages > 0 && p.pages < 12).length;
      const pills = [
        ["all", `All (${{total}})`],
        ["pass", `Ready / Pass (${{passed}})`],
        ["fail", `Needs Action (${{failed}})`],
        ["ltp", `LTP Blockers (${{ltpBlockers}})`],
        ["cr5", `Missing CR-5 (${{cr5Fails}})`],
        ["short", `Short <12 pp (${{shorts}})`]
      ];
      document.getElementById("filter-pills").innerHTML = pills.map(([k, lbl]) =>
        `<button class="btn" aria-pressed="${{activeFilter === k}}" data-filter="${{k}}" onclick="applyFilter('${{k}}')">${{lbl}}</button>`
      ).join("");
    }}

    function renderPageChart() {{
      const w = 660, h = 212, padL = 32, padR = 12, padT = 18, padB = 28;
      const plotW = w - padL - padR, plotH = h - padT - padB;
      const maxP = Math.max(22, ...PAPERS.map(p => p.pages + 2));
      const step = plotW / Math.max(1, PAPERS.length);
      const barW = Math.max(10, step - 6);
      const yOf = v => padT + plotH - (v / maxP) * plotH;

      let svg = `<svg viewBox="0 0 ${{w}} ${{h}}" style="width:100%; height:auto; display:block;" role="img" aria-label="Page count chart">`;
      [
        {{ v: 6, label: "6p", color: "var(--muted)" }},
        {{ v: 12, label: "12p", color: "var(--chart-2)" }},
        {{ v: 20, label: "20p", color: "var(--warning)" }}
      ].forEach(g => {{
        const y = yOf(g.v);
        svg += `<line x1="${{padL}}" y1="${{y}}" x2="${{w - padR}}" y2="${{y}}" stroke="${{g.color}}" stroke-dasharray="3 3" stroke-opacity="0.55" stroke-width="1"/>`;
        svg += `<text x="${{padL - 5}}" y="${{y + 3}}" text-anchor="end" font-size="10" fill="var(--muted)">${{g.label}}</text>`;
      }});
      svg += `<line x1="${{padL}}" y1="${{padT + plotH}}" x2="${{w - padR}}" y2="${{padT + plotH}}" stroke="var(--border)" stroke-width="1"/>`;

      PAPERS.forEach((p, idx) => {{
        const x = padL + idx * step + (step - barW) / 2;
        const barH = (p.pages / maxP) * plotH;
        const y = padT + plotH - barH;
        const fill = p.status === "Pass" ? "var(--success)" : ((p.category === "ltp" || p.category === "missing") ? "var(--error)" : "var(--warning)");
        const sel = expandedId === p.id;
        svg += `<g class="bar-g" onclick="inspectPaper('${{p.id}}')">
          <title>#${{p.num}} (${{p.id}}) — ${{p.pages}} pp — ${{p.status}}</title>
          <rect x="${{x}}" y="${{y}}" width="${{barW}}" height="${{Math.max(2, barH)}}" rx="3" fill="${{fill}}" ${{sel ? 'stroke="var(--fg)" stroke-width="2"' : ''}}/>
          <text x="${{x + barW / 2}}" y="${{y - 4}}" text-anchor="middle" font-size="9.5" fill="var(--muted)">${{p.pages || "—"}}</text>
          <text x="${{x + barW / 2}}" y="${{h - 10}}" text-anchor="middle" font-size="9.5" fill="var(--muted)">#${{p.num}}</text>
        </g>`;
      }});
      svg += `</svg>`;
      document.getElementById("page-chart").innerHTML = svg;
    }}

    function renderComplianceChart() {{
      const total = PAPERS.length || 1;
      const passC = PAPERS.filter(p => p.status === "Pass").length;
      const cr5C = PAPERS.filter(p => p.category === "cr5").length;
      const ltpC = PAPERS.filter(p => p.category === "ltp" || p.category === "missing").length;

      const r = 46, cx = 62, cy = 62, sw = 14, C = 2 * Math.PI * r;
      let offset = 0, circles = "";
      [
        {{ c: passC, col: "var(--success)" }},
        {{ c: cr5C, col: "var(--warning)" }},
        {{ c: ltpC, col: "var(--error)" }}
      ].forEach(s => {{
        const len = (s.c / total) * C;
        circles += `<circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="none" stroke="${{s.col}}" stroke-width="${{sw}}"
          stroke-dasharray="${{len}} ${{C - len}}" stroke-dashoffset="${{-offset}}" transform="rotate(-90 ${{cx}} ${{cy}})"/>`;
        offset += len;
      }});

      document.getElementById("donut-chart").innerHTML = `
        <svg width="124" height="124" viewBox="0 0 124 124">
          <circle cx="${{cx}}" cy="${{cy}}" r="${{r}}" fill="none" stroke="var(--content)" stroke-width="${{sw}}"/>
          ${{circles}}
          <text x="${{cx}}" y="${{cy - 2}}" text-anchor="middle" font-size="20" font-weight="700" fill="var(--fg)">${{passC}}/${{PAPERS.length}}</text>
          <text x="${{cx}}" y="${{cy + 14}}" text-anchor="middle" font-size="11" fill="var(--muted)">Ready</text>
        </svg>`;

      const rules = [
        ["cr1", "CR-1 Page Limits (6–20 pp)", "short"],
        ["cr2", "CR-2 LNCS Template & Build", "all"],
        ["cr3", "CR-3 Author Consistency", "all"],
        ["cr4", "CR-4 Wet-Signed LTP", "ltp"],
        ["cr5", "CR-5 Disclosure of Interests", "cr5"]
      ];
      document.getElementById("rule-bars").innerHTML = rules.map(([k, lbl, flt]) => {{
        const ok = PAPERS.filter(p => p.rules[k]).length;
        const pct = Math.round((ok / total) * 100);
        const fail = PAPERS.length - ok;
        const col = fail === 0 ? "var(--success)" : (k === "cr4" ? "var(--error)" : "var(--warning)");
        return `<button class="rule-btn" onclick="applyFilter('${{flt}}')">
          <div class="between" style="margin-bottom:4px; font-size:12px;">
            <span class="rule-name">${{lbl}}</span>
            <span class="mono tabular muted">${{ok}}/${{PAPERS.length}}</span>
          </div>
          <div class="track" style="margin:0;"><div class="fill" style="width:${{pct}}%; background:${{col}}"></div></div>
        </button>`;
      }}).join("");
    }}

    function applyFilter(f) {{
      activeFilter = f;
      document.querySelectorAll("#filter-pills button").forEach(b => {{
        b.setAttribute("aria-pressed", b.dataset.filter === f ? "true" : "false");
      }});
      renderTable();
    }}

    function matchesFilter(p) {{
      if (activeFilter === "pass" && p.status !== "Pass") return false;
      if (activeFilter === "fail" && p.status === "Pass") return false;
      if (activeFilter === "ltp" && p.category !== "ltp" && p.category !== "missing") return false;
      if (activeFilter === "cr5" && p.rules.cr5) return false;
      if (activeFilter === "short" && !(p.pages > 0 && p.pages < 12)) return false;
      if (searchQuery) {{
        const q = searchQuery.toLowerCase();
        const hay = `#${{p.num}} ${{p.id}} ${{p.title}} ${{p.authors}} ${{p.corr}} ${{p.email}} ${{p.note}}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }}
      return true;
    }}

    function inspectPaper(id) {{
      const p = PAPERS.find(x => x.id === id);
      if (p && activeFilter !== "all" && !matchesFilter(p)) applyFilter("all");
      expandedId = expandedId === id ? null : id;
      renderPageChart();
      renderTable();
      if (expandedId) {{
        const el = document.getElementById("row-" + id);
        if (el) el.scrollIntoView({{ behavior: "smooth", block: "nearest" }});
      }}
    }}

    function renderTable() {{
      let rows = PAPERS.filter(matchesFilter);
      if (sortBy === "num") rows.sort((a, b) => a.num - b.num);
      else if (sortBy === "id") rows.sort((a, b) => Number(a.id) - Number(b.id));
      else if (sortBy === "pages-desc") rows.sort((a, b) => b.pages - a.pages || a.num - b.num);
      else if (sortBy === "pages-asc") rows.sort((a, b) => a.pages - b.pages || a.num - b.num);
      else if (sortBy === "status") rows.sort((a, b) => (a.status === b.status ? a.num - b.num : (a.status === "Pass" ? 1 : -1)));

      const tbody = document.getElementById("papers-tbody");
      if (!rows.length) {{
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:28px;" class="muted">No papers match the current filter.</td></tr>`;
      }} else {{
        tbody.innerHTML = rows.map(p => {{
          const open = expandedId === p.id;
          const ltpCell = p.ltpStatus === "ok" ? badge(p.ltp, "success")
            : p.ltpStatus === "docx" ? badge(".docx (PDF?)", "warning")
            : p.ltpStatus === "unsigned" ? badge("Unsigned p.5", "error")
            : badge("Missing", "error");
          const stCell = p.status === "Pass" ? badge("Pass", "success")
            : p.category === "ltp" || p.category === "missing" ? badge("Blocker", "error")
            : badge("Fail", "warning");
          const bldCell = badge(p.build, p.build === "OK" ? "success" : "warning");

          let html = `<tr id="row-${{p.id}}" class="paper-row ${{open ? 'open' : ''}}" onclick="inspectPaper('${{p.id}}')">
            <td class="mono muted">#${{p.num}}</td>
            <td class="mono">${{esc(p.id)}}</td>
            <td>
              <div class="title-cell">${{esc(p.title)}}</div>
              <div class="authors-sub">${{esc(p.authors)}}</div>
            </td>
            <td class="mono tabular" style="text-align:right; ${{p.pages > 0 && p.pages < 6 ? 'color:var(--warning); font-weight:700;' : ''}}">${{p.pages || "—"}}</td>
            <td>${{ltpCell}}</td>
            <td>${{stCell}}</td>
            <td style="text-align:center;">${{bldCell}}</td>
          </tr>`;

          if (open) {{
            const rBadges = ["cr1","cr2","cr3","cr4","cr5"].map(k => badge(k.toUpperCase() + (p.rules[k] ? " ✓" : " ✕"), p.rules[k] ? "success" : "error")).join(" ");
            html += `<tr class="detail-row"><td colspan="7">
              <div class="detail-grid">
                <div style="display:flex; flex-direction:column; gap:8px;">
                  <div class="row">${{rBadges}}</div>
                  <div style="font-size:12px;"><span class="muted">Authors:</span> ${{esc(p.authors)}}</div>
                  <div class="note-box">${{p.note ? esc(p.note) : '<span class="muted">No compliance issues or minor notes.</span>'}}</div>
                </div>
                <div class="note-box" style="display:flex; flex-direction:column; gap:6px;">
                  <div><span class="muted">Folder:</span> <code class="mono" style="color:var(--code)">papers/p${{esc(p.id)}}/</code></div>
                  <div><span class="muted">Received:</span> ${{esc(p.received)}}</div>
                  <div><span class="muted">Corresponding:</span> ${{esc(p.corr || "—")}}</div>
                  <div class="between">
                    <code class="mono" style="color:var(--link); word-break:break-all;">${{esc(p.email || "—")}}</code>
                    ${{p.email ? `<button class="btn" style="padding:3px 8px;" onclick="event.stopPropagation(); copyText('${{esc(p.email)}}','${{esc(p.email)}}')">Copy</button>` : ""}}
                  </div>
                  ${{p.draft ? `<div class="muted">Draft: <code class="mono" style="color:var(--code)">${{esc(p.draft)}}</code></div>` : ""}}
                </div>
              </div>
            </td></tr>`;
          }}
          return html;
        }}).join("");
      }}

      const sumP = rows.reduce((s, p) => s + p.pages, 0);
      document.getElementById("table-footer").innerHTML =
        `<span>Showing <strong style="color:var(--fg)">${{rows.length}}</strong> of ${{PAPERS.length}} papers (click any row for details)</span>
         <span>Subset pages: <strong style="color:var(--fg)" class="mono tabular">${{sumP}} pp</strong></span>`;
    }}

    function renderActions() {{
      const pending = PAPERS.filter(p => p.status !== "Pass");
      document.getElementById("actions-title").textContent =
        `Pending Author Follow-Ups (${{pending.length}} Paper${{pending.length === 1 ? '' : 's'}}${{DATA.deadline ? ' · Deadline ' + DATA.deadline : ''}})`;

      const groups = [
        ["Missing Submissions", "Camera-ready package not yet received.", pending.filter(p => p.category === "missing"), "error"],
        ["Critical LTP Blockers", "Cannot submit to Springer until wet-signed 5-page LNCS LTP PDFs arrive.", pending.filter(p => p.category === "ltp"), "error"],
        ["CR-5 & Camera-Ready Fixes", "Missing Disclosure of Interests section, header email, short-paper length, or PDF export.", pending.filter(p => p.category === "cr5"), "warning"]
      ].filter(g => g[2].length > 0);

      if (!groups.length) {{
        document.getElementById("action-cards").innerHTML = `<div class="card" style="text-align:center; padding:32px; color:var(--success); font-weight:600;">All 24 papers Pass compliance! Ready for Springer packaging.</div>`;
        return;
      }}

      document.getElementById("action-cards").innerHTML = groups.map(([title, desc, list, tone]) => `
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div class="row"><h3>${{title}}</h3> ${{badge(list.length + " paper" + (list.length === 1 ? "" : "s"), tone)}}</div>
          <div class="muted">${{desc}}</div>
          <div class="cards-2">
            ${{list.map(p => `
              <div class="card action-card">
                <div style="display:flex; flex-direction:column; gap:6px;">
                  <div class="between">
                    <span class="mono muted">Paper #${{p.num}} · Sub. ID ${{esc(p.id)}} · ${{p.pages || "—"}} pp</span>
                    ${{badge(p.category === "ltp" ? "LTP Blocker" : p.category === "missing" ? "Missing" : "CR-5 / Minor", tone)}}
                  </div>
                  <div style="font-weight:600;">${{esc(p.title)}}</div>
                  <div class="muted">Corresponding: <strong style="color:var(--fg)">${{esc(p.corr || "—")}}</strong></div>
                  <div class="note-box" style="background:var(--content);">${{esc(p.note || "Pending submission.")}}</div>
                </div>
                <div class="between" style="border-top:1px solid var(--divider); padding-top:10px;">
                  <code class="mono" style="color:var(--link); font-size:12px;">${{esc(p.email || "—")}}${{p.cc ? " (Cc: " + esc(p.cc) + ")" : ""}}</code>
                  <div class="row">
                    ${{p.draft ? `<span class="muted mono" style="font-size:11.5px;">${{esc(p.draft)}}</span>` : ""}}
                    ${{p.email ? `<button class="btn" onclick="copyText('${{esc(p.email)}}','${{esc(p.corr)}}')">Copy Email</button>` : ""}}
                  </div>
                </div>
              </div>
            `).join("")}}
          </div>
        </div>
      `).join("");
    }}

    function renderChecklist() {{
      let total = 0, done = 0;
      CHECKLIST.forEach(g => g.items.forEach(i => {{ total++; if (chkState[i.id]) done++; }}));
      const pct = total ? Math.round((done / total) * 100) : 0;
      document.getElementById("checklist-progress").textContent = `${{done}} / ${{total}} (${{pct}}%)`;

      document.getElementById("checklist-grid").innerHTML = CHECKLIST.map(g => {{
        const gDone = g.items.filter(i => chkState[i.id]).length;
        return `<div class="card" style="display:flex; flex-direction:column; gap:10px;">
          <div class="between" style="border-bottom:1px solid var(--divider); padding-bottom:8px;">
            <h3>${{esc(g.group)}}</h3>
            <span class="mono muted">${{gDone}}/${{g.items.length}}</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:10px;">
            ${{g.items.map(i => `
              <label class="chk-item">
                <input type="checkbox" ${{chkState[i.id] ? "checked" : ""}} onchange="toggleChk('${{i.id}}')" />
                <div>
                  <div class="${{chkState[i.id] ? 'done-text' : ''}}">${{esc(i.label)}}</div>
                  ${{i.meta ? `<div class="muted" style="margin-top:2px;">${{esc(i.meta)}}</div>` : ""}}
                </div>
              </label>
            `).join("")}}
          </div>
        </div>`;
      }}).join("");
    }}

    function toggleChk(id) {{
      chkState[id] = !chkState[id];
      saveChk();
      renderChecklist();
    }}

    document.getElementById("search-input").addEventListener("input", e => {{
      searchQuery = e.target.value.trim();
      renderTable();
    }});
    document.getElementById("sort-select").addEventListener("change", e => {{
      sortBy = e.target.value;
      renderTable();
    }});
    document.getElementById("copy-all-emails").addEventListener("click", () => {{
      const emails = PAPERS.filter(p => p.status !== "Pass" && p.email).map(p => p.email);
      copyText(emails.join(", "), emails.length + " pending author emails");
    }});
    document.getElementById("reset-checklist").addEventListener("click", () => {{
      try {{ localStorage.removeItem(STORAGE_KEY); }} catch (e) {{}}
      chkState = loadChk();
      renderChecklist();
      showToast("Checklist reset to submission/springer-checklist.md");
    }});

    renderHeaderAndKPIs();
    renderPageChart();
    renderComplianceChart();
    renderTable();
    renderActions();
    renderChecklist();
  </script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Build VERIF-AI 2026 HTML status dashboard.")
    ap.add_argument(
        "--output",
        default=str(ROOT / "tracking" / "dashboard.html"),
        help="Output HTML path (default: tracking/dashboard.html)",
    )
    args = ap.parse_args()

    papers = parse_paper_tracking(ROOT / "tracking" / "paper-tracking.md")
    merge_toc_csv(papers, ROOT / "submission" / "toc.csv")
    deadline = merge_author_emails(papers, ROOT / "tracking" / "author-emails.md")
    merge_drafts(papers, ROOT / "tracking" / "drafts")
    enrich_rules(papers)

    checklist = parse_checklist(ROOT / "submission" / "springer-checklist.md")
    volume_number = parse_volume_number(ROOT / "submission" / "springer-checklist.md")
    proceedings_pages = get_pdf_pages(ROOT / "proceedings.pdf")

    payload = {
        "generatedAt": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "volumeNumber": volume_number,
        "deadline": deadline,
        "proceedingsPages": proceedings_pages,
        "papers": papers,
        "checklist": checklist,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_html(payload), encoding="utf-8")

    passed = sum(1 for p in papers if p["status"] == "Pass")
    print(
        f"[OK] Generated {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path} "
        f"({len(papers)} papers, {passed} Pass, {len(papers) - passed} Fail/Pending, "
        f"{proceedings_pages or sum(p['pages'] for p in papers)} pp)"
    )


if __name__ == "__main__":
    main()
