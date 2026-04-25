---
date: 2026-04-24
type: audit-report
classification: confidential
owner: GrowDirect LLC
phase: G2
scope: GrowDirect docs (SHOW) + Platform-supporting Brain
---

# CTO-Readiness Audit — GrowDirect Docs + Platform Brain

## Summary

48 files audited across `docs/sdds/{platform,alx}/`, `docs/superpowers/{briefs,specs,plans,dispatches}/` (filtered to non-app-specific), `docs/dispatches/`, `Brain/projects/` (Method/Factory/GrowDirect/RetailSpine), `Brain/method/`, `Brain/wiki/methodology-*` and `Brain/wiki/growdirect-factory-process.md`, plus root `README.md` / `CLAUDE.md` / `SECURITY.md`.

Total findings: **41**. Critical **1** · High **5** · Medium **4** · Low **31** (frontmatter sweep).

Sensitive-name leakage and missing classification frontmatter dominate. AI-voice residue is essentially clean (one stylistic quote in a demo script, no genuine AI-residue in prose). Doc quality is high — no Lorem ipsum, no malformed wikilinks, no empty sections detected. Several spec/dispatch files reference legacy Jeffe/SysRepublic/Kroger material that needs scrub or relocation under the user's "scrub client names" feedback.

Completion: **100%** of declared SHOW scope swept. Time used: ~12 min.

## Findings by severity

### CRITICAL (1)

**C1 — Named retail clients used as structural source labels in synthesis-layer wikis.**
Files: `Brain/wiki/methodology-ibm-retail-diagnostic.md`, `Brain/wiki/methodology-ibm-it-architecture-options.md`.
Lines: retail-diagnostic.md L5/14/17/24/33/47/50/128/132/136/182/205/224/230/232/234/244/249/255/301; it-architecture-options.md L5/14/17/25/194/210/213/219.
Dimension: Sensitive names.
Severity: CRITICAL — these are Brain `wiki/` files (synthesis layer), and the user's standing rule is that synthesis layers (wiki/briefs/playbooks/research) abstract named retail clients into NFR deployment archetypes. Both files (a) name the retailer in titles, frontmatter `source:`, and body text dozens of times; (b) reference original-deliverable filenames that include the client name; (c) the retail-diagnostic article ALSO contains a worked case study at L255–301 with a "(illustrative archetype, not a real engagement)" disclaimer at L301 — that disclaimer is good, but the surrounding article still names the client as the structural template owner. IBM as a methodology source is acceptable; treating an IBM client deck as a *named pattern* in the synthesis layer is not.
Recommended action: Replace client-named pattern labels (`(<Client> pattern)`, `the <Client> deck`, `In <Client>:`) with archetype labels (e.g., "European footwear specialty pattern" / "UK grocery anchor pattern"); keep the IBM BCS methodology attribution; move client-name provenance into a private `Brain/raw/` companion file, not the synthesis-layer wiki. Keep the L301 disclaimer model and propagate it.

### HIGH (5)

**H1 — Live demo dispatch references named LP-engineering-org employers as audience.**
File: `docs/dispatches/dispatch-demo-prep-2026-04-22.md`.
Lines: 10 ("build loss prevention systems at scale for [TIER-1 retailer], [TIER-1 retailer], [TIER-1 retailer]"), 731, 734, 736, 744.
Dimension: Sensitive names.
Severity: HIGH — these names appear in a non-archived dispatch describing the live demo audience ("[Big-3 grocery]", "[mass merchant]", "[mass-merchant grocery]") and provenance of seed Brain files (`[grocer]-*` files, `[POS-LP-vendor]-*` files). Per the user's "scrub client names" feedback this material should be in `Brain/raw/inbox/` (HIDE), not in active `docs/dispatches/`.
Recommended action: Either (a) abstract retailer names to "tier-1 grocery / mass-merchant" archetype language in the dispatch and remove the path strings naming `[grocer]-*` and `[POS-LP-vendor]-*` files, OR (b) move the dispatch to `docs/_archive/` (HIDE) since the demo window has passed.

