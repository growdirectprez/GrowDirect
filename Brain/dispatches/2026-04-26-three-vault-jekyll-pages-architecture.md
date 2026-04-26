---
type: dispatch
status: ready-for-execution
date: 2026-04-26
target: Sonnet (mechanical execution; no Opus-level synthesis required)
priority: medium-high (architectural cleanup blocks the public partner/investor surface)
phase: three-vault architecture — public serving + factory boundary enforcement
prerequisite: three-vault architecture decision committed (see Brain memory `project_three_vault_architecture.md`)
companion-repos:
  - growdirect-llc/catz (public — method)
  - growdirect-llc/canary-retail-brain (public — product / spine)
companion-org: growdirectprez/GrowDirect (internal — factory; this dispatch lives here)
tags: [three-vault, github-pages, jekyll, public-serving, architecture, dispatch-protocol]
---

# Dispatch — Serve CATz and CRB via GitHub Pages + Jekyll, Enforce No-Local-Copy Boundary

## Why this dispatch exists

The founder decided 2026-04-26 on a three-vault architecture with an explicit audience split:

- **CATz** (`growdirect-llc/catz`) — public, audience: investors / partners / clients
- **Canary-Retail-Brain (CRB)** (`growdirect-llc/canary-retail-brain`) — public, audience: investors / partners / clients
- **GrowDirect** (`growdirectprez/GrowDirect`) — internal, audience: agents and founder; source/factory for the other two

Decision: CATz and CRB should have **no persistent local clone** on the laptop or mini. They live in git as source of truth, are served externally via GitHub Pages, and edited only via transient `gh repo clone` cycles when an agent is publishing curated content from GrowDirect.

This dispatch lands the serving stack (GitHub Pages + Jekyll on each public repo) and the GrowDirect-side hooks (external Project MOCs, CLAUDE.md update), then deletes the local clones.

Serving stack chosen: **GitHub Pages + Jekyll** (free, zero-infra, native GitHub support, defaults are good enough for v1).

## Current state

Both public repos have substantive content already in place:

**CATz** (`/Users/gclyle/CATz/` — to be deleted at end of dispatch):
- Top-level: ACKNOWLEDGMENT.md, CONTRIBUTING.md, Home.md, NOTICE.md, README.md, SECURITY.md, ready-to-show-confirmation.md
- Folders: about, agents, agreements, api-contracts, bios, cbm-v2, method, partnerships, proof-cases, standards, welcome-journey
- 23 files contain Obsidian-style `[[wikilinks]]`

**CRB** (`/Users/gclyle/Canary-Retail-Brain/` — to be deleted at end of dispatch):
- Top-level: ACKNOWLEDGMENT.md, CONTRIBUTING.md, Home.md, NOTICE.md, README.md, SECURITY.md, ready-to-show-confirmation.md
- Folders: architecture, case-studies, integrations, modules, platform, roadmap
- 28 files contain Obsidian-style `[[wikilinks]]`
- 18 active branches (4 laptop/gro-* and 13 mini/dispatch-mini*-X-manifest-deepening) on top of main — coordinate with founder before merging

Neither repo has any Jekyll config (`_config.yml`, `Gemfile`, `index.md/html`, `404.md`) yet.

GrowDirect/Brain/projects/ already holds the existing project MOC pattern (Canary.md, Cove.md, Method.md, Factory.md, RetailSpine.md, GrowDirect.md, Angel.md, Seacove.md, Secure.md). Two new MOCs are needed for CATz and CRB; they should follow the same `type: project-moc` frontmatter convention but with an `external-repo:` field and link OUT to github.com URLs (no `[[local/path]]` wikilinks).

## Tasks

### 1. Wikilink handling decision

Both repos use Obsidian wikilinks (`[[platform/spine-13-prefix]]`, etc.) — Jekyll doesn't natively render these. Two paths:

a) **Convert to standard markdown links** (recommended): script a one-pass conversion `[[path/page]]` → `[page](path/page.md)`. Keeps the "GitHub Pages with no plugin" promise, no Gemfile, no Bundler, fastest build. Only loss: the Obsidian-native UX inside the source repo, which doesn't matter post-deletion since the source repos won't be opened locally.

