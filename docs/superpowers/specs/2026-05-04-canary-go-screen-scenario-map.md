---
type: spec
title: Canary Go — Screen-Level User Scenario Map
status: draft
date: 2026-05-04
source: 2026-05-04-counterpoint-canary-ux-crosswalk.md × 2026-05-03-canary-go-ui-wave-plan.md
gro: TBD
purpose: For every Canary Go screen: user role, entry points, enumerated user scenarios, primary elements, actions, CP equivalent, and UX design callouts. Input document for wireframe briefs.
---

# Canary Go — Screen-Level User Scenario Map

**Governing thesis:** Every screen on the Canary Go portal is a named surface that a specific user role visits to accomplish a specific set of tasks. This document enumerates every scenario per screen so that wireframe briefs can be written from a complete scenario set — not from guesswork about what operators need.

**Structure per screen:**
- **URL** and screen title
- **Who** — primary user role(s)
- **How they get here** — entry points
- **Scenarios** — numbered user stories (actor + action + outcome)
- **Primary display elements** — what's on screen
- **Actions available** — buttons, links, mutations
- **CP equivalent** — what form/screen this replaces in Counterpoint
- **UX callout** — design decision or improvement over CP

**Roles:**
- `LP` — Loss Prevention Investigator
- `MGR` — Store Manager
- `BYR` — Buyer / Merchandising Manager
- `RCV` — Receiving Clerk
- `ADM` — Admin / IT / Operator
- `EMP` — Employee (clock-in only)

---

## Admin (Cross-Wave)

---

### `/admin/users` — Users List

**Who:** ADM  
**Entry points:** Admin nav item, Settings → Users link

**Scenarios:**
1. ADM views all active user accounts across all tenants
2. ADM searches for a specific user by name or email
3. ADM sees at a glance which users have LP Investigator vs Manager vs Viewer roles
4. ADM identifies users who have never logged in (provisioned but inactive)
5. ADM clicks through to a user record to change their role
6. ADM deactivates a user who has left the organization

**Primary display:** Paginated table — name, email, role badge, last login, status (active/inactive), tenant. Search bar. Filter by role.  
**Actions:** View user, Deactivate user, Invite new user  
**CP equivalent:** `frmsecuritycodes` + user record management (security codes form + user records — two separate places in CP)  
**UX callout:** CP splits users and security codes into two separate forms. Canary unifies: role = security profile, assigned on one screen.

---

### `/admin/users/:id` — User Detail + Role Assignment

**Who:** ADM  
**Entry points:** Users list row click

**Scenarios:**
1. ADM views a user's current role and tenant assignment
2. ADM promotes a Viewer to LP Investigator
3. ADM restricts a Manager to Viewer (role demotion)
4. ADM assigns a user to specific stores (multi-store tenants)
5. ADM resets a user's access (force re-authentication)
6. ADM views the user's last 10 login events

**Primary display:** User profile card — name, email, role selector, store assignment checklist, login history.  
**Actions:** Save role changes, Reset access, Deactivate  
**CP equivalent:** User record maintenance + security code assignment  
**UX callout:** CP requires navigating to two separate forms. Canary: one screen, immediate role change, store-scoped access in one save.

---

### `/admin/audit` — Audit Log

**Who:** ADM, LP  
**Entry points:** Admin nav, Case detail → "View system events"

**Scenarios:**
1. ADM verifies who changed a detection rule and when
2. ADM investigates a suspected configuration tampering event
3. LP Investigator confirms a case mutation was made by a specific user
4. ADM exports audit log for compliance review
5. ADM filters audit log by user, action type, or date range

**Primary display:** Time-ordered log — timestamp, actor, action type, affected entity, hash of record state. Filters: user, action type, date range, entity type. Export button.  
**Actions:** Filter, Export (CSV), Link to affected entity  
**CP equivalent:** None — Counterpoint has no audit trail  
**UX callout:** CP has zero audit capability. Every Canary mutation carries actor + timestamp + record hash. This screen is the forensic surface for that chain.

---

### `/admin/config` — System Config Health

**Who:** ADM  
**Entry points:** Admin nav, Alert when config ingestion fails

**Scenarios:**
1. ADM checks which tenants have completed store config sync (N.1–N.3)
2. ADM identifies a store whose LP substrate fields (drawer thresholds, discount caps) are not yet populated — blocking LP rules from firing
3. ADM sees last successful sync time per tenant
4. ADM manually triggers a config re-sync for a specific tenant
5. ADM diagnoses a failed sync (error message + last attempt)

**Primary display:** Tenant table — tenant name, N.1 sync status, N.2 sync status, N.3 sync status, LP substrate status (populated/missing), last sync timestamp, error indicator.  
**Actions:** Re-sync tenant config, View sync error detail  
**CP equivalent:** None — Counterpoint has no cloud-side config health surface  
**UX callout:** Critical for multi-tenant operations. A tenant whose config hasn't synced has no LP coverage — operators need to know immediately.

---

## Wave 1 — LP Investigator Core

---

### `/alerts` — Alert List

**Who:** LP, MGR  
**Entry points:** Primary nav, Email notification link, Dashboard alert widget

**Scenarios:**
1. LP opens their shift and reviews new alerts since last login
2. LP filters alerts by severity (Critical / High / Medium) to triage
3. LP filters alerts by store to focus on their assigned location
4. LP filters alerts by alert type (drawer, discount, void, comp) to work a specific detection family
5. LP sees which alerts are unacknowledged vs acknowledged vs escalated
6. MGR reviews alert volume for their store over the past week
7. LP bulk-acknowledges low-severity alerts that don't warrant investigation
8. LP clicks an alert to open its detail and begin investigation

**Primary display:** Table — severity badge, alert type, rule name, store, cashier/terminal, transaction amount, timestamp, status badge (New / Acknowledged / Escalated / Case-linked). Filters: severity, store, alert type, date range, status. Bulk-select for mass acknowledge.  
**Actions:** View detail, Acknowledge (single/bulk), Escalate, Link to case, Export  
**CP equivalent:** None — Counterpoint has no alert surface  
**UX callout:** This is Canary's primary entry point. The LP investigator starts every shift here. Speed of triage matters — severity filtering and bulk acknowledge are not secondary features.

---

### `/alerts/:id` — Alert Detail + Acknowledge

**Who:** LP, MGR  
**Entry points:** Alert list row, Email notification deep-link

**Scenarios:**
1. LP reviews the full context of an alert: which rule fired, what transaction triggered it, what threshold was exceeded
2. LP views the raw ticket data that triggered the alert (line items, tender, cashier, terminal, time)
3. LP views the cashier's alert history (have they triggered this rule before?)
4. LP views the customer's profile (if customer-linked transaction)
5. LP acknowledges the alert with a disposition code (explained / suspicious / escalate)
6. LP escalates to a Hawk case — alert becomes the seed evidence record
7. LP adds a note explaining why this alert is a false positive
8. LP views the allow-list entry that should have suppressed this alert but didn't (surfaced if rule fired on an allow-listed pattern — indicates allow-list needs update)

