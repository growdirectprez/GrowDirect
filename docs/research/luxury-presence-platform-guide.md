# Luxury Presence Platform — Complete Offline Guide

> Scraped from help.luxurypresence.com/helpcenter — 2026-04-08
> ~40 articles fully read, entire topic catalog mapped
> Purpose: Script the complete LP website build without going back to their site

---

## BLOCKED ARTICLES (Require LP Platform Login)

These articles returned "Error" pages — likely gated behind authentication:

1. **Understanding User Role Permissions on the Presence Platform** — `/article/Understanding-User-Role-Permissions-on-the-Presence-Platform`
2. **How AI Lead Nurture Works (Overview)** — `/article/How-AI-Lead-Nurture-Works`
3. **How AI Engages, Qualifies & Prioritizes Leads** — `/article/Understanding-AI-Lead-Nurture-How-AI-Engages-Qualifies-Prioritizes-Leads`
4. **AI Lead Nurture Complete Guide** — `/article/AI-Lead-Nurture-Knowledge-Base`
5. **Understanding the Follow Up Boss Pixel** — `/article/What-is-the-Follow-Up-Boss-Pixel`
6. **How to Log In and Access the Brokerage Listing Network** — `/article/How-to-Log-In-and-Access-the-Brokerage-Listing-Network`
7. **Understanding Google Tag Manager (Meta Tags)** — `/article/How-to-Ensure-A-Meta-Tag-is-Implemented-Correctly`

**Action needed:** Log into the Presence Platform and manually read these 7 articles. The AI Lead Nurture and FUB Pixel articles are particularly important for lead conversion strategy.

---

## 1. COMPLETE TOPIC CATALOG

### Getting Started
- Account Setup
- FAQ & Troubleshooting

### Contacts
- CRM Integrations
- Lead FAQs

### SEO & Analytics
- 3rd Party Widgets
- Analytics
- Google Business Profile
- Google Search Console
- Google Tag Manager
- SEO FAQs

### Home Search & MLS
- MLS Integration & Setup
- Home Search Tool Overview
- Saved Search Alerts & Lead Capture
- MLS FAQ & Troubleshooting

### Video Tutorials
- Product Spotlight
- How-to Videos

### Presence Platform: Content Management
- Properties
- Agents
- Blogs
- Neighborhoods
- Testimonials
- Press Releases
- Developments
- Teams
- Offices

### Presence Platform: Website Builder
- Forms
- Elements
- Menus & Pages
- Logos
- Site Settings
- Media (Images/Videos)
- Website Design
- Password Protection
- Platform FAQ & Troubleshooting

### Tools & Features
- Agent Subdomains
- AI Marketing Specialists (Advertising, Blog, Lead Nurture, SEO)
- Branded Mobile App
- Brokerage Listing Network
- Domains & DNS
- Listing Feeds
- Luxury Presence Mobile App
- Mobile Website
- Presentations
- Property Websites

---

## 2. PLATFORM FUNDAMENTALS

### Website Ownership
- LP websites are **proprietary** — not portable to other platforms
- Monthly plan includes: support for edits, 24/7 uptime monitoring, Amazon Cloud (AWS) hosting, SSL, feature releases, platform training
- LP does NOT proactively manage your content — you must request changes
- Review your specific contract for plan details

### User Management
- **Three roles:** Admin, Member, Guest
- Only Admins can add/edit/remove users
- **Agent profile vs user account** — an agent profile is the public-facing page; a user account is login credentials. You can have 20 agent profiles but only 5 user accounts
- Members MUST be linked to an agent profile (create agent profile first in Content > Agents)
- Admins and Guests can optionally have "No Profile"
- Each user needs a unique email address
- Deleting a user removes login access but does NOT delete their agent profile

### Platform Login
- Login via email + password at the Presence Platform
- Mobile app: "Presence Copilot" — available on App Store and Google Play

---

## 3. DOMAINS & DNS

### Domain Purchase
- **Cannot buy domains through Presence Platform** — must use third-party registrar
- **Recommended registrars:** Squarespace Domains, Namecheap, GoDaddy
- **Avoid Wix** — Wix domains are difficult to connect and cause delays

