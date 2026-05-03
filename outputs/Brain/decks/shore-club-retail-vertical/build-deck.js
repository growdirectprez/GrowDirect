// Shore Club retail-vertical deck — first-draft build
// Companion to outputs/memo-to-principals-retail-vertical.md
// 12 slides total: 10 main + 2 appendix
//
// HEADER NOTE FOR RECONCILIATION: The prior session's v1 deck did not surface
// in the wave's corpus load. This is a from-scratch first-draft build aligned
// to the launch prompt's required structure (cover with King Harbor anchor;
// three-lineage section divider; venture-instance overview with three-pillar
// genesis + RapidPOS + DriftPOS; compliance-by-architecture; throwaway-key /
// Lightning-operator forward optionality; closing values triad). When the v1
// surfaces, reconcile.

const PptxGenJS = require('pptxgenjs');
const path = require('path');

const pres = new PptxGenJS();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5

// Color palette — Ocean Gradient with cream accent
const NAVY = '21295C';
const DEEP = '065A82';
const TEAL = '1C7293';
const CREAM = 'ECE2D0';
const WHITE = 'FFFFFF';
const CHARCOAL = '36454F';
const SAND = 'F5F1E8';

const FONT_HEAD = 'Georgia';
const FONT_BODY = 'Calibri';

const SHORE_CLUB_LOGO = '/sessions/lucid-peaceful-tesla/mnt/GrowDirect/Cove/docs/brand/shore-club-original.png';

// Footer applied via slide master
pres.defineSlideMaster({
  title: 'MAIN',
  background: { color: WHITE },
  objects: [
    {
      text: {
        text: 'King Harbor — Redondo Beach — pier',
        options: {
          x: 0.4, y: 7.05, w: 6, h: 0.3,
          fontFace: FONT_BODY, fontSize: 9, color: CHARCOAL, italic: true,
        },
      },
    },
    {
      text: {
        text: 'eljeffe Hash and Seal Protocol',
        options: {
          x: 7.0, y: 7.05, w: 6.0, h: 0.3,
          fontFace: FONT_BODY, fontSize: 9, color: CHARCOAL, align: 'right',
        },
      },
    },
  ],
});

pres.defineSlideMaster({
  title: 'DARK',
  background: { color: NAVY },
  objects: [
    {
      text: {
        text: 'King Harbor — Redondo Beach — pier',
        options: {
          x: 0.4, y: 7.05, w: 6, h: 0.3,
          fontFace: FONT_BODY, fontSize: 9, color: CREAM, italic: true,
        },
      },
    },
    {
      text: {
        text: 'eljeffe Hash and Seal Protocol',
        options: {
          x: 7.0, y: 7.05, w: 6.0, h: 0.3,
          fontFace: FONT_BODY, fontSize: 9, color: CREAM, align: 'right',
        },
      },
    },
  ],
});

// ============================================================================
// SLIDE 1 — COVER
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'DARK' });

  s.addText('Retail vertical', {
    x: 0.7, y: 1.2, w: 12, h: 0.7,
    fontFace: FONT_HEAD, fontSize: 28, color: CREAM, italic: true,
  });

  s.addText('Proposed approach, structure, and 100-day plan', {
    x: 0.7, y: 1.9, w: 12, h: 1.0,
    fontFace: FONT_HEAD, fontSize: 44, color: WHITE, bold: true,
  });

  s.addText('A proposal to the principals.', {
    x: 0.7, y: 3.3, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 18, color: CREAM,
  });

  s.addText('eljeffe Hash and Seal Protocol — Wyoming-anchored. BTC-native. Anti-extraction by construction.', {
    x: 0.7, y: 3.9, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 14, color: CREAM, italic: true,
  });

  // Date + author block
  s.addText('2026-05-03', {
    x: 0.7, y: 5.8, w: 4, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: CREAM,
  });
  s.addText('Tell me where I\'m wrong.', {
    x: 0.7, y: 6.1, w: 12, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: CREAM, italic: true,
  });

  // Accent rule on the left margin
  s.addShape(pres.ShapeType.rect, {
    x: 0.4, y: 1.2, w: 0.04, h: 5.0,
    fill: { color: CREAM }, line: { color: CREAM },
  });
}

