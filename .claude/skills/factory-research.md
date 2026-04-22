---
name: factory-research
roles-primary:[PhD]
roles-assist:[Architect]
stage: research
description: |
  Prior art gathering before blueprint. Queries memory bus for decisions and
  domain context, optionally queries GitNexus for blast radius, Obsidian for
  notes, Firecrawl for external docs. Outputs a context bundle consumed by
  blueprint. All sources are optional — degrades gracefully.
allowed-tools:
  - Read
  - Grep
  - Glob
  - TodoWrite
  - WebSearch
  - WebFetch
---

# factory-research — Prior Art & Context Gathering

Runs between preflight and blueprint. Assembles a context bundle from available
sources so blueprint doesn't start from scratch.

**Announce at start:** "Running factory-research — gathering prior art and context."

## Sources

### 0. Platform Standards (MANDATORY)

Read `~/GrowDirect/CLAUDE.md` and the app's `CLAUDE.md`. This is not optional — it runs every time, even if all other sources are unavailable.

Extract and include in the context bundle:
- **Model standards:** PK type (`Mapped[uuid.UUID]`), timestamp requirements, relationship syntax
- **Auth pattern:** session backend, login methods, role model
- **Config pattern:** env-based classes, no hardcoded secrets
- **Infrastructure:** which databases, which ports, which shared services
- **Hard rules:** no SQLite, no lazy pipes, canonical UUID, etc.

If the app's existing code deviates from the platform standard (e.g., `String(36)` UUIDs in Cove), note the deviation and mark the platform standard as authoritative for new code.

### 1. Memory Bus (optional)

If the memory bus MCP is available:

```
memory_recall(query="[GRO issue title and key terms]", limit=10)
```

Then for domain-specific work:

```
context_assemble(topic="[domain area]", gro_issue="GRO-XXX")
```

If the memory bus is not running (yellow from preflight), skip and note it.

### 2. GitNexus (optional)

If GitNexus MCP is configured and the repo is indexed:

```
gitnexus_impact(symbol="[key function/class mentioned in GRO issue]", depth=2)
gitnexus_query(query="[architecture question from GRO issue]")
```

If not available, skip.

### 3. Obsidian (optional)

If Obsidian MCP is configured:

Search for notes related to the GRO issue domain (architecture decisions,
meeting notes, design discussions).

If not available, skip.

### 4. Firecrawl (optional)

If the GRO issue involves a third-party API (Square, Stripe, etc.) and
Firecrawl MCP is configured:

Crawl the relevant API documentation pages for current specs.

If not available, skip.

## Output

Compile findings into a context bundle:

```markdown
## Research Context for GRO-XXX

### Platform Standards (from ~/GrowDirect/CLAUDE.md)
[PK type, model syntax, timestamps, auth pattern, hard rules]
[App-specific deviations noted with "DEVIATION:" prefix]

### Prior Decisions
[memory_recall results — key decisions related to this work]

### Domain Context
[context_assemble results — architecture, workflows, data models]

### Code Impact
[GitNexus results — what code exists, blast radius]

### External References
[Obsidian notes, API docs — if found]
```

If no sources are available, output:

```
No prior context found. Blueprint starts from scratch.
```

## Key Principle

Every source is independently optional. Research should never block the pipeline.
If all sources fail, blueprint proceeds without context — same as today. Research
adds value when sources are available, but its absence is not an error.
