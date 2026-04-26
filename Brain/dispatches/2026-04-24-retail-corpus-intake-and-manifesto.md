---
title: Dispatch — Retail Corpus Intake and Manifesto Synthesis
type: dispatch
status: open
created: 2026-04-24
updated: 2026-04-24
tags: [dispatch, retail-manifesto, third-branch, corpus-intake, factory-run]
owner: ALX
project: third-branch
related:
  - "[[Brain/raw/inbox/_queue|Corpus Queue]]"
  - "[[third-branch]]"
  - "[[tesco-technical-library]]"
  - "[[intactix-canonical-validation]]"
  - "[[srd-shelf-edge-label]]"
  - "[[Brain/projects/RetailSpine|RetailSpine MOC]]"
  - "[[Brain/projects/Method|Method MOC]]"
---

# Dispatch — Retail Corpus Intake and Manifesto Synthesis

**Governing thesis.** The third-branch thesis has accumulated a 20-year operator
corpus that now spans ~80 files across 9 threads — BroadVision 1998–2000, PwC
e-biz methodology 2000–2003, Pitney Bowes ops 1997–1999, Auto-ID 2002, JDA
Intactix 2003–2005, F&E / Tesco US 2006–2013 (TTL + SRD + TOM six-workstream
+ Aquarius site), Tesco International post-2013, Secure / xBR-replacement
2016–2018, and a JLP outlier. The corpus is queued but not yet in Brain as
properly-framed raw intakes, and the cross-corpus synthesis has not been
lifted out of the founder-autobiography voice into a **declarative retail
manifesto** — a first-principles statement of what retail *is*, what the
industry got wrong, what the canonical looks like, and what GrowDirect does.
This dispatch executes both: corpus → intake in parallel, then intake → manifesto
as the one synthesis pass. Hand-off unit is Linear issue; single owner per batch;
definition of done on every item.

## Scope at a glance

| Track | Output | Input | Owner | Done when |
|---|---|---|---|---|
| **A1** | `Brain/raw/inbox/*.md` intakes for 6 binary uploads (2006-era + 2016/18) | Extracted .txt + .pdf already in outputs/ | ALX + Jess | One intake per source, frontmatter per `raw-intake` template, source path preserved |
| **A2** | `Brain/raw/inbox/*.md` intakes for 7 pre-extracted TOM markdowns | Uploaded .md files with markitdown frontmatter | ALX + Jess | Retagged (drop erroneous `secure` tag, add `f-and-e`, `tom-2006`), moved into inbox, cross-linked as a TOM corpus set |
| **A3** | Bulk intake for 3 folders (BP/, BV Nuggets/, EBiz Def Des Dev/) | 55 legacy binaries in-place under `Brain/raw/inbox/` | Research | Extracted → markdown intakes, clustered by thread, one cluster-level synthesis note per folder |
| **B** | `Brain/wiki/retail-manifesto.md` — declarative retail manifesto, v0.1 | All intakes from Track A + already-processed wikis | Tom (architect) + ALX polish | Governing thesis first paragraph, three-canonical framework rendered as diagram + table, executive summary, brand-voice Big 4 polish, provenance boundary note at top |

## Track A — Raw into Brain

The queue log at `[[Brain/raw/inbox/_queue|_queue.md]]` is the single source of
truth for what is unprocessed. Track A clears that queue in three sequenced
batches. Each batch is one Linear issue. Each intake follows
`[[Brain/templates/raw-intake]]`.

### A1 — Six binary uploads (2026-04-24 first drop)

Source files already extracted to `outputs/` during earlier session work:

| Upload | Extracted at | Thread | Intake destination |
|---|---|---|---|
| `Over Short Reporting Revised.pptx` | `outputs/Over_Short_Reporting_Revised.txt` | Post-F&E / Secure-era LP | `Brain/raw/inbox/secure-over-short-reporting-2016.md` |
| `Property App Overview.ppt` | `outputs/Property_App_Overview.txt` | F&E site / Project Aquarius 2006 | `Brain/raw/inbox/fne-project-aquarius-site-canonical.md` |
| `Oracle Project Costing User Guide.pdf` | `outputs/Oracle_Project_Costing_User_Guide_first10pages.txt` | Reference (supports Aquarius) | `Brain/raw/inbox/oracle-project-costing-r11i-reference.md` (light intake — reference doc, no deep extraction) |
| `2210 updated DS processes[1].ppt` | `outputs/2210_updated_DS_processes.txt` | JLP outlier | `Brain/raw/inbox/jlp-ds-processes-2006-reference.md` (light intake — outlier, cited once as design-era reference) |
| `DV Private Label Food Setup v3.ppt` | `outputs/DV_Private_Label_Food_Setup_v3.txt` | TTL operator-side (workshop) | `Brain/raw/inbox/fne-private-label-food-setup-workshop-2006.md` |
| `Copy of FnE DSD Annual Summary iRED view.xlsx` | `outputs/FnE_DSD_Annual_Summary_iRED_view.txt` | Secure-era DSD analytics | `Brain/raw/inbox/fne-dsd-ired-annual-summary-2018.md` |

