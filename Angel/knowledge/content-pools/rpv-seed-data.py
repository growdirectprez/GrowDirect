"""
Rancho Palos Verdes — Content Hub Seed Data
Generated 2026-04-10 from web research.
Use: Database seeding for TheHillPV.com neighborhood pages.

Two exports:
    RPV_ENTITIES  — restaurants, businesses, schools, landmarks, parks
    RPV_EVENTS    — community events (recurring and one-time)
    RPV_VOICE     — Angelique Lyle voice overlay sections
"""

# ---------------------------------------------------------------------------
# 1. ENTITIES
# ---------------------------------------------------------------------------

RPV_ENTITIES = [
    # ── Restaurants: Terranea Resort ──────────────────────────────────────
    {
        "name": "mar'sel",
        "entity_type": "restaurant",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "fine_dining",
        "description": (
            "Terranea's signature fine dining room. Chef Fabio Ugoletti runs "
            "seasonal California tasting menus with Pacific views. The Sunday "
            "brunch draws from across the South Bay."
        ),
        "website": "https://www.terranea.com/dining/marsel",
        "tags": ["fine_dining", "ocean_view", "brunch", "terranea", "date_night"],
    },
    {
        "name": "Nelson's",
        "entity_type": "restaurant",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "casual_dining",
        "description": (
            "Cliff-top casual spot above the coves from the old Sea Hunt TV "
            "series. Fire pits, Baja fish tacos, craft cocktails, and the best "
            "sunset seat on the Peninsula. No reservations — first come, first served."
        ),
        "website": "https://www.terranea.com/dining/nelsons",
        "tags": ["casual", "ocean_view", "sunset", "terranea", "fire_pits", "outdoor"],
    },
    {
        "name": "Catalina Kitchen",
        "entity_type": "restaurant",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "casual_dining",
        "description": (
            "Terranea's all-day restaurant. Coastal California comfort food — "
            "elevated but relaxed. The breakfast buffet is popular with resort "
            "guests and locals alike."
        ),
        "website": "https://www.terranea.com/dining/catalina-kitchen",
        "tags": ["breakfast", "brunch", "casual", "terranea", "ocean_view", "family"],
    },

    # ── Restaurants: Golden Cove Shopping Center ──────────────────────────
    {
        "name": "Avenue Italy",
        "entity_type": "restaurant",
        "address": "31243 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "italian",
        "description": (
            "Lively Italian at Golden Cove. Wood-fired pizzas, handmade pasta, "
            "and a full bar. Family-friendly with a patio that catches the "
            "afternoon breeze. Weekend waits are real — go early or make a reservation."
        ),
        "website": "https://avenueitaly.com/",
        "tags": ["italian", "golden_cove", "family", "patio", "pizza", "pasta"],
    },
    {
        "name": "Swan Thai",
        "entity_type": "restaurant",
        "address": "31234 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "thai",
        "description": (
            "Authentic Thai in Golden Cove. The marinated shrimp spring rolls "
            "and crispy garlic wings are standouts. Consistent quality, quick "
            "lunch service, and a loyal local following."
        ),
        "website": None,
        "tags": ["thai", "golden_cove", "lunch", "takeout"],
    },
    {
        "name": "Peninsula Tap House",
        "entity_type": "restaurant",
        "address": "31234 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "bar_and_grill",
        "description": (
            "Craft beer bar in Golden Cove with 18 rotating taps, pub grub, "
            "darts, and a jukebox. The outdoor patio is the move on warm evenings. "
            "Low-key neighborhood hangout energy."
        ),
        "website": None,
        "tags": ["craft_beer", "golden_cove", "bar", "patio", "casual"],
    },
    {
        "name": "Asaka Sushi",
        "entity_type": "restaurant",
        "address": "31234 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "japanese",
        "description": (
            "Neighborhood sushi spot in Golden Cove. Fresh fish, solid rolls, "
            "and a small but loyal clientele. Good for a quick lunch or casual dinner."
        ),
        "website": None,
        "tags": ["sushi", "japanese", "golden_cove", "casual"],
    },
    {
        "name": "Poke Me",
        "entity_type": "restaurant",
        "address": "31234 Palos Verdes Dr W Ste A, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "poke",
        "description": (
            "Build-your-own poke bowls in Golden Cove. Fresh, fast, and "
            "customizable. Popular with the post-hike and after-school crowds."
        ),
        "website": None,
        "tags": ["poke", "golden_cove", "healthy", "quick_service"],
    },
    {
        "name": "Tomatillo Mexican Grill",
        "entity_type": "restaurant",
        "address": "31234 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "mexican",
        "description": (
            "Casual Mexican grill in Golden Cove. Burritos, tacos, and bowls "
            "with fresh ingredients. Fast counter service, good for families."
        ),
        "website": None,
        "tags": ["mexican", "golden_cove", "casual", "family", "quick_service"],
    },
    {
        "name": "Yellow Vase",
        "entity_type": "restaurant",
        "address": "31176 Hawthorne Blvd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "cafe",
        "description": (
            "French-California cafe, florist, and bakery — all in one space. "
            "The brioche French toast draws weekend crowds. Also has a location "
            "in Malaga Cove. Great for client meetings and casual brunch."
        ),
        "website": "https://yellowvase.com/",
        "tags": ["cafe", "brunch", "bakery", "florist", "golden_cove"],
    },

    # ── Restaurants: Other RPV ────────────────────────────────────────────
    {
        "name": "Trump National Golf Club Restaurant",
        "entity_type": "restaurant",
        "address": "1 Ocean Trails Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "fine_dining",
        "description": (
            "Clubhouse restaurant at Trump National overlooking the 18th green "
            "and the Pacific. Open to the public for dining. California-American "
            "menu with ocean views that stretch to Catalina."
        ),
        "website": "https://www.trumpnationallosangeles.com/dining",
        "tags": ["fine_dining", "ocean_view", "golf", "portuguese_bend"],
    },

    # ── Businesses ────────────────────────────────────────────────────────
    {
        "name": "Terranea Resort",
        "entity_type": "business",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "resort_hotel",
        "description": (
            "102-acre oceanfront resort on the site of the old Marineland. "
            "Four restaurants, full spa, golf course, multiple pools, kayaking, "
            "and coastal trails. The anchor destination for visitors to RPV."
        ),
        "website": "https://www.terranea.com/",
        "tags": ["resort", "hotel", "spa", "ocean", "destination", "weddings"],
    },
    {
        "name": "Trump National Golf Club Los Angeles",
        "entity_type": "business",
        "address": "1 Trump National Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "golf_club",
        "description": (
            "Championship 18-hole course along the Portuguese Bend coastline. "
            "Dramatic cliffside holes, ocean views on every fairway, and a "
            "30,000 sq ft clubhouse. Private membership with public dining."
        ),
        "website": "https://www.trumpnationallosangeles.com/",
        "tags": ["golf", "private_club", "ocean_view", "portuguese_bend"],
    },
    {
        "name": "Golden Cove Shopping Center",
        "entity_type": "business",
        "address": "31176 Hawthorne Blvd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "shopping_center",
        "description": (
            "RPV's main retail hub at Hawthorne and Palos Verdes Drive West. "
            "Anchored by Trader Joe's, with 20+ shops and restaurants. Ocean "
            "views from the parking lot — the kind of thing you stop noticing "
            "until a visitor points it out."
        ),
        "website": "https://shopgoldencove.com/",
        "tags": ["shopping", "trader_joes", "retail", "dining", "golden_cove"],
    },
    {
        "name": "Trader Joe's — Golden Cove",
        "entity_type": "business",
        "address": "31176 Hawthorne Blvd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "grocery",
        "description": (
            "The anchor of Golden Cove. Standard Trader Joe's with the usual "
            "loyal following. Parking lot gets intense on weekends."
        ),
        "website": "https://locations.traderjoes.com/ca/rancho-palos-verdes/",
        "tags": ["grocery", "golden_cove", "shopping"],
    },
    {
        "name": "Golden Cove Pharmacy",
        "entity_type": "business",
        "address": "31234 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "pharmacy",
        "description": (
            "Independent pharmacy in Golden Cove. Old-school service — they "
            "know your name and your prescriptions. A neighborhood institution."
        ),
        "website": None,
        "tags": ["pharmacy", "golden_cove", "healthcare"],
    },

    # ── Landmarks & Parks ─────────────────────────────────────────────────
    {
        "name": "Point Vicente Lighthouse",
        "entity_type": "business",
        "address": "31550 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "landmark",
        "description": (
            "Built in 1926, celebrating its centennial in 2026. The lighthouse "
            "sits on 130-foot bluffs and is open to visitors on the second "
            "Saturday of each month. The adjacent Interpretive Center covers "
            "Peninsula history, geology, and gray whale migration."
        ),
        "website": "https://palosverdes.com/pvlight/",
        "tags": ["landmark", "lighthouse", "whale_watching", "history", "views"],
    },
    {
        "name": "Point Vicente Interpretive Center",
        "entity_type": "business",
        "address": "31501 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "museum",
        "description": (
            "10,000 square feet of exhibits on Peninsula natural history, the "
            "gray whale, and local geology. Daily hours 10am-5pm. The whale "
            "viewing deck is the best free vantage point during migration season "
            "(December through April)."
        ),
        "website": "https://www.rpvca.gov/",
        "tags": ["museum", "whale_watching", "education", "family", "views"],
    },
    {
        "name": "Abalone Cove Shoreline Park",
        "entity_type": "business",
        "address": "5970 Palos Verdes Dr S, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "park",
        "description": (
            "109-acre ecological reserve with two beaches (Abalone Cove and "
            "Sacred Cove), tide pools, bluff trails, and a State Marine "
            "Conservation Area. Parking opens at 9am. The tide pools are "
            "some of the best in LA County — go at low tide."
        ),
        "website": "https://www.rpvca.gov/1178/Abalone-Cove-Shoreline-Park-Reserve",
        "tags": ["beach", "tide_pools", "hiking", "nature", "reserve", "family"],
    },
    {
        "name": "South Coast Botanic Garden",
        "entity_type": "business",
        "address": "26300 Crenshaw Blvd, Palos Verdes Peninsula, CA 90274",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "garden",
        "description": (
            "87 acres of gardens built on a former landfill — one of the great "
            "reclamation stories in LA. Rotating exhibitions (Trolls through "
            "October 2026), monthly dog walks, concerts, and seasonal butterfly "
            "experiences. Open daily 8am-5pm."
        ),
        "website": "https://southcoastbotanicgarden.org/",
        "tags": ["garden", "nature", "family", "events", "art", "dog_friendly"],
    },
    {
        "name": "Wayfarers Chapel",
        "entity_type": "business",
        "address": "5755 Palos Verdes Dr S, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "landmark",
        "description": (
            "Lloyd Wright's glass-and-redwood chapel, built in 1951. Dismantled "
            "in 2024 due to Portuguese Bend landslide movement. Planned "
            "relocation to Battery Barnes site near RPV City Hall — about one "
            "mile west of the original location. Federal land transfer "
            "legislation pending. A defining piece of Peninsula identity."
        ),
        "website": "https://www.wayfarerschapel.org/",
        "tags": ["landmark", "architecture", "lloyd_wright", "chapel", "history", "relocation"],
    },
    {
        "name": "Ladera Linda Community Park",
        "entity_type": "business",
        "address": "32201 Forrestal Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "park",
        "description": (
            "Hilltop park with a brand-new community center (opened February "
            "2024). Basketball court, paddle tennis, playground, hiking trail "
            "access, and a multipurpose room. Open 8am to one hour after sunset."
        ),
        "website": "https://www.rpvca.gov/facilities/facility/details/Ladera-Linda-Community-Park-9",
        "tags": ["park", "community_center", "playground", "hiking", "paddle_tennis"],
    },
    {
        "name": "Del Cerro Park",
        "entity_type": "business",
        "address": "30940 Crenshaw Blvd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "park",
        "description": (
            "4.5-acre blufftop park with panoramic ocean and Catalina views. "
            "Open field, walking paths, and one of the best kite-flying spots "
            "on the Peninsula. Quiet and uncrowded on weekdays."
        ),
        "website": "https://www.rpvca.gov/138/Parks-Facilities",
        "tags": ["park", "views", "ocean_view", "catalina", "open_space"],
    },

    # ── Schools ───────────────────────────────────────────────────────────
    {
        "name": "Point Vicente Elementary",
        "entity_type": "school",
        "address": "30540 Rue De La Pierre, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "elementary",
        "description": (
            "PVPUSD elementary (K-5) in the heart of RPV. Strong test scores, "
            "engaged parent community, and a campus surrounded by open space. "
            "Feeds into Ridgecrest Intermediate."
        ),
        "website": "https://pointvicente.pvpusd.net/",
        "tags": ["school", "elementary", "pvpusd", "k5"],
    },
    {
        "name": "Soleado Elementary",
        "entity_type": "school",
        "address": "27800 Longhill Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "elementary",
        "description": (
            "PVPUSD elementary serving the Eastview area of RPV. Consistent "
            "academic performance and a tight-knit school community."
        ),
        "website": "https://soleado.pvpusd.net/",
        "tags": ["school", "elementary", "pvpusd", "k5", "eastview"],
    },
    {
        "name": "Mira Catalina Elementary",
        "entity_type": "school",
        "address": "30511 Lucania Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "elementary",
        "description": (
            "PVPUSD elementary with strong academics and an active PTA. Located "
            "in the Mira Catalina neighborhood near Abalone Cove."
        ),
        "website": "https://miracatalina.pvpusd.net/",
        "tags": ["school", "elementary", "pvpusd", "k5"],
    },
    {
        "name": "Silver Spur Elementary",
        "entity_type": "school",
        "address": "5500 Ironwood St, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "elementary",
        "description": (
            "PVPUSD elementary in the Silver Spur area. Well-regarded academics "
            "and a campus that benefits from the neighborhood's family orientation."
        ),
        "website": "https://silverspur.pvpusd.net/",
        "tags": ["school", "elementary", "pvpusd", "k5"],
    },
    {
        "name": "Cornerstone at Pedregal Elementary",
        "entity_type": "school",
        "address": "27800 Longhill Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "elementary",
        "description": (
            "PVPUSD elementary with a project-based learning emphasis. Located "
            "on the Soleado campus in the Eastview area of RPV."
        ),
        "website": "https://cornerstone.pvpusd.net/",
        "tags": ["school", "elementary", "pvpusd", "k5", "project_based"],
    },
    {
        "name": "Ridgecrest Intermediate",
        "entity_type": "school",
        "address": "28915 Northbay Rd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "middle",
        "description": (
            "PVPUSD middle school (6-8) drawing from RPV elementary feeders. "
            "Strong STEM programs, performing arts, and competitive athletics."
        ),
        "website": "https://ris.pvpusd.net/",
        "tags": ["school", "middle", "pvpusd", "6_8"],
    },
    {
        "name": "Miraleste Intermediate",
        "entity_type": "school",
        "address": "29323 Palos Verdes Dr E, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "middle",
        "description": (
            "PVPUSD middle school (6-8) serving the eastern side of RPV. "
            "Active parent involvement and a solid extracurricular program."
        ),
        "website": "https://miraleste.pvpusd.net/",
        "tags": ["school", "middle", "pvpusd", "6_8", "eastview"],
    },
    {
        "name": "Palos Verdes Peninsula High School",
        "entity_type": "school",
        "address": "27118 Silver Spur Rd, Rolling Hills Estates, CA 90274",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rolling Hills Estates",
        "category": "high_school",
        "description": (
            "One of two PVPUSD high schools. 10/10 GreatSchools, A+ Niche, "
            "97% graduation rate. Many RPV students attend here. The Sea Kings "
            "athletics program and the performing arts department are standouts."
        ),
        "website": "https://peninsula.pvpusd.net/",
        "tags": ["school", "high_school", "pvpusd", "9_12"],
    },
    {
        "name": "Palos Verdes High School",
        "entity_type": "school",
        "address": "600 Cloyden Rd, Palos Verdes Estates, CA 90274",
        "neighborhood": "rancho_palos_verdes",
        "city": "Palos Verdes Estates",
        "category": "high_school",
        "description": (
            "The other PVPUSD high school. 10/10 GreatSchools, average SAT "
            "around 1330, strong AP program. Some RPV neighborhoods feed here. "
            "Top 5% of California school districts."
        ),
        "website": "https://pvhs.pvpusd.net/",
        "tags": ["school", "high_school", "pvpusd", "9_12"],
    },
    {
        "name": "Dodson Middle School",
        "entity_type": "school",
        "address": "28014 Montereina Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "rancho_palos_verdes",
        "city": "Rancho Palos Verdes",
        "category": "middle",
        "description": (
            "LAUSD middle school within RPV city limits, serving the Eastview "
            "area. An important note for buyers: parts of RPV fall in LAUSD, "
            "not PVPUSD. Always verify school boundaries before purchasing."
        ),
        "website": None,
        "tags": ["school", "middle", "lausd", "6_8", "eastview"],
    },
]


