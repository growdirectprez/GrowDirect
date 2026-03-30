---
type: workorder
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Architecture Diagram Standard Document
**Version 1.0 | February 26, 2026**

---

## 1. Diagram Type Definitions

### Type 1: System Context Diagram

| Attribute | Detail |
|-----------|--------|
| **Audience** | Everyone — merchants, investors, board, partners |
| **Purpose** | Present the system in relation to the outside world. No internal components visible. One-page overview. |
| **Required Contents** | System as single logical box; data sources (any network, webhooks); data owners (merchant, source platform, GrowDirect); inbound flows (webhooks, events); outbound flows (alerts, evidence records, validation responses) |
| **Level of Detail** | High-level, no Crown Jewels exposed |
| **IP Classification** | Investor-safe. No proprietary internals. |

### Type 2: Component Diagram

| Attribute | Detail |
|-----------|--------|
| **Audience** | Technical team (engineering, architecture, PM) |
| **Purpose** | Show internal components and all connections between them. Enable engineers to understand data flow, technology choices, and scale points. |
| **Required Contents** | All six nodes (receiver, queue, three subscribers, validation API); labeled data flow arrows (what moves, when, format); technology annotation per component (e.g., "Valkey Streams", "PostgreSQL JSONB"); phase annotations where applicable (Phase 1 Docker, Phase 3 K8s) |
| **Level of Detail** | Medium. Component names, technology stack, queuing strategy. No source code. |
| **IP Classification** | May contain Crown Jewels. Internal documentation only. |

### Type 3: Deployment Diagram

| Attribute | Detail |
|-----------|--------|
| **Audience** | Engineering, DevOps, investors (credibility/operational maturity) |
| **Purpose** | Show where everything runs and scales. Two distinct versions required: Phase 1 (now) and Phase 3 (scale). |
| **Required Contents** | **Phase 1**: Single machine, Docker Compose, all services + managed PostgreSQL outside; **Phase 3**: Kubernetes cluster boundaries, per-service autoscaling annotations, managed PostgreSQL explicitly outside cluster boundary, ingress/egress points. |
| **Level of Detail** | Infrastructure-focused. Resource allocation, scaling parameters, external dependencies explicitly marked. |
| **IP Classification** | Phase 1 can be external. Phase 3 investor-safe (no secrets, no keys). |

### Type 4: Data Flow Diagram

| Attribute | Detail |
|-----------|--------|
| **Audience** | Patent filing, legal counsel, technical investors (due diligence) |
| **Purpose** | Trace the complete journey of a single event from source transmission → sealed evidence → Bitcoin inscription → validation. Must be legally precise for patent applications. |
| **Required Contents** | Every atomic step with cryptographic operations explicitly annotated (HMAC verify, SHA-256 hash, Merkle tree build, Ordinal inscription, bilateral verification); two response timelines (instant seal vs. ~10 min Bitcoin confirmation); bilateral verification path (dotted line showing stored hash compared against source network send log) |
| **Level of Detail** | High precision. Every operation named. Hash algorithms, key derivation, signature schemes all specified. Feeds patent filing. |
| **IP Classification** | Confidential — Internal Only. Contains notarization method. |

### Type 5: Business Model Diagram

| Attribute | Detail |
|-----------|--------|
| **Audience** | Investors, board, potential partners |
| **Purpose** | One visual showing the complete business model loop: Treasury assets → Ordinal pool → merchant notarization → validation payment → GrowDirect revenue. |
| **Required Contents** | Treasury (sat pool owner); inscription pool (asset/resource); any network (customer input); notarization service (operation); validation API (L402 gate); sat payment (revenue mechanism); Bitcoin foundation (trustless ledger). Revenue flow explicitly highlighted. |
| **Level of Detail** | Strategic. Focus on money flow, asset ownership, and revenue mechanism. Technical depth secondary. |
| **IP Classification** | Investor-safe. Public-friendly version exists. |

---

## 2. Tool Decision Matrix

| Diagram Type | Primary Tool | Secondary Tool | Use Case | Rationale |
|---|---|---|---|---|
| System Context | draw.io | — | Investor deck, partner presentations, public materials | Visual polish, easy export to PNG/PDF/SVG. Version control via SVG export to docs/. |
| Component | Mermaid | — | PRDs, technical RFC, architecture decisions | Plain-text, version-controlled in Git, renders natively in GitHub. Single source of truth. |
| Deployment (Phase 1) | Mermaid | draw.io (for investor variant) | Engineering documentation, sprint planning | Phase 1 is simple enough for Mermaid. draw.io variant for investor credibility. |
| Deployment (Phase 3) | draw.io | Mermaid (internal ref) | Investor materials, customer trust. Internal K8s spec | K8s complexity benefits from visual fidelity. draw.io easier for stakeholder communication. |
| Data Flow | Mermaid | — | Patent filing, legal review, technical spec | Precision required. Mermaid sequence diagrams handle parallel flows well. Version control mandatory for legal audit trail. |
| Business Model | draw.io | — | Investor deck, board materials, partner onboarding | Business flow + visual polish. High stakeholder impact. |

