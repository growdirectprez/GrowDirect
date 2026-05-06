---
type: dispatch
status: ready-to-dispatch
date: 2026-04-25
target: claude-code-session (engineer agent, fresh)
priority: medium
unblocks: CATz Phase III delivery framework + engagement-shape differentiation + agreements / artifact templates
parallel-with: 2026-04-25-rapid-pos-deep-dive.md
companion-pattern: docs/playbooks/playbook-method-katz-reverse-engineer.md
tags: [catz, engagement-archive, sysrepublic-era, sanitization, content-engine-ingest]
---

# Dispatch — Secure Engagement Archive → CATz Phase III

A separate Claude Code session ingests 11 engagement-archive
documents from the founder's Sysrepublic / Secure-era external
drive, extracts the structural pattern from each, and lands
sanitized templates in CATz. Goal: fill the Phase III delivery
side of CATz that today is thin.

Companion pattern: same as
`docs/playbooks/playbook-method-katz-reverse-engineer.md` (extract
structural discipline, strip client/product/lineage references,
land in external vault). Same rules apply.

## Why

Today CATz has Phase I (assess & design) and Phase II (select &
implement) as workstream lists. Phase III (deploy & operate, the
100-day-plan side) is a gap. The founder's prior career
(Sysrepublic / Secure 2017 era) ran a tight, recognizable
version of the 100-day deployment shape. The artifacts that
governed it are on a backup drive. Mining them produces:

- Phase III as a real phase, not a placeholder
- Engagement-shape differentiation (on-premise vs SaaS)
- Concrete artifact templates (resource plan, baseline plan,
  data flow, requirements survey, engagement timeline)
- Contract templates (engagement schedule, SaaS order form)
- A delivery framework that captures cadence, gates, escalation,
  sign-off discipline

These aren't reinvention. They're 25-year-refined patterns the
founder operated. The mining surfaces the structure; the
sanitization removes prior-client / prior-product traces.

## Source corpus (11 documents)

Located at `/Volumes/My Passport/macpro/Users/geoff/Documents/`
(external drive — must be mounted at runtime). One additional
document at `/Volumes/My Passport/CLIENTS/DELIVERY/`.

