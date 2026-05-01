---
card-type: runbook
card-id: runbook-workspace-admin
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [google-workspace, email, dns, admin, onboarding, offboarding, mfa, 2sv]
last-compiled: 2026-05-01
needs-review: false
---

## What this is

The operational runbook for Google Workspace on `growdirect.io`. Covers initial configuration state, mailbox and group management, MFA, and DNS record ownership.

## Configuration state (provisioned 2026-05-01)

**Tier:** Business Starter (or Standard — confirm in admin console)
**Primary mailbox:** `gclyle@growdirect.io`
**Registrar:** Cloudflare (transferred from GoDaddy per GRO-718)
**DNS authority:** Cloudflare zone `growdirect.io` — `arch.ns.cloudflare.com` / `sloan.ns.cloudflare.com`

### Mail DNS records

| Type | Name | Value | Status |
|------|------|-------|--------|
| MX | `@` | `aspmx.l.google.com` (pri 1) + 4 alts | ✅ Live |
| TXT | `@` | `v=spf1 include:_spf.google.com ~all` | ✅ Live |
| TXT | `google._domainkey` | DKIM 2048-bit key | ✅ Live |
| TXT | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:dmarc@growdirect.io` | Pending — escalate to `p=reject` after 30-day clean run |
| TXT | `@` | `google-site-verification=...` | ✅ Live |

### Groups (aliases → gclyle@growdirect.io)

| Address | Purpose |
|---------|---------|
| `hello@growdirect.io` | General inbound |
| `contact@growdirect.io` | General inbound |
| `support@growdirect.io` | Customer-facing (Canary, Cove) |
| `noreply@growdirect.io` | Transactional send-only (app magic links, alerts) |
| `partners@growdirect.io` | NCR VAR channel, co-sell inbound |
| `dmarc@growdirect.io` | DMARC aggregate report delivery |

## Procedures

### Add a new user
1. Admin console → Directory → Users → Add new user
2. Set temporary password, force reset on first login
3. Assign to appropriate OU if structure exists
4. Enforce 2SV enrollment within 24 hours of provisioning

### Remove a user (offboarding)
1. Admin console → Users → select user → Suspend (do not delete immediately)
2. Transfer Drive ownership to `gclyle@growdirect.io`
3. Set up mail forwarding to `gclyle@` for 30 days
4. After 30 days: delete user, release license
5. Rotate any shared credentials the user held

### Reset MFA / 2SV
1. Admin console → Users → select user → Security → 2-Step Verification → Turn off
2. User re-enrolls on next login
3. If security key is lost: remove specific key from user's account, do not disable 2SV policy

### Add a group alias
1. Admin console → Directory → Groups → Create group
2. Set group email, add `gclyle@growdirect.io` as member
3. Access type: Anyone on the internet can post (for external-facing aliases)
4. No need for a separate mailbox — Groups deliver to member inboxes

### Update DKIM key (annual rotation recommended)
1. Admin console → Apps → Google Workspace → Gmail → Authenticate email
2. Generate new key → copy TXT value
3. Add new record to Cloudflare DNS as `google._domainkey` (or use selector2 for zero-downtime rotation)
4. Activate in admin console
5. Delete old key after 48 hours

### DMARC escalation (after 30-day clean run)
1. Check DMARC reports delivered to `dmarc@growdirect.io`
2. If no legitimate failures: update Cloudflare DNS `_dmarc` TXT to `p=reject`
3. Keep `rua=mailto:dmarc@growdirect.io` in place for ongoing monitoring

## DMARC escalation gate

Current policy: `p=quarantine` — set 2026-05-01. Target escalation date: **2026-06-01**.
Escalate to `p=reject` only after reviewing aggregate reports and confirming zero legitimate mail sources outside SPF/DKIM alignment.

## Failure modes

**Symptom:** Mail to `@growdirect.io` bouncing  
**Check:** `dig MX growdirect.io` — verify Google MX records are live  
**Fix:** Re-add MX records in Cloudflare DNS if missing

---

**Symptom:** DKIM signature failures in DMARC reports  
**Check:** `dig TXT google._domainkey.growdirect.io` — verify record is present  
**Fix:** Re-activate DKIM in Workspace admin → Gmail → Authenticate email

---

**Symptom:** Group alias not delivering  
**Check:** Admin console → Groups → verify member list and posting permissions  
**Fix:** Confirm "Anyone on the internet can post" is enabled for external-facing groups

## Related

- GRO-718 — domain transfer off GoDaddy
- GRO-719 — Workspace provisioning dispatch
- `Brain/wiki/cards/runbook-cowork-memory-bus-setup.md` — memory bus setup (same pattern)
