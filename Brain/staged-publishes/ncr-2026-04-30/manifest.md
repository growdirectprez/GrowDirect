---
classification: internal
type: publish-manifest
target-vault: ncr.growdirect.io (growdirect-llc/ncr)
target-branch: main
staged-at: 2026-04-30
status: dry-run — NOT pushed
allowlist: services/memory-bus/curation/ncr.yaml
---

# NCR Vault — Staged Publish 2026-04-30 (Dry Run)

**Status:** Staged for review. Not pushed. Awaiting founder approval after the 2026-05-01 RapidPOS Next Gen meeting and any feedback / sandbox-data follow-on.

## Why this push exists

The 2026-04-30 prep session for the RapidPOS Friday meeting produced a single new piece of public-safe positioning content — the five-phase Counterpoint modernization path. This is our point of view on how an NCR Counterpoint VAR delivers cloud-native modernization to their customers without forcing a register-UI rip-and-replace. The article is sanitized of confidential source material (Bart's internal DriftPOS architecture docs stay in `Brain/wiki/rapidpos-driftpos-platform-brief.md`, internal-only).

Pushing this to `ncr.growdirect.io` puts our POV in front of any VAR who lands on the site (Bart is on the Cloudflare Access whitelist; future VARs to be onboarded). It also gives the Friday meeting attendees a reference URL to share if Topic #2 conversation calls for it.

## Files staged in this push

| Source | Target in NCR vault | Role |
|--------|---------------------|------|
| `Brain/staged-publishes/ncr-2026-04-30/modernization/index.md` | `modernization/index.md` | New top-level section. Five-phase migration positioning. nav_order: 30. |

Single new file. New section. No edits to existing NCR vault content in this push.

## Frontmatter projection

Source frontmatter (Brain/wiki/ncr-counterpoint-modernization-path.md) has internal fields (`classification`, `companion`, `projects-to`, `source`, `source-evidence`). The staged version strips those and uses minimal NCR-vault frontmatter:

```yaml
---
title: Counterpoint Modernization — Without the Rip-and-Replace
nav_order: 30
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---
```

## IP-strip transforms applied

| Pattern in source | Replacement in staged | Rationale |
|---|---|---|
| `satoshi-precision cost truth` | `high-precision cost truth` | Satoshi-precision operating model is protected core IP; public copy uses generic precision language |
| `satoshi-cost migration` | `high-precision cost migration` | Same as above |
| `OTB is gated, not just reported` | `OTB is policy-gated, not just reported` | L402-gating language is protected core IP; public copy uses generic policy-gating language |

Internal stakeholder names (Bart, D'Orin, Tim, Matt, Geoff, Chris) — none appear in the source article body. No redaction needed.

## What's NOT in this push (intentionally held)

- **Brain/wiki/rapidpos-driftpos-platform-brief.md** — the internal DriftPOS analysis. Source material is from Bart's confidential Azure DevOps repos. Held in Brain only. Per `services/memory-bus/curation/ncr.yaml` deny list.
- **Brain/wiki/bart-mccleskey-rapid-garden-pos.md** — relationship profile with phone, email. Internal only. Per allowlist deny.
- **Brain/wiki/ncr-rapidpos-alignment-notes.md** and the **catz-** / **crb-** alignment notes — internal audit artifacts, not partner-facing.
- **L402 / satoshi / L2 protected-IP cards** — explicitly excluded from any public projection per allowlist `ip_protected` list.

## Push procedure (when approved)

Per CLAUDE.md "External Vaults — Clone on Demand," the push uses the transient clone pattern:

```bash
TMP=/tmp/ncr-publish-2026-04-30
gh repo clone growdirect-llc/ncr "$TMP"

# Copy staged payload
mkdir -p "$TMP/modernization"
cp Brain/staged-publishes/ncr-2026-04-30/modernization/index.md "$TMP/modernization/"

# Commit and push
git -C "$TMP" add modernization/
git -C "$TMP" commit -m "content(modernization): five-phase Counterpoint modernization path

Adds the modernization/ section with our point of view on how NCR
Counterpoint VARs deliver cloud-native, AI-native, multi-store
modernization to customers without forcing a register-UI rip-and-
replace. Five phases from observer to spine to platform takeover.

Authored 2026-04-30 in prep for RapidPOS Next Gen discussion. IP-stripped
per services/memory-bus/curation/ncr.yaml. Source-of-truth lives at
Brain/wiki/ncr-counterpoint-modernization-path.md."
git -C "$TMP" push origin main

rm -rf "$TMP"
```

Optional: a small `Home.md` edit on the same commit to add `[Modernization](modernization/)` to the top nav. Not authored as part of this dry run; if desired, add to a follow-up push.

## Verification after push

1. Site builds: GitHub Actions completes Quartz/build.py successfully
2. `https://ncr.growdirect.io/modernization/` returns the article
3. Top nav shows the new section (if Home.md was updated)
4. No build errors in the Actions log

## Hold reasons

- **Awaiting Friday meeting feedback.** Tomorrow's call may reveal positioning changes that affect the article. Better to push after, not before.
- **Awaiting sandbox-data confirmation.** If Bart provides Counterpoint sandbox access during the call, we may want to update Phase 0 description with concrete proof-of-concept language before the public push.
- **Founder has not given final review.** Per CLAUDE.md, public vault pushes require explicit confirmation in chat.

## Next session resume

If the Friday meeting reaffirms our POV (no major reframes), execute the push procedure above. If the meeting suggests changes, edit the source-of-truth article in Brain/wiki/ first, re-stage, then push.
