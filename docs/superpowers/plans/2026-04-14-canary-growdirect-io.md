# canary.growdirect.io Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the canary.growdirect.io landing page — a single static HTML file that showcases the Canary platform and captures partnership leads via Formspree.

**Architecture:** Single HTML file with embedded CSS and inline JS. No build step, no framework, no external JS dependencies. Served as static files from `Canary/static/landing/`. Uses the existing sample page (`Canary/static/landing/index.html`) as the starting point for visual tokens, SVG assets, and CSS patterns — but the content, structure, and sections are rebuilt from the design spec.

**Tech Stack:** HTML5, CSS3 (embedded), vanilla JS, Google Fonts (Space Grotesk), Formspree, GA4

**Spec:** `docs/superpowers/specs/2026-04-14-canary-growdirect-io-design.md`

---

## File Structure

| File | Action | Purpose |
|------|--------|---------|
| `Canary/static/landing/index.html` | **Rewrite** | The landing page. Single file, all CSS embedded, inline SVG. |

That's it. One file. The existing sample at this path gets replaced entirely.

---

## Chunk 1: Page Shell, Nav, Hero

### Task 1: Set up the HTML document shell

**Files:**
- Rewrite: `Canary/static/landing/index.html`

- [ ] **Step 1: Create the document shell**

Replace the entire file. Start with:
- `<!DOCTYPE html>`, lang="en"
- Meta charset, viewport
- `<title>Canary — The Canary in the Data Mine</title>`
- Meta description: "Transaction monitoring for Square merchants. Enterprise retail expertise applied to the SMB market. Connect your Square account. See where you're losing money."
- Canonical: `https://canary.growdirect.io/`
- OG meta tags (og:title, og:description, og:type=website, og:url)
- Twitter card meta (summary_large_image)
- Favicon: `/img/canary-icon.svg`
- Google Fonts preconnect + Space Grotesk link (weights: 400, 500, 600, 700) with `display=swap`
- Skip-to-content link: `<a href="#main" class="skip-link">Skip to content</a>`

CSS tokens — copy from the existing sample's `:root` block:
```css
:root {
  --bg-ink: #0D1117;
  --bg-surface: #161B22;
  --bg-card: #1C2128;
  --border: #30363D;
  --border-light: #21262D;
  --gold: #FBBF24;
  --amber: #F59E0B;
  --gold-glow: rgba(251, 191, 36, 0.15);
  --gold-glow-strong: rgba(251, 191, 36, 0.25);
  --green: #059669;
  --green-glow: rgba(5, 150, 105, 0.15);
  --text-primary: #E6EDF3;
  --text-secondary: #8B949E;
  --text-muted: #6B7280;
  --font: 'Space Grotesk', system-ui, -apple-system, sans-serif;
}
```

Base reset + body styles — same as existing sample.

- [ ] **Step 2: Verify the shell renders**

Open in browser. Confirm: dark background, no errors in console, fonts loading.

- [ ] **Step 3: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): document shell with tokens and meta tags"
```

---

### Task 2: Build the nav

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add the nav bar**

Structure:
```html
<nav class="nav" aria-label="Main navigation">
  <div class="nav-brand">
    <!-- Canary bird SVG (small, 28x28) — copy from existing sample line 566-575 -->
    Canary
  </div>
  <div class="nav-links">
    <a href="#how-it-works">How It Works</a>
    <a href="#background">Background</a>
    <a href="#partner" class="btn-nav-cta">Partner With Us</a>
  </div>
  <button class="nav-hamburger" aria-label="Toggle menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</nav>
```

CSS for nav:
- Flex, space-between, max-width 960px, centered
- `.nav-links` — flex, gap 24px, align center
- `.nav-links a` — color: var(--text-secondary), font-size 14px, font-weight 500
- `.nav-links a:hover` — color: var(--gold)
- `.btn-nav-cta` — padding 8px 16px, border 1px solid var(--gold), border-radius 8px, color var(--gold), font-weight 600
- `.nav-hamburger` — display: none (shown below 768px)
- `@media (max-width: 768px)`: hide `.nav-links`, show `.nav-hamburger`, `.btn-nav-cta` stays visible outside the hamburger menu
- Mobile menu: when hamburger toggled, `.nav-links` displays as column, positioned below nav

- [ ] **Step 2: Add hamburger toggle JS**

Minimal vanilla JS at bottom of `<body>`:
```javascript
document.querySelector('.nav-hamburger').addEventListener('click', function() {
  const nav = document.querySelector('.nav-links');
  const expanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', !expanded);
  nav.classList.toggle('nav-open');
});
```

- [ ] **Step 3: Test nav at desktop and mobile widths**

Verify: links scroll to correct anchors (sections don't exist yet — just verify no JS errors). Hamburger shows/hides at 768px breakpoint.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): nav bar with hamburger menu"
```