// ============================================================================
// SLIDE 2 — THE MOMENT
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('The moment', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 38, color: NAVY, bold: true,
  });

  s.addText('A once-in-a-decade inflection.', {
    x: 0.7, y: 1.3, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 18, color: TEAL, italic: true,
  });

  // Four-column "what's happening" grid
  const cols = [
    { title: 'Square pushes BTC', body: 'Bitcoin functionality reaching the merchant. The back-end question — where do my numbers live, what does my P&L denominate in — has exactly one answer.' },
    { title: 'Counterpoint VARs aging out', body: 'RapidPOS and the broader cohort. 2015 architecture. 20-year owners looking to exit clean. Channel partnership beats acquisition.' },
    { title: 'Compliance fragmenting', body: 'State-by-state privacy laws. ATF, NICS, alcohol direct-shipping, age-verification. Compliance-by-architecture is the differentiator.' },
    { title: 'Operators want sovereignty', body: 'Gun-store owners, ranchers, wine retailers, garden centers, multi-generational family operators. Same values stack. Nobody is building for them.' },
  ];
  cols.forEach((c, i) => {
    const x = 0.7 + i * 3.05;
    s.addShape(pres.ShapeType.rect, {
      x: x, y: 2.2, w: 2.85, h: 4.4,
      fill: { color: SAND }, line: { color: TEAL, width: 0.5 },
    });
    s.addText(c.title, {
      x: x + 0.2, y: 2.4, w: 2.5, h: 0.6,
      fontFace: FONT_HEAD, fontSize: 16, color: NAVY, bold: true,
    });
    s.addText(c.body, {
      x: x + 0.2, y: 3.1, w: 2.5, h: 3.4,
      fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL,
      paraSpaceAfter: 4, valign: 'top',
    });
  });
}

// ============================================================================
// SLIDE 3 — WHAT THE SUBSTRATE DOES
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('What the substrate does', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('Four operations. The proof is the proof.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  const ops = [
    { n: '01', title: 'Hash', body: 'Every consequential event — sale, transfer, vote, license, attestation — hashed cryptographically. Deterministic. Irreversible.' },
    { n: '02', title: 'Batch', body: 'Hashes assembled into a Merkle tree. The root represents every event in the batch with a single cryptographic fingerprint.' },
    { n: '03', title: 'Inscribe', body: 'Merkle root sealed onto a Bitcoin satoshi as an Ordinal at a specific block height. Permanent. No re-issuance possible.' },
    { n: '04', title: 'Verify', body: 'Anyone with a Bitcoin node verifies existence + ordering + integrity by Merkle proof against the immutable chain. No notary, no clerk, no goodwill.' },
  ];
  ops.forEach((c, i) => {
    const x = 0.7 + i * 3.05;
    s.addShape(pres.ShapeType.rect, {
      x: x, y: 2.2, w: 2.85, h: 4.4,
      fill: { color: SAND }, line: { color: TEAL, width: 0.5 },
    });
    s.addText(c.n, {
      x: x + 0.2, y: 2.4, w: 2.5, h: 0.5,
      fontFace: FONT_HEAD, fontSize: 14, color: TEAL, italic: true,
    });
    s.addText(c.title, {
      x: x + 0.2, y: 2.85, w: 2.5, h: 0.6,
      fontFace: FONT_HEAD, fontSize: 22, color: NAVY, bold: true,
    });
    s.addText(c.body, {
      x: x + 0.2, y: 3.55, w: 2.5, h: 2.9,
      fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL,
      paraSpaceAfter: 4, valign: 'top',
    });
  });
}

