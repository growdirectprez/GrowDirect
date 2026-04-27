# Canary Site — Dynamic Vault Integration
**Date:** 2026-04-26
**Repo:** `growdirectprez/canary-site`
**Status:** Design spec — reviewed, ready for implementation planning

---

## Executive Summary

The three GrowDirect knowledge vaults (NCR, CRB, CATz) currently live as separate Quartz sites at their own subdomains. This spec wires them into `canary.growdirect.io/rapidpos/` as dynamically rendered pages using the design system from the RapidPOS handoff. When a vault author pushes a markdown change, the canary site rebuilds and the updated page is live within ~90 seconds. No manual HTML conversion. No copy-paste. No sync drift.

All three vault repos are public (`growdirect-llc/ncr`, `growdirect-llc/canary-retail-brain`, `growdirect-llc/catz`).

---

## Architecture

### The single governing constraint

The vault repos are **not modified** except for adding one GitHub Actions workflow file to each (the cross-repo trigger). They continue to build to their own Quartz sites. Eleventy is an additional downstream consumer of the same markdown — it reads vault content but doesn't own it.

### Component map

```
growdirectprez/canary-site
├── package.json              ← Eleventy + markdown-it + plugins
├── .eleventy.js              ← Eleventy config
├── .github/workflows/
│   └── build-deploy.yml      ← builds on push + repository_dispatch
├── content/                  ← git submodules (vault content)
│   ├── ncr/                  → growdirect-llc/ncr (submodule)
│   ├── crb/                  → growdirect-llc/canary-retail-brain (submodule)
│   └── catz/                 → growdirect-llc/catz (submodule)
├── src/
│   ├── _includes/
│   │   ├── wiki.njk          ← wiki page layout (from wiki-template.html)
│   │   ├── shared-styles.njk ← <style> block extracted from wiki-template.html
│   │   ├── nav.njk           ← shared top nav (extracted from proposal pages)
│   │   └── footer.njk        ← shared footer
│   ├── _data/
│   │   └── vault.js          ← global vault metadata (labels, paths)
│   ├── rapidpos/             ← static proposal pages (pass-through)
│   │   ├── index.html
│   │   ├── architecture.html
│   │   ├── endpoints.html
│   │   ├── integrate.html
│   │   ├── store-2030.html
│   │   ├── armstrong.html
│   │   ├── wiki-template.html
│   │   ├── ncr -> ../../../content/ncr   ← committed symlink
│   │   ├── crb -> ../../../content/crb   ← committed symlink
│   │   └── catz -> ../../../content/catz ← committed symlink
│   └── rapidpos/
│       ├── ncr.json          ← directory data: layout=wiki.njk, vault=ncr
│       ├── crb.json          ← directory data: layout=wiki.njk, vault=crb
│       └── catz.json         ← directory data: layout=wiki.njk, vault=catz
└── _site/                    ← Eleventy build output → GitHub Pages

growdirect-llc/ncr  (and crb, catz — one workflow added to each)
└── .github/workflows/
    └── notify-canary.yml     ← dispatches repository_dispatch to canary-site on push
```

### URL routing

| Vault | Source path | Published URL |
|---|---|---|
| NCR | `content/ncr/Home.md` | `/rapidpos/ncr/` |
| NCR | `content/ncr/modules/T-transaction-pipeline.md` | `/rapidpos/ncr/modules/T-transaction-pipeline/` |
| CRB | `content/crb/platform/index.md` | `/rapidpos/crb/platform/` |
| CATz | `content/catz/method/index.md` | `/rapidpos/catz/method/` |

Eleventy computes permalinks from file path relative to the vault root. `Home.md` → `index.html` in each vault directory.

---

## Eleventy Configuration

### Shared slug function (`src/_utils/slug.js`)

This function is the single source of truth for URL slug generation. Both Eleventy's permalink output and the wikilink plugin's `postProcessPagePath` must use this exact function to guarantee that wikilinks resolve to the correct URLs.

```javascript
// src/_utils/slug.js
module.exports = function slug(str) {
  return str
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")   // strip special chars (including em-dash)
    .replace(/[\s_]+/g, "-")    // spaces and underscores → hyphens
    .replace(/^-+|-+$/g, "");   // trim leading/trailing hyphens
};
```

### `.eleventy.js`

