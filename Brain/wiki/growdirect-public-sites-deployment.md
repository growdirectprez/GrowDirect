---
tags: [ops, deployment, github-pages, quartz, infrastructure]
last-compiled: 2026-04-26
needs-review: 2026-05-10
---

# GrowDirect Public Sites — Deployment

Four sites live under `growdirect-llc` on GitHub Pages. DNS is GoDaddy with CNAMEs pointing to `growdirect-llc.github.io`.

| Repo | Domain | Type |
|---|---|---|
| `growdirect-llc/proposal` | proposal.growdirect.io | Static HTML (single file) |
| `growdirect-llc/ncr` | ncr.growdirect.io | Quartz v4 vault |
| `growdirect-llc/canary-retail-brain` | crb.growdirect.io | Quartz v4 vault |
| `growdirect-llc/catz` | catz.growdirect.io | Quartz v4 vault |

---

## Proposal (proposal.growdirect.io)

Single self-contained HTML file. No build step. Pages serves directly from `main` branch root.

**Source file:** `/Users/gclyle/Desktop/proposal-index.html`

**To deploy an update:**
```bash
SHA=$(gh api repos/growdirect-llc/proposal/contents/index.html --jq '.sha')
CONTENT=$(base64 < /Users/gclyle/Desktop/proposal-index.html)
gh api --method PUT repos/growdirect-llc/proposal/contents/index.html \
  --field message="your commit message here" \
  --field content="$CONTENT" \
  --field sha="$SHA" \
  --jq '.commit.sha'
```

Pages config: Source = `main` branch, root `/`. CNAME file in repo root contains `proposal.growdirect.io`. No Actions workflow — Pages deploys directly from branch.

---

## Quartz Vaults (NCR, CRB, CATz)

Content-only repos. The Quartz framework is fetched and built by a GitHub Actions workflow (`Deploy Quartz site to GitHub Pages`) on every push to `main`. Pages is configured with `build_type: workflow`, not branch-served.

> **Critical:** Never switch these to branch-based Pages serving. If misconfigured, fix with `build_type: workflow` and push a commit to trigger a fresh build.

### Customization files committed in each vault

| File | Purpose |
|---|---|
| `quartz.config.ts` | Theme colors, plugins, baseUrl |
| `quartz.layout.ts` | Component layout (sidebar, explorer, TOC) |
| `quartz/styles/custom.scss` | CSS overrides — mobile, branding |
| `CNAME` | Custom domain (e.g. `ncr.growdirect.io`) |
| Markdown content | All vault content |

### Brand palette (quartz.config.ts — identical across all three)

```typescript
lightMode: {
  light: "#F5F0E8",        // parchment background
  lightgray: "#EAE4D6",
  gray: "#6B6B6B",
  darkgray: "#3A3A3A",
  dark: "#1C3A2B",         // green-dark text
  secondary: "#2A5240",    // green-mid
  tertiary: "#4CAF7D",     // green-light accent
  highlight: "rgba(28,58,43,0.06)",
  textHighlight: "#BF870044",
},
darkMode: {
  light: "#0f1c10",
  lightgray: "#1C3A2B",
  gray: "#4CAF7D",
  darkgray: "#C8C0B0",
  dark: "#F5F0E8",
  secondary: "#4CAF7D",
  tertiary: "#BF8700",     // gold accent
  highlight: "rgba(76,175,125,0.12)",
  textHighlight: "#BF870055",
}
```

Typography: `header: "Source Serif 4"` · `body: "Inter"` · `code: "IBM Plex Mono"`

### To update a vault

```bash
REPO=growdirect-llc/ncr   # or catz, canary-retail-brain
TMPDIR=/tmp/$(basename $REPO)-$$
gh repo clone $REPO $TMPDIR

# make changes...

git -C $TMPDIR add -A
git -C $TMPDIR commit -m "your message"
git -C $TMPDIR pull --rebase   # required — Actions commits back to main after each build
git -C $TMPDIR push
rm -rf $TMPDIR
```

Pull before push is not optional — Actions commits back to `main` during each build, so the remote is always ahead of a fresh clone.

### Verify build succeeded

```bash
gh api repos/growdirect-llc/ncr/actions/runs \
  --jq '.workflow_runs[0]|{status,conclusion,name}'
# expect: {"status":"completed","conclusion":"success","name":"Deploy Quartz site to GitHub Pages"}
```

**Check all four at once:**
```bash
for repo in proposal ncr canary-retail-brain catz; do
  echo "=== $repo ==="
  gh api repos/growdirect-llc/$repo/actions/runs \
    --jq '.workflow_runs[0]|{status,conclusion}' 2>/dev/null
done
```

---

## Troubleshooting

### Site returns 404 or raw markdown (Quartz vaults)
Most common cause: Pages switched to `build_type: legacy` (branch-served). Fix:

```bash
REPO=growdirect-llc/ncr  # replace as needed
gh api --method DELETE repos/$REPO/pages 2>/dev/null || true
sleep 3
gh api --method POST repos/$REPO/pages -F "build_type=workflow" --jq '.status'
# then push a commit to trigger a fresh build
git -C $TMPDIR commit --allow-empty -m "chore: trigger Pages redeploy"
git -C $TMPDIR push
```

### Proposal not loading
- Confirm Pages source is `main / root`
- Confirm CNAME file is present in repo root
- Confirm GoDaddy CNAME: `proposal` → `growdirect-llc.github.io`

### SSL not enforcing
GitHub auto-provisions after DNS validates (~5–30 min). Do not force via API — the PUT returns 204 and may error if cert isn't ready.

---

## Related

- [[Brain/projects/CATz]] — CATz vault project MOC
- [[Brain/projects/CanaryRetailBrain]] — CRB vault project MOC
- GRO-606 — Build Quartz knowledge sites for CATz and Canary Retail