**H2 — Secure-to-Canary handoff brief embeds raw client filenames and pricing detail.**
File: `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md`.
Lines: 21, 29, 35, 68, 82, 94, 108 (POS T-log pricing $660K/y + $450K install, DSD $350K, Pharmacy $500K with grocer name in path), 122 (2001 grocer Retek workaround catalog with grocer name in path), 136 (data-retention dispute by grocer with name in path), 150, 164, 184, 201.
Dimension: Sensitive names + client commercial detail.
Severity: HIGH — this is a synthesis-layer brief (`docs/superpowers/briefs/`) that names a tier-1 grocery client repeatedly, embeds 25-year-old commercial deal pricing tied to that client, and links forward to private wiki cards (`secure-client-[grocer]`). Per "scrub client names" rule, this content belongs in `Brain/raw/inbox/` (HIDE) where it's already gated, not in the brief layer.
Recommended action: Rewrite the brief to reference "the tier-1 grocery archetype deployment" / "an enterprise on-prem LP customer" patterns. Strip the `~/mnt/nas-archive/Work/Clients/[CLIENT]/...` filesystem paths; if provenance is required, link to a private inbox card. Remove specific dollar figures or label them as "indicative legacy enterprise pricing."

**H3 — Audit-spec doc references the same sensitive-client benchmarks as exemplars.**
File: `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md`.
Lines: 91, 234 (`## [Tier-1-grocer] Benchmark — Enterprise Scale Gap Analysis`), 306, 678.
Dimension: Sensitive names.
Severity: HIGH — the CTO-readiness audit's own design spec, which is a SHOW-layer doc, names a tier-1 grocer four times as a scale-benchmark anchor. The benchmark itself is fine; the named anchor is not.
Recommended action: Replace named-grocer references with "tier-1 enterprise grocery benchmark" or "Fortune-100 grocery scale baseline." The benchmark gap analysis already lives in a sibling audit report at `docs/audit-2026-04-23/enterprise-scale-gap-analysis.md` — wording there should match.

**H4 — Founder-name overload across SHOW dispatches and Brain MOC.**
Files: `docs/dispatches/dispatch-primetime-2026-04-23.md` (L39, 108, 428, 452), `docs/dispatches/dispatch-vscode-library-narrative-2026-04-22.md` (L35), `docs/dispatches/dispatch-site-2026-04-22.md` (L25, 43, 56), `docs/superpowers/briefs/2026-04-growdirect-method-initiative.md` (L34, 145), `docs/superpowers/specs/2026-04-15-growdirect-site-refresh-design.md` (L220 — `jeffe.io` server URL), `docs/superpowers/specs/2026-04-23-qa-agent-linear-filing-atlas-inline-design.md` (L22), `docs/superpowers/plans/2026-04-15-growdirect-site-refresh.md` (L595, 596 — same `jeffe.io` URL), `docs/superpowers/plans/2026-04-24-cto-readiness-remaining.md` (L29 — explicitly notes "Jeffe → CATz/Canary-Retail-Brain" sibling-vault refs scrubbed), `docs/sdds/platform/skill-architecture.md` (L132 — `jeffe-review` skill), `Brain/projects/GrowDirect.md` (L119, 129, 170), `Brain/wiki/growdirect-factory-process.md` (L26, 30, 34, 58, 100, 169, 171, 214, 218, 226, 235, 266, 291–348 entire "SysRepublic Factory" section).
Dimension: Sensitive names (founder/legacy-employer references).
Severity: HIGH — the founder's first name appears as a code identifier, server URL, Brain article filename references, role label ("PENDING JEFFE APPROVAL"), and as the named author of pull-quotes inside `growdirect-factory-process.md`. Some uses (skill name `jeffe-review`, role label `Jeffe` in factory roster) are intentional internal vocabulary; others (`jeffe.io` as production URL in two files, "Jeffe Quotes" wiki link in MOC) are footguns if these docs ever leave the org. The factory-process wiki additionally contains a complete "SysRepublic Factory — Where This Came From" section (L291–348) that names the legacy employer, the legacy product (Secure 3.5 / Secure 4 / Secure 5), the live URLs (`factory.solutions-sysrepublic.com`, `factoryqa.solutions-sysrepublic.com`), and a 2016 acquisition narrative. Per "scrub client names" the grocer is the highest-risk sensitive name; founder/legacy-employer names are a tier-down but the SysRepublic block is enough material to identify the founder uniquely and reproduce a prior-employer narrative in a wiki document.
Recommended action: (a) For `jeffe.io` URL leftovers (site-refresh spec/plan L595–596, L220): purge or convert to `growdirect.io`; flag as a Linear cleanup. (b) For `Brain/wiki/growdirect-factory-process.md` L291–348: split the SysRepublic provenance section into a private `Brain/raw/` card and replace with a single-line attribution ("Factory pipeline draws on a prior-employer methodology developed by founder; provenance archived privately"). (c) Leave the internal role label `Jeffe` and skill name `jeffe-review` as-is — they're internal vocabulary, but document this in a "Glossary / proper names" section so an external reviewer understands the convention. (d) "PENDING JEFFE APPROVAL" → "pending founder approval."

