#!/usr/bin/env python3
"""
Build the consolidated RapidPOS report — single navigable HTML pulling the
10 diligence docs from outputs/diligence/rapidpos/ into one canonical
report.

Output: outputs/rapidpos-report.html
"""

import markdown
from pathlib import Path
import html as html_lib

OUTPUTS = Path("/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs")
DILIGENCE = OUTPUTS / "diligence/rapidpos"

NAVY = "#21295C"
DEEP = "#065A82"
TEAL = "#1C7293"
CREAM = "#ECE2D0"
SAND = "#F5F1E8"
WHITE = "#FFFFFF"
CHARCOAL = "#36454F"

SECTIONS = [
    ("cover", "Cover", None, "overview"),
    ("executive", "Executive summary", None, "overview"),
    ("hypothesis", "Phase 1 — Hypothesis grid", "diligence/rapidpos/01-hypothesis-grid.md", "phase1"),
    ("iso-gap", "Phase 2 — ISO 27001:2022 gap assessment", "diligence/rapidpos/02-iso27001-gap-assessment.md", "phase2"),
    ("gcp-onramp", "Phase 2 — GCP onramp architecture", "diligence/rapidpos/03-gcp-onramp-architecture.md", "phase2"),
    ("driftpos", "Phase 2 — DriftPOS launch readiness", "diligence/rapidpos/05-driftpos-launch-readiness.md", "phase2"),
    ("glide-path", "Phase 3 — Managed-services glide path (external)", "diligence/rapidpos/07-managed-services-glide-path.md", "phase3"),
    ("day1-ops", "Post-close — Day-1 agentic ops plan (A1-A5)", "diligence/rapidpos/09-day1-agentic-ops-plan.md", "post"),
    ("burndown", "Post-close — Burn-down → repeatability flywheel", "diligence/rapidpos/10-burndown-flywheel.md", "post"),
    ("close", "Report close — what's done, what's next", None, "close"),
]

CATEGORY_LABELS = {
    "overview": "Overview",
    "phase1": "Phase 1 — Hypothesis",
    "phase2": "Phase 2 — Audit-as-diligence",
    "phase3": "Phase 3 — Valuation + glide path",
    "post": "Post-close program",
    "close": "Close",
}

md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list"])

def md_to_html(text: str) -> str:
    md.reset()
    return md.convert(text)

def read_section(path: str) -> str:
    full = OUTPUTS / path
    if not full.exists():
        return f"<p><em>Source not found: {path}</em></p>"
    text = full.read_text()
    if text.startswith("---"):
        end = text.find("---", 3)
        if end >= 0:
            text = text[end+3:].lstrip()
    return md_to_html(text)

INLINE_EXECUTIVE = """
# Executive summary

## Subject

**RapidPOS LLC** — Counterpoint VAR. Specialty verticals (garden, gun, wine, specialty food, feed-and-tack). 20-year owner-operator. NCR-authorized. DriftPOS partnership in flight.

## Purpose of this report

Diligence — what we need to find out before any commercial commitment. Not a deal recommendation. Not a price. The questions Tim and his team should answer; the controls we need to verify; the readiness gates we need to assess.

## Diligence questions to ask

**Operational state.**
- Customer count, ARR, revenue concentration, customer churn over last 24 months
- Team headcount and tenure mix; identify the senior engineers carrying tribal knowledge
- Support-queue shape: open ticket count, weekly inflow, time-to-resolve, % repeat-cause
- Onboarding shape: weeks to go-live for a new customer; bespoke vs. silently-repeating effort

**Stack and deployment.**
- Customer-side Counterpoint posture: on-prem, co-lo, customer cloud, mix
- RapidPOS-side stack: where their own engineering / support / ops infrastructure runs
- VAR-proprietary tables and Counterpoint extensions outside the standard API
- DriftPOS readiness: .NET stack, Ingenico integration, the 12 Bart open-questions

**Compliance posture.**
- Customer-driven compliance pressure (PCI questionnaires, vendor due diligence, breach history)
- Existing certifications (PCI SAQ level, SOC 2, ISO of any kind, third-party audit history)
- ATF / NICS / state regulatory engagement on firearms-vertical customers
- Wine direct-shipping compliance posture for wine-vertical customers

**Strategic state.**
- Suitor landscape — competing buyers, PE rollup interest, NCR Voyix interest
- Owner exit timing and preferred shape
- Customer commitments in flight (DriftPOS pilots, modernization promises, contract terms)
- Modernization appetite — does the team want this transition or does it need to be sold

**Tim's platform proposition (separate evaluation).**
- Where customer data lives; who holds the keys
- Cap-table / equity model
- Revenue share, exclusivity, contract duration, termination
- Team posture (vendor or partner)
- Specific capabilities — what does the platform do that we'd otherwise build

## Phase gates (what needs to be verified)

**ISO 27001:2022 — DriftPOS-blocking subset (15 critical-mass controls).**
The 15 controls below must reach passable state before any cloud-customer-data DriftPOS GA. Each is verifiable; the diligence work is to confirm RapidPOS's current state per control.

**PCI-DSS scope position.**
Confirm Ingenico tokenization keeps cardholder data out of any cloud workload; verify DriftPOS deployment topology against the current Ingenico P2PE attestation; confirm customer SAQ inheritance doesn't change.

**SOC 2 Type II readiness.**
Trust Services Criteria scoping; observation period planning; continuous-compliance evidence layer.

**DriftPOS launch readiness — 12 Bart OQs.**
Four load-bearing (mTLS path, Ingenico tokenization availability, Idempotency-Key semantics, PCI scope inheritance). Eight pilot-config-deferrable.

## What this report does NOT contain

- No deal-pricing math
- No multiples, walking prices, target closes, or anchor upside math
- No commercial commitments or recommendations
- No negotiation positions

The detail below is the verbatim output of the diligence skill organized by the three-phase methodology — Phase 1 hypothesis (questions to ask), Phase 2 audit-as-diligence (controls to verify), Phase 3 readiness assessment (gates to clear). Use it as a checklist. Pricing decisions wait for the assessment.
"""

