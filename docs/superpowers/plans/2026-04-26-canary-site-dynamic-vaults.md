# Canary Site — Dynamic Vault Integration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the three GrowDirect knowledge vaults (NCR, CRB, CATz) into `canary.growdirect.io/rapidpos/` as dynamically rendered HTML pages — vault authors push markdown, site rebuilds in ~90 seconds.

**Architecture:** Eleventy 3 consumes vault markdown via committed git submodules in `growdirectprez/canary-site`. A `wiki.njk` Nunjucks layout wraps the rendered markdown in the existing RapidPOS design system. Each vault repo gains one GitHub Actions workflow that fires a `repository_dispatch` event to `canary-site` on markdown push, triggering a submodule-update + Eleventy build + Pages deploy.

**Tech Stack:** Eleventy 3, markdown-it 14, markdown-it-wikilinks 1.4, Nunjucks, GitHub Actions, GitHub Pages (workflow build type)

**Spec:** `docs/superpowers/specs/2026-04-26-canary-site-dynamic-vaults-design.md`

---

## File Map

### New files in `growdirectprez/canary-site`

| File | Purpose |
|---|---|
| `package.json` | Eleventy + markdown-it dependencies, build scripts |
| `.eleventy.js` | Full Eleventy config: ignores, markdown processor, filters, collections |
| `src/_utils/slug.js` | Shared slug function — used by both Eleventy permalinks and wikilink plugin |
| `src/_includes/shared-styles.njk` | CSS extracted from `rapidpos/wiki-template.html` lines 16–585 |
| `src/_includes/nav.njk` | Top nav extracted from `rapidpos/index.html` lines 495–513 |
| `src/_includes/footer.njk` | Footer extracted from `rapidpos/index.html` lines 644–end |
| `src/_includes/wiki.njk` | Wiki page layout: sidebar nav + breadcrumb + `{{ content }}` |
| `src/rapidpos/ncr` | Committed symlink → `../../../content/ncr` |
| `src/rapidpos/crb` | Committed symlink → `../../../content/crb` |
| `src/rapidpos/catz` | Committed symlink → `../../../content/catz` |
| `src/rapidpos/ncr.json` | Directory data: `layout=wiki.njk`, `vault=ncr` |
| `src/rapidpos/crb.json` | Directory data: `layout=wiki.njk`, `vault=crb` |
| `src/rapidpos/catz.json` | Directory data: `layout=wiki.njk`, `vault=catz` |
| `.github/workflows/build-deploy.yml` | Build + deploy on push and `repository_dispatch` |
| `.gitignore` | Add `_site/`, `node_modules/` |
| ~~`src/_data/vault.js`~~ | **Not implemented** — vault identity injected via per-directory `.json` data files. No global data file needed in v1. |

### Modified files in `growdirectprez/canary-site`

| File | Change |
|---|---|
| (existing `rapidpos/*.html`) | Moved into `src/rapidpos/` — Eleventy pass-through |

### New files in each vault repo (`growdirect-llc/ncr`, `canary-retail-brain`, `catz`)

| File | Purpose |
|---|---|
| `.github/workflows/notify-canary.yml` | Fires `repository_dispatch` to `canary-site` on markdown push |

---

## Chunk 1: Repository setup + Eleventy scaffold

### Task 1: Clone canary-site and restructure for Eleventy

**Repos touched:** `growdirectprez/canary-site`

- [ ] **Step 1: Clone canary-site**

```bash
TMPDIR=/tmp/canary-site-dev-$$
gh repo clone growdirectprez/canary-site $TMPDIR
cd $TMPDIR
```

- [ ] **Step 2: Create `src/` directory, move existing static files into `src/rapidpos/`**

```bash
mkdir -p src/rapidpos
# Move all existing rapidpos HTML files into src/rapidpos/
mv rapidpos/*.html src/rapidpos/
rmdir rapidpos
```

- [ ] **Step 3: Create `.gitignore`**