### Domain Hosting / Nameservers
- LP hosts domains via Cloudflare
- To check who hosts your domain: go to whois.com/whois, check Name Servers
- LP Cloudflare nameserver pairs:
  - `amy.ns.cloudflare.com` & `byron.ns.cloudflare.com` → Luxury Presence
  - `jerry.ns.cloudflare.com` & `meera.ns.cloudflare.com` → Luxury Presence
  - `jose.ns.cloudflare.com` & `raphaela.ns.cloudflare.com` → Luxury Presence
  - `kate.ns.cloudflare.com` & `piotr.ns.cloudflare.com` → **Side Brokerage** (not LP)

### Business Email Setup
- LP does NOT create or provide email addresses
- If LP hosts your domain, they can add DNS records (MX, TXT, CNAME) to Cloudflare
- **Process:** Choose email provider (Google Workspace recommended) → get DNS records from provider → confirm LP hosts your domain → send records to LP support
- DNS propagation: usually 10 minutes, up to 48 hours
- **GoDaddy email:** Email Plus plan, set up through Email & Microsoft 365 dashboard
- Side-hosted domains: contact your Side Business Manager (LP cannot make changes)

### Domain Forwarding
- Configure at your registrar, not in Presence
- Use **301 permanent redirect** (not 302) for SEO
- Enable SSL on forwarded domains to prevent browser warnings
- LP doesn't need to do anything on their end

### Domain Migration (Changing Domains)
- **Only migrate when long-term benefits outweigh short-term SEO impact**
- Audit and preserve all high-performing content
- Create 1:1 old URL → new URL mapping document
- Implement 301 redirects for EVERY page
- Update ALL internal links site-wide
- Confirm HTTPS, www/non-www redirects, trailing slashes at server level
- **Post-migration:** reverify in Google Search Console, submit updated sitemap, use Change of Address tool, install GA4 before launch
- Expect 4-8 weeks for ranking recovery
- Don't restructure content AND change domain simultaneously
- **Recommended domain provider:** Squarespace (Google Domains is deprecated)

### Registrar Access Sharing (for LP to manage DNS)
- LP has guides for sharing access from: GoDaddy, Bluehost, Namecheap, Squarespace, Register.com, Network Solutions, WordPress, DomainPricedRight

---

## 4. SEO STRATEGY

### What LP Handles (if on SEO plan)
- On-page and LLM optimizations via AI SEO Specialist
- SEO migration support
- Business citations and reputation monitoring
- Google Business Profile setup, optimization, monthly posts
- 2 optimized blog posts/month via AI Blog Specialist
- Regular site audits filtering noise from automated reports

### What You Control
- **Meta titles & descriptions** — keep under 60 chars, include keywords
- **Internal links** — descriptive anchor text, no "click here"
- **Blog categories** — organize for navigation (indirect SEO value)
- **Preferred Neighborhoods** — focus AI Blog Specialist on specific areas
- **Page SEO titles** — set on page creation, different from internal Page Name
- **SEO preview images** — 1200x628px JPEG/PNG, set per page in Page Settings
- **Image optimization** — compress/resize before uploading
- **Alt text** — add to all images after uploading (<125 chars, descriptive, include keywords naturally)

### Internal Linking Best Practices
- Every page needs at least one inbound link (no orphan pages)
- Use descriptive anchor text — "Beverly Hills neighborhood guide" not "click here"
- Fewer than 100 links per page (including nav links)
- Link from higher-level pages down to specific pages
- Update older content with links to newer content periodically
- Add links in: content fields, CTA modules, navigation menus, built-in element links

### SEO Audit Reports
- Third-party tools (SEMrush) flag many issues that don't actually matter
- "Critical" in automated report ≠ critical for rankings
- LP sites are already built on SEO best practices
- Focus on: meta titles/descriptions, internal links, broken links, content quality
- Can send audit reports to LP for review
- Check indexed pages: `site:yourdomain.com` in Google

### SEO Timeline
- 3-6 months for meaningful ranking improvements
- New domains may experience Google "sandbox" period
- Depends on: market competitiveness, site age/authority, content consistency, link building

### Page Speed
- LP websites optimized for modern browsers
- Testing tool scores often simulate outdated devices — misleading
- LP actively: removes unused code, streamlines image formats, improves lazy loading, ensures compression
- You should: publish quality content, collect reviews, compress images before uploading