---

### Task 3: Build the hero section (Layer 1)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add the hero HTML**

```html
<main id="main">
<section class="hero" aria-label="Introduction">
  <div class="hero-bird">
    <!-- Full canary bird SVG from existing sample lines 587-602 -->
    <!-- Wrapped in prefers-reduced-motion media query for animation -->
  </div>
  <h1>The Canary in the Data Mine</h1>
  <p class="hero-sub">
    Transaction monitoring for Square merchants. Connect your account.
    Get a weekly report showing exactly where you're losing money.
  </p>
  <div class="hero-cta-group">
    <a href="#how-it-works" class="btn-primary">See How It Works</a>
    <a href="#partner" class="btn-secondary">Partner With Us</a>
  </div>
  <p class="hero-trust">Built on Square APIs · Read-only access · Your data stays yours</p>
</section>
```

- [ ] **Step 2: Add hero CSS**

Copy hero styles from existing sample (lines 82-117) as the base. Adjustments:
- `.hero h1` — color: var(--text-primary), no `<em>` gold treatment (headline is straight)
- `.hero-sub` — max-width 560px, color var(--text-secondary)
- `.hero-trust` — font-size 13px, color var(--text-muted), margin-top 24px
- `.hero-bird` — filter: drop-shadow(0 0 32px var(--gold-glow-strong))
- Button styles: copy `.btn-primary` and `.btn-secondary` from existing sample (lines 120-160)

Bird animation and mobile sizing:
```css
@media (prefers-reduced-motion: no-preference) {
  @keyframes gentle-bob {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
  }
  .hero-bird svg g { animation: gentle-bob 3s ease-in-out infinite; }
}
@media (max-width: 480px) {
  .hero-bird svg { width: 80px; height: auto; }
  .hero-bird { filter: drop-shadow(0 0 16px var(--gold-glow)); }
}
```

Focus rings (add to base styles):
```css
:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.partner-section :focus-visible { outline-color: var(--green); }
```

- [ ] **Step 3: Test hero rendering**

Verify: bird animates, headline renders in white (not gold), subhead is readable, both buttons present, trust line visible below CTAs. Check at 480px width — single column, bird scales down.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): hero section with canary bird and CTAs"
```

---

## Chunk 2: Proof and Credentials (Layers 2-3)

### Task 4: Weekly report mock (Layer 2, part 1)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add the weekly report mock section**

```html
<section class="report-section" id="how-it-works" aria-label="What Canary finds">
  <div class="container">
    <div class="report-card">
      <div class="report-card-header">
        <!-- Small canary SVG (24x22) -->
        <span>Canary Weekly Report — Mar 24-30</span>
      </div>
      <div class="report-hero-num">
        <span class="amount">$437</span>
        <span class="label">in potential losses found this week</span>
      </div>
      <div class="report-body">
        <strong>Biggest driver:</strong> Your Tuesday and Thursday evening
        refund rate is 3.8x your store average. That pattern has been
        consistent for three weeks and accounts for about $280 of this
        week's total. The remaining $157 came from two post-sale voids
        on Wednesday.
      </div>
      <div class="report-action">
        <div class="report-action-label">Recommended action</div>
        Review the 6 flagged refunds with your Tuesday/Thursday closing staff.
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add report card CSS**

Copy the report card styles from the existing sample (lines 340-414). Key styles:
- `.report-section` — padding 80px 24px
- `.report-card` — max-width 480px, margin 0 auto, background var(--bg-card), border 1px solid var(--border), border-radius 16px, box-shadow 0 0 40px var(--gold-glow), padding 28px
- `.report-hero-num .amount` — font-size 48px, font-weight 700, color var(--gold)
- `.report-hero-num .label` — font-size 15px, color var(--text-secondary)
- `.report-body` — font-size 14px, color var(--text-secondary), line-height 1.6
- `.report-action` — background rgba(5,150,105,0.1), border 1px solid rgba(5,150,105,0.2), border-radius 8px, padding 12px 16px
- Mobile: `.report-card` goes full-width with 16px padding

- [ ] **Step 3: Test report card**