**Principle:** *Mermaid is the default for technical documentation (Git-versioned, renders in GitHub). draw.io is used when visual polish or non-technical stakeholder communication is primary.*

---

## 3. Brand Standards

### Color Palette

| Color | Hex | Primary Use | Context |
|---|---|---|---|
| Signal Yellow | #FBBF24 | Most important component, primary revenue flow, message queues | Call attention. Use sparingly. |
| Deep Blue | #1F4D78 | Infrastructure, storage, databases, PostgreSQL | Stability, foundation, data at rest. |
| Health Green | #10B981 | Active/healthy state, successful completion, running services | Operational health, positive signal. |
| Alert Red | #EF4444 | Failure states, rejected events, blocked transactions | Critical attention, errors, blocks. |
| Charcoal | #374151 | Text on light backgrounds, labels, annotations | Standard text, readable. |
| Ink | #0D1117 | Dark background option, text on light fills | High contrast, dark mode. |

### Typography

| Context | Font | Use |
|---|---|---|
| Web / screen (Mermaid, GitHub) | Inter | All digital documentation, technical diagrams |
| Word / PowerPoint / investor materials | Calibri | Exported decks, printed materials, client-facing documents |

### Layout Rules

1. **Data flow direction:** Left-to-right or top-to-bottom. No bidirectional crossing arrows. If flow is bidirectional, show separately (dotted for verification/confirmation paths).
2. **Component labeling:** Every box must have component name + technology (e.g., "Webhook Receiver (Node.js + Express)" or "PostgreSQL JSONB Store").
3. **Arrow labeling:** Every arrow labeled with what flows (e.g., "raw JSON payload", "hash + chain_id", "Merkle root").
4. **Grouping:** Use swim lanes or explicit cluster boundaries for multi-component systems (e.g., Kubernetes cluster).
5. **Verification paths:** Dotted lines for bilateral verification, confirmation, or audit trails.
6. **Bitcoin layer:** Distinctive styling — gold border or special fill to distinguish trustless/immutable layer.

### Version and Classification

- **Version footer on every diagram:** `v[N] | [Month Day, Year] | CONFIDENTIAL — Internal Only` (or omit classification for external).
- **Diagram title:** Descriptive, includes type (e.g., "Component Diagram — Triple Subscriber Pipeline").
- **Date:** Maintain version history. Old versions archived, never deleted.

---

## 4. File Naming and Storage Convention

### Location

- **Technical diagrams (Mermaid source):** Embedded in the document they describe (PRD, RFC, ADR). Also stored standalone in `docs/diagrams/`.
- **Standalone diagrams (draw.io, Figma exports):** Stored by type.
- **Investor materials:** `Canary_IP/Markdown/Investor/diagrams/`

### Naming Convention

```
[Component]_[Type]_v[Version].[Format]

Examples:
  - Canary_ComponentDiagram_DualSubscriber_v1.0.md (Mermaid in Markdown)
  - Canary_DeploymentDiagram_Phase3_Kubernetes_v1.0.svg (draw.io export)
  - Canary_SystemContext_v1.0.png (investor variant, PNG)
  - Canary_DataFlow_SingleTransaction_v1.0.md (Mermaid in Markdown)
```

### Format by Tool

| Tool | Primary Format | Secondary Formats | Storage |
|---|---|---|---|
| Mermaid | `.md` (source + rendering) | `.svg` (export for embedding) | `docs/diagrams/[type]/` |
| draw.io | `.svg` (version control) | `.png`, `.pdf` (exports for decks) | `Canary_IP/Markdown/Investor/diagrams/` |
| Figma | `.pdf` (export) | `.png` (high-res) | `Canary_IP/Markdown/Investor/decks/` |

---

## 5. Required Diagrams — Immediate Queue

| # | Diagram | Type | Tool | Audience | Owner | Status | Feed |
|---|---|---|---|---|---|---|---|
| 1 | Full Pipeline System Context | System Context | draw.io | Merchants, investors, board | Jess + Art | Not started | Investor deck, partner materials |
| 2 | Triple Subscriber Component View | Component | Mermaid | Technical team | Jess | **IN PROGRESS** | PRDs, architecture decisions |
| 3 | Phase 1 Docker Compose Deployment | Deployment | Mermaid | Engineering, DevOps | Jess + Jeremy | Not started | Engineering docs, sprint planning |
| 4 | Phase 3 Kubernetes Deployment | Deployment | draw.io | Engineering, investors (credibility) | Jess + Tom | Not started | Investor materials, operational maturity |
| 5 | Single Transaction Data Flow | Data Flow | Mermaid | Patent filing, legal, technical investors | Jess + PhD | Not started | Patent application, legal review |
| 6 | Business Model Flow | Business Model | draw.io | Investors, board | Jess + Jeffe | Not started | Investor deck, board materials |

---

## 6. Agent Standing Instruction Block

Copy this block into your session context when working on architecture diagrams. It ensures consistency across all team members.

