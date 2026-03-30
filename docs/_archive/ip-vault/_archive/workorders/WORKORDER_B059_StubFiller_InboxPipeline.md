---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order B-059: War Chest Stub Filler + Eva Inbox Pipeline

**Created:** February 27, 2026
**Owner:** ALX
**Sprint:** 6 (Track 2 — no heavy code)
**Priority:** 🟡 HIGH — 20 stubs need filling before Gold Build

---

## Context

War Chest v3.0 restructure is complete. 43 source files, renumbered to match Pitch Spine v0.4. 21 are written. 20 are stubs. 1 is a gap (ISS-002, The Ask). Each stub names its Manifesto section, its source material, and what needs extraction.

This work order has two phases:
- **Phase 1 (now):** Fill the 20 stubs from existing source material. No new research needed — the content exists in the Manifesto and agent deliverables. This is extraction and formatting, not writing.
- **Phase 2 (future):** Build the Eva inbox pipeline — drop a file, Eva routes it, asks clarifying questions, weaves it into the knowledge base.

---

## Phase 1: Stub Filler

### What It Does

For each stub file in `_ALX/WarChest/sources/`:

1. **Read the stub** — extract the Manifesto section tag(s) and source reference(s)
2. **Read the Manifesto section** — pull the prose from `GrowDirect_Manifesto_v1.0.md`
3. **Read the source document(s)** — pull from the referenced agent deliverables (PhD briefs, Condor PRDs, Strategic Thesis, Addendum, etc.)
4. **Draft investor-grade prose** — not internal notes, not raw Manifesto text. Polished, clear, investor-facing language. One source file = one topic = one clear argument.
5. **Output the draft** to the same source file path, replacing the stub
6. **Update manifest.json** status from `"stub"` to `"draft"`

### Execution Model

- **One stub at a time.** Fill one. Review. Approve. Move to next.
- **Agent:** Any agent can fill a stub — Jeremy for tech sections (20-23), PhD for thesis sections (10-16, 31-32), Eva for product sections (05, 37-38), ALX for operational (00, 42).
- **Approval:** Jeffe reviews each filled stub before status moves from `"draft"` to `"written"`.
- **Local-first option:** This is ideal for Qwen or any local model. The task is: read two documents (Manifesto section + source reference), produce one document (investor-grade prose, 500-2000 words). No API calls needed. No code. Just text extraction and polishing.

### Stub Fill Order (suggested)

Priority order based on what's closest to having full source material:

| Priority | File | Why First |
|---|---|---|
| 1 | `05-the-chirp.md` | Content fully in Manifesto III.3. Simple extract. |
| 2 | `10-the-pool.md` | Content fully in Manifesto IV.1 + Addendum. |
| 3 | `11-the-notary.md` | Content fully in Manifesto IV.2 + Addendum. |
| 4 | `12-the-gate.md` | Content fully in Manifesto IV.3 + Addendum. |
| 5 | `13-the-scale.md` | Content fully in Manifesto IV.4 + Addendum. |
| 6 | `14-the-mining-moat.md` | Content fully in Manifesto IV.5 + PhD Layer5. |
| 7 | `15-the-network.md` | Content fully in Manifesto IV.6 + Addendum. |
| 8 | `16-the-vision.md` | Content fully in Manifesto IV.7 + Addendum. |
| 9 | `21-triple-subscriber.md` | Content in Condor PRDs TSP-01 through TSP-09. |
| 10 | `22-the-pipe.md` | Content in Sprint 6 WO B-052 + Manifesto V.4. |
| 11 | `23-the-l402.md` | Content in Condor TSP-07 + Manifesto V.5. |
| 12 | `31-genesis-pool.md` | Content in PhD GenesisPool thesis + Manifesto VI.2. |
| 13 | `32-fee-window.md` | Content in PhD FeeWindowModel + Manifesto VI.3. |
| 14 | `33-the-patent.md` | Content in Manifesto VI.4 + provisional filing. |
| 15 | `37-projections.md` | Content in WP-4.4 (now 36-revenue.md). Needs split. |
| 16 | `38-the-rollout.md` | Content in Strategic Thesis + Manifesto VII.5. |
| 17 | `41-why-now.md` | Content in Strategic Thesis + Manifesto VIII.4. |
| 18 | `42-sovereignty.md` | NEW CONTENT — needs writing from Jeffe's vision (this session). |
| 19 | `01-founders-case.md` | Partially blocked by B-056 (evidence hunt). Draft can proceed. |
| 20 | `00-the-demo.md` | Blocked by Sprint 6 Track 1 (protocol pipe must work). |

### Source Material Paths

