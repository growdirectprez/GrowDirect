# CATz — Co-Sell Toolkit Vault

## What this is

This directory is the **CATz (Co-sell Assets & Toolkit)** companion vault —
a partner-and-prospect-facing projection of `GrowDirect/Brain/` scoped to
co-sell, positioning, and sales enablement content. It is published at
`catz.growdirect.io`.

**Source of truth: `GrowDirect/Brain/`**

Do NOT edit content in this directory directly. All edits go to
`GrowDirect/Brain/wiki/` or `GrowDirect/Brain/projects/`. This directory
is refreshed via the vault sync workflow (see below) before any external
access window.

---

## Vault sync workflow

When asked to sync, refresh, or update this vault:

1. **Identify changed articles** in `GrowDirect/Brain/wiki/` and
   `GrowDirect/Brain/projects/` since last sync (check `last-compiled`
   frontmatter vs previous sync date).

2. **Scope filter** — copy only co-sell and positioning articles:
   - `Brain/wiki/canary-*` (platform and product) → `CATz/wiki/`
   - `Brain/wiki/retail-*` (RetailSpine, retail domain) → `CATz/wiki/`
   - `Brain/wiki/crb-*` (Canary Retail Brain capabilities) → `CATz/wiki/`
   - `Brain/wiki/growdirect-the-*` (Chirp, Fox product articles) → `CATz/wiki/`
   - `Brain/projects/Canary.md` (MOC index) → `CATz/projects/`
   - Partner-facing briefs from `Brain/wiki/brief-*` → `CATz/wiki/`

3. **Strip internal provenance** before copying any article that carries
   `classification: confidential` or references internal-only lineage
   (client names, founder-operator provenance notes, internal Linear issue
   numbers, cap table references). Use the scrub-generic rule: remove client
   names, keep canonical patterns.

4. **Verify links** — Obsidian `[[wikilinks]]` that point outside the
   CATz-scoped projection will break in the published vault. Replace with
   plain text or external URLs before pushing.

5. **Update `projects/Canary.md`** — confirm the MOC index reflects all
   articles now in `CATz/wiki/`.

6. **Commit and push** — `git add CATz/ && git commit -m "catz: sync from Brain $(date +%Y-%m-%d)"`.

7. **Note sync date** — update the `last-sync` field in this file:

```
last-sync: 2026-04-27
```

**last-sync: 2026-04-27**

---

## What stays out of this vault

- Angel, Cove, Seacove content
- HOA / WPBCA governance documents
- Internal financial projections or cap table
- Secure-era client artifacts (even scrubbed — leave in Brain only)
- Memory bus architecture internals
- Raw inbox / unprocessed intake files
- Team profiles and compensation data
- Any article with `classification: confidential`
- Vendor-specific content (that belongs in NCR or other vendor vaults)

---

## Related vaults

| Vault | Location | Audience | Source |
|---|---|---|---|
| CATz | `CATz/` (this dir) | Partners, prospects | `GrowDirect/Brain/` |
| CRB | `Canary/brain/` | Internal + partners | `GrowDirect/Brain/` |
| NCR | `~/GrowDirect-NCR/` (sibling repo) | NCR Counterpoint VARs | `GrowDirect/Brain/` |

All vaults are projections of `GrowDirect/Brain/`. Never edit vault
content directly — always edit the source and re-sync.