b) **Add a wikilinks Jekyll plugin** (e.g., `jekyll-wikilinks` from the GitHub Pages whitelist if available, or build via `_plugins/`): preserves wikilinks but requires custom Gemfile, breaks the zero-config promise, slower build, more failure modes.

**Recommended: option (a). Document the conversion script under `Canary-Retail-Brain/_tooling/` (and `CATz/_tooling/`) so it can be re-run if anyone authors new wikilinks via the web editor.**

### 2. Land Jekyll config on CATz

Create at repo root:

- `_config.yml` — title, description, theme. Suggested theme: `jekyll-theme-cayman` (technical-doc feel, GitHub-supported, no Gemfile needed). Set `markdown: kramdown`. Exclude `.obsidian/`, `_tooling/`.
- `index.md` (or rename existing `Home.md` → `index.md`) — landing page. Strip Obsidian-only frontmatter that Jekyll might mis-render.
- `404.md` — minimal not-found page with a link back to `/`.
- `.gitignore` (if missing) — ignore `_site/`, `.jekyll-cache/`, `Gemfile.lock`.

Run the wikilink conversion (Task 1) across the repo. Verify on a local Jekyll build (`bundle exec jekyll serve` in a temp dir) before pushing.

Commit + push to `main`. Title style per existing repo conventions.

### 3. Land Jekyll config on CRB

Same as Task 2, applied to CRB. Pay attention to:
- The `modules/` folder uses `X-name.md` and `X-name.manifest.yaml` pairs (one .md per spine prefix). Jekyll will render the .md; .yaml files become assets.
- The `architecture/`, `integrations/`, `roadmap/` directories are currently empty placeholders — Jekyll will skip them. Add `index.md` to each saying "(coming soon)" so navigation doesn't dead-end.
- 18 active branches. **Do not merge them in this dispatch.** Stay on `main`. Coordinate with founder if any branch should land on main as part of the v1 site.

### 4. Enable GitHub Pages on both repos

Via `gh` CLI (preferred — no clicking through web settings):

```
gh api -X PUT repos/growdirect-llc/catz/pages \
  -f source[branch]=main -f source[path]=/
gh api -X PUT repos/growdirect-llc/canary-retail-brain/pages \
  -f source[branch]=main -f source[path]=/
```

Wait for the first build (~1–2 min). Verify the published URLs render:
- `https://growdirect-llc.github.io/catz/`
- `https://growdirect-llc.github.io/canary-retail-brain/`

Spot-check 5+ pages including: home, a deep page (e.g., `modules/Q-loss-prevention.md` for CRB), a navigation crosslink (verify wikilink conversion held).

### 5. Add external Project MOCs in GrowDirect

Create:

- `GrowDirect/Brain/projects/CATz.md`
- `GrowDirect/Brain/projects/CanaryRetailBrain.md`

Follow the existing project-MOC frontmatter shape from `Brain/projects/Canary.md`, but add:

```yaml
external-repo: https://github.com/growdirect-llc/<repo>
external-site: https://growdirect-llc.github.io/<repo>/
audience: investors / partners / clients
local-clone: none (clone-on-demand only — see CLAUDE.md "External Vault Access")
```

Body should:
- One-paragraph summary of what the vault is and who it serves
- Link to the GitHub repo and the published site
- Brief topic index pointing at the published-site URLs (no `[[wikilinks]]`)
- A pointer to this dispatch as the architecture rationale

### 6. Update CLAUDE.md

Add a section titled **"External Vaults — Clone on Demand"** (place it near the existing "Brain — Domain Knowledge" section).

Content:
- Name CATz and CRB as the two external vaults; give the org/repo slugs and audience
- State the rule: no persistent local clone. Don't `cd ~/CATz` or `cd ~/Canary-Retail-Brain`.
- Pattern for an agent that needs to read CATz/CRB content: `gh repo clone <repo> /tmp/<slug>-$$ && ... && rm -rf /tmp/<slug>-$$`
- Pattern for publishing GrowDirect → CATz/CRB: same transient clone, copy curated content, commit, push, cleanup
- Note the published sites as the canonical surface for human reading
- Reference this dispatch + the `project_three_vault_architecture.md` memory

