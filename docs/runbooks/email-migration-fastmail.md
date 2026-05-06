# Email Migration — GoDaddy M365 → Fastmail

Operational playbook for moving `growdirect.io` email off GoDaddy-brokered
Microsoft 365 onto Fastmail Standard. Work through this top to bottom over
one or two sessions. Check boxes as you go.

---

## Decisions made

- **New provider:** Fastmail Standard, $5/user/month
- **User seats:** 1 (solo founder; all addresses as aliases on one mailbox)
- **Primary mailbox:** `gclyle@growdirect.io`
- **Aliases on that mailbox:** `hello@`, `contact@`, + any others you add
- **Domain registration:** stays at GoDaddy (separate decision; not in scope here)

---

## Critical path blocker — decide this first

The `gclyle@growdirect.io` mailbox has a half-enrolled Microsoft Authenticator
entry that's preventing sign-in. To migrate its mail history, you need IMAP
access to the old mailbox, which requires passing MFA.

**Pick one:**

- [ ] **A. Fix MFA, preserve history.** Call GoDaddy (480-505-8877). Script:
      *"I have Microsoft 365 through GoDaddy on growdirect.io. I'm locked
      out of MFA on user mailbox gclyle@growdirect.io. Please reset MFA on
      that user so I can re-enroll Authenticator."* After reset, sign in at
      `outlook.office.com`, re-enroll fresh, then proceed with full migration.
      **Time: ~30 min call + enrollment.**
- [ ] **B. Skip gclyle@ history, start clean.** Don't fix MFA. Migrate
      `hello@` and any other non-locked mailboxes, cutover DNS, accept that
      gclyle@'s back-catalog is gone. **Time: 0 min.**
- [ ] **C. Admin portal reset.** If you have tenant admin on
      `admin.microsoft.com`, reset the gclyle@ password directly (wipes MFA
      in the process). Faster than GoDaddy support but requires admin
      credentials.

Record your choice: ________________________

---

## Phase 1 — Fastmail setup (no impact on live email)

Everything in this phase is additive. Your current GoDaddy email keeps
working. Nothing breaks.

- [ ] Go to `fastmail.com`, sign up for a Standard plan. Use a personal
      email (gmail, hotmail — anything not `@growdirect.io`) to create the
      account.
- [ ] Fastmail admin → Domains → Add domain → enter `growdirect.io`.
- [ ] Fastmail gives you a TXT record for domain verification. Add it at
      GoDaddy DNS (Products → DNS → Manage DNS for growdirect.io). Leave
      all other records alone. Wait ~15 min, click Verify in Fastmail.
- [ ] In Fastmail → Settings → Mail → Identities/Aliases:
  - Primary address: `gclyle@growdirect.io`
  - Add alias: `hello@growdirect.io`
  - Add alias: `contact@growdirect.io`
  - (Add any others you want)
- [ ] For each alias, set up a send identity so you can send *from* that
      address. Fastmail prompts you.
- [ ] Optional: enable catch-all (Settings → Domains → growdirect.io →
      Catch-all → route to gclyle@). Lets you hand out one-off addresses
      without pre-creating them.

---

## Phase 2 — Migrate existing mail (before cutover)

Only applicable if you picked option A or C above. Skip this phase if you
picked B.

- [ ] Fastmail → Settings → Import → IMAP.
- [ ] For each old mailbox:
  - Server: `outlook.office365.com`
  - Port: 993, SSL
  - Username: full email address (e.g., `hello@growdirect.io`)
  - Password: mailbox password (after MFA reset if applicable)
  - Run the import. Can take minutes to hours depending on mail volume.
- [ ] After import completes, spot-check in Fastmail web UI that folders
      and messages look right.

---

## Phase 3 — Cutover (DNS swap)

This is the moment live mail flips. Do it when you have 15 uninterrupted
minutes. Mail delivery may be spotty for up to an hour during propagation.
**Best done in the morning on a weekday** so you're around if anything
breaks.

### Records to REMOVE from GoDaddy DNS

- [ ] MX `@` priority 0 → `growdirect-io.mail.protection.outlook.com`
- [ ] CNAME `autodiscover` → `autodiscover.outlook.com`
- [ ] CNAME `email` → `email.secureserver.net`
- [ ] TXT `@` → `v=spf1 include:secureserver.net -all`
- [ ] TXT `@` → `NETORGFT19175160.onmicrosoft.com` (Microsoft tenant
      verification — only remove AFTER you've canceled the GoDaddy M365
      subscription; otherwise Microsoft may re-verify and re-route)

### Records to ADD to GoDaddy DNS

Use Fastmail's onboarding wizard as authoritative — values below are
templates, but Fastmail will show you the exact values with your account
details baked in.

- [ ] MX `@` priority 10 → `in1-smtp.messagingengine.com`
- [ ] MX `@` priority 20 → `in2-smtp.messagingengine.com`
- [ ] TXT `@` → `v=spf1 include:spf.messagingengine.com ?all`
      (use `?all` during migration to be lenient; tighten to `-all` later)
