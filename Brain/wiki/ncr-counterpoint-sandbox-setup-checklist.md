---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
companion: Brain/wiki/ncr-counterpoint-connection-runbook.md
---

# NCR Counterpoint Sandbox Setup — Operator Action Checklist

What GrowDirect needs to action to stand up a Counterpoint API sandbox for Phase 0 fixture testing. The connection runbook (`ncr-counterpoint-connection-runbook.md`) covers the technical bring-up; this article covers the **operator-facing prerequisites** that gate it — the things only the operator can do because they require human-in-the-loop NCR partner-channel interaction.

## Three NCR-side credentials needed (separate requests)

### 1. Partner Portal access — `retailchannel.radiantsystems.com`

The "Partner Portal" is the legacy Radiant-era interface NCR still operates for Counterpoint VARs and partners. It gates: the API server installer (.exe download) AND the API-option-request flow for future customer deployments. Without it, you can't download the software.

**Action:** apply for partner status. Two paths:
- **Direct NCR Channel Partner application** — `https://www.ncrvoyix.com/company/become-a-channel-partner`. Channel Sales contact form. As GrowDirect LLC; frame the application as ISV / integration partner (not reseller — see `Brain/wiki/...` notes about ISV vs Channel-Partner distinction).
- **Via an existing VAR** — any of the Counterpoint VARs (Rapid POS, AMS Retail, RCS, Mariner) can sponsor partner-portal access for a partner's application. Faster if the VAR sees a co-sell opportunity.

**Time-to-credentials:** typical vendor ISV onboarding is 1-4 weeks. Could be faster via VAR sponsorship.

**Once approved you get:**
- Partner Portal login
- Counterpoint API server installer (.exe) download
- API option request capability (for future customer-side enablement)
- API Key application form access

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

## Operator-action summary (do these now)

- [ ] **Submit NCR Channel Partner application** (or contact a VAR for sponsorship): https://www.ncrvoyix.com/company/become-a-channel-partner
- [ ] **Submit Developer API Key application**: https://retailchannel.radiantsystems.com/api_request.htm — needs Partner Portal login first OR can be submitted as a developer-only request (verify at submission time)
- [ ] **Decide on sandbox host** — cloud Windows VM (recommended) vs local Mac Windows VM. Approximate cost: $30-60/month for a small Azure/AWS Windows VM
- [ ] **Provision the sandbox host** — install Windows + .NET 4.5.2 + SQL Server Express, configure firewall for inbound HTTPS
- [ ] **Once partner credentials arrive**: request FTP test DB credentials
- [ ] **Confirm with the H&G chain (Phase 5+)**: do they currently have the API option enabled? If not, their VAR needs to request it.

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