**Agent instruction (A1):** For each row, author a raw intake markdown file at
the destination path using the `raw-intake` template. Frontmatter must include
`date: 2026-04-24`, `type: raw`, `source: <original upload path>`, `tags: [...]`
per the thread, `project: third-branch`, `status: unprocessed`. Copy the full
extracted text into the Raw content section. Key takeaways section may be empty
(filled during synthesis). Links to existing knowledge must reference the
`_queue.md` log and the appropriate already-processed wiki.

### A2 — Seven pre-extracted TOM markdowns (2026-04-24 second drop)

The seven files are in the uploads folder with markitdown frontmatter already
present:

- `top-down-design--retail-ops-jb-final.md` (Retail Ops, Golding + Dodd, June 2006)
- `commercial-operating-model-v4.md` (Commercial, Lucy Williams, June 2006)
- `tom-forecast--ordering-v3.md` (Forecast & Ordering, June 2006)
- `tesco-operating-model---finance-ver2.md` (Finance, Lisa Baglin, June 2006)
- `tom-business-model-v15-supply-chain.md` (Supply Chain, June 2006 — OCR failed, 29 lines)
- `copy-of-2018-02-02-eagle-eye-functional-and-non-functional-requirements-v4-0-ns-comments.md` (Eagle Eye Requirements, Feb 2018)
- `copy-of-fne-dsd-annual-summary-ired-view.md` (same iRED data as A1 row 6 — deduplicate)

**Agent instruction (A2):**

1. Move the five June 2006 TOM files into `Brain/raw/inbox/` renamed to a clean
   convention: `fne-tom-2006-retail-ops.md`, `fne-tom-2006-commercial.md`,
   `fne-tom-2006-forecast-ordering.md`, `fne-tom-2006-finance.md`,
   `fne-tom-2006-supply-chain.md`.
2. Rewrite each file's frontmatter: drop the erroneous `tags: [secure]`, replace
   with `tags: [f-and-e, tesco-us, tom-2006, operating-model, <workstream>]`,
   change `project` to `third-branch`.
3. Move the Eagle Eye file to `Brain/raw/inbox/secure-eagle-eye-requirements-2018.md`,
   frontmatter retag to `[secure, sysrepublic, sainsburys-or-secure-customer,
   fraud-detection-requirements]`. Flag the "NS comments" author signature for
   founder identification.
4. Deduplicate the iRED markdown against the A1 intake — keep whichever has more
   content; delete the other.
5. Author a TOM corpus index note at `Brain/raw/inbox/fne-tom-2006-corpus.md`
   that cross-links the five workstream intakes plus the already-in-Brain SRD
   `060623-top-down-design--space--range---display-v04.md`. Note the Supply Chain
   deck is image-heavy and requires visual extraction (flag as open follow-up).

### A3 — Three folder bulks (BP/, BV Nuggets/, EBiz Def Des Dev/)

Folders already sit under `Brain/raw/inbox/`; contents are legacy binaries.

| Folder | Count | Thread | Extraction approach |
|---|---|---|---|
| `BP/` | 46 files (25 .doc + 21 .ppt) | Pitney Bowes ops 1997–1999 | Bulk soffice → markitdown; produce one cluster-level intake (`pitney-bowes-ops-corpus-1997-1999.md`) summarizing the 46 docs by category (AP / AR / EDI / Treasury / Payroll / etc.); per-doc full-text intakes only for the 3–5 most diagnostic files |
| `BV Nuggets/` | 6 files | BroadVision 1999–2000 | Per-doc intakes (corpus is curated, small, high-value); author Christian Saucier noted in frontmatter for each |
| `EBiz Def Des Dev/` | 3 files | PwC e-biz methodology 2000 | Per-doc intakes (only 3 files, each is a major template); PwC authorship noted; link to the 18 PwC/IBM client decks already in Brain |