// ============================================================================
// SLIDE 5 — THE STRUCTURE PROPOSAL
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('The structure', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('Parent → GrowDirect → IP → RapidPOS license. Substrate underneath.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  // Four-box stack diagram
  const boxes = [
    { title: 'Parent operating company', sub: 'Three principals at genesis tier — Governance, Domain, Ops/Cloud. Holds equity in GrowDirect.', color: NAVY, textColor: WHITE },
    { title: 'GrowDirect', sub: 'Owns the Canary IP stack (ILDWAC #63/991,596 + methodology + codebase). Founder serves as President of Retail.', color: DEEP, textColor: WHITE },
    { title: 'RapidPOS — channel partner', sub: 'Licenses Canary from GrowDirect. Customer base flows onto the platform via partnership, not acquisition. Founder serves concurrently as CTO.', color: TEAL, textColor: WHITE },
    { title: 'eljeffe Hash and Seal Protocol — substrate', sub: 'Wyoming LLC + DAO LLC. Smart contracts, lineage-weighted ordinals, L402 micropayments, customer-owned data with DAO governance, BTC-denominated cost basis. Anti-extraction by construction.', color: CREAM, textColor: NAVY },
  ];
  boxes.forEach((b, i) => {
    const y = 1.9 + i * 1.2;
    s.addShape(pres.ShapeType.rect, {
      x: 0.7, y: y, w: 12, h: 1.0,
      fill: { color: b.color }, line: { color: b.color },
    });
    s.addText(b.title, {
      x: 0.9, y: y + 0.05, w: 11.6, h: 0.4,
      fontFace: FONT_HEAD, fontSize: 16, color: b.textColor, bold: true,
    });
    s.addText(b.sub, {
      x: 0.9, y: y + 0.45, w: 11.6, h: 0.55,
      fontFace: FONT_BODY, fontSize: 12, color: b.textColor,
    });
  });
}

// ============================================================================
// SLIDE 6 — THREE-PILLAR GENESIS PRINCIPALS
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('Three-pillar genesis', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('Roles, not names. Each pillar carries a specific kind of authority.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  const pillars = [
    {
      label: 'DOMAIN',
      title: 'Domain principal',
      role: 'You.',
      body: '25+ years retail-tech expertise. Canary IP stack contribution. Strategic leadership of the retail vertical. President of Retail at GrowDirect; CTO of RapidPOS during transition. The dual role keeps strategy and operations in the same hands.',
    },
    {
      label: 'GOVERNANCE',
      title: 'Governance principal',
      role: 'Tim.',
      body: 'Bylaws stewardship. DAO-process oversight. Compliance-architecture sign-off at the principal level. Co-founder of the parent operating company. The long-term governance signal.',
    },
    {
      label: 'OPS / CLOUD',
      title: 'Ops principal',
      role: 'Third — TBD.',
      body: 'GCP architecture. Substrate operation. The infrastructure layer that runs the protocol. Tim\'s existing partner, a separately-recruited cloud-architecture lead, or the compliance-architecture lead elevated. Founder + Tim alignment to name.',
    },
  ];
  pillars.forEach((p, i) => {
    const x = 0.7 + i * 4.1;
    s.addShape(pres.ShapeType.rect, {
      x: x, y: 2.0, w: 3.85, h: 4.6,
      fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
    });
    s.addText(p.label, {
      x: x + 0.25, y: 2.15, w: 3.5, h: 0.4,
      fontFace: FONT_BODY, fontSize: 11, color: TEAL, bold: true,
    });
    s.addText(p.title, {
      x: x + 0.25, y: 2.55, w: 3.5, h: 0.6,
      fontFace: FONT_HEAD, fontSize: 22, color: NAVY, bold: true,
    });
    s.addText(p.role, {
      x: x + 0.25, y: 3.2, w: 3.5, h: 0.4,
      fontFace: FONT_HEAD, fontSize: 16, color: DEEP, italic: true,
    });
    s.addText(p.body, {
      x: x + 0.25, y: 3.7, w: 3.5, h: 2.7,
      fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL, valign: 'top',
    });
  });
}

// ============================================================================
// SLIDE 7 — ECONOMICS
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('Economics in shape', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('Three-year sketch. Illustrative ranges. Why the numbers work.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  // Year table on left
  const rows = [
    ['Year', 'Revenue', 'Net', 'What\'s happening'],
    ['Y1', '$1-2M', '~breakeven', 'Eager-cohort migrating; first Square-BTC merchants; foundation built'],
    ['Y2', '$5-10M', '$1-4M positive', 'Steady cohort migrating; ISO 27001 cert; DriftPOS GA; new-logo wins'],
    ['Y3', '$15-40M', '$7-22M positive', 'Full cohort migration; possible first anchor; channel-partner momentum'],
  ];
  s.addTable(rows.map((r, i) => r.map(c => ({
    text: c,
    options: {
      fontFace: i === 0 ? FONT_HEAD : FONT_BODY,
      fontSize: i === 0 ? 12 : 11,
      color: i === 0 ? WHITE : CHARCOAL,
      bold: i === 0,
      fill: { color: i === 0 ? NAVY : (i % 2 === 0 ? SAND : WHITE) },
      valign: 'middle',
    },
  }))), {
    x: 0.7, y: 2.0, w: 7.5, colW: [0.6, 1.4, 1.7, 3.8],
    border: { type: 'solid', color: 'D0D0D0', pt: 0.5 },
  });

  // "Why these numbers work" stack on right
  s.addText('Why this works where typical SaaS doesn\'t:', {
    x: 8.6, y: 2.0, w: 4.4, h: 0.4,
    fontFace: FONT_HEAD, fontSize: 13, color: NAVY, bold: true,
  });
  s.addText([
    { text: '• No acquisition cost. ', options: { bold: true } },
    { text: 'RapidPOS is a channel partner; ~$2-3M not paid.\n' },
    { text: '• No HR overhead. ', options: { bold: true } },
    { text: '~$1M+/year structurally avoided.\n' },
    { text: '• Variable contributor comp. ', options: { bold: true } },
    { text: 'L402 pay-per-use; low-rev periods don\'t burn fixed payroll.\n' },
    { text: '• No T3 forced ramp. ', options: { bold: true } },
    { text: 'GCP scales with revenue.\n' },
    { text: '• Five customer cohorts. ', options: { bold: true } },
    { text: 'VAR roll-up, DriftPOS pilots, Square BTC, future channel partners, direct independent retail. Diversified.' },
  ], {
    x: 8.6, y: 2.5, w: 4.4, h: 4.0,
    fontFace: FONT_BODY, fontSize: 11, color: CHARCOAL,
    paraSpaceAfter: 4, valign: 'top',
  });
}

// ============================================================================
// SLIDE 8 — COMPLIANCE-BY-ARCHITECTURE
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('Compliance-by-architecture', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('The substrate produces audit-defensible evidence by construction.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  // Two columns — what the substrate does + concrete instantiation
  s.addShape(pres.ShapeType.rect, {
    x: 0.7, y: 2.0, w: 5.9, h: 4.6,
    fill: { color: SAND }, line: { color: TEAL, width: 0.5 },
  });
  s.addText('What the substrate does', {
    x: 0.95, y: 2.15, w: 5.5, h: 0.5,
    fontFace: FONT_HEAD, fontSize: 16, color: NAVY, bold: true,
  });
  s.addText([
    { text: 'Hash. ', options: { bold: true } }, { text: 'Every consequential event hashed cryptographically.\n' },
    { text: 'Batch. ', options: { bold: true } }, { text: 'Hashes assembled into a Merkle tree.\n' },
    { text: 'Inscribe. ', options: { bold: true } }, { text: 'Merkle root sealed onto a Bitcoin sat as an Ordinal at a specific block height.\n' },
    { text: 'Verify. ', options: { bold: true } }, { text: 'Existence + ordering + integrity, by Merkle proof, against the immutable chain.\n' },
    { text: '\n' },
    { text: 'ISO 27001:2022 — substrate-to-auditor translation per the compliance-architecture role.\n' },
    { text: 'PCI-DSS — Ingenico tokenization keeps cardholder data out of substrate scope.\n' },
    { text: 'SOC 2 Type II — observation period start month 18.\n' },
  ], {
    x: 0.95, y: 2.7, w: 5.5, h: 3.7,
    fontFace: FONT_BODY, fontSize: 11, color: CHARCOAL,
    paraSpaceAfter: 4, valign: 'top',
  });

  s.addShape(pres.ShapeType.rect, {
    x: 7.0, y: 2.0, w: 5.9, h: 4.6,
    fill: { color: NAVY }, line: { color: NAVY },
  });
  s.addText('Concrete: NICS attestation', {
    x: 7.25, y: 2.15, w: 5.5, h: 0.5,
    fontFace: FONT_HEAD, fontSize: 16, color: WHITE, bold: true,
  });
  s.addText([
    { text: 'A buyer wants to purchase a firearm. Federal law requires a NICS background check.\n\n' },
    { text: 'Today: ', options: { bold: true } }, { text: 'Paper Form 4473. Twenty-year binder. PII sitting in the dealer\'s basement.\n\n' },
    { text: 'On the substrate: ', options: { bold: true } }, { text: 'Cryptographic proof of clearance, sealed onto the chain. Dealer receives confirmation; PII never leaves the buyer. ATF-defensible. Customer-privacy-preserving.\n\n' },
    { text: 'Same architecture extends: alcohol direct-shipping, age-verification, controlled substances, regulated gaming.', options: { italic: true } },
  ], {
    x: 7.25, y: 2.7, w: 5.5, h: 3.7,
    fontFace: FONT_BODY, fontSize: 11, color: CREAM,
    paraSpaceAfter: 4, valign: 'top',
  });
}

// ============================================================================
// SLIDE 9 — HOW WE RECRUIT AND OPERATE
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('How we recruit and operate', {
    x: 0.7, y: 0.5, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 36, color: NAVY, bold: true,
  });

  s.addText('No HR. No finance department. No legal department. Substrate handles what each function used to do.', {
    x: 0.7, y: 1.3, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: TEAL, italic: true,
  });

  s.addText([
    { text: 'No resumes. Ever. ', options: { bold: true, color: NAVY } },
    { text: 'Read the wiki, pick up a ticket, demonstrate fit by doing the work. Smart contract auto-issues. Token-earn begins. Self-selection is the primary filter.\n\n' },
    { text: 'Trusted-network model. ', options: { bold: true, color: NAVY } },
    { text: 'Founders invite their trusted core; the core invites their networks. Each invitation is a stake — bringing someone in poorly hurts the inviter\'s standing. The trust filter is structural, not procedural.\n\n' },
    { text: 'Two contributor segments. ', options: { bold: true, color: NAVY } },
    { text: 'Young go-getters (early-career, hungry, values-aligned). 45+ second/third-career professionals (ex-devs stuck in middle management or out of work despite huge talent). New AI tools let that 45+ segment earn equity bit by byte.\n\n' },
    { text: 'Sales: public highscore leaderboard. ', options: { bold: true, color: NAVY } },
    { text: 'Token-generating value to the ecosystem — L402 throughput, retention, network effects — not just bookings revenue. Aligns the sales motion with ecosystem health, not gross-revenue-at-any-cost.\n\n' },
    { text: 'Office: King Harbor / Redondo Beach / pier. ', options: { bold: true, color: NAVY } },
    { text: 'Gold\'s Gym private membership; nodes wherever a trusted contributor is; remote-friendly; in-person when it makes sense. The architecture is distributed; the culture is in-person-when-possible.' },
  ], {
    x: 0.7, y: 2.0, w: 12.0, h: 4.7,
    fontFace: FONT_BODY, fontSize: 12.5, color: CHARCOAL,
    paraSpaceAfter: 4, valign: 'top',
  });
}

// ============================================================================
// SLIDE 8 — WHAT THIS PROTECTS (CLOSING)
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'DARK' });

  s.addText('What this protects.', {
    x: 0.7, y: 0.5, w: 12, h: 0.7,
    fontFace: FONT_HEAD, fontSize: 24, color: CREAM, italic: true,
  });

  s.addText('Customer · Contributor · Operator', {
    x: 0.7, y: 1.3, w: 12, h: 1.0,
    fontFace: FONT_HEAD, fontSize: 38, color: WHITE, bold: true,
  });

  const values = [
    {
      label: 'CUSTOMER',
      body: 'Their data is theirs. The substrate doesn\'t hold it; doesn\'t see it; doesn\'t broker it. Cross-customer use requires their explicit, on-chain ratification. Withdrawal works cleanly.',
    },
    {
      label: 'CONTRIBUTOR',
      body: 'Their work earns continuously and permanently. No vesting cliff. No clawback. No off-chain reputation score that can be re-keyed by a sponsor. What they earned is what they hold.',
    },
    {
      label: 'OPERATOR',
      body: 'Their stake at genesis cannot be diluted by issuing new tokens. Their authority sunsets gracefully when the substrate matures, but their position in the chain is permanent. They cannot be culled.',
    },
  ];
  values.forEach((v, i) => {
    const x = 0.7 + i * 4.1;
    s.addText(v.label, {
      x: x, y: 3.3, w: 3.8, h: 0.5,
      fontFace: FONT_HEAD, fontSize: 14, color: CREAM, bold: true,
    });
    s.addText(v.body, {
      x: x, y: 3.85, w: 3.8, h: 2.7,
      fontFace: FONT_BODY, fontSize: 12, color: WHITE, valign: 'top',
    });
  });

  s.addText('Tell me where I\'m wrong. Let\'s align.', {
    x: 0.7, y: 6.6, w: 12, h: 0.4,
    fontFace: FONT_HEAD, fontSize: 14, color: CREAM, italic: true, align: 'center',
  });
}

