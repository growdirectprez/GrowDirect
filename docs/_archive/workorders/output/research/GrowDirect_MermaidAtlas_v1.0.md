---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GrowDirect — Mermaid Diagram Atlas v1.0

**Version:** 1.0
**Date:** March 1, 2026
**Author:** PhD (Research Framework)
**Classification:** MAXIMUM CONFIDENTIAL — Intellectual Property
**Master Source:** GrowDirect Manifesto v1.1 DRAFT
**Purpose:** Canonical diagram reference for all GrowDirect collateral. Jess references by figure number. Art converts to production SVGs.

---

## Figure Index

| Fig. | Title | Type | Manifesto | Category |
|------|-------|------|-----------|----------|
| 1 | Six-Node Architecture | flowchart TD | V.1 | Architecture |
| 2 | Triple Subscriber Pipeline | flowchart TD | V.2 | Architecture |
| 3 | The Protocol Pipe (End-to-End) | sequenceDiagram | V.4 | Architecture |
| 4 | Three-Layer Protocol Stack | flowchart TD | IV.4, B-071 | Architecture |
| 5 | Hybrid Chain Architecture | flowchart LR | V.1, B-069 | Architecture |
| 6 | The Economic Loop | flowchart TD | IV.1–IV.7 | Economic |
| 7 | Revenue Layer Stack | flowchart BT | IV.1–IV.7 | Economic |
| 8 | The gLog: tLog to gLog Evolution | flowchart LR | I.1, III.4 | Thesis |
| 9 | DAO Governance Phases | flowchart LR | IV.6, B-071 | Economic |
| 10 | L402 Validation Gate Flow | sequenceDiagram | V.5 | Architecture |
| 11 | The Fee Window | flowchart LR | VI.3 | Moat |
| 12 | Competitive Positioning | quadrantChart | VI.6, VII.2 | Moat |
| 13 | DAO Treasury Allocation | pie | IV.6, B-071 | Economic |
| 14 | Appendix C Status Map | flowchart TD | Appendix C | Architecture |

---

## ARCHITECTURE DIAGRAMS

---

### Fig. 1 — Six-Node Architecture

**Caption:** The complete elJeffe pipeline. Every webhook-originated event traverses six nodes in sequence: received, hashed, sealed, parsed, batched, inscribed. Data flows top-down from external source to permanent Bitcoin anchor. Each node is stateless and independently deployable.

**Manifesto:** V.1 — The Six-Node Architecture
**War Chest:** Source 03 (Unified Architecture), Source 10 (Six-Node Reference), Source 50 (Technical Overview)

```mermaid
flowchart TD
    EXT["External Source<br/>(Square Webhooks)"] -->|"HTTPS POST"| N1

    subgraph PIPELINE["elJeffe — Six-Node Architecture"]
        direction TB
        N1["<b>Node 1 — API Gateway</b><br/>OAuth 2.0 · HMAC-SHA256<br/>Correlation ID · Valkey publish"]
        N2["<b>Node 2 — Event Normalizer</b><br/>SHA-256 of raw payload<br/>Hash = permanent event identity"]
        N3["<b>Node 3 — Hash Engine</b><br/>Sub 1: Hash & Seal<br/>INSERT-only evidence store<br/>Hash chain · Immutability triggers"]
        N4["<b>Node 4 — Evidence Store</b><br/>Sub 2: Parse & Route<br/>CRDM canonical schema<br/>26 Chirp rules · Fox case routing"]
        N5["<b>Node 5 — Merkle Batcher</b><br/>Sub 3: Merkle & Ordinal<br/>Accumulate hashes · Build tree<br/>Compute Merkle root"]
        N6["<b>Node 6 — Ordinal Inscriber</b><br/>Inscribe root on Bitcoin L1<br/>OrdinalsBot API (Phase 1)<br/>Return: inscription ID · block height · TX ID"]

        N1 -->|"Raw payload + hash"| N2
        N2 -->|"Valkey Streams"| N3
        N2 -->|"Valkey Streams"| N4
        N2 -->|"Valkey Streams"| N5
        N5 -->|"Merkle root"| N6
    end

    N6 -->|"Anchor receipt"| BTC["Bitcoin L1<br/>Permanent Inscription"]

    N3 -.->|"Evidence sealed"| PG[("PostgreSQL<br/>canary_sales<br/>append-only")]
    N4 -.->|"Alerts & views"| APP[("PostgreSQL<br/>canary_app<br/>reference data")]
    N4 -.->|"Metrics"| MET[("PostgreSQL<br/>canary_metrics<br/>derived analytics")]

    style N1 fill:#1a5276,stroke:#fff,color:#fff
    style N2 fill:#1a5276,stroke:#fff,color:#fff
    style N3 fill:#7d3c98,stroke:#fff,color:#fff
    style N4 fill:#7d3c98,stroke:#fff,color:#fff
    style N5 fill:#7d3c98,stroke:#fff,color:#fff
    style N6 fill:#b7950b,stroke:#fff,color:#fff
    style BTC fill:#f39c12,stroke:#fff,color:#fff
    style EXT fill:#2c3e50,stroke:#fff,color:#fff
    style PG fill:#1e8449,stroke:#fff,color:#fff
    style APP fill:#1e8449,stroke:#fff,color:#fff
    style MET fill:#1e8449,stroke:#fff,color:#fff
```