**H5 — `Brain/projects/RetailSpine.md` references named UK grocery client as interface-spec source.**
File: `Brain/projects/RetailSpine.md`.
Lines: 47 ("a [UK-grocer] interface or a Canary rule"), 70, 77, 391 ("`Brain/raw/inbox/Interface Design Documents/` — 378 [UK-grocer] interface specs, ...").
Dimension: Sensitive names.
Severity: HIGH — `RetailSpine` is a SHOW-scope MOC (per audit instructions). The MOC names a UK grocer four times as the source of 378 interface design specs that seed the spine. Same rule as C1: synthesis layer should abstract.
Recommended action: Replace "[UK-grocer]" with "tier-1 UK grocery archetype" or "the canonical UK-grocer interface set"; keep the inbox path under a relabeled folder ("Interface Design Documents — UK grocery") if file moves are desired, or leave the inbox path as-is (HIDE-scope) and just remove the client name from the MOC body.

### MEDIUM (4)

**M1 — Inbound platform doc refs an undocumented "Walmart, Target, Kroger" target audience.**
File: `docs/dispatches/dispatch-demo-prep-2026-04-22.md` line 10.
Dimension: Sensitive names + go-to-market positioning.
Severity: MEDIUM — names three named tier-1 retailers as the demo audience. This is more of a positioning leak than a client-relationship leak; the named retailers are not GrowDirect customers, just hypothetical reviewers. Still violates the "abstract named retail clients" rule.
Recommended action: "build loss prevention systems at scale for tier-1 retailers" — or list the demo-attendee orgs in a private prep doc.

**M2 — Memory-bus SDD ships with a default API key embedded as a non-secret literal.**
File: `docs/sdds/platform/memory-bus.md`.
Lines: 297 (`MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}`), 457 (same), 597 (same), 600, 612, 680.
Dimension: Doc quality / security hygiene (cross-references the security audit).
Severity: MEDIUM — the SDD documents the existence of a default-baked dev API key and explicitly flags it as P0-1 / P0-2 to fix. The doc is doing the right thing by surfacing the gap, but the literal string `growdirect-memory-dev-key` appears verbatim six times in committed documentation; if this default is still live anywhere, scanners will flag it. This is a duplicate of a finding already in `security.md`; recording here for completeness.
Recommended action: Cross-reference. If the dev key is being rotated, replace the literal in the doc with `<dev-default-redacted>` and put the actual default in `.env.example`.

**M3 — Memory-bus SDD documents `growdirect_memory` DB credentials inline.**
File: `docs/sdds/platform/shared-infrastructure.md`.
Lines: 192 (`POSTGRES_PASSWORD = growdirect_dev`), 199 (`--requirepass valkey_dev`), 206 (`PGADMIN_DEFAULT_PASSWORD = admin`), 217 (MCP_API_KEY default), 320 (P0-4 explicitly flags this).
Dimension: Doc quality / security hygiene.
Severity: MEDIUM — same shape as M2; SDD is telling the truth about dev credentials and flags the issue at L320 as P0-4. Confidentiality classification on the SDD would help.
Recommended action: Add the standard `classification: confidential` frontmatter (see L1–L48 sweep below); leave content as-is since the doc already calls out the gap.