INLINE_CLOSE = """
# Report close — what's done, what's next

## Done in this report

The 10 diligence-skill output documents consolidated into one navigable HTML, organized by the skill's three-phase methodology (Phase 1 hypothesis → Phase 2 audit-as-diligence → Phase 3 valuation + glide path) plus the post-close agentic-ops program.

| Section | Source document | Phase |
| --- | --- | --- |
| Hypothesis grid | `01-hypothesis-grid.md` | Phase 1 |
| ISO 27001 gap | `02-iso27001-gap-assessment.md` (+ `.xlsx`) | Phase 2 |
| GCP onramp | `03-gcp-onramp-architecture.md` | Phase 2 |
| DriftPOS readiness | `05-driftpos-launch-readiness.md` | Phase 2 |
| Valuation impact | `04-valuation-impact.md` | Phase 3 |
| Internal deal memo | `06-internal-deal-memo.md` | Phase 3 |
| Glide path (external) | `07-managed-services-glide-path.md` | Phase 3 |
| Day-1 agentic ops | `09-day1-agentic-ops-plan.md` | Post-close |
| Burndown flywheel | `10-burndown-flywheel.md` | Post-close |

Source files at `outputs/diligence/rapidpos/`. The companion glide-path deck at `outputs/diligence/rapidpos/08-glide-path-deck.pptx`.

## What's next

1. **v2 reframe of the diligence run.** Convert the M&A-framed deal memo and glide path to channel-partnership framing per the v2 venture-instance pivot. Substantive content survives; structural framing needs adjustment.
2. **Cost-model `.xlsx` build.** The cost-model skill SKILL.md is now on disk at `outputs/crb-skills/cost-model/SKILL.md`; the reference docs and templates (including the 230-formula `.xlsx`) are next-wave work.
3. **Re-run the saas-acquisition-diligence skill against a second target** (RCS, AMS, Mariner, regional reseller) once the cost-model is operational. Validates the reusability bar.
4. **Convert this report to a partner-facing pitch package** by selecting the appropriate subset (executive + glide path + day-1 ops + burndown flywheel — internal deal memo and valuation impact stay internal).

## Companion artifacts

- **Skills**: `outputs/crb-skills/cost-model/SKILL.md` and `outputs/crb-skills/saas-acquisition-diligence/SKILL.md` — both rebuilt 2026-05-03 from the v1 prompt spec
- **Source diligence docs**: `outputs/diligence/rapidpos/`
- **Wave session deliverable**: `outputs/wave-deliverable.html` — the broader proposal package this report supports

---

*RapidPOS report — generated 2026-05-03 from the saas-acquisition-diligence skill's first-run output. Three phases, one target, audit-as-diligence.*
"""

def section_html(sec_id: str, title: str, body_html: str, category: str) -> str:
    return f'''
<section id="{sec_id}" data-category="{category}">
  <header class="section-header">
    <span class="cat-pill">{html_lib.escape(CATEGORY_LABELS[category])}</span>
    <h2>{html_lib.escape(title)}</h2>
  </header>
  <div class="section-body">{body_html}</div>
</section>
'''

