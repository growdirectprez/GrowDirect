import os

# Ruptiv brand tokens — Brand Guide v5
BG      = "#0F1729"   # Deep Ink
FG      = "#F4F1EA"   # Ivory
MUTED   = "#6B7E9C"   # secondary text (between Slate and Ivory)
ACCENT  = "#4FC3DC"   # Cyan
SIGNAL  = "#F2C94C"   # Signal Yellow — rare, one focal use per surface
BORDER  = "#1F2D4A"   # Slate
CARD_BG = "#162033"   # slightly lighter than Deep Ink for card surfaces
MONO    = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace'
SANS    = '"Söhne", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'

CSS = f"""
  :root {{
    --bg: {BG};
    --fg: {FG};
    --muted: {MUTED};
    --accent: {ACCENT};
    --signal: {SIGNAL};
    --border: {BORDER};
    --card-bg: {CARD_BG};
    --mono: {MONO};
    --sans: {SANS};
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--fg); font-family: var(--sans); line-height: 1.6; margin: 0; padding: 0; }}
  .container {{ max-width: 980px; margin: 0 auto; padding: 48px 32px 96px 32px; }}
  .doc-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 48px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }}
  .doc-type {{ font-family: var(--mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted); }}
  h1 {{ font-family: var(--sans); font-weight: 300; font-size: 32px; letter-spacing: -0.03em; margin: 0 0 8px 0; color: var(--fg); }}
  h2 {{ font-family: var(--mono); font-size: 11px; margin-top: 56px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.15em; border-top: 1px solid var(--border); padding-top: 16px; }}
  h3 {{ font-family: var(--mono); font-size: 11px; color: var(--accent); margin-top: 28px; text-transform: uppercase; letter-spacing: 0.1em; }}
  p {{ margin: 12px 0; }}
  code, .mono {{ font-family: var(--mono); background: var(--card-bg); padding: 2px 6px; border-radius: 3px; font-size: 0.875em; color: var(--accent); }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }}
  th, td {{ text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  th {{ font-family: var(--mono); font-weight: 400; background: var(--card-bg); color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; }}
  ul, ol {{ padding-left: 24px; }}
  li {{ margin: 4px 0; }}
  .diagram {{ background: var(--card-bg); padding: 24px; border-radius: 4px; border: 1px solid var(--border); margin: 24px 0; overflow-x: auto; }}
  .meta {{ color: var(--muted); font-family: var(--mono); font-size: 11px; letter-spacing: 0.04em; margin-bottom: 32px; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .lead {{ font-size: 15px; color: var(--fg); line-height: 1.7; margin: 0 0 40px 0; max-width: 760px; }}
  .footer {{ margin-top: 80px; padding-top: 20px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
  .footer-tag {{ font-family: var(--mono); font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }}
"""

BUG_SVG = f'''<svg width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
  <rect width="28" height="28" rx="4" fill="{BG}"/>
  <line x1="7" y1="14" x2="21" y2="14" stroke="{MUTED}" stroke-width="1"/>
  <line x1="7" y1="14" x2="14" y2="8" stroke="{MUTED}" stroke-width="1"/>
  <line x1="21" y1="14" x2="14" y2="8" stroke="{MUTED}" stroke-width="1"/>
  <circle cx="7"  cy="14" r="2.5" fill="{CARD_BG}" stroke="{MUTED}" stroke-width="1"/>
  <circle cx="21" cy="14" r="2.5" fill="{CARD_BG}" stroke="{MUTED}" stroke-width="1"/>
  <circle cx="14" cy="8"  r="2.5" fill="{CARD_BG}" stroke="{MUTED}" stroke-width="1"/>
  <circle cx="14" cy="14" r="3"   fill="{SIGNAL}"/>
</svg>'''

DEFS = f'''<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/>
  </marker>
  <marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="{ACCENT}"/>
  </marker>
</defs>'''

def svg_open(width, height):
    return f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width:{width}px;height:auto;display:block;margin:0 auto;">{DEFS}'

