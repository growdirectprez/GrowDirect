---
classification: internal
type: wiki
sub-type: atlas
status: active
date: 2026-04-30
last-compiled: 2026-04-30
needs-review: 2026-05-08
source: brainstorm session 2026-04-30 — DriftPOS intake → long-arc reframe → PCI / data hosting compliance
companion: rapidpos-driftpos-platform-brief.md
companion: cards/platform-thesis.md
---

# Canary Long-Arc Atlas

**Governing thesis.** Canary's long-term destination is to become the merchant POS by absorption — not a permanent intelligence layer on top of Counterpoint. The four-phase arc spans 5-7 years, ends with Counterpoint turned off, and pulls Canary into both PCI Service Provider scope and full SaaS data-hosting compliance at Phase 4. This atlas collects the twelve diagrams that anchor the strategic and architectural decisions surrounding that arc. **This is internal strategy. External surfaces (CRB, CATz, NCR, marketing, partner conversations) stay Phase-1-framed throughout.**

## Atlas index

| # | Title | Anchors |
|---|---|---|
| I.1 | Four-phase long arc | The strategic spine — Counterpoint replacement by absorption |
| I.2 | Where the players sit on the arc | NCR, Bart, DriftPOS, Canary positioned by phase |
| I.3 | DriftPOS maturity ladder | Where the architecture-doc evidence places DriftPOS today |
| II.1 | Card data flow with PCI boundary | Pinpad → processor — Canary never touches card data |
| II.2 | Compliance gate between Phase 3 and Phase 4 | $500K-$1M / 12-18 month PCI work-stream |
| II.3 | Compliance scope rings | Trust → SOC 2 → privacy → PCI nested regimes |
| III.1 | CRDM in the cloud | Algorithms (IP) + outputs (tenant data) + anchors (public) |
| III.2 | POSBackend interface | Single interface, multiple adapters (Track 2 — parked) |
| III.3 | 13-module spine + adapter location | Where `internal/posbackend/` lives in Canary Go |
| IV.1 | Per-tenant request flow | Tenant resolution → pool cache → tenant DB |
| IV.2 | Demo loop (Day 4 deliverable) | Plan-and-write loop for the parked Track 2 prototype |
| V.1 | Prototype plan reframed | Track 1 stays, Track 2 parks, Friday = Phase 1 framing |

## Part I — The Strategic Spine

### I.1 — Four-phase long arc

Canary's destination by phase. Phase 0-2 are observable from where we sit today. Phase 3-4 are architectural intent that requires the compliance gate (II.2) to clear.

```mermaid
flowchart LR
    P0["Phase 0 today<br/>Counterpoint runs<br/>the merchant"]
    P1["Phase 1<br/>Canary alongside<br/>intelligence layer"]
    P2["Phase 2<br/>Canary absorbs<br/>workflows Counterpoint<br/>does badly or not at all"]
    P3["Phase 3<br/>Canary runs the<br/>register-adjacent experience<br/>Counterpoint = back-office residual"]
    P4["Phase 4<br/>Canary IS the POS<br/>Counterpoint turned off"]
    P0 --> P1 --> P2 --> P3 --> P4
    style P0 fill:#3b1a1a,stroke:#fff,color:#fff
    style P1 fill:#3b3b00,stroke:#fff,color:#fff
    style P2 fill:#1a3b3b,stroke:#fff,color:#fff
    style P3 fill:#1a3b1a,stroke:#fff,color:#fff
    style P4 fill:#0d4d0d,stroke:#fff,color:#fff
```

Memory anchor: `project_canary_replaces_counterpoint_long_arc.md`.

### I.2 — Where the players sit on the arc

DriftPOS attempts the one-shot Counterpoint-to-DriftPOS replacement at Phase 4. Canary attempts replacement-by-absorption from Phase 1 onward. Both routes target the same destination. Bart's company is parallel-competitor + distribution-partner-for-Phase-1 simultaneously — the simplest meeting framing keeps it Phase 1.