```bash
cat > .gitignore << 'EOF'
_site/
node_modules/
.DS_Store
EOF
```

- [ ] **Step 4: Verify git status — only renames and new .gitignore**

```bash
git status
# Expected: renamed rapidpos/*.html → src/rapidpos/*.html, new .gitignore
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: restructure — move static pages into src/rapidpos/, add .gitignore"
```

---

### Task 2: Add git submodules for vault content

**Repos touched:** `growdirectprez/canary-site`

- [ ] **Step 1: Add the three vault repos as submodules**

```bash
git submodule add https://github.com/growdirect-llc/ncr.git content/ncr
git submodule add https://github.com/growdirect-llc/canary-retail-brain.git content/crb
git submodule add https://github.com/growdirect-llc/catz.git content/catz
```

- [ ] **Step 2: Verify submodule content is present**

```bash
ls content/ncr/   # should show: Home.md, modules/, integration/, etc.
ls content/crb/   # should show: Home.md, platform/, modules/, etc.
ls content/catz/  # should show: Home.md, method/, agents/, etc.
```

- [ ] **Step 3: Commit submodule registration**

```bash
git add .gitmodules content/
git commit -m "chore: add NCR, CRB, CATz as git submodules under content/"
```

---

### Task 3: Create committed symlinks for Eleventy input

**Why symlinks:** Eleventy's input directory is `src/`. Vault content lives in `content/`. Symlinks committed to the repo let Eleventy traverse them without any workflow step.

- [ ] **Step 1: Create symlinks from `src/rapidpos/` into each vault submodule**

From `src/rapidpos/`, the repo root is two levels up (`../..`), then `content/<vault>`.

```bash
cd src/rapidpos
ln -s ../../content/ncr ncr
ln -s ../../content/crb crb
ln -s ../../content/catz catz
cd ../..
```

- [ ] **Step 2: Verify symlinks resolve correctly — must show actual files, not an error**

```bash
ls -la src/rapidpos/ncr  # → ../../content/ncr
ls src/rapidpos/ncr/     # must list vault files: Home.md, modules/, etc.
# If you see "No such file or directory", the symlink depth is wrong — re-check from repo root
```

- [ ] **Step 3: Commit symlinks**

```bash
git add src/rapidpos/ncr src/rapidpos/crb src/rapidpos/catz
git commit -m "chore: add committed symlinks for vault content under src/rapidpos/"
```

---

### Task 4: Install Eleventy and create package.json

- [ ] **Step 1: Create `package.json`**

```bash
cat > package.json << 'EOF'
{
  "name": "canary-site",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build": "eleventy",
    "serve": "eleventy --serve --port 4000"
  },
  "devDependencies": {
    "@11ty/eleventy": "^3.0.0",
    "markdown-it": "^14.1.0",
    "markdown-it-wikilinks": "^1.4.0",
    "markdown-it-obsidian-callouts": "^1.0.0"
  }
}
EOF
```

- [ ] **Step 2: Install dependencies**

```bash
npm install
```

Expected: `node_modules/` created, `package-lock.json` generated. No errors.