# ---------------------------------------------------------------------------
# 2. EVENTS
# ---------------------------------------------------------------------------

RPV_EVENTS = [
    {
        "title": "Whale of a Day Festival",
        "event_date": None,
        "location_name": "Point Vicente Interpretive Center",
        "neighborhood": "rancho_palos_verdes",
        "category": "festival",
        "description": (
            "Annual gray whale migration celebration at Point Vicente. Free "
            "admission. Food trucks, kids' activities, beer and wine garden, "
            "lighthouse tours. The 41st annual was held April 2026. Shuttle "
            "from Ken Dyda Civic Center."
        ),
        "is_recurring": True,
    },
    {
        "title": "July 4th Celebration",
        "event_date": None,
        "location_name": "Ken Dyda Civic Center",
        "neighborhood": "rancho_palos_verdes",
        "category": "festival",
        "description": (
            "RPV's signature summer event, 3pm-9pm. Live music, dancing, rides, "
            "inflatables, food and dessert booths, beer and wine, and a drone "
            "light show at dusk. The whole city turns out."
        ),
        "is_recurring": True,
    },
    {
        "title": "Cactus & Succulent Show and Sale",
        "event_date": None,
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rancho_palos_verdes",
        "category": "garden",
        "description": (
            "Annual show and sale at the Botanic Garden. Rare specimens, expert "
            "growers, and everything you need for a drought-tolerant garden. "
            "Held each spring."
        ),
        "is_recurring": True,
    },
    {
        "title": "Trolls: A Field Study",
        "event_date": None,
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rancho_palos_verdes",
        "category": "art",
        "description": (
            "Large-scale troll sculptures installed throughout the garden. "
            "Running through October 2026. Outdoor art experience that works "
            "for all ages. Worth a garden membership."
        ),
        "is_recurring": False,
    },
    {
        "title": "SOAR: Tropical Butterflies",
        "event_date": None,
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rancho_palos_verdes",
        "category": "nature",
        "description": (
            "Annual immersive butterfly experience at the Botanic Garden. "
            "Walk-through enclosure with hundreds of tropical species. Opens "
            "each May and sells out — book early."
        ),
        "is_recurring": True,
    },
    {
        "title": "Dogtoberfest",
        "event_date": None,
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rancho_palos_verdes",
        "category": "community",
        "description": (
            "October dog-friendly festival at the Botanic Garden. Costume "
            "contests, vendors, and a full day out with your dog."
        ),
        "is_recurring": True,
    },
    {
        "title": "Dog Walking Day",
        "event_date": None,
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rancho_palos_verdes",
        "category": "community",
        "description": (
            "Last Sunday of every month, dogs are welcome to walk the Botanic "
            "Garden trails. Low-key, social, and one of the few off-leash-ish "
            "events on the Peninsula."
        ),
        "is_recurring": True,
    },
    {
        "title": "Native Plant Garden Volunteer Day",
        "event_date": None,
        "location_name": "Various RPV locations",
        "neighborhood": "rancho_palos_verdes",
        "category": "volunteer",
        "description": (
            "Monthly habitat restoration and planting events run by PVPLC. "
            "Great way to meet neighbors and learn the native plant landscape "
            "of the Peninsula."
        ),
        "is_recurring": True,
    },
    {
        "title": "Point Vicente Lighthouse Open House",
        "event_date": None,
        "location_name": "Point Vicente Lighthouse",
        "neighborhood": "rancho_palos_verdes",
        "category": "history",
        "description": (
            "The lighthouse opens to visitors on the second Saturday of every "
            "month. Free admission. Docent-led tours of the 1926 lighthouse — "
            "celebrating its centennial in 2026."
        ),
        "is_recurring": True,
    },
    {
        "title": "PV Farmers Market",
        "event_date": None,
        "location_name": "Peninsula High School",
        "neighborhood": "rancho_palos_verdes",
        "category": "market",
        "description": (
            "Every Sunday, 8am-1pm at the Peninsula High campus (Hawthorne & "
            "Silver Spur). Year-round. Produce, artisan goods, prepared food, "
            "and the neighborhood social scene. Get there before 9 for the "
            "best selection."
        ),
        "is_recurring": True,
    },
    {
        "title": "Rolling Ranchos Neighborhood Garage Sale",
        "event_date": None,
        "location_name": "Rolling Ranchos neighborhood",
        "neighborhood": "rancho_palos_verdes",
        "category": "community",
        "description": (
            "Annual spring neighborhood-wide garage sale. Dozens of homes "
            "participate across the Rolling Ranchos area of RPV."
        ),
        "is_recurring": True,
    },
    {
        "title": "Shredding Event",
        "event_date": None,
        "location_name": "Ken Dyda Civic Center",
        "neighborhood": "rancho_palos_verdes",
        "category": "community",
        "description": (
            "Free drive-through document shredding hosted by the City. Held "
            "several times per year. Bring boxes, they handle the rest."
        ),
        "is_recurring": True,
    },
]


