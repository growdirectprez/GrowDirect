# OwnPalosVerdes LP Site Rebuild — Design Spec + Runbook

> **Date:** 2026-04-08
> **Status:** Draft
> **Site:** OwnPalosVerdes (LP site ID: 6640af74-339a-4bac-8ba6-db2a4dad701d)
> **Current state:** Preview Ready, no domain assigned, template scaffold with default content
> **Target:** Rebuild into prototype lead-gen homepage, then assign ownpalosverdes.com domain
> **Approach:** B — Native LP Builder + Script Injection (Phase 2)
> **Live site (angeliquelyle.com) is NOT touched.**

---

## 1. WHAT EXISTS (Current Scaffold)

### Pages
| Page | Status | Action |
|------|--------|--------|
| Home | Default template content | **Gut and rebuild all elements** |
| About | Default bio | **Rewrite copy + replace photo** |
| Active Properties | LP IDX template | Keep — LP handles this |
| Sold Properties | LP IDX template | Keep — LP handles this |
| Property Details | LP template page | Keep |
| Neighborhoods | Default cards | **Replace with PV neighborhoods** |
| Neighborhood Details | Template page | Keep — feeds from CMS |
| Testimonials | Default testimonials | **Replace with our 3 testimonials** |

### Current Homepage Elements (top to bottom)
1. Hero image slider (5 slides of PV homes)
2. "Meet Angelique Lyle" — bio + headshot + social icons + "View Full Bio"
3. Neighborhood cards (Rolling Hills, Redondo Beach, Hermosa Beach) + "View All"
4. Testimonials section (Mary H.)
5. CTA banner — coastal image + "Let's Connect"
6. Footer — address, contact, newsletter signup

### Footer (Global Element)
- Address: 35 Peninsula Center Rolling Hills Estates
- Contact: (310) 751-8335, Angelique@VistaSir.com
- Newsletter: email signup with consent checkbox

---

## 2. TARGET STATE (From Prototype)

### Homepage Sections (mapped from prototype-lp-homepage.html)

| # | Prototype Section | LP Element Type | Content |
|---|------------------|-----------------|---------|
| 1 | Hero with headline + stats | Opening/hero element | "Life above the Pacific starts here." + 4 stats (PVE Median, Top 1.5%, 20+ Years, 5.0 Reviews) |
| 2 | Lead capture form | Form element (overlaid or below hero) | Name, Email, Phone, Interest dropdown, Address. CTA: "Connect with Angelique" |
| 3 | Explore the Hill | 3-card grid element | Neighborhoods, School Guide, Market Report — link to TheHillPV.com |
| 4 | Testimonials | Testimonial element | 3 cards: Mary H. (PVE seller), Dorothy & Bill H. (RHE buyers), Kellner Family (Lunada Bay repeat) |
| 5 | Book Time CTA | CTA/banner element | "Let's find your perfect address." + Schedule Call / Call / Email buttons |
| 6 | Footer | Global element | Updated address, phone, email, DRE#, Compass branding, newsletter |

### Brand Settings (Website Styles)

| Setting | Value | Source |
|---------|-------|--------|
| Primary color | #000000 (black) | Prototype --black |
| Secondary color | #1A1A1A (near-black) | Prototype --near-black |
| Accent / CTA | #000000 (black buttons, white text) | Prototype button style |
| Text body | #1A1A1A | Prototype --near-black |
| Text muted | #666666 | Prototype --gray-600 |
| Background | #FFFFFF | Prototype --white |
| Alt background | #F7F7F7 | Prototype --off-white (testimonials bg) |
| Heading font | DM Serif Display (or closest Google Font) | Prototype --heading |
| Body font | DM Sans (Google Font) | Prototype --body |
| Button style | Black fill, white text, no border-radius | Prototype .form-submit |
| Button hover | #222222 (gray-900) | Prototype hover state |

### Navigation Menu

**Header Menu (Desktop):**
- Neighborhoods → https://thehillpv.com/neighborhoods (external)
- Schools → https://thehillpv.com/schools (external)
- Market → https://thehillpv.com/market (external)
- Reviews → /testimonials (internal)
- Book Time → #book or /contact (internal)

**Phone CTA:** (310) 751-8335

**Side Menu (Mobile):** Same items + Home, About, Properties

---

## 3. RUNBOOK — Step-by-Step LP Builder Instructions

### Phase 1: Website Styles (Global)

**Step 1.1: Open Website Styles**
1. In the builder, click the **Paint Can icon** in the top white nav bar
2. This opens the Website Styles panel on the left

**Step 1.2: Colors**
1. Click **Colors** in the left panel
2. Set primary text color: `#1A1A1A`
3. Set heading color: `#000000`
4. Set link color: `#000000`
5. Set background: `#FFFFFF`
6. Set button primary: background `#000000`, text `#FFFFFF`
7. Set button hover: background `#222222`
8. Save