// ============================================================================
// SLIDE 11 — APPENDIX A — THROWAWAY-KEY / AGENT-MEDIATED INTERACTION
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('Appendix A', {
    x: 0.7, y: 0.5, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 13, color: TEAL, bold: true,
  });

  s.addText('Throwaway-key / agent-mediated interaction', {
    x: 0.7, y: 1.0, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 30, color: NAVY, bold: true,
  });

  s.addText('Forward optionality. Not part of the 100-day ask. Surfacing here so the strategic shape is visible.', {
    x: 0.7, y: 1.85, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL, italic: true,
  });

  s.addText([
    { text: 'A name is permanent. A pen is borrowed for an afternoon.\n\n', options: { italic: true, fontSize: 14, color: NAVY } },
    { text: 'Satoshi-as-key. ', options: { bold: true } },
    { text: 'The satoshi an operator holds is their identity in the namespace, permanently. Lineage on chain. History stamped into the ordinal — every vote cast, every proposal submitted, every transfer signed. Reading the ordinal tells you who its holder is and what they have done. Reputation is the substrate, not a separate score.\n\n' },
    { text: 'Serialization-as-throwaway. ', options: { bold: true } },
    { text: 'A specific interaction (a single payment, a single attestation, a single document signature) uses a leased key that exists only for that interaction. DHCP-style: bounded, scoped, expires when the work is done. The persistent identity authorizes the lease; the lease does the work; the lease cannot reach beyond its scope.\n\n' },
    { text: 'Architectural answer to: ', options: { bold: true } },
    { text: '"How does a person prove they are who they say they are without handing over a copy of their driver\'s license at every step?" The ordinal proves the person. The lease does the transaction. The two are connected and the connection is inspectable, but the lease doesn\'t carry the driver\'s license.' },
  ], {
    x: 0.7, y: 2.4, w: 12.0, h: 4.4,
    fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL,
    paraSpaceAfter: 6, valign: 'top',
  });
}