---

### Fig. 2 — Triple Subscriber Pipeline

**Caption:** The TSP is the heart of elJeffe's processing model. Three competing consumers on a single Valkey Streams queue, each performing a distinct function. Sub 1 seals the legal witness (raw truth). Sub 2 makes data useful (business intelligence). Sub 3 anchors to Bitcoin (permanent record). If Sub 2 fails, Sub 1 has raw original — Sub 2 is a projection that can be reindexed. All three are stateless and horizontally scalable.

**Manifesto:** V.2 — The Triple Subscriber Pipeline
**War Chest:** Source 03 (Unified Architecture), Source 09 (TSP Reference), Source 50 (Technical Overview)

```mermaid
flowchart TD
    NORM["Event Normalizer<br/>SHA-256 hash computed<br/>Raw payload preserved"] -->|"Publish to queue"| VK["Valkey Streams<br/>Durable message queue<br/>At-least-once delivery"]

    VK -->|"Competing consumer"| S1
    VK -->|"Competing consumer"| S2
    VK -->|"Competing consumer"| S3

    subgraph SUB1["Sub 1 — Hash & Seal (The Legal Witness)"]
        S1["Raw payload → SHA-256 hash<br/>INSERT to evidence store<br/>Immutability triggers<br/>Hash chain detection"]
    end

    subgraph SUB2["Sub 2 — Parse & Route (The Business Layer)"]
        S2["Structured parse → CRDM schema<br/>26 Chirp rule evaluation<br/>Alert write → Today's View<br/>Fox case routing"]
    end

    subgraph SUB3["Sub 3 — Merkle & Ordinal (The Anchor)"]
        S3["Batch accumulation<br/>Merkle tree construction<br/>Root computation<br/>Submit for inscription"]
    end

    S1 -->|"Sealed evidence"| DB1[("canary_sales<br/>Append-only ledger")]
    S2 -->|"Parsed data"| DB2[("canary_app<br/>Reference + alerts")]
    S3 -->|"Merkle root"| INS["Ordinal Inscriber<br/>Bitcoin L1 anchor"]

    S2 -.->|"If Sub 2 fails:<br/>reindex from Sub 1 raw"| S1

    style SUB1 fill:#2c3e50,stroke:#7d3c98,color:#fff
    style SUB2 fill:#2c3e50,stroke:#1a5276,color:#fff
    style SUB3 fill:#2c3e50,stroke:#b7950b,color:#fff
    style S1 fill:#7d3c98,stroke:#fff,color:#fff
    style S2 fill:#1a5276,stroke:#fff,color:#fff
    style S3 fill:#b7950b,stroke:#fff,color:#fff
    style VK fill:#e74c3c,stroke:#fff,color:#fff
    style NORM fill:#2c3e50,stroke:#fff,color:#fff
    style INS fill:#f39c12,stroke:#fff,color:#fff
    style DB1 fill:#1e8449,stroke:#fff,color:#fff
    style DB2 fill:#1e8449,stroke:#fff,color:#fff
```

---

### Fig. 3 — The Protocol Pipe (End-to-End)

**Caption:** The complete heartbeat: a single Square event traversing the full protocol from OAuth authorization through Bitcoin inscription and back. This is the proof that elJeffe works end-to-end. Sprint 6 target: first production heartbeat — a real Square merchant event sealed, inscribed, and receipted on Bitcoin.

**Manifesto:** V.4 — The Protocol Pipe
**War Chest:** Source 03 (Unified Architecture), Source 50 (Technical Overview), Source 54 (Lightning Two Phases)