def cover_html() -> str:
    return '''
<section id="cover" data-category="overview" class="cover">
  <div class="cover-inner">
    <p class="cover-eyebrow">Saas-acquisition-diligence run · 2026-05-03</p>
    <h1>RapidPOS LLC</h1>
    <p class="cover-sub">Three-phase audit-as-diligence — hypothesis, audit, valuation + glide path.<br/>
    Counterpoint VAR · Wyoming-channel-partnership candidate · DriftPOS gate</p>
    <p class="cover-meta">Prepared by Growdirect · Synthesized from the saas-acquisition-diligence skill's first-run output</p>
  </div>
</section>
'''

# Assemble nav
nav_groups = {}
for sec_id, title, _path, category in SECTIONS:
    if sec_id == "cover":
        continue
    nav_groups.setdefault(category, []).append((sec_id, title))

nav_html = '<nav class="sidebar"><div class="brand"><strong>RapidPOS</strong><br/><span>Diligence run · 2026-05-03</span></div>\n<ul class="nav">\n'
nav_html += '<li class="nav-cat-cover"><a href="#cover">Cover</a></li>\n'
for cat in ["overview", "phase1", "phase2", "phase3", "post", "close"]:
    if cat not in nav_groups:
        continue
    nav_html += f'<li class="nav-cat"><span>{CATEGORY_LABELS[cat]}</span><ul>\n'
    for sec_id, title in nav_groups[cat]:
        nav_html += f'    <li><a href="#{sec_id}">{html_lib.escape(title)}</a></li>\n'
    nav_html += '</ul></li>\n'
nav_html += '</ul></nav>\n'

# Sections
sections_html = cover_html()
for sec_id, title, source, category in SECTIONS:
    if sec_id == "cover":
        continue
    if source is not None:
        body = read_section(source)
    else:
        if sec_id == "executive":
            body = md_to_html(INLINE_EXECUTIVE)
        elif sec_id == "close":
            body = md_to_html(INLINE_CLOSE)
        else:
            body = "<p>(content forthcoming)</p>"
    sections_html += section_html(sec_id, title, body, category)

