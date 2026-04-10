# Media Library — Content Management Database

## Why This Matters

Every page on TheHillPV.com needs images. The hero needs a PV coastline
shot. Event cards need venue photos. Neighborhood pages need street-level
shots. Archives need historical photos. Market pages need property photos.

Right now it's CSS gradients. The site needs to feel like the Peninsula —
and that means real imagery from real places, managed in a real system.

---

## Image Sourcing Strategy — Priority Order

### Tier 1: Angelique's Own Photos (BEST — owned, authentic, exclusive)

Angelique lives on the Hill. She goes to these events. Her Instagram
(@angeliquelylehomes) already has:
- Lighthouse shots (Point Vicente, sunset behind it)
- Bluff/coastline photos from walks
- Neighborhood street scenes
- Market and event coverage
- Property photos from listings and open houses
- Sunset/ocean views from PVE, RPV, Lunada Bay

**Process:** She sends us photos (or we pull from a shared Google Photos
album / Dropbox). We tag them with location, neighborhood, category, date,
and season. They go into the media library as `source_type: agent_original`.

**Rights:** She owns them. We have full license to use on TheHillPV.com and
AngeliqueLyle.com. No attribution needed. No licensing cost.

### Tier 2: PV Interpretive Center / City of RPV (free, official)

The Point Vicente Interpretive Center (rpvca.gov) is a public facility.
RPV city website has photos of:
- Vicente Bluffs Reserve
- Point Vicente Lighthouse
- Abalone Cove
- Coastal trails and parks
- City events

**Process:** Request media kit from RPV Communications department. Many
public entities will provide high-res photos for community/editorial use.

### Tier 3: PV Library District Archives (historical, licensed)

palosverdeshistory.org — 3,614 historical photos. Watermarked thumbnails
online; high-res scans available for purchase. Requires reproduction
request to the Library District.

**Best candidates:**
- 1920s–30s Malaga Cove Plaza construction
- Marineland era (1954–1987)
- Historical aerial views of the Peninsula
- Early Palos Verdes Estates homes and streets
- La Venta Inn, PV Golf Club, community events

**Process:** Submit reproduction request via palosverdeshistory.org/pages/reproduction.
Budget: ~$15–50 per image. Worth it for the "From the Archives" features.

### Tier 4: Unsplash / Pexels (free stock, generic coastal)

Unsplash (unsplash.com/s/photos/palos-verdes) and Pexels both have PV photos:
- General coastal cliff shots
- Ocean sunset/sunrise
- Beach scenes
- California coastal landscapes

**Rights:** Free for commercial use, no attribution required (Unsplash license).
Good for fallback/generic coastal imagery. Not Peninsula-specific enough
for neighborhood pages.

### Tier 5: Community Contributors (UGC — future)

Once TheHillPV.com has an audience, run a photo submission feature:
"Share your favorite PV moment." Community-submitted photos for the
events calendar, neighborhood pages, seasonal features. Requires a
simple submission form with rights agreement.

### Tier 6: Professional Shoot (highest quality, scheduled)

