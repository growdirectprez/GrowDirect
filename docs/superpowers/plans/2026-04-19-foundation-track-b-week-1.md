# Foundation Track B — Week 1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Note on adaptation:** This plan is legal-filing work, not code. The writing-plans skill's TDD pattern is adapted: each task has an artifact (filed document, stamped copy, confirmation) and a verification step (check the artifact / check the government portal / check the confirmation email) in place of a test. The bite-size / exact-path / frequent-commit discipline still applies.

**Goal:** File the Abalone Cove Foundation as a California Nonprofit Public Benefit Corporation, obtain EIN, adopt bylaws, and submit IRS Form 1023-EZ + CA Attorney General Form CT-1 + CA FTB Form 3500A — all within the 4–8 week window per Foundation spec §8 Track B, with Week 1 covering CA Articles filing, EIN issuance, and bylaws drafting.

**Architecture:** California Nonprofit Public Benefit Corporation under Corp. Code §§ 5110 et seq. Not Wyoming. Not Delaware. Confirmed in [`Brain/wiki/foundation-ca-formation.md`](../../../Brain/wiki/foundation-ca-formation.md). Standalone bylaws per Corp. Code §§ 5150–5152 (cannot borrow WPBCA's 2012 bylaws). Filing sequence: CA Articles (ARTS-PB-501(c)(3)) → EIN (IRS SS-4 online) → Board adopts bylaws → CA CT-1 + FTB 3500A → IRS Form 1023-EZ.

**Tech Stack:** CA Secretary of State bizfile online portal; IRS EIN online application; IRS Form 1023-EZ (Pay.gov); CA AG Registry of Charitable Trusts; CA FTB e-file; document templates drafted in plaintext markdown then exported to PDF where required.

**Parent spec:** [`docs/superpowers/specs/2026-04-18-abalone-cove-foundation-design.md`](../specs/2026-04-18-abalone-cove-foundation-design.md) §8 Track B + §9 Foundation Formation Specifics + Appendix "Entity Formation: California, Confirmed" + "Separate Bylaws Required."

**Sibling plan:** [`docs/superpowers/plans/2026-04-19-foundation-track-a-week-1.md`](2026-04-19-foundation-track-a-week-1.md) runs in parallel. Neither blocks the other.

**Supporting wiki:** `foundation-ca-formation.md`, `foundation-bylaws.md`, `foundation-legal-framework.md`, `foundation-three-hat-compensation.md`, `foundation-crypto-donations.md`, `foundation-llc-rescue-status.md`.

---

## Blocker Gates (per §14 Open Decisions)

| Gate | §14 item | Blocks | Default if user wants to proceed |
|---|---|---|---|
| **B-B1 — Foundation legal name** | §14.1 | CA Articles filing (T3) | Default: *Abalone Cove Foundation*. User to confirm or choose alternative before T3 |
| **B-B2 — Three initial directors** | §14.2 | Every task requiring board authorization (T4 onward) | **Hard blocker** — cannot proceed past T3 without this. User-identified candidates must be confirmed; director affidavits drafted |
| **B-B3 — Registered agent** | §14.3 | CA Articles filing (T3) | Default per spec §9: one of the directors personally for initial phase. Alternative: registered-agent service ($50–150/year) |
| **B-B4 — Fiscal year** | §14.5 | Bylaws (T5) + FTB 3500A (T8) | Default: calendar year (January 1 – December 31) per spec §9 |
| **B-B5 — Board counsel engagement** | §14.7 | Bylaws review (T5 verify step) | Options per spec: (a) existing CoAC counsel, (b) separate 501(c)(3) counsel, (c) both. Spec appendix recommends Foundation and CoAC have **separate** counsel |
| **B-B6 — Formation timing** | §14.8 | Whether to start this week | User decision to launch Track B. Gate is either open (proceed) or closed (hold the plan) |
| **B-B7 — Separate bylaws drafting sign-off** | Spec appendix "Separate Bylaws Required" | 1023-EZ filing (T9) | Either counsel-drafted or counsel-reviewed before submission. Do NOT submit 1023-EZ with un-reviewed bylaws |

**Gate clearance protocol:** each task lists the gates that block it. If a gate is open, stop at that task, surface to user, resume when cleared. Do not "default and proceed" on hard-blocker gates (B-B2, B-B5, B-B7).

---

## File Structure

All artifacts live in `Cove/docs/foundation/formation/` (new directory — Cove project's admin docs tree, NOT Brain). Filings themselves are submitted to state / federal portals; copies of everything are archived locally for chain of custody.

```
Cove/docs/foundation/formation/
├── 00-filing-checklist.md                        # Running checklist tracking all 7 filings
├── 01-articles-of-incorporation.md               # Draft CA ARTS-PB-501(c)(3) narrative
├── 01-articles-of-incorporation-FILED.pdf        # Filed-stamped copy from CA SOS
├── 02-ein-application.md                         # SS-4 field values (per IRS online form)
├── 02-ein-confirmation-letter.pdf                # IRS CP 575 EIN notice
├── 03-bylaws-draft.md                            # Foundation bylaws draft (Markdown)
├── 03-bylaws-adopted.pdf                         # Board-adopted bylaws (exported to PDF, signed)
├── 04-initial-board-minutes.md                   # First board meeting minutes (organizational)
├── 04-initial-board-minutes-signed.pdf           # Signed copy
├── 05-form-ct-1-draft.md                         # CA AG Registry of Charities Form CT-1
├── 05-form-ct-1-FILED.pdf                        # Filed / receipt
├── 06-form-3500A-draft.md                        # CA FTB Form 3500A state exemption
├── 06-form-3500A-FILED.pdf                       # Filed / confirmation
├── 07-form-1023-EZ-narrative.md                  # IRS 1023-EZ narrative content
├── 07-form-1023-EZ-FILED.pdf                     # IRS Pay.gov submission receipt
├── conflict-of-interest-policy.md                # IRS-required COI policy
├── director-affidavits/                          # One per director
│   ├── director-1-<lastname>.md
│   ├── director-2-<lastname>.md
│   └── director-3-<lastname>.md
└── chain-of-custody.md                           # Running log of all filings, receipts, dates
```

**Read these first (source wiki):**
- `Brain/wiki/foundation-ca-formation.md` — California as formation state, rationale
- `Brain/wiki/foundation-bylaws.md` — bylaws requirements (Corp. Code §§ 5150–5152, IRS 1023-EZ reqs)
- `Brain/wiki/foundation-three-hat-compensation.md` — compensation policy (WPBCA volunteer / Foundation paid / LLC commercial)
- `Brain/wiki/foundation-crypto-donations.md` — crypto gift acceptance policy (mandatory 24-48h conversion)
- `Brain/wiki/foundation-legal-framework.md` — overall legal framework
- Spec §9 — Foundation Formation Specifics (costs, timeline, forms)

**External references:**
- CA SOS bizfile online: https://bizfileonline.sos.ca.gov
- CA AG Registry of Charities: https://oag.ca.gov/charities/initial-reg
- IRS EIN online: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online
- IRS Form 1023-EZ: https://www.pay.gov (search "1023-EZ")
- CA FTB Form 3500A: https://www.ftb.ca.gov/forms

---

## Chunk 1: Pre-filing preparation (Gates B-B1, B-B2, B-B3)

### Task T1: Create the filing directory + running checklist

**Files:**
- Create: `Cove/docs/foundation/formation/00-filing-checklist.md`
- Create: `Cove/docs/foundation/formation/chain-of-custody.md`

**Gates:** none.

- [ ] **Step 1: Create directory**

Run:
```bash
cd ~/GrowDirect && mkdir -p Cove/docs/foundation/formation/director-affidavits
```

- [ ] **Step 2: Create `00-filing-checklist.md`**

Content: running table of the 7 filings with columns (Filing / Status / Submitted / Confirmed / Notes / File-path). Pre-populate with rows for:
1. CA Articles of Incorporation (ARTS-PB-501(c)(3))
2. IRS EIN (Form SS-4 online)
3. Bylaws adoption (initial board meeting)
4. Initial Board Meeting Minutes
5. CA AG Form CT-1 (Registry of Charities)
6. CA FTB Form 3500A (state tax exemption)
7. IRS Form 1023-EZ (federal tax exemption)

- [ ] **Step 3: Create `chain-of-custody.md`**

Header: "Every filing and correspondence logged here with date, sender/recipient, method (online / mail / email), confirmation number, and file-path to local archived copy. This is the official audit trail."

First entry: date, "Directory created; checklist initialized."

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/ && git commit -m "foundation(formation): create filing directory + checklist + chain-of-custody"
```

### Task T2: Director recruitment confirmation + affidavits

**Files:**
- Create: `Cove/docs/foundation/formation/director-affidavits/director-1-<lastname>.md`
- Create: `Cove/docs/foundation/formation/director-affidavits/director-2-<lastname>.md`
- Create: `Cove/docs/foundation/formation/director-affidavits/director-3-<lastname>.md`

**Gates:** **B-B2 (hard blocker).** If user has not identified 3 candidates, STOP and surface.

- [ ] **Step 1: Confirm 3 directors with user**

User action (not agent action): identify 3 informed allies per spec §8 Track B step 1. Recruitment is discrete; the directors should understand the plan before the site launches (see Track A T5).

Agent action: once user provides 3 names + contact info, proceed.

- [ ] **Step 2: For each director, draft an affidavit / acceptance letter**

Template per director:
- Full legal name
- Mailing address
- Contact (email + phone)
- Statement: "I accept appointment as an initial director of [FOUNDATION NAME per B-B1] upon its incorporation as a California Nonprofit Public Benefit Corporation."
- Disclosure: any potential conflicts of interest (per spec appendix "Separate Bylaws Required" — strong COI policy is a 1023-EZ requirement)
- Signature line + date

Officer-role assignment (per spec §9): President, Secretary, CFO (minimum officer set under CA nonprofit law). One director per role, or dual-hat acceptable if the other two roles are assigned.

- [ ] **Step 3: Verification**

Each affidavit must have:
- Legal name (matches government ID)
- California address (not required by law for directors — California Nonprofit Public Benefit Corp directors can be nonresident — but at least one director should be CA-resident for practical governance)
- Signed + dated
- Officer role if applicable

- [ ] **Step 4: Commit (with director names redacted if user prefers, or plaintext if public-OK)**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/director-affidavits/ && git commit -m "foundation(formation): initial director affidavits recorded"
```

**Note:** If user wants affidavits kept off-repo until Foundation is formed (privacy), skip the git add; store locally and log the existence + signed status in `chain-of-custody.md` only.

---

## Chunk 2: CA Articles of Incorporation (Gates B-B1, B-B2, B-B3)

### Task T3: Draft + file CA Articles of Incorporation (ARTS-PB-501(c)(3))

**Files:**
- Create: `Cove/docs/foundation/formation/01-articles-of-incorporation.md`
- Receive: `Cove/docs/foundation/formation/01-articles-of-incorporation-FILED.pdf`

**Gates:** B-B1 (name), B-B2 (directors), B-B3 (registered agent).

- [ ] **Step 1: Draft Articles narrative per CA Form ARTS-PB-501(c)(3)**

Required fields:
1. **Corporate Name** — per Gate B-B1; default: *Abalone Cove Foundation*
2. **Statement of Purpose** — verbatim from spec §3:
   > "Preservation of historical documentary records with continuing legal and civic significance; education of the community on the relationship between those records and contemporary land-use, preservation, and governance questions; advocacy for stewardship of scenic, ecological, and historical assets consistent with applicable regulatory frameworks."
3. **IRS-required 501(c)(3) language** — the CA ARTS-PB-501(c)(3) form's built-in Article states the corporation is organized exclusively for purposes under IRC §501(c)(3); that on dissolution assets go to another 501(c)(3) or government. Use the form's default text — do not modify.
4. **Service of Process** — per Gate B-B3. Either one of the directors (name + CA address) OR a registered agent service.
5. **Incorporator(s)** — typically one of the directors or the founding organizer. Signature required.

Source: `Brain/wiki/foundation-ca-formation.md`.

- [ ] **Step 2: Verification — pre-filing checks**

Before submitting:
1. **Name availability** — search CA SOS bizfile: https://bizfileonline.sos.ca.gov/search/business. If *Abalone Cove Foundation* is taken, flag to user immediately for B-B1 resolution.
2. **501(c)(3) form-specific** — confirm using ARTS-PB-501(c)(3) (the form for Public Benefit Corps electing 501(c)(3) tax status), NOT ARTS-PB (generic Public Benefit) or ARTS-MU (Mutual Benefit).
3. **Registered agent consent** — if using a director, confirm written consent in the affidavit (T2).
4. **Statement of purpose text** — matches spec §3 verbatim.

- [ ] **Step 3: File online via bizfile**

1. Log in to https://bizfileonline.sos.ca.gov with a California.gov account.
2. Submit ARTS-PB-501(c)(3).
3. Pay fee: $30 base + $25 expedited (optional but recommended) = $55 total.
4. Note confirmation number in `chain-of-custody.md` immediately.

Expected turnaround: ~3 days with expedited; ~6–8 weeks without.

- [ ] **Step 4: Await filed-stamp copy + archive**

When CA SOS returns the filed copy (PDF), download it. Save as `Cove/docs/foundation/formation/01-articles-of-incorporation-FILED.pdf`.

Verify: filed-stamp visible, filing date recorded, entity number assigned.

Update `00-filing-checklist.md` row 1: status → "Filed [date] — Entity No. [X]."

- [ ] **Step 5: Commit the filed PDF**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/01-articles-of-incorporation.md Cove/docs/foundation/formation/01-articles-of-incorporation-FILED.pdf Cove/docs/foundation/formation/00-filing-checklist.md Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): CA Articles filed — Entity No. [X]"
```

---

## Chunk 3: EIN + Bylaws (Gates B-B2, B-B4, B-B5, B-B7)

### Task T4: Obtain IRS EIN (Form SS-4 online)

**Files:**
- Create: `Cove/docs/foundation/formation/02-ein-application.md`
- Receive: `Cove/docs/foundation/formation/02-ein-confirmation-letter.pdf` (IRS CP 575)

**Gates:** B-B2 (need responsible party); Articles must be filed (T3 complete).

- [ ] **Step 1: Prepare SS-4 field values**

Draft in `02-ein-application.md`:
- Legal name of entity (must match CA Articles exactly)
- Trade name if different (leave blank unless applicable)
- Executor/Trustee/etc.: blank
- Mailing address (can be director's address, PO box, or registered-agent address)
- Principal office address (physical)
- Responsible party: one director — must be a person, not another entity. Name + SSN.
- Type of entity: "Other nonprofit organization" — Line 9a "Other" → "501(c)(3) charity"
- Reason for applying: "Started new business"
- Date business started: date of Articles filing (CA SOS filing date)
- Closing month of accounting year: per B-B4 — "December" if calendar year
- Highest number of employees expected in next 12 months: 0 (or honest estimate)
- Principal activity: "Historical preservation / community education"

**Source:** IRS Pub 1635.

- [ ] **Step 2: Apply online**

Go to https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online.

EIN is issued instantly at end of online application. Download the CP 575 PDF confirmation letter immediately (IRS will not resend).

- [ ] **Step 3: Archive**

Save as `02-ein-confirmation-letter.pdf`. Update `00-filing-checklist.md` row 2: "EIN: [9-digit-number], issued [date]."

- [ ] **Step 4: Verification**

Verify:
1. EIN matches the legal name on Articles
2. CP 575 letter is the official confirmation (not the summary screen)
3. Address on CP 575 matches mailing address on SS-4

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/02-* Cove/docs/foundation/formation/00-filing-checklist.md && git commit -m "foundation(formation): EIN issued [XX-XXXXXXX]"
```

### Task T5: Draft Foundation bylaws

**Files:**
- Create: `Cove/docs/foundation/formation/03-bylaws-draft.md`

**Gates:** B-B2 (directors named); B-B4 (fiscal year); B-B5 (counsel engagement — review before adoption); B-B7 (counsel sign-off before 1023-EZ).

- [ ] **Step 1: Draft bylaws per Corp. Code §§ 5150–5152 and IRS 1023-EZ requirements**

Structure (per spec appendix "Separate Bylaws Required"):
1. **Article I — Name, Offices, Fiscal Year.** Legal name per Gate B-B1; principal office address; fiscal year per Gate B-B4.
2. **Article II — Purpose.** Verbatim §3 purpose statement + IRC §501(c)(3) compliance language.
3. **Article III — Directors.** Minimum 3 per Cal. Corp. Code §5221; recommended 5–7 for resilience; terms (e.g., staggered 2-year); meeting cadence; quorum; voting.
4. **Article IV — Officers.** President, Secretary, CFO minimum; election / appointment / removal.
5. **Article V — Committees.** Authority to establish committees; standing committees (audit, COI, grants) optional.
6. **Article VI — Conflict of Interest Policy.** Full COI policy (IRS 1023-EZ requirement). Template in IRS Pub 4220 Appendix A is acceptable starting point.
7. **Article VII — Compensation.** **Critical — embed three-hat model per spec appendix:**
   - Reasonable compensation to the founder for Foundation-role work only
   - Founding-period (Q1 2026) pre-formation work ratification language
   - Disinterested-director review requirement (founder recused)
   - File-path allocation rule for categorizing time (per `foundation-three-hat-compensation.md`)
   - Target rate $50–$75/hr, $25–60k Y1 cap pending comparable-data validation
8. **Article VIII — Gift Acceptance.** Reference to separate Gift Acceptance Policy (see `foundation-crypto-donations.md`). Authorization for:
   - Cryptocurrency donations (mandatory 24–48h USD conversion unless board specifically approves holding)
   - Conservation easements
   - Other non-cash gifts
9. **Article IX — Dissolution.** On dissolution, assets go to another 501(c)(3) or government entity — IRS-required language.
10. **Article X — Supplemental Record-Keeping.** Authorization for cryptographic timestamping (OpenTimestamps / Bitcoin-anchored) as supplemental proof-of-record per spec appendix "Blockchain Proof Layer" — does NOT replace Davis-Stirling secret-ballot oversight.
11. **Article XI — Limitations.** Explicitly prohibit governance over CoAC, CHOA, or any HOA; prohibit candidate endorsement / electioneering (501(c)(3) political-activity guardrails).
12. **Article XII — Amendments.** Bylaw amendment procedure.

**Length target:** 10–20 pages per spec appendix.

- [ ] **Step 2: Verification — self-review**

Check:
1. §5150 conformance (no inconsistency with Articles)
2. No governance-over-HOA language (spec requirement)
3. COI policy included (IRS 1023-EZ requirement)
4. Three-hat compensation language present with disinterested-director review
5. Crypto + conservation-easement gift authorization present
6. OpenTimestamps record-keeping authorization present
7. No political-activity authorization

- [ ] **Step 3: Counsel review (Gate B-B5 / B-B7)**

If Gate B-B5 is "(a) existing CoAC counsel" or "(b) separate 501(c)(3) counsel" — route draft to counsel. **Do not adopt without counsel review if B-B7 requires counsel sign-off before 1023-EZ.**

If user wants to proceed without counsel: explicitly log in `chain-of-custody.md` that counsel review was waived by founder; retain the draft for later retroactive review.

- [ ] **Step 4: Commit draft (pre-adoption)**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/03-bylaws-draft.md && git commit -m "foundation(formation): bylaws draft — pre-adoption, pending board + counsel review"
```

### Task T6: Initial organizational board meeting + bylaws adoption

**Files:**
- Create: `Cove/docs/foundation/formation/04-initial-board-minutes.md`
- Receive: `04-initial-board-minutes-signed.pdf` + `03-bylaws-adopted.pdf`

**Gates:** B-B2 (directors), B-B5 + B-B7 (bylaws reviewed).

- [ ] **Step 1: Schedule organizational meeting**

Three directors per Cal. Corp. Code §5211. In-person or by unanimous written consent per §5211(b). Date logged in `chain-of-custody.md`.

- [ ] **Step 2: Draft minutes template**

Per §5211 and standard organizational-meeting agenda:
- Call to order / attendance
- Appointment of temporary chair + secretary
- Acknowledge filing of Articles (attach filed copy)
- Acknowledge receipt of EIN (attach CP 575)
- **Adopt bylaws** (attach final reviewed draft)
- Elect officers per Article IV
- Appoint registered agent (confirm from Articles)
- Designate bank(s) / authorize account opening
- **Adopt Conflict of Interest Policy** (per bylaws Article VI)
- **Adopt Gift Acceptance Policy** (per bylaws Article VIII; reference crypto-donation policy from `foundation-crypto-donations.md`)
- **Ratify founding-period pre-formation work** per bylaws Article VII
- Authorize filing of IRS 1023-EZ + CA CT-1 + FTB 3500A
- Adjournment

- [ ] **Step 3: Hold meeting + sign minutes**

Minutes signed by secretary; attested by chair. Export to PDF as `04-initial-board-minutes-signed.pdf`. Export adopted bylaws to PDF as `03-bylaws-adopted.pdf`.

- [ ] **Step 4: Update chain of custody**

Log: meeting held [date], [N] directors present, bylaws adopted, officers elected, COI + Gift Acceptance + ratification resolutions passed.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/03-bylaws-adopted.pdf Cove/docs/foundation/formation/04-initial-board-minutes.md Cove/docs/foundation/formation/04-initial-board-minutes-signed.pdf Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): initial board meeting held; bylaws adopted; officers elected"
```

---

## Chunk 4: State + Federal exemption filings (Gate B-B7)

### Task T7: File CA AG Form CT-1 (Registry of Charitable Trusts initial registration)

**Files:**
- Create: `Cove/docs/foundation/formation/05-form-ct-1-draft.md`
- Receive: `05-form-ct-1-FILED.pdf`

**Gates:** T3 complete (need Entity No.); T4 complete (need EIN); T6 complete (need adopted bylaws).

- [ ] **Step 1: Draft CT-1**

Required fields per CA AG form:
- Legal name (from Articles)
- Entity No. (from Articles filing)
- EIN (from CP 575)
- Mailing address
- Fiscal year end (per bylaws)
- Purposes (verbatim from Articles)
- Directors (from minutes)
- Officers (from minutes)
- Attach: Articles, bylaws, IRS determination letter (pending — can file CT-1 before 1023-EZ determination)

Fee: $50 initial registration (updated from spec's $25 — verify current fee on CA AG site before submission).

- [ ] **Step 2: Verification**

- Name / EIN / Entity No. match Articles + CP 575 exactly
- Attached bylaws match T6 adopted version
- Fiscal year matches bylaws

- [ ] **Step 3: File online**

https://oag.ca.gov/charities/initial-reg. Upload PDFs; pay fee; note confirmation in `chain-of-custody.md`.

- [ ] **Step 4: Archive confirmation**

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/05-* Cove/docs/foundation/formation/00-filing-checklist.md Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): CA AG CT-1 filed"
```

### Task T8: File CA FTB Form 3500A (state tax exemption)

**Files:**
- Create: `Cove/docs/foundation/formation/06-form-3500A-draft.md`
- Receive: `06-form-3500A-FILED.pdf`

**Gates:** T3 + T4 complete; ideally T9 (IRS 1023-EZ filed) — but 3500A can be filed contemporaneously and references the pending 1023-EZ.

- [ ] **Step 1: Draft 3500A**

CA FTB Form 3500A is the simplified state tax exemption form for organizations that have filed (or will file) IRS Form 1023/1023-EZ. Fields:
- Legal name + Entity No. + EIN
- Fiscal year
- Statement that organization has filed (or will file) 1023-EZ
- Attach: Articles, bylaws, IRS determination letter (when available)

No fee for 3500A.

- [ ] **Step 2: Verify + file**

https://www.ftb.ca.gov — locate Form 3500A. File online or by mail per current FTB guidance.

- [ ] **Step 3: Archive**

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/06-* Cove/docs/foundation/formation/00-filing-checklist.md Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): CA FTB 3500A filed"
```

### Task T9: File IRS Form 1023-EZ (federal 501(c)(3) exemption)

**Files:**
- Create: `Cove/docs/foundation/formation/07-form-1023-EZ-narrative.md`
- Receive: `07-form-1023-EZ-FILED.pdf` (Pay.gov receipt)

**Gates:** T3 + T4 + T6 complete; **B-B7 (counsel sign-off on bylaws before submission).**

- [ ] **Step 1: Eligibility check for 1023-EZ**

Per IRS Form 1023-EZ Eligibility Worksheet:
- Projected annual gross receipts < $50,000 (initial years)
- Projected total assets < $250,000
- Not a private foundation under §509(a)(3)
- Not a church, school, hospital, supporting org, etc.

If any "No" → must file full Form 1023 ($600, 6–12 month determination). **Check this before proceeding.**

Foundation (initial 3 years): expected < $50k gross receipts per spec §9 ($50K-$250K Year 1 estimate suggests may exceed $50K threshold — verify). **Ambiguity flag:** spec §9 cites "conservative estimate $50K–$250K Year 1" — this straddles the 1023-EZ threshold. If projected revenue ≥ $50k, must file full 1023.

- [ ] **Step 2: Decision point**

Based on step 1 eligibility:
- **If 1023-EZ eligible:** proceed
- **If must file full 1023:** STOP — the scope of this plan (1023-EZ, ~$275 fee, 2–4 week determination) does NOT cover full 1023. Surface to user; full 1023 adds 3–9 month timeline and $600 fee. Update plan before proceeding.

- [ ] **Step 3: Draft 1023-EZ narrative (if eligible)**

IRS Pay.gov form; narrative fields:
- Name, EIN, mailing address, state of incorporation, date of incorporation
- Purpose (matches Articles)
- NTEE code — for the Foundation, likely **A80 — Historical Societies & Historic Preservation** or **S21 — Community Improvement / Organizations**. Evaluate before filing.
- Activities: describe research, documentation, educational publishing, convening; ~250 words
- Attestation: bylaws include COI policy; no private-benefit / private-inurement
- Fee: $275 (Pay.gov)

Source: IRS Instructions for Form 1023-EZ.

- [ ] **Step 4: Counsel sign-off (Gate B-B7)**

If B-B7 requires counsel sign-off — route narrative + attached documents to counsel. Counsel confirms:
- No misrepresentation
- Bylaws as attached are consistent with narrative
- COI policy attached
- Compensation arrangements disclosed

Log sign-off in `chain-of-custody.md`.

- [ ] **Step 5: Submit via Pay.gov**

Log in to https://www.pay.gov; find 1023-EZ; complete + submit + pay $275. Download Pay.gov receipt as `07-form-1023-EZ-FILED.pdf`.

- [ ] **Step 6: Verification**

- Pay.gov tracking number logged in `chain-of-custody.md`
- Submission confirmation email received from IRS
- Local PDF archive saved

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/07-* Cove/docs/foundation/formation/00-filing-checklist.md Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): IRS 1023-EZ filed — Pay.gov tracking [XXX]"
```

### Task T10: Await IRS determination letter (Week 2–4 follow-up)

**Files:**
- Receive: IRS determination letter (typically 2–4 weeks for 1023-EZ per spec §9)

**Gates:** T9 complete.

- [ ] **Step 1: Poll Pay.gov / IRS portal weekly**

Week 2: check Pay.gov status.
Week 3: check; if no determination, file IRS Form 4506 status inquiry.
Week 4: if still pending, call IRS Tax Exempt / Government Entities line.

- [ ] **Step 2: On receipt of determination letter**

Save as `Cove/docs/foundation/formation/08-irs-determination-letter.pdf`. Update `00-filing-checklist.md` row 7: "Approved [date] — effective [incorporation date]."

- [ ] **Step 3: Trigger Track A handoff (T5 and T14 update)**

Notify Track A: directors confirmed (if they weren't already from T2) + Foundation status updated. Track A's placeholder text can now be replaced with "California Nonprofit Public Benefit Corporation, 501(c)(3) status effective [date]."

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect && git add Cove/docs/foundation/formation/08-* Cove/docs/foundation/formation/00-filing-checklist.md Cove/docs/foundation/formation/chain-of-custody.md && git commit -m "foundation(formation): IRS 501(c)(3) determination received — effective [date]"
```