```javascript
const markdownIt = require("markdown-it");
const markdownItWikilinks = require("markdown-it-wikilinks");
const markdownItCallouts = require("markdown-it-obsidian-callouts");
const slug = require("./_utils/slug.js");

module.exports = function(eleventyConfig) {

  // ── Pass-through: static proposal HTML, CSS, images ──────────────────────
  eleventyConfig.addPassthroughCopy("src/rapidpos/*.html");
  eleventyConfig.addPassthroughCopy("src/rapidpos/*.css");
  eleventyConfig.addPassthroughCopy("src/rapidpos/img/**");

  // ── Ignore Quartz build artifacts and Obsidian config in vault submodules ─
  // These files are committed by Quartz Actions and must not be processed.
  eleventyConfig.ignores.add("src/rapidpos/*/public/**");
  eleventyConfig.ignores.add("src/rapidpos/*/quartz/**");
  eleventyConfig.ignores.add("src/rapidpos/*/.obsidian/**");
  eleventyConfig.ignores.add("src/rapidpos/*/.github/**");
  eleventyConfig.ignores.add("src/rapidpos/*/node_modules/**");
  eleventyConfig.ignores.add("src/rapidpos/*/static/**");   // Quartz static assets

  // ── Exclude draft:true files from build ───────────────────────────────────
  eleventyConfig.addGlobalData("eleventyComputed", {
    eleventyExcludeFromCollections: (data) => data.draft === true,
  });
  // Also prevent draft pages from being written to _site
  eleventyConfig.on("eleventy.before", () => {});
  eleventyConfig.addCollection("livePosts", (api) =>
    api.getAll().filter((p) => !p.data.draft)
  );

  // ── Markdown processor ─────────────────────────────────────────────────────
  const md = markdownIt({ html: true, linkify: true, typographer: true })
    .use(markdownItWikilinks, {
      // uriSuffix: "" → clean directory-style URLs (no .html extension)
      uriSuffix: "",
      // makeAllLinksAbsolute ensures links work from any page depth
      makeAllLinksAbsolute: true,
      // baseURL is vault-aware: wikilinks are prefixed with the vault path.
      // Since markdown-it-wikilinks has a single baseURL, vault-relative
      // resolution is handled by postProcessPagePath — the baseURL is set to
      // "/rapidpos/" and the vault prefix is injected via the Nunjucks layout
      // using a per-page data cascade (vault = "ncr"|"crb"|"catz").
      // NOTE: Cross-vault wikilinks are not supported in v1 — they resolve
      // as broken links. Internal vault links only.
      baseURL: "/rapidpos/",
      postProcessPagePath: (path) => slug(path),
      postProcessLabel: (label) => label,
    })
    .use(markdownItCallouts);

  eleventyConfig.setLibrary("md", md);

  // ── Filters ────────────────────────────────────────────────────────────────

  // Breadcrumb: takes a URL string, returns array of path segments
  eleventyConfig.addFilter("breadcrumb", (url) => {
    return url
      .replace(/^\/rapidpos\//, "")
      .replace(/\/$/, "")
      .split("/")
      .filter(Boolean);
  });

  // Which vault does this URL belong to?
  eleventyConfig.addFilter("vaultName", (url) => {
    if (url.startsWith("/rapidpos/ncr/")) return "NCR";
    if (url.startsWith("/rapidpos/crb/")) return "CRB";
    if (url.startsWith("/rapidpos/catz/")) return "CATz";
    return null;
  });

  // Strip Quartz/Obsidian frontmatter fields irrelevant to this build
  const STRIP_FIELDS = ["enableToc", "cssclasses", "graph", "backlinks",
                        "search", "noindex", "weight", "date"];
  eleventyConfig.addFilter("stripQuartzFrontmatter", (data) =>
    Object.fromEntries(Object.entries(data).filter(([k]) => !STRIP_FIELDS.includes(k)))
  );

  // ── Sidebar nav collections ────────────────────────────────────────────────
  // Build a nav collection for each vault: array of { label, links: [{url, title}] }
  // Groups pages by their immediate parent directory within the vault.
  function buildVaultNav(api, vaultPrefix) {
    const pages = api.getFilteredByGlob(`src/rapidpos/${vaultPrefix}/**/*.md`)
      .filter((p) => !p.data.draft)
      .sort((a, b) => {
        // Index files first, then alphabetical by title
        const aIsIndex = a.fileSlug === "index" || a.fileSlug === "Home";
        const bIsIndex = b.fileSlug === "index" || b.fileSlug === "Home";
        if (aIsIndex && !bIsIndex) return -1;
        if (!aIsIndex && bIsIndex) return 1;
        return (a.data.title || a.fileSlug).localeCompare(b.data.title || b.fileSlug);
      });

    const sections = {};
    for (const page of pages) {
      // Get path relative to vault root, e.g. "modules/T-transaction-pipeline"
      const rel = page.url.replace(`/rapidpos/${vaultPrefix}/`, "").replace(/\/$/, "");
      const parts = rel.split("/");
      const sectionKey = parts.length > 1 ? parts[0] : "Overview";
      const label = sectionKey.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

      if (!sections[sectionKey]) sections[sectionKey] = { label, links: [] };
      sections[sectionKey].links.push({
        url: page.url,
        title: page.data.title || page.fileSlug.replace(/-/g, " "),
      });
    }
    return Object.values(sections);
  }

  eleventyConfig.addCollection("ncrNav",  (api) => buildVaultNav(api, "ncr"));
  eleventyConfig.addCollection("crbNav",  (api) => buildVaultNav(api, "crb"));
  eleventyConfig.addCollection("catzNav", (api) => buildVaultNav(api, "catz"));

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
};
```