**M4 — `dispatch-primetime-2026-04-23.md` references parked file `docs/playbook-method-katz-reverse-engineer.md`.**
File: `docs/dispatches/dispatch-primetime-2026-04-23.md` lines 39, 428, 452.
Dimension: Sensitive names — "Katz method" cites a named industry figure as a methodology.
Severity: MEDIUM — multiple parked references to a method labelled with the surname of a named retail-LP industry figure. The file is described as "Not started / PARKED." If it's never going to ship, decision: name change or archive.
Recommended action: Rename the parked playbook (e.g., `playbook-method-reverse-engineering-frame.md`); update all three references; or excise the row entirely.

### LOW (31)

**L1–L48 (consolidated) — 100% of audited SHOW files lack the `classification: confidential` and `owner: GrowDirect LLC` frontmatter declared as the standard in the audit-design spec L141 ("Confidentiality frontmatter").**

48 of 48 files (100%) have neither field. This is uniform absence, not selective absence — the standard hasn't been rolled out yet.

Files affected (compact list, all SHOW paths):
- `docs/sdds/platform/{aws-target-architecture,factory-pipeline,memory-bus,shared-infrastructure,skill-architecture}.md` (5)
- `docs/sdds/alx/{mcp-service-layer,test-lab}.md` (2)
- `docs/dispatches/dispatch-{demo-prep-2026-04-22,primetime-2026-04-23,vscode-library-narrative-2026-04-22,site-2026-04-22,api-docs-gateway-2026-04-22}.md` (5)
- `docs/superpowers/briefs/2026-04-{growdirect-method-initiative,secure-to-canary-handoff}.md` (2)
- `docs/superpowers/specs/{2026-03-30-mcp-consolidation-design, 2026-03-30-sdd-buildout-design, 2026-04-11-growdirect-workflow-wiki-design, 2026-04-13-sdd-ops-upgrade-design, 2026-04-14-growdirect-io-portfolio-site-design, 2026-04-15-growdirect-site-refresh-design, 2026-04-20-growdirect-services-page-design, 2026-04-21-qa-agent-tier-0-unblock-design, 2026-04-22-qa-agent-page-context-primary-design, 2026-04-23-qa-agent-linear-filing-atlas-inline-design}.md` (10)
- `docs/superpowers/dispatches/2026-04-22-demo-reseed.md` (1)
- `docs/superpowers/plans/{2026-03-30-mcp-consolidation, 2026-04-14-growdirect-io-portfolio-site, 2026-04-15-growdirect-site-refresh, 2026-04-21-qa-agent-tier-0-unblock, 2026-04-22-qa-agent-page-context-primary, 2026-04-23-qa-agent-linear-filing-atlas-inline, 2026-04-24-cto-readiness-remaining}.md` (7)
- `Brain/projects/{Method,Factory,GrowDirect,RetailSpine}.md` (4)
- `Brain/method/{Activities,CommDocs,Models,Orchestration,Roles,Techniques,WorkProducts}.md` (7)
- `Brain/wiki/{growdirect-factory-process,methodology-ibm-it-architecture-options,methodology-ibm-retail-diagnostic}.md` (3)
- `README.md`, `CLAUDE.md`, `SECURITY.md` (3 — README/CLAUDE/SECURITY are arguably PUBLIC by intent for SECURITY.md and the README for the public site, so frontmatter for those should probably read `classification: public`).

Total: 49 entries across 48 distinct files (count differs because the audit-design spec at `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md` was the meta-doc and is the only file in the spec list that does have a partial header).

Severity: LOW (per file) but **HIGH in aggregate** because none of the SHOW corpus is yet labeled per the policy that the audit itself is verifying. Per audit-spec requirements, the remediation is mechanical.

Recommended action: One pass of frontmatter insertion using existing `Brain/templates/`. Decide whether `Brain/projects/`, `Brain/method/`, and `Brain/wiki/methodology-*` are `confidential` or `internal` — the `methodology-ibm-*` wikis cite client provenance, so `confidential` is right; the Method MOC structure is `internal` at most. `README.md` and `SECURITY.md` should be `classification: public`.