**Agent instruction (A3):** Use `soffice --headless --convert-to pdf` for .doc
and .ppt, then `markitdown` for clean markdown. For `BP/`, produce **one cluster
intake + 3–5 deep-dives** rather than 46 per-file intakes (the 46 docs are
operationally repetitive and the graph will choke on the per-file noise). For
`BV Nuggets/` and `EBiz Def Des Dev/`, do per-file intakes — these are
curated/small. All intakes follow the `raw-intake` template.

### Track A — Definition of done

- Every queue item has a corresponding `Brain/raw/inbox/*.md` intake (or is
  subsumed into a cluster intake with explicit file list).
- `_queue.md` is updated to mark each processed item with a check-mark and
  link to its intake.
- The five open decisions in `_queue.md` §"Open decisions" are preserved and
  carried forward to Track B as synthesis inputs.
- No loose .txt extraction artifacts in `outputs/` that aren't either (a)
  linked from an intake or (b) explicitly marked for deletion.

## Track B — Retail Manifesto

### Framing

The retail manifesto is **not** `[[third-branch]]`. Third Branch is the
founder's 25-year autobiographical thesis — substrate-and-resubstration as the
load-bearing claim, founder lineage as private provenance. The retail
manifesto is a **sibling artifact** that carries the same architectural claim
but speaks from retail's point of view, impersonally, declaratively, with no
autobiographical thread. It is what we give to a CIO, a strategy partner, a
board member who needs to understand what we believe about retail in one
read.

The manifesto inherits from Third Branch the way a client-facing proposal
inherits from an investor deck: same architectural truth, cleaner voice,
provenance behind the wall.

### Required sections

| § | Section | Contents |
|---|---|---|
| **Opening** | *Governing thesis (first paragraph)* | What retail is. What the industry built instead. What has now changed. What we build. All in one paragraph. No autobiography. |
| **Executive summary** | *What retail is, in one table* | 4-row table: the four canonicals (Site · Merchandising · Planogram · Specification) by master-of-record, by kill-switch relationship, by what they contribute to the shelf-edge-label compile |
| **I** | *The three retail canonicals (or four)* | The RMS / SRD / TTL triangle. Decision point: Site as fourth canonical or sibling-stack. Resolve here. |
| **II** | *The compile target — the shelf-edge label* | Why the label is load-bearing. Two-latency reconciliation. S039 + S101 + CRDM + Storeline. Diagram. |
| **III** | *The ordering gate and the spec gate* | F&E's operating discipline: planogram gates procurement; spec gates pack-copy; supply chain bends to shelf. Without autobiography — just what the discipline is and why it works. |
| **IV** | *What the industry got wrong* | ERP alone is ledger-after-the-fact. Consulting alone is discrete labor. Personalization alone is content-free adjacency. Planogram alone is shelf-without-spec. Each partial truth; none load-bearing alone. |
| **V** | *The substrate change — what 2026 makes possible* | Continuous observation. Sat-denominated attribution. Agent orchestration (MCP-native). The 5-to-10 orders-of-magnitude cost collapse. |
| **VI** | *What GrowDirect is* | The bubble (Canary). The spine (RetailSpine). The agents (MCP over S-prefix). The accounting primitive (sats). The fresh-prep module (TTL-descendant C090). The commercial wedge (LP / Asset Protection). |
| **VII** | *The one-paragraph version* | Same discipline as `[[third-branch]]` §VIII — one paragraph, no autobiography, no "I" voice, speaks in the industry's own vocabulary. |

### Voice rules

- **No first-person.** Third Branch uses "I"; the manifesto does not. "The
  industry." "The retailer." "GrowDirect." "The canonical."
- **No founder biography.** Dates, places, client names, operator-era details
  stay in Third Branch and its companions. Manifesto carries the architecture
  on its engineering merits.
- **Declarative, not reflective.** The manifesto states what retail *is*, not
  what the author *discovered* retail was. Present tense. Active voice.
- **One framework per section.** Either a table or a diagram or a tight
  enumerated claim-set per §. No prose walls.
- **Big 4 polish.** Per CLAUDE.md — governing thesis first paragraph,
  executive summary above the fold, MECE decomposition, opinions land where
  warranted.

