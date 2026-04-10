# LP Manual Update Guide — Angelique Lyle Reskin

**Site:** https://app.luxurypresence.com → Angelique Lyle (Preview Ready, no domain)
**Preview:** https://p-6640af74-339a-4bac-8ba6-db2a4dad701d.presencepreview.site/

Do these in order. Total time: ~30 minutes.

---

## Step 1: Paste Updated CSS (5 min)

1. Open LP Dashboard → click the site → three-dot menu → **Site Settings**
2. Left sidebar: click **Global Scripts**
3. In the **Head JavaScript** editor: **Select All** (Cmd+A), then **paste** the entire contents of this file:
   ```
   ~/GrowDirect/lp-injection/lp-head-inject.html
   ```
4. Click **Save**
5. Check the preview site — fonts, nav, buttons should all be monochrome/sharp

> The CSS handles fonts, colors, layout. Logo and content changes are done in the steps below.

---

## Step 2: Update General Settings (already done, verify)

1. Site Settings → **General** (left sidebar)
2. Verify these fields:
   - **Brokerage Name:** `Compass | Accardo Real Estate Associates`
   - **Email:** `angelique.lyle@compass.com`
   - **Cell Phone:** `(310)751-8335` (keep)
   - **Full Name:** `Angelique Lyle` (keep)
3. Save if any changes needed

---

## Step 3: Update Homepage Content via LP Editor

Close the Settings modal. You'll see the visual page editor with the preview.

### 3a. Hero Section (Homepage Opening)

Click **Edit** (top right) → click on the hero section area.

LP's hero is a Slick slider. In the component editor:
- **Hero text:** Keep "Angelique Lyle" (LP auto-generates from the name field)
- **Slider images:** Replace the current brokerage photos with PV coastal images. You can upload these or use LP's media library. The prototype uses this image for the hero:
  ```
  https://media-production.lp-cdn.com/media/ruzqfo5d9fxziagofncw
  ```
  (PV coastal view — may already be in your LP media library)

### 3b. About Section (Featured Agent)

Click on the About section in the editor. Update the **Content** tab:

**Subtitle (eyebrow):** `Meet Angelique`

**Title:** `The Peninsula's relocation expert.`

**Bio text (replace the entire old bio with):**

```
I moved to Palos Verdes not knowing a soul. Two kids, a pile of boxes, and a lot of questions the internet couldn't answer — which neighborhood actually suited our family, which elementary school fed where, and where to get a decent coffee after the movers left. I figured it all out the hard way.

That experience is why I do what I do. For nearly 20 years I've been guiding buyers and sellers across all price ranges — from the Hill to the beach cities — and somewhere along the way I became the person families call not just to find a house, but to figure out how to build a life here. I raised my own two kids through PVPUSD, watched them graduate, and sent them off to Big Ten universities. I know this community from the inside.

As a USC and FIDM graduate with degrees in Communication, French, and Fashion Design, I bring an eye for detail and design to every transaction. Ranked in the top 1.5% of agents nationally with Compass — the #1 brokerage in LA — and partnered with the Accardo Real Estate Associates team, I offer the reach of a major brand with the personal attention of a neighbor.
```

**Button text:** `Work with me →`

### 3c. Neighborhoods Section

Click on the Neighborhoods section. Update:

**Subtitle:** `The Peninsula`
**Title:** `Six communities, one coastline.`
**Description:** `Browse our neighborhood guides for schools, market data, and what daily life actually looks like in each community.`

The existing neighborhood cards (Rolling Hills, Redondo Beach, Hermosa Beach) are fine — those are real PV/South Bay neighborhoods. If you can add more, the prototype has 6:
- Palos Verdes Estates (Luxury · Views · PVE, Median ~$2.8M)
- Rancho Palos Verdes (Coastal · Family · RPV, Median ~$1.6M)
- Rolling Hills Estates (Trails · Schools · RHE, Median ~$1.4M)
- Rolling Hills (Gated · Equestrian · Private, Median ~$3M+)
- Redondo Beach (Beach · Walkable · Active)
- Hermosa Beach (Surf · Sand · Community)

### 3d. Testimonials Section

Click on the Testimonials section. Update:

**Subtitle:** `Client Stories`
**Title:** `What the Peninsula says.`