## Findings by dimension

| Dimension | Hits | Severity profile |
|---|---|---|
| AI-voice (style residue) | 0 substantive (1 quoted demo dialogue, 1 self-referential pattern table in audit spec) | none |
| Sensitive names | 5 distinct hot-spots + 1 critical concentration (methodology-ibm-* wikis) | C1 + H1, H2, H3, H4, H5, M1, M4 |
| Markers (TODO/FIXME/WIP) | 7 hits, all meta or in active in-flight plans | none → all justified |
| Confidentiality frontmatter | 48 of 48 files (100%) absent | LOW per file, HIGH aggregate |
| Doc quality (Lorem ipsum, broken wikilinks, empty sections) | 0 | clean |
| Inline secrets / credentials | 2 SDDs document defaults inline (memory-bus, shared-infrastructure) | M2, M3 — duplicates of security.md findings |

Notable absences (good news):
- No Lorem ipsum or template placeholders.
- No malformed wikilinks across SHOW corpus.
- No AI-voice residue in narrative prose. The two AI-voice rg-hits were a quoted line of demo dialogue ("Now let me show you how this was built") and the audit-design spec listing AI-voice patterns as detection targets — both legitimate.
- No `[TBD]`, `[?]`, or `<placeholder>`-style unresolved tokens.

## Judgment calls

**J1 — Internal proper-name vocabulary vs. external scrub.** The factory pipeline uses the founder's first name (`Jeffe`) and a set of role-name proper nouns (`Eva, Tom, Jess, Jeremy, Jim, Owl, Art, Syd, ALX, ...`) as internal team/skill identifiers. These are pervasive and structural — they aren't accidents, they're the team-vocab convention. The `jeffe-review` skill, the "Jeffe directive" cite, the "Syd revision" press-release tag are all intentional. Founder decision: keep the internal vocabulary AND publish a one-page glossary, OR rename out of "Jeffe" to a generic "Founder Review" / "FoundeReview" / etc. Recommendation: keep + glossary. Internal role nouns are not the rule the "scrub client names" feedback is targeting; that rule targets *external client* names.

**J2 — `Brain/wiki/methodology-ibm-*` extent of scrub.** The two methodology articles credit IBM BCS 2006 deliverables for two specific named retail clients (Critical C1). The user's feedback is unambiguous that synthesis-layer wiki abstracts named clients. But the IBM BCS attribution itself is core to the article's authority claim. Founder decision: do we (a) abstract both client names but keep IBM BCS attribution; (b) abstract clients AND drop IBM attribution; or (c) move provenance entirely to `Brain/raw/` and write the wiki as a clean "structural pattern: retail diagnostic / IT architecture options" article. Recommendation: (c) — the wiki carries the framework, the raw inbox carries the IBM/client provenance. Companion skill files in `.claude/skills/consulting/` already exist; verify they don't carry the client name (out of scope of this audit; flag for canary-cleanup batch).