```mermaid
flowchart TB
    NCR[NCR Voyix - defends Counterpoint]
    Bart[Bart VAR - Counterpoint reseller]
    CG[Canary Go today]
    CG2[Canary 2027-28]
    DP[DriftPOS - leaps to P4 directly]
    CG3[Canary 2029+]
    P0[Phase 0] --> P1[Phase 1] --> P2[Phase 2] --> P3[Phase 3] --> P4[Phase 4]
    NCR --> P0
    Bart --> P0
    CG --> P1
    CG2 --> P2
    DP --> P4
    CG3 --> P4
    style DP fill:#3b1a3b,stroke:#fff,color:#fff
    style NCR fill:#3b1a1a,stroke:#fff,color:#fff
    style Bart fill:#3b1a1a,stroke:#fff,color:#fff
    style CG fill:#1f3b73,stroke:#fff,color:#fff
    style CG2 fill:#1a3b3b,stroke:#fff,color:#fff
    style CG3 fill:#0d4d0d,stroke:#fff,color:#fff
```

### I.3 — DriftPOS maturity ladder

Where the evidence in the DriftPOS architecture document places that platform today. Yellow = the band the evidence supports (foundational-only module list, hypothetical worked examples, "honest gaps" listed unresolved, zero customer mentions, internal Azure DevOps URLs). Dashed-green = the optimistic ceiling we can't rule out without asking. The wiki brief was over-positioned at "multi-tenant 5+ paying" before this calibration.

```mermaid
flowchart LR
    D1[Design<br/>doc only]
    D2[Skeleton<br/>boots locally]
    D3[Internal pilot<br/>RapidPOS staff dogfooding]
    D4[First customer<br/>one paying tenant]
    D5[Multi-tenant<br/>5+ paying]
    D6[Mature<br/>fleet]
    D1 --> D2 --> D3 --> D4 --> D5 --> D6
    style D2 fill:#3b3b00,stroke:#fff,color:#fff
    style D3 fill:#3b3b00,stroke:#fff,color:#fff
    style D4 fill:#1a3b1a,stroke:#fff,color:#fff,stroke-dasharray: 4 2
```

Memory anchor: `feedback_arch_doc_not_maturity.md`.

## Part II — Compliance & Trust

### II.1 — Card data flow with PCI boundary

Semi-integrated POS — same model Square / Toast / Lightspeed / Clover use. Card data flows pinpad → processor and never enters Canary. Red boxes are inside the Cardholder Data Environment. The POS application sees only auth result + masked PAN.

```mermaid
flowchart LR
    Card[Customer card]
    Pinpad[Pinpad PED<br/>P2PE certified]
    Proc[Payment processor<br/>Heartland FreedomPay etc]
    POS[POS application<br/>Counterpoint today<br/>Canary at Phase 4]
    Bank[Card brand bank]
    Card -->|swipe insert tap| Pinpad
    Pinpad -->|encrypted at swipe<br/>P2PE blob| Proc
    Proc -->|auth request| Bank
    Bank -->|approve decline| Proc
    Proc -->|auth result only<br/>no PAN no track| Pinpad
    Pinpad -->|auth result + masked PAN| POS
    POS -->|charge command| Pinpad
    style Pinpad fill:#3b1a1a,stroke:#fff,color:#fff
    style Proc fill:#3b1a1a,stroke:#fff,color:#fff
    style POS fill:#0d4d0d,stroke:#fff,color:#fff
```

Memory anchor: `project_pci_scope_phase4.md`.

### II.2 — Compliance gate between Phase 3 and Phase 4

The Phase 3-to-Phase 4 transition has a real compliance work-stream that funds and runs *before* first paying transaction at Phase 4. ~$500K-$1M launch + 12-18 months. Same gate any new entrant would have to pay — a moat once crossed.

```mermaid
flowchart LR
    P1[Phase 1<br/>zero PCI scope]
    P2[Phase 2<br/>zero PCI scope]
    P3[Phase 3<br/>scope decision point]
    GATE[PCI compliance gate<br/>SSF + DSS-SP + EMV certs<br/>500K-1M, 12-18 months]
    P4[Phase 4<br/>Service Provider scope]
    P1 --> P2 --> P3 --> GATE --> P4
    style GATE fill:#3b1a1a,stroke:#fff,color:#fff
    style P4 fill:#0d4d0d,stroke:#fff,color:#fff
```

### II.3 — Compliance scope rings

Four nested regimes apply at Phase 4. PCI is the innermost (most prescriptive, narrowest). The merchant trust contract is the outermost — and the only one that's commercial rather than regulatory. Combined Phase 4 launch readiness: ~$1-1.5M; ongoing $500K-$1M/year.