```
─────────────────────────────────────────────────────────────
ARCHITECTURE DIAGRAM STANDARD — GrowDirect

When creating or updating architecture diagrams:

TOOL SELECTION:
  • Mermaid (.md): Technical diagrams (component, data flow, deployment Phase 1)
    → Version control, Git-versioned, GitHub rendering
  • draw.io (.svg): System context, investor/deployment diagrams, business model
    → Visual polish, easy export, stakeholder communication

COLOR CODES (Brand Palette):
  • Signal Yellow #FBBF24 — queues, revenue flows, critical paths
  • Deep Blue #1F4D78 — databases, storage, infrastructure
  • Health Green #10B981 — active services, success states
  • Alert Red #EF4444 — failure, rejection, blocked states
  • Charcoal #374151 — text on light backgrounds
  • Ink #0D1117 — dark backgrounds

LAYOUT RULES:
  ✓ Data flows left-to-right or top-to-bottom
  ✓ No crossing arrows (use grouping/layers instead)
  ✓ Every component labeled: Name + Technology
  ✓ Every arrow labeled: What flows, when, format
  ✓ Dotted lines for verification/bilateral paths
  ✓ Bitcoin layer marked distinctively (gold border or special fill)

NAMING CONVENTION:
  [Component]_[Type]_v[Version].[Ext]
  Example: Canary_ComponentDiagram_DualSubscriber_v1.0.md

VERSION & CLASSIFICATION:
  Footer on every diagram: v[N] | [Month Day, Year] | CONFIDENTIAL — Internal Only
  Or remove classification for external materials.

DOCUMENTATION:
  ✓ Mermaid source in .md files, stored in docs/diagrams/[type]/
  ✓ draw.io exports as .svg (version control), .png/.pdf for decks
  ✓ Investor materials in Canary_IP/Markdown/Investor/diagrams/

QUESTIONS?
  Refer to: Jess_ArchDiagram_Standard_v1.0.md
─────────────────────────────────────────────────────────────
```

---

## 7. Review and Approval Workflow

1. **Author:** Jess (primary), with technical input from subject-matter expert (Tom for architecture, Jeremy for deployment, PhD for patent flow).
2. **Technical review:** Tom or Jeremy (architecture/deployment review).
3. **Brand/visual review:** Art (Figma/draw.io polish, color consistency).
4. **Legal review:** Syd (Data Flow diagrams, patent filing).
5. **Approval gate:** Jeffe (final sign-off for all external materials).

All diagrams are stored in Git. Version bumps trigger review cycle. No unsigned diagrams go external.

---

## 8. Maintenance and Versioning

- **Version bump triggers:** Architecture change, new deployment phase, new tool, brand refresh.
- **Archive old versions:** Keep in Git history. Do not delete. Link to current version in documents.
- **Quarterly review:** Jess audits all diagrams for accuracy and brand compliance.
- **Update frequency:** Diagrams updated synchronously with architecture changes. No diagram lags architecture.

---

**End of Standard Document**

---

## Appendix: Quick Reference for Each Diagram Type

### System Context Diagram Checklist
- [ ] System shown as one box
- [ ] Data sources labeled (any network, webhooks)
- [ ] Data owners identified (merchant, platform, GrowDirect)
- [ ] Inbound flows labeled (webhook, event, request)
- [ ] Outbound flows labeled (alert, evidence, validation response)
- [ ] No internal components visible
- [ ] Draw.io or Figma for visual polish
- [ ] Investor-safe (no Crown Jewels)

### Component Diagram Checklist
- [ ] All six nodes present (receiver, queue, Sub 1, Sub 2, Sub 3, API)
- [ ] Data flow arrows labeled (what, when, format)
- [ ] Technology annotations per component
- [ ] Phase annotations (Phase 1 Docker, Phase 3 K8s)
- [ ] Mermaid source, version-controlled
- [ ] Bilateral verification path (dotted)
- [ ] Bitcoin layer marked distinctively

### Deployment Diagram Checklist
- [ ] Phase 1 and Phase 3 both shown (or separate diagrams)
- [ ] Docker Compose details (Phase 1)
- [ ] Kubernetes cluster boundary (Phase 3)
- [ ] PostgreSQL explicitly outside cluster
- [ ] Autoscaling annotations per service
- [ ] Ingress/egress marked
- [ ] Resource allocation visible (or in notes)
- [ ] draw.io for visual clarity

### Data Flow Diagram Checklist
- [ ] Every atomic step numbered and named
- [ ] Cryptographic operations annotated (HMAC, SHA-256, Merkle, Ordinal)
- [ ] Two response timelines (instant vs. ~10 min Bitcoin)
- [ ] Bilateral verification path shown
- [ ] Validation path shown (POST → L402 → verified response)
- [ ] Mermaid sequence or graph, version-controlled
- [ ] Precise enough for patent filing

### Business Model Diagram Checklist
- [ ] Treasury → Ordinal pool shown
- [ ] Merchant → notarization → validation shown
- [ ] L402 payment gate shown
- [ ] Revenue flow highlighted (Signal Yellow)
- [ ] Bitcoin foundation layer visible
- [ ] draw.io for stakeholder communication
- [ ] Investor-safe, no technical depth required