**J3 — `Brain/wiki/growdirect-factory-process.md` SysRepublic provenance section.** The article devotes lines 291–348 to documenting the SysRepublic origin of the methodology, including production URLs, screenshot evidence, and the 2016 acquisition narrative. This is genuine institutional-knowledge value (it's *why* the method works), and on the public-facing scrub axis it's mostly defensible (SysRepublic is a defunct entity, the URLs are dead). But the section names a specific prior employer, prior product line (Secure 3.5/4/5), and prior modules (LP Case Management, ICMS, EBR, Cashier Performance, Audit & Survey, Refund Management, Foundation Management, Incident Management, Risk Management). Founder decision: how much SysRepublic provenance survives the scrub. Recommendation: replace the entire L291–348 block with a 3-line attribution and move the rich content to a private `Brain/raw/founder-archive/factory-provenance.md`.

**J4 — `Brain/projects/Secure.md` and `Brain/projects/RetailSpine.md` MOCs are SHOW per audit instructions, but their content is heavily HIDE-flavored.** RetailSpine names a UK grocer four times (H5); Secure (referenced at GrowDirect MOC L236 as "archival retail LP IP from IBM / Appriss / Sysrepublic (career-lineage reference)") would be classified HIDE if the audit spec had said so, but it's listed as SHOW per the project taxonomy in `CLAUDE.md`. Founder decision: are RetailSpine and Secure (and the soon-to-arrive `Brain/wiki/secure-*` series) genuinely SHOW-layer artifacts, or are they internal-only career-archive material? Recommendation: declare them `classification: internal` (not `confidential`, not `public`), name-scrub the MOC bodies, and let the underlying `secure-client-*` wikis carry the named client material under `confidential` with raw inbox under HIDE. Effectively three tiers: HIDE (raw), CONFIDENTIAL (secure-client-*), INTERNAL (RetailSpine / Secure MOC).

**J5 — `docs/dispatches/dispatch-demo-prep-2026-04-22.md` and `dispatch-primetime-2026-04-23.md` are post-event dispatches.** Their demo windows (April 22–26) end inside the audit window (April 23). Either archive them to `docs/_archive/2026-Q2/` (HIDE) or scrub-and-keep. Recommendation: archive — the named-retailer audience and "[grocer]-* files" pointers don't need to live in active dispatches.

## Files audited

**Total: 48 distinct files, 100% of declared SHOW scope.** Breakdown:
- `docs/sdds/platform/` — 5/5
- `docs/sdds/alx/` — 2/2
- `docs/dispatches/` — 5/7 (excluded `dispatch-solex-*` per HIDE-scope = Solex out of scope)
- `docs/superpowers/briefs/` — 2/2
- `docs/superpowers/specs/` — 11/35 (excluded Canary/Cove/Angel/Seacove/Solex/Foundation/Abalone/PV/poster-prompts/etc per HIDE)
- `docs/superpowers/dispatches/` — 1/5 (excluded canary-login, cove-functional, map-sprint, coac-hoa per HIDE)
- `docs/superpowers/plans/` — 7/27 (excluded all app-named plans per HIDE)
- `Brain/projects/` — 4/9 (Method, Factory, GrowDirect, RetailSpine; excluded Angel, Canary, Cove, Seacove, Secure per HIDE)
- `Brain/method/` — 7/7
- `Brain/wiki/` — 3/N (only growdirect-factory-process + methodology-ibm-{retail-diagnostic,it-architecture-options} are SHOW per scope rules)
- Repo root — 3/3 (`README.md`, `CLAUDE.md`, `SECURITY.md`)

Excluded from audit per HIDE rules: 119 files in `Brain/raw/inbox/`, all `Brain/wiki/canary-*` / `cove-*` / `angel-*` / `secure-*` / `wpbca-*` / `coac-*` / `dao-*` / `ownpv-*` / `lunada-*` / `pv-*` / `foundation-*` / `seacove*` (~110 files), `docs/sdds/{canary,cove,angel,arc,consulting}/`, `docs/_archive/`, app-specific plans/specs/dispatches.

## Sibling-report cross-references

- **Memory-bus / shared-infrastructure inline credentials (M2, M3):** already filed in `docs/audit-2026-04-23/security.md`. Not duplicate-counting them in totals beyond the medium severity for documentation-quality purposes.
- **Kroger benchmark scale gaps (H3, M1):** the *content* of the named benchmark lives in `docs/audit-2026-04-23/enterprise-scale-gap-analysis.md`. The finding here is purely about naming hygiene in the spec doc, not the analytical conclusion.

## Recommended order of operations

1. **J2 + C1 first** — methodology-ibm wiki rewrite. Highest leverage scrub.
2. **H4 partial — `jeffe.io` URL scrub** — three files, mechanical fix.
3. **L1–L48 frontmatter sweep** — mechanical, big footprint, unblocks future audits.
4. **H1, J5 — archive demo dispatches** — one move + one rewrite.
5. **H2 — Secure-to-Canary handoff brief rewrite** — content rework.
6. **H5 — RetailSpine MOC scrub** — light content rework.
7. **J3 — Factory-process wiki SysRepublic split** — judgment call, defer until founder confirms approach.
8. **M4 — Katz playbook rename or archive** — only if file activates.

End of audit.