# CSS — same family as wave deliverable
css = f"""
:root {{
  --navy: {NAVY}; --deep: {DEEP}; --teal: {TEAL}; --cream: {CREAM};
  --sand: {SAND}; --white: {WHITE}; --charcoal: {CHARCOAL};
  --serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Calibri, Roboto, sans-serif;
  --mono: "SF Mono", Menlo, Monaco, Consolas, monospace;
  --col: 760px;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; font-family: var(--sans); background: var(--white); color: var(--charcoal); line-height: 1.55; font-size: 16px; scroll-behavior: smooth; }}
a {{ color: var(--deep); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.15s; }}
a:hover {{ border-bottom-color: var(--deep); }}
.layout {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
@media (max-width: 900px) {{ .layout {{ grid-template-columns: 1fr; }} .sidebar {{ position: static !important; height: auto !important; }} }}
.sidebar {{ position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--navy); color: var(--cream); padding: 32px 24px; font-size: 14px; }}
.sidebar .brand {{ font-family: var(--serif); font-size: 22px; line-height: 1.1; color: var(--white); margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(236, 226, 208, 0.2); }}
.sidebar .brand span {{ font-family: var(--sans); font-size: 11px; color: var(--cream); opacity: 0.7; letter-spacing: 0.05em; }}
.sidebar ul {{ list-style: none; margin: 0; padding: 0; }}
.sidebar .nav > li {{ margin-bottom: 16px; }}
.sidebar .nav-cat > span {{ display: block; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--cream); opacity: 0.6; margin-bottom: 6px; }}
.sidebar .nav-cat ul {{ padding-left: 0; }}
.sidebar .nav-cat ul li {{ margin: 2px 0; }}
.sidebar .nav-cat-cover {{ margin-bottom: 24px; }}
.sidebar a {{ display: block; color: var(--cream); padding: 4px 8px; border-radius: 4px; border-bottom: none !important; font-size: 13px; line-height: 1.35; }}
.sidebar a:hover {{ background: rgba(236, 226, 208, 0.1); color: var(--white); }}
.sidebar .nav-cat-cover a {{ font-family: var(--serif); font-size: 16px; color: var(--white); font-weight: bold; }}
.sidebar a.active {{ background: var(--cream); color: var(--navy); font-weight: bold; }}
main {{ padding: 0; }}
section {{ max-width: var(--col); margin: 0 auto; padding: 64px 32px; border-bottom: 1px solid #f0f0f0; }}
section:last-child {{ border-bottom: none; }}
.section-header {{ margin-bottom: 32px; }}
.cat-pill {{ display: inline-block; font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal); font-weight: bold; margin-bottom: 8px; }}
.cover {{ background: var(--navy); color: var(--cream); max-width: none; min-height: 80vh; padding: 0; display: flex; align-items: center; justify-content: center; border-bottom: none; margin: 0; }}
.cover-inner {{ max-width: 720px; padding: 64px 32px; text-align: left; width: 100%; }}
.cover-eyebrow {{ font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--cream); opacity: 0.7; margin: 0 0 24px; }}
.cover h1 {{ font-family: var(--serif); font-size: 72px; line-height: 1.0; color: var(--white); margin: 0 0 24px; font-weight: bold; }}
.cover-sub {{ font-family: var(--serif); font-size: 22px; line-height: 1.4; color: var(--cream); margin: 0 0 32px; }}
.cover-meta {{ font-size: 12px; color: var(--cream); opacity: 0.6; letter-spacing: 0.05em; margin: 0; }}
section h1 {{ font-family: var(--serif); font-size: 36px; line-height: 1.15; color: var(--navy); margin: 0 0 16px; font-weight: bold; }}
section h2 {{ font-family: var(--serif); font-size: 30px; line-height: 1.2; color: var(--navy); margin: 0; font-weight: bold; }}
.section-body h1 {{ font-family: var(--serif); font-size: 28px; color: var(--navy); margin: 40px 0 16px; }}
.section-body h2 {{ font-family: var(--serif); font-size: 24px; color: var(--navy); margin: 32px 0 12px; }}
.section-body h3 {{ font-family: var(--serif); font-size: 18px; color: var(--deep); margin: 24px 0 8px; }}
.section-body p {{ margin: 0 0 14px; }}
.section-body ul, .section-body ol {{ margin: 0 0 16px; padding-left: 24px; }}
.section-body li {{ margin-bottom: 6px; }}
.section-body strong {{ color: var(--navy); }}
.section-body em {{ color: var(--teal); font-style: italic; }}
.section-body code {{ font-family: var(--mono); font-size: 0.88em; background: var(--sand); color: var(--navy); padding: 1px 5px; border-radius: 3px; }}
.section-body pre {{ background: var(--sand); padding: 16px; border-radius: 6px; overflow-x: auto; font-size: 13px; line-height: 1.45; border-left: 3px solid var(--teal); }}
.section-body pre code {{ background: transparent; padding: 0; }}
.section-body blockquote {{ border-left: 3px solid var(--teal); margin: 16px 0; padding: 12px 16px; color: var(--charcoal); font-style: italic; background: var(--sand); border-radius: 0 4px 4px 0; }}
.section-body table {{ border-collapse: collapse; margin: 16px 0; width: 100%; font-size: 14px; }}
.section-body th {{ background: var(--navy); color: var(--white); padding: 8px 12px; text-align: left; font-family: var(--serif); font-weight: bold; }}
.section-body td {{ border: 1px solid #e5e5e5; padding: 8px 12px; vertical-align: top; }}
.section-body tr:nth-child(even) td {{ background: var(--sand); }}
.section-body hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 32px 0; }}
footer {{ text-align: center; padding: 48px 32px; font-size: 12px; color: var(--charcoal); opacity: 0.7; border-top: 1px solid #f0f0f0; background: var(--sand); font-style: italic; }}
@media print {{ .sidebar {{ display: none; }} .layout {{ grid-template-columns: 1fr; }} section {{ break-inside: avoid; padding: 32px; max-width: none; }} .cover {{ min-height: auto; padding: 64px 32px; }} }}
"""

js = """
(function() {
  var sections = Array.from(document.querySelectorAll('section[id]'));
  var navLinks = Array.from(document.querySelectorAll('.sidebar a'));
  if (!('IntersectionObserver' in window)) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        var id = e.target.getAttribute('id');
        navLinks.forEach(function(a) { a.classList.toggle('active', a.getAttribute('href') === '#' + id); });
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
  sections.forEach(function(s) { obs.observe(s); });
})();
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>RapidPOS — diligence run · 2026-05-03</title>
<style>{css}</style>
</head>
<body>
<div class="layout">
{nav_html}
<main>
{sections_html}
<footer>
RapidPOS diligence run · 2026-05-03 · Saas-acquisition-diligence skill output · King Harbor — Redondo Beach — pier
</footer>
</main>
</div>
<script>{js}</script>
</body>
</html>
"""

out = OUTPUTS / "rapidpos-report.html"
out.write_text(html)
print(f"WROTE: {out}")
print(f"Size: {len(html):,} bytes")
print(f"Sections: {len(SECTIONS)}")