### Vault content wiring — committed symlinks

The vault content is exposed to Eleventy via symlinks committed to the repo (not created at build time). This is the reliable approach in GitHub Actions — the symlink is part of the repo state and works without any workflow step.

```bash
# One-time setup — run locally, commit the result
cd /path/to/canary-site/src/rapidpos
ln -s ../../../content/ncr ncr
ln -s ../../../content/crb crb
ln -s ../../../content/catz catz
git add ncr crb catz
git commit -m "chore: add vault content symlinks"
```

The symlinks point relative to their location (`src/rapidpos/`) to the submodule roots (`content/ncr/`, etc.), so they resolve correctly both locally and in GitHub Actions once submodules are checked out.

### Directory data files

Each vault directory gets a `.json` data file that injects the layout and vault identifier into every markdown page under it, without requiring frontmatter in the vault markdown files themselves.

```json
// src/rapidpos/ncr/ncr.json
{
  "layout": "wiki.njk",
  "vault": "ncr",
  "vaultLabel": "NCR Vault"
}
```

Same pattern: `crb.json` with `"vault": "crb", "vaultLabel": "Canary Retail Brain"` and `catz.json` with `"vault": "catz", "vaultLabel": "CATz Method"`.

---

## Wiki Layout Template (`src/_includes/wiki.njk`)

Derived directly from `rapidpos/wiki-template.html`. The `<style>` block is extracted into `shared-styles.njk` and `{% include %}`d here. The sidebar nav uses the `collections[vault + "Nav"]` collection built above.

Key differences from the static template:
- `{% include "shared-styles.njk" %}` — single source of truth for CSS
- `{% include "nav.njk" %}` — shared top nav
- `{{ content | safe }}` — rendered markdown injection point
- Sidebar nav is dynamic from the collection, not hardcoded
- Breadcrumb computed from `page.url`
- Active nav link detected by comparing `link.url` to `page.url`

```njk
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title or fileSlug | replace("-", " ") | title }} — Canary {{ vaultLabel }}</title>
  {% if description %}<meta name="description" content="{{ description }}">{% endif %}
  {% include "shared-styles.njk" %}
</head>
<body>
  {% include "nav.njk" %}

  <div class="wiki-layout">
    <nav class="wiki-sidebar">
      <div class="wiki-vault-header">
        <span class="label">{{ vaultLabel | upper }}</span>
      </div>

      {% set navCollection = collections[vault + "Nav"] %}
      {% if navCollection %}
        {% for section in navCollection %}
          <div class="wiki-section">
            <div class="wiki-section-label">{{ section.label }}</div>
            {% for link in section.links %}
              <a href="{{ link.url }}"
                 class="wiki-nav-link{% if link.url == page.url %} active{% endif %}">
                {{ link.title }}
              </a>
            {% endfor %}
          </div>
        {% endfor %}
      {% endif %}

      <div class="vault-switcher">
        <span class="label">Vaults</span>
        <a href="/rapidpos/ncr/"  class="vault-link{% if vault == 'ncr' %}  active{% endif %}">NCR</a>
        <a href="/rapidpos/crb/"  class="vault-link{% if vault == 'crb' %}  active{% endif %}">CRB</a>
        <a href="/rapidpos/catz/" class="vault-link{% if vault == 'catz' %} active{% endif %}">CATz</a>
      </div>
    </nav>

    <main class="wiki-content">
      <div class="breadcrumb">
        <a href="/rapidpos/">RapidPOS</a>
        {% for crumb in page.url | breadcrumb %}
          <span class="sep">›</span>
          <span>{{ crumb | replace("-", " ") | title }}</span>
        {% endfor %}
      </div>
      {{ content | safe }}
    </main>
  </div>

  {% include "footer.njk" %}
</body>
</html>
```