Hire a local photographer for a half-day shoot of key locations:
- Malaga Cove Plaza (fountain, shops, Lunada Market, Neptune's)
- Lunada Bay bluffs and surf
- Point Vicente Lighthouse
- PV Farmers Market on a Sunday morning
- South Coast Botanic Garden
- Terranea from the coastal trail
- Neighborhood streets (PVE, RPV, RHE)

**Budget:** $500–1,500 for a half-day with a local photographer.
This gives us 50–100 high-quality, owned images that become the
visual backbone of the entire site.

---

## Database Schema

Lives in the `cove` database (Angel is a Cove module). Schema: `angel`.

```sql
-- Media Library: all images/assets for TheHillPV.com content
CREATE TABLE angel.media_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- File info
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path TEXT NOT NULL,              -- S3/R2 path: media/2026/04/lighthouse-sunset.jpg
    file_size INTEGER,                    -- bytes
    mime_type VARCHAR(50) NOT NULL,       -- image/jpeg, image/png, image/webp
    width INTEGER,
    height INTEGER,
    aspect_ratio VARCHAR(10),             -- 16:9, 4:3, 1:1, etc.

    -- Sourcing
    source_type VARCHAR(30) NOT NULL,     -- agent_original, city_official, archive_licensed,
                                          -- stock_free, community_ugc, professional_shoot
    source_name VARCHAR(255),             -- "Angelique Lyle", "PV Library District", "Unsplash"
    source_url TEXT,                       -- Instagram URL, Unsplash URL, archive item URL
    photographer VARCHAR(255),
    license_type VARCHAR(50),             -- owned, cc0, cc_by, editorial_license, purchased
    license_notes TEXT,                   -- any restrictions or attribution requirements
    acquisition_date DATE,
    acquisition_cost DECIMAL(8,2),        -- $0 for free stock, $25 for archive purchases

    -- Content tagging
    title VARCHAR(255),
    alt_text TEXT NOT NULL,               -- accessibility + SEO
    caption TEXT,
    description TEXT,

    -- Location
    neighborhood VARCHAR(100),            -- lunada_bay, malaga_cove, rolling_hills_estates, etc.
    location_name VARCHAR(255),           -- "Point Vicente Lighthouse", "Malaga Cove Plaza"
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),

    -- Classification
    categories TEXT[] NOT NULL DEFAULT '{}',  -- landscape, event, property, historical, aerial,
                                              -- street_scene, food, people, architecture
    tags TEXT[] NOT NULL DEFAULT '{}',         -- sunset, ocean, lighthouse, farmers_market, etc.
    season VARCHAR(20),                   -- spring, summer, fall, winter, all_seasons
    time_of_day VARCHAR(20),              -- golden_hour, sunrise, midday, sunset, blue_hour, night

    -- Usage tracking
    usage_count INTEGER DEFAULT 0,         -- how many times used across site
    last_used_at TIMESTAMP WITH TIME ZONE,
    primary_use VARCHAR(50),              -- hero, card_bg, archive_feature, newsletter,
                                          -- neighborhood_page, event_card, property_card

    -- Quality/editorial
    quality_score INTEGER CHECK (quality_score BETWEEN 1 AND 5),  -- 5 = hero-worthy
    is_hero_eligible BOOLEAN DEFAULT false,  -- approved for full-bleed hero use
    is_approved BOOLEAN DEFAULT false,       -- editorial review passed
    approved_by VARCHAR(100),
    approved_at TIMESTAMP WITH TIME ZONE,

    -- Variants
    has_thumbnail BOOLEAN DEFAULT false,
    thumbnail_path TEXT,
    has_webp BOOLEAN DEFAULT false,
    webp_path TEXT,

    -- Embedding for visual search
    embedding Vector(1024),               -- Ollama qwen3-embedding for visual similarity search

    -- Standard
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX idx_media_neighborhood ON angel.media_assets(neighborhood);
CREATE INDEX idx_media_categories ON angel.media_assets USING GIN(categories);
CREATE INDEX idx_media_tags ON angel.media_assets USING GIN(tags);
CREATE INDEX idx_media_source_type ON angel.media_assets(source_type);
CREATE INDEX idx_media_quality ON angel.media_assets(quality_score) WHERE is_approved = true;
CREATE INDEX idx_media_hero ON angel.media_assets(id) WHERE is_hero_eligible = true AND is_approved = true;
CREATE INDEX idx_media_embedding ON angel.media_assets USING ivfflat(embedding vector_cosine_ops);

-- Usage tracking: which pages/components use which images
CREATE TABLE angel.media_placements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    media_asset_id UUID NOT NULL REFERENCES angel.media_assets(id),
    page_type VARCHAR(50) NOT NULL,       -- events_weekly, neighborhood, school_guide,
                                          -- market_report, newsletter, archive_feature
    page_identifier VARCHAR(255),          -- "this-week-2026-04-06", "lunada-bay", "pvpusd"
    component VARCHAR(50) NOT NULL,        -- hero, card_background, inline_photo,
                                          -- archive_feature, newsletter_header
    position INTEGER,                      -- order if multiple images on same component
    display_width INTEGER,                 -- rendered width in px
    display_height INTEGER,
    crop_params JSONB,                    -- { x: 0, y: 120, width: 1200, height: 400 }
    placed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    removed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_placements_asset ON angel.media_placements(media_asset_id);
CREATE INDEX idx_placements_page ON angel.media_placements(page_type, page_identifier);

-- Collections: curated groups for specific uses
CREATE TABLE angel.media_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,           -- "PV Lighthouse Collection", "Sunset Heroes",
                                          -- "Farmers Market Series", "Historical Malaga Cove"
    description TEXT,
    collection_type VARCHAR(50),          -- hero_rotation, neighborhood, seasonal, event_venue,
                                          -- historical, newsletter
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE angel.media_collection_items (
    collection_id UUID NOT NULL REFERENCES angel.media_collections(id),
    media_asset_id UUID NOT NULL REFERENCES angel.media_assets(id),
    position INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (collection_id, media_asset_id)
);
```

---

## Key Collections to Build First

| Collection | Use Case | Source Priority | Min Images |
|-----------|----------|----------------|------------|
| **Peninsula Heroes** | Full-bleed hero banners for This Week, homepage | Agent original (lighthouse sunset, bluff panoramas) | 6–8 |
| **Lighthouse Series** | Lighthouse anniversary feature, neighborhood pages | Agent IG, RPV city, archive | 4–6 |
| **Farmers Market** | Recurring events section, newsletter | Agent original (Sunday morning shots) | 3–5 |
| **Malaga Cove Historical** | Archives features, neighborhood page | PV Library District (1920s–30s) | 4–6 |
| **Marineland / Terranea** | Archives features, RPV neighborhood | PV Library District + Magazine articles | 3–4 |
| **Neighborhood Street Scenes** | Neighborhood guide cards | Agent original or pro shoot | 8–10 (2 per hood) |
| **South Bay Coastal** | Generic section backgrounds | Unsplash/Pexels (fallback) | 10+ |
| **Event Venue Photos** | Event card backgrounds | Agent original from events | Ongoing |
| **Sunset/Ocean Views** | Newsletter headers, social graphics | Agent IG (golden hour shots) | 5–8 |

---

## Angelique Instagram Image Audit — What to Look For

When cataloging her IG (@angeliquelylehomes), tag each photo with:

1. **Hero-worthy?** — Wide, high-res, no text overlay, good for full-bleed
2. **Neighborhood** — Which PV neighborhood is this?
3. **Category** — Landscape, event, property, street scene, food, people
4. **Season/Time** — Golden hour, midday, sunset, specific season
5. **Location** — Specific venue or landmark name

Priority shots to request from Angelique:
- [ ] Lighthouse at sunset (hero banner #1)
- [ ] Lunada Bay bluffs from Paseo Del Mar (hero banner #2)
- [ ] PV Farmers Market on a Sunday morning
- [ ] Malaga Cove Plaza + Neptune fountain
- [ ] View from Terranea coastal trail
- [ ] South Coast Botanic Garden
- [ ] Abalone Cove tide pools
- [ ] Any neighborhood street scenes she loves
- [ ] PV Interpretive Center / whale watching spot

---

## Immediate Action: Populate Prototype with Real Images

For the v2 prototype (this-week-v2.html), replace CSS gradients with:

1. **Hero banner:** Request from Angelique — lighthouse or bluff sunset shot
   - Fallback: Unsplash PV coastal (photo ID to be sourced)
2. **Featured event (Lighthouse 100th):** Lighthouse photo from Angelique IG
3. **Whale of a Day card:** Ocean/bluff shot
4. **Film Festival card:** Nature/conservation themed
5. **Recurring event cards:** Farmers market, Riviera Village, harbor shots
6. **Photo break divider:** Wide panoramic bluff shot

Once we have 10–15 real images tagged and uploaded, the site transforms
from "nice prototype" to "this is actually our town."

---

## Technical Notes

- Storage: Cloudflare R2 (S3-compatible, included in our infra)
- Image processing: Sharp (Node) or Pillow (Python) for resize/webp conversion
- Every upload generates: original, 1200w hero, 600w card, 300w thumbnail, webp variants
- Alt text is required on every image (accessibility + SEO)
- Embedding: generate via Ollama qwen3-embedding on alt_text + tags for semantic search
  ("show me sunset photos near the lighthouse" → vector similarity query)
