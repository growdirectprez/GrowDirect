---
type: project-moc
status: active
tags: [method, growdirect-method, methodology, navigation-moc]
---

# Method

GrowDirect's method — the structured navigation over how work gets done here. Modeled on IBM Global Services MethodWeb's structure (Models / Roles / Techniques / Work Products / Activities / Communication Documents), adapted for how GrowDirect actually operates today: Linear for activities, Obsidian for the graph, skills for executable techniques, Brain templates for work products.

## Summary

Every project at GrowDirect runs through the same shape:
1. A **Model** (a method — the Factory pipeline is the dominant one; superpowers brainstorm→plan→execute is the meta-model)
2. Executed by **Roles** (ALX, Tom, Eva, Jeremy, Jess, Jim, Owl, Art, Compliance, DevOps, Legal, Research)
3. Applying **Techniques** (skills from plugins)
4. Producing **Work Products** (Brain templates, SDDs, plans, briefs)
5. Through **Activities** (Linear issues)
6. Surfaced via **Communication Documents** (SDDs, briefs, handoff docs)

This MOC indexes each category. Start here to navigate the method; drill into Factory.md for the dominant operational pipeline.

## Models (methods)

- [[Brain/projects/Factory|Factory Pipeline]] — 9-stage dev pipeline (preflight → close). The dominant GrowDirect method.
- [[Brain/method/Models|Models Index]] — other methods: superpowers workflow (brainstorm → spec → plan → execute), brand-voice generation, legal triage flows, marketing campaign flows, enterprise-search digest flow

## Roles

Who does what. Each role has a profile that captures responsibilities, typical work, and coordination relationships.

- [[Brain/method/Roles|Roles Index]] — all role profiles with links to [[Canary/docs/profiles/ops/|Canary/docs/profiles/ops/*.md]]

Current roster: ALX (orchestration), Tom (architecture), Eva (program), Jeremy (build + DevOps), Jess (documentation), Jim (customer sentiment), Owl (product AI), Art (UX/creative), Compliance, Legal, DevOps, Research.

## Techniques (skills)

The how-to library. Each skill is an executable technique — not documentation about how to do something, but a runnable workflow.

- [[Brain/method/Techniques|Techniques Index]] — skills grouped by plugin (superpowers, engineering, brand-voice, legal, marketing, enterprise-search, anthropic-skills, rpv-permit-architect, claude-api)

~45+ skills in `.claude/skills/` plus plugin skills loaded per-session.

## Work Products

Deliverable templates. What agents produce when they work.

- [[Brain/method/WorkProducts|Work Products Index]] — Brain templates, SDD templates, plan template, brief template, spec template

Current Brain templates: card, claim, daily-note, decision, meeting, raw-intake, wiki-article.

## Activities

Live work. Tracked in Linear, not duplicated here.

- [[Brain/method/Activities|Activities Index]] — Linear project / cycle / label reference + saved-view conventions per role

Linear workspace: [GrowDirect](https://linear.app/growdirect) (team key `GRO`).

## Communication Documents

Client-facing and cross-agent artifact structures.

- [[Brain/method/CommDocs|CommDocs Index]] — SDD structure, brief structure, spec structure, wiki-article structure, handoff-brief structure

## How to use this MOC

- **Planning work?** Start at [[Brain/projects/Factory|Factory]] to pick a stage; drill to the skill that runs it; check which role primary-runs it.
- **Onboarding a new role or agent?** Start at [[Brain/method/Roles|Roles Index]] and read the role profile; the profile links to the techniques the role uses and the WPs the role produces.
- **Adding a new technique (skill)?** Start at [[Brain/method/Techniques|Techniques Index]] to find where it fits; when published, add it to the index and tag the roles that use it.
- **Checking what Linear issues a role owns?** Activity views are defined in [[Brain/method/Activities|Activities Index]].

## Design notes

- **Linear is the activity layer.** Activities here are abstractions; real work is in Linear.
- **Obsidian is the graph.** Cross-references use `[[...]]` wiki-link syntax so Obsidian's graph view renders the method as a navigable map.
- **Skills are executable techniques.** A technique isn't complete until it's a skill file; a skill file isn't complete until it runs in a Cowork/Claude Code session.
- **Brain templates are WP specs.** A WP template isn't complete until it's in `Brain/templates/` and used by at least one Linear issue's output.
- **SDDs are CommDocs.** Each SDD is a cross-agent communication artifact; they collectively describe the platform.

## Sprint history

- **Sprint A (this commit)** — scaffold Method + Factory MOCs + 5 category MOCs (Roles / Techniques / WorkProducts / Activities / CommDocs). Pure navigation; no changes to existing assets.
- **Sprint B (pending)** — augment each role profile in `Canary/docs/profiles/ops/` with "Produces / Uses / Performs" cross-reference sections.
- **Sprint C (pending)** — add `roles:` frontmatter to skills; add `stage:` + `role:` to Brain templates; add `author-role:` to SDDs. Rebuild registry so the graph is queryable.

## Related

- [[Brain/projects/Factory|Factory Pipeline MOC]] — the dominant operational method
- [[Brain/projects/Canary|Canary]] — the app where Factory was codified
- [[Brain/projects/Cove|Cove]], [[Brain/projects/Angel|Angel]], [[Brain/projects/Seacove|Seacove]], [[Brain/projects/Secure|Secure]] — other project MOCs
- [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]] — authoritative factory spec
- [[docs/sdds/platform/skill-architecture|Skill Architecture SDD]] — skill composition rules
- IBM MethodWeb (source inspiration, not ingested): `/Users/gclyle/Desktop/IBM Method Web/IBMGSM40/` — 2001-era reference for the structure, not the content