---

## Markdown Transformation Details

### Wikilinks

`[[T — Transaction Pipeline]]` renders to:
`<a href="/rapidpos/T-transaction-pipeline">T — Transaction Pipeline</a>`

The slug function strips the em-dash and special characters, producing `t-transaction-pipeline`, which Eleventy's permalink for `T-transaction-pipeline.md` also produces. They match.

**Vault-path limitation (v1):** The `baseURL: "/rapidpos/"` means all wikilinks resolve relative to `/rapidpos/` regardless of which vault the source page is in. A wikilink `[[T — Transaction Pipeline]]` in an NCR doc resolves to `/rapidpos/T-transaction-pipeline` (missing the `/ncr/modules/` prefix). In v1 this is acceptable — the nav sidebar provides the primary navigation. Cross-vault internal links are not supported. Full vault-aware wikilink resolution is a v2 enhancement.

### Obsidian callouts

```
> [!note] Title
> Body text here.
```
→
```html
<div class="callout callout-note">
  <div class="callout-label">Title</div>
  <p>Body text here.</p>
</div>
```

Callout types mapped to CSS classes:
- `[!note]`, `[!info]` → `callout-note` — gold left border
- `[!warning]`, `[!danger]` → `callout-warning` — red left border  
- `[!tip]`, `[!success]` → `callout-tip` — green-light left border

### Frontmatter

Stripped entirely (not rendered): `draft`, `enableToc`, `cssclasses`, `graph`, `backlinks`, `search`, `noindex`, `weight`, `date`

Used by Eleventy:
- `title` → `<title>` tag and `<h1>` if no `#` heading in content body
- `description` → `<meta name="description">`
- `tags` → added as `<meta name="keywords">`, not rendered in body

`draft: true` → page is excluded from build entirely (not written to `_site`).

### Tables

Standard markdown tables → `<table class="wiki-table">` with alternating row shading (`--bg` / `--bg-alt`), `border-collapse: collapse`, header row in `--green-dark` with `--text-on-dark` text. CSS for this is in `shared-styles.njk`.

### Images and Obsidian embeds

Obsidian `![[image.png]]` embeds are **not transformed** in v1. They will render as literal text. Standard markdown image syntax `![alt](./path/image.png)` will render as `<img>` tags, but vault images are not included in the submodule checkout unless committed to the vault repo. In v1 this is acceptable — most vault content is text-heavy. Image support is a v2 enhancement (copy static assets from vault to `_site` during build, or reference Quartz subdomain for images).

### 404 strategy for broken wikilinks

Wikilinks to pages that do not exist in the Eleventy build (e.g., Quartz-only pages, cross-vault links) will render as dead links in v1. No redirect strategy is implemented. The nav sidebar is the primary navigation surface; wikilinks are supplementary. A future enhancement could add a build-time check that logs unresolved wikilinks as warnings.

---

## Cross-Repo Trigger

### `repository_dispatch` pattern

Each vault repo gets one workflow file. On push to `main` with any `.md` change, it fires a `repository_dispatch` event to `canary-site`. The canary-site build workflow listens for this event and runs a full submodule update + Eleventy build.

**In each vault repo** (`.github/workflows/notify-canary.yml`):

```yaml
name: Notify canary-site
on:
  push:
    branches: [main]
    paths: ["**/*.md"]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Dispatch to canary-site
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.CANARY_SITE_DISPATCH_TOKEN }}
          repository: growdirectprez/canary-site
          event-type: vault-updated
          client-payload: '{"vault":"${{ github.repository }}","sha":"${{ github.sha }}"}'
```