| # | Source file | Type | Structural pattern to extract |
|---|---|---|---|
| 1 | `Schedule D Secure Service 2-7-17 GLyle Edits.doc.docx` | Contract clause | Engagement scope-of-work / schedule structure |
| 2 | `Secure Engagement Overview - On Premise.doc` | Engagement frame | On-premise engagement overview shape |
| 3 | `Secure SaaS Order Form (Template) gcl comments 3-9-17.docx` | Contract template | SaaS commercial order form |
| 4 | `SolutionRequirementsSurvey_20170328.docx` | Pre-deployment instrument | Requirements survey questions + structure |
| 5 | `BaseLine Case Plan.pdf` | Project plan | Generic baseline case plan structure |
| 6 | `Secure 3.5 Baseline Plan.pdf` | Project plan | Product-versioned baseline plan structure |
| 7 | `Secure 3.5 Resource Plan.pdf` | Resource model | FTE × week allocation pattern |
| 8 | `Secure Data Flow.pdf` | Architecture | Data flow diagram pattern |
| 9 | `Taco Bell Secure 3.5 Timeline.pdf` | Engagement timeline | 100-day timeline shape (per-client instance) |
| 10 | `Taco Bell Secure Resource Plan.pdf` | Resource allocation | Per-client resource shape (companion to #7) |
| 11 | `/Volumes/My Passport/CLIENTS/DELIVERY/Delivery Framework v1 2.pdf` | Delivery discipline | Cross-engagement delivery framework |

## Sanitized output map

Each source produces one or more CATz artifacts. Numbers
correspond to the source list above.

| Source | Sanitized output path in CATz |
|---|---|
| 1 | `agreements/engagement-schedule-template.md` (rename "Schedule D" if the letter is product-specific) |
| 2 | `method/engagement-shapes/on-premise.md` |
| 3 | `agreements/saas-order-form-template.md` |
| 4 | `method/artifacts/solution-requirements-survey.md` |
| 5, 6 | merged → `method/artifacts/baseline-plan-template.md` |
| 7, 10 | merged → `method/artifacts/resource-plan-template.md` |
| 8 | `method/artifacts/data-flow-template.md` |
| 9 | `method/artifacts/engagement-timeline-100-day-template.md` |
| 11 | `method/delivery-framework/overview.md` + supporting docs as the framework dictates |

Plus a NEW Phase III article:

`method/phases/phase-3-deploy-and-operate.md` — the 100-day
deployment phase as a peer to Phase I + Phase II. Synthesized
from #5–11; structures the workstreams that run during a
deployment (kickoff / baseline / configuration / data-load /
training / acceptance / cutover / post-cutover stabilization).

## Scrub rules — forbidden in sanitized output

The following must NEVER appear in CATz vault content produced
by this dispatch. Engineer agent runs a final grep before
proposing each artifact for merge.

**Prior product / company names:**
- `Sysrepublic`, `Secure` (as product name; `secure` as adjective is fine), `Appriss`, `Appriss Retail`, `Tri-Tech`, `Sysrepublic Retail`
- `Secure Service`, `Secure Store`, `Secure 3.5`, any version-specific product references

**Prior clients:**
- `Taco Bell` and any other client name appearing in the source files
- Specific store identifiers, location IDs, or merchant-specific tokens

**Prior personnel:**
- Any personal name appearing in a source file's authoring metadata, "Reviewed by" line, or commentary, except `Geoffrey C. Lyle` (the founder, in an authoring-credit context only)

**Internal artifacts:**
- File path references to the external drive
- Internal version numbers tied to the source product (Secure 3.5, etc.)
- Specific deployment topology details that read as the prior product's architecture

**Generic permitted abstractions:**
- "the 100-day deployment" / "the deployment phase"
- "the platform vendor" / "the platform"
- "the customer" / "the engaged retailer"
- Schedule structure (whatever generic letter or naming GrowDirect uses)
- Generic role names (Project Manager, Solution Architect, Configuration Lead — these are common and not prior-product-specific)

## Internal source-of-record

Sanitized templates land in CATz. Original source provenance
records as an internal-only Brain article:

`Brain/wiki/founder-context-secure-engagement-archive.md`

Contents:
- Source file inventory with original paths
- What each contributed to the sanitized CATz output
- Founder context (HIDE scope) — the engagement model, the era,
  the deployment patterns
- Cross-reference: maps each CATz artifact back to its source
  for future provenance lookups

This file is HIDE scope — never externalized. Stays in
GrowDirect/Brain/wiki/ as ALX's memory-bus context for
"explaining where the methodology came from" when relevant.

## Engineer agent operating procedure

1. Verify the external drive is mounted at
   `/Volumes/My Passport/`. If not, request founder mount it
   before proceeding.

2. For each source document:
   - Read the file (use `markitdown` for binary formats; for
     PDF, use `pdftotext` or equivalent extraction)
   - Identify the structural pattern (sections, fields,
     tables, decision points)
   - Map specific content to the abstract pattern (what's
     prior-client-specific, what's prior-product-specific,
     what's structurally generic)
   - Draft the sanitized template per the output map above

3. After each draft:
   - Run forbidden-name grep against the draft
   - Verify zero hits before proposing for merge
   - Cross-check: does the structural pattern survive the
     sanitization, or did stripping the names hollow it out?
     If hollowed, return for revision.

4. Produce the internal-only provenance article
   (`Brain/wiki/founder-context-secure-engagement-archive.md`)
   capturing source-to-output mapping.

5. Founder reviews each sanitized artifact before merging into
   CATz main. Founder reviews the internal provenance article
   before merging into Brain.

## Acceptance criteria

- [ ] All 11 source documents read and structurally analyzed
- [ ] 11+ sanitized CATz artifacts produced per the output map
- [ ] New `method/phases/phase-3-deploy-and-operate.md` article
      synthesized
- [ ] Internal `Brain/wiki/founder-context-secure-engagement-
      archive.md` produced with source-to-output mapping
- [ ] Forbidden-name grep clean on all CATz outputs (zero hits)
- [ ] Founder review pass on each artifact before merge
- [ ] Memory-bus ingestion of the new wiki articles
- [ ] Dispatch closes with a one-page summary of what's now in
      CATz that wasn't before

## Dependencies + parallelism

- Independent of the RAPID POS deep-dive dispatch
  (`2026-04-25-rapid-pos-deep-dive.md`). Can run in parallel.
- Independent of ALXjr's Quartz setup. Can run in parallel.
- Memory-bus ingestion order doesn't matter; both dispatches'
  outputs are additive.
- The new Phase III article and delivery framework will inform
  ALXjr's Engagement 2 (Boutique H&G chain) Phase II → Phase III
  scope — so this dispatch landing IMPROVES ALXjr's output but
  doesn't block it.

## Estimated time

- Per-document extraction + sanitization: 30-60 min each (11 docs
  = ~5-10 hours)
- Phase III synthesis: 1-2 hours
- Internal provenance article: 30 min
- Founder review pass: variable, founder-driven

Total engineer time: 6-12 hours. Suitable for a single
sustained subagent dispatch with checkpoints after each
document.

## Out of scope

- Do not modify the original source files on the external
  drive. Read-only.
- Do not reproduce client engagement specifics (timelines,
  pricing, resource counts) — abstract the shape, not the
  numbers.
- Do not infer detail not present in the source. If a template
  has gaps, mark them as gaps, don't invent fill.
- Do not rewrite Schedule D contract clauses to be legally
  binding GrowDirect agreements. Templates here are
  *structural* — actual legal review happens elsewhere when
  contracts execute.

## Related

- `docs/playbooks/playbook-method-katz-reverse-engineer.md` — the
  companion pattern for the Katz 2003 archive
- `Brain/dispatches/2026-04-25-rapid-pos-deep-dive.md` —
  parallel corpus-mining dispatch (different goal)
- `CATz/method/overview.md` — the method this fills
- `CATz/method/phases/` — destination for the new Phase III
  article

---

**Dispatch author:** Founder via Claude Code, 2026-04-25
**Executor:** Claude Code session (engineer agent)
**Review gate:** Founder reviews each sanitized artifact before
merge to CATz main; founder reviews internal provenance article
before merge to GrowDirect Brain
