---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Git Security + Repo Remote Fix
*Issued by ALX · February 26, 2026 · Priority: 🔴 CRITICAL*

## ⚠️ STATUS: COMPLETED & SUPERSEDED — March 3, 2026

This work order has been **completed**. The changes below have been applied:

- `canary-mvp` repo is **retired**. All code lives in `growdirect-ops`.
- Both machines use SSH authentication (`git@github.com:growdirectprez/growdirect-ops.git`).
- No HTTPS token URLs remain in any `.git/config`.
- All references to `canary-mvp` have been removed from operational files.

**Current state:**

| GitHub Repo | Purpose | Local Folder |
|---|---|---|
| `growdirectprez/growdirect-ops` | Canary LP application + ops | `GrowDirect/Canary/` |
| `growdirectprez/growdirect_website` | growdirect.io HTML site | Separate |

**canary-mvp is archived on GitHub. Do not use it.**

---

*Original work order preserved below for audit trail.*

---

## Original Context (February 26, 2026)

The exposed GitHub token has been revoked. No further damage possible from that token.
Two problems existed:

1. Wrong remote — `GrowDirect/Canary/` was pointing at `growdirect-ops`. At the time, we wanted it at `canary-mvp`.
2. No SSH keys — both machines needed SSH keys.

**Resolution:** SSH keys were configured. The decision was later made to consolidate everything into `growdirect-ops` (not `canary-mvp`). The remote now correctly points to `growdirect-ops`.

## Acceptance Criteria — Final Status

| # | Criterion | Status |
|---|---|---|
| AC-1 | Mac Mini SSH key added to GitHub | ✅ Done |
| AC-2 | iMac UAT SSH key added to GitHub | ✅ Done |
| AC-3 | Canary `.git/config` → `growdirect-ops.git` | ✅ Done (updated from canary-mvp) |
| AC-4 | growdirect-ops `.git/config` → `growdirect-ops.git` | ✅ Done |
| AC-5 | No HTTPS token URLs in any `.git/config` | ✅ Done |
| AC-6 | `git push origin main` succeeds without credentials prompt | ✅ Done |
| AC-7 | `.git-old` removed from Canary repo | ✅ Done |

*Closed by ALX, March 3, 2026.*