```mermaid
sequenceDiagram
    participant M as Square Merchant
    participant SQ as Square API
    participant GW as Node 1: API Gateway
    participant EN as Node 2: Event Normalizer
    participant VK as Valkey Streams
    participant S1 as Sub 1: Hash & Seal
    participant S2 as Sub 2: Parse & Route
    participant S3 as Sub 3: Merkle & Ordinal
    participant MB as Node 5: Merkle Batcher
    participant OI as Node 6: Ordinal Inscriber
    participant BTC as Bitcoin L1

    M->>SQ: Transaction occurs
    SQ->>GW: Webhook POST (HMAC-SHA256 signed)
    GW->>GW: Validate OAuth 2.0 + signature
    GW->>EN: Forward raw payload
    EN->>EN: Compute SHA-256 hash
    EN->>VK: Publish (payload + hash + correlation ID)

    par Triple Subscriber Pipeline
        VK->>S1: Consume
        S1->>S1: INSERT raw + hash (append-only)
        Note over S1: Evidence sealed (milliseconds)
    and
        VK->>S2: Consume
        S2->>S2: Parse → CRDM schema
        S2->>S2: Evaluate 26 Chirp rules
        Note over S2: Alerts + Today's View updated
    and
        VK->>S3: Consume
        S3->>MB: Accumulate hash
    end

    MB->>MB: Build Merkle tree
    MB->>OI: Submit Merkle root
    OI->>BTC: Inscribe via OrdinalsBot API

    BTC-->>OI: Inscription ID + block height + TX ID
    OI-->>S1: Anchor receipt stored

    Note over M,BTC: Instant response: hash sealed, chain position assigned
    Note over M,BTC: Confirmed (~10 min): inscription ID, block number, explorer URL
```

---

### Fig. 4 — Three-Layer Protocol Stack

**Caption:** The hybrid architecture operates across three distinct layers. Settlement (Bitcoin Ordinals) provides permanence — the chain of record. Execution (Avalanche private subnet) provides speed — sub-second merchant-visible receipts. Treasury (DAO-controlled) provides sustainability — self-funding at scale. Each layer serves a distinct function; together they form a complete protocol.

**Manifesto:** IV.4 — Layer 4: The Scaling Model, B-071 Position Paper
**War Chest:** Source 55 (DAO Treasury Protocol), Source 03 (Unified Architecture), B-069 (Hybrid Chain)

```mermaid
flowchart TD
    subgraph TREASURY["TREASURY LAYER (DAO-Controlled)"]
        direction LR
        T1["Revenue<br/>Allocation"]
        T2["Inscription Pool<br/>Replenishment"]
        T3["Governance<br/>Decisions"]
        T4["Validator<br/>Rewards"]
        T1 --- T2 --- T3 --- T4
    end

    subgraph EXECUTION["EXECUTION LAYER (Avalanche Private Subnet)"]
        direction LR
        E1["Real-time<br/>Receipt Minting"]
        E2["Sub-second<br/>Confirmation"]
        E3["Smart Contract<br/>Inscription Policies"]
        E4["Merchant-visible<br/>Interface"]
        E1 --- E2 --- E3 --- E4
    end

    subgraph SETTLEMENT["SETTLEMENT LAYER (Bitcoin Ordinals)"]
        direction LR
        S1["Merkle Root<br/>Inscription"]
        S2["Permanent<br/>Record"]
        S3["Proof-of-Work<br/>Security"]
        S4["Chain of<br/>Record"]
        S1 --- S2 --- S3 --- S4
    end

    TREASURY <-->|"Fund allocation<br/>Policy governance"| EXECUTION
    EXECUTION <-->|"Periodic rollup<br/>Batch inscription"| SETTLEMENT

    MERCHANT["Merchant Events"] -->|"Real-time flow"| EXECUTION
    SETTLEMENT -->|"Anchor receipts"| PROOF["Permanent Proof<br/>on Bitcoin"]
    TREASURY -->|"40% inscription pool<br/>30% operations<br/>20% development<br/>10% validator rewards"| ALLOC["Self-sustaining<br/>at ~17 merchants"]

    style TREASURY fill:#8e44ad,stroke:#fff,color:#fff
    style EXECUTION fill:#2980b9,stroke:#fff,color:#fff
    style SETTLEMENT fill:#f39c12,stroke:#fff,color:#fff
    style MERCHANT fill:#2c3e50,stroke:#fff,color:#fff
    style PROOF fill:#b7950b,stroke:#fff,color:#fff
    style ALLOC fill:#1e8449,stroke:#fff,color:#fff
```

---

### Fig. 5 — Hybrid Chain Architecture

**Caption:** Sprint 6 builds the pure Ordinals path — direct inscription via OrdinalsBot API. When the hybrid architecture deploys (Phase 2), the Sprint 6 code becomes the Bitcoin adapter within a chain-agnostic adapter layer. Nothing is thrown away. The Avalanche subnet handles real-time receipt minting at $0.001/tx; Bitcoin handles permanent settlement via periodic Merkle root inscriptions at ~$621/year globally. Condor B-069 scored this hybrid 44/50 vs. pure Ordinals 28/50.

**Manifesto:** V.1 — Six-Node Architecture, B-069 (Condor Hybrid Chain)
**War Chest:** B-069 Hybrid Architecture v1.0, B-069 Chain Comparison v1.0