| Source Document | Path |
|---|---|
| Manifesto | `Canary_IP/Markdown/Strategy/GrowDirect_Manifesto_v1.0.md` |
| ElJeffe Business Model Addendum | `_ALX/ElJeffe_BusinessModel_Addendum.md` |
| PhD tLogToGlog | `_ALX/WorkOrders/output/PhD/tLogToGlog_FounderCase_v1.0.md` |
| PhD Layer5 GenesisPool | `_ALX/WorkOrders/output/PhD/PhD_Layer5_GenesisPool_CapitalThesis.md` |
| PhD Layer5 FeeWindow | `_ALX/WorkOrders/output/PhD/PhD_Layer5_FeeWindowModel.md` |
| PhD Layer5 TrustCollapse | `_ALX/WorkOrders/output/PhD/PhD_Layer5_TrustCollapsisThesis.md` |
| PhD B053 Compliance | `_ALX/WorkOrders/output/PhD/PhD_B053_ComplianceByConstruction_Brief.md` |
| PhD Brief5 v2.0 | `_ALX/WorkOrders/output/PhD/PhD_B054_Brief5_TlogToGlog_v2.0.md` |
| Condor PRDs | `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/` |
| Strategic Thesis | `Canary_IP/Markdown/Strategy/` (locate exact file) |
| Sprint 6 Work Order | `_ALX/WorkOrders/WORKORDER_B052_Sprint6_ParallelTracks.md` |
| Syd B-058 Legal Review | `_ALX/WorkOrders/output/Syd/` (locate exact file) |

---

## Phase 2: Eva Inbox Pipeline (FUTURE — stub spec only)

### Vision

Drop a file into an inbox folder. Eva picks it up, asks clarifying questions, and weaves it into the knowledge base. The knowledge base grows by ingestion — not by manual editing.

### How It Would Work

```
1. FILE DROP
   └─ User drops a file into: _ALX/WarChest/inbox/
   └─ Any format: .md, .pdf, .docx, .txt, .html, screenshot, transcript

2. EVA TRIAGE
   └─ Eva reads the file
   └─ Eva asks (via AskUserQuestion or chat):
      • "What is this?" (if not obvious from content)
      • "Which Manifesto section does this advance?" (suggests best match)
      • "Who produced it?" (agent attribution)
      • "Is this investor-facing or internal?"
   └─ Eva classifies: { manifesto_section, source_file, audience, action }

3. EVA ROUTES
   └─ If content updates an existing source: Eva drafts the update, shows diff, asks for approval
   └─ If content is new and doesn't map to existing source: Eva flags it for ALX routing
   └─ If content is evidence (photos, emails, docs): Eva files to reference library, tags Manifesto section

4. EVA UPDATES
   └─ Source file updated (or new content appended with separator)
   └─ manifest.json status updated
   └─ Manifesto Section Index status updated
   └─ HANDOFF.md updated with "Eva ingested [file] → [source]. Jeffe review needed."

5. JEFFE APPROVES
   └─ Nothing moves from "draft" to "written" without Jeffe review
```

### Technical Requirements (when built)

- File watcher on `_ALX/WarChest/inbox/` (could be cron, could be MCP, could be manual trigger)
- Eva agent profile needs standing instruction for inbox triage
- PDF/DOCX text extraction (already available via skills)
- Diff preview before any source file is modified
- Manifesto section matching (fuzzy match against Section Index)

### Not Building Yet Because

- Phase 1 (stub filling) is the immediate need
- The inbox pipeline is a Sprint 7+ capability
- Need the first full version of the War Chest (all stubs filled, all outputs rebuilt) before automating ingestion
- B-030 Phase 2 (filesystem cleanup + inbox) is the existing tracker for this work

---

## Acceptance Criteria

### Phase 1
- [ ] All 20 stubs filled with investor-grade prose
- [ ] Each filled stub reviewed and approved by Jeffe
- [ ] manifest.json status updated for each filled source
- [ ] Manifesto Section Index updated to reflect source completion
- [ ] No stub references any content that doesn't exist yet (no forward references)

### Phase 2 (future)
- [ ] `_ALX/WarChest/inbox/` directory exists
- [ ] Eva can triage a dropped file and suggest routing
- [ ] Source file updates require Jeffe approval before committing
- [ ] manifest.json and Manifesto Section Index auto-update on approval

---

## Blocker Registration

| ID | Description | Severity | Notes |
|---|---|---|---|
| B-059 | War Chest stub filling + inbox pipeline | 🟡 HIGH | Phase 1 gates Gold Build. Phase 2 is Sprint 7+. |

---

*Work order filed by ALX, February 27, 2026.*
*Manifesto tag: feeds all War Chest outputs.*