---

## Exit criteria for Track B Week 1

Week 1 proper covers Tasks T1–T4 (directory, directors, Articles, EIN). Tasks T5–T10 extend through Weeks 2–4 per spec §9 timeline. The "Week 1" exit criteria:

- [ ] `Cove/docs/foundation/formation/` directory established with checklist + chain of custody
- [ ] 3 directors confirmed + affidavits signed (Gate B-B2 cleared)
- [ ] Foundation legal name locked (Gate B-B1 cleared)
- [ ] Registered agent designated (Gate B-B3 cleared)
- [ ] CA Articles filed — Entity No. received
- [ ] EIN issued and CP 575 archived
- [ ] Bylaws draft complete (pending counsel review per Gate B-B5 / B-B7)

**Through-Week-4 exit criteria:**

- [ ] Initial board meeting held; bylaws adopted; officers elected
- [ ] CA AG CT-1 filed
- [ ] CA FTB 3500A filed
- [ ] IRS 1023-EZ filed (or upgrade to full 1023 decision made)
- [ ] IRS determination letter received → Track A handoff to update status copy

## Post-formation backlog (not in this plan)

- Bank account opening (requires determination letter + EIN)
- Initial grant / donation intake (requires determination letter)
- State-level fundraising registration (CA-only initially; other states only if soliciting)
- Annual FTB + IRS filings (Form 199 / 990-N or 990-EZ depending on receipts)
- Wyoming LLC subsidiary evaluation (deferred per spec §13 — Epic 3, Year 2+)

## Gate summary (blockers the user must clear)

| Gate | What's needed | Blocks starting | Hard or soft |
|---|---|---|---|
| B-B1 | Foundation legal name confirmation | T3 | Soft (default: *Abalone Cove Foundation*) |
| B-B2 | 3 director identities + acceptance | T2, T3, T5, T6 | **Hard** |
| B-B3 | Registered agent (director vs. service) | T3 | Soft (default: one of the directors) |
| B-B4 | Fiscal year (calendar vs. other) | T5, T8 | Soft (default: calendar) |
| B-B5 | Board counsel engagement decision | T5 verify | Soft if user waives review; **hard** if required for 1023-EZ |
| B-B6 | Formation timing go/no-go | Any Track B task | User decision to launch |
| B-B7 | Counsel sign-off on bylaws before 1023-EZ | T9 | **Hard** if counsel engaged |