Verify: card is centered, gold glow visible, dollar amount prominent, action box green-tinted. Test at 480px — card fills width.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): weekly report mock card"
```

---

### Task 5: Detection examples (Layer 2, part 2)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add detection examples below the report card**

Inside the same `report-section`, below the report card:

```html
    <div class="detection-examples">
      <h2>What Canary flags</h2>
      <div class="detection-list">
        <div class="detection-item">
          <span class="detection-marker"></span>
          <p>A voided sale 3 minutes after the customer left</p>
        </div>
        <div class="detection-item">
          <span class="detection-marker"></span>
          <p>A $300 payment processed at 2 AM — you close at 10</p>
        </div>
        <div class="detection-item">
          <span class="detection-marker"></span>
          <p>One employee's discount rate is 5x the store average</p>
        </div>
        <div class="detection-item">
          <span class="detection-marker"></span>
          <p>Refunds filed faster than a real return takes</p>
        </div>
      </div>
    </div>
```

- [ ] **Step 2: Add detection list CSS**

- `.detection-examples` — max-width 560px, margin 64px auto 0
- `.detection-examples h2` — font-size 22px, font-weight 600, margin-bottom 24px
- `.detection-list` — display flex, flex-direction column, gap 16px
- `.detection-item` — display flex, gap 12px, align-items baseline
- `.detection-marker` — 6px x 6px circle, background var(--gold), border-radius 50%, flex-shrink 0, margin-top 8px
- `.detection-item p` — font-size 16px, color var(--text-secondary), line-height 1.5

No emojis. No category labels. Gold dot markers only.

- [ ] **Step 3: Test detection list**

Verify: list items are clean, gold dot markers, no emojis, readable at all widths.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): detection examples list"
```

---

### Task 6: Credentials section (Layer 3)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add credentials section**

```html
<section class="credentials" id="background" aria-label="Background">
  <div class="container">
    <div class="credentials-grid">
      <div class="credential-block">
        <h3>Enterprise retail background</h3>
        <p>30 years. IBM 4690 POS systems, national chains, high-volume production environments. Transaction processing at scale.</p>
      </div>
      <div class="credential-block">
        <h3>Big 5 process capability</h3>
        <p>Enterprise-grade methodology and support practices, applied to the SMB market through automation.</p>
      </div>
      <div class="credential-block">
        <h3>Data integrity</h3>
        <p>If we flag something, we have the evidence. Every finding is backed by immutable, timestamped records.</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add credentials CSS**

- `.credentials` — padding 80px 24px, border-top 1px solid var(--border-light)
- `.credentials-grid` — display grid, grid-template-columns repeat(3, 1fr), gap 32px, max-width 800px, margin 0 auto
- `.credential-block h3` — font-size 16px, font-weight 600, color var(--gold), margin-bottom 8px
- `.credential-block p` — font-size 14px, color var(--text-secondary), line-height 1.6
- `@media (max-width: 768px)`: single column

- [ ] **Step 3: Test credentials section**

Verify: three columns on desktop, stacks on mobile, gold headings, secondary text. Short and factual — no storytelling.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): credentials section"
```

---

## Chunk 3: Platform, Vision, Partnership (Layers 4-6)

### Task 7: Platform section (Layer 4)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add platform section**

