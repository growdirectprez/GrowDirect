---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Operations Console — Full Build
*Issued by ALX · March 4, 2026 · Priority: CRITICAL PATH*
*Linear: GRO-9, GRO-10, GRO-73 (Quality Gate)*
*Plan Source: `Canary_Integration_Prep_Plan_v1.0.docx`*

**Context:** We have a pipeline monitor, a Square Capability Explorer, test data pumps, seed scripts, health checks, feature flag models, and merchant dashboards — all built at different times with different design languages and no shared navigation. Jeffe wants one unified Operations Console with the eljeffe.io dark theme for plumbing, the existing merchant dashboard for data verification, and all the old disjointed routes killed.

**Goal:** Ship a professional `/ops/*` route tree that consolidates all devops, testing, monitoring, and configuration tools under a single navigation shell. Then wire the Test Lab to drive scenarios that verify on the merchant-facing dashboard (Same Glass Principle). Kill all old routes.

**Same Glass Principle:** The merchant dashboard IS the test assertion surface. Drive test scenarios from the Ops Console; verify outcomes on the merchant-facing views. If the dashboard shows wrong data, that IS the bug.

---

## SCOPE — WHAT CHANGES

### New Files to Create

| File | Purpose |
|---|---|
| `static/css/ops.css` | Shared operations theme extracted from `static/square_explorer.html` inline styles |
| `templates/ops/base_ops.html` | Shared shell: top bar, sidebar nav, design tokens, JS utilities |
| `templates/ops/dashboard.html` | System health overview (extends base_ops.html) |
| `templates/ops/pipeline.html` | Pipeline monitor (extends base_ops.html, content from templates/devops/monitor.html) |
| `templates/ops/explorer.html` | Square Explorer (extends base_ops.html, content from static/square_explorer.html) |
| `templates/ops/test_lab.html` | Test scenario runner with verify links to merchant views |
| `templates/ops/api_docs.html` | Swagger UI wrapper (extends base_ops.html) |
| `templates/ops/config.html` | Feature flag toggles + AppConfig editor (extends base_ops.html) |
| `templates/ops/logs.html` | Log viewer with filtering (extends base_ops.html) |
| `canary/blueprints/ops_console.py` | Master `/ops/*` blueprint — all ops routes |
| `canary/services/ops_test_lab.py` | Test scenario execution engine (wraps test_reset.py + level_b_demo.py) |

### Files to Refactor (Edit in Place)

| File | Change |
|---|---|
| `wsgi.py` | Add `ops_console_bp` to BLUEPRINT_SPECS. Remove `devops_monitor_bp` and `square_explorer_bp` entries. |
| `canary/blueprints/devops_monitor.py` | Keep API routes (`/api/pipeline-state`, `/api/recent-events`, `/api/event/<id>`). Remove HTML route (`/devops/monitor`). The ops_console blueprint calls these APIs. |
| `canary/blueprints/square_explorer_wired.py` | Keep `/explore/<family>` API route. Remove `/explorer` HTML route. The ops_console blueprint serves the new template. |
| `templates/partials/sidebar.html` | Update DevOps section: change `/devops/monitor` → `/ops/pipeline`, `/explorer` → `/ops/explorer`. Add new ops nav items. |

### Files to Delete (After Migration Verified)

| File | Reason |
|---|---|
| `static/square_explorer.html` | Replaced by `templates/ops/explorer.html` |
| `templates/devops/monitor.html` | Replaced by `templates/ops/pipeline.html` |

---

## PHASE 1: Shell & Theme Extraction

### Step 1.1: Extract ops.css from Square Explorer

The Square Explorer at `static/square_explorer.html` has the best UX in the project. Extract its inline `<style>` block into a standalone CSS file.

```bash
# Source: static/square_explorer.html lines 10-470 (inline <style> block)
# Target: static/css/ops.css
```