### LLM Visibility (ChatGPT/Gemini)
- LLMs discover agents from trusted third-party sources, not just your website
- **Key platforms to maintain:** Zillow, Realtor.com, Homes.com, Google Business Profile, Yelp, local directories
- Keep NAP (name, address, phone) consistent across all platforms
- **Publish LLM-friendly content:** assert leadership explicitly, first-person content, client success stories
- **Homepage matters significantly:** state mission/positioning upfront, highlight accolades, make differentiation obvious
- **Build brand mentions:** collaborate with local partners, contribute to Quora/Reddit Q&As, seek "best of" editorial features
- **Technical:** ensure bios/testimonials/awards are crawlable, add schema markup, maintain strong backlinks
- If on performance SEO plan, LP handles technical; you handle brand-building activities

### Google Business Profile
- Common issues: suspensions, duplicates, ownership conflicts
- Suspensions: review Google guidelines, submit appeal with supporting docs
- Duplicates: request ownership or delete duplicate
- Ownership conflicts: use Google's request access process
- Two profiles at same address: need distinct names, categories, phone numbers, entrances
- Documentation Google asks for: business license, utility bill, registration certificate, photos of signage

---

## 5. WEBSITE BUILDER

### Website Styles (Global Settings)
- **Colors** — core palette via color picker or HEX codes; per-site only (not global across sites)
- **Buttons** — primary/secondary, hyperlinks, pagination, social icons; customize color, shape, size, hover states
- **Typography** — font families from Google Fonts, sizes, weights, line spacing for headings/body
- **Page Border** — optional border around content area; color, thickness, style
- **Website Branding:**
  - Favicon — 32x32px, ICO or PNG format
  - Loading screen logo
  - Property image placeholders

### Page Types & Creation
- **Pre-configured layouts:** Blog Details, Agent Details, Property Details, Team Details
- **Custom / Blank** — empty canvas for service pages, neighborhood guides, FAQ, testimonials, landing pages
- Pages are **live by URL immediately** but NOT in navigation until manually added
- You can build and preview before making discoverable

| Field | Required | Notes |
|-------|----------|-------|
| Page Type | Yes | Predefined or Custom/Blank |
| Page Name | Yes | Internal only — not shown to visitors |
| Page Path | Yes | URL slug, lowercase with hyphens, starts with / |
| Page SEO Title | Recommended | Browser tab + Google results, <60 chars |

- **Don't change page paths after publishing** — breaks links and hurts rankings
- If you must change, set up a redirect from old path to new

### Navigation Menus
- **Two menus:** Header Menu (desktop/tablet) and Side Menu (mobile)
- **Important:** Header Menu is NOT visible on mobile — always add important pages to BOTH menus
- Managed through Global Elements (four dots icon in top nav)
- Can add: single links, dropdown groups
- Items: reorder via drag (six-dots icon), remove via trash icon
- Each menu is independent — can have different items
- Keep main menu items to 5-7
- Use clear, familiar labels (About, Contact, Services, Blog)
- Group related pages in dropdowns
- Order by importance
- **Landing pages** can have custom navigation menus (separate from main site)
- **Property websites** have separate nav customization
- Agent subdomains: Neighborhoods and Blog Detail pages NOT supported — use redirect to main brand site

### Elements
- Add elements via + icon between sections (hover to reveal)
- Available: text blocks, images, buttons, forms, video, Instagram feed, home valuation, mortgage calculator, and more
- **Reorder:** three-dots menu > Reorder Elements > drag six-dots icon
- **Remove:** trash can icon in Reorder Elements view
- **Padding:** top/bottom padding adjustable per element via Custom toggle + sliders (no left/right padding control — contact support)
- Preview Page option via three-dots menu

### Forms
- Built into the platform
- Lead capture forms on pages
- Connected to LP's lead management system
- Home valuation form captures seller leads

### Password Protection
- Can password-protect individual property listings
- Protected listings show placeholder image instead of photos
- Visitors can enter password OR submit contact form to request access
- Contact form creates a lead in Presence CRM
- No limit on how many properties can be password protected
- Ideal for pocket listings / off-market properties

---

## 6. MEDIA & IMAGES