```html
<section class="platform" aria-label="How Canary works">
  <div class="container">
    <h2>How Canary works</h2>
    <div class="platform-flow">
      <span>Connect Square</span>
      <span class="flow-arrow">&rarr;</span>
      <span>Transactions flow in real-time</span>
      <span class="flow-arrow">&rarr;</span>
      <span>Detection engine evaluates every event</span>
      <span class="flow-arrow">&rarr;</span>
      <span>Patterns surface as plain-language insights</span>
      <span class="flow-arrow">&rarr;</span>
      <span>Evidence sealed and timestamped</span>
    </div>
    <div class="arch-cards">
      <div class="arch-card">
        <h4>Square webhook ingestion</h4>
        <p>Real-time event stream with HMAC verification</p>
      </div>
      <div class="arch-card">
        <h4>Detection engine</h4>
        <p>Configurable rules per merchant</p>
      </div>
      <div class="arch-card">
        <h4>Immutable evidence store</h4>
        <p>INSERT-only, hash-chained, trigger-enforced</p>
      </div>
      <div class="arch-card">
        <h4>Case management</h4>
        <p>Court-ready documentation</p>
      </div>
      <div class="arch-card">
        <h4>AI analysis</h4>
        <p>Pattern narrative generation</p>
      </div>
    </div>
    <div class="stack-tags">
      <span>Python</span><span>Flask</span><span>PostgreSQL</span><span>Square SDK</span><span>Docker</span>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add platform CSS**

- `.platform` — padding 80px 24px, border-top 1px solid var(--border-light)
- `.platform h2` — font-size 24px, font-weight 700, margin-bottom 32px
- `.platform-flow` — display flex, flex-wrap wrap, align-items center, gap 8px, margin-bottom 40px, font-size 14px, color var(--text-secondary)
- `.flow-arrow` — color var(--gold), font-weight 700
- `.arch-cards` — display grid, grid-template-columns repeat(auto-fit, minmax(180px, 1fr)), gap 16px, margin-bottom 32px
- `.arch-card` — padding 20px, background var(--bg-surface), border 1px solid var(--border), border-radius 10px
- `.arch-card h4` — font-size 14px, font-weight 600, color var(--text-primary), margin-bottom 4px
- `.arch-card p` — font-size 13px, color var(--text-secondary)
- `.stack-tags` — display flex, flex-wrap wrap, gap 8px
- `.stack-tags span` — padding 4px 12px, border 1px solid var(--border), border-radius 6px, font-size 12px, color var(--text-muted)

- [ ] **Step 3: Test platform section**

Verify: flow reads left-to-right with gold arrows, architecture cards in grid, stack tags at bottom. Stacks on mobile.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): platform architecture section"
```

---

### Task 8: Vision section (Layer 5)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add vision section**

```html
<section class="vision" aria-label="Vision">
  <div class="container">
    <div class="vision-block">
      <h3>The tLog problem</h3>
      <p>IBM created the transaction log in 1986. Every POS system since uses the same model: a mutable record on a server someone controls. The log can be edited. It happens.</p>
      <p>Canary's evidence store is different. INSERT-only. Hash-chained. Merkle roots anchored to Bitcoin. Records can't be altered after the fact.</p>
    </div>
    <div class="vision-block">
      <h3>The gLog</h3>
      <p>Canary is building the successor to the tLog — an immutable transaction record that works from one receipt to one billion.</p>
      <p>Not blockchain for its own sake. A direct fix for a specific problem in how retail transactions have been recorded for 40 years.</p>
    </div>
    <div class="vision-block">
      <h3>Open source</h3>
      <p>The detection logic, evidence storage, and data handling will be public. Transparency is the standard. Execution is the differentiator.</p>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add vision CSS**

- `.vision` — padding 80px 24px, border-top 1px solid var(--border-light)
- `.vision-block` — max-width 640px, margin 0 auto 48px
- `.vision-block:last-child` — margin-bottom 0
- `.vision-block h3` — font-size 18px, font-weight 600, color var(--text-primary), margin-bottom 12px
- `.vision-block p` — font-size 15px, color var(--text-secondary), line-height 1.6, margin-bottom 8px

Flat. No cards, no special treatment. Just text blocks.

- [ ] **Step 3: Test vision section**

Verify: readable text blocks, no visual flair, content is the manifesto material for people who dig this deep.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): vision section — tLog, gLog, open source"
```

---

### Task 9: Partnership section (Layer 6)

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add partnership section with green accent transition**