**Secret required:** `CANARY_SITE_DISPATCH_TOKEN` — a GitHub fine-grained PAT scoped to `growdirectprez/canary-site` with `Actions: Read and Write` permission. Store this secret in each vault repo under Settings → Secrets → `CANARY_SITE_DISPATCH_TOKEN`. One token value, added to all three vault repos.

**In `growdirectprez/canary-site`** (`.github/workflows/build-deploy.yml`):

```yaml
name: Build and deploy
on:
  push:
    branches: [main]
  repository_dispatch:
    types: [vault-updated]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout with submodules
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
          # GITHUB_TOKEN is sufficient — all vault repos are public

      - name: Update submodules to latest main
        run: git submodule update --remote --merge

      - name: Setup Node 20
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Build Eleventy
        run: npm run build

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_site"

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Pages Source Migration

The `growdirectprez/canary-site` repo currently uses `build_type: legacy` (branch-served from `main`). Adding an Actions deployment requires switching to `build_type: workflow`.

**This causes a brief planned outage** — the DELETE removes Pages config entirely; the site is offline until the first Actions deployment completes. Expected downtime: 2–5 minutes. Schedule during low-traffic hours.

```bash
# Step 1 — delete current Pages config
gh api --method DELETE repos/growdirectprez/canary-site/pages
# Step 2 — wait for deletion to propagate (not just sleep 3)
until ! gh api repos/growdirectprez/canary-site/pages 2>/dev/null | grep -q "html_url"; do
  sleep 5
done
echo "Pages config deleted"
# Step 3 — re-enable with workflow build type
gh api --method POST repos/growdirectprez/canary-site/pages \
  -F "build_type=workflow" \
  --jq '.status'
# Step 4 — push a commit to canary-site to trigger first build
# (or merge the Eleventy setup PR — that push triggers it)
```

Verify recovery:
```bash
gh api repos/growdirectprez/canary-site/actions/runs \
  --jq '.workflow_runs[0]|{status,conclusion,name}'
# expect: {"status":"completed","conclusion":"success","name":"Build and deploy"}
```

---

## Dependencies

```json
{
  "name": "canary-site",
  "version": "1.0.0",
  "scripts": {
    "build": "eleventy",
    "serve": "eleventy --serve"
  },
  "devDependencies": {
    "@11ty/eleventy": "^3.0.0",
    "markdown-it": "^14.1.0",
    "markdown-it-wikilinks": "^1.4.0",
    "markdown-it-obsidian-callouts": "^1.0.0"
  }
}
```

All dev dependencies — nothing runs at runtime. Build output is pure static HTML.

`.eleventy.js`, `package.json`, and `package-lock.json` are committed to `canary-site`. The `_site/` output directory is in `.gitignore`. GitHub Actions generates it fresh on every build.

---

## What Does NOT Change

| Thing | Status |
|---|---|
| `growdirect-llc/ncr` markdown content and structure | Unchanged |
| `growdirect-llc/canary-retail-brain` markdown content | Unchanged |
| `growdirect-llc/catz` markdown content | Unchanged |
| Quartz builds for ncr / crb / catz subdomains | Unchanged — still build and deploy independently |
| Existing static HTML proposal pages in `rapidpos/` | Unchanged — Eleventy passes through |
| `canary.growdirect.io` root `index.html` | Unchanged |
| GoDaddy DNS | Unchanged |
| Vault repos' Quartz config | Unchanged |

The only additions to vault repos: one `.github/workflows/notify-canary.yml` file each, and one repo secret (`CANARY_SITE_DISPATCH_TOKEN`).

---

## v2 Enhancements (out of scope for this spec)

- Vault-aware wikilink resolution (prefix links with vault path)
- Image/asset handling (copy vault static assets into `_site`)
- Build-time wikilink validation (warn on unresolved links)
- Cross-vault wikilinks (link from NCR page to CATz page)
- Search across all vault content

---

## Related

- `docs/superpowers/specs/2026-04-26-rapidpos-site-design-brief.md` — RapidPOS site design brief
- [[Brain/wiki/growdirect-public-sites-deployment]] — deployment wiki
- GRO-606 — Build Quartz knowledge sites for CATz and Canary Retail