def box(x, y, w, h, label, sub="", highlight=False):
    fill = CARD_BG
    stroke = SIGNAL if highlight else BORDER
    stroke_w = "1.5" if highlight else "1"
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>']
    cx = x + w/2
    label_color = SIGNAL if highlight else FG
    if sub:
        out.append(f'<text x="{cx}" y="{y + h/2 - 4}" text-anchor="middle" font-family=\'{MONO}\' font-size="12" font-weight="600" fill="{label_color}">{label}</text>')
        out.append(f'<text x="{cx}" y="{y + h/2 + 13}" text-anchor="middle" font-family=\'{MONO}\' font-size="10" fill="{MUTED}">{sub}</text>')
    else:
        out.append(f'<text x="{cx}" y="{y + h/2 + 5}" text-anchor="middle" font-family=\'{MONO}\' font-size="12" font-weight="600" fill="{label_color}">{label}</text>')
    return "\n".join(out)

def arrow_solid(x1, y1, x2, y2, label="", label_offset=(0, -6)):
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arrow)"/>']
    if label:
        mx = (x1+x2)/2 + label_offset[0]
        my = (y1+y2)/2 + label_offset[1]
        text_w = max(60, len(label)*7)
        out.append(f'<rect x="{mx - text_w/2}" y="{my - 9}" width="{text_w}" height="14" rx="3" fill="{BG}"/>')
        out.append(f'<text x="{mx}" y="{my + 2}" text-anchor="middle" font-family=\'{MONO}\' font-size="10" fill="{MUTED}">{label}</text>')
    return "\n".join(out)

def seq_diagram(width, actors, messages):
    n = len(actors)
    margin_x = 30
    margin_top = 30
    actor_box_h = 44
    lifeline_top = margin_top + actor_box_h + 10
    msg_spacing = 36
    height = lifeline_top + msg_spacing * len(messages) + 30
    actor_w = (width - 2*margin_x) / n
    actor_xs = [margin_x + actor_w*(i+0.5) for i in range(n)]
    parts = [svg_open(width, height)]
    for i, (lbl,) in enumerate(actors):
        bx = actor_xs[i] - actor_w*0.4
        bw = actor_w*0.8
        parts.append(f'<rect x="{bx}" y="{margin_top}" width="{bw}" height="{actor_box_h}" rx="4" fill="{CARD_BG}" stroke="{BORDER}"/>')
        parts.append(f'<text x="{actor_xs[i]}" y="{margin_top + actor_box_h/2 + 5}" text-anchor="middle" font-family=\'{MONO}\' font-size="12" font-weight="600" fill="{FG}">{lbl}</text>')
        parts.append(f'<line x1="{actor_xs[i]}" y1="{lifeline_top}" x2="{actor_xs[i]}" y2="{height - 20}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 4"/>')
    for j, (src, dst, label, kind) in enumerate(messages):
        y = lifeline_top + msg_spacing*(j+1)
        x1, x2 = actor_xs[src], actor_xs[dst]
        if kind == 'dashed':
            parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrow-accent)"/>')
            color = ACCENT
        else:
            parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arrow)"/>')
            color = MUTED
        mx = (x1+x2)/2
        text_w = max(70, len(label)*7)
        parts.append(f'<rect x="{mx - text_w/2}" y="{y - 18}" width="{text_w}" height="14" rx="3" fill="{BG}"/>')
        parts.append(f'<text x="{mx}" y="{y - 7}" text-anchor="middle" font-family=\'{MONO}\' font-size="10" fill="{color}">{label}</text>')
    parts.append("</svg>")
    return "\n".join(parts)