```html
<section class="partner-section" id="partner" aria-label="Partner with us">
  <div class="container">
    <h2>Partner with us</h2>

    <div class="partner-paths">
      <div class="partner-path">
        <h3>Merchant partner</h3>
        <p>You run a Square operation. We need a merchant willing to connect their account, work with real data, and help refine the product. Any size. Read-only access. No commitment beyond trying it.</p>
        <a href="#partner-form" class="btn-partner" data-source="merchant-partner">Get in touch</a>
      </div>
      <div class="partner-path">
        <h3>Team / service partner</h3>
        <p>We're building enterprise-level retail tooling for the SMB market — multi-location support, a canonical retail data model for back-office integrations, and detection at scale. Looking for people or firms who want to work in this space.</p>
        <a href="#partner-form" class="btn-partner" data-source="team-partner">Get in touch</a>
        <!-- Calendly link — URL TBD. Uncomment when ready:
        <a href="https://calendly.com/PLACEHOLDER" class="btn-calendly" target="_blank" rel="noopener">Or book a call</a>
        -->
      </div>
    </div>

    <form class="partner-form" id="partner-form"
          action="https://formspree.io/f/NEW_FORM_ID" <!-- TODO: REPLACE with actual Formspree form ID -->
          method="POST">
      <input type="hidden" name="_source" id="partnerSource" value="direct">
      <div class="form-row">
        <div class="form-field">
          <label for="name">Name</label>
          <input type="text" id="name" name="name" required>
        </div>
        <div class="form-field">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" required>
        </div>
      </div>
      <div class="form-row">
        <div class="form-field">
          <label for="business">Business name</label>
          <input type="text" id="business" name="business">
        </div>
        <div class="form-field">
          <label for="locations">Number of locations</label>
          <input type="text" id="locations" name="locations" placeholder="Optional">
        </div>
      </div>
      <div class="form-field">
        <label for="message">Message</label>
        <textarea id="message" name="message" rows="4"></textarea>
      </div>
      <button type="submit" class="btn-primary btn-submit">Send</button>
    </form>

    <div class="form-success" id="partnerFormSuccess">
      Received. We'll be in touch.
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add partnership CSS**

- `.partner-section` — padding 80px 24px, background linear-gradient(180deg, var(--bg-ink) 0%, rgba(5,150,105,0.05) 100%)
- `.partner-section h2` — font-size 28px, font-weight 700, color var(--green), margin-bottom 40px, text-align center
- `.partner-paths` — display grid, grid-template-columns repeat(2, 1fr), gap 32px, max-width 720px, margin 0 auto 48px
- `.partner-path` — padding 24px, background var(--bg-surface), border 1px solid var(--border), border-radius 12px
- `.partner-path h3` — font-size 18px, font-weight 600, color var(--text-primary), margin-bottom 12px
- `.partner-path p` — font-size 14px, color var(--text-secondary), line-height 1.6, margin-bottom 16px
- `.btn-partner` — display inline-block, padding 10px 20px, border 1px solid var(--green), border-radius 8px, color var(--green), font-weight 600, font-size 14px
- `.btn-partner:hover` — background rgba(5,150,105,0.1)
- Form fields: standard dark theme inputs matching existing sample patterns
- `.partner-form` — max-width 560px, margin 0 auto
- `.form-row` — display grid, grid-template-columns repeat(2, 1fr), gap 16px
- `label` — font-size 13px, font-weight 500, color var(--text-secondary), margin-bottom 4px, display block
- `input, textarea` — width 100%, padding 12px 14px, background var(--bg-surface), border 1px solid var(--border), border-radius 8px, color var(--text-primary), font-family var(--font), font-size 15px
- `input:focus, textarea:focus` — border-color var(--green), outline none
- `.btn-submit` — background linear-gradient(135deg, var(--green), #047857), margin-top 16px
- `.form-success` — same pattern as existing sample, hidden by default
- `@media (max-width: 768px)`: partner-paths single column, form-row single column

- [ ] **Step 3: Add partner form JS**

```javascript
// Partner source attribution
document.querySelectorAll('.btn-partner').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('partnerSource').value = this.dataset.source;
    document.getElementById('partner-form').scrollIntoView({ behavior: 'smooth' });
  });
});

// Also check URL param: ?from=merchant-partner or ?from=team-partner
var urlSource = new URLSearchParams(window.location.search).get('from');
if (urlSource) {
  document.getElementById('partnerSource').value = urlSource;
}

// Form submission via AJAX
document.getElementById('partner-form').addEventListener('submit', function(e) {
  e.preventDefault();
  var form = this;
  var data = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    body: data,
    headers: { 'Accept': 'application/json' }
  }).then(function(response) {
    if (response.ok) {
      form.style.display = 'none';
      document.getElementById('partnerFormSuccess').style.display = 'block';
    } else {
      // Fallback to mailto
      window.location.href = 'mailto:gclyle@growdirect.io?subject=Canary%20Partnership&body='
        + encodeURIComponent('Name: ' + data.get('name') + '\nEmail: ' + data.get('email')
        + '\nBusiness: ' + data.get('business') + '\nMessage: ' + data.get('message'));
    }
  }).catch(function() {
    window.location.href = 'mailto:gclyle@growdirect.io?subject=Canary%20Partnership';
  });
});
```

- [ ] **Step 4: Test partnership section**

Verify: green accent transition visible, two partner path cards side by side, form renders with proper labels, hidden source field updates when clicking "Get in touch" buttons, `?from=merchant-partner` URL param sets the source field. Test at 480px — cards and form fields stack.

- [ ] **Step 5: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): partnership section with form and source attribution"
```

---

### Task 10: Footer

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add footer**