### Media Gallery
- Central hub for all images
- **Access from:** Settings (organize), Website Builder (replace on page), CMS section (manage per entity)
- **Sections:** Upload Files, My Images (your library), Assigned (in-use images), Curated Images (LP-provided), Stock Images (Unsplash, royalty-free)
- **No folders** — use descriptive filenames instead
- **No image editing** — cannot crop, resize, rotate inside gallery. Use Canva/Photoshop/TinyPNG before uploading
- **No auto-compression** — images stored at uploaded size/quality
- **Supported formats:** JPEG, PNG, GIF, SVG, WebP
- **Alt text:** add after uploading via pen icon. Keep under 125 chars, descriptive, include keywords, don't start with "Image of..."
- **Deleting:** permanent, cannot be recovered. Replace assigned images FIRST, then delete old ones

### Image Specifications

| Image Type | Dimensions | Format | Quality | Max Size |
|-----------|-----------|--------|---------|----------|
| Hero / opening images | 1920x1200px | JPEG | 80-90% | 500 KB |
| Property listing photos | 1920x1200px | JPEG | 85-90% | 500 KB |
| Blog featured images | 1920x1200px | JPEG | 80-90% | 400 KB |
| Media Gallery images | 1920x1200px | JPEG | 80-90% | 400 KB |
| Agent headshots (hi-res) | 1500x1500px | JPEG | 85-90% | 300 KB |
| Agent headshots (light) | 300x300px | JPEG | 85-90% | 50 KB |
| Video thumbnails | 413x245px | JPEG | 85-90% | 100 KB |
| SEO preview images | 1200x628px | JPEG/PNG | High | — |
| Favicon | 32x32px | ICO/PNG | — | — |

**Format rules:** JPEG for photos. PNG only for transparency. SVG for logos. WebP for max compression.

**Optimization workflow:** Choose dimensions → Resize → Compress → Rename descriptively → Upload → Add alt text

**Tools:** ImageResizer, Canva, Photoshop, TinyPNG, Squoosh

### Blurry Listing Images
- Almost always caused by MLS compression
- MLS boards reduce file sizes before syncing
- Fix: replace MLS-synced images with your own 1920x1200px JPEGs
- Turn off Image Sync to prevent MLS from overwriting your custom photos
- Use Birme for free batch resizing

### Video
- **Opening/background videos** (muted, looping): upload directly to Presence
  - Under 30 seconds, 1080p (NOT 4K), MP4 H.264, remove audio, 10-15MB target (50MB max), 24-30fps
  - Compress with: HandBrake (free), Clideo/CloudConvert (browser), Premiere Pro
- **Everything else** (tours, testimonials, market updates, audio): host on YouTube/Vimeo, embed URL
  - Set videos to **Unlisted** — plays on your site but not publicly searchable
  - Adaptive streaming, no file burden on your site, YouTube SEO benefits
- **Blog post videos:** embed YouTube/Vimeo URL via play button icon in Post Body editor (no direct upload)

---

## 7. CONTENT MANAGEMENT

### Properties
- **Add manually:** Content > Properties > Add New — fill in address, price, status, specs, description, features, agent, open house, documents, virtual tour link
- **MLS sync:** most listings import automatically from MLS feed
- **Image specs:** 1920x1200px JPEG, under 500KB, multiple images supported
- **Saving = publishing** — no separate draft/publish step
- Appears in: property grids, property search, individual detail page
- **Property website** vs **property listing:** listing lives on main site; property website is standalone site with own URL
- **Buyer's Agent Sync:** display sold listings where you represented buyer (MLS-dependent, must be activated by LP IDX team, sold listings only, 2-year limit)

### Property Websites
- Dedicated standalone site per listing
- Free subdomain: `123-main-st.luxurypresence.com`
- Custom domain: purchase separately (not Wix), configure via nameservers or DNS records
- Two designs: The Pinnacle, The Edge
- **Included for all clients, unlimited quantity**
- SEO-optimized, ideal for paid ad landing pages
- Integrates with connected CRM
- DNS propagation: 24-48 hours for custom domains

### Blog Posts
- Content > Blog Posts > Add New or edit existing
- **Categories** for organization and filtering (indirect SEO value)
- Blog elements on pages can filter by category
- **Editing:** changes go live immediately on Publish
- **To edit without affecting live:** change status to Draft first, edit, then re-publish
- **Publish date:** can backdate, update to current, or set future (does not unpublish)
- **Don't change URLs on ranking posts** — update content, not the path
- **Tips:** fix errors immediately, add internal links to new content, refresh data every 3-6 months, update seasonal content annually
- RSS feed integration available
- Interactive maps can be added to blog pages
- Social icons on blog pages