- [ ] **Step 3: Commit package files (not node_modules — that's in .gitignore)**

```bash
git add package.json package-lock.json
git commit -m "chore: add Eleventy 3 + markdown-it dependencies"
```

---

### Task 5: Create slug utility

**File:** `src/_utils/slug.js`

This function is used by both Eleventy's permalink computation (via `.eleventy.js`) and the wikilink plugin's `postProcessPagePath`. They must produce identical output or wikilinks will 404.

- [ ] **Step 1: Create the utils directory and slug function**

```bash
mkdir -p src/_utils
cat > src/_utils/slug.js << 'EOF'
/**
 * Shared slug function.
 * Used by: Eleventy permalink filter + markdown-it-wikilinks postProcessPagePath.
 * Both must use this exact function or wikilinks will produce 404s.
 */
module.exports = function slug(str) {
  return str
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")   // strip special chars (em-dash, apostrophes, etc.)
    .replace(/[\s_]+/g, "-")    // spaces and underscores → hyphens
    .replace(/^-+|-+$/g, "");   // trim leading/trailing hyphens
};
EOF
```

- [ ] **Step 2: Verify function output manually — covers real vault filename patterns**

```bash
node -e "
const slug = require('./src/_utils/slug.js');
console.log(slug('T — Transaction Pipeline'));   // expect: t-transaction-pipeline
console.log(slug('R-Customer Record'));           // expect: r-customer-record
console.log(slug('Home'));                        // expect: home
console.log(slug('API (v2)'));                    // expect: api-v2
console.log(slug('Store 2030: The Vision'));      // expect: store-2030-the-vision
console.log(slug(\"It's a Test\"));              // expect: its-a-test
"
```

Expected output:
```
t-transaction-pipeline
r-customer-record
home
api-v2
store-2030-the-vision
its-a-test
```

If any output does not match, fix `slug.js` before continuing — a mismatch here means wikilinks will produce 404s in production.

- [ ] **Step 3: Commit**

```bash
git add src/_utils/slug.js
git commit -m "chore: add shared slug utility for consistent URL generation"
```

---

### Task 6: Create directory data files for vault layout injection

These JSON files tell Eleventy to use `wiki.njk` layout and inject vault identity for every markdown file under each vault symlink — without requiring frontmatter in the vault markdown files.

- [ ] **Step 1: Create vault directory data files**

```bash
cat > src/rapidpos/ncr.json << 'EOF'
{
  "layout": "wiki.njk",
  "vault": "ncr",
  "vaultLabel": "NCR Vault"
}
EOF

cat > src/rapidpos/crb.json << 'EOF'
{
  "layout": "wiki.njk",
  "vault": "crb",
  "vaultLabel": "Canary Retail Brain"
}
EOF

cat > src/rapidpos/catz.json << 'EOF'
{
  "layout": "wiki.njk",
  "vault": "catz",
  "vaultLabel": "CATz Method"
}
EOF
```

- [ ] **Step 2: Commit**

```bash
git add src/rapidpos/ncr.json src/rapidpos/crb.json src/rapidpos/catz.json
git commit -m "chore: add directory data files for vault layout injection"
```

---

### Task 7: Create `.eleventy.js`

- [ ] **Step 1: Create the Eleventy config**

```bash
cat > .eleventy.js << 'EOF'
const markdownIt = require("markdown-it");
const markdownItWikilinks = require("markdown-it-wikilinks");
const markdownItCallouts = require("markdown-it-obsidian-callouts");
const slug = require("./src/_utils/slug.js");

module.exports = function(eleventyConfig) {

  // ── Pass-through: static proposal HTML files ─────────────────────────────
  // The existing rapidpos/*.html pages have no .css or img/ assets (confirmed),
  // so only HTML pass-through is needed. Add .css / img/ here if assets are added later.
  eleventyConfig.addPassthroughCopy("src/rapidpos/*.html");

  // ── Ignore Quartz build artifacts and config inside vault submodules ──────
  // Quartz commits its built output (public/) back to main on each build.
  // Without these ignores, Eleventy processes thousands of Quartz HTML files.
  eleventyConfig.ignores.add("src/rapidpos/*/public/**");
  eleventyConfig.ignores.add("src/rapidpos/*/quartz/**");
  eleventyConfig.ignores.add("src/rapidpos/*/.obsidian/**");
  eleventyConfig.ignores.add("src/rapidpos/*/.github/**");
  eleventyConfig.ignores.add("src/rapidpos/*/node_modules/**");
  eleventyConfig.ignores.add("src/rapidpos/*/static/**");

  // ── Exclude draft:true pages from build ──────────────────────────────────
  eleventyConfig.addGlobalData("eleventyComputed", {
    eleventyExcludeFromCollections: (data) => data.draft === true,
  });
  eleventyConfig.addCollection("livePosts", (api) =>
    api.getAll().filter((p) => !p.data.draft)
  );

  // ── Markdown processor ────────────────────────────────────────────────────
  const md = markdownIt({ html: true, linkify: true, typographer: true })
    .use(markdownItWikilinks, {
      uriSuffix: "",                        // clean URLs — no .html extension
      makeAllLinksAbsolute: true,
      baseURL: "/rapidpos/",
      postProcessPagePath: (p) => slug(p),  // same slug fn as Eleventy
      postProcessLabel: (label) => label,
    })
    .use(markdownItCallouts);

  eleventyConfig.setLibrary("md", md);

  // ── Filters ───────────────────────────────────────────────────────────────

  // breadcrumb: URL string → array of path segments after /rapidpos/
  eleventyConfig.addFilter("breadcrumb", (url) => {
    return url
      .replace(/^\/rapidpos\//, "")
      .replace(/\/$/, "")
      .split("/")
      .filter(Boolean);
  });

  // vaultName: URL string → display label
  eleventyConfig.addFilter("vaultName", (url) => {
    if (url.startsWith("/rapidpos/ncr/"))  return "NCR";
    if (url.startsWith("/rapidpos/crb/"))  return "CRB";
    if (url.startsWith("/rapidpos/catz/")) return "CATz";
    return null;
  });

  // ── Sidebar nav collections ───────────────────────────────────────────────
  function buildVaultNav(api, vaultPrefix) {
    const pages = api
      .getFilteredByGlob(`src/rapidpos/${vaultPrefix}/**/*.md`)
      .filter((p) => !p.data.draft)
      .sort((a, b) => {
        const aIsIndex = a.fileSlug === "index" || a.fileSlug === "Home";
        const bIsIndex = b.fileSlug === "index" || b.fileSlug === "Home";
        if (aIsIndex && !bIsIndex) return -1;
        if (!aIsIndex && bIsIndex) return 1;
        return (a.data.title || a.fileSlug)
          .localeCompare(b.data.title || b.fileSlug);
      });

    const sections = {};
    for (const page of pages) {
      const rel = page.url
        .replace(`/rapidpos/${vaultPrefix}/`, "")
        .replace(/\/$/, "");
      const parts = rel.split("/");
      const sectionKey = parts.length > 1 ? parts[0] : "overview";
      const label = sectionKey
        .replace(/-/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());

      if (!sections[sectionKey]) sections[sectionKey] = { label, links: [] };
      sections[sectionKey].links.push({
        url:   page.url,
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
      input:    "src",
      output:   "_site",
      includes: "_includes",
      data:     "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine:     "njk",
  };
};
EOF
```

- [ ] **Step 2: Run a dry-run build to verify the config and modules load without errors**

```bash
npx eleventy --dryrun 2>&1 | head -40
```

Expected: Eleventy starts, lists files it would process, no `Error` or `Cannot find module` lines. The static HTML files appear as pass-through.

Note: `--dryrun` does NOT render Nunjucks templates — it only discovers files and loads config. Template errors (undefined filters, `wiki.njk` syntax issues) surface only in a full build (Task 11 Step 2). This step only gates config loading and module resolution.

If you see `Cannot find module 'markdown-it-obsidian-callouts'`, run `npm install` again and verify the package exists on npm: `npm info markdown-it-obsidian-callouts version`.

- [ ] **Step 3: Commit**

```bash
git add .eleventy.js
git commit -m "feat: add Eleventy 3 config with vault ignores, wikilinks, nav collections"
```

---

## Chunk 2: Templates — shared styles, nav, footer, wiki layout

### Task 8: Extract shared CSS into `shared-styles.njk`

The CSS lives in `src/rapidpos/wiki-template.html` between `<style>` (line 16) and `</style>` (line 585). Extract it verbatim — do not edit it.

- [ ] **Step 1: Create `src/_includes/` directory**

```bash
mkdir -p src/_includes
```

- [ ] **Step 2: Extract the `<style>` block from wiki-template.html using pattern matching (not line numbers)**

Pattern-based extraction is resilient to any future edits to wiki-template.html.

```bash
# Extract everything between <style> and </style> tags (exclusive)
sed -n '/<style>/,/<\/style>/p' src/rapidpos/wiki-template.html \
  | tail -n +2 | head -n -1 > /tmp/css-body.tmp

# Wrap with tags and write the include
{
  echo "<style>"
  cat /tmp/css-body.tmp
  echo "</style>"
} > src/_includes/shared-styles.njk

rm /tmp/css-body.tmp
```

- [ ] **Step 3: Verify the file starts and ends correctly**

```bash
head -3 src/_includes/shared-styles.njk   # line 1: <style>  line 2: :root {
tail -3 src/_includes/shared-styles.njk   # last line: </style>
wc -l src/_includes/shared-styles.njk     # should be ~570 lines
grep -c "var(--green-dark)" src/_includes/shared-styles.njk  # should be > 0
```

- [ ] **Step 4: Commit**

```bash
git add src/_includes/shared-styles.njk
git commit -m "feat: extract shared CSS into shared-styles.njk include"
```

---

### Task 9: Extract top nav into `nav.njk`

The nav HTML lives in `src/rapidpos/index.html` between `<nav class="nav"` (line 495) and `</nav>` (line 513).

- [ ] **Step 1: Extract the nav block**

```bash
sed -n '495,513p' src/rapidpos/index.html > src/_includes/nav.njk
```

- [ ] **Step 2: Verify content**

```bash
cat src/_includes/nav.njk
# Should show: <nav class="nav"...> with logo, page links, CTA button, </nav>
```

- [ ] **Step 3: Commit**

```bash
git add src/_includes/nav.njk
git commit -m "feat: extract shared top nav into nav.njk include"
```

---

### Task 10: Create `footer.njk`

Extract the footer from `src/rapidpos/index.html` (from `<footer` to `</footer>`).

- [ ] **Step 1: Find footer line range**

```bash
grep -n "<footer\|</footer" src/rapidpos/index.html
```

Note the line numbers from the output.

- [ ] **Step 2: Extract footer**

```bash
# Replace START and END with the line numbers from Step 1
sed -n 'START,ENDp' src/rapidpos/index.html > src/_includes/footer.njk
```

- [ ] **Step 3: Verify**

```bash
cat src/_includes/footer.njk
# Should show: <footer class="footer">...</footer>
```

- [ ] **Step 4: Commit**

```bash
git add src/_includes/footer.njk
git commit -m "feat: extract shared footer into footer.njk include"
```

---

### Task 11: Create `wiki.njk` layout template

This is the wiki page shell. It uses all three includes above and injects the Eleventy `{{ content }}` variable.

- [ ] **Step 1: Create `src/_includes/wiki.njk`**

```bash
cat > src/_includes/wiki.njk << 'NJKEOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ title or fileSlug | replace("-", " ") | title }} — Canary {{ vaultLabel }}</title>
  {% if description %}<meta name="description" content="{{ description }}">{% endif %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
  {% include "shared-styles.njk" %}
</head>
<body>
  {% include "nav.njk" %}

  <div class="wiki-layout">
    <aside class="wiki-sidebar" aria-label="Vault navigation">
      <div class="wiki-vault-header">
        <span class="label">{{ vaultLabel | upper }}</span>
      </div>

      {% set navKey = vault + "Nav" %}
      {% set navCollection = collections[navKey] %}
      {% if navCollection and navCollection.length %}
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
        <div class="switcher-row">
          <a href="/rapidpos/ncr/"  class="vault-link{% if vault == 'ncr' %}  active{% endif %}">NCR</a>
          <a href="/rapidpos/crb/"  class="vault-link{% if vault == 'crb' %}  active{% endif %}">CRB</a>
          <a href="/rapidpos/catz/" class="vault-link{% if vault == 'catz' %} active{% endif %}">CATz</a>
        </div>
      </div>
    </aside>

    <main class="wiki-content">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/rapidpos/">RapidPOS</a>
        {% for crumb in page.url | breadcrumb %}
          <span class="sep">›</span>
          <span class="{% if loop.last %}current{% endif %}">
            {{ crumb | replace("-", " ") | title }}
          </span>
        {% endfor %}
      </nav>

      <article>
        {{ content | safe }}
      </article>
    </main>
  </div>

  {% include "footer.njk" %}
</body>
</html>
NJKEOF
```

- [ ] **Step 2: Run a full local build and verify no template errors**

```bash
npm run build 2>&1 | tail -20
```

Expected: build completes, output like:
```
[11ty] Wrote NNN files in X.Xs (vN.N.N)
```

No `TemplateRenderError`, no `Error`, no `undefined is not iterable`.

If the build fails with a `Cannot find module` error, run `npm install` again.
If the build fails with a Nunjucks template error, check the error line number in `wiki.njk`.

- [ ] **Step 3: Spot-check build output — verify a vault page was generated**

```bash
# Should exist and contain wiki-layout HTML
ls _site/rapidpos/ncr/
cat _site/rapidpos/ncr/index.html | grep -c "wiki-sidebar"
# Expected: 1 (the sidebar div is present)
```

- [ ] **Step 4: Serve locally and visually verify one vault page**

```bash
npm run serve
# Open http://localhost:4000/rapidpos/ncr/ in browser
# Verify: top nav present, sidebar with vault nav links, breadcrumb, content rendered
```

- [ ] **Step 5: Commit**

```bash
git add src/_includes/wiki.njk
git commit -m "feat: add wiki.njk layout — sidebar, breadcrumb, vault switcher"
```

---

## Chunk 3: GitHub Actions — build/deploy + cross-repo triggers

### Task 12: Create `build-deploy.yml` for canary-site

This replaces the implicit branch-served Pages deployment with an explicit Actions build. Note: this workflow will not activate until the Pages source is switched in Task 14.

- [ ] **Step 1: Create the workflow**

```bash
mkdir -p .github/workflows
cat > .github/workflows/build-deploy.yml << 'EOF'
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

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout with submodules
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
          # All vault repos are public — GITHUB_TOKEN is sufficient

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
EOF
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/build-deploy.yml
git commit -m "feat: add GitHub Actions build-deploy workflow for Eleventy + Pages"
```

- [ ] **Step 3: Push canary-site to remote**

```bash
git pull --rebase
git push
```

The push will trigger the existing branch-served Pages (no harm — it just deploys the current `main` state via the old method until we switch in Task 14).

---

### Task 13: Create PAT and add notify workflows to vault repos

This task requires a GitHub personal access token to be created in the browser. It cannot be automated — it's a one-time manual step.

- [ ] **Step 1: Create fine-grained PAT (manual — browser required)**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Token name: `canary-site-dispatch`
4. Resource owner: `growdirectprez`
5. Repository access: Only select repositories → `growdirectprez/canary-site`
6. Permissions → Repository permissions → Actions: **Read and Write**
7. Generate token — copy the value immediately

- [ ] **Step 2: Add the PAT as a secret to all three vault repos**

```bash
# Replace TOKEN_VALUE with the actual PAT from Step 1
gh secret set CANARY_SITE_DISPATCH_TOKEN \
  --body "TOKEN_VALUE" \
  --repo growdirect-llc/ncr

gh secret set CANARY_SITE_DISPATCH_TOKEN \
  --body "TOKEN_VALUE" \
  --repo growdirect-llc/canary-retail-brain

gh secret set CANARY_SITE_DISPATCH_TOKEN \
  --body "TOKEN_VALUE" \
  --repo growdirect-llc/catz
```

Expected: no errors, secret set confirmation for each repo.

- [ ] **Step 3: Add `notify-canary.yml` to each vault repo**

```bash
for REPO in ncr canary-retail-brain catz; do
  TMPDIR=/tmp/${REPO}-notify-$$
  gh repo clone growdirect-llc/$REPO $TMPDIR
  mkdir -p $TMPDIR/.github/workflows
  cat > $TMPDIR/.github/workflows/notify-canary.yml << 'EOF'
name: Notify canary-site on content change

on:
  push:
    branches: [main]
    paths: ["**/*.md"]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Dispatch rebuild to canary-site
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.CANARY_SITE_DISPATCH_TOKEN }}
          repository: growdirectprez/canary-site
          event-type: vault-updated
          client-payload: '{"vault":"${{ github.repository }}","sha":"${{ github.sha }}"}'
EOF
  git -C $TMPDIR add .github/workflows/notify-canary.yml
  git -C $TMPDIR commit -m "feat: notify canary-site on markdown push"
  git -C $TMPDIR pull --rebase
  git -C $TMPDIR push
  rm -rf $TMPDIR
done
```

- [ ] **Step 4: Verify workflows appear in each vault repo**

```bash
for REPO in ncr canary-retail-brain catz; do
  echo "=== $REPO ==="
  gh api repos/growdirect-llc/$REPO/actions/workflows --jq '.workflows[].name'
done
```

Expected: `Notify canary-site on content change` listed for each repo.

---

### Task 14: Switch canary-site Pages from branch-served to workflow

**This causes a ~2–5 minute outage for `canary.growdirect.io`.** The site goes offline when Pages config is deleted and comes back after the first Actions deployment completes.

- [ ] **Step 1: Confirm current Pages config is `legacy` (branch-served)**

```bash
gh api repos/growdirectprez/canary-site/pages --jq '.build_type'
# Expected: "legacy"
```

- [ ] **Step 2: Delete current Pages config**

```bash
gh api --method DELETE repos/growdirectprez/canary-site/pages
echo "Pages config deleted — site is offline"
```

- [ ] **Step 3: Wait for deletion to propagate (not just sleep — verify)**

```bash
until ! gh api repos/growdirectprez/canary-site/pages 2>/dev/null | grep -q "html_url"; do
  echo "Waiting for Pages deletion..."; sleep 5
done
echo "Pages config gone"
```

- [ ] **Step 4: Re-enable Pages with workflow build type**

```bash
gh api --method POST repos/growdirectprez/canary-site/pages \
  -F "build_type=workflow" \
  --jq '.status'
# Expected: "queued" or "built"
```

- [ ] **Step 5: Trigger first Actions deployment by pushing an empty commit**

```bash
# Re-clone if you no longer have a local copy — don't rely on $TMPDIR from Task 12
CANARY=/tmp/canary-site-deploy-$$
gh repo clone growdirectprez/canary-site $CANARY
git -C $CANARY pull
git -C $CANARY commit --allow-empty -m "chore: trigger first Eleventy Pages deployment"
git -C $CANARY push
rm -rf $CANARY
```

- [ ] **Step 6: Monitor the Actions run until complete**

```bash
until gh api repos/growdirectprez/canary-site/actions/runs \
  --jq '.workflow_runs[0].conclusion' | grep -q "success\|failure"; do
  echo "Build in progress..."; sleep 10
done
gh api repos/growdirectprez/canary-site/actions/runs \
  --jq '.workflow_runs[0]|{status,conclusion,name}'
# Expected: {"status":"completed","conclusion":"success","name":"Build and deploy"}
```

- [ ] **Step 7: Verify site is live**

```bash
curl -s -o /dev/null -w "%{http_code}" https://canary.growdirect.io/
# Expected: 200

curl -s -o /dev/null -w "%{http_code}" https://canary.growdirect.io/rapidpos/
# Expected: 200

curl -s -o /dev/null -w "%{http_code}" https://canary.growdirect.io/rapidpos/ncr/
# Expected: 200
```

---

## Chunk 4: End-to-end verification

### Task 15: Verify full update pipeline

Confirm that a vault markdown change flows all the way through to the live site automatically.

- [ ] **Step 1: Make a trivial markdown edit in the NCR vault**

```bash
TMPDIR=/tmp/ncr-test-$$
gh repo clone growdirect-llc/ncr $TMPDIR
# Add a test line to Home.md
echo "" >> $TMPDIR/Home.md
echo "<!-- canary-site integration verified $(date -u +%Y-%m-%dT%H:%M:%SZ) -->" >> $TMPDIR/Home.md
git -C $TMPDIR add Home.md
git -C $TMPDIR commit -m "chore: verify canary-site integration"
git -C $TMPDIR pull --rebase
git -C $TMPDIR push
rm -rf $TMPDIR
```

- [ ] **Step 2: Verify NCR vault dispatched the event to canary-site**

```bash
# Give it 15 seconds for the NCR workflow to run
sleep 15
gh api repos/growdirect-llc/ncr/actions/runs \
  --jq '.workflow_runs[0]|{status,conclusion,name}'
# Expected: {"status":"completed","conclusion":"success","name":"Notify canary-site on content change"}
```

- [ ] **Step 3: Monitor the canary-site build triggered by the dispatch**

```bash
until gh api repos/growdirectprez/canary-site/actions/runs \
  --jq '.workflow_runs[0].conclusion' | grep -q "success\|failure"; do
  echo "Canary-site rebuilding..."; sleep 10
done
gh api repos/growdirectprez/canary-site/actions/runs \
  --jq '.workflow_runs[0]|{status,conclusion,name}'
# Expected: {"status":"completed","conclusion":"success","name":"Build and deploy"}
```

- [ ] **Step 4: Verify the updated NCR home page is live**

```bash
curl -s https://canary.growdirect.io/rapidpos/ncr/ | grep -c "wiki-sidebar"
# Expected: 1 — wiki layout is rendered

curl -s https://canary.growdirect.io/rapidpos/ncr/ | grep "canary-site integration verified"
# Expected: the HTML comment from Step 1 is present in the output
```

- [ ] **Step 5: Check all three vault home pages return 200**

```bash
for path in ncr crb catz; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://canary.growdirect.io/rapidpos/$path/)
  echo "$path: $STATUS"
done
# Expected: all three return 200
```

- [ ] **Step 6: Verify proposal pages still work (no regression)**

```bash
for page in "" "architecture" "endpoints" "integrate" "store-2030" "armstrong"; do
  URL="https://canary.growdirect.io/rapidpos/$page"
  [ -z "$page" ] && URL="https://canary.growdirect.io/rapidpos/"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  echo "$page (${URL##*/rapidpos/}): $STATUS"
done
# Expected: all return 200
```

- [ ] **Step 7: Clean up temp clone if still present**

```bash
rm -rf /tmp/canary-site-dev-* 2>/dev/null || true
```

---

## Update deployment wiki after completion

Once Task 15 passes, update `Brain/wiki/growdirect-public-sites-deployment.md` via the Obsidian MCP to note that `canary-site` now uses `build_type: workflow` (Eleventy), and document the update workflow:

```bash
# To update a vault (content auto-syncs to canary.growdirect.io/rapidpos/<vault>/)
REPO=growdirect-llc/ncr   # or canary-retail-brain, catz
TMPDIR=/tmp/$(basename $REPO)-$$
gh repo clone $REPO $TMPDIR
# edit markdown files...
git -C $TMPDIR add -A
git -C $TMPDIR commit -m "content: ..."
git -C $TMPDIR pull --rebase
git -C $TMPDIR push
rm -rf $TMPDIR
# canary-site rebuilds automatically in ~90 seconds
```