```mermaid
flowchart LR
    EVENT["Merchant<br/>Event"] --> ADAPTER

    subgraph ADAPTER["Chain-Agnostic Adapter"]
        direction TB
        ROUTE{"Route by<br/>phase config"}
        BTC_A["Bitcoin Adapter<br/>(Sprint 6 code)"]
        AVA_A["Avalanche Adapter<br/>(Phase 2)"]
        ROUTE -->|"Phase 1<br/>Sprint 6"| BTC_A
        ROUTE -->|"Phase 2<br/>Hybrid"| AVA_A
    end

    subgraph SPRINT6["SPRINT 6 PATH (Pure Ordinals)"]
        direction TB
        P1_HASH["SHA-256 Hash"]
        P1_SEAL["PostgreSQL Seal"]
        P1_BATCH["Merkle Batch"]
        P1_INS["OrdinalsBot API"]
        P1_HASH --> P1_SEAL --> P1_BATCH --> P1_INS
    end

    subgraph HYBRID["PHASE 2 PATH (Hybrid)"]
        direction TB
        P2_RECEIPT["Avalanche Subnet<br/>Real-time receipt<br/>$0.001/tx · sub-second"]
        P2_BATCH["Periodic Rollup<br/>Batch subnet events"]
        P2_INS["Bitcoin Inscription<br/>Merkle root of rollup<br/>~$621/year global"]
        P2_RECEIPT --> P2_BATCH --> P2_INS
    end

    BTC_A --> SPRINT6
    AVA_A --> HYBRID

    SPRINT6 --> BTC1["Bitcoin L1<br/>Direct inscription"]
    HYBRID --> BTC2["Bitcoin L1<br/>Rollup inscription"]

    BTC1 --> SAME["Same Permanent<br/>Anchor"]
    BTC2 --> SAME

    style EVENT fill:#2c3e50,stroke:#fff,color:#fff
    style ADAPTER fill:#34495e,stroke:#e74c3c,color:#fff
    style SPRINT6 fill:#1a5276,stroke:#fff,color:#fff
    style HYBRID fill:#7d3c98,stroke:#fff,color:#fff
    style BTC1 fill:#f39c12,stroke:#fff,color:#fff
    style BTC2 fill:#f39c12,stroke:#fff,color:#fff
    style SAME fill:#b7950b,stroke:#fff,color:#fff
    style ROUTE fill:#e74c3c,stroke:#fff,color:#fff
```

---

## ECONOMIC / THESIS DIAGRAMS

---

### Fig. 6 — The Economic Loop

**Caption:** The self-reinforcing flywheel. Merchant events generate inscriptions. Inscriptions create the validation base. Validation requests generate sat payments via L402. Sats flow to treasury. Treasury funds more inscriptions. More inscriptions expand the validation base. The loop compounds: every past inscription generates future validation revenue indefinitely. Self-sustaining at approximately 17 merchants.

**Manifesto:** IV.1–IV.7 (All Revenue Layers)
**War Chest:** Source 04 (Economic Flywheel), Source 55 (DAO Treasury), Source 41 (Mining Economics)

```mermaid
flowchart TD
    MERCH["Merchant Events<br/>(Square webhooks)"] -->|"Notarize"| INSCRIBE

    INSCRIBE["Inscription Engine<br/>Seal → Batch → Inscribe<br/>on Bitcoin L1"] -->|"Permanent record"| POOL

    POOL["Inscription Pool<br/>Growing base of<br/>notarized events"] -->|"Every event = future income"| VALIDATE

    VALIDATE["Validation Requests<br/>Auditors · Regulators · Courts<br/>Counterparties · Insurance"] -->|"POST /validate"| L402

    L402["L402 Gate<br/>HTTP 402 → Lightning invoice<br/>→ pay sats → 200 OK + proof"] -->|"Sat payments"| TREASURY

    TREASURY["DAO Treasury<br/>40% pool replenishment<br/>30% operations<br/>20% development<br/>10% validator rewards"] -->|"Fund inscriptions"| INSCRIBE

    MERCH -.->|"Subscription revenue<br/>(the door)"| TREASURY
    L402 -.->|"Validation revenue<br/>(the house)"| TREASURY

    GROW["Network Growth<br/>More merchants<br/>→ more events<br/>→ more inscriptions<br/>→ more validations"] -.->|"Compounds<br/>monotonically"| MERCH

    style MERCH fill:#2c3e50,stroke:#fff,color:#fff
    style INSCRIBE fill:#1a5276,stroke:#fff,color:#fff
    style POOL fill:#7d3c98,stroke:#fff,color:#fff
    style VALIDATE fill:#b7950b,stroke:#fff,color:#fff
    style L402 fill:#e74c3c,stroke:#fff,color:#fff
    style TREASURY fill:#1e8449,stroke:#fff,color:#fff
    style GROW fill:#f39c12,stroke:#fff,color:#fff
```