### AI Blog Specialist
- Generates SEO-focused blog content
- Rotates through all neighborhoods by default
- **Preferred Neighborhoods:** Settings > Content > Preferred Locations — focus on specific areas
- Once generated, neighborhood assignment is PERMANENT
- Requires active SEO Blog plan

### Testimonials
- Content > Testimonials > Add New
- Required fields: author name, testimonial body (photo optional)
- Two-step: create in CMS, then add to testimonial element on page
- If element has custom order, new testimonials won't appear automatically
- Can control display order via Display Order number or manual drag in element settings

### Agents
- Content > Agents — public-facing profiles (name, bio, headshot, contact, social media)
- Agent profile exists whether or not agent has login access
- Social media links supported: Facebook, Instagram, LinkedIn, TikTok, Twitter/X, YouTube, Yelp, Zillow, GBP, Brokerage URL, Podcast
- Must enter full URLs (not just usernames)
- Instagram feed: connect account via Settings > Connected Accounts (team) or Content > Agents (individual)

### Agent Subdomains
- Personalized landing page on brokerage domain (e.g., `agentname.brokerage.com`)
- **Single-page only** — no blog, neighborhood, or additional pages
- Includes: brokerage branding, IDX search, MLS listings, lead capture, lead routing
- Agents can customize: video headers, lead capture forms, galleries, media, stats, press, forms, home search
- **Not transferable** if agent leaves brokerage
- **Not eligible** for LP marketing packages (need fully branded site for that)
- **SEO:** optimized for agent name + local searches; broader SEO benefit supports brokerage domain authority
- Personal domain can be **forwarded** to subdomain
- Created and managed exclusively by LP team

---

## 8. LEAD CAPTURE & CRM

### Lead Sources
- Home Search Tool favorites and saved searches
- Contact forms on pages
- Newsletter signups
- Property views and activity tracking
- Home valuation form (seller leads)
- Password-protected property access requests

### Listing Alert System
**Favoriting a property** triggers hourly alerts for:
- New Listing, Price Reduction, Price Increase, Back on Market, Pending/Backup Offer, Sold, Withdrawn

**Saved Searches:**

| Frequency | When |
|-----------|------|
| Instant | Every hour for matching changes |
| Daily | 2:30 PM PST |
| Weekly | Mondays 3:30 PM PST |
| Monthly | 1st of month 4:30 PM PST |

- Agents can set frequency for client's saved searches
- Sender name and subject line customizable

### Instant Home Valuation
- Element captures seller leads with automated home value estimates
- Powered by ATTOM data (U.S. addresses only)
- Supported: single-family, townhomes, condos, co-ops, multi-family
- NOT supported: manufactured homes, vacant land, new construction, commercial, international
- Process: visitor enters address → provides name/email/phone to unlock report → views valuation on-screen → copy sent to email → can schedule consultation
- Assign specific agent to valuation experience

### Mortgage Calculator
- Built into Home Search Tool on active listing pages
- Shows estimated monthly payment
- Default: 20% down, 30-year fixed, 7% rate
- Buyers can adjust: down payment, loan type, interest rate, taxes, HOA
- Appears on: Active, Coming Soon, Pending, Under Contract listings

### Native CRM Integrations
- **Follow Up Boss** — API key integration + tracking pixel + import integration
  - Generate API key in FUB: Admin > API > Create API Key
  - Add in Presence: Settings > Integrations > Add New > Follow Up Boss
  - Names must match exactly between platforms for lead routing
  - Separate FUB Import integration needed for non-LP lead sources
- **Compass CRM** — Compass agents only, requires Compass email
  - Settings > CRM Integrations > Add New > Compass CRM
  - No custom lead routing currently
- **Lofty CRM** — direct integration
- **Rechat CRM** — direct integration
- **Cloze CRM** — direct integration

### Webhooks API (for unsupported CRMs)
- **One-way sync only** — LP → external CRM
- Syncs: new lead submissions, contact activity (views, searches, signups)
- Two options:
  1. Custom developer-hosted HTTP POST endpoint (requires REST API experience)
  2. No-code via Zapier
- Webhook signature verification available
- Custom integrations available at additional cost from LP

---

## 9. AI MARKETING SPECIALISTS