```mermaid
flowchart LR
    Trust[Trust contract]
    SOC[SOC 2 + ISO 27001]
    Privacy[GDPR + CCPA]
    PCI[PCI SSF + DSS-SP]
    Canary[Canary Phase 4]
    Trust --> SOC --> Privacy --> PCI --> Canary
    style Canary fill:#0d4d0d,stroke:#fff,color:#fff
    style PCI fill:#3b1a1a,stroke:#fff,color:#fff
    style Privacy fill:#3b3b00,stroke:#fff,color:#fff
    style SOC fill:#1a3b3b,stroke:#fff,color:#fff
    style Trust fill:#1f3b73,stroke:#fff,color:#fff
```

Memory anchor: `project_data_hosting_compliance_phase4.md`.

## Part III — Architecture

### III.1 — CRDM in the cloud

CRDM runs in our GCP environment alongside the rest of the Canary Go runtime. Three distinct things live in the cloud, each with its own protection posture: algorithms (purple — trade secret + patents, never shipped), per-tenant outputs (green — subject to data-hosting compliance from II.3), and public blockchain anchors (blue — hash-only, no plaintext, evidentiary rail by design).

```mermaid
flowchart TB
    txn[transactions]
    inv[inventory + costs]
    vendor[vendor invoices]
    algo[CRDM algorithms + weights<br/>core IP]
    ilwac[5-dim ILWAC engine]
    rib[RIB batch builder]
    cost[satoshi cost dims]
    wac[weighted avg cost]
    anchor[blockchain anchors]
    Merch[Merchant Backoffice<br/>sees own outputs only]
    Public[L2 blockchain<br/>hash anchors only]
    txn --> ilwac
    inv --> ilwac
    vendor --> ilwac
    algo --> ilwac
    ilwac --> rib
    rib --> cost
    rib --> wac
    rib --> anchor
    cost --> Merch
    wac --> Merch
    anchor --> Public
    style algo fill:#3b1a3b,stroke:#fff,color:#fff
    style ilwac fill:#3b1a3b,stroke:#fff,color:#fff
    style cost fill:#0d4d0d,stroke:#fff,color:#fff
    style anchor fill:#1f3b73,stroke:#fff,color:#fff
```

Open architectural decision pending: shared-service CRDM (network-effect moat, careful cross-tenant engineering) versus per-tenant CRDM (clean compliance, no compounding). Recommended: shared service with strict tenant-scoped data flow + offline aggregate learning on de-identified extracts.

### III.2 — POSBackend interface (Track 2 — parked)

The keeper artifact from the Track 2 prototype, even though Track 2 itself parks indefinitely. A single Go interface that Counterpoint, DriftPOS, and any future POS implements. Spine modules import the interface; `cmd/server/main.go` wires the implementation.

```mermaid
flowchart LR
    item[item]
    inv[inventory]
    xfer[transfer]
    pricing[pricing]
    ret[returns]
    owl[owl analytics]
    IF[POSBackend interface]
    cp[counterpoint adapter]
    dp[driftpos adapter]
    sq[square adapter]
    CPS[(Counterpoint SQL)]
    MOCK[driftpos-mock 9090]
    SQS[(Square API)]
    item --> IF
    inv --> IF
    xfer --> IF
    pricing --> IF
    ret --> IF
    owl --> IF
    IF --> cp
    IF --> dp
    IF --> sq
    cp --> CPS
    dp --> MOCK
    sq --> SQS
    style IF fill:#1f3b73,stroke:#fff,color:#fff
    style MOCK fill:#444,stroke:#999,color:#fff,stroke-dasharray: 4 2
```

### III.3 — 13-module spine + adapter location

`internal/posbackend/` is shared infrastructure. Every spine module that needs POS data depends on the interface, none know which adapter is wired in. Same modules-manifest pattern as DriftPOS, applied to backend selection instead of feature loading.

```mermaid
flowchart TB
    hawk[hawk detection]
    bull[bull events]
    IF[Backend interface]
    cp[counterpoint]
    dp[driftpos]
    item[item]
    asset[asset]
    inv[inventory]
    recv[receiving]
    xfer[transfer]
    pricing[pricing]
    emp[employee]
    cust[customer]
    ret[returns]
    rep[report]
    owl[owl 8084 analytics]
    iaas[inventory-as-a-service 9081]
    item --> IF
    asset --> IF
    inv --> IF
    recv --> IF
    xfer --> IF
    pricing --> IF
    cust --> IF
    ret --> IF
    IF --> cp
    IF --> dp
    iaas --> IF
    owl --> bull
    bull --> hawk
    style IF fill:#1f3b73,stroke:#fff,color:#fff
    style dp fill:#2d5016,stroke:#fff,color:#fff
```