---

### Fig. 7 — Revenue Layer Stack

**Caption:** Seven cumulative revenue layers, each building on the one below. Layer 1 (inscription pool) is the asset. Layer 2 (notarization) is the operation. Layer 3 (validation gate) is the recurring revenue. Layers 4–7 are scale, moat, network, and vision respectively. Traditional SaaS stops at Layer 2. elJeffe's economics begin at Layer 3 and compound through Layer 7.

**Manifesto:** IV.1–IV.7
**War Chest:** Source 04 (Economic Model), Source 06 (Revenue Layers), Source 55 (DAO Protocol)

```mermaid
flowchart BT
    L1["<b>Layer 1 — The Inscription Pool</b><br/>The Asset<br/>Bitcoin treasury → mint Ordinals<br/>Every sat = permanent balance sheet asset"]

    L2["<b>Layer 2 — The Notarization Service</b><br/>The Operation<br/>Receive → seal → batch → inscribe<br/>Instant hash + confirmed inscription"]

    L3["<b>Layer 3 — The Validation Gate</b><br/>The Revenue<br/>L402 micropayment per validation<br/>Perpetual royalty on time chain"]

    L4["<b>Layer 4 — The Scaling Model</b><br/>The Infrastructure<br/>Auto-purchase block space at threshold<br/>Fee-aware · Idle costs nothing"]

    L5["<b>Layer 5 — Block Space as Write Access</b><br/>The Mining Moat<br/>Mining reward → inscription raw material<br/>Zero fee competition via pool relationship"]

    L6["<b>Layer 6 — The Network Effect</b><br/>The Platform<br/>Basic → Treasury → Full Node → Enterprise<br/>DAO governance · Self-sustaining at ~17 merchants"]

    L7["<b>Layer 7 — The Egalitarian Copyright</b><br/>The Vision<br/>Smart contract royalties on Bitcoin<br/>No VIP lane · Coffee shop = Universal Music"]

    L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7

    style L1 fill:#1a5276,stroke:#fff,color:#fff
    style L2 fill:#1a5276,stroke:#fff,color:#fff
    style L3 fill:#e74c3c,stroke:#fff,color:#fff
    style L4 fill:#7d3c98,stroke:#fff,color:#fff
    style L5 fill:#7d3c98,stroke:#fff,color:#fff
    style L6 fill:#b7950b,stroke:#fff,color:#fff
    style L7 fill:#f39c12,stroke:#fff,color:#fff
```

---

### Fig. 8 — The gLog: tLog to gLog Evolution

**Caption:** Three eras of transaction logging. The IBM 4690 tLog (1986) was the foundation of modern retail — mutable, proprietary, locked in a box. Modern POS logs (cloud era) moved the data but kept the mutability problem. The gLog — (∞)log — (2026) anchors every event to Bitcoin's proof-of-work time chain. Geoffrey's Log: the permanent successor. Same data. Immutable record. No box.

**Manifesto:** I.1 — The tLog Problem, III.4 — The gLog
**War Chest:** Source 01 (Founder Story), Source 40 (tLog to gLog Case), Source 50 (Technical Overview)

```mermaid
flowchart LR
    subgraph ERA1["1986 — IBM 4690 tLog"]
        direction TB
        T1_DESC["Transaction log on POS terminal<br/>Foundation of retail data<br/>Every scan, tender, void recorded"]
        T1_PROP["Mutable · Proprietary<br/>Locked in the box<br/>Jeffe built the world's largest<br/>private retail database on this"]
    end

    subgraph ERA2["2000s — Modern POS Logs"]
        direction TB
        T2_DESC["Cloud-hosted transaction data<br/>Square · Shopify · Toast<br/>Webhooks stream events"]
        T2_PROP["Still mutable · Cloud servers<br/>Provider controls record<br/>No cryptographic proof<br/>Chargebacks = word vs. word"]
    end

    subgraph ERA3["2026 — The gLog"]
        direction TB
        T3_DESC["Geoffrey's Log<br/>Bitcoin-anchored event record<br/>SHA-256 hash · Merkle root<br/>Ordinal inscription"]
        T3_PROP["Immutable · Permanent<br/>Proof-of-work secured<br/>Merchant owns proof<br/>Receipts outlive the company"]
    end

    ERA1 -->|"Data moved<br/>to cloud"| ERA2
    ERA2 -->|"Data anchored<br/>to Bitcoin"| ERA3

    style ERA1 fill:#7f8c8d,stroke:#fff,color:#fff
    style ERA2 fill:#2c3e50,stroke:#fff,color:#fff
    style ERA3 fill:#f39c12,stroke:#fff,color:#fff
```

---

### Fig. 9 — DAO Governance Phases