The current testimonials (Dorothy & Bill H., Jim & Gloria P.) are already real — keep those. The prototype includes four:

1. **John O.** — "She is the one in a million — knows the market, negotiates brilliantly, and makes everyone feel like a winner."
2. **Jim & Gloria P.** — "Angelique became our agent while we still lived in North Carolina. She worked with us long-distance for months and found exactly what we'd envisioned."
3. **Dan L.** — "We've done four transactions with Angelique — two primary residences and two secondary. She worked tirelessly and stands out in her creative use of every tool available."
4. **Kirk V.** — "Her years of experience have made her an absolute master in a field that requires in-depth knowledge of so many variables."

---

## Step 4: Update Footer Content

The footer is a theme-level component. Look for footer settings (may be under the three-dot menu → **Footer** or at the bottom of the page editor).

**Address:** `550 Silver Spur Road, Suite 110, Rancho Palos Verdes, CA 90275`
**Phone:** `(310) 751-8335`
**Email:** `angelique.lyle@compass.com`
**DRE:** `CA DRE# 01475592`

Delete or replace the Sotheby's trademark disclaimer text. Replace with:
```
Compass | Accardo Real Estate Associates
```

### Footer Logo — DELETE the Sotheby's image

This is an uploaded image, not generated by CSS. It must be removed in LP, not hidden.

1. In the footer editor (or Site Settings > Branding), find the logo upload field
2. **Delete** the Vista Sotheby's International Realty logo image
3. Upload a Compass logo (white version for dark background) if you have one
4. If no Compass logo file handy, leave it blank — LP will show "Angelique Lyle" text instead, which is clean

### Sidemenu Logo — same thing

The hamburger menu (MENU button, top right) opens a side panel that also shows the Sotheby's logo.
1. Find the sidemenu/mobile menu logo setting
2. **Delete** the Sotheby's image
3. Upload Compass logo or leave blank

---

## Step 5: Check Other Pages

LP generates several pages automatically. Click the **page dropdown** (top left, says "Home") and check these:

- **About** — Should pull from the Featured Agent content. Update if needed.
- **Active Properties / Sold Properties** — These are IDX-powered by LP. Our CSS styles them with the monochrome design. No content changes needed.
- **Neighborhoods** — LP generates from the Featured Neighborhoods. Should be fine.
- **Blog** — Empty is fine for now.
- **Contact** — LP generates a contact page from the form template. Our CSS styles the form inputs.

---

## Step 6: Verify on Preview

Reload: https://p-6640af74-339a-4bac-8ba6-db2a4dad701d.presencepreview.site/

Check:
- [ ] Nav: "Angelique Lyle" in serif, DRE badge, uppercase links, frosted glass
- [ ] Hero: Coastal imagery, serif name overlay
- [ ] About: New bio text, headshot photo
- [ ] Neighborhoods: 3+ PV area cards with hover zoom
- [ ] Testimonials: Real client quotes
- [ ] Footer: Compass branding, correct address/email, no Sotheby's logo
- [ ] Contact popup: Clean form, black submit button
- [ ] Mobile hamburger menu: No Sotheby's logo in side panel

---

## What the CSS Does (for reference)

The `lp-head-inject.html` file is ~700 lines of CSS that:
- Swaps all fonts to DM Serif Display (headings) + DM Sans (body)
- Forces monochrome palette (black/gray/white, no accent colors)
- Removes all border-radius (sharp/square everything)
- Reskins LP's `.btn-blue` to black
- Adds gradient overlays to neighborhood cards
- Styles the hero with bottom gradient text overlay
- Responsive breakpoints at 1024/900/600px

The `lp-body-inject.html` is ~200 lines of JS that:
- Injects Google Fonts (DM Serif Display + DM Sans)
- Adds scroll shadow to nav (`.al-scrolled` class)
- Has a disabled webhook bridge (for later activation)

Both files are already pasted into LP Global Scripts. Step 1 above only updates
the Head JavaScript with the latest version that includes Sotheby's removal.

---

## After This — What I'll Build Next

Once the reskin looks right, I'll get back to code:
1. Wire the LP Custom Webhook → Cove's `angel_webhook_bp`
2. Add `source` field to Lead model + migration
3. HMAC verification on the webhook
4. Lead dedup (email + 5min window)
5. Twilio SMS notification to Angelique
6. Angel Agent sidecar MVP