# ---------------------------------------------------------------------------
# 3. VOICE OVERLAY — Angelique Lyle first-person content
# ---------------------------------------------------------------------------

RPV_VOICE = {
    "neighborhood_slug": "rancho_palos_verdes",
    "city": "Rancho Palos Verdes",
    "byline": "Angelique Lyle",
    "updated": "April 2026",

    "intro": (
        "Rancho Palos Verdes is the biggest city on the Peninsula — about "
        "42,000 people spread across 13 square miles of bluffs, canyons, and "
        "coastline. And that's exactly why it feels different from the other PV "
        "cities. RPV has range. You can be in a quiet cul-de-sac above "
        "Portuguese Bend watching pelicans skim the water, or grabbing Thai "
        "food at Golden Cove ten minutes later. It's not one thing. It's a "
        "collection of micro-neighborhoods, each with its own character, held "
        "together by the ocean, the preserves, and some of the best schools "
        "in California.\n\n"
        "I've sold homes in every corner of RPV — from the oceanfront estates "
        "along Palos Verdes Drive South to the townhomes near Highridge Road. "
        "What I tell every client is the same thing: drive it at golden hour. "
        "When the light hits the cliffs and Catalina sharpens on the horizon, "
        "you'll understand why people stay."
    ),

    "real_estate": (
        "The RPV market covers a wider range than people expect. The median "
        "sale price is running around $1.7 million as of early 2026, but "
        "that number hides the real story. You can find condos and townhomes "
        "starting below $800K in areas like Eastview and Sea Terrace. Move "
        "toward the coast — Portuguese Bend, Abalone Cove, the Trump National "
        "corridor — and you're looking at $3M to $10M+ for ocean-facing lots. "
        "The average home value sits near $1.84M, and homes are selling at "
        "about 98% of asking price.\n\n"
        "Inventory is moderate — around 115 homes on the market at any given "
        "time, with a median of 58 days to pending. That's slower than Lunada "
        "Bay or Malaga Cove, partly because RPV has more variety and a bigger "
        "footprint. The micro-markets matter here more than anywhere else on "
        "the Hill. A home in Eastview (LAUSD schools) prices very differently "
        "from one in the PVPUSD attendance zone two streets over. I walk "
        "clients through that boundary map early — it changes everything.\n\n"
        "The median household income is about $175,000, and the population "
        "skews older than the rest of LA — median age around 50. That's "
        "changing as younger families discover they can enter the PV market "
        "here at a lower price point than PVE or Rolling Hills."
    ),

    "highlights": (
        "Here's what makes RPV worth your attention:\n\n"
        "**Terranea Resort** is the anchor. A 102-acre oceanfront destination "
        "built on the old Marineland site. Three restaurants — mar'sel for "
        "fine dining, Catalina Kitchen for all-day, and Nelson's for sunset "
        "cocktails on the cliffs. I take every out-of-town client to Nelson's. "
        "When someone asks me why this area, I don't show them a spreadsheet. "
        "I take them to a fire pit overlooking the Pacific.\n\n"
        "**Point Vicente Lighthouse** turned 100 in 2026. It's open to the "
        "public one Saturday a month, and the Interpretive Center next door "
        "is worth a visit for the whale exhibits alone. During gray whale "
        "season (December through April), you can watch from the bluff deck "
        "for free.\n\n"
        "**Abalone Cove** is 109 acres of tide pools, two beaches, and "
        "bluff trails above a Marine Conservation Area. The tide pools are "
        "among the best in LA County. Go at low tide with the kids and plan "
        "to lose two hours.\n\n"
        "**South Coast Botanic Garden** — 87 acres of gardens reclaimed from "
        "a former landfill. The Trolls sculpture exhibition runs through "
        "October 2026, the annual butterfly experience opens each May, and "
        "the monthly dog walk is a favorite.\n\n"
        "**Wayfarers Chapel** — Lloyd Wright's glass-and-redwood chapel was "
        "dismantled in 2024 due to Portuguese Bend land movement. The plan is "
        "to rebuild it about a mile west at Battery Barnes near City Hall. "
        "Federal land transfer legislation is in progress. This is a story "
        "the whole Peninsula is watching.\n\n"
        "**Portuguese Bend** is the wildest stretch of coast in LA County — "
        "active landslide geology, the Portuguese Bend Reserve with 400 acres "
        "of trails, and some of the most dramatic homesites on the Peninsula. "
        "It's not for everyone, and that's the point."
    ),

    "dining": (
        "RPV eating breaks into two categories: resort dining and neighborhood "
        "dining.\n\n"
        "The resort side is Terranea. **mar'sel** is where I go for a "
        "celebratory dinner or to close a deal — seasonal tasting menus, "
        "ocean views, and impeccable service. **Nelson's** is the casual play "
        "— you're sitting on a cliff above the coves, fire pits going, Baja "
        "fish tacos in hand, watching the sun drop behind Catalina. It's the "
        "single best sunset dining spot on the Peninsula. **Catalina Kitchen** "
        "handles breakfast and all-day dining with a coastal California menu.\n\n"
        "The neighborhood side centers on **Golden Cove Shopping Center** at "
        "Hawthorne and PV Drive West. **Avenue Italy** is the standout — "
        "lively, family-friendly Italian with a patio. **Swan Thai** is "
        "consistent and quick. **Peninsula Tap House** is 18 taps of craft "
        "beer and good pub energy. **Yellow Vase** does French-California cafe "
        "and florist in one — the brioche French toast is a weekend ritual. "
        "**Poke Me** and **Tomatillo** handle the fast-casual side.\n\n"
        "For a special occasion, **Trump National's clubhouse restaurant** is "
        "open to the public and the Pacific views from the dining room are "
        "genuinely staggering."
    ),

    "community": (
        "RPV runs like a well-managed city that mostly stays out of your way. "
        "The city incorporated in 1973 and has kept a low-density, residential "
        "character ever since. No commercial high-rises, no strip malls beyond "
        "Golden Cove and the Peninsula Center area. The tradeoff is that you "
        "drive for most errands — this is not a walkable city in the urban "
        "sense. But the payoff is space, quiet, and 1,400+ acres of preserved "
        "open space.\n\n"
        "The school situation requires attention. Most of RPV feeds into "
        "**PVPUSD** — one of the top districts in California. Point Vicente "
        "Elementary, Soleado, Mira Catalina, and Silver Spur are the RPV "
        "elementary feeders, with Ridgecrest and Miraleste as the intermediate "
        "schools. But parts of Eastview RPV are zoned for **LAUSD** — Dodson "
        "Middle School, Crestwood Elementary. The difference in property values "
        "across that boundary is significant. I always pull the school zone map "
        "with clients before they fall in love with a house.\n\n"
        "Community events happen year-round. The **July 4th Celebration** at "
        "Civic Center is the big one — drone light show, food trucks, the "
        "whole city shows up. **Whale of a Day** at Point Vicente draws "
        "thousands every April. The **Farmers Market** every Sunday at "
        "Peninsula High is a weekly ritual for most families. South Coast "
        "Botanic Garden runs programs almost every weekend.\n\n"
        "The Portuguese Bend landslide situation is the elephant in the room "
        "for parts of RPV. Active land movement has been ongoing for decades "
        "in the southern corridor. It forced the Wayfarers Chapel dismantling "
        "and affects infrastructure and home values in the area. If you're "
        "looking at Portuguese Bend or the south coast, we need to have an "
        "honest conversation about geology. I don't sugarcoat that — I explain "
        "it, and then we figure out if the view is worth the risk for you."
    ),

    "further_reading": (
        "- [RPV Official City Calendar](https://www.rpvca.gov/Calendar.aspx) "
        "— Events, council meetings, recreation programs\n"
        "- [South Coast Botanic Garden](https://southcoastbotanicgarden.org/) "
        "— Exhibitions, classes, seasonal events\n"
        "- [PVPLC Events](https://pvplc.org/events) — Guided hikes, "
        "volunteer days, nature programs\n"
        "- [Terranea Resort](https://www.terranea.com/) — Dining, spa, events\n"
        "- [Wayfarers Chapel Rebuilding](https://www.wayfarerschapel.org/) "
        "— Relocation updates\n"
        "- [PVPUSD School Finder](http://schools.pvpusd.net/) — Verify "
        "attendance boundaries\n"
        "- [Rancho Palos Verdes Housing Market (Redfin)](https://www.redfin.com/"
        "city/15404/CA/Rancho-Palos-Verdes/housing-market) — Current stats\n"
        "- [Palos Verdes Source](https://palosverdessource.com/) — Local "
        "news and home sales data\n"
        "- [South Bay by Jackie Weekend Guide](https://www.southbaybyjackie.com/"
        "weekend-guide.php) — Weekly events roundup"
    ),

    "closing": (
        "RPV is the city where you can find your version of Peninsula life "
        "without a $4M entry fee. It has the schools, the coastline, the "
        "preserves, and the quiet. What it doesn't have is pretension — this "
        "is a city of families, retirees, and people who chose the view over "
        "the commute. I've watched buyers circle back to RPV after looking at "
        "every other South Bay city, and the reason is always the same: the "
        "space, the light, and the fact that you can stand on your deck and "
        "see Catalina.\n\n"
        "If you're thinking about RPV, call me. I'll drive you through the "
        "neighborhoods, show you where the school boundaries actually fall, "
        "and find you the right block — not just the right house."
    ),
}


# ---------------------------------------------------------------------------
# Quick validation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Entities: {len(RPV_ENTITIES)}")
    print(f"  Restaurants: {sum(1 for e in RPV_ENTITIES if e['entity_type'] == 'restaurant')}")
    print(f"  Businesses:  {sum(1 for e in RPV_ENTITIES if e['entity_type'] == 'business')}")
    print(f"  Schools:     {sum(1 for e in RPV_ENTITIES if e['entity_type'] == 'school')}")
    print(f"Events: {len(RPV_EVENTS)}")
    print(f"  Recurring:   {sum(1 for e in RPV_EVENTS if e['is_recurring'])}")
    print(f"  One-time:    {sum(1 for e in RPV_EVENTS if not e['is_recurring'])}")
    print(f"Voice sections: {len([k for k in RPV_VOICE if k not in ('neighborhood_slug', 'city', 'byline', 'updated')])}")

    # Check for banned words
    banned = ["nestled", "boasts", "vibrant", "prestigious"]
    all_text = str(RPV_ENTITIES) + str(RPV_EVENTS) + str(RPV_VOICE)
    for word in banned:
        if word.lower() in all_text.lower():
            print(f"WARNING: Banned word '{word}' found in output!")
        else:
            print(f"OK: '{word}' not found")
