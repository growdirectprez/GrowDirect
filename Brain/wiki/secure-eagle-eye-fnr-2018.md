---
date: 2026-04-23
type: wiki
tags: [secure, eagle-eye, requirements, functional, non-functional, user-stories, ns-comments, 2018]
sources:
  - Brain/raw/inbox/copy-of-2018-02-02-eagle-eye-functional-and-non-functional-requirements-v4-0-ns-comments.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Eagle Eye — Functional & Non-Functional Requirements v4.0 (Feb 2018, NS Comments)

## Summary

**Eagle Eye requirements workbook** dated **2 February 2018**, version 4.0, with inline review comments from NS (Nick Stinde — then-Secure product leader). A full functional + non-functional requirements catalogue in modern agile user-story format, used as a working review artefact during the Eagle Eye product scoping phase.

## Structure

Each requirement row carries the following fields (consolidated from the spreadsheet's multi-header layout):

| Field | Purpose |
|---|---|
| Req ID | Unique requirement identifier |
| Updated in version | Version-tracking for change history |
| Functional Area | Category grouping |
| Requirement | Short title |
| Description (As a… I want) | Agile user-story form of the requirement |
| Rationale (so that…) | The "why" — value delivered |
| Acceptance Criteria (inc. key Business Controls) | Testable pass conditions |
| Comments | Working-draft notes |
| Solution | Proposed implementation approach |
| **NS Comments / Questions to JB/GL/DL** | Review feedback from Nick Stinde, directed at JB / GL (Geoffrey Lyle) / DL |
| Priority | Business priority ranking |
| Current or New Requirement | Carry-over vs. fresh |
| In or Out of scope | Binary scope flag |
| Status | Workflow status |
| Owner | Accountable individual |
| Raised By | Originator |
| Origin | Source document / meeting / stakeholder |
| Solution Type | Architecture categorisation |
| Notes | Free-form |
| Associated NFR's ID | Cross-reference to non-functional requirements |
| Related Requirements | Requirement graph edges |
| Change | Change-control tracking |
| System | Target system |
| Workstream | Project workstream |
| Keywords | Taxonomy tags |
| Related Documents | Links |
| Customer Data | Data handled |
| High Level Requirement | Parent requirement |
| Functional Design Use case | Design-artefact reference |
| Business Process Ref. | Process-doc reference |
| Solution design | Design-doc reference |
| Technical Design | Technical-doc reference |
| UAT Scenario | Test-case reference |
| Test Completion Report | Test-evidence reference |

## Why So Many Columns

This is a **traceability matrix crossed with a user-story catalogue**. The leftmost columns capture the requirement in the modern "As a… I want… so that…" user-story form. The middle columns manage scope + prioritisation + status. The rightmost cluster provides end-to-end traceability from requirement → use case → business process → solution design → technical design → UAT → test completion.

Sysrepublic adopted this format in the 2016–2018 era when Eagle Eye was being scoped against enterprise customers who demanded SDLC-grade traceability for audit. The `NS Comments / Questions to JB/GL/DL` column is the living-document annotation track — Nick Stinde's review feedback is captured per-row rather than as a separate review doc.

## Why This Matters

- **Format precedent.** The Eagle Eye requirements workbook is a good template to reference for any future SDD or PRD that needs traceability. The column set covers requirement definition → scope → prioritisation → design → test — everything an auditor asks for, and everything a product team needs to manage change.
- **Archaeology of Secure product line.** Eagle Eye was a Sysrepublic product line distinct from Secure Store EBR. The requirements here define what Eagle Eye aimed to deliver that Secure Store EBR did not.
- **GL (Geoffrey Lyle) attribution.** Several requirements route questions directly to GL, confirming Jeffe's active role in the review chain.

## Open Items Flagged for Session Review

This wiki card captures the *structure* of the workbook. Individual requirement contents (all 100+ rows across multiple functional areas) are preserved in the full source xlsx at the path in frontmatter. A deeper synthesis pass could extract specific requirement themes (e.g., analytics, alerting, reporting) into standalone wiki cards if they surface high-value lineage for Canary. Left for a later-session decision.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-sysrepublic-xbr-2016|Sysrepublic xBR Response (2016)]] — earlier sibling requirements doc
- [[Brain/wiki/secure-architecture|Secure Architecture]]
- [[Brain/projects/Canary|Canary]] — forward lineage

## Sources

- `Brain/raw/inbox/Copy of 2018.02.02 Eagle Eye Functional and Non-Functional Requirements v4.0 NS Comments.xlsx` — Eagle Eye FR/NFR workbook v4.0 with NS review comments, 2 Feb 2018

Extraction path: `.xlsx` → markitdown.