**Caption:** Progressive decentralization triggered by merchant count thresholds. Phase 1: traditional company, maximum speed, clear accountability. Phase 2: multi-signature treasury, merchant advisory board, governance weight distributes. Phase 3: full DAO-controlled protocol, Wyoming DUNA legal framework, governance weight from inscription volume — not token purchase. The protocol earns its decentralization.

**Manifesto:** IV.6 — Layer 6: The Network Effect, B-071 Position Paper
**War Chest:** Source 55 (DAO Treasury Protocol), Source 34 (Network Effect Brief)

```mermaid
flowchart LR
    subgraph P1["PHASE 1 — Foundation<br/>Now → 100 merchants"]
        direction TB
        P1A["Traditional company"]
        P1B["Founding team controls<br/>all decisions"]
        P1C["Maximum speed<br/>Clear accountability"]
        P1A --- P1B --- P1C
    end

    subgraph P2["PHASE 2 — Council<br/>100 → 1,000 merchants"]
        direction TB
        P2A["Multi-sig treasury"]
        P2B["Merchant advisory board"]
        P2C["Key decisions require<br/>council approval"]
        P2D["GrowDirect remains<br/>operator"]
        P2A --- P2B --- P2C --- P2D
    end

    subgraph P3["PHASE 3 — Full Protocol<br/>1,000+ merchants"]
        direction TB
        P3A["DAO-controlled treasury"]
        P3B["Governance weight from<br/>inscription volume"]
        P3C["Wyoming DUNA<br/>legal framework"]
        P3D["Protocol self-governs"]
        P3A --- P3B --- P3C --- P3D
    end

    P1 -->|"100 merchants<br/>threshold"| P2
    P2 -->|"1,000 merchants<br/>threshold"| P3

    SELF["Self-sustaining<br/>at ~17 merchants"] -.-> P1

    style P1 fill:#1a5276,stroke:#fff,color:#fff
    style P2 fill:#7d3c98,stroke:#fff,color:#fff
    style P3 fill:#f39c12,stroke:#fff,color:#fff
    style SELF fill:#1e8449,stroke:#fff,color:#fff
```

---

### Fig. 10 — L402 Validation Gate Flow

**Caption:** The validation gate in action. A client posts an event hash and inscription ID. The server responds with HTTP 402 — Payment Required — and a Lightning invoice denominated in sats. Client pays the invoice. Server returns 200 OK with full Merkle proof: verified status, block number, Merkle position, inscription ID, timestamp, canonical authority, and proof path. Caller can independently verify without trusting GrowDirect. At scale, validation revenue dominates. Subscription is the door. L402 gate is the house.

**Manifesto:** V.5 — The L402 Validation Gate
**War Chest:** Source 07 (L402 Gate Reference), Source 54 (Lightning Two Phases)

```mermaid
sequenceDiagram
    participant C as Client<br/>(Auditor / Regulator /<br/>Court / Insurer)
    participant API as elJeffe API<br/>POST /validate
    participant LN as Lightning Network
    participant DB as Evidence Store
    participant BTC as Bitcoin L1

    C->>API: POST /validate<br/>{ event_hash, inscription_id }

    API->>DB: Lookup event hash
    DB-->>API: Found — inscription exists

    API-->>C: 402 Payment Required<br/>Lightning invoice: N sats

    C->>LN: Pay invoice
    LN-->>API: Payment confirmed

    API->>DB: Retrieve Merkle proof
    API->>BTC: Verify inscription on-chain

    API-->>C: 200 OK<br/>{ verified: true,<br/>  block: 884201,<br/>  merkle_position: 4721,<br/>  inscription_id: "i39f7a...",<br/>  timestamp: "2026-02-26T14:23:01Z",<br/>  canonical_authority: "eljeffe.io",<br/>  merkle_proof_path: [...] }

    Note over C,BTC: Client can independently verify<br/>proof without trusting GrowDirect
    Note over C,BTC: No expiration · No cancellation<br/>No marginal cost · O(log n) proof computation
```

---

## MOAT / COMPETITIVE DIAGRAMS

---

### Fig. 11 — The Fee Window

**Caption:** Time-dependent moat. Bitcoin transaction fees are historically low today (1–3 sat/vB, ~$0.02 per inscription). Three escalation drivers converge: halving cycle compresses block reward, adoption increases fee floor, inscription competition consumes block space. Break-even for a bootstrapped competitor: 50–100 sat/vB sustained. Point of no return: 12–24 months from genesis. Every month GrowDirect inscribes at current rates, competitor cost to achieve parity increases. The gap widens monotonically. Under hybrid economics, Genesis Pool funds 13–68 years of operations.

**Manifesto:** VI.3 — The Fee Window
**War Chest:** Source 41 (Mining Economics), Source 05 (Fee Window Analysis), B-069 (Hybrid Economics)