def phase_structure(method_data):
    phases = method_data["phases"]
    n = len(phases)
    W = 940

    if n == 3:
        H = 540
        phase_ys = [60, 240, 420]
        charter_y = 240
    else:
        margin_top = 30
        spacing = 130 if n <= 5 else 110
        phase_ys = [margin_top + i * spacing for i in range(n)]
        H = phase_ys[-1] + 100
        charter_y = phase_ys[len(phase_ys)//2] - 4

    parts = [svg_open(W, H)]
    parts.append(box(20, charter_y, 100, 56, "charter"))

    for (name, sub, imprints), py in zip(phases, phase_ys):
        parts.append(box(180, py, 200, 64, name, sub))
        panel_x = 440
        panel_h = max(110, min(len(imprints), 5) * 22 + 24)
        panel_y = py - (panel_h - 64) / 2
        parts.append(f'<rect x="{panel_x}" y="{panel_y}" width="240" height="{panel_h}" rx="4" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="3 3"/>')
        for i, imp in enumerate(imprints[:5]):
            parts.append(f'<text x="{panel_x+10}" y="{panel_y + 18 + i*22}" font-family=\'{MONO}\' font-size="10" fill="{MUTED}">{imp}</text>')
        if len(imprints) > 5:
            parts.append(f'<text x="{panel_x+10}" y="{panel_y + 18 + 5*22}" font-family=\'{MONO}\' font-size="10" fill="{MUTED}">+ {len(imprints)-5} more</text>')
        parts.append(f'<line x1="380" y1="{py+32}" x2="440" y2="{py+32}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="3 3"/>')
        parts.append(arrow_solid(120, charter_y+28, 180, py+32))

    parts.append(box(720, charter_y, 100, 56, "synthesis", highlight=True))
    parts.append(box(840, charter_y, 80, 56, "handoff"))
    for py in phase_ys:
        parts.append(arrow_solid(380, py+32, 720, charter_y+28))
    parts.append(arrow_solid(820, charter_y+28, 840, charter_y+28))
    parts.append("</svg>")
    return "\n".join(parts)

def overlay_diagram(method_data):
    cfg = method_data["overlay"]
    return seq_diagram(940, cfg["actors"], cfg["messages"])


METHODS = {
    "strategic-positioning": {
        "title": "Strategic Positioning Execution Primer",
        "lead": "A positioning engagement establishes who the company serves, what the brand stands for, where it wins against competitors, and what it should do next to bring its strategy to market. The result is a clear picture of the core customer, the brand promise, the competitive position, and a sequenced plan to act on them.",
        "outputs": [
            ("Charter", "signed JSON artifact"),
            ("Customer-base + segment-fragments", "schema-fragments"),
            ("Brand promise + value prop", "schema-fragments"),
            ("Competitive position + white space", "schema-fragments"),
            ("Channel + merchandising recommendations", "schema-fragments"),
            ("Activation roadmap", "schema-fragment"),
            ("Handoff package", "folder + bus snapshot, signed"),
        ],
        "phases": [
            ("phase 1", "market + core customer", [
                "customer-segmentation", "core-customer-definition",
                "market-sizing", "channel-context-scan", "customer-journey-baseline",
            ]),
            ("phase 2", "brand + competitive position", [
                "brand-promise-articulation", "value-prop-statement",
                "competitive-set-mapping", "white-space-analysis", "differentiation-test",
            ]),
            ("phase 3", "activation strategy", [
                "channel-mix-recommendation", "merchandising-fit-test",
                "experience-pillars", "activation-roadmap",
            ]),
        ],
        "overlay": {
            "title": "Merchandise fit test",
            "description": "Per assortment cluster, score the fit against the core customer. Surface gaps (under-served jobs) and stretches (clusters that don't belong). The fit-test agent reads the customer fragment and the assortment, emits a per-cluster score.",
            "actors": [("Astronaut",), ("Capsule",), ("Fit-Test Agent",), ("Customer Fragment",), ("Merch System",), ("Bus",)],
            "messages": [
                (0, 1, "dispatch merchandise-fit-test", "sync"),
                (1, 5, "load core-customer + target-segments", "sync"),
                (1, 2, "instantiate with assortment scope", "sync"),
                (2, 3, "pull customer jobs + tolerances", "sync"),
                (2, 4, "pull assortment clusters + price ladder", "sync"),
                (2, 5, "emit fit-score per cluster", "sync"),
                (1, 5, "index by cluster, gap, stretch", "sync"),
            ],
        },
        "data_points": [
            ("core-customer-fit-score per cluster", "How well each merchandise cluster serves the core customer", "Drives keep / cut / extend"),
            ("white-space positions", "Unclaimed market positions with viable demand", "Drives brand promise + value prop choices"),
            ("competitive-pressure zones", "Where the brand is most and least pressured", "Drives differentiation focus"),
            ("channel-mix recommendation", "Owned / earned / paid / retail allocation", "Drives marketing investment"),
            ("merchandising-stretch index", "Assortment clusters that don't fit the core customer", "Drives assortment cuts"),
            ("experience-pillar priority", "Signature touches ranked by leverage", "Drives experience-design investment"),
            ("activation sequence", "Moves with dependencies and impact timing", "Drives the launch roadmap"),
        ],
        "handoff_items": [
            ("Engagement record", "folder + bus snapshot"),
            ("Core customer + target segments", "JSON + narrative"),
            ("Brand promise + value prop", "JSON + narrative"),
            ("Competitive set + white space", "JSON + narrative"),
            ("Channel + merchandising recommendations", "JSON + narrative"),
            ("Experience pillars", "JSON + narrative"),
            ("Activation roadmap", "JSON + narrative"),
            ("Open question registry", "issue export"),
            ("Decision log", "append-only JSON"),
        ],
    },

    "sisp": {
        "title": "SISP Execution Primer",
        "lead": "An information systems planning engagement examines how the company's technology supports the business today, defines what it should look like to support the business tomorrow, and produces a prioritized portfolio of projects with a roadmap and investment plan. The result aligns IT with the business and gives leadership a clear program to execute.",
        "outputs": [
            ("Charter", "signed JSON artifact"),
            ("Business strategy alignment", "schema-fragment"),
            ("As-is portfolios (apps, data, tech, governance)", "schema-fragments"),
            ("To-be target architecture", "schema-fragments"),
            ("Project portfolio + prioritization", "schema-fragment"),
            ("Roadmap + investment plan", "schema-fragment"),
            ("Handoff package", "folder + bus snapshot, signed"),
        ],
        "phases": [
            ("phase 1", "business + IS situational alignment", [
                "business-strategy-extraction", "as-is-application-portfolio",
                "as-is-data-architecture", "as-is-tech-architecture",
                "as-is-governance", "alignment-gap-analysis",
            ]),
            ("phase 2", "architecture target", [
                "to-be-application-portfolio", "to-be-data-architecture",
                "to-be-tech-architecture", "governance-target", "capability-gap-mapping",
            ]),
            ("phase 3", "portfolio + roadmap", [
                "project-portfolio-build", "prioritization-matrix",
                "dependency-graph", "roadmap-sequencing", "investment-plan",
            ]),
        ],
        "overlay": {
            "title": "TIME quadrant scoring",
            "description": "Each application is placed on McFarlan's strategic grid — Strategic / Turnaround / Factory / Support — driving the disposition (invest, modernize, maintain, sunset). The quadrant agent reads the app portfolio and the strategic capability needs, emits a quadrant + disposition per app.",
            "actors": [("Astronaut",), ("Capsule",), ("Quadrant Agent",), ("Portfolio Fragment",), ("Strategy Fragment",), ("Bus",)],
            "messages": [
                (0, 1, "dispatch quadrant-scoring", "sync"),
                (1, 5, "load application-portfolio + business-strategy", "sync"),
                (1, 2, "instantiate with portfolio scope", "sync"),
                (2, 3, "pull each app's role + cost + risk", "sync"),
                (2, 4, "pull strategic capability needs", "sync"),
                (2, 5, "emit quadrant + disposition per app", "sync"),
                (1, 5, "index by quadrant, disposition, dependency", "sync"),
            ],
        },
        "data_points": [
            ("TIME quadrant per application", "Strategic / Turnaround / Factory / Support placement", "Drives invest / modernize / maintain / sunset"),
            ("capability-gap matrix", "Required capabilities vs. current capabilities", "Drives target architecture priorities"),
            ("data-domain ownership map", "Domain owners and master-data location", "Drives data governance redesign"),
            ("integration-brittleness index", "Integrations ranked by failure probability + blast radius", "Drives integration consolidation"),
            ("governance-maturity per domain", "Decision rights, funding, standards posture", "Drives operating model redesign"),
            ("project-portfolio prioritization", "Projects scored by NPV + risk + dependency", "Drives portfolio investment"),
            ("roadmap sequencing", "Waves with dependencies and milestones", "Drives execution planning"),
            ("investment plan", "Capex + opex by year by program", "Drives budget submission"),
        ],
        "handoff_items": [
            ("Engagement record", "folder + bus snapshot"),
            ("Business strategy alignment", "JSON + narrative"),
            ("As-is portfolios", "JSON + narrative"),
            ("To-be target architecture", "JSON + narrative"),
            ("TIME quadrant per application", "JSON"),
            ("Project portfolio + dependencies", "JSON + narrative"),
            ("Roadmap + investment plan", "JSON + narrative"),
            ("Open question registry", "issue export"),
            ("Decision log", "append-only JSON"),
        ],
    },

    "saas": {
        "title": "SaaS Execution Primer",
        "lead": "A SaaS engagement examines the commercial, product, and operational reality of a software business — its customers, recurring revenue, technology, integrations, team, and compliance posture — and produces the evidence base leadership or a buyer needs to make sound investment, partnership, or transformation decisions.",
        "outputs": [
            ("Charter", "signed JSON artifact"),
            ("Customer base + ARR cohorts + churn", "schema-fragments"),
            ("Codebase + architecture + tech debt", "schema-fragments"),
            ("Integration map + security posture", "schema-fragments"),
            ("GTM + CS + finance + compliance fragments", "schema-fragments"),
            ("Handoff package", "folder + bus snapshot, signed"),
        ],
        "phases": [
            ("phase 1", "commercial reality", [
                "customer-base-saas", "arr-cohort-analysis",
                "churn-decomposition", "segment-concentration",
                "billing-health", "sales-motion-trace",
            ]),
            ("phase 2", "product + tech reality", [
                "codebase-archeology", "sdlc-characterization",
                "architecture-as-is", "tech-debt-inventory",
                "integration-map", "security-posture",
            ]),
            ("phase 3", "org + ops reality", [
                "team-capability-map", "gtm-motion-trace",
                "cs-support-pattern", "finance-pattern", "compliance-stack-audit",
            ]),
        ],
        "overlay": {
            "title": "ARR cohort decomposition",
            "description": "Break ARR by acquisition cohort. Plot retention curves. Surface which cohorts drive net retention and which drag. The cohort agent reads subscription history and acquisition metadata, emits cohort retention + NRR + drag attribution.",
            "actors": [("Astronaut",), ("Capsule",), ("Cohort Agent",), ("Billing System",), ("CRM",), ("Bus",)],
            "messages": [
                (0, 1, "dispatch arr-cohort-analysis", "sync"),
                (1, 5, "load customer-base + segment-concentration", "sync"),
                (1, 2, "instantiate with cohort scope", "sync"),
                (2, 3, "pull subscription history + MRR per customer", "sync"),
                (2, 4, "pull acquisition date + segment", "sync"),
                (2, 5, "emit cohort retention + NRR + drag attribution", "sync"),
                (1, 5, "index by cohort, segment, vector", "sync"),
            ],
        },
        "data_points": [
            ("ARR cohort retention curves", "Retention curve per acquisition cohort", "Drives NRR forecast and segment focus"),
            ("NRR by segment", "Net revenue retention split by customer segment", "Drives expansion vs. retention motion"),
            ("churn decomposition", "Voluntary / involuntary / downgrade by vector", "Drives churn-reduction priorities"),
            ("segment-concentration risk", "Top-10-by-revenue, concentration over 25%", "Drives diversification strategy"),
            ("tech-debt impact categorized", "Debt categorized by impact and remediation cost", "Drives engineering investment"),
            ("integration blast-radius", "Integration map with break-impact scores", "Drives integration consolidation"),
            ("security-posture gap", "Controls present vs. needed for next compliance cert", "Drives compliance roadmap"),
            ("unit economics", "CAC, LTV, gross margin, burn multiple", "Drives commercial model decisions"),
            ("compliance-stack readiness", "Path to next certification", "Drives compliance investment"),
        ],
        "handoff_items": [
            ("Engagement record", "folder + bus snapshot"),
            ("Customer base + ARR cohorts + churn", "JSON + narrative"),
            ("Codebase + architecture + tech debt", "JSON + narrative"),
            ("Integration graph", "JSON + diagram"),
            ("Security + compliance posture", "JSON + narrative"),
            ("Team + GTM + CS + finance fragments", "JSON + narrative"),
            ("Risk + opportunity register", "JSON + narrative"),
            ("Open question registry", "issue export"),
            ("Decision log", "append-only JSON"),
        ],
    },
    "iso27001-audit": {
        "title": "ISO 27001 Audit Execution Primer",
        "lead": "An ISO 27001 audit examines the organization's information security management system and produces a signed audit report with a recommendation to certify, conditionally certify, or not certify. The certification body uses that recommendation to issue or maintain the certificate. The structured evidence record produced also feeds annual surveillance audits and the three-year recertification cycle.",
        "outputs": [
            ("Charter", "signed JSON artifact"),
            ("ISMS scope, context, interested parties, policy", "schema-fragments"),
            ("Risk register, treatment plan, Statement of Applicability", "schema-fragments"),
            ("Per-Annex-A control implementation evidence", "one schema-fragment per control"),
            ("Audit findings register with classification", "schema-fragment"),
            ("Audit report", "signed synthesis"),
            ("Certification recommendation", "signed decision artifact"),
            ("Corrective action plan + surveillance schedule", "schema-fragments"),
        ],
        "phases": [
            ("phase 0", "provision", [
                "imprint-iso-charter-signing",
                "imprint-iso-environment-provisioning",
            ]),
            ("phase 1", "context + scope (stage 1)", [
                "imprint-iso-isms-scope-verification",
                "imprint-iso-interested-parties-review",
                "imprint-iso-context-issue-mapping",
                "imprint-iso-isms-policy-review",
                "imprint-iso-stage1-readiness-judgment",
            ]),
            ("phase 2", "risk + SoA", [
                "imprint-iso-risk-methodology-review",
                "imprint-iso-risk-register-validation",
                "imprint-iso-risk-treatment-plan-review",
                "imprint-iso-soa-coverage-validation",
            ]),
            ("phase 3", "control evidence (stage 2)", [
                "imprint-iso-control-design-review",
                "imprint-iso-control-evidence-collection",
                "imprint-iso-operating-effectiveness-test",
                "imprint-iso-control-finding-classification",
                "imprint-iso-control-owner-interview",
                "imprint-iso-management-review-evidence",
            ]),
            ("phase 4", "findings synthesis", [
                "imprint-iso-findings-aggregation",
                "imprint-iso-nonconformity-classification",
                "imprint-iso-audit-report-synthesis",
                "imprint-iso-management-response-capture",
            ]),
            ("phase 5", "closeout", [
                "imprint-iso-corrective-action-plan-review",
                "imprint-iso-certification-recommendation",
                "imprint-iso-surveillance-schedule-set",
            ]),
        ],
        "overlay": {
            "title": "Per-control four-step pattern",
            "description": "For each Annex A control in scope, the audit dispatches four imprints in sequence: design review, evidence collection, operating effectiveness test, finding classification. The pattern produces one control-implementation fragment per control with conformity classification (conformity / observation / minor non-conformity / major non-conformity).",
            "actors": [("Astronaut",), ("Capsule",), ("Design Review",), ("Evidence",), ("Effectiveness",), ("Bus",)],
            "messages": [
                (0, 1, "dispatch per-control pattern", "sync"),
                (1, 5, "load policy + procedure fragments", "sync"),
                (1, 2, "design review for control X", "sync"),
                (2, 5, "design adequacy finding", "sync"),
                (1, 3, "evidence collection for control X", "sync"),
                (3, 5, "artifacts indexed", "sync"),
                (1, 4, "operating effectiveness test", "sync"),
                (4, 5, "sample test result", "sync"),
                (1, 5, "compose control-implementation fragment", "sync"),
            ],
        },
        "data_points": [
            ("ISMS scope verification", "Scope statement, exclusions with justification", "Drives Stage 1 readiness judgment"),
            ("SoA coverage validation", "Every Annex A control marked applicable / not applicable with justification", "Drives Stage 2 control selection"),
            ("Risk register validation", "Sample risks with identification, analysis, evaluation, treatment", "Drives risk treatment plan review"),
            ("Per-control design adequacy", "Documentation read, design described", "Drives evidence-collection scope per control"),
            ("Per-control operating effectiveness", "Sample-tested control runs with size, period, results", "Drives conformity classification"),
            ("Findings classification register", "Conformity / observation / minor NC / major NC per control and clause", "Drives certification recommendation"),
            ("Major non-conformities count", "Systemic gaps blocking certification", "Drives recommendation to certify, conditionally certify, or not certify"),
            ("Corrective action plan", "Per non-conformity: root cause, action, owner, target date, retest method", "Drives certification body's decision and follow-up"),
            ("Surveillance schedule", "Annual surveillance + 3-year recertification dates", "Drives long-term engagement cadence"),
        ],
        "handoff_items": [
            ("Engagement record", "folder + bus snapshot"),
            ("ISMS scope, context, policy", "JSON fragments + narrative"),
            ("Risk register, treatment plan, SoA", "JSON + narrative"),
            ("Per-Annex-A control implementations", "JSON fragments per control"),
            ("Audit findings register", "JSON + narrative"),
            ("Audit report", "signed synthesis"),
            ("Certification recommendation", "signed decision"),
            ("Corrective action plan", "JSON + narrative"),
            ("Surveillance schedule", "JSON"),
        ],
    },

    "pci-audit": {
        "title": "PCI DSS Audit Execution Primer",
        "lead": "A PCI DSS audit examines the cardholder data environment and produces a Report on Compliance with an Attestation of Compliance signed by the audit team and the customer. The audit confirms the customer's compliance posture against PCI DSS v4.0.1 requirements and feeds the customer's acquirer and card brand reporting.",
        "outputs": [
            ("Charter", "signed JSON artifact"),
            ("CDE boundary, payment flow, system inventory", "schema-fragments"),
            ("Service provider register, compensating-controls register", "schema-fragments"),
            ("Per-requirement implementation evidence", "one schema-fragment per Req 1-12"),
            ("Quarterly ASV scans + annual pen test results", "evidence captures + summary"),
            ("Findings register with classification", "schema-fragment"),
            ("Report on Compliance", "signed synthesis"),
            ("Attestation of Compliance", "signed by QSA + customer"),
            ("Remediation plan + annual surveillance schedule", "schema-fragments"),
        ],
        "phases": [
            ("phase 0", "provision", [
                "imprint-pci-charter-signing",
                "imprint-pci-environment-provisioning",
                "imprint-pci-qsa-team-credential-verification",
            ]),
            ("phase 1", "scope (CDE)", [
                "imprint-pci-cde-boundary-mapping",
                "imprint-pci-payment-flow-mapping",
                "imprint-pci-system-component-inventory",
                "imprint-pci-segmentation-validation",
                "imprint-pci-saq-or-roc-determination",
            ]),
            ("phase 2", "documentation", [
                "imprint-pci-policy-procedure-review",
                "imprint-pci-service-provider-register-review",
                "imprint-pci-compensating-controls-review",
                "imprint-pci-incident-response-plan-review",
            ]),
            ("phase 3", "technical evidence (stage 2)", [
                "imprint-pci-requirement-design-review",
                "imprint-pci-requirement-evidence-collection",
                "imprint-pci-requirement-operating-effectiveness-test",
                "imprint-pci-requirement-finding-classification",
                "imprint-pci-external-asv-scan-review",
                "imprint-pci-penetration-test-review",
                "imprint-pci-cardholder-data-discovery",
            ]),
            ("phase 4", "findings synthesis", [
                "imprint-pci-findings-aggregation",
                "imprint-pci-nonconformity-classification",
                "imprint-pci-compensating-control-validation",
                "imprint-pci-customized-approach-validation",
                "imprint-pci-roc-synthesis",
            ]),
            ("phase 5", "closeout", [
                "imprint-pci-aoc-issuance",
                "imprint-pci-remediation-plan-review",
                "imprint-pci-annual-surveillance-schedule-set",
                "imprint-pci-acquirer-notification",
            ]),
        ],
        "overlay": {
            "title": "Per-requirement four-step pattern",
            "description": "For each PCI DSS requirement (1-12), the audit dispatches four imprints in sequence: design review, evidence collection, operating effectiveness test, finding classification. The pattern produces one requirement-implementation fragment per requirement with classification (In Place / In Place with Compensating Control / Not Applicable / Not Tested / Not in Place).",
            "actors": [("Astronaut",), ("Capsule",), ("Design Review",), ("Evidence",), ("Effectiveness",), ("Bus",)],
            "messages": [
                (0, 1, "dispatch per-requirement pattern", "sync"),
                (1, 5, "load CDE boundary + policy fragments", "sync"),
                (1, 2, "design review for Req X", "sync"),
                (2, 5, "approach + design adequacy", "sync"),
                (1, 3, "evidence collection for Req X", "sync"),
                (3, 5, "artifacts indexed", "sync"),
                (1, 4, "operating effectiveness test", "sync"),
                (4, 5, "sample test result", "sync"),
                (1, 5, "compose requirement-implementation fragment", "sync"),
            ],
        },
        "data_points": [
            ("CDE boundary verification", "Perimeter, included systems, segmentation validation", "Drives sample selection per requirement"),
            ("Payment flow map", "End-to-end CHD flow: entry, processing, storage, transmission, deletion", "Drives CDE scope reduction discussion"),
            ("Cardholder data discovery", "Scan results: any unaccounted-for CHD outside the CDE", "Drives scope expansion or remediation"),
            ("Per-requirement design adequacy", "Approach (Defined or Customized), design description", "Drives evidence-collection scope per requirement"),
            ("Per-requirement operating effectiveness", "Sample-tested control runs with size, period, results", "Drives In Place / Compensating Control / Not in Place classification"),
            ("Compensating-controls validation", "Risk analysis + control equivalence + monitoring", "Drives QSA acceptance of compensating controls"),
            ("Customized Approach validation", "Targeted risk analysis + equivalence to objective", "Drives QSA acceptance of customized approach"),
            ("ASV scan posture", "Four passing quarterly external scans within assessment period", "Drives Req 11.3 compliance"),
            ("Pen test posture", "Annual application + network + segmentation pen test", "Drives Req 11.4 compliance"),
            ("Findings classification register", "In Place / In Place w/ CC / NA / Not Tested / Not in Place per requirement", "Drives RoC and AoC sign-off"),
            ("Remediation plan", "Per Not in Place finding: action, owner, target date, retest method", "Drives next-cycle re-test"),
        ],
        "handoff_items": [
            ("Engagement record", "folder + bus snapshot"),
            ("CDE boundary + payment flow + system inventory", "JSON fragments + narrative"),
            ("Service provider register", "JSON + responsibility matrix"),
            ("Per-requirement implementations (Req 1-12)", "JSON fragments per requirement"),
            ("ASV scan + pen test results", "captures + summary"),
            ("Findings register", "JSON + narrative"),
            ("Report on Compliance", "signed synthesis"),
            ("Attestation of Compliance", "signed by QSA + customer"),
            ("Remediation plan", "JSON + narrative"),
            ("Annual surveillance schedule", "JSON"),
        ],
    },

}


def render_primer(slug, data):
    phase_svg = phase_structure(data)
    overlay_svg = overlay_diagram(data)

    outputs_rows = "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a,b in data["outputs"])
    data_point_rows = "\n".join(f"<tr><td><code>{n}</code></td><td>{s}</td><td>{d}</td></tr>" for n,s,d in data["data_points"])
    handoff_rows = "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a,b in data["handoff_items"])

    # imprint table grouped by phase
    imprint_blocks = []
    for name, sub, imprints in data["phases"]:
        imp_list = "".join(f"<li><code>{i}</code></li>" for i in imprints)
        imprint_blocks.append(f"<h3>{name} — {sub}</h3>\n<ul>{imp_list}</ul>")
    imprints_section = "\n".join(imprint_blocks)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{data['title']} — Ruptiv</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">

<div class="doc-header">
  <div>
    <div class="doc-type">Execution Primer</div>
    <h1>{data['title']}</h1>
    <div class="meta">Ruptiv · Five-D Method · 2026-05-04</div>
  </div>
  <div>{BUG_SVG}</div>
</div>

<p class="lead">{data['lead']}</p>

<h2>What it produces</h2>
<table>
<tr><th>Output</th><th>Form</th></tr>
{outputs_rows}
</table>

<h2>Phase structure</h2>
<div class="diagram">{phase_svg}</div>

<h2>Imprints per phase</h2>
{imprints_section}

<h2>Method overlay — {data['overlay']['title']}</h2>
<p>{data['overlay']['description']}</p>
<div class="diagram">{overlay_svg}</div>

<h2>Data points produced</h2>
<table>
<tr><th>Data point</th><th>What it captures</th><th>Decision it enables</th></tr>
{data_point_rows}
</table>

<h2>Handoff package</h2>
<table>
<tr><th>Item</th><th>Form</th></tr>
{handoff_rows}
</table>

<h2>Companion specs</h2>
<ul>
<li><code>Brain/wiki/diagnostic-execution-primer.html</code> — substrate primer</li>
<li><code>Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md</code> — artifact types and envelope</li>
<li><code>Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md</code> — imprint header schema</li>
<li><code>Brain/wiki/cards/execution-primer-template.md</code> — primer template spec</li>
</ul>

<div class="footer">
  <span class="footer-tag">Ruptiv · Internal</span>
  <span class="footer-tag">Workflows, reinvented.</span>
</div>

</div>
</body>
</html>"""
    return html


target_dir = "/Users/gclyle/GrowDirect/Brain/wiki"
os.makedirs(target_dir, exist_ok=True)

for slug, data in METHODS.items():
    html = render_primer(slug, data)
    out_path = f"{target_dir}/{slug}-execution-primer.html"
    with open(out_path, "w") as f:
        f.write(html)
    print(f"wrote {out_path} ({len(html):,} bytes)")