**What to extract:**
- All CSS custom properties (`:root` block — lines 16-37)
- All component classes: `.top-bar`, `.wordmark`, `.content`, `.section-header`, `.grid`, `.card`, etc.
- All state classes: `.status-ok`, `.status-error`, `.status-empty`, `.status-scope`
- The grain overlay (`body::after`)
- Animation keyframes (`@keyframes pulse`)
- Responsive breakpoints

**What to generalize:**
- Rename `.explorer-*` prefixed classes to `.ops-*`
- Add generic classes: `.ops-table`, `.ops-modal`, `.ops-toast`, `.ops-form`, `.ops-toggle`
- Add sidebar nav styles (the Explorer doesn't have a sidebar — add it)

**Design tokens to preserve exactly:**
```css
:root {
  --bg: #0a0d12;
  --bg-card: rgba(15, 19, 26, 0.85);
  --bg-card-hover: rgba(20, 25, 35, 0.92);
  --border: #1a1f2a;
  --border-hover: #f59e0b44;
  --amber: #f59e0b;
  --green: #22c55e;
  --red: #ef4444;
  --text: #e2e8f0;
  --text-muted: #6b7280;
  --font-display: 'Syne', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### Step 1.2: Create base_ops.html

This is the shared shell template. All `/ops/*` pages extend it.

**File:** `templates/ops/base_ops.html`

**Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Ops{% endblock %} — Canary Operations</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/ops.css">
  {% block head_extra %}{% endblock %}
</head>
<body>
  <!-- Top Bar (from Square Explorer .top-bar pattern) -->
  <div class="ops-topbar">
    <div class="ops-wordmark">CANARY <span class="ops-wordmark-dim">OPS</span></div>
    <div class="ops-env-badge">{{ config.SQUARE_ENVIRONMENT | upper }}</div>
    <div class="ops-status">
      <span class="ops-status-dot" id="health-dot"></span>
      <span class="ops-status-text" id="health-text">checking...</span>
    </div>
  </div>

  <!-- Sidebar Nav -->
  <nav class="ops-sidebar">
    <a href="/ops" class="ops-nav-item{% if active_tab == 'dashboard' %} active{% endif %}">
      <span class="ops-nav-icon">⊞</span> Dashboard
    </a>
    <a href="/ops/pipeline" class="ops-nav-item{% if active_tab == 'pipeline' %} active{% endif %}">
      <span class="ops-nav-icon">⟹</span> Pipeline
    </a>
    <a href="/ops/explorer" class="ops-nav-item{% if active_tab == 'explorer' %} active{% endif %}">
      <span class="ops-nav-icon">⬡</span> Explorer
    </a>
    <a href="/ops/test-lab" class="ops-nav-item{% if active_tab == 'test-lab' %} active{% endif %}">
      <span class="ops-nav-icon">⚗</span> Test Lab
    </a>
    <a href="/ops/api-docs" class="ops-nav-item{% if active_tab == 'api-docs' %} active{% endif %}">
      <span class="ops-nav-icon">⊡</span> API Docs
    </a>
    <a href="/ops/config" class="ops-nav-item{% if active_tab == 'config' %} active{% endif %}">
      <span class="ops-nav-icon">⊕</span> Config
    </a>
    <a href="/ops/logs" class="ops-nav-item{% if active_tab == 'logs' %} active{% endif %}">
      <span class="ops-nav-icon">≡</span> Logs
    </a>
    <div class="ops-nav-divider"></div>
    <a href="/dashboard" class="ops-nav-item ops-nav-merchant" target="_blank">
      ↗ Merchant View
    </a>
  </nav>

  <!-- Main Content -->
  <main class="ops-main">
    {% block content %}{% endblock %}
  </main>

  <!-- Toast Container -->
  <div id="ops-toasts" class="ops-toast-container"></div>

  <script>
  // Shared: health polling, toast system, status chip renderer
  const OPS = {
    toast(msg, type='info') {
      const el = document.createElement('div');
      el.className = `ops-toast ops-toast-${type}`;
      el.textContent = msg;
      document.getElementById('ops-toasts').appendChild(el);
      setTimeout(() => el.remove(), 5000);
    },
    async healthCheck() {
      try {
        const r = await fetch('/health');
        const d = await r.json();
        document.getElementById('health-dot').className = 'ops-status-dot ok';
        document.getElementById('health-text').textContent = `v${d.version} · healthy`;
      } catch(e) {
        document.getElementById('health-dot').className = 'ops-status-dot err';
        document.getElementById('health-text').textContent = 'unreachable';
      }
    },
    statusChip(status) {
      const colors = {ok:'var(--green)',error:'var(--red)',warn:'var(--amber)',empty:'var(--text-muted)'};
      return `<span class="ops-chip" style="--chip-color:${colors[status]||colors.empty}">${status}</span>`;
    }
  };
  OPS.healthCheck();
  setInterval(OPS.healthCheck, 30000);
  </script>
  {% block scripts_extra %}{% endblock %}
</body>
</html>
```

**Critical notes:**
- Do NOT extend `base.html` (the merchant template). This is a completely separate shell.
- Do NOT import `canary.css`. The ops console uses `ops.css` only.
- The "Merchant View" link opens the merchant dashboard in a new tab — this is the Same Glass verify path.

### Step 1.3: Create ops_console.py Blueprint

**File:** `canary/blueprints/ops_console.py`

```python
"""Operations Console — unified devops/admin interface.

All /ops/* routes. Consolidates:
  - Pipeline Monitor (was /devops/monitor)
  - Square Explorer (was /explorer)
  - Test Lab (new)
  - API Docs (new)
  - Config (was /admin/config)
  - Logs (new)

Sandbox guard: all routes blocked unless SQUARE_ENVIRONMENT == "sandbox".
Feature flag gate: ops_console_enabled must be true in FeatureFlag table.
"""

import logging
import os

from flask import Blueprint, jsonify, render_template, request, redirect

logger = logging.getLogger("canary.ops_console")

ops_console_bp = Blueprint(
    "ops_console", __name__,
    template_folder="../../templates/ops",
)


# ── Guard: sandbox only ──────────────────────────────────────────────────

@ops_console_bp.before_request
def sandbox_guard():
    if os.getenv("SQUARE_ENVIRONMENT") != "sandbox":
        return jsonify({"error": "sandbox_only"}), 403


# ── Tab Routes ───────────────────────────────────────────────────────────

@ops_console_bp.route("/")
def dashboard():
    return render_template("ops/dashboard.html", active_tab="dashboard")


@ops_console_bp.route("/pipeline")
def pipeline():
    return render_template("ops/pipeline.html", active_tab="pipeline")


@ops_console_bp.route("/explorer")
def explorer():
    return render_template("ops/explorer.html", active_tab="explorer")


@ops_console_bp.route("/test-lab")
def test_lab():
    return render_template("ops/test_lab.html", active_tab="test-lab")


@ops_console_bp.route("/api-docs")
def api_docs():
    return render_template("ops/api_docs.html", active_tab="api-docs")


@ops_console_bp.route("/config")
def config():
    return render_template("ops/config.html", active_tab="config")


@ops_console_bp.route("/logs")
def logs():
    return render_template("ops/logs.html", active_tab="logs")


# ── Legacy Redirects ─────────────────────────────────────────────────────

# These ensure old bookmarks/links still work

@ops_console_bp.route("/legacy/monitor")
def legacy_monitor():
    return redirect("/ops/pipeline", code=301)


@ops_console_bp.route("/legacy/explorer")
def legacy_explorer():
    return redirect("/ops/explorer", code=301)
```

### Step 1.4: Register in wsgi.py

**Edit `wsgi.py` BLUEPRINT_SPECS list:**

**Remove these two lines:**
```python
("canary.blueprints.square_explorer_wired", "square_explorer_bp", "", "Square Capability Explorer", False),
("canary.blueprints.devops_monitor", "devops_monitor_bp", "/devops", "DevOps Pipeline Monitor", True),
```

**Add this line:**
```python
("canary.blueprints.ops_console", "ops_console_bp", "/ops", "Operations Console", True),
```

**Also add redirect routes in views_wired.py** (or wsgi.py directly) for the old URLs:
```python
# Legacy redirects for old devops routes
@app.route("/devops/monitor")
def legacy_devops_monitor():
    return redirect("/ops/pipeline", code=301)

@app.route("/explorer")
def legacy_explorer():
    return redirect("/ops/explorer", code=301)
```

**IMPORTANT:** The devops_monitor.py API routes (`/devops/monitor/api/*`) are still needed — the Pipeline tab calls them via JavaScript. Keep devops_monitor.py registered BUT only for its API routes. Two options:

**Option A (preferred):** Move the API routes into ops_console.py as `/ops/api/pipeline/*`
**Option B (quick):** Keep devops_monitor_bp registered at `/devops` but strip the HTML route, so `/devops/monitor/api/*` still works and `/devops/monitor` redirects to `/ops/pipeline`

Choose Option B for speed, then migrate to Option A later.

### Step 1.5: Update Merchant Sidebar

**Edit `templates/partials/sidebar.html`** — update the DevOps section:

**Replace:**
```html
<div class="sidebar-section">
    <div class="sidebar-section-label">DevOps</div>
    <a href="/devops/monitor" ...>Pipeline</a>
    <a href="/explorer" ...>Explorer</a>
</div>
```

**With:**
```html
<div class="sidebar-section">
    <div class="sidebar-section-label">Operations</div>
    <a href="/ops" class="sidebar-item{% if active_page == 'ops' %} active{% endif %}" data-color="pipeline">
        <span class="nav-icon" style="background: var(--nav-audit);"></span>
        Ops Console
    </a>
</div>
```

Single link to `/ops` from the merchant sidebar. Everything else lives inside the ops console's own nav.

### Step 1.6: Build Dashboard Tab

**File:** `templates/ops/dashboard.html`

Content: system health overview aggregating:
- Flask health status (poll `/health`)
- Three database connection status (poll each DB via new API endpoint)
- Valkey connection status
- Pipeline summary (stream depths, consumer group lag — from devops_monitor API)
- Recent events count (last 1h, last 24h)
- Table row counts across all 3 databases
- Quick links to all other tabs

Use card-based layout matching Square Explorer's `.card` pattern. Poll every 10 seconds.

### Step 1.7: Migrate Pipeline Monitor

**File:** `templates/ops/pipeline.html`

Take the content from `templates/devops/monitor.html` and:
1. Change `{% extends %}` to use `ops/base_ops.html` (or embed in base_ops block)
2. Strip the standalone `<html>`, `<head>`, inline `<style>` — all replaced by base_ops.html + ops.css
3. Keep ALL the JavaScript (pipeline diagram, event feed, action buttons, polling)
4. Restyle with ops.css classes instead of inline GitHub-dark styles
5. Keep API calls pointing to `/devops/monitor/api/*` (Option B from Step 1.4)

### Step 1.8: Migrate Square Explorer

**File:** `templates/ops/explorer.html`

Take the content from `static/square_explorer.html` and:
1. Wrap in `{% extends "ops/base_ops.html" %}` / `{% block content %}`
2. Strip standalone HTML boilerplate (already in base_ops)
3. Strip inline `<style>` (already extracted to ops.css)
4. Keep ALL the JavaScript (API family cards, test buttons, result display)
5. Keep API calls pointing to `/explore/<family>` (these stay as-is)

### Step 1.9: Rebuild and Verify

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
```

**Verify:**
```bash
# New routes
curl -s http://localhost:5001/ops | grep "Canary OPS"
curl -s http://localhost:5001/ops/pipeline | grep "Pipeline"
curl -s http://localhost:5001/ops/explorer | grep "Explorer"

# Legacy redirects
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/devops/monitor  # Should be 301
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/explorer        # Should be 301

# API routes still work
curl -s http://localhost:5001/devops/monitor/api/pipeline-state | python3 -m json.tool
curl -s http://localhost:5001/explore/merchants | python3 -m json.tool

# Merchant sidebar updated
curl -s http://localhost:5001/dashboard | grep "/ops"
```

---

## PHASE 2: Test Lab & Config

### Step 2.1: Create ops_test_lab.py Service

**File:** `canary/services/ops_test_lab.py`

This wraps the existing CLI tools in a Python service that the ops_console blueprint can call.

**Functions:**
```python
def purge_pipeline(dry_run=False) -> dict:
    """Wraps devops/scripts/test_reset.py logic. Returns purge report."""

def seed_reference_data() -> dict:
    """Wraps devops/seeds/level_b_demo.py seed_app(). Returns seed report."""

def seed_sales_data() -> dict:
    """Wraps devops/seeds/level_b_demo.py seed_sales(). Returns seed report."""

def generate_test_event(event_type: str) -> dict:
    """Generate a test webhook event (payment, refund, void, cash).
    Calls the same sandbox tool endpoints that the pipeline monitor's
    'Generate Transaction' buttons call."""

def run_scenario(scenario_id: str) -> dict:
    """Execute a predefined test scenario.
    Returns step-by-step results with verify links to merchant views."""

def get_scenario_definitions() -> list[dict]:
    """Return the 8 predefined scenario definitions."""
```

**API routes in ops_console.py:**
```python
@ops_console_bp.route("/api/test-lab/purge", methods=["POST"])
@ops_console_bp.route("/api/test-lab/seed", methods=["POST"])
@ops_console_bp.route("/api/test-lab/generate", methods=["POST"])
@ops_console_bp.route("/api/test-lab/scenario/<scenario_id>", methods=["POST"])
@ops_console_bp.route("/api/test-lab/scenarios", methods=["GET"])
```

### Step 2.2: Build Test Lab Template

**File:** `templates/ops/test_lab.html`

Layout (extends base_ops.html):
- **Left panel:** Scenario selector (cards for each of 8 scenarios)
- **Right panel:** Execution/results area
- **Bottom strip:** Quick actions (Purge, Seed, Generate Transaction)
- Each scenario card shows: name, description, DRIVE summary, VERIFY link (opens merchant view in new tab)

### Step 2.3: Build Config Tab

**File:** `templates/ops/config.html`

Two sections:
1. **Feature Flags:** Card per flag, grouped by category. Toggle switches for boolean values. Source: query `FeatureFlag` table via new API.
2. **App Config:** Key-value editor. Secret values masked. Source: query `AppConfig` table.

**API routes in ops_console.py:**
```python
@ops_console_bp.route("/api/config/flags", methods=["GET"])
@ops_console_bp.route("/api/config/flags/<flag_key>", methods=["PUT"])
@ops_console_bp.route("/api/config/app", methods=["GET"])
@ops_console_bp.route("/api/config/app/<key>", methods=["PUT"])
```

### Step 2.4: Build Logs Tab

**File:** `templates/ops/logs.html`

- Tail the Flask application log (last N lines)
- Filter by level (DEBUG/INFO/WARNING/ERROR)
- Webhook event log (query ingestion_log table)
- Search/filter by event_id, merchant_id, timestamp range

### Step 2.5: Seed Feature Flags

Create a migration or seed script to populate the initial feature flags:

```python
INITIAL_FLAGS = [
    ("ops_console_enabled", "Operations Console", "integration", True),
    ("pipeline_monitor_enabled", "Pipeline Monitor", "integration", True),
    ("test_lab_enabled", "Test Lab", "integration", True),
    ("swagger_enabled", "API Documentation", "integration", True),
    ("webhook_debug_mode", "Webhook Debug Logging", "security", False),
    ("detection_dry_run", "Detection Dry Run", "analytics", False),
    ("schema_drift_alerts", "Schema Drift Alerts", "analytics", True),
    ("seed_data_allowed", "Seed Data Operations", "integration", False),
    ("pipeline_purge_allowed", "Pipeline Purge", "integration", False),
    ("square_api_explorer", "Square API Explorer", "integration", True),
]
```

### Step 2.6: Rebuild and Verify

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
```

**Verify all 7 tabs respond:**
```bash
for tab in "" pipeline explorer test-lab api-docs config logs; do
  echo -n "/ops/$tab → "
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/ops/$tab
  echo
done
```

---

## PHASE 3: API Docs & Regression Runner

### Step 3.1: Swagger Integration

Add `flasgger` to requirements.txt:
```
flasgger>=0.9.7
```

Configure in wsgi.py (or ops_console.py):
- Auto-generate spec from Flask routes
- Serve at `/ops/api-docs/spec.json`
- Embed Swagger UI in the API Docs tab with ops theme override

### Step 3.2: Regression Cycle Runner

Add to ops_test_lab.py:
```python
def run_full_regression() -> dict:
    """Execute all 8 scenarios in sequence.
    1. Purge pipeline
    2. Seed reference data
    3. Run scenarios 1-8, collecting results
    4. Generate regression report
    Returns: {scenarios: [...], passed: int, failed: int, duration_s: float}
    """
```

UI button in Test Lab: "Run Full Regression" — shows real-time progress through all 8 scenarios.

### Step 3.3: Delete Old Files

After all tabs verified working:

```bash
cd ~/GrowDirect/Canary
rm static/square_explorer.html
rm templates/devops/monitor.html
rmdir templates/devops/  # if empty
```

Update any references:
```bash
grep -r "square_explorer.html" canary/ templates/ static/
grep -r "devops/monitor.html" canary/ templates/
```

---

## FILES TOUCHED (SUMMARY)

### Do Not Touch List Override
This work order explicitly modifies `wsgi.py` (adding/removing BLUEPRINT_SPECS entries). Jeffe authorized this on March 4, 2026: "kill all the old crap."

### Created
- `static/css/ops.css`
- `templates/ops/base_ops.html`
- `templates/ops/dashboard.html`
- `templates/ops/pipeline.html`
- `templates/ops/explorer.html`
- `templates/ops/test_lab.html`
- `templates/ops/api_docs.html`
- `templates/ops/config.html`
- `templates/ops/logs.html`
- `canary/blueprints/ops_console.py`
- `canary/services/ops_test_lab.py`

### Modified
- `wsgi.py` — BLUEPRINT_SPECS (add ops_console_bp, keep devops_monitor for API only)
- `canary/blueprints/devops_monitor.py` — remove HTML route, keep API routes
- `canary/blueprints/square_explorer_wired.py` — remove HTML route, keep API route
- `templates/partials/sidebar.html` — DevOps section → single "Ops Console" link
- `requirements.txt` — add flasgger (Phase 3)

### Deleted (Phase 3, after verification)
- `static/square_explorer.html`
- `templates/devops/monitor.html`

---

## SUCCESS CRITERIA

- [ ] `curl http://localhost:5001/ops` returns 200 with Canary OPS header
- [ ] All 7 tabs render with eljeffe.io dark theme (Syne + JetBrains Mono)
- [ ] Pipeline Monitor shows real-time pipeline state (same data as old /devops/monitor)
- [ ] Square Explorer tests all 16 API families (same functionality as old /explorer)
- [ ] Test Lab can execute "Happy Path Payment" scenario
- [ ] Test Lab verify links open merchant dashboard views in new tab
- [ ] Config tab shows feature flags with working toggle switches
- [ ] `/devops/monitor` redirects to `/ops/pipeline` (301)
- [ ] `/explorer` redirects to `/ops/explorer` (301)
- [ ] Merchant sidebar shows single "Ops Console" link under Operations section
- [ ] No references to `square_explorer.html` or `devops/monitor.html` remain in codebase
- [ ] All 3 test layers pass after rebuild

---

## EXECUTION ORDER

```
Phase 1 (Shell):  1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 → 1.7 → 1.8 → 1.9 (rebuild + verify)
Phase 2 (Lab):    2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 (rebuild + verify)
Phase 3 (Docs):   3.1 → 3.2 → 3.3 (rebuild + verify)
```

Each phase ends with a Docker rebuild and full verification. Do not proceed to Phase 2 until Phase 1 is green.

---

*Canary LP | GrowDirect Inc. | Confidential*