```mermaid
flowchart LR
    subgraph NOW["TODAY<br/>Fee Window OPEN"]
        direction TB
        NOW1["1–3 sat/vB<br/>~$0.02 per inscription"]
        NOW2["GrowDirect mints<br/>Genesis Pool"]
        NOW3["Accumulates inscriptions<br/>at low cost"]
        NOW1 --- NOW2 --- NOW3
    end

    subgraph DRIVERS["ESCALATION DRIVERS"]
        direction TB
        D1["Halving cycle<br/>Block reward compression<br/>→ miners rely on fees"]
        D2["Adoption demand<br/>L2 opens/closes · DeFi<br/>→ block space consumed"]
        D3["Inscription competition<br/>More entities discover<br/>→ fee pressure rises"]
        D1 --- D2 --- D3
    end

    subgraph CLOSE["WINDOW CLOSES<br/>12–24 months"]
        direction TB
        C1["50–100 sat/vB sustained"]
        C2["Competitor break-even<br/>threshold reached"]
        C3["New entrant cannot replicate<br/>throughput + history<br/>at comparable cost"]
        C1 --- C2 --- C3
    end

    subgraph AFTER["AFTER WINDOW"]
        direction TB
        A1["GrowDirect holds<br/>accumulated position"]
        A2["Genesis Pool: 13–68 years<br/>under hybrid economics"]
        A3["Gap widens<br/>monotonically"]
        A1 --- A2 --- A3
    end

    NOW -->|"Fees rising"| DRIVERS
    DRIVERS -->|"Point of<br/>no return"| CLOSE
    CLOSE -->|"Permanent<br/>structural lead"| AFTER

    style NOW fill:#1e8449,stroke:#fff,color:#fff
    style DRIVERS fill:#b7950b,stroke:#fff,color:#fff
    style CLOSE fill:#e74c3c,stroke:#fff,color:#fff
    style AFTER fill:#f39c12,stroke:#fff,color:#fff
```

---

### Fig. 12 — Competitive Positioning

**Caption:** GrowDirect occupies a category that does not yet have a name. Enterprise LP vendors (Appriss, Sysrepublic, Agilence) serve large chains but are not Bitcoin-native, hold no Ordinal keys, and stop at 500+ locations. Generic blockchain timestampers (OpenTimestamps, OriginStamp) provide timestamps but not LP intelligence, CRDM analytics, or merchant tooling. Cloud providers (AWS, Oracle) could build notification services but cannot fabricate a time-chain position or Genesis Pool minted from a founder's mining reward. GrowDirect is first on chain, with keys, with receipts, targeting the 4.5M+ Square merchants with zero LP tools today.

**Manifesto:** VI.6 — Competitive Positioning, VII.2 — Competitive Landscape
**War Chest:** Source 11 (Competitive Analysis), Source 48 (Market Brief), Source 42 (Merchant Weapon)

```mermaid
quadrantChart
    title Competitive Positioning: Bitcoin-Native LP
    x-axis "Generic Tooling" --> "LP-Specialized"
    y-axis "Mutable Infrastructure" --> "Bitcoin-Native"
    quadrant-1 "GrowDirect Territory"
    quadrant-2 "No Current Player"
    quadrant-3 "Cloud Providers"
    quadrant-4 "Enterprise LP"
    "GrowDirect (elJeffe)": [0.85, 0.90]
    "Appriss Retail": [0.80, 0.15]
    "Sysrepublic": [0.70, 0.10]
    "Agilence": [0.75, 0.12]
    "StoreIQ": [0.65, 0.10]
    "OpenTimestamps": [0.15, 0.80]
    "OriginStamp": [0.20, 0.75]
    "AWS": [0.30, 0.20]
    "Oracle": [0.35, 0.18]
    "Microsoft": [0.25, 0.15]
```

---

## ADDITIONAL DIAGRAMS

---

### Fig. 13 — DAO Treasury Allocation at Maturity

**Caption:** At protocol maturity (Phase 3, 1,000+ merchants), the DAO treasury allocates revenue across four functions. 40% replenishes the inscription pool — the productive asset that generates all validation revenue. 30% covers operations. 20% funds protocol development. 10% rewards validators. Self-sustaining at approximately 17 merchants; at that threshold, protocol revenue covers all inscription costs, operations, and development without external capital.

**Manifesto:** IV.6 — Layer 6: The Network Effect, B-071 Position Paper
**War Chest:** Source 55 (DAO Treasury Protocol)

```mermaid
pie title DAO Treasury Allocation at Maturity
    "Inscription Pool Replenishment" : 40
    "Operations" : 30
    "Development" : 20
    "Validator Rewards" : 10
```

---