## Part IV — Operational Sequences

### IV.1 — Per-tenant request flow

Direct steal from DriftPOS architecture §13: per-tenant Postgres, fungible hosts, request-time tenant resolution. The pool cache eviction policy matters as tenant counts grow — 50 tenants × 5 pools × 20 connections = 5,000 connections per host. File as a Canary Go ADR before the spine ships.

```mermaid
sequenceDiagram
    autonumber
    participant Cli as Canary client
    participant Mid as TenantMiddleware
    participant Reg as Tenant registry
    participant Pool as Postgres pool cache
    participant DB as Tenant DB
    participant POS as POSBackend
    Cli->>Mid: HTTP request<br/>X-Tenant-Id acme-cove
    Mid->>Reg: lookup acme-cove
    Reg-->>Mid: dsn + backend driftpos
    Mid->>Pool: pool acme-cove
    alt cache miss
        Pool->>DB: NewDataSource dsn
        DB-->>Pool: pool ref
    end
    Pool-->>Mid: pool ref
    Mid->>POS: ctx with tenant + pool + backend
    POS->>DB: SELECT FROM products
    DB-->>POS: rows
    POS-->>Cli: JSON
```

### IV.2 — Demo loop (Day 4 of the parked Track 2)

The plan-and-write loop that would have demoed the DriftPOS adapter against the mock. Two reads, one write, one render. Track 2 parks but the *interface* this exercises is still the keeper.

```mermaid
sequenceDiagram
    autonumber
    participant CG as Canary Go
    participant ADP as DriftPOS adapter
    participant MOCK as driftpos-mock 9090
    participant DB as mock tenant DB
    Note over CG: assortment plan job
    CG->>ADP: Inventory PositionByStore
    ADP->>MOCK: GET catalog inventory
    MOCK->>DB: SELECT
    DB-->>MOCK: stock rows
    MOCK-->>ADP: JSON
    ADP-->>CG: InventoryPosition
    Note over CG: compute multi-tier plan
    CG->>ADP: Plans PostTransferRec
    ADP->>MOCK: POST sync recommendations
    MOCK->>DB: INSERT recommendation
    DB-->>MOCK: ok
    MOCK-->>ADP: 201 + plan_id
    ADP-->>CG: PlanReceipt
    Note over MOCK: Backoffice page<br/>shows queued rec
```

## Part V — Reframes

### V.1 — Prototype plan reframed by the long arc

How the DriftPOS prototype recommendation changed once the long-arc framing landed: Track 1 (steal architectural patterns into Canary Go's design) gets *more* valuable, Track 2 (build an adapter against DriftPOS) parks indefinitely (not just delayed), and Friday's meeting reframes from platform-to-platform negotiation to a Phase 1 conversation anchored on the CATz pitch.

```mermaid
flowchart LR
    T1[Track 1 STAYS]
    T2[Track 2 PARKS]
    FRI[Friday Phase 1 framing]
    style T1 fill:#1a3b1a,stroke:#fff,color:#fff
    style T2 fill:#3b1a1a,stroke:#fff,color:#fff
    style FRI fill:#1f3b73,stroke:#fff,color:#fff
```

## What this changes downstream

Three documents are misaligned with the long arc and need updates when convenient. None are urgent before Friday — the meeting itself is Phase 1 framed regardless.

- **`Brain/wiki/cards/platform-thesis.md`** — add an internal-only Phase 4 destination section. Keep externally-facing summary Phase 1 framed.
- **`Brain/wiki/rapidpos-driftpos-platform-brief.md`** — re-cast DriftPOS as parallel competitor + architectural prior art (not peer integration target). Update the maturity assessment to match I.3. Promote "deployment status — live customers today?" to question #1.
- **`Brain/projects/Canary.md` MOC** — anchor the project narrative on the four-phase arc.

## References

- Memory: `project_canary_replaces_counterpoint_long_arc.md`
- Memory: `project_pci_scope_phase4.md`
- Memory: `project_data_hosting_compliance_phase4.md`
- Memory: `feedback_arch_doc_not_maturity.md`
- Wiki: [[rapidpos-driftpos-platform-brief]]
- Wiki: [[cards/platform-thesis]]