### 7. Delete local clones

Only after Tasks 1–6 are committed AND the published sites verify clean:

```
rm -rf /Users/gclyle/CATz
rm -rf /Users/gclyle/Canary-Retail-Brain
```

Verify final hierarchy:
- `/Users/gclyle/GrowDirect/` — present, on a tracked branch, clean
- `/Users/gclyle/CATz/` — absent
- `/Users/gclyle/Canary-Retail-Brain/` — absent
- `/Users/gclyle/.worktrees/` — unchanged (existing GrowDirect worktrees only)

### 8. Mini posture (deferred — flag only, do not execute)

Confirm the mini also has no `~/CATz/` or `~/Canary-Retail-Brain/` clones. If it does, file a follow-up dispatch targeting `Target/mini` to clean those up. Do not delete on the mini from a laptop session.

## Acceptance criteria

- [ ] Both `https://growdirect-llc.github.io/catz/` and `https://growdirect-llc.github.io/canary-retail-brain/` resolve and render at least the home page + 4 internal pages cleanly
- [ ] Internal navigation (former wikilinks) works in the rendered site — no 404s on a 5-page spot check
- [ ] Both repos build green in GitHub Actions (Pages build workflow shows success on the latest main commit)
- [ ] `GrowDirect/Brain/projects/CATz.md` and `CanaryRetailBrain.md` exist with the external frontmatter; both link to the live published URLs
- [ ] CLAUDE.md has the "External Vaults — Clone on Demand" section; future agents reading CLAUDE.md will not try to `cd ~/CATz`
- [ ] `/Users/gclyle/CATz/` and `/Users/gclyle/Canary-Retail-Brain/` are gone from the laptop
- [ ] One commit per logical task on each repo (CATz commits land on `growdirect-llc/catz`; CRB commits on `growdirect-llc/canary-retail-brain`; GrowDirect MOC + CLAUDE.md commits land on whichever feat branch is active in GrowDirect or a fresh `chore/external-vault-pages` branch)

## Open questions / decisions for the executor

1. **Theme** — `jekyll-theme-cayman` is the recommendation. If the founder later wants `just-the-docs` (sidebar nav, search) it's a `_config.yml` swap. Stick with cayman for v1.
2. **Custom domain** — out of scope for this dispatch. Default to `*.github.io` URLs. Founder can wire DNS later if a `*.growdirect.app` or similar subdomain is desired.
3. **Branch coordination on CRB** — the 4 laptop/gro-* branches and 13 mini/dispatch-mini* branches are out of scope. **Stay on main.** Flag to founder if any of those branches need to merge as part of the v1 public site.
4. **Wikilink conversion script** — first-pass implementation can be a small Python script under `_tooling/convert_wikilinks.py` in each repo. Idempotent. Document in repo README.
5. **Linear issue** — file a Linear issue under the Dispatch project pointing at this brief, with `Target/laptop`, `Agent/<TBD>`, priority Medium-High. The executor should pick up via Linear lifecycle (per CLAUDE.md "Dispatch Protocol").

## What this dispatch does NOT do

- Does not migrate the 13 `mini/dispatch-mini*-X-manifest-deepening` branches into main on CRB.
- Does not backfill source artifacts in GrowDirect/Brain/ for the historical CRB content authored directly there. That is a separate "going-forward" architectural acceptance — old content stays, new content originates in GrowDirect.
- Does not set up the memory bus to ingest CRB/CATz on a cron pull. Flag as a follow-up if agent-side semantic search across the public vaults becomes a felt need.
- Does not configure custom domains or analytics on the published sites.
- Does not touch the mini.

## On completion

Comment on the Linear issue with: artifact paths (commits in CATz, CRB, GrowDirect), commit SHAs, the two published URLs, one-paragraph summary, and any GRO tickets recommended for filing (e.g., custom-domain wiring, theme upgrade, memory bus pull, mini cleanup).
