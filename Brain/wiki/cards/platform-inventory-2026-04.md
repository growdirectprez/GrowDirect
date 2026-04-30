---
type: wiki-article
status: active
classification: internal-confidential
owner: GrowDirect LLC
tags: [platform, inventory, identity, dns, gcp, github, secrets, gap-analysis, rebaseline, wave-1, preflight]
created: 2026-04-30
last-compiled: 2026-04-30
related-dispatch: GRO-703
needs-review: 2026-05-14
---

# Platform Inventory — Current State (April 2026)

A read-only audit of platform state on the eve of GCP rebaseline ([GRO-700](https://linear.app/growdirect/issue/GRO-700)) and the build-phase preflight waves. **No production state was touched.** Output is the gap list in §9 — the input to Wave 1 dispatches #2–#6 and Waves 2–5.

## Headline

Email is already on **Microsoft 365 (via the GoDaddy bundle)** — *not* a Workspace greenfield as Wave 1 originally framed. DNS sits at **GoDaddy** (`ns23/24.domaincontrol.com`), not Cloudflare. SPF, DKIM, and DMARC are misconfigured against the M365 reality. GCP is genuinely greenfield (no `gcloud`, no ADC, no projects). GitHub `growdirect-llc` org has **no 2FA enforcement**, this repo is on free tier (no branch protection available), there are **no CI workflows at the repo root**, and **no secret scanning** is enabled. The single biggest decision point: **commit to M365 (cheap, halfway-done) or migrate to Workspace (clean break, more work).**

The rest is detail.

## §1 — Domains & DNS

### `growdirect.io`

| Item | State |
|---|---|
| Registrar | **GoDaddy.com, LLC** |
| Expiry | 2027-07-08 |
| Privacy proxy | Domains By Proxy, LLC (Arizona) |
| Authoritative NS | `ns23.domaincontrol.com`, `ns24.domaincontrol.com` (GoDaddy DNS) |
| Apex A records | GitHub Pages IPs (`185.199.108–111.153`) |
| MX | `growdirect-io.mail.protection.outlook.com` (**Microsoft 365**) |
| Tenant | `NETORGFT19175160.onmicrosoft.com` (GoDaddy-bundled M365 reseller pattern) |
| SPF | `v=spf1 include:secureserver.net -all` (**points to GoDaddy email forwarder; does NOT include M365 — misaligned with MX**) |
| DKIM (`selector1/2._domainkey`) | **Not configured** — M365 DKIM signing is OFF |
| DMARC | `v=DMARC1; p=reject; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net` (**reports go to GoDaddy, not internal**) |
| autodiscover | `autodiscover.outlook.com` (M365) |
| sip / lyncdiscover | `sipdir.online.lync.com`, `webdir.online.lync.com` (Skype-for-Business / Teams) |
| msoid | `clientconfig.microsoftonline-p.net` (M365) |
| `_domainconnect` | `_domainconnect.gd.domaincontrol.com` (GoDaddy DNS auto-config) |
| enterpriseregistration | **Not configured** (Azure AD device registration not set up) |

### Subdomain map

| Subdomain | State | Target |
|---|---|---|
| `catz.growdirect.io` | live | CNAME → `growdirect-llc.github.io` (three-vault architecture) |
| `crb.growdirect.io` | live | CNAME → `growdirect-llc.github.io` |
| `ncr.growdirect.io` | live | CNAME → `growdirect-llc.github.io` |
| `www.growdirect.io` | live | apex |
| `ops.growdirect.io` | **missing** | reserved for future ops dashboard |
| `mail.growdirect.io` | **missing** | M365 webmail lives at `outlook.com`; subdomain unneeded |
| `id.growdirect.io` | **missing** | reserved for future identity proxy |
| `api.growdirect.io` | **missing** | reserved for Canary Go API endpoint |
| `dev.growdirect.io` | **missing** | reserved for staging |

### `ownpalosverdes.com`

| Item | State |
|---|---|
| Authoritative NS | `arch.ns.cloudflare.com`, `sloan.ns.cloudflare.com` (**Cloudflare**) |
| Apex A | Cloudflare proxy IPs (`104.21.81.108`, `172.67.159.86`) |
| Notes | Different registrar/zone host from `growdirect.io`. Founder owns analytics under `gclyle@gmail.com` (per memory). |

### Founder-action required

- Confirm GoDaddy account ownership (which email is logged in)
- Confirm M365 admin tenant access on `NETORGFT19175160.onmicrosoft.com`
- Confirm Cloudflare account ownership for `ownpalosverdes.com`

---

## §2 — Identity

### Bound identities discovered

| System | Identity | Authority | Notes |
|---|---|---|---|
| Git committer (this repo) | `Alejandro <bonsallprotea@gmail.com>` | committer | matches the user-email in session context |
| Linear workspace | `gclyle@growdirect.io` | M365 mailbox | proves M365 mailbox is in active use |
| GitHub user (active) | `growdirectprez` | personal account | NOT an org; owns this repo |
| GitHub org | `growdirect-llc` | org | personal account is a member; 2FA NOT enforced |
| GitHub auth method | SSH (`id_canary` keypair) + `gh` CLI PAT (scopes: `admin:public_key, gist, read:org, repo`) | session | scoped read-only on org admin |
| Cloudflare (`ownpalosverdes.com`) | unknown account | founder-only | no API token in env; `wrangler` not authenticated |
| Anthropic / OpenAI | unknown | founder-only | not in this session's env |
| GoDaddy registrar (`growdirect.io`) | unknown account | founder-only | likely email-bundled with M365 tenant |
| Square sandbox | `gclyle@gmail.com` (per memory) | founder-only | Canary integration tests |
| GA4 / Search Console (`ownpalosverdes.com`) | `gclyle@gmail.com` (per memory) | founder-only | personal Gmail, not Workspace/M365 |

### MFA state

| System | MFA enforced? |
|---|---|
| GitHub `growdirect-llc` org | **No** (`two_factor_requirement_enabled: false`) |
| GitHub `growdirectprez` user | unknown (cannot inspect from CLI) |
| M365 tenant | unknown (founder-action) |
| All other SaaS | unknown (founder-action) |

### Founder-action required

- Audit M365 tenant identities + conditional access policies
- Confirm `growdirectprez` MFA + recovery codes state
- Sweep personal-Gmail bindings across Anthropic, OpenAI, Cloudflare, Square admin, Linear admin, etc.

---

## §3 — GitHub

### `growdirectprez` — user account, owns this repo

| Item | State |
|---|---|
| Account type | **User** (not org) — corrects CLAUDE.md note about "two GitHub orgs" |
| MFA | unknown (cannot inspect) |
| Token scopes | `admin:public_key, gist, read:org, repo` |

### `growdirect-llc` — org

| Item | State |
|---|---|
| Members 2FA enforced | **No** |
| Members can create repos | yes (default) |
| Repos | `canary-retail-brain` (public), `canary-retail` (private), `ncr` (public), `catz` (public), `proposal` (public) |

### `growdirectprez/GrowDirect` — this repo

| Item | State |
|---|---|
| Visibility | private |
| Default branch | `main` |
| Branch protection on `main` | **Not available** — repo on free tier; requires Pro |
| CODEOWNERS | **Not present** |
| `.github/workflows/` at root | **Does not exist** |
| Existing CI | only `Canary/.github/workflows/ci.yml` (sub-app, separate Canary repo) |
| Actions secrets | none |
| Secret scanning / Dependabot | **Not enabled** (`security_and_analysis: null`) |
| Signed commits | not configured |

### Founder-action required

- Decide GitHub plan: free (current) → Pro (per-user) or Team/Enterprise (per-org)
- Decide whether to convert `growdirectprez` → org, or migrate this repo into `growdirect-llc`

---

## §4 — GCP

### State: **genuinely greenfield**

| Item | State |
|---|---|
| `gcloud` SDK installed | **No** (`gcloud not found`) |
| `gcloud` config dir | **Does not exist** (`~/.config/gcloud/` absent) |
| ADC file | **Does not exist** |
| Projects, orgs, billing | unknown (cannot inspect without CLI) |

Wave 2 prerequisites: install Google Cloud SDK; complete `gcloud auth login` and `gcloud auth application-default login`; link a billing account; create org → folder → project hierarchy.

### Founder-action required

- Confirm whether a GCP organization exists today under any founder identity
- Decide billing payment method (existing card vs. separate finance account)

---

## §5 — Secrets & credentials

### Local-only (NOT currently tracked in git)

| Location | Type | Notes |
|---|---|---|
| `.mcp.json` (gitignored) | Obsidian REST API key, memory-bus dev API key | local-loopback-only auth (`127.0.0.1`); compromise impact limited |
| `~/Library/Application Support/Claude/claude_desktop_config.json` | memory-bus key | desktop Cowork-side MCP |
| `Canary/.env`, `Canary/.env.test`, `Cove/.env`, `Solex/.env` | app dev secrets | gitignored via top-level directory patterns |
| `~/.ssh/id_canary` (single keypair) | SSH private key | used for `git@github.com` auth |

### Tracked in git (templates only — no values)

- `Angel/.env.example`
- `Solex/.env.example`

### Risk: historical `.mcp.json` commits

`git log` returns commits touching `.mcp.json`. Current state: not tracked. The `.gitignore` adds an explicit comment "MCP server config — contains API keys, never commit." That implies the file was *committed before being gitignored*. Keys are local-loopback (Obsidian REST + memory-bus dev key) so practical compromise is low, but **secrets that ever land in git history should be rotated** even if low-impact.

### Tools NOT installed

- `gcloud` (Google Cloud SDK)
- `op` (1Password CLI)
- `aws` (AWS CLI)

### Tools installed

- `wrangler` 4.85.0 (Cloudflare; **not authenticated**)
- `gh` (authenticated as `growdirectprez`)
- Docker (per CLAUDE.md, not re-verified here)

### Founder-action required

- Decide secrets-store strategy: 1Password (recommended), GCP Secret Manager (Wave 2), or both
- Decide whether to rotate the historically-committed Obsidian REST API key

---

## §6 — Cloudflare

### State: **partially used, not authenticated locally**

| Domain | Cloudflare? |
|---|---|
| `growdirect.io` | **No** — uses GoDaddy DNS |
| `ownpalosverdes.com` | **Yes** — `arch.ns / sloan.ns.cloudflare.com` |

`wrangler` is installed but **not authenticated**. No `~/.wrangler/` config dir exists. No Cloudflare API token in local env.

### Founder-action required

- Confirm Cloudflare account email and 2FA state
- Decide whether to migrate `growdirect.io` DNS from GoDaddy → Cloudflare during Wave 1 (recommendation: yes — Cloudflare is more agentable, cheaper, and faster to manage at this scale)

---

## §7 — Mini (ALXjr workstation)

### Cannot inspect from this session

This audit ran on the laptop. The mini runs the production Docker stack and is the dispatch executor. Per CLAUDE.md the expected state is:

- Docker stack at `~/GrowDirect/devops/docker-compose.yml` + `~/GrowDirect/CanaryGo/deploy/docker-compose.yml`
- Memory bus at `http://127.0.0.1:8003/mcp`
- Embeddings via `growdirect_ollama` container
- Per memory, Ollama "unhealthy" status is a known false positive (curl not in image)

### Founder-action required (or first dispatch of Wave 3)

On the mini, capture and append to this card:

```
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
which gcloud && gcloud config list
ls -la ~/.config/gcloud/application_default_credentials.json 2>&1
git -C ~/GrowDirect status --short
git -C ~/GrowDirect log --oneline -3
git -C ~/GrowDirect branch --show-current
curl -s http://127.0.0.1:8003/mcp -H "X-API-Key: $MCP_API_KEY" | head -1
```

Best filed as the first dispatch of Wave 3 (mini-as-dev-workstation rebaseline). The mini will also need `gcloud` install + ADC.

---

## §8 — Linear & Brain

### Linear

| Item | State |
|---|---|
| Workspace | `growdirect` (team key `GRO`) |
| Dispatch project | exists, lead `gclyle@growdirect.io`, status Backlog |
| Open Todo dispatches | 4 (incl. this one): GRO-684, GRO-603, GRO-594, GRO-703 |
| Label set | mature: `Target/{any,laptop,mini}`, `Agent/{ALX,ALXjr,Canary Builder,Cove Builder,Jeffe}`, `Type/{Research,Tech Debt,Feature,Bug}`, `Compliance/{Privacy,PCI,Davis-Stirling}`, `Stage/{Blueprint,TDD,Assembly,Verify,Ship,QA}` |
| Founder-action required | Confirm Linear SSO state; bind to M365 identity |

### Brain MOC coverage

12 project MOCs in `Brain/projects/` — CLAUDE.md mentions only five (Method, Canary, Cove, Angel, Secure) but the actual set is broader: Angel, CATz, Canary, CanaryRetailBrain, Cove, Factory, GrowDirect, Method, NCR, RetailSpine, Seacove, Secure.

`Brain/wiki/cards/` contains 69 cards. `Brain/` top-level folders: agents, attachments, dispatches, method, playbooks, process-decomp, projects, raw, templates, wiki.

CLAUDE.md is mildly out-of-date on the project MOC enumeration. Worth a one-line update in a future Wave 4 dispatch.

### Repo-level oddities (worth flagging)

- `CATz/` directory exists locally — per `feedback_solex_illustrative` and the three-vault feedback ("no persistent local clone"), this is a violation. Content lives in the `growdirect-llc/catz` repo; the local directory should be removed.
- `Solex/` directory exists with full app scaffolding (`.env`, `pyproject.toml`, `package.json`, `devops/`). Per memory, Solex is *illustrative not authoritative*; flag for cleanup.
- `private/` directory holds personal financial documents (1099-NEC, 1095, 1098-T, 1099-INT). **Confirmed gitignored** with zero tracked files. Safe.
- `.superpowers/brainstorm/` exists at repo root and is **not gitignored**. Worth deciding whether brainstorm artifacts should be tracked.
- Repo size: **12 GB** (almost entirely `Brain/raw/` intake binaries — the Secure/Kroger sprint and pre-history archives).

---

## §9 — Gap analysis (sequenced)

### Wave 1 — Identity spine (revised)

The original Wave 1 framing assumed Workspace greenfield. Reality is a half-finished M365 install with broken DNS hygiene. Two reroutes:

- **Path A — Commit to M365.** Cheaper, faster. Fix SPF, set up DKIM, redirect DMARC reports to internal mailbox, formalize tenant admin practices. Identity source for downstream becomes Microsoft Entra ID (Azure AD), federated to GCP IAM via OIDC.
- **Path B — Migrate to Workspace.** Clean break, better Google ecosystem fit. More work — domain MX cutover, mailbox migration, M365 tenant teardown.

**Recommendation:** Path A, unless there is a strategic reason to leave M365. The mailbox is in active daily use; migration cost is real; M365 → Entra ID → GCP IAM via OIDC is a viable identity spine. Wave 1 below is scoped against Path A.

Wave 1 dispatches (Path A):

1. ✅ This inventory (GRO-703)
2. **Audit M365 admin posture** — tenant admin email, conditional access, MFA enforcement, recovery accounts. Founder-action: log into `admin.microsoft.com` and capture state into a follow-up wiki card. Target: laptop.
3. **Fix SPF / DKIM / DMARC** — replace SPF with M365 include; configure `selector1/2._domainkey` CNAMEs to M365; update DMARC `rua` to internal mailbox. ALX drafts records; founder applies in GoDaddy DNS. Target: laptop.
4. **Migrate `growdirect.io` DNS GoDaddy → Cloudflare** — recommended for tooling, cost, and agentability. Target: laptop. Founder + ALX co-execute.
5. **Stand up M365 group spine** — `engineers@`, `ops@`, `admins@`, `founders@`, `dispatch@` as M365 / Entra ID groups. Target: laptop. Founder-action.
6. **Identity migration audit** — sweep every SaaS where `gclyle@gmail.com` or `bonsallprotea@gmail.com` is the bound identity; produce sequenced cutover plan to `gclyle@growdirect.io`. Target: laptop. ALX drafts; founder confirms.
7. **M365 admin runbook** — `Brain/wiki/cards/m365-admin-runbook.md`: onboarding, offboarding, MFA reset, group membership. Target: laptop. Agent: ALX.
8. **Wave-1 closeout audit** — verify §1–§7 of *this* card flip from "founder-action required" to "configured." Target: laptop. Agent: ALX.

### Wave 2 — GCP rebaseline (GRO-700)

Greenfield install. Prerequisites: install Google Cloud SDK (laptop + mini); pick org email (M365 mailbox); select billing payment method.

Dispatches: install gcloud + ADC; create GCP org → `growdirect-prod` and `growdirect-dev` projects; bind IAM to M365/Entra ID groups via Workload Identity Federation; provision Secret Manager, Artifact Registry, Cloud Build; create audit log sinks to BigQuery; set org policies (no public buckets, no service-account-key creation).

### Wave 3 — Mini-as-dev-workstation rebaseline

Mini-side install of `gcloud` + ADC; verify Docker stack health; verify memory bus + embeddings; document standard startup sequence as a Brain card; clean up mini-side artifacts not in this repo.

### Wave 4 — Repo + CI rebaseline

- Decide GitHub plan upgrade (free → Pro / Team / Enterprise) — required for branch protection on private repos
- Add `.github/CODEOWNERS` at repo root
- Add `.github/workflows/` with at least: lint, test, secret-scan, dependency-review, signed-commit verification
- Wire GitHub → GCP via Workload Identity Federation (no service-account keys ever in Actions secrets)
- Enable secret scanning + Dependabot on `growdirectprez/GrowDirect` and on all `growdirect-llc` repos
- Enforce 2FA on `growdirect-llc` org
- Decide whether to convert `growdirectprez` user → org, or migrate this repo into `growdirect-llc`
- Reinstall the post-commit memory-bus seed hook fresh
- Install `pre-commit` framework with secret-scanning hooks (gitleaks)
- Rotate the historically-committed Obsidian REST API key

### Wave 5 — Insurance closeout (GRO-686 → GRO-699)

Most insurance items resolve as side effects of Waves 1–4:

- Identity baseline (MFA, recovery, identity source) → **Wave 1**
- IAM and audit logging → **Wave 2**
- Secret management → **Wave 2 + Wave 4**
- CI security (secret scan, dep review, signed commits) → **Wave 4**

Residual: policy docs that aren't a side effect of any technical change.

- Acceptable use policy
- Incident response runbook
- Data classification + retention
- Vendor risk register
- Backup + DR runbook

These are dispatchable to ALX with founder review.

### Wave 6 — First Canary Go build dispatch

Spine bootstrap: structured logging, config, observability shim, `/healthz`, GCP creds wiring via ADC. Prereq: Waves 1–4 green.

`CanaryGo/go.mod` and `go.sum` already exist (744 / 4917 bytes — barely bootstrapped). The actual module skeleton from `docs/sdds/go-handoff/go-module-layout.md` has not landed yet.

---

## Closeout

**Biggest single insight:** This is M365, not Workspace. Wave 1 reroutes around that fact. Everything else sequences behind it.

**Decision points the founder owns** (in dependency order):

1. M365 vs Workspace (Path A vs B) — *biggest*, gates Wave 1
2. GoDaddy → Cloudflare DNS migration — gates Wave 1 dispatches #3, #4
3. GitHub plan upgrade — gates Wave 4
4. Whether to rotate historically-committed MCP keys — Wave 4 hygiene
5. GCP billing source — gates Wave 2

## Related

- [[Brain/projects/Method|Method MOC]] — methodology context
- [[Brain/wiki/cards/platform-thesis|Platform Thesis]] — three accountability rails, meter model
- [[Brain/wiki/cards/platform-stack-commitment|Platform Stack Commitment]] — GCP-and-bought-not-built decision (2026-04-29)
- [[Brain/wiki/canary-go-portal|Canary Go Portal]] — active build reference

**Related Linear issues:** GRO-700 (GCP rebuild), GRO-686 → GRO-699 (insurance prereqs), GRO-684 (Brain synthesis), GRO-703 (this audit).
