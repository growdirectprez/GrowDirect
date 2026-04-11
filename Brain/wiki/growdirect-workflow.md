---
date: 2026-04-11
type: wiki
tags: [platform, workflow, operations, agents, knowledge]
sources: [CLAUDE.md, Brain/wiki/document-management.md, feedback-memories]
last-compiled: 2026-04-11
---


**Wiki:** [[Brain/Home|Home]]

# GrowDirect Workflow

GrowDirect is a solo-founder operation (Lyle) building four SaaS products with two AI agent systems. Neither system has full context on its own. This article is the operating manual — how sessions work, what they can see, and how knowledge flows between them.

Companion article: [[Brain/wiki/document-management|Document Management Strategy]] covers where files go. This article covers how we actually work.

---

## The Two Agent Systems

### Claude Code (Terminal)

Builds software. Runs in the terminal with full filesystem and Docker access.

**Skills:** Factory pipeline in `.claude/skills/` — blueprinting, TDD, assembly, QA, shipping. Each app (Canary, Cove) has project-specific variants.

**MCP access:** Memory Bus (session decisions, vector recall on port 8003), Cove Knowledge (legal document search).

**No access to:** Linear, Gmail, Canva, Figma.

**Persistence:** Feedback memories in `.claude/projects/` survive across sessions. Memory Bus stores session decisions in PostgreSQL with vector indexing.

### Cowork (Desktop)

Strategizes, writes content, manages operations. Runs as a desktop app with plugin skills.

**Skills:** Superpowers plugin — brainstorming, presentations, spreadsheets, legal review, marketing, engineering, contract review, SEO.

**MCP access:** Linear (task management), Gmail, Canva (design), Figma.

**No access to:** Memory Bus, Cove Knowledge MCP, `.claude/skills/`.

**Persistence:** None across sessions. Cowork starts fresh every time.

### The Gap

These systems do not share memory. Claude Code cannot read Cowork's conversation history. Cowork cannot query the Memory Bus. A decision made in a Claude Code session is invisible to Cowork unless it reaches Brain.

---

## Knowledge Layers

Five layers hold different kinds of knowledge. Understanding what each agent can see prevents duplicate work and missed context.

| Layer | What it holds | Claude Code | Cowork |
|-------|--------------|:-----------:|:------:|
| **CLAUDE.md** | Agent rules, standards, constraints | Yes | Yes |
| **Brain** | Curated domain knowledge, wiki articles, MOCs | Yes | Yes |
| **Memory Bus** | Session decisions, findings, architecture notes | Yes | No |
| **Knowledge Chunks** | Legal document search (WPBCA CC&Rs, deeds) | Yes | No |
| **GitNexus** | Code intelligence graph (symbols, flows) | Deferred | No |

**Brain is the bridge.** It is the only knowledge layer both systems can read. When a Claude Code session produces a decision worth keeping, it should be distilled into a Brain wiki article so Cowork sessions can access it. When a Cowork session produces strategy or research, it goes into Brain so Claude Code sessions can build from it.

**CLAUDE.md is the rulebook.** Both systems read it at session start. It holds hard constraints (tech stack, code standards, Docker rules) and session discipline. Brain holds domain knowledge; CLAUDE.md holds operational rules.

---

## Working Style

These principles come from real sessions. Every one exists because a session violated it and burned tokens.

**Build, don't organize.** If a session produces folders and configs but no running code, it failed. One working feature beats ten planned ones.

**One deliverable per session.** Scope to something that can be committed and verified. "Organize all docs" is not a deliverable. "Get Canary login working" is.

**Iterate with what you have.** Don't ask for better source material, higher-res scans, or DWG files. Work with what exists. It might take 150 passes — that's fine. The iteration is the process.

**Verify before claiming broken.** Read current files before asserting something doesn't work. Don't repeat error numbers from a previous session or old validation script without re-checking. If you don't know the current state, say "let me check."

**Flag dependency changes.** Never silently add packages. Tell the user, get approval, commit the change, rebuild the Docker image.

**No scaffolding without a Linear issue.** Don't create skills, migrations, or infrastructure speculatively. If it's not tied to a GRO issue, it shouldn't be built.

**No loose files.** Don't drop files in the repo root. Don't hand-place files in `Brain/raw/inbox/`. Use defined locations or don't create files. See the document-management wiki for where everything goes.