### AI Advertising Specialist
- Manages Google + Meta ad campaigns automatically
- Shifts budget to top-performing channels in real time
- Tests messaging and visuals based on engagement
- **All-In plans:** Google (Search, Display, Gmail, YouTube) + Meta (Facebook, Instagram)
  - Phase 1 (first 4-8 weeks): traffic-focused ads
  - Phase 2 (ongoing): retargeting past visitors
- **Leads Pro:** Google PPC (Search) only
- You choose: target audience (buyers/sellers), budget amount
- AI determines: channels, tactics, optimizations
- Results visible in Proof-of-Work Dashboard + weekly/bi-weekly digest email

### AI Blog Specialist
- Generates neighborhood-focused SEO blog content
- Rotates through all neighborhoods by default
- Configure preferred neighborhoods in Settings > Content > Preferred Locations
- Neighborhood assignment per post is permanent once generated

### AI SEO Specialist
- On-page optimization
- LLM optimization (ChatGPT/Gemini visibility)
- Available on Brand plan and above

### AI Lead Nurture Specialist
- **BLOCKED — requires login to read full articles**
- Automated lead follow-up and qualification
- Available on specific plans

---

## 10. TOOLS & FEATURES

### Branded Mobile App
- Custom-branded, mobile-first client collaboration app
- AI-powered: smart notes, chat-style interactions, activity tracking
- Lead capture & retention: white-label, prevents client loss
- Market insights & MLS integration: hyper-local data, real-time updates
- Requires Apple Developer account setup

### Brokerage Listing Network
- **BLOCKED — requires login**
- Off-market / pocket listing management

### 3rd Party Widgets
- Dedicated topic for widget integrations
- **Iframes:** NOT self-serve — must submit code + placement to LP support
- Iframe content NOT indexed by Google (no SEO value)
- Not all iframe codes will work (depends on third-party security settings)
- Follow Up Boss pixel for cross-site tracking

### Analytics & Tracking
- **Google Analytics:** paste GA4 Measurement ID (starts with G-) into Site Settings > Tracking IDs > Client Tracking ID. May take 24 hours.
- **Google Search Console:** separate integration
- **Google Tag Manager:** separate integration (article blocked)
- **Google Business Profile:** manage through Google directly; LP can help with website integration
- Other tracking: Adwerx retargeting pixel, CookieYes cookie banner

### Social Media
- **Instagram feed:** connect via Settings > Connected Accounts (team) or Content > Agents (individual). Display via Instagram element on website.
- **Social media links on profiles:** Facebook, Instagram, LinkedIn, TikTok, Twitter/X, YouTube, Yelp, Zillow, GBP, Brokerage URL, Podcast. Must use full URLs.

---

## 11. COMPLETE SETUP CHECKLIST

### Phase 1: Foundation
- [ ] Confirm domain registrar (Squarespace/Namecheap/GoDaddy recommended)
- [ ] Share registrar access with LP team
- [ ] Set up business email (Google Workspace recommended) + send DNS records to LP
- [ ] Set up Website Styles: colors (HEX), typography (Google Fonts), buttons, page border
- [ ] Upload favicon (32x32px ICO/PNG)
- [ ] Upload loading screen logo
- [ ] Configure property image placeholders
- [ ] Set up user accounts (Admin for you, Members for agents with profiles)

### Phase 2: Analytics & Tracking
- [ ] Create GA4 property, add Measurement ID to Site Settings > Tracking IDs
- [ ] Connect Google Search Console
- [ ] Set up Google Tag Manager
- [ ] Claim and optimize Google Business Profile
- [ ] Install Follow Up Boss pixel (if using FUB)
- [ ] Add CookieYes banner if needed

### Phase 3: SEO
- [ ] Set Page SEO Title on every page (<60 chars with keywords)
- [ ] Set SEO preview images on key pages (1200x628px)
- [ ] Write meta descriptions for key pages
- [ ] Set Preferred Neighborhoods for AI Blog Specialist
- [ ] Build internal linking strategy — no orphan pages, descriptive anchor text
- [ ] Forward all owned domains via 301 redirects
- [ ] Run `site:yourdomain.com` to check indexed pages
- [ ] Request LP SEO audit report review

