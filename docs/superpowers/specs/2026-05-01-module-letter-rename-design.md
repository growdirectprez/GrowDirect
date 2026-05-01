---
date: 2026-05-01
type: refactor-spec
status: active
owner: GrowDirect LLC
classification: confidential
related-linear: gd-rename-modules
---

# Module Letter Rename — Canonical Mapping

> **Why now.** The 13-module spine grew its letter assignments incrementally. Some letters are mnemonic (T, F, L, P, D, A, S, Q); some aren't (R for Customer, J for Forecast/Order, W for Work Execution, C for Commercial — which reads "British" in US retail terminology). Renaming costs 3–5 days now or compounds across 1000s of cross-references later. Doing it now.

## Canonical mapping

| Old | New | Module name (new) | Change type |
|---|---|---|---|
| A | A | Asset Management | unchanged |
| C | **M** | Merchandising | letter swap (C→M; reads as US-standard "Merchandising") |
| D | D | Distribution | unchanged |
| F | F | Finance | unchanged |
| J | **O** | Orders | letter swap (J→O; "Forecast & Order" → "Orders") |
| L | L | **Labor** | name shorten (was "Labor & Workforce") |
| N | N | Device | unchanged |
| P | P | Pricing & Promotion | unchanged |
| Q | Q | Loss Prevention | unchanged |
| R | **C** | Customer | letter swap (R→C; takes the C letter freed by C→M) |
| S | S | **Space** | name shorten (was "Space, Range, Display") |
| T | T | Transaction | unchanged |
| W | **E** | Execution | letter swap (W→E; "Work Execution" → "Execution") |

Four letter swaps: **C→M, J→O, R→C, W→E**. Two name-only shortenings: **S, L**.

## Workflow ordering (replaces alpha sort in vault sidebars)

1. **M** — Merchandising
2. **O** — Orders
3. **D** — Distribution
4. **S** — Space
5. **P** — Pricing & Promotion
6. **C** — Customer
7. **T** — Transaction
8. **Q** — Loss Prevention
9. **F** — Finance
10. **A** — Asset Management
11. **N** — Device
12. **L** — Labor
13. **E** — Execution

Reads as: plan (M) → buy (O) → move (D) → place (S) → price (P) → engage (C) → sell (T) → protect (Q) → book (F) → operate (A, N, L, E).

## Execution rules

### Two-stage substitution to avoid letter collision

C is reused: it was Commercial, becomes Customer. R→C must happen *after* C→M, otherwise "Module C" matches the wrong concept.

**Stage 1 — non-overlapping renames:**
- C → M (Commercial → Merchandising)
- J → O (Forecast & Order → Orders)
- W → E (Work Execution → Execution)
- S name shorten ("Space, Range, Display" → "Space")
- L name shorten ("Labor & Workforce" → "Labor")

**Stage 2 — after Stage 1 is applied and verified:**
- R → C (Customer takes the freed C letter)

### Detection rule sub-letters

`Q-C-01` through `Q-C-05` (B2B detection rules, currently tagged with old-C-for-Commercial) → rename to `Q-M-01` through `Q-M-05`. These rules detect commercial-account fraud patterns; they belong to the Merchandising domain, not Customer.

### L3 process IDs

Format `X.Y.Z` (e.g., `T.2.3`, `Q.6.4`). Letter renames cascade:
- C.Y.Z → M.Y.Z (Commercial)
- J.Y.Z → O.Y.Z
- W.Y.Z → E.Y.Z
- R.Y.Z → C.Y.Z (Stage 2 after Stage 1)

Numeric portions unchanged.

## Surfaces touched

- **Brain/wiki/cards/canary-module-*.md** — file renames + content
- **Brain/wiki/canary-module-*.md** — file renames + content
- **Brain/projects/Canary.md** — MOC link updates
- **docs/sdds/canary/ncr-counterpoint-module-*.md** — file renames + content
- **CanaryGo** — letter-keyed constants in code, detection rule ID strings, tests, fixtures
- **NCR vault** (`growdirect-llc/ncr`) — `modules/X-name.md` rename + sidebar order
- **CRB vault** (`growdirect-llc/canary-retail-brain`) — same
- **CATz vault** (`growdirect-llc/catz`) — proof-case cross-refs only (no module folder)
- **Linear** — GRO ticket retitles where module letter appears in title
- **Memory bus** — full re-seed (`seed_standalone.py --drop-first`) after content settles

## Order of operations

1. Brain + SDDs rename (source of truth) — branch `gd-rename-modules`
2. CanaryGo code rename — same branch
3. Three vaults rename — temp clones, push direct to their `main`
4. Merge `gd-rename-modules` to GrowDirect `main` and push
5. Linear ticket retitles
6. Memory bus reseed (auto via post-commit hook + manual `--drop-first` for full rebuild)

## What does NOT change

- File numeric sequences in L3 IDs (only the letter prefix changes)
- Module count (13)
- Q rule sub-letters other than `Q-C-xx`
- Internal CanaryGo package names (`cmd/chirp`, `cmd/fox`, `cmd/customer`, etc. — function-named, not letter-named)
- Detection rule numbering inside each Q-XX-NN family

## Acceptance

The rename is "done" when:
- All three vaults render with workflow-ordered sidebar and new letters/names
- `grep -rn "Module C\|Module R\|Module J\|Module W" Brain/ docs/` returns nothing in current-context references (historical references in sources / archive content can remain)
- `grep -rn "C\.[0-9]\+\.[0-9]\+\|R\.[0-9]\+\.[0-9]\+\|J\.[0-9]\+\.[0-9]\+\|W\.[0-9]\+\.[0-9]\+" Brain/wiki/cards docs/sdds` returns nothing in active L3 IDs
- CanaryGo `go build ./...` passes
- Memory bus reseed completes; `memory_recall("merchandising spine")` returns the renamed M card