// ============================================================================
// SLIDE 12 — APPENDIX B — LIGHTNING OPERATOR FORWARD PATH
// ============================================================================
{
  const s = pres.addSlide({ masterName: 'MAIN' });

  s.addText('Appendix B', {
    x: 0.7, y: 0.5, w: 12, h: 0.5,
    fontFace: FONT_BODY, fontSize: 13, color: TEAL, bold: true,
  });

  s.addText('Lightning operator — forward path', {
    x: 0.7, y: 1.0, w: 12, h: 0.8,
    fontFace: FONT_HEAD, fontSize: 30, color: NAVY, bold: true,
  });

  s.addText('Three-phase progression. Same arc the Wyoming mining-mini-op partnership gives us for chain writes.', {
    x: 0.7, y: 1.85, w: 12, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, color: CHARCOAL, italic: true,
  });

  const phases = [
    {
      label: 'PHASE 0',
      title: 'Consume',
      timeframe: 'Now → Phase A',
      body: 'Lightning rails for L402 micropayments. Someone else operates the nodes; we are a customer. LND or Voltage as the rails. Sufficient channel capacity for 100-day Phase A traffic.',
    },
    {
      label: 'PHASE 1',
      title: 'Internal',
      timeframe: 'Month 12+',
      body: 'Stand up our own nodes for internal traffic. Contributor-cohort-only. Our sat-flow stays on our infrastructure. Begin running routes for the namespace\'s own L402 payments.',
    },
    {
      label: 'PHASE 2',
      title: 'External',
      timeframe: 'Month 24+',
      body: 'Serve external customers as a Lightning operator at scale. Routing fee revenue. Substrate sovereignty across the routing layer. US state money-transmission licensing per the regulatory analysis.',
    },
  ];
  phases.forEach((p, i) => {
    const x = 0.7 + i * 4.1;
    s.addShape(pres.ShapeType.rect, {
      x: x, y: 2.5, w: 3.85, h: 4.0,
      fill: { color: WHITE }, line: { color: TEAL, width: 1 },
    });
    s.addText(p.label, {
      x: x + 0.25, y: 2.65, w: 3.5, h: 0.4,
      fontFace: FONT_BODY, fontSize: 11, color: TEAL, bold: true,
    });
    s.addText(p.title, {
      x: x + 0.25, y: 3.05, w: 3.5, h: 0.6,
      fontFace: FONT_HEAD, fontSize: 22, color: NAVY, bold: true,
    });
    s.addText(p.timeframe, {
      x: x + 0.25, y: 3.7, w: 3.5, h: 0.4,
      fontFace: FONT_BODY, fontSize: 12, color: DEEP, italic: true,
    });
    s.addText(p.body, {
      x: x + 0.25, y: 4.2, w: 3.5, h: 2.2,
      fontFace: FONT_BODY, fontSize: 11.5, color: CHARCOAL, valign: 'top',
    });
  });
}

// ============================================================================
// WRITE
// ============================================================================
const outPath = '/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx';
pres.writeFile({ fileName: outPath }).then(name => {
  console.log('WROTE: ' + name);
}).catch(err => {
  console.error('ERROR: ' + err);
  process.exit(1);
});