### Phase 4: Content
- [ ] Create agent profiles (Content > Agents) with full bios, headshots (1500x1500px), social links
- [ ] Add property listings (or verify MLS sync is working)
- [ ] Upload high-res property photos (1920x1200px JPEG, <500KB) — turn off Image Sync if replacing MLS photos
- [ ] Create neighborhood guide pages (Custom/Blank type)
- [ ] Set up blog categories
- [ ] Enable AI Blog Specialist (if on plan)
- [ ] Add testimonials (Content > Testimonials) + add to testimonial element on page
- [ ] Create service/buyer/seller pages
- [ ] Create About page
- [ ] Add press releases if applicable

### Phase 5: Lead Capture
- [ ] Add forms to key pages (contact, home valuation, property inquiries)
- [ ] Add Instant Home Valuation element (if targeting sellers)
- [ ] Configure listing alerts and saved search defaults
- [ ] Customize listing alert sender name + subject line
- [ ] Connect CRM (Follow Up Boss API key, or Compass/Lofty/Rechat/Cloze, or webhooks)
- [ ] Enable AI Lead Nurture (if on plan)
- [ ] Set up Buyer's Agent Sync (if MLS supports it)

### Phase 6: Navigation & UX
- [ ] Build Header Menu (desktop) — 5-7 items max, dropdown groups for related pages
- [ ] Build Side Menu (mobile) — add ALL important pages (mobile only sees Side Menu)
- [ ] Add all new pages to both menus
- [ ] Create custom nav for landing pages if needed
- [ ] Configure property website navigation
- [ ] Test mobile website experience
- [ ] Set up custom loading screen
- [ ] Connect Instagram feed

### Phase 7: Media Optimization
- [ ] Compress all images before uploading (TinyPNG/Squoosh)
- [ ] Add alt text to all uploaded images
- [ ] Upload opening video (if using) — <30s, 1080p, MP4 H.264, no audio, 10-15MB
- [ ] Host longer videos on YouTube/Vimeo (Unlisted), embed via URL
- [ ] Use descriptive filenames for all media

### Phase 8: Advanced
- [ ] Explore Branded Mobile App for client collaboration
- [ ] Set up agent subdomains (if team/brokerage)
- [ ] Configure Brokerage Listing Network (if applicable)
- [ ] Submit iframe requests for needed third-party embeds (not self-serve)
- [ ] Set up Zapier webhooks for CRM automation
- [ ] Enable AI Advertising Specialist (if on plan)
- [ ] Password-protect off-market / pocket listings
- [ ] Build LLM visibility: maintain profiles on Zillow/Realtor.com/GBP/Yelp, assert leadership on homepage, build brand mentions

---

## 12. KEY LIMITATIONS

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| No direct code access (HTML/CSS/JS) | Can't add custom code | Request iframes from LP support |
| Iframes not self-serve | Dependency on LP support | Submit early, batch requests |
| Iframe content not SEO-indexed | Embedded content invisible to Google | Use native LP content instead |
| Google Fonts only | Limited typography | Choose from Google Fonts catalog |
| One-way webhook API | Can't push data INTO LP | Use LP's native CRM integrations |
| Page paths shouldn't change after publish | Breaking change for SEO | Set correct paths at creation |
| Blog post neighborhood is permanent | Can't reassign after generation | Set preferred neighborhoods first |
| Color themes are per-site | No global brand theme | Document HEX codes for consistency |
| No image editing in Media Gallery | Can't crop/resize/rotate | Use Canva/Photoshop/TinyPNG before upload |
| No auto-compression | Large uploads slow site | Always compress before uploading |
| No folders in Media Gallery | Hard to organize | Use descriptive filenames + alt text |
| Top/bottom padding only | No left/right padding control | Contact LP support for advanced layout |
| Sites not portable | Can't export to another platform | LP is proprietary; review contract |
| LP doesn't proactively manage | Content updates require your action | Submit support requests or do it yourself |
| Avoid Wix domains | Connection issues with Presence | Use Squarespace/Namecheap/GoDaddy |
| Agent subdomains are single-page | No blog/neighborhood pages | Use fully branded site for full features |

---

## 13. SUPPORT CONTACTS

- **Live chat:** Log into Presence Platform, gold button bottom-right (fastest, 24/7 except major holidays)
- **Email:** support@luxurypresence.com
- **Phone:** 310-955-1077, option 2

---

*Source: Luxury Presence Knowledge Base (help.luxurypresence.com/helpcenter)*
*~40 articles fully scraped, 7 blocked (require login)*
*Scraped: 2026-04-08*