**Primary display:** Alert header (severity, rule, store, timestamp), Transaction card (ticket # with line detail, tender, cashier, terminal), Cashier alert history (sparkline + count by rule type), Customer card (if present — name, risk score, case history), Rule context panel (what the rule checks, what threshold was exceeded, what the actual value was). Disposition selector. Notes field.  
**Actions:** Acknowledge + disposition, Escalate to case, Add note, View full transaction, View cashier profile, Update allow-list  
**CP equivalent:** None  
**UX callout:** The most-used screen in the system. The rule context panel (what the rule checks vs what it found) is critical — LP investigators need to explain alerts to managers. CP operators currently do this entirely from memory.

---

### `/settings/alert-routing` — Alert Routing Config

**Who:** ADM, MGR  
**Entry points:** Settings nav, Alert detail → "Why wasn't I notified?"

**Scenarios:**
1. ADM configures which alert severity levels trigger email notifications vs in-app only
2. ADM routes Critical alerts to the LP manager's mobile email immediately
3. ADM assigns alerts for Store A to LP Investigator X, Store B to Investigator Y
4. MGR configures their own notification preferences (digest vs immediate)
5. ADM sets business hours for alert delivery (suppress 2am notifications for non-critical)

**Primary display:** Routing rules table — severity level, delivery channel (in-app / email / SMS), recipients (by role or individual), schedule (immediate / business hours / digest). Per-store routing overrides.  
**Actions:** Add routing rule, Edit rule, Delete rule, Test notification  
**CP equivalent:** None — Counterpoint has no notification system  
**UX callout:** Alert fatigue is a real problem in LP. Routing configuration is what keeps the system from becoming noise.

---

### `/rules` — Detection Rules List

**Who:** LP, ADM  
**Entry points:** Primary nav, Alert detail → "View rule"

**Scenarios:**
1. LP audits which of the 24 detection rules are currently enabled for their tenant
2. LP sees which rules are firing most frequently (alert volume per rule)
3. LP disables a rule that is producing excessive false positives during a training period
4. ADM enables a new rule that was previously disabled
5. LP searches for a specific rule by name or rule family
6. LP identifies which rules apply to which transaction types

**Primary display:** Table — rule name, rule family (11 families), description, enabled/disabled toggle, alert count (30 days), last fired timestamp, allow-list dependency indicator. Filter by rule family, status.  
**Actions:** Enable/disable toggle, View rule detail, Search  
**CP equivalent:** None  
**UX callout:** Show alert count per rule inline — LP needs to know which rules are "hot" vs silent before they start investigating. CP has no equivalent; LP teams currently guess.

---

### `/rules/:id` — Detection Rule Detail + Enable/Disable

**Who:** LP, ADM  
**Entry points:** Rules list, Alert detail → rule name link

**Scenarios:**
1. LP reads the full description of what a rule detects and why it matters
2. LP reviews the threshold configuration (e.g., "fires when discount > 20% on any single line")
3. LP views the alert history for this rule (recent alerts, cashiers most frequently triggering)
4. LP links this rule to its allow-list (which patterns are pre-approved and exempt from this rule)
5. ADM enables or disables the rule with an audit-logged reason
6. LP views which transactions triggered this rule in the past 30 days

**Primary display:** Rule card — name, family, description, detection logic (human-readable: "Fires when X exceeds Y at terminal Z"), threshold values, enabled state, last modified by / when. Alert history table (30 days). Allow-list summary (linked allow-list entries that suppress this rule).  
**Actions:** Enable/Disable with reason, Edit thresholds (if configurable), View allow-list, Export alert history  
**CP equivalent:** None  
**UX callout:** Detection logic must be human-readable — not a regex or a SQL predicate. LP investigators are not engineers. "Fires when a cashier voids more than 3 transactions in a single shift above $25" is what's needed, not the underlying query.

---

### `/chirps` — Chirp Feed

**Who:** LP, MGR  
**Entry points:** Primary nav, Alert detail → "View source chirp"

**Scenarios:**
1. LP monitors the real-time transaction feed from all stores
2. LP filters chirps by store to watch a specific location's activity
3. LP spots a pattern in the feed before a rule fires (pre-rule situational awareness)
4. LP filters by chirp type (sale, return, void, discount, end-of-day) to focus
5. LP drills into a specific chirp to see the full transaction detail
6. MGR confirms that transactions are flowing (system health check)

**Primary display:** Reverse-chronological feed — chirp type badge, store, terminal, cashier, amount, timestamp, item count. Filter by store, type, cashier, time window. Auto-refresh toggle. Pause for review.  
**Actions:** View chirp detail, Filter, Pause/resume live feed, Flag chirp for review  
**CP equivalent:** None — closest is the Z-Tape report run after close  
**UX callout:** The chirp feed is Canary's live window into the store. CP operators are blind until end of day. Canary operators see every transaction as it posts.

---

### `/chirps/:id` — Chirp Detail

**Who:** LP  
**Entry points:** Chirp feed row, Alert detail → transaction context

**Scenarios:**
1. LP reads the full parsed ticket: line items, quantities, prices, discounts, tender, cashier, terminal, timestamps
2. LP verifies the hash seal — confirms this chirp was not altered after ingestion
3. LP views the ARTS POSLog event representation of this ticket
4. LP checks for any rules that evaluated this transaction and their outcomes
5. LP links this chirp to an existing case as corroborating evidence
6. LP opens the customer profile linked to this transaction

**Primary display:** Transaction card (all fields from ticket), Hash seal status (verified / tampered indicator), ARTS event expand, Rules evaluated panel (list of rules that ran + pass/fail), Evidence link action, Customer card (if customer-linked).  
**Actions:** Link to case as evidence, Open customer profile, View full proof, Export transaction record  
**CP equivalent:** View Ticket History (`frmpstickethistory`) — read-only, no hash, no rule context  
**UX callout:** Hash seal status must be prominent and instant. If this ticket shows "tampered" — that is the alert. Counterpoint has no way to detect post-close ticket alteration.

---

### `/cases/hawk` — Case List (Hawk)

**Who:** LP, MGR  
**Entry points:** Primary nav, Alert detail → "Escalate to case"

**Scenarios:**
1. LP views their open investigation caseload
2. LP filters by case status (Open / Under Review / Pending / Closed)
3. LP filters by store to see all open cases for a location
4. LP sees case age (days open) to prioritize stale investigations
5. MGR reviews all cases across their stores
6. LP searches for a case by subject name, cashier, or ticket number

**Primary display:** Table — case ID, subject name, store, cashier, case type, status badge, days open, evidence count, assigned investigator. Filters: status, store, assignee, date range, case type. Sort by age.  
**Actions:** Open case, Create new case, Filter, Export case list  
**CP equivalent:** None  
**UX callout:** Days open as a visible field is non-negotiable. Stale investigations are a real operational problem — LP managers need to see them without running a report.

---

### `/cases/hawk/:id` — Case Detail (Hawk)

**Who:** LP, MGR  
**Entry points:** Case list, Alert detail → escalate, Evidence attach

**Scenarios:**
1. LP reads the full case narrative and understands what's under investigation
2. LP reviews the evidence timeline in chronological order (which alerts/chirps contributed)
3. LP verifies the hash-chained integrity of each evidence record
4. LP adds a case note documenting their findings at a specific point in the investigation
5. LP reviews the subject's full transaction history across all stores
6. LP identifies a corroborating transaction not yet in the evidence record and links it
7. LP changes case status (Open → Under Review → Pending → Closed)
8. LP requests manager review
9. MGR views the case, adds their note, approves closure
10. LP sees the cross-case pattern view for this subject (other cases involving same cashier or customer)

**Primary display:** Case header (ID, status, subject, store, assigned investigator, open date). Evidence timeline (chronological — each item shows: timestamp, type, amount, hash status, linked transaction). Case notes (threaded — actor + timestamp + note). Subject profile panel (right rail — summary of subject's alert history, transaction volume, risk score). Action bar.  
**Actions:** Add evidence, Add note, Change status, Request review, Link transaction, View subject patterns, Close case, Export case report  
**CP equivalent:** None  
**UX callout:** The evidence timeline with hash status per item is what makes this legally defensible. Every evidence record shows: ingested at (timestamp), hash (fingerprint), status (intact / tampered). A case that goes to HR or prosecution needs this audit chain. CP has nothing remotely close.

---

### `/cases/hawk/:id/evidence` — Evidence Attach

**Who:** LP  
**Entry points:** Case detail → "Add evidence"

**Scenarios:**
1. LP searches for a specific transaction by ticket number and adds it as evidence
2. LP searches for transactions by cashier + date range and reviews candidates before adding
3. LP attaches an external document (screenshot, camera image, PDF report) as evidence
4. LP adds a manual evidence record (verbal statement, physical observation) with free-text description
5. LP confirms the hash is computed and the record is sealed before submission

**Primary display:** Search panel (find transactions by ticket #, cashier, date, amount), transaction preview before attach, file upload zone, manual record form. Seal status shown after attach.  
**Actions:** Search transactions, Attach transaction, Upload file, Add manual record, Cancel  
**CP equivalent:** None  
**UX callout:** The hash is computed on attach — LP cannot edit evidence after sealing. This is the core integrity guarantee. Make the seal confirmation explicit: "This evidence record is now sealed and cannot be modified."

---

### `/cases/hawk/analytics` — Case Analytics

**Who:** LP, MGR  
**Entry points:** Cases nav → Analytics tab

**Scenarios:**
1. MGR reviews LP performance for the period: cases opened, closed, dollars recovered
2. MGR identifies which stores have the most open cases
3. MGR sees case closure rate by investigator
4. LP sees which rule families are generating the most cases
5. MGR tracks case age distribution (are cases being closed promptly?)
6. MGR reviews the estimated shrink dollar amount across all open cases

**Primary display:** Summary KPIs (cases open, cases closed this period, avg days to close, estimated dollars at risk). Chart: cases by store. Chart: cases by rule family. Table: investigator workload. Case age histogram.  
**Actions:** Filter by date range, Export report, Drill into a specific store's cases  
**CP equivalent:** None  
**UX callout:** Estimated dollars at risk is a calculated field — Canary computes this from the transaction amounts attached as evidence across all open cases. CP has no equivalent visibility.

---

### `/cases/hawk/patterns` — Cross-Case Pattern View

**Who:** LP  
**Entry points:** Case detail → "View subject patterns", Cases nav → Patterns tab

**Scenarios:**
1. LP identifies that the same cashier appears as subject in 4 separate open cases
2. LP sees a customer who is linked to 3 different cases across 2 stores
3. LP identifies that a specific terminal (not cashier) is generating disproportionate alert volume — suggesting hardware or configuration issue rather than individual misconduct
4. LP flags a pattern as a coordinated scheme (multiple subjects working together)
5. LP sees temporal patterns — alert clustering on specific days/shifts

**Primary display:** Subject graph — nodes are subjects (cashiers, customers, terminals), edges are cases linking them. Subject table — subject name/ID, type (cashier/customer/terminal), case count, total amount, stores involved. Temporal heatmap (alert density by day of week / hour).  
**Actions:** Open subject's full case list, Flag as coordinated scheme, Export pattern report  
**CP equivalent:** None  
**UX callout:** This is the needle-in-a-haystack screen. A cashier with 4 cases in 60 days across 2 stores is a signal no individual alert surface reveals. Counterpoint operators discover this only through manual review of paper Z-tapes.

---

### Allow-List Screens (`/settings/allowlist/*`)

Four screens — same pattern, different rule family. One entry per screen:

**Shared scenarios (all 4 allow-list screens):**
1. ADM views the current allow-list for this rule type
2. ADM adds a new allow-list entry (e.g., "Cashier J. Smith is pre-authorized for unlimited voids on Saturdays due to training role")
3. ADM edits the scope of an existing entry (extend date range, narrow to specific store)
4. ADM deactivates an entry that is no longer valid
5. LP searches for a specific allow-list entry when investigating an alert that was suppressed
6. LP requests ADM to add an entry for a pattern they've confirmed as legitimate

**CP equivalent (all 4):** None — Counterpoint's security codes can restrict POS functions but cannot create pre-approved exception patterns that suppress alert-generation logic.

| Screen | Allow-list type | Key field |
|---|---|---|
| `/settings/allowlist/dead-count` | Pre-approved cashier/store pairs with known-good dead-count patterns | Store, cashier, threshold override |
| `/settings/allowlist/discounts` | Pre-approved discount patterns by reason code + amount | Reason code, max %, store, cashier, date range |
| `/settings/allowlist/voids` | Authorized admin-void reason codes | Reason code, authorized cashier role, max per shift |
| `/settings/allowlist/comps` | Authorized comp reason codes | Reason code, authorized role, max dollar per ticket |

**UX callout (all 4):** Counterpoint security codes control what operators *can* do. Canary allow-lists control what Canary *won't alert on*. These are complementary, not redundant. The allow-list is Canary's institutional memory of "we know about this pattern; it's fine."

---

### `/settings/training-mode` — Training Mode Toggle

**Who:** ADM, MGR  
**Entry points:** Settings nav → Training Mode

**Scenarios:**
1. MGR enables training mode for a specific store before a new cashier onboarding week (suppresses LP alerts that would fire on trainee behavior)
2. MGR sets a training mode end date (auto-disables after the training period)
3. ADM reviews which stores are currently in training mode
4. MGR disables training mode early when training is complete

**Primary display:** Store list with training mode toggle per store + start date + end date + who enabled it.  
**Actions:** Enable/disable per store, Set end date, View history  
**CP equivalent:** None — CP has no mechanism to suppress LP-style detection during training  
**UX callout:** Training mode is a safety valve. Without it, a new cashier's first week generates hundreds of false-positive alerts and destroys investigator trust in the system. CP operators had no option but to ignore all alerts during training — Canary makes this precise and audited.

---

### Customer Investigator Screens (`/customers/*`)

---

### `/customers` — Customer Lookup (Investigator)

**Who:** LP  
**Entry points:** Primary nav, Alert detail → customer link, Case detail → subject search

**Scenarios:**
1. LP searches for a customer by name, email, phone, or loyalty number
2. LP finds a customer linked to a suspicious transaction before opening the full profile
3. LP reviews the customer's risk score before investigating
4. LP identifies customers with multiple open cases
5. LP filters customers by risk band (High / Medium / Low / None)

**Primary display:** Search bar (name, email, phone, loyalty #). Results table — name, loyalty #, risk score badge, case count, last transaction, store. Risk band filter.  
**Actions:** Search, View customer detail  
**CP equivalent:** `frmcustomers` — full form but no risk score, no case context  
**UX callout:** The investigator view of a customer is fundamentally different from the operator view. The investigator needs risk score and case history in the search results — not address and terms codes.

---

### `/customers/:id` — Customer Detail

**Who:** LP, MGR  
**Entry points:** Customer lookup, Alert detail

**Scenarios:**
1. LP reviews the customer's purchase history to identify patterns (frequent returns, specific item affinity, store affinity)
2. LP checks the customer's loyalty point balance and transaction history
3. LP views the customer's address and contact information
4. LP sees total lifetime spend, average transaction size, return rate
5. MGR reviews a high-value customer's account status before a sensitive interaction
6. LP checks if this customer has been a subject in prior cases

**Primary display:** Customer card (name, contact, loyalty number, status). KPI row (lifetime spend, avg ticket, return rate, loyalty balance). Transaction history table (filterable by store, date, amount). Cases tab (cases where this customer is a subject). Loyalty tab (balance, earning history, redemption history).  
**Actions:** View transaction, Open case, Link to existing case, Export customer report  
**CP equivalent:** `frmcustomers` A/R Documents tab + Ticket History tab — two separate tabs with no analytics overlay  
**UX callout:** Canary surfaces the investigator-relevant analytics (return rate, store affinity, risk indicators) that CP buries across multiple tabs. The investigator should not have to navigate 4 tabs to build their mental model of a customer.

---

### `/customers/:id/risk` — Customer Risk Score

**Who:** LP  
**Entry points:** Customer detail → Risk tab

**Scenarios:**
1. LP reads the customer's current risk score and the factors driving it
2. LP understands which specific transactions contributed most to the score
3. LP sees risk score trend over time (is this customer escalating or normalizing?)
4. LP identifies whether the risk score is driven by return volume, discount patterns, or cross-case involvement
5. LP manually overrides the risk score with a documented reason (e.g., known-good VIP customer who returns frequently as a matter of preference)

**Primary display:** Risk score gauge (0–100). Contributing factors breakdown (return rate weight, discount pattern weight, case involvement weight, velocity weight). Transaction evidence list (top contributing transactions). Score history sparkline (30/60/90 days). Override section (manual score override with reason and expiry).  
**Actions:** View contributing transaction, Manual score override, Export risk report  
**CP equivalent:** None  
**UX callout:** The score decomposition (why is this score 73?) is more important than the score itself. An investigator who can't explain the score to a manager can't act on it.

---

### `/customers/:id/context` — Customer Cross-Module Context

**Who:** LP  
**Entry points:** Customer detail → Context tab

**Scenarios:**
1. LP confirms this customer has never appeared as a subject in any case (innocence check before clearing an alert)
2. LP identifies that this customer appears in 3 open cases across 2 stores
3. LP sees which transactions involving this customer have been attached as case evidence
4. LP views co-occurrence: which cashiers have processed this customer's transactions most frequently (collusion signal)

**Primary display:** Summary panel (cases as subject: N, transactions as evidence: M, stores transacted at: K). Case list (cases where this customer appears). Evidence appearances list. Cashier co-occurrence table (which cashiers handled this customer's transactions most + alert overlap).  
**Actions:** Open case, View transaction, Flag co-occurrence pattern  
**CP equivalent:** None  
**UX callout:** Cashier co-occurrence (this customer + this cashier appear together disproportionately) is a collusion detection signal that no existing retail LP system surfaces automatically. This screen makes it visible.

---

### N.4 LP Substrate Config Screens

Four screens — same pattern. See allow-list screens for scenario template. These configure the thresholds that LP rules evaluate against.

| Screen | What it configures | Rule it feeds |
|---|---|---|
| `/settings/store/drawer` | Max drawer cash variance before alert | Q-DC-01 |
| `/settings/store/discounts` | Max discount % per reason code per store | Q-DR-01 |
| `/settings/store/void-reasons` | Valid void reason code list | Q-VO-01 |
| `/settings/store/comp-reasons` | Valid comp reason code list | Q-CO-01 |

**Shared scenario pattern:**
1. ADM sets the drawer cash variance threshold for each store (different stores may have different cash volume norms)
2. ADM configures store-specific discount caps (a flagship store may allow higher manager discounts)
3. MGR reviews current threshold settings before enabling LP monitoring
4. ADM adjusts thresholds based on LP review findings (e.g., threshold was too tight, generating excessive false positives)

**CP equivalent:** `frmpscontrol` (POS Control) — CP has configuration for these values but stores them in a monolithic 200-field form with no connection to any alert logic.  
**UX callout:** CP's POS Control form is unusable for non-technical users. These 4 Canary screens each have ONE purpose. ADM sets the value, sees what rule it feeds, and understands immediately what changes.

---

## Wave 2 — Store Ops Visibility

---

### `/transactions` — Transaction List

**Who:** LP, MGR  
**Entry points:** Primary nav, Chirp feed → "View in transactions", Alert detail

**Scenarios:**
1. MGR reviews all transactions from a store for a specific date
2. LP filters by cashier to pull all transactions for an investigative subject
3. LP filters by transaction type (sale / return / void / layaway) to find anomalies
4. LP searches for a specific ticket number
5. MGR audits end-of-day by reviewing high-value transactions
6. LP exports filtered transaction set for offline analysis

**Primary display:** Table — ticket #, type badge, store, terminal, cashier, customer (if linked), item count, subtotal, discount total, tax, total, tender type, timestamp. Filters: store, date range, type, cashier, terminal, amount range, has-discount flag. Sort any column.  
**Actions:** View detail, Filter, Export, Link to case  
**CP equivalent:** View Ticket History (`frmpstickethistory`) — similar but no hash status, no case-link, no discount filter  
**UX callout:** The "has-discount flag" filter doesn't exist in CP. It's one click to get all discounted transactions for a cashier on a date — in CP this requires running a Price Exceptions report.

---

### `/transactions/:id` — Transaction Detail

**Who:** LP, MGR  
**Entry points:** Transaction list row, Chirp detail, Alert detail

**Scenarios:**
1. LP reads the full ticket: every line item, quantity, price, discount applied, tender type, cashier, terminal, timestamps
2. LP verifies the hash-before-parse seal (was this ticket altered after ingestion?)
3. LP reviews all discount events on this ticket (what discounts were applied, by which reason code)
4. LP identifies which detection rules evaluated this transaction and their outcomes
5. LP links this transaction to a case as evidence
6. MGR reprints / exports this transaction record as PDF
7. LP views the customer's profile linked to this transaction

**Primary display:** Header (ticket #, store, terminal, cashier, date/time, status). Line items table (item #, description, qty, unit price, discount amount, reason code, extended price). Tender section (tender type, amount per tender, change). Summary (subtotal, total discounts, tax, total). Hash seal panel (hash value, verified status, ingested timestamp). Rules evaluated panel. Customer card (if linked).  
**Actions:** Link to case, View audit proof, View customer, Export PDF, View cashier profile  
**CP equivalent:** View Ticket History detail — no hash, no rule overlay, no case link  
**UX callout:** The hash seal + rules evaluated panels transform a passive receipt view into an active investigative tool. Every transaction becomes a piece of potential evidence, not just a record.

---

### `/transactions/:id/proof` — Audit Proof Verification

**Who:** LP, ADM, external auditor  
**Entry points:** Transaction detail → "View audit proof"

**Scenarios:**
1. LP generates a verifiable audit proof showing this transaction was not altered after close
2. LP exports the audit proof as a PDF for HR/legal proceedings
3. ADM demonstrates Canary's integrity model to an auditor (SOC 2, loss prevention audit)
4. LP verifies a specific transaction's inclusion in the Merkle tree (cryptographic proof of inclusion)

**Primary display:** Transaction hash (SHA-256). Merkle path (proof of inclusion in the audit tree). Anchor record (blockchain hash if S4-anchored). Verification status (all green / tamper detected). Exportable proof certificate.  
**Actions:** Verify proof (re-run on demand), Export proof certificate (PDF), Copy hash  
**CP equivalent:** None  
**UX callout:** This screen will rarely be used in daily operations — and that's fine. When it IS needed (HR hearing, police report, insurance claim), it is irreplaceable. Counterpoint operators have nothing to show. Canary operators show a cryptographic proof certificate.

---

### `/transfers` — Transfer List

**Who:** MGR, RCV  
**Entry points:** Primary nav, Inventory section

**Scenarios:**
1. MGR reviews all open (in-transit) transfers between stores
2. MGR identifies transfers that are overdue (shipped but not received within expected window)
3. RCV finds a specific inbound transfer to process the receipt
4. MGR reviews completed transfers and their variance outcomes
5. LP filters transfers by variance status (any shrink detected in transit?)

**Primary display:** Table — transfer ID, from store, to store, item count, initiated date, expected receipt date, status (Initiated / In Transit / Received / Variance-Flagged). Filters: status, store, date range, overdue-only toggle.  
**Actions:** View detail, New transfer (NEW), Filter  
**CP equivalent:** Transfer Out / Transfer In (two separate screens in CP — no unified view)  
**UX callout:** CP has no single view of all in-transit transfers. Operators run Transfer Out on one machine and Transfer In on another with no visibility of what's in flight. Canary's unified list is a material operational improvement.

---

### `/transfers/new` — Transfer Initiation (NEW — not in original wave plan)

**Who:** MGR  
**Entry points:** Transfer list → New Transfer button

**Scenarios:**
1. MGR initiates a transfer of slow-moving items from Store A to Store B where they're selling faster
2. MGR creates an emergency transfer of a specific item to cover a stockout at another location
3. MGR selects items for transfer by scanning barcodes or searching item catalog
4. MGR specifies quantities per item (up to on-hand at source location)
5. MGR adds transfer notes (reason, expected delivery date)
6. MGR reviews and confirms — transfer status becomes "Initiated" and receiving store is notified

**Primary display:** Store selector (from → to). Item search + add lines (item #, description, on-hand at source, transfer qty). Transfer notes. Summary panel (total units, estimated cost).  
**Actions:** Add item, Remove item, Confirm transfer, Save draft  
**CP equivalent:** Transfer Out entry (`frmimtransferout`) — Windows-only, no cross-location on-hand visibility during entry  
**UX callout:** CP's Transfer Out form requires the user to know the on-hand quantity before entering — no inline lookup. Canary shows on-hand at source location on every line. Major usability win.

---

### `/transfers/:id` — Transfer Detail

**Who:** MGR, RCV  
**Entry points:** Transfer list

**Scenarios:**
1. MGR reviews what items are included in this transfer and their quantities
2. RCV uses this screen as the picking list to pull items for shipment
3. MGR adds a note about an item that couldn't be fully fulfilled (partial transfer)
4. RCV confirms shipment (status → In Transit, auto-notifies destination store)

**Primary display:** Transfer header (from/to store, dates, status). Line items (item #, description, qty requested, qty to ship — editable). Notes. Action bar.  
**Actions:** Edit quantities, Confirm shipment, Add note, Print picking list  
**CP equivalent:** Transfer Out detail — no partial-fulfillment notation, no receiving-store notification  

---

### `/transfers/:id/receive` — Transfer Receipt (NEW — not in original wave plan)

**Who:** RCV, MGR  
**Entry points:** Transfer detail → "Receive this transfer" (destination store)

**Scenarios:**
1. RCV receives a transfer by scanning each item and confirming quantities
2. RCV identifies a discrepancy (shipped 24, received 22 — 2 units missing)
3. RCV records damaged goods (received but not saleable)
4. RCV confirms receipt — perpetual ledger updates immediately, inventory position at destination increases
5. System auto-creates a variance record if received qty ≠ shipped qty
6. LP is notified if variance exceeds threshold (transfer shrink alert)

**Primary display:** Transfer header (from store, items expected). Line items (item, expected qty, received qty field — editable, variance indicator). Damage notation field. Receipt confirmation button.  
**Actions:** Enter received quantities, Note damages, Confirm receipt, Flag for LP review  
**CP equivalent:** Transfer In entry (`frmimtransferin`) — Windows-only, no auto-alert on variance  
**UX callout:** In CP, a variance discovered at receiving requires the operator to manually note it somewhere (often paper) and send a message to LP. In Canary, the variance auto-triggers the LP alert. The receiving clerk's form is also the evidence creation point.

---

### `/transfers/:id/variance` — Transfer Variance Review

**Who:** LP, MGR  
**Entry points:** Transfer list (variance-flagged row), LP alert → link

**Scenarios:**
1. LP reviews the variance: what was shipped vs what was received, which items are short
2. LP determines disposition: legitimate damage / carrier loss / internal shrink
3. LP links this variance to an existing case or opens a new one
4. MGR approves variance write-off (within their authorized threshold)
5. LP notes the pattern: this is the third transfer from Store X with short counts

**Primary display:** Transfer header. Variance table (item, shipped, received, variance qty, variance value, disposition selector). Pattern flag (has this store pair had variances before?). Case link section.  
**Actions:** Set disposition (damage/loss/shrink), Link to case, Request approval, Approve write-off  
**CP equivalent:** No equivalent — variance resolution is entirely manual in CP  

---

### `/inventory/count/new` — Physical Count Create (NEW)

**Who:** MGR, ADM  
**Entry points:** Inventory nav → Physical Count → New Count

**Scenarios:**
1. MGR schedules a full store count (all items, all locations)
2. MGR schedules a cycle count for a specific department/category (e.g., "electronics only")
3. MGR schedules a count for a specific storage location (e.g., "Warehouse B")
4. ADM configures whether the count locks inventory movement during counting (blind count vs non-blind)
5. MGR assigns count sessions to specific employees (who counts what section)

**Primary display:** Count type selector (Full store / Category / Location). Item filter (if category/location). Date selector (count date for GL posting). Blind count toggle (hide current on-hand from counters). Assign counters (user list, assign to sections). Confirm.  
**Actions:** Configure and create count, Save draft  
**CP equivalent:** `frmimphyscountcreate` — Windows-only, no mobile assignment, no section-based assignment  
**UX callout:** CP's physical count requires printing paper worksheets and distributing them. Canary creates a count session that opens on each counter's mobile device. Eliminates paper entirely.

---

### `/inventory/count/:id` — Physical Count Entry

**Who:** EMP (counter), MGR  
**Entry points:** Physical Count list, assigned session notification

**Scenarios:**
1. Counter scans item barcode, sees item name, enters count quantity
2. Counter flags a damaged item (can count but note condition)
3. Counter moves to next item (keyboard/button flow — high velocity data entry)
4. Counter completes their section and marks it done
5. MGR monitors count progress in real-time (what % of items counted)
6. MGR sees which sections are complete and which are in progress
7. MGR identifies items with no count entered (counter may have missed them)
8. Counter rescans an item to update a previously entered count

**Primary display (counter — mobile optimized):** Large scan zone, item name + image, current count entry field (large tap target), previous count (if non-blind), confirm button. Navigation: previous/next item. Progress indicator.  
**Primary display (manager — portal):** Count progress dashboard — % complete by section, items counted vs total, counter-by-counter progress, flag items with no entry.  
**Actions (counter):** Scan / search item, Enter quantity, Flag damage, Mark section complete  
**Actions (manager):** Monitor progress, Assign uncounted items, View real-time discrepancies  
**CP equivalent:** `frmimphyscountenter` — Windows desktop, no mobile, no real-time progress view  
**UX callout:** The manager view showing real-time count progress doesn't exist in CP at all. Managers currently have no idea how the count is going until it's done. Canary makes this live.

---

### `/inventory/count/:id/post` — Physical Count Post

**Who:** MGR  
**Entry points:** Physical Count detail → "Post Count"

**Scenarios:**
1. MGR reviews count results before posting: which items have variances vs current on-hand
2. MGR identifies high-variance items and decides whether to recount before posting
3. MGR reviews the total inventory shrink dollar amount this count will recognize
4. MGR posts the count — on-hand quantities update, GL adjustment generated
5. System auto-creates LP alerts for high-variance items (possible theft)

**Primary display:** Variance summary (items over, items under, total variance units, total variance value). Variance table (item, on-hand before, counted, variance, value). High-variance flag (items > threshold get a review flag). GL distribution preview (debit shrinkage expense, credit inventory). Post button.  
**Actions:** Review variance, Flag for recount, Post count, Export variance report  
**CP equivalent:** Physical count post in `frmimphyscountenter` — posts but no LP integration, no recount flag  
**UX callout:** The LP integration at post time (auto-alert on high-variance items) is unique to Canary. In CP, a manager reviews the physical count journal and manually tells LP about variances — days later. Canary makes this instantaneous.

---

### `/inventory/adjustments/new` — Inventory Adjustment Create (NEW)

**Who:** MGR  
**Entry points:** Inventory nav → Adjustments → New Adjustment

**Scenarios:**
1. MGR records a damaged item write-off (broke in storage — remove from inventory)
2. MGR corrects a receiving error (received 12 but entered 10 — add 2 units)
3. MGR adjusts for a vendor short-ship discovered after receiving is closed
4. MGR records a sample or gift (item given away at no charge — remove from inventory)
5. Adjustment is logged with reason code, GL account, and user for audit

**Primary display:** Item search, quantity (+ or −), reason code selector, notes, GL account override (for non-standard adjustments). Save → auto-posts immediately with audit entry.  
**Actions:** Add adjustment lines, Select reason code, Post, Cancel  
**CP equivalent:** `frmimadjustmentsenter` — Windows only  
**UX callout:** Same functionality, web-native. The audit log on every adjustment (who, when, why) is automatic in Canary and manual (paper) in CP.

---

### `/items` — Item Catalog Search

**Who:** LP, MGR, BYR  
**Entry points:** Primary nav (Inventory section), Alert detail → item link

**Scenarios:**
1. LP searches for an item involved in a suspicious transaction
2. MGR looks up an item's current on-hand position across all stores
3. BYR searches for items in a specific category to review performance
4. MGR checks an item's current regular price and any active special prices
5. LP views an item's return rate and discount rate (shrink signal)

**Primary display:** Search bar (item #, description, barcode scan). Results table — item #, description, category, on-hand (total), on-hand by location (expand), regular price, return rate %, last received date.  
**Actions:** View item detail, Filter by category, Export  
**CP equivalent:** `frmitems` — Windows, no cross-location on-hand at a glance, no return rate  
**UX callout:** Cross-location on-hand summary in search results doesn't exist in CP. Buyers need to open each item record and navigate to inventory tab to see locations. Canary puts it in the search results row.

---

### `/items/:id` — Item Detail

**Who:** LP, MGR, BYR  
**Entry points:** Item search

**Scenarios:**
1. BYR reviews an item's complete attribute set (category, vendor, unit, barcodes)
2. MGR reviews on-hand at each location and identifies which stores are overstocked
3. BYR views the item's committed inventory (reserved by open orders vs truly available)
4. LP checks an item's return rate and discount rate as a shrinkage signal
5. BYR views the item's sales velocity (units/week) and GMROI
6. BYR views the item's full price history (when was price last changed and by whom)
7. MGR checks for any active special prices, promotions, or contract prices on this item

**Primary display:** Item card (image, description, attributes, category, vendor, status). Inventory panel (on-hand by location, committed qty, available qty). Performance KPIs (sell-through, return rate, discount rate, GMROI). Price panel (regular price, active specials/promotions). Sales chart (units/week, 90 days). Tabs: Pricing, Inventory by Location, Sales History, Related Alerts.  
**Actions:** View alert, Edit item (new), Add adjustment (new), View in receiving  
**CP equivalent:** `frmitems` — similar data but no performance KPIs, no cross-location committed view, no alert overlay  
**UX callout:** Committed inventory (on-hand minus reserved by orders/layaways = truly available) is a key field buyers need. CP shows raw on-hand; Canary shows available. Major merchandising decision quality improvement.

---

## Wave 3 — Finance + Receiving

---

### `/vendors` — Vendor List (NEW)

**Who:** BYR, ADM  
**Entry points:** Purchasing nav section

**Scenarios:**
1. BYR finds a vendor to place a new PO
2. BYR reviews a vendor's recent delivery performance (on-time %, short-ship rate)
3. BYR identifies vendors with open RTVs
4. ADM manages vendor master data (add, update, deactivate)

**Primary display:** Table — vendor name, vendor #, category, primary contact, open POs, pending RTVs, last receiving date, on-time delivery %. Search bar. Filter by category.  
**Actions:** View vendor, New vendor, Filter  
**CP equivalent:** Vendor maintenance form — no delivery performance metrics  
**UX callout:** Delivery performance (on-time %, short-ship rate) calculated from receiving history. CP has no vendor scorecarding. Buyers currently have no data-driven way to evaluate vendors.

---

### `/vendors/:id` — Vendor Detail

**Who:** BYR  
**Entry points:** Vendor list

**Scenarios:**
1. BYR reviews vendor contact, terms, and ship-via preferences
2. BYR reviews this vendor's item catalog (all items sourced from this vendor)
3. BYR reviews open POs for this vendor
4. BYR reviews receiving history (last 12 months: orders placed, received on time, shorted)
5. BYR reviews outstanding RTVs against this vendor
6. BYR updates vendor contact information or terms

**Primary display:** Vendor card (contact, terms, ship-via, categories). Performance scorecards (on-time %, fill rate, short-ship rate, avg lead time). Tabs: Items, Open POs, Receiving History, RTVs, Notes.  
**Actions:** Edit vendor, New PO for this vendor, New RTV  
**CP equivalent:** `frmvendors` — no performance metrics, no integrated PO/RTV history  

---

### `/orders/new` — Purchase Order Create (NEW)

**Who:** BYR  
**Entry points:** Vendors → vendor → New PO, Suggested Orders → Approve and create PO

**Scenarios:**
1. BYR creates a PO for a specific vendor by manually adding line items
2. BYR approves a suggested order and converts it directly to a PO (single click)
3. BYR modifies quantities on a suggested order before converting to PO
4. BYR adds freight/handling charges to the PO
5. BYR sets delivery date and ship-via instructions
6. BYR reviews the PO total and confirms

**Primary display:** Vendor selector (or pre-filled from suggested order). Header (order date, delivery date, ship-to, ship-via, terms, buyer). Lines (item search + add, qty, unit cost, extended). Misc charges (freight, handling). Summary (total units, total cost). Notes.  
**Actions:** Add line, Remove line, Save draft, Submit PO, Print/export PO  
**CP equivalent:** `frmpopreqenter` — Windows, same concept  
**UX callout:** The "Convert suggested order to PO" flow is the key UX win. In CP, the buyer runs a Purchasing Advice report, prints it, then manually keys a new PO. In Canary: Suggested Orders → select → Approve → PO created, pre-filled.

---

### `/orders/suggested` — Suggested Orders List

**Who:** BYR  
**Entry points:** Purchasing nav

**Scenarios:**
1. BYR reviews items that have dropped below minimum on-hand
2. BYR reviews items where Days of Supply has fallen below the target (e.g., < 14 days)
3. BYR adjusts the suggested quantity before approving (demand is higher than algorithm suggests)
4. BYR defers a suggestion (item is being discontinued — do not reorder)
5. BYR groups multiple suggestions for the same vendor and converts them to a single PO
6. BYR filters by vendor to work one vendor's replenishment at a time

**Primary display:** Table — item, vendor, current on-hand, min on-hand, days of supply, suggested qty, suggested cost, urgency indicator (overdue / urgent / normal). Filter by vendor, urgency, category. Group by vendor toggle (for combined PO creation).  
**Actions:** Approve (single), Approve + create PO, Defer, Adjust qty, Group and create PO  
**CP equivalent:** Purchasing Advice report (printed/viewed, then manually keyed) — no interactive approval  
**UX callout:** This is a fundamental workflow redesign. CP: run report → read printout → key PO → post. Canary: review queue → approve → PO created. Eliminates the manual re-keying step entirely.

---

### `/receiving` — Receiving Sessions List

**Who:** RCV, MGR  
**Entry points:** Purchasing nav

**Scenarios:**
1. RCV sees today's expected deliveries (POs with delivery date = today)
2. RCV opens a receiving session for an arriving delivery
3. MGR reviews receiving sessions from the past week (what came in, what was short)
4. RCV identifies a delivery arriving without a PO (blind receiving needed)
5. MGR reviews which POs are overdue (delivery date passed, not yet received)

**Primary display:** Table — receiving session ID, vendor, linked PO #, expected qty, received qty, status (Open / In Progress / Closed / Vouchered), delivery date. Filter: status, vendor, date range, overdue-only. "New receiving" button. "Blind receiving" button.  
**Actions:** Open session, New session (with PO), Blind receiving (without PO), Filter  
**CP equivalent:** `frmporeceivingsenter` (list view) — Windows-only  

---

### `/receiving/:id` — Receiving Session — Line Entry

**Who:** RCV  
**Entry points:** Receiving sessions list

**Scenarios:**
1. RCV scans each item barcode and enters received quantity (one line at a time)
2. RCV identifies a line that was short-shipped and enters the actual quantity received (< expected)
3. RCV notes damaged goods on a specific line (received but not saleable)
4. RCV identifies an item on the delivery that wasn't on the PO (overage or substitution)
5. RCV adds a misc charge (freight invoice from carrier differs from PO estimate)
6. RCV saves progress and resumes later (partial receiving session)

**Primary display:** Session header (vendor, PO #, delivery date). Lines table (item #, description, expected qty, received qty — editable, variance indicator, damage flag, notes per line). Misc charges section. Progress (lines confirmed vs total). Save + resume.  
**Actions:** Enter received qty, Flag damage, Add unplanned line, Add misc charge, Save, Close session  
**CP equivalent:** `frmporeceivingsenter` line entry — same concept, Windows-only  
**UX callout:** Barcode scan on mobile vs keyboard entry on Windows desktop. Receiving clerks work in the receiving dock, not at a PC. Canary's mobile-web session is usable where CP's isn't.

---

### `/receiving/:id/close` — Receiving Close + Post

**Who:** MGR, RCV  
**Entry points:** Receiving session detail → "Close Session"

**Scenarios:**
1. MGR reviews the full receiving session before posting (expected vs received)
2. MGR sees total cost of this receiving, including freight adjustments
3. MGR decides whether to voucher this receiving (approve for A/P processing)
4. MGR posts — inventory increases, cost posts to perpetual ledger
5. System auto-prints receiving labels (if configured)
6. System notifies LP if variance exceeds threshold

**Primary display:** Session summary (vendor, PO #, total lines, total units expected vs received, total cost). Variance summary (shorted items, value). Voucher action (voucher now vs leave open). Post button.  
**Actions:** Voucher, Post, Print labels, Cancel  
**CP equivalent:** Receiving close and voucher — same concept  

---

### `/returns/:id` — RTV Detail

**Who:** BYR, RCV  
**Entry points:** Returns list

**Scenarios:**
1. BYR creates an RTV for defective merchandise to return to vendor
2. RCV confirms quantities being shipped back to vendor
3. BYR records the vendor's credit memo number when received
4. BYR reconciles the credit (vendor credit applied against future PO or requested as cash)
5. MGR reviews all pending RTVs to understand vendor credit exposure

**Primary display:** RTV header (vendor, return date, reason). Lines (item, qty returning, cost, extended). Credit section (credit memo #, credit amount, reconciled status). Notes.  
**Actions:** Confirm quantities, Record credit memo, Reconcile credit, Print RTV form  
**CP equivalent:** RTV entry form — Windows-only  

---

### Finance Report Screens

Three screens per wave plan. Scenarios follow the same pattern:
- MGR selects period (day / week / period / YTD)
- MGR compares to prior period
- MGR exports report for accounting
- LP uses financial data to contextualize LP findings

| Screen | Primary metric | Key comparison |
|---|---|---|
| `/reports/finance` | Revenue, COGS, gross margin, shrink cost | vs prior period, vs budget |
| `/reports/payments` | Tender mix (cash/card/gift card/SVC), refund rate by tender | vs prior period |
| `/reports/tax` | Tax collected by authority, by rate | vs prior period |
| `/reports/eod` (NEW) | Daily totals, settlement, variance vs plan | vs yesterday, vs same day prior week |

**CP equivalent:** CP has Crystal Reports equivalents for finance and tax. EOD is from X/Z-Tape. None have prior-period comparison built in.  
**UX callout:** Prior-period comparison inline (not a separate report run) is the primary improvement over CP.

---

## Wave 4 — Merchandising + Labor

---

### `/timecards` — Timecard Editor (NEW)

**Who:** MGR  
**Entry points:** Employees nav → Timecards tab

**Scenarios:**
1. MGR reviews the week's timecard entries for their store
2. MGR corrects a missed clock-out (employee forgot to clock out — manager enters actual end time)
3. MGR approves the week's timecards before payroll export
4. MGR sees total hours per employee for the period
5. MGR identifies employees who clocked in late or worked overtime
6. LP flags a timecard anomaly: employee clocked in but no transactions on their cashier ID for that shift

**Primary display:** Calendar week view — employee rows, day columns, time entries shown per cell (clock-in / clock-out / total hours). Edit cell inline. Approve toggle per employee. Overtime flag (hours > threshold).  
**Actions:** Edit entry, Approve, Export (payroll), Flag anomaly  
**CP equivalent:** `frmsytimecardsenter` — Windows-only  
**UX callout:** The LP cross-reference (employee clocked in but no transactions on their terminal) doesn't exist in CP. Canary connects timecards to transaction data — a ghost shift (clocked in, sold nothing) is an anomaly Canary surfaces automatically.

---

### `/timeclock` — Mobile Clock-In (NEW)

**Who:** EMP  
**Entry points:** Direct URL, shared tablet in break room, QR code

**Scenarios:**
1. Employee clocks in at start of shift (tap ID, confirm, done)
2. Employee clocks out at end of shift
3. Employee takes a break (clock out for break, clock in return)
4. Employee sees their own hours for the current pay period
5. Manager PIN override for correction at the clock station

**Primary display (mobile-optimized):** Employee ID entry (or scan), clock-in / clock-out buttons, current shift duration, current pay period total hours. That's it — nothing else on this screen.  
**Actions:** Clock in, Clock out, Break in/out  
**CP equivalent:** Windows time clock station (dedicated hardware)  
**UX callout:** No dedicated hardware required. Any phone, tablet, or shared browser acts as the clock. Eliminates $1,500+ hardware cost per store for a clock-in workstation.

---

### `/timecards/export` — Payroll Export (NEW)

**Who:** MGR, ADM  
**Entry points:** Timecards screen → Export

**Scenarios:**
1. MGR exports approved timecards for the pay period as a CSV for payroll processing
2. ADM configures the export format (which payroll system — ADP, Paychex, manual)
3. MGR reviews totals before export (regular hours, overtime hours, per employee)
4. MGR exports and confirms successful transmission

**Primary display:** Pay period selector, employee filter, export format selector, totals preview (regular, OT, total per employee), export button.  
**Actions:** Select period, Select format, Export  
**CP equivalent:** Timecard export (CSV) — Windows-only, single format  

---

### `/settings/loyalty/programs` — Loyalty Program Config (NEW)

**Who:** ADM, MGR  
**Entry points:** Settings → Loyalty

**Scenarios:**
1. ADM creates a new loyalty program with a name and enrollment rules
2. ADM configures earning rules (e.g., "1 point per $1 spent; 2x points on Fridays")
3. ADM configures redemption rules (e.g., "100 points = $1 off; eligible on any item > $5")
4. ADM previews how a $50 transaction earns points under the configured rules
5. ADM activates or deactivates a loyalty program
6. MGR sees how many customers are enrolled in each program

**Primary display:** Program list (name, status, enrolled customer count). Program detail: earning rules builder (per dollar / per unit, multiplier by day/category), redemption rules builder (value per point, eligible items), live preview (enter transaction amount → see points earned → see redemption value).  
**Actions:** Create program, Edit rules, Preview, Activate/deactivate  
**CP equivalent:** Loyalty program setup across 3 separate screens in CP — earning rules in one, redemption in another, enrollment conditions in a third. No preview.  
**UX callout:** The live preview is the key win. Operators can see "if a customer spends $50 on a Friday, they earn 100 points, worth $1" before activating. In CP, this requires running a test transaction and reviewing the output.

---

### `/customers/:id/loyalty` — Customer Loyalty Tab (NEW)

**Who:** MGR  
**Entry points:** Customer detail → Loyalty tab

**Scenarios:**
1. MGR checks a customer's current point balance
2. MGR reviews point earning history (transactions that earned points)
3. MGR reviews point redemption history (when points were spent)
4. MGR manually adjusts points (add points for a service recovery, deduct for a return)
5. MGR enrolls a customer in a loyalty program
6. MGR unenrolls a customer from a program (customer request)

**Primary display:** Program enrollment badges. Point balance per program. Earning history table (date, transaction, points earned). Redemption history table. Manual adjustment form (add/deduct, reason, amount).  
**Actions:** Enroll, Unenroll, Add points, Deduct points  
**CP equivalent:** `frmarloyptsadjustmentsenter` + customer loyalty enrollment (two separate screens in CP)  

---

### `/settings/pricing/rules` — Price Rules Management (NEW)

**Who:** BYR, ADM  
**Entry points:** Settings → Pricing → Rules

**Scenarios:**
1. BYR creates a BOGO rule ("Buy 1 Get 1 50% off on all items in category X")
2. BYR creates a mix-and-match rule ("Any 3 items from Group A for $10")
3. BYR sets a start and end date for a rule
4. BYR previews how a rule applies to a sample basket
5. ADM activates or deactivates a rule
6. BYR reviews all active rules to check for conflicts (two rules applying to same items)

**Primary display:** Rule list (name, type, status, date range, affected items/categories). Rule builder: type selector (BOGO / twofer / mix-and-match / volume), conditions (which items, which qty threshold), pricing outcome (what price results). Date range. Store scope. Preview panel (enter a sample basket, see rule applied).  
**Actions:** Create rule, Edit rule, Activate/deactivate, Preview  
**CP equivalent:** `frmimmixmatchcodes` + `frmimplannedpromotions` (Rules tab) — two separate forms, no preview  
**UX callout:** Canary's rule builder consolidates all rule types (BOGO, twofer, mix-and-match) into one unified form with a preview. CP has these scattered across different forms with no unified preview capability.

---

### Merchandising Analytics Screens

| Screen | Who | Primary scenario | CP equivalent |
|---|---|---|---|
| `/reports/range` | BYR | BYR reviews sell-through, turn, GMROI by category for range planning decisions | Crystal Reports — Merchandise Analysis |
| `/promotions` | BYR, MGR | BYR views promotion calendar (what's running, when) + edits upcoming promotions | `frmimplannedpromotions` — Windows-only |
| `/reports/pricing` | BYR | BYR sees item price vs competitive market (if competitive data feed connected) | None in CP |
| `/reports/price-history` | BYR, LP | BYR / LP audits all price changes: what changed, from what to what, who changed it, when | None in CP — no price change audit |
| `/reports/markdowns` | BYR | BYR reviews markdown effectiveness: did the markdown drive volume or just margin loss? | Crystal Reports — Markdown History (no effectiveness calc) |
| `/reports/grid` (NEW) | BYR | BYR reviews sales by color/size matrix for seasonal planning | CP: Sales Analysis by Color/Size report |
| `/reports/flash` (NEW) | MGR | MGR monitors intraday sales pacing vs target | CP: X-Tape (manual run) |

---

## Wave 5 — W Execution (Cross-Domain)

The W-module screens follow the same scenario pattern as the Q Hawk case screens but generalize across all exception types (not just LP). One entry per key screen:

| Screen | Generalizes from | Key new scenarios |
|---|---|---|
| `/exceptions` | `/alerts` | MGR sees all operational exceptions across domains (not just LP) — inventory variance, receiving discrepancy, OTB breach, labor anomaly |
| `/exceptions/:id` | `/alerts/:id` | Cross-domain exception with context pulled from the relevant module |
| `/cases/new` | `/cases/hawk/:id/evidence` | Create a case from any exception type — not just LP alerts |
| `/cases/:id/evidence` | `/cases/hawk/:id/evidence` | Evidence from any module (receiving variance, inventory adjustment, timecard) |
| `/cases/:id/correlation` | `/cases/hawk/patterns` | Cross-domain subject correlation — same employee appears in LP case AND timecard anomaly |
| `/cases/:id/remediate` | New | Dispatch remediation action to the responsible module (e.g., "fix this item's price" → routes to pricing module) |
| `/reports/cases` | `/cases/hawk/analytics` | Cross-domain case performance — cases by module, by exception type, by resolution |

---

## Summary Tables

### Screens by User Role (Primary)

| Role | Primary screens | Count |
|---|---|---|
| LP Investigator | Alerts, Chirps, Cases, Transactions, Customers | ~25 screens |
| Store Manager | Transfers, Physical Count, Receiving, Reports, Timecards | ~30 screens |
| Buyer | Vendors, Orders, Suggested Orders, Promotions, Pricing, Range reports | ~20 screens |
| Receiving Clerk | Receiving session entry, Transfer receipt, RTV | ~8 screens |
| Admin | Users, Audit, Config health, All settings | ~15 screens |
| Employee | Time Clock only | 1 screen |

### Screens by Action Type

| Action type | Description | Example screens |
|---|---|---|
| Dashboard | Read-only KPI and status view | `/alerts`, `/chirps`, `/reports/*` |
| MCP Investigator | Deep-dive investigative surface | `/cases/hawk/:id`, `/transactions/:id/proof`, `/customers/:id/risk` |
| Workflow / Approval | Multi-step action with confirmation | `/receiving/:id`, `/transfers/new`, `/orders/new` |
| Config / Admin | Settings and configuration | All `/settings/*` screens |

### New Screens vs Original Wave Plan

| | Original wave plan | Amended (this doc) |
|---|---|---|
| Admin | 4 | 4 |
| Wave 1 — LP Core | 25 | 25 |
| Wave 2 — Store Ops | 16 | +7 (physical count ×3, transfer initiation+receipt, adjustment create, flash sales) = 23 |
| Wave 3 — Finance + Receiving | 10 | +7 (vendor ×2, PO ×2, blind receiving, EOD summary, GL distribution tab) = 17 |
| Wave 4 — Merch + Labor | 8 | +8 (timecard editor, mobile timeclock, payroll export, loyalty config, loyalty tab, price rules, grid report, calendar) = 16 |
| Wave 5 — W Execution | 7 | 7 |
| **Total** | **70** | **~92** |

---

*Source: 2026-05-04-counterpoint-canary-ux-crosswalk.md*  
*Every scenario in this document maps to at least one L3 process in the CRB or a confirmed Counterpoint user scenario from the functional decomp.*