```html
</main>
<footer class="footer">
  <div class="footer-brand">
    <!-- Small canary SVG (18x16) -->
    Canary by GrowDirect
  </div>
  <p><a href="mailto:gclyle@growdirect.io">gclyle@growdirect.io</a> · <a href="https://growdirect.io">growdirect.io</a></p>
</footer>
```

- [ ] **Step 2: Add footer CSS**

Copy footer styles from existing sample (lines 524-544).

- [ ] **Step 3: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): footer"
```

---

## Chunk 4: Analytics, Scroll Tracking, Final Polish

### Task 11: GA4 and scroll tracking

**Files:**
- Modify: `Canary/static/landing/index.html`

- [ ] **Step 1: Add GA4 script tag**

In `<head>`, after the font link:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ELPTR2ZLP3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-ELPTR2ZLP3');
</script>
```

- [ ] **Step 2: Add scroll tracking and form event JS**

In the `<script>` block at the bottom:

```javascript
// Section scroll tracking via Intersection Observer
var trackedSections = {};
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting && !trackedSections[entry.target.id]) {
      trackedSections[entry.target.id] = true;
      gtag('event', 'section_scroll', { section: entry.target.id });
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('section[id]').forEach(function(section) {
  observer.observe(section);
});

// Form submit event — add inside existing submit handler
// After successful submit:
gtag('event', 'partner_form_submit', { source: data.get('_source') });
```

- [ ] **Step 3: Test analytics**

Open browser dev tools Network tab, verify GA4 requests fire on page load. Scroll through sections and verify `section_scroll` events in the console (use GA4 debug mode or check Network for collect requests).

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "feat(landing): GA4 with section scroll and form submit tracking"
```

---

### Task 12: Formspree form ID setup

**Files:**
- Modify: `Canary/static/landing/index.html`

**NOTE:** This task requires creating a new Formspree form. The form action URL placeholder `NEW_FORM_ID` must be replaced with the actual Formspree form ID.

- [ ] **Step 1: Create Formspree form**

Go to formspree.io, create a new form for the Canary landing page. Get the form ID.

- [ ] **Step 2: Replace placeholder**

In `index.html`, replace `NEW_FORM_ID` with the actual Formspree form ID in the form action URL.

- [ ] **Step 3: Test form submission**

Submit a test entry. Verify it appears in Formspree dashboard with the `_source` field populated.

- [ ] **Step 4: Commit**

```bash
git add Canary/static/landing/index.html
git commit -m "chore(landing): set Formspree form ID"
```

---

### Task 13: Final review and polish

**Files:**
- Review: `Canary/static/landing/index.html`

- [ ] **Step 1: Full page review at desktop width**

Walk through all 6 layers top to bottom. Verify:
- Headline is "The Canary in the Data Mine" (no hype, no fluff)
- Weekly report card is the visual centerpiece
- Detection examples use gold dot markers, no emojis
- Credentials section is three short factual blocks
- Platform section shows architecture cards and stack tags
- Vision section is plain text blocks (tLog, gLog, open source)
- Partner section has green accent, two paths, form works
- Footer links to growdirect.io and shows email

- [ ] **Step 2: Mobile review at 480px**

Verify all sections stack properly, hamburger works, form fields stack, touch targets are 44px+.

- [ ] **Step 3: Accessibility check**

- Skip-to-content link works
- All sections have `aria-label`
- Form inputs have `<label>` elements
- Color contrast: body text is white on dark (passes), gold is headings/accents only (large text)
- `prefers-reduced-motion` disables bird animation

- [ ] **Step 4: Console check**

No JS errors, no 404s for resources, fonts loaded.

- [ ] **Step 5: Commit any fixes**

```bash
git add Canary/static/landing/index.html
git commit -m "fix(landing): polish and accessibility fixes"
```

---

## DNS and Hosting (post-implementation)

These steps require infrastructure access and are not code tasks:

1. **Formspree** — create new form endpoint at formspree.io (Task 12)
2. **DNS** — add CNAME record: `canary` pointing to wherever the Canary app is hosted (or GitHub Pages / Vercel if deploying static)
3. **Nginx** — if serving from the Canary server, add a server block for `canary.growdirect.io` that serves `Canary/static/landing/` as static files
4. **SSL** — certbot for the new subdomain

5. **robots.txt** — ensure `Canary/static/landing/robots.txt` exists with `User-agent: *\nAllow: /` (or configure in Nginx)

These are noted here for tracking but executed outside this plan.