**Step 1.3: Typography**
1. Click **Typography** in the left panel
2. Set heading font family: **DM Serif Display** (search Google Fonts)
3. Set body font family: **DM Sans** (search Google Fonts)
4. Adjust heading sizes if needed (hero should be large — clamp around 2.4-3.8rem)
5. Set body text size: ~16px (0.95rem)
6. Save

**Step 1.4: Buttons**
1. Click **Buttons** in the left panel
2. Primary button: background `#000000`, text `#FFFFFF`, no border-radius (square corners)
3. Button text: uppercase, letter-spacing 0.1em, font-weight 600
4. Hover: background `#222222`
5. Save

**Step 1.5: Website Branding**
1. Click **Website Branding** in the left panel
2. Upload new favicon (32x32px, LP logo or Angelique monogram)
3. Set loading screen logo
4. Save

---

### Phase 2: Homepage Rebuild

**Step 2.1: Enter Edit Mode**
1. Navigate to Home page in the page dropdown
2. Click **Edit** in the top-right corner

**Step 2.2: Strip Existing Elements**
1. Click three-dots menu > **Reorder Elements**
2. Delete elements we don't want:
   - Remove the existing "Meet Angelique" bio section (we'll rebuild this differently)
   - Remove existing neighborhood cards (replacing with Explore the Hill)
   - Keep: Hero, Testimonials shell, CTA shell
3. Save after removing

**Step 2.3: Rebuild Hero**
1. Click on the hero/opening element
2. In Content settings:
   - Replace headline text with: **"Life above the Pacific starts here."**
   - Subheadline: **"Palos Verdes Peninsula - South Bay Beach Cities"**
   - Update CTA button text: **"HOME SEARCH"** (or "Connect with Angelique")
3. In Images:
   - Keep or replace hero images with high-quality PV peninsula shots
   - Recommended: 1920x1200px JPEG, under 500KB each
4. Save

**Step 2.4: Add Stats Element (below hero)**
1. Hover between hero and next section, click **+** to open element library
2. Search for a **Stats** or **Numbers** element
3. Add 4 stats:
   - `$2.8M` — PVE Median 2026
   - `Top 1.5%` — Agents Nationwide
   - `20+` — Years on the Hill
   - `5.0 ★` — Client Reviews
4. Save

**Step 2.5: Add Lead Capture Form**
1. Hover below stats, click **+** to add element
2. Search for **Form** or **Contact Form** element
3. Configure fields:
   - Full Name (required)
   - Email (required)
   - Phone
   - Interest dropdown: "Looking to buy on the Hill", "Thinking about selling", "Relocating to the South Bay", "Exploring schools for my kids", "Investment property", "Just exploring"
   - Current Address or City (optional)
4. Submit button text: **"Connect with Angelique →"**
5. Form heading: **"Let's find your home."**
6. Subtext: **"Tell me what you're looking for and I'll personally follow up — usually within the hour."**
7. Save

**Step 2.6: Add Explore the Hill Cards**
1. Hover below form, click **+** to add element
2. Search for **Image Cards** or **Grid** element (3-column)
3. Add section heading:
   - Tag: "Explore the Hill"
   - Heading: "Discover what makes this place home."
4. Card 1: **Neighborhoods**
   - Image: PV neighborhood shot (1920x1200px)
   - Tag: "6 Communities"
   - Title: "Neighborhoods"
   - Description: "PVE, RPV, Rolling Hills, RHE + beach cities"
   - Link: https://thehillpv.com/neighborhoods
5. Card 2: **School Guide**
   - Image: School/campus shot
   - Tag: "PVPUSD - Private - Charter"
   - Title: "School Guide"
   - Description: "Feeder patterns, ratings, campus tours"
   - Link: https://thehillpv.com/schools
6. Card 3: **Market Report**
   - Image: Market/aerial PV shot
   - Tag: "Updated Monthly"
   - Title: "Market Report"
   - Description: "Prices, inventory, days on market by zip"
   - Link: https://thehillpv.com/market
7. Save

**Step 2.7: Update Testimonials**
1. First, go to **Content > Testimonials** in the main LP platform (not the builder)
2. Delete or archive all existing testimonials
3. Add 3 new testimonials:

**Testimonial 1:**
- Author: Mary H.
- Detail: Seller - Palos Verdes Estates
- Body: "Angelique made selling our home of 25 years feel manageable. She knew the neighborhood, priced it perfectly, and communicated every step. We got over asking in 9 days."

**Testimonial 2:**
- Author: Dorothy & Bill H.
- Detail: Buyers - Rolling Hills Estates
- Body: "We relocated from Chicago with two kids. Angelique spent hours showing us schools, parks, and the neighborhoods that fit our family. She didn't just find us a house — she found us a community."

**Testimonial 3:**
- Author: The Kellner Family
- Detail: Repeat Clients - Lunada Bay
- Body: "This was our third transaction with Angelique. Her market knowledge is unmatched on the Hill. She told us to wait three weeks before listing — we ended up $200K above what we would have gotten."

4. Return to builder, click on testimonials element
5. In element settings > Select Testimonials, add all 3
6. Reorder if needed
7. Save

**Step 2.8: Update CTA Section**
1. Click on the existing CTA/banner element
2. Update heading: **"Let's find your perfect address."**
3. Update subtext: **"Whether you're buying, selling, or just starting to think about it — a quick call with Angelique is always free and always honest."**
4. Button 1: **"Schedule a Call"** → link to calendar/scheduling URL
5. Button 2: **"Call (310) 751-8335"** → tel:3107518335
6. Button 3: **"Email Angelique"** → mailto:angelique@angeliquelyle.com
7. Below buttons, add text: **"Accardo Real Estate Associates - Compass - CA DRE# 01475592"**
8. Save

---

### Phase 3: Supporting Pages

**Step 3.1: About Page**
1. Switch to About page in page dropdown
2. Click Edit
3. Replace bio text with:

> **Headline:** Life above the Pacific starts here.
>
> **Bio:** Top 1.5% nationally. 20+ years guiding families home to the Peninsula and South Bay. USC grad, relocation specialist, and a mom who raised her kids right here on this Hill.
>
> Whether you are a lifelong resident of the South Bay or relocating to the area, I can assist you. As a Realtor with Vista Sotheby's International Realty and a consistent top producer, I represent fine properties and noteworthy homes with extraordinary lives. I have the experience, perspective, dedication and caring you need on your side.
>
> Please contact me directly anytime at (310) 751-8335 or by email at angelique@angeliquelyle.com.

4. Replace headshot with updated photo (1500x1500px JPEG, under 300KB)
5. Update social media links to current URLs
6. Save

**Step 3.2: Neighborhoods Page**
1. Switch to Neighborhoods page
2. Update neighborhood cards with PV-specific communities:
   - Palos Verdes Estates
   - Rancho Palos Verdes
   - Rolling Hills
   - Rolling Hills Estates
   - Lunada Bay
   - Beach Cities (Redondo, Hermosa, Manhattan)
3. Each card: appropriate image + brief description
4. Save

**Step 3.3: Update Neighborhood CMS Data**
1. Go to Content > Neighborhoods in main platform
2. Add/update entries for each PV community with descriptions
3. These feed into the Neighborhood Details template pages

---

### Phase 4: Global Elements

**Step 4.1: Header Menu**
1. In builder, click **Global Elements** icon (four dots)
2. Select **Header** menu
3. Click Content
4. Replace menu items:
   - Neighborhoods → https://thehillpv.com/neighborhoods (external link)
   - Schools → https://thehillpv.com/schools (external link)
   - Market → https://thehillpv.com/market (external link)
   - Reviews → /testimonials (internal page)
   - Properties → /active-properties (internal page)
5. Save

**Step 4.2: Side Menu (Mobile)**
1. Select **Side Menu** in Global Elements
2. Add same items as Header plus:
   - Home → / (internal)
   - About → /about (internal)
3. Save

**Step 4.3: Footer**
1. Update footer address: **35 Peninsula Center, Rolling Hills Estates**
2. Update contact email: **angelique@angeliquelyle.com** (not VistaSir.com)
3. Update phone: **(310) 751-8335**
4. Update DRE#: **CA DRE# 01475592**
5. Add: **Accardo Real Estate Associates - Compass**
6. Newsletter signup: keep the existing form element
7. Save

---

### Phase 5: SEO Setup

**Step 5.1: Page SEO Titles** (via Page Settings on each page)
| Page | SEO Title (<60 chars) |
|------|----------------------|
| Home | Angelique Lyle - Palos Verdes Real Estate - Compass |
| About | About Angelique Lyle - Top PV Realtor - Compass |
| Active Properties | Palos Verdes Homes for Sale - Angelique Lyle |
| Sold Properties | Recently Sold PV Homes - Angelique Lyle |
| Neighborhoods | Palos Verdes Neighborhoods Guide - Angelique Lyle |
| Testimonials | Client Reviews - Angelique Lyle Real Estate |

**Step 5.2: SEO Preview Images**
- Upload 1200x628px images for each page in Page Settings > SEO Image
- Home: PV coastline panorama or hero image
- About: Angelique headshot
- Properties: Featured listing exterior

**Step 5.3: Google Analytics**
1. Settings > Site Settings > Tracking IDs
2. Add GA4 Measurement ID (starts with G-)

**Step 5.4: Google Search Console**
- Verify domain in GSC after domain is assigned

---

### Phase 6: Domain Assignment

**Step 6.1: Assign ownpalosverdes.com**
1. Once rebuild is complete and reviewed
2. Go to Publish settings for the OwnPalosVerdes site
3. Option A: Custom Domain — enter ownpalosverdes.com
4. Change GoDaddy nameservers to LP's Cloudflare pair
5. Wait 24-48 hours for DNS propagation
6. Verify SSL is working (LP handles this automatically)

**Step 6.2: Set up 301 redirects**
- Redirect old WordPress URLs to new LP pages
- Contact LP support to configure redirects

**Step 6.3: Business email DNS**
- After domain points to LP Cloudflare, send Google Workspace MX/TXT records to LP support

---

### Phase 7: Script Injection (Angel Widget + Webhook)

**Step 7.1: Test Global Scripts access**
1. Settings > Site Settings (or contact LP support)
2. Check if Custom Scripts / Global Scripts section exists
3. If yes: inject Angel chat widget JS
4. If no: contact LP support to enable

**Step 7.2: Angel Chat Widget (future)**
```html
<script src="https://thehillpv.com/static/js/angel-widget.js" defer></script>
```

**Step 7.3: Lead Webhook (future)**
- Configure LP form to POST to: `https://cove.growdirect.com/api/webhooks/lp`
- Or use Zapier as intermediary if LP doesn't support custom webhook URLs

---

## 4. IMAGE CHECKLIST

Prepare these images before starting the build:

| Image | Dimensions | Format | Max Size | Description |
|-------|-----------|--------|----------|-------------|
| Hero slides (3-5) | 1920x1200px | JPEG 85% | 500KB | PV peninsula homes, ocean views, lifestyle |
| Angelique headshot | 1500x1500px | JPEG 85% | 300KB | Professional photo, updated |
| Explore card: Neighborhoods | 1920x1200px | JPEG 85% | 400KB | PV neighborhood streetscape |
| Explore card: Schools | 1920x1200px | JPEG 85% | 400KB | School campus or family scene |
| Explore card: Market | 1920x1200px | JPEG 85% | 400KB | Aerial PV or market chart graphic |
| CTA banner background | 1920x1200px | JPEG 80% | 500KB | Coastal PV scene |
| SEO preview (Home) | 1200x628px | JPEG | - | PV coastline panorama |
| Favicon | 32x32px | ICO/PNG | - | Monogram or logo mark |
| Loading screen logo | - | PNG | - | Full logo with transparency |

**Optimize all with TinyPNG or Squoosh before uploading.**

---

## 5. COPY DOCUMENT

All text content ready to paste into LP elements:

### Hero
- **Eyebrow:** Palos Verdes Peninsula - South Bay Beach Cities
- **Headline:** Life above the Pacific starts here.
- **Subheadline:** Top 1.5% nationally. 20+ years guiding families home to the Peninsula and South Bay. USC grad, relocation specialist, and a mom who raised her kids right here on this Hill.

### Stats
- $2.8M — PVE Median 2026
- Top 1.5% — Agents Nationwide
- 20+ — Years on the Hill
- 5.0 ★ — Client Reviews

### Lead Form
- **Heading:** Let's find your home.
- **Subtext:** Tell me what you're looking for and I'll personally follow up — usually within the hour.
- **Button:** Connect with Angelique →
- **Below form:** No spam. No pressure. Just a real conversation with a real person.
- **Alt CTA:** Book a 15-min call

### Explore the Hill
- **Tag:** Explore the Hill
- **Heading:** Discover what makes this place home.

### CTA
- **Tag:** Ready to Talk?
- **Heading:** Let's find your perfect address.
- **Subtext:** Whether you're buying, selling, or just starting to think about it — a quick call with Angelique is always free and always honest.
- **Footer line:** Accardo Real Estate Associates - Compass - CA DRE# 01475592

### Footer
- **Email:** angelique@angeliquelyle.com (NOT VistaSir.com)
- **Phone:** (310) 751-8335
- **Address:** 35 Peninsula Center, Rolling Hills Estates
- **Legal:** 2026 Angelique Lyle - Accardo Real Estate Associates - Compass

---

## 6. BLOCKED ARTICLES TO READ

Before executing the full build, log into LP help center and read these gated articles:
1. Understanding User Role Permissions
2. AI Lead Nurture — Overview + Complete Guide + How AI Engages
3. Follow Up Boss Pixel
4. Brokerage Listing Network Access
5. Google Tag Manager

---

*Source: prototype-lp-homepage.html + LP Knowledge Base scrape (2026-04-08)*