- [ ] CNAME `fm1._domainkey` → `fm1.growdirect.io.dkim.fmhosted.com`
- [ ] CNAME `fm2._domainkey` → `fm2.growdirect.io.dkim.fmhosted.com`
- [ ] CNAME `fm3._domainkey` → `fm3.growdirect.io.dkim.fmhosted.com`
- [ ] TXT `_dmarc` → `v=DMARC1; p=none; rua=mailto:gclyle@growdirect.io`
      (start permissive with `p=none`, tighten to `p=quarantine` later
      after 2+ weeks of clean DMARC reports)

### Propagation

- [ ] Save. DNS typically updates within an hour but can take up to 48h
      globally. Use `https://mxtoolbox.com/SuperTool.aspx` and enter
      `growdirect.io` → MX Lookup to watch for the change.

---

## Phase 4 — Verification

- [ ] Send a test email to `gclyle@growdirect.io` from an outside account
      (gmail, etc.). Confirm it arrives in Fastmail.
- [ ] Repeat for `hello@`, `contact@`.
- [ ] Send a test email FROM each alias out to
      `test-xxxxxx@mail-tester.com`. Visit the provided URL to get a
      deliverability score. You want 9/10 or 10/10. If lower, Fastmail's
      docs explain each check.
- [ ] Reply to a test and confirm it sends from the right identity.

---

## Phase 5 — Configure Apple Mail

- [ ] Mail → Settings → Accounts → **+**
- [ ] Choose **Fastmail** if offered, or **Other Mail Account** →
      auto-config should find it from the domain.
- [ ] Email: `gclyle@growdirect.io`
- [ ] Password: your Fastmail password (or an app-specific password
      generated at Fastmail → Settings → Password & Security → App
      Passwords — recommended)
- [ ] Aliases show up as send-from options automatically.
- [ ] Repeat on iPhone (Settings → Mail → Accounts → Add Account →
      Fastmail).
- [ ] Optional: add CalDAV (calendar) and CardDAV (contacts) accounts to
      Apple Calendar / Contacts using the server values Fastmail lists
      under Settings → Devices.

---

## Phase 6 — Decommission GoDaddy email

**Wait at least 7 days after cutover** before canceling. This catches any
stragglers still using cached old MX records.

- [ ] Week after cutover, confirm no new mail landing in old mailboxes
      (sign in at `outlook.office.com` with gclyle@ to check).
- [ ] GoDaddy → My Products → Email & Office → cancel the M365
      subscription.
- [ ] Remove the `NETORGFT19175160.onmicrosoft.com` TXT record from DNS
      (deferred from Phase 3 — safe now that subscription is canceled).
- [ ] Domain stays at GoDaddy as registrar; only email is gone.

---

## Post-migration cleanup (optional, do later)

- [ ] After 2 weeks of clean Fastmail operation, tighten SPF from
      `?all` to `-all`.
- [ ] After 2 weeks of clean DMARC reports, tighten DMARC from
      `p=none` to `p=quarantine`, then eventually `p=reject`.
- [ ] Update any service that sends mail from `@growdirect.io` (Postmark,
      SendGrid, Mailgun, transactional senders) to include their SPF in
      your SPF record, e.g.,
      `v=spf1 include:spf.messagingengine.com include:sendgrid.net -all`.
- [ ] Consider moving domain registration off GoDaddy to a cleaner
      registrar (Cloudflare, Porkbun). Not urgent.

---

## Current state snapshot (as of 2026-04-23)

For reference if anything goes sideways. GoDaddy DNS currently shows:

| Type  | Name           | Value                                          |
|-------|----------------|------------------------------------------------|
| MX    | @ (prio 0)     | growdirect-io.mail.protection.outlook.com      |
| CNAME | autodiscover   | autodiscover.outlook.com                       |
| CNAME | email          | email.secureserver.net                         |
| TXT   | @              | NETORGFT19175160.onmicrosoft.com               |
| TXT   | @              | v=spf1 include:secureserver.net -all           |

Tenant ID: `NETORGFT19175160.onmicrosoft.com`
Admin portal: `admin.microsoft.com`
GoDaddy support: 480-505-8877

Known mailboxes:
- `gclyle@growdirect.io` — MFA-locked, needs reset before migration
- `hello@growdirect.io` — state unknown, likely accessible

---

## Rollback plan

If cutover goes sideways and mail isn't flowing within 2 hours:

1. Revert MX record at GoDaddy back to `growdirect-io.mail.protection.outlook.com` priority 0.
2. Revert SPF TXT back to `v=spf1 include:secureserver.net -all`.
3. Remove Fastmail DKIM CNAMEs (they won't hurt anything but clean up).
4. Wait an hour for DNS to propagate back.
5. Mail resumes flowing to GoDaddy M365. Debug Fastmail setup at leisure.

Your old GoDaddy subscription is still active until Phase 6, so rollback
is always possible.