### Intake dependencies for Track B

Manifesto synthesis should happen after Track A lands these minimally:

- [x] TTL corpus (`[[tesco-technical-library]]`, already processed)
- [x] Intactix validation (`[[intactix-canonical-validation]]`, already processed)
- [x] SRD SEL interfaces (`[[srd-shelf-edge-label]]`, already processed)
- [ ] A1 row 2 (Project Aquarius / Site canonical) — needed to resolve the
  three-vs-four-canonical decision in §I
- [ ] A1 row 5 (DV Private Label Food Setup v3) — strengthens TTL C090 proposal
  referenced in §VI fresh-prep module
- [ ] A2 TOM corpus index (six-workstream picture) — needed for §III ordering-gate
  and §VI GrowDirect-is framing
- [ ] A3 BV Nuggets cluster — needed for §IV "personalization got to content-free
  adjacency" claim with contemporaneous primary sources

A3 (`BP/`, `EBiz Def Des Dev/`) can land in parallel with manifesto v0.1;
they strengthen §IV but are not blocking.

### Deliverable location

- **Primary artifact:** `Brain/wiki/retail-manifesto.md` (v0.1 on first pass)
- **External-facing variant:** once v0.1 holds up to founder review, author
  a customer-safe version at `docs/positioning/retail-manifesto.md` with
  provenance boundary enforced (no internal wiki links, no Brain references
  outside the footer). This variant is what goes to CATz / CIO conversations /
  investor materials.

## Sequencing

```
T+0   (now)        : Dispatch approved, Linear issues opened
T+0.5 (same day)   : A1 + A2 — six binary uploads + seven markdowns → intakes
T+1   (day two)    : A3 — three folders bulk-processed
T+1.5              : _queue.md drained, checkpoint review with founder
T+2                : Track B kickoff — Retail Manifesto v0.1 drafted
T+3                : v0.1 brand-voice polish + provenance boundary sweep
T+4                : Founder review, v0.2 if required
T+5                : External variant authored from approved v0.2
```

Track A is parallelizable; Track B is linear and depends on A1 + A2 + a subset
of A3. Expect 3–5 calendar days from dispatch approval to manifesto v0.2.

## Definition of done (dispatch level)

1. `Brain/raw/inbox/_queue.md` shows every queue item either processed
   (check-marked with intake link) or explicitly deferred with rationale.
2. `Brain/wiki/retail-manifesto.md` exists at v0.2 or later, passes brand-voice
   enforcement, carries the provenance boundary note.
3. The three-vs-four-canonical decision is **resolved in the manifesto** (not
   deferred) — either Site is inside RetailSpine (the C-prefix catalog grows)
   or Site is sibling (the manifesto cites it and moves on).
4. `[[third-branch]]` has a link to the manifesto in its front-matter
   `related:` block, and the manifesto has a link back to Third Branch in a
   "Companion" sidebar note near the top (one-line, not a prose reference).
5. A customer-safe variant exists at `docs/positioning/retail-manifesto.md`
   with a clean provenance wall.

## Open decisions the synthesis pass must close

Lifted from `_queue.md` §"Open decisions":

1. **Site as fourth canonical vs. sibling-stack** — *resolve in §I of the
   manifesto*
2. **CRDM decade-spanning vs. two-CRDMs reading** — *resolve via founder
   recollection during A1 intake of the 2016 Over/Short deck*
3. **Over/Short + iRED — F&E-provenance or SEG-provenance?** — *resolve
   during A1 + A2 retagging; may remain open if founder cannot disambiguate*
4. **JLP DS-processes doc — cite once or drop?** — *drop unless §IV benefits
   from a contemporaneous "what Tesco was reading" citation; default: drop*
5. **Canary fresh-prep module timing (C090 TTL-descendant canonical)** —
   *resolve via Canary MOC update as part of manifesto §VI*

---

*Source: `[[Brain/raw/inbox/_queue|corpus queue]]` as of 2026-04-24; dispatch
authored against CLAUDE.md delivery-mode standards (governing thesis first,
MECE decomposition, framework-per-section, brand-voice polish). Handoff unit:
Linear issue per batch (A1, A2, A3, B), with this dispatch linked from each
issue body. Owner per batch named in the Scope table. Dispatch becomes
reference material (not deliverable) once all five definition-of-done items
are green.*
