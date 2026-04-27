---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
companion: Brain/wiki/ncr-counterpoint-connection-runbook.md
----

# NCR Counterpoint Sandbox Setup — Operator Action Checklist

What GrowDirect needs to action to stand up a Counterpoint API sandbox for Phase 0 fixture testing. The connection runbook (`ncr-counterpoint-connection-runbook.md`) covers the technical bring-up; this article covers the **operator-facing prerequisites** that gate it — the things only the operator can do because they require human-in-the-loop NCR partner-channel interaction.

## Strategic context — NCR Voyix is a competitor

**Important:** NCR Voyix competes with Canary in the back-office analytics + LP layer. Treat NCR-gated credentials as scarce and strategic, NOT as routine vendor onboarding. Per memory `project_ncr_voyix_is_competitor.md`:

- APIKey applications are manually reviewed by NCR — competitive applicants can be rejected
- Channel Partner / ISV applications expose competitive intelligence to NCR
- The integration-access strategy routes through the customer (license holder), not via NCR partnership
- Frame any NCR-facing communication neutrally (data access / connector), not as competitive LP/analytics positioning

The credentials below are listed in priority order. The single hard dependency on NCR is the **Developer APIKey** (#2). The other paths have customer-side workarounds that don't require NCR cooperation.

## NCR-side credentials (in priority order)

### 1. Partner Portal access — OPTIONAL (and competitively sensitive)

The "Partner Portal" gates the API server installer download. **You don't need this if customers self-host their own Counterpoint API server (which they typically do)** — the customer's existing Counterpoint deployment already includes the API server installer through their VAR.

**Recommendation:** **deprioritize the Partner Portal application.** It's a competitive-intelligence exposure with limited unique value. If you want the installer for sandbox stand-up specifically, request through a friendly VAR rather than direct.

**If you do apply:**
- Direct NCR Channel Partner application: `https://www.ncrvoyix.com/company/become-a-channel-partner`. Frame as ISV / data-access partner, not reseller. **Avoid emphasizing LP / fraud detection / analytics** in the application description (those are competitive surfaces; Voyix may decline).
- Alternative: ask a Counterpoint VAR (Rapid POS, AMS Retail, RCS, Mariner) to provide installer access without partner-portal application.

### 2. Developer API Key — REQUIRED, COMPETITIVELY GATED

This is the **one NCR-side dependency you cannot work around** for production deployments. Almost every useful endpoint requires an APIKey header; without one, calls fail 403.

**The risk:** NCR reviews applications manually. They CAN decline a competitor's application or one whose stated purpose competes with their portfolio.

**Application form:** [`https://retailchannel.radiantsystems.com/api_request.htm`](https://retailchannel.radiantsystems.com/api_request.htm)

**Framing for the application** — protective drafting (avoid lying; frame for what's defensible):
- Company Name: `GrowDirect LLC`
- Issued To: `Geoffrey C. Lyle`
- Application Name: `Canary` (neutral; the brand; it is what it is)
- Description: focus on **integration / data-access / connector** language. Example: "Canary is a data-integration platform that allows specialty SMB retailers to connect their Counterpoint data to downstream analytics, reporting, and operational tools. The Canary adapter reads Counterpoint via the public REST API on a per-customer basis under each customer's own API option license; the customer authorizes access on a per-tenant basis."
- **Do NOT emphasize:** loss prevention, fraud detection, anomaly detection, employee monitoring, cash anomalies — these are NCR's competitive surfaces.
- **Do emphasize:** read-only integration, customer-permissioned, per-tenant isolation, complements (not replaces) the customer's existing Counterpoint stack.

**Mitigations if rejected:**
1. **Customer's own APIKey route** — each customer applies for their own Developer Key for "internal Counterpoint integration"; Canary's adapter operates within their Key. Per-customer, doesn't scale, but works.
2. **VAR partnership / acquisition** — VARs already have APIKeys; Canary becomes a value-add inside a VAR's offering. Strategic pivot.
3. **Direct SQL fallback** — customer grants SQL Server access; Canary reads via SQL, not REST. Brittle, customer-permission-dependent, works.

**Once approved (delivered via email, ~1-2 weeks):**
- `Canary_key.txt` — plain-text key (embed in adapter)
- `Canary_key.xml` — signed XML file (drop into `<install>/APIKeys/` on every Counterpoint API server Canary connects to)
- Valid 2 years

### 3. FTP credentials for `files165.cyberlynk.net` — DEFERRED

Test database for sandbox. Useful for spec-vs-reality validation but **not required for Phase 0-4 work** (OpenAPI mocks suffice; see `Brain/wiki/ncr-counterpoint-connection-runbook.md` for the lightweight alternative path).

**Recommendation:** defer. Don't request until Phase 5 cutover validation OR until customer-real-instance access is unavailable. Saves a competitive-intelligence ping to NCR and removes a non-blocking dependency.

If needed: request via NCR Channel Sales OR your VAR.

### 2. Developer API Key — `https://retailchannel.radiantsystems.com/api_request.htm`

Free; manually reviewed. Required for almost all useful API calls (most endpoints fail with 403 without one).

**Action:** submit application form. Required fields:
- Company Name: `GrowDirect LLC`
- Issued To: `Geoffrey C. Lyle`
- Email 1, Email 2 (recommend founder + a backup ops mailbox)
- Application Name: `Canary` (or `Canary Retail Ops` if more specific)
- Description: tight one-paragraph — back-office analytics + loss prevention layer for SMB specialty retailers; reads from Counterpoint via REST; doesn't write to customer data; per-tenant isolated.

**Constraint:** "a distinct key is used for each 'usage' of the API." If GrowDirect builds multiple Counterpoint-using products in the future, each needs its own key. For now: one key for Canary.

**Once approved you get** (delivered via email, ~1-2 weeks typical):
- `Canary_key.txt` — plain-text key (embed in adapter, treat as secret)
- `Canary_key.xml` — signed XML file (drop into `<install>/APIKeys/` on every Counterpoint API server Canary connects to)
- Key valid for 2 years; renewal is separate cycle

### 3. FTP credentials for `files165.cyberlynk.net`

Test database + TLD for sandbox. Issued by NCR per partner.

**Action:** request via NCR Channel Sales OR via your VAR after partner-portal access is established. Cite the public README pointer ("test databases can be downloaded via ftp from `files165.cyberlynk.net`").

**Once approved you get:** FTP credentials (username + password) → download QATestGolf or similar standard test DB + TLD bundle.

## Sandbox host requirements

Counterpoint API server is **Windows-only**. Three host options:

| Option | Setup time | Pros | Cons |
|---|---|---|---|
| Dedicated Windows VM (cloud — Azure, AWS, Hetzner) | 1-2 hours | Isolated; persists; team-accessible | Monthly cost; needs SQL Server |
| Windows VM on Mac (Parallels / VMware Fusion / UTM) | 1-2 hours setup + license | Local; free if Windows license already owned | Mac resources; not team-shared |
| Spare physical Windows machine | Instant if available | Free; native | Not always available |

**Recommended for Phase 0 development:** dedicated cloud Windows VM. Specifications:
- Windows Server 2019 or 2022 (newer than minimum; less TLS-1.2 plumbing)
- .NET 4.5.2+ (already present on Server 2019/2022)
- 8 GB RAM
- SQL Server Express (free) or SQL Server Developer Edition (free for non-prod)
- Open inbound HTTPS port (default 52000)
- TLD folder created (any local drive)

**Mini relevance:** the Mac mini reconfig dispatch (`Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md`) does NOT include hosting Counterpoint sandbox — that would put a Windows VM on the mini, which adds complexity beyond the mini's narrowed steady-state role (Quartz + apps + supporting infra). Sandbox should live on a separate cloud or local-Mac VM.

## Customer-side prerequisite (for production deployments — Phase 5+)

The **customer's** Counterpoint license must have the **API user option** enabled in their `registration.ini`. This is a paid add-on to the customer's Counterpoint subscription.

**Action (for the customer's reseller partner — typically the VAR who deployed Counterpoint):** request the option at `https://retailchannel.radiantsystems.com/api_option_request.htm`:
1. Login to Partner Portal (the VAR has this; GrowDirect may eventually too)
2. Navigate to api_option_request.htm
3. Choose the customer's Counterpoint system serial number
4. Submit

NCR Sales Ops processes the request and adds the option to the customer's `registration.ini`. Time: typically days.

**For new merchants** (greenfield Counterpoint customers): the VAR adds "Please Add API Option" to system notes during the order; sales ops includes it.

**This is NOT something GrowDirect can do for the customer.** The customer's Counterpoint reseller has to request it. For the H&G chain engagement, this is part of the customer-facing onboarding — confirm during Phase II To-Be Workshops that the customer has the API option (or get it requested) before integration work begins.

## Sequencing — when to do each

| When | Action |
|---|---|
| Now (today) | Submit Partner Portal application (Path 1). Submit API Key application (Path 2 — may run in parallel). |
| Within 1 week | Stand up Windows sandbox VM (Path B preparation). Don't wait on NCR — VM stand-up is operator-driven. |
| Once partner credentials arrive (~2-4 weeks expected) | Download installer; request FTP creds for test DB; install + configure per the connection runbook |
| Once API Key XML arrives (separate from partner — could come earlier) | Drop into APIKeys/ folder on the configured API server |
| Phase 0 ready | Smoke-test with `GET /SystemInfo`; run first endpoint reads via Canary's TSP adapter |

## Operator-action summary (revised — NCR-as-competitor framing)

**Today / this week:**
- [ ] **Submit Developer API Key application** with NEUTRAL framing (data-access/integration, NOT LP/analytics). Per the protective-drafting guidance in §"Developer API Key" above. This is the one NCR-side dependency that's hard to work around. 1-2 weeks NCR-side response.
- [ ] **Skip Partner Portal application** unless VAR-sponsored and you have specific need for the installer. Competitive-intel exposure with limited unique value.
- [ ] **Skip FTP / sandbox-host provisioning for now.** Phase 0-4 work runs against the OpenAPI mock / fixture path (see `Brain/wiki/ncr-counterpoint-connection-runbook.md` lightweight alternative). Saves cloud-VM cost + avoids NCR-side ping.

**When APIKey arrives:**
- [ ] Drop `Canary_key.xml` into a known-good location for distribution to customer Counterpoint installations
- [ ] Document the renewal cycle (2-year validity) in operations runbook

**For the H&G chain engagement (Phase 5+):**
- [ ] Confirm customer has API option enabled in their `registration.ini` (their VAR requests)
- [ ] Customer creates a Canary-specific service account on their Counterpoint API server
- [ ] Customer installs `Canary_key.xml` in their `<install>/APIKeys/` folder
- [ ] Customer-side firewall / Cloudflare Tunnel / VPN configured for Canary access
- [ ] Smoke-test against the customer's actual Counterpoint API server

**APIKey-rejection contingency** (if NCR declines the application):
- [ ] Pivot to customer's-own-APIKey route (per-customer; tedious; works) OR
- [ ] Pivot to VAR partnership (Canary inside a VAR's offering; strategic) OR
- [ ] Pivot to direct SQL fallback (brittle but works)

**What's no longer on the operator critical path:**
- ~~Partner Portal application~~ (deprioritized; competitively risky)
- ~~Sandbox host provisioning~~ (deferred; OpenAPI mocks suffice for development)
- ~~FTP test DB request~~ (deferred; customer-real-instance is the realistic Phase 5 substrate)

## Open questions

- Does the partner-portal application have a typical SLA for response? (Have not surfaced this from public sources.)
- Is the API Key application separable from full Partner Portal access? (Some signals suggest yes — developer API Key may be available to non-partners; need to verify when submitting.)
- Does NCR offer a hosted-sandbox alternative (e.g., a shared dev environment) so we don't have to stand up our own? (Not surfaced in public docs; worth asking Channel Sales.)

## Related

- `Brain/wiki/ncr-counterpoint-connection-runbook.md` — technical bring-up steps once credentials are in hand
- `Brain/wiki/ncr-counterpoint-api-reference.md` — API surface catalog
- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 dispatch (consumes this sandbox)
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/InstallationAndConfiguration/Installing.md` — NCR's official install doc
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/InstallationAndConfiguration/Licensing.md` — NCR's API key + registration.ini option doc
