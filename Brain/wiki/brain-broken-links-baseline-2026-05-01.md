---
tags: [brain, health, broken-links, baseline, vault-maintenance, link-checker, false-positive]
last-compiled: 2026-05-01
needs-review: 2026-08-01
related: [agent-card-format, canary-go-portal]
---

# Brain — Broken-Links Baseline (2026-05-01)

> **Governing thesis.** The obsidian-mcp `find_broken_links_tool` reports **1,982 broken-link references** across the Brain wiki. After categorization, **62% are link-checker false positives** (target files exist somewhere in the vault but the checker doesn't resolve cross-directory references the way Obsidian's native renderer does). The actual missing-target count is **156 unique files**, of which a majority are deliberate forward-references (planned cards in cove/coac/foundation governance work) or cross-vault references (CRB-resident files). **Real cleanup work scoped to ~30-50 entries**, not 1,982. This card is the categorization baseline so future link-health audits start from accurate ground truth.

## Method

Source: `mcp__obsidian__find_broken_links_tool` against `Brain/wiki/` directory, run 2026-05-01.

Categorization steps:

1. Extract unique broken-link target basenames from the report (430 unique).
2. Build set of all `.md` filenames across the vault (Brain + docs, excluding `raw/`, code dirs, transient clones) — 1,062 files.
3. Set difference: targets that exist somewhere vs targets that don't.
4. For real-missing targets, manually inspect to identify category (forward-reference, typo, cross-vault, code-file-conflated, genuinely-needed).

## Headline counts

| Metric | Value |
|---|---|
| Total broken-link references | 1,982 |
| Affected source notes | 255 |
| Unique broken-link target basenames | 430 |
| Targets that exist somewhere (link-checker false positive) | **266 (62%)** |
| Targets that do NOT exist anywhere (real missing) | 156 (38%) |

## Why so many false positives

The obsidian-mcp link checker resolves wikilinks within a directory scope. When `Brain/wiki/canary-go-endpoint-library.md` references `[[tier-stream]]`, the checker looks for `Brain/wiki/tier-stream.md` — which doesn't exist. But Obsidian's native renderer searches the entire vault and finds `Brain/wiki/cards/tier-stream.md` (which does exist). The renderer succeeds; the checker fails.

**Examples:**

| Target | Checker says | Vault reality |
|---|---|---|
| `tier-stream.md` | 21 broken refs | Exists at `Brain/wiki/cards/tier-stream.md` |
| `tier-reference.md` | 23 broken refs | Exists at `Brain/wiki/cards/tier-reference.md` |
| `platform-thesis.md` | 18 broken refs | Exists at `Brain/wiki/cards/platform-thesis.md` |
| `microservice-architecture.md` | 4 broken refs | Exists at `docs/sdds/go-handoff/microservice-architecture.md` |
| `pos-adapter-substrate.md` | several refs | Exists in BOTH `docs/sdds/canary/` and `docs/sdds/go-handoff/` |

These render perfectly in Obsidian. The checker can't see them.

## Real missing — categorized

Of the 156 truly missing targets:

| Category | Count | Disposition |
|---|---|---|
| **Forward-references to planned cards** (cove/coac/foundation governance + bylaws + historical docs) | ~80 | Author when timing is right; this is intentional roadmap not error |
| **CRB-resident cards** (exist in `growdirect-llc/canary-retail-brain` repo, not in local Brain) | ~25 | Cross-vault references; document as expected behavior |
| **Code-file references** (`tools.py`, `evidence_chain.py`, `*.manifest.yaml`) | ~10 | Not actually wiki links; checker conflates with markdown links |
| **Typos / wrong paths** | ~5 | Fix surgically (one fixed in this commit: `canary-module-m-merchandising.md` had `../platform/RetailSpine` should be `../projects/RetailSpine`) |
| **Genuinely-needed concepts not yet authored** | ~30 | Author opportunistically when adjacent work surfaces them; this commit creates `canary-canonical-positioning.md` (referenced 3x) |
| **Empty / malformed targets** (e.g., `""`, `.md` with no filename) | ~7 | Edit source to remove the malformed link |

## Quick wins applied in this commit

1. Fixed wrong-path typo in `canary-module-m-merchandising.md` line 85: `../platform/RetailSpine` → `../projects/RetailSpine`.
2. Created stub: `canary-canonical-positioning.md` (referenced 3x — anchors the founder-locked WHO/WHAT/HOW positioning statement, ties to memory `project_canary_canonical_positioning`).

## Out of scope for this baseline

- Bulk cleanup of cove/coac/foundation forward-references — these belong to a future governance-content authoring pass when the founder is ready to write those cards.
- Cross-vault reference cleanup — references from Brain to CRB-resident content are expected; the three-vault architecture is intentional.
- Code-file reference cleanup — these are markdown links to source files (e.g., `[evidence_chain.py](path/to/evidence_chain.py)`), not wiki links; the checker is mis-categorizing them.
- Re-running the link checker after fixes — the false-positive count won't drop materially without changes to the checker itself.

## Operating principle going forward

**The headline number from `find_broken_links_tool` is misleading.** When evaluating Brain link health:

1. Run the checker
2. Categorize: `comm -23 <broken-targets> <full-vault-basenames>` to find actual-missing
3. Report the real-missing count, not the raw broken-link count
4. Focus cleanup on the genuinely-needed concepts; accept the rest

## Methodology for future audits

```bash
# 1. Run the link checker against Brain/wiki
# 2. Build full-vault basename set
find /Users/gclyle/GrowDirect -name "*.md" \
  -not -path "*/raw/*" -not -path "*/.git/*" \
  -not -path "*/Cove/*" -not -path "*/Canary/*" -not -path "*/Seacove/*" \
  | awk -F'/' '{print $NF}' | sed 's/\.md$//' | sort -u > /tmp/full_vault_basenames.txt

# 3. Extract unique broken target basenames from the report
jq -r '.broken_links[].broken_link' "$REPORT" | \
  awk -F'/' '{print $NF}' | sed 's/\.md$//' | sort -u > /tmp/broken_basenames.txt

# 4. Set difference reveals real-missing
comm -23 /tmp/broken_basenames.txt /tmp/full_vault_basenames.txt
```

Sub-30 minutes from raw report to actionable real-missing list.

## See also

- [[agent-card-format]] — vault discipline that minimizes future link rot
- [[canary-go-portal]] — main MOC (the most-linked-to article in the wiki)
- Tool: `mcp__obsidian__find_broken_links_tool` — the source of the raw report
- Memory: `feedback_no_volatile_data_in_wiki` (relevant — broken-link counts ARE volatile, hence the dated baseline)