---

## Session Lifecycle

### Startup

1. Read the project MOC (`Brain/projects/<Project>.md`). It links to wiki articles, source material, and design docs.
2. Check the Brain registry before creating new content: `python3 content-engine/engine.py registry check "<topic>"`. If Brain already covers it, update the existing article.
3. Know your environment. Claude Code sessions have Memory Bus and filesystem. Cowork sessions have Linear, Gmail, Canva, Figma. Don't try to use tools you don't have.

### During Work

4. One deliverable. Stay focused on what can be committed and verified.
5. Commit or revert. Don't leave uncommitted changes for the next session to untangle.
6. If work produces knowledge (research, analysis, decisions), route it through Brain during the same session — don't leave loose files.

### Shutdown

7. Ingest any knowledge produced: `python3 content-engine/engine.py ingest <file> -p <project>`.
8. Delete session artifacts (reports, manifests, one-shot scripts). The content engine is a permanent tool; its output is temporary.
9. If a wiki article was created or updated, rebuild the registry: `python3 content-engine/engine.py registry build`.

---

## Anti-Patterns

These specific mistakes have burned tokens in past sessions. Every item here happened.

| Anti-pattern | What went wrong |
|-------------|----------------|
| Files in repo root | Sprint plan dropped at `GrowDirect/` root with no reason. Root is not a workspace. |
| Hand-placing in Brain inbox | Session copied a file to `Brain/raw/inbox/` manually instead of using `engine.py ingest`. The copy was different from the original. |
| Duplicating between locations | Same content in two places, modified differently. Neither version authoritative. |
| Scaffolding without a Linear issue | Skills, migrations, infrastructure created speculatively. No GRO issue, no customer need. |
| Organizing instead of building | Session spent all its tokens renaming files and creating folder structures. Nothing shipped. |
| Stale error numbers | Session quoted validation errors from a script written weeks earlier. When the actual files were checked, the errors didn't exist. |
| Assuming things are broken | Told the user polygons were unusable without reading the current output. They were fine. |
| Silent dependency additions | Added packages to requirements.txt without telling the user. Docker image didn't match. |

---

## Cross-Session Handoffs

### Brain as the Bridge

Knowledge flows in one direction through Brain:

```
Claude Code session → Memory Bus (automatic)
                    → Brain (manual, via content engine)
                    → Cowork session (reads Brain)

Cowork session → Brain (manual, via content engine)
               → Claude Code session (reads Brain)
```

The manual step is deliberate. Not everything in a session is worth keeping. The content engine filters signal from noise.

### Playbooks

For repeatable multi-session workflows, Brain playbooks at `Brain/playbooks/` define the full process: what to read, where sources are, what the steps are, where output goes. Both agent systems can read these. Use playbooks when the same kind of work will happen more than once.

### What a Handoff Needs

When one system needs to dispatch work to the other, the handoff must include:

- **What** to do (the task, linked to a GRO issue)
- **How** to do it (pattern to follow, reference implementation)
- **Where** the relevant code/content lives (file paths)
- **What done looks like** (testable outcome)

A handoff that says "fix GRO-386" is insufficient. A handoff that says "fix GRO-386 — copy Cove's Flask-Session config to Canary, wire to Valkey DB 0, test login/logout" gives the receiving session everything it needs.

### Linear vs Brain

**Linear** is the task system. Issues, priorities, sprints, backlog. What needs to be done.

**Brain** is the knowledge system. Domain understanding, architecture, decisions, workflows. What we know.

Don't put knowledge in Linear issues (it gets buried). Don't put tasks in Brain articles (they go stale). Sprint plans and work orders live in `docs/plans/` or Linear — not in Brain, not in the repo root.

---

## Related

- [[Brain/wiki/document-management|Document Management Strategy]] — where files go, the seven document types
- [[Brain/Home|Brain Home]] — vault structure, content engine usage
- `CLAUDE.md` — hard rules, tech stack, session discipline, knowledge architecture
- `Brain/playbooks/` — repeatable workflow definitions

## Sources

- `CLAUDE.md` session discipline rules and knowledge architecture section
- `.claude/projects/` feedback memories (8 entries capturing working-style violations)
- `Brain/wiki/document-management.md` (companion article)
- `.claude/projects/-Users-gclyle-GrowDirect/memory/project_playbook_approach.md`