### Fig. 14 — Appendix C Status Map: What Is Live vs. What Is Next

**Caption:** Current state of the elJeffe protocol mapped across four deployment horizons. LIVE TODAY: 26 webhooks, 16 API families, TSP pipeline (33 files, 3,247 lines), evidence seal layer. SPRINT 6: OAuth self-auth, webhook signature verification, OrdinalsBot bridge, first production heartbeat. PHASE 2: Avalanche subnet, chain-agnostic adapter, stacked inscriptions, L402 gate. FUTURE: DAO governance (Phase 3), Kubernetes auto-purchase, hash rate leasing, cross-vertical expansion.

**Manifesto:** Appendix C — What Is Live vs. Sprint 6 vs. Future Architecture
**War Chest:** Source 03 (Unified Architecture), Source 50 (Technical Overview), Attack Plan v3.0

```mermaid
flowchart TD
    subgraph LIVE["LIVE TODAY ✅"]
        direction TB
        L1["26 Square webhooks<br/>all 200 OK"]
        L2["16 API families<br/>mapped and wired"]
        L3["TSP pipeline committed<br/>33 files · 3,247 lines"]
        L4["Sprint 5 baseline<br/>tagged @ 72d0082"]
        L5["Evidence seal layer<br/>(Sub 1) built"]
        L6["Capability Dashboard live"]
    end

    subgraph S6["SPRINT 6 🔧"]
        direction TB
        S6A["OAuth 2.0 self-auth"]
        S6B["Webhook signature<br/>verification"]
        S6C["OrdinalsBot inscription<br/>bridge"]
        S6D["Production credentials<br/>cutover"]
        S6E["First production<br/>heartbeat"]
    end

    subgraph PH2["PHASE 2 🏗️"]
        direction TB
        PH2A["Avalanche private<br/>subnet"]
        PH2B["Chain-agnostic<br/>adapter"]
        PH2C["Stacked inscriptions<br/>on designated sat"]
        PH2D["L402 gate<br/>deployment"]
        PH2E["Self-custody<br/>evaluation"]
    end

    subgraph FUT["FUTURE ARCHITECTURE 🗺️"]
        direction TB
        FUT1["DAO governance<br/>(Phase 3)"]
        FUT2["Kubernetes<br/>auto-purchase"]
        FUT3["Pool relationship /<br/>hash rate leasing"]
        FUT4["Cross-vertical expansion<br/>healthcare · supply chain"]
        FUT5["Heartbeat network<br/>always-on monitoring"]
    end

    LIVE -->|"Sprint 6<br/>delivers"| S6
    S6 -->|"Phase 1<br/>validates"| PH2
    PH2 -->|"Scale<br/>demands"| FUT

    style LIVE fill:#1e8449,stroke:#fff,color:#fff
    style S6 fill:#2980b9,stroke:#fff,color:#fff
    style PH2 fill:#7d3c98,stroke:#fff,color:#fff
    style FUT fill:#b7950b,stroke:#fff,color:#fff
```

---

## Rendering Notes

### Mermaid Compatibility

All diagrams in this atlas use standard Mermaid syntax compatible with:

- GitHub Markdown rendering (`.md` files with mermaid code blocks)
- Mermaid Live Editor (https://mermaid.live)
- VS Code Mermaid Preview extension
- Any CommonMark renderer with Mermaid support

### Color Legend (consistent across all diagrams)

| Color | Hex | Meaning |
|-------|-----|---------|
| Dark blue | `#1a5276` | Core pipeline / infrastructure |
| Purple | `#7d3c98` | Processing / transformation |
| Gold | `#b7950b` | Bitcoin / settlement |
| Orange | `#f39c12` | Bitcoin L1 / final state |
| Red | `#e74c3c` | Critical path / payment gate |
| Green | `#1e8449` | Data stores / live systems |
| Dark gray | `#2c3e50` | External / entry points |
| Gray | `#7f8c8d` | Legacy / historical |

### Art Direction Notes

When Art converts these to production SVGs:

1. Maintain the color semantics — they are consistent across all 14 figures
2. Fig. 1 and Fig. 2 are the most reproduced — optimize for both slide and document context
3. Fig. 6 (Economic Loop) is the investor pitch centerpiece — prioritize visual clarity
4. Fig. 12 (Competitive Positioning) may need manual adjustment for presentation — quadrant chart rendering varies across tools
5. Fig. 3 and Fig. 10 (sequence diagrams) may be tall — consider horizontal layout for slides

---

*Atlas compiled from GrowDirect Manifesto v1.1 DRAFT, War Chest sources 01–55, PhD prior output (22 briefs), and Condor B-069 architecture work. Every diagram references running code, filed IP, or documented architecture — not aspirational concepts.*

**— PhD, Research Framework**
**March 1, 2026**
