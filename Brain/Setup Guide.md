---
type: reference
---

# Obsidian Setup Guide

## Opening the vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `GrowDirect` folder
4. Obsidian will find the `.obsidian` config and load everything

## Recommended community plugins

Go to Settings > Community Plugins > Browse, then install:

1. **Dataview** — query your notes like a database (filter by tags, dates, status)
2. **Templater** — enhanced templates with dynamic dates and prompts
3. **Obsidian Web Clipper** (browser extension) — clip web articles directly into `Brain/raw/clips/`
4. **Calendar** — visual calendar for daily notes
5. **Graph Analysis** — better graph view for seeing connections

Optional but useful:
- **Kanban** — turn notes into project boards
- **Excalidraw** — whiteboard/diagramming inside Obsidian
- **Git** — auto-commit vault changes (keeps history of everything)

## Workflow

### Quick capture
- Use the daily note (click the calendar icon) for quick thoughts
- New notes land in `Brain/inbox/` by default
- Use Cmd+T to create from templates

### Karpathy processing cycle
1. Dump raw material into `Brain/raw/` (or use Web Clipper)
2. Periodically ask ALX/Claude: "Process my raw notes and update the wiki"
3. Claude reads `Brain/raw/`, synthesizes, and creates/updates `Brain/wiki/` articles
4. Wiki articles link back to sources and to each other

### Linking conventions
- Use `[[wikilinks]]` for everything inside the vault
- Tag with `#project/canary`, `#project/cove`, `#project/seacove`
- Frontmatter `type:` field for filtering (wiki, raw, decision, meeting, journal)

## Folder map

```
GrowDirect/                    ← THE VAULT
├── .obsidian/                 ← Obsidian config (auto-managed)
├── Brain/                     ← YOUR SECOND BRAIN
│   ├── raw/                   ← Karpathy-style intake
│   │   ├── inbox/             ← Quick capture, unprocessed
│   │   ├── clips/             ← Web clipper articles
│   │   ├── research/          ← Papers, deep dives
│   │   └── meetings/          ← Meeting notes
│   ├── wiki/                  ← LLM-compiled knowledge articles
│   ├── projects/              ← Project dashboards (MOCs)
│   ├── journal/               ← Daily notes
│   ├── decisions/             ← ADRs and decision logs
│   ├── templates/             ← Note templates
│   └── attachments/           ← Images, files
├── Canary/                    ← Canary codebase + docs (existing)
│   └── docs/                  ← Atlas, profiles, field registry
├── Cove/                      ← Cove codebase + archive (existing)
│   └── docs/archive/          ← Legal docs, narrative, analysis
└── ARC/                       ← Seacove blueprints (existing)
```
