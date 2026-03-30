---
name: gitnexus
description: |
  GitNexus code intelligence — consolidated reference for exploring, debugging,
  impact analysis, refactoring, and CLI operations. Use when working with any
  GitNexus-indexed repo. Covers all 6 original sub-skills in one file.
  Deferred until GitNexus MCP is set up at platform level.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# GitNexus — Code Intelligence Reference

GitNexus builds a knowledge graph from your codebase, enabling semantic code
queries, blast radius analysis, safe refactoring, and execution flow tracing.

> **Status:** GitNexus MCP setup is deferred to a future GRO issue. This skill
> serves as the consolidated reference for when it's configured. Currently
> indexed: Canary (7959 symbols, 21644 relationships, 300 execution flows).

## Always Start Here

1. **Read `gitnexus://repo/{name}/context`** — codebase overview + index freshness
2. **Match your task** to a workflow below
3. **Follow the checklist**

> If the index is stale: `npx gitnexus analyze` in terminal.

---

## Tools Quick Reference

| Tool | Purpose |
|------|---------|
| `query` | Find execution flows by concept — "payment processing", "auth validation" |
| `context` | 360-degree symbol view — callers, callees, processes it participates in |
| `impact` | Blast radius before editing — what breaks at depth 1/2/3 |
| `detect_changes` | Git-diff impact — what your current changes affect |
| `rename` | Multi-file coordinated rename with confidence-tagged edits |
| `cypher` | Raw Neo4j-style graph queries |
| `list_repos` | Discover indexed repos |

## Resources (lightweight reads, ~100-500 tokens)

| Resource | Content |
|----------|---------|
| `gitnexus://repo/{name}/context` | Stats, staleness check |
| `gitnexus://repo/{name}/clusters` | All functional areas with cohesion scores |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths |
| `gitnexus://repo/{name}/processes` | All execution flows |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace |
| `gitnexus://repo/{name}/schema` | Graph schema for Cypher queries |

---

## Workflow: Exploring

**Triggers:** "How does X work?", "What's the architecture?", "Show me the auth flow"

```
1. READ gitnexus://repo/{name}/context        → Overview, check staleness
2. gitnexus_query({query: "<concept>"})        → Find related execution flows
3. gitnexus_context({name: "<symbol>"})        → Deep dive on specific symbol
4. READ gitnexus://repo/{name}/process/{name}  → Trace full execution flow
5. Read source files for implementation details
```

---

## Workflow: Impact Analysis

**Triggers:** "What breaks if I change X?", "Is it safe to modify this?", "Blast radius"

```
1. gitnexus_impact({target: "X", direction: "upstream"})  → What depends on this
2. READ gitnexus://repo/{name}/processes                   → Check affected flows
3. gitnexus_detect_changes()                               → Map git changes to scope
4. Assess risk and report
```

### Risk Levels

| Depth | Risk | Meaning |
|-------|------|---------|
| d=1 | **WILL BREAK** | Direct callers/importers — MUST update |
| d=2 | LIKELY AFFECTED | Indirect dependencies — should test |
| d=3 | MAY NEED TESTING | Transitive effects — test if critical path |

### Risk Assessment

| Scope | Risk |
|-------|------|
| <5 symbols, few processes | LOW |
| 5-15 symbols, 2-5 processes | MEDIUM |
| >15 symbols or many processes | HIGH |
| Critical path (auth, payments) | CRITICAL |

**MUST warn the user** if impact analysis returns HIGH or CRITICAL risk.

---

## Workflow: Debugging

**Triggers:** "Why is X failing?", "Trace this error", "This endpoint returns 500"

```
1. gitnexus_query({query: "<error or symptom>"})   → Find related flows
2. gitnexus_context({name: "<suspect>"})           → See callers/callees/processes
3. READ gitnexus://repo/{name}/process/{name}       → Trace execution flow
4. gitnexus_cypher({query: "MATCH path..."})        → Custom traces if needed
```

| Symptom | Approach |
|---------|----------|
| Error message | `query` for error text → `context` on throw sites |
| Wrong return value | `context` → trace callees for data flow |
| Intermittent failure | `context` → look for external calls, async deps |
| Performance issue | `context` → find symbols with many callers (hot paths) |
| Recent regression | `detect_changes` to see what changed |

---

## Workflow: Refactoring

**Triggers:** "Rename this function", "Extract this into a module", "Split this service"

### Rename

```
1. gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})  → Preview
2. Review graph edits (safe) vs ast_search edits (needs review)
3. gitnexus_rename({..., dry_run: false})  → Apply
4. gitnexus_detect_changes()  → Verify scope
5. Run tests for affected processes
```

### Extract/Split

```
1. gitnexus_context({name: target})  → All incoming/outgoing refs
2. gitnexus_impact({target, direction: "upstream"})  → All external callers
3. Define new interface, extract code, update imports
4. gitnexus_detect_changes()  → Verify scope
5. Run tests for affected processes
```

**NEVER** rename symbols with find-and-replace — use `gitnexus_rename`.

---

## CLI Commands

| Command | Purpose |
|---------|---------|
| `npx gitnexus analyze` | Build or refresh the index |
| `npx gitnexus analyze --embeddings` | Include embeddings for semantic search |
| `npx gitnexus status` | Check index freshness |
| `npx gitnexus clean` | Delete the index |
| `npx gitnexus wiki` | Generate documentation from the graph |
| `npx gitnexus list` | Show all indexed repos |

**After committing code:** Re-run `npx gitnexus analyze` to update the index.
If embeddings existed previously, use `--embeddings` to preserve them.

---

## Graph Schema

**Nodes:** File, Function, Class, Interface, Method, Community, Process
**Edges (CodeRelation.type):** CALLS, IMPORTS, EXTENDS, IMPLEMENTS, DEFINES, MEMBER_OF, STEP_IN_PROCESS

```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "myFunc"})
RETURN caller.name, caller.filePath
```

---

## Mandatory Checks

Before completing any code modification in a GitNexus-indexed repo:

1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated
