"""
Miraleste — Content Hub Data
Neighborhood: Miraleste, Rancho Palos Verdes, CA
Crawl date: 2026-04-10
Sources: Redfin, NeighborhoodScout, GreatSchools, Niche, Yelp, TripAdvisor,
         RPV Calendar, PVPLC, shopgoldencove.com, PV Pulse, PV Source,
         rubyhome.com, AllTrails, Terranea Resort, SeeCalifornia.com
"""

# ===========================================================================
# 1. ENTITIES — restaurants, businesses, schools
# ===========================================================================

ENTITIES = [
    # --- Schools ---
    {
        "name": "Miraleste Intermediate School",
        "entity_type": "school",
        "address": "29323 Palos Verdes Dr E, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "public middle school",
        "description": (
            "Grades 6-8 in the PVPUSD system. Home of the Marauders. "
            "746 students, 21:1 student-teacher ratio. 72% proficient in reading, "
            "67% in math. Gifted & Talented program and Project Lead The Way STEM "
            "curriculum. Consistently ranks in the top 10% of California middle schools."
        ),
        "website": "https://mis.pvpusd.net/",
        "tags": ["PVPUSD", "middle school", "STEM", "PLTW", "gifted"],
    },
    {
        "name": "Ridgecrest Intermediate School",
        "entity_type": "school",
        "address": "28915 Northbay Rd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "public middle school",
        "description": (
            "Grades 6-8 in PVPUSD. 917 students, 26:1 student-teacher ratio. "
            "83% proficient in reading, 77% in math. One of the top-rated public "
            "middle schools in California."
        ),
        "website": "https://ris.pvpusd.net/",
        "tags": ["PVPUSD", "middle school", "top-rated"],
    },
    {
        "name": "Mira Catalina Elementary School",
        "entity_type": "school",
        "address": "30511 Lucania Dr, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "public elementary school",
        "description": (
            "K-5 elementary in the PVPUSD system. Feeds into Miraleste Intermediate. "
            "Located in the eastern portion of the peninsula serving the Miraleste area."
        ),
        "website": "https://mc.pvpusd.net/",
        "tags": ["PVPUSD", "elementary", "K-5"],
    },
    {
        "name": "Palos Verdes High School",
        "entity_type": "school",
        "address": "600 Cloyden Rd, Palos Verdes Estates, CA 90274",
        "neighborhood": "palos_verdes_estates",
        "city": "Palos Verdes Estates",
        "category": "public high school",
        "description": (
            "Grades 9-12, PVPUSD. 10/10 GreatSchools, A+ Niche. 97% graduation rate, "
            "average SAT 1330. Feeds from Miraleste Intermediate. One of the feeder "
            "high schools for Miraleste-area families."
        ),
        "website": "https://pvhs.pvpusd.net/",
        "tags": ["PVPUSD", "high school", "top-rated", "feeder"],
    },
    {
        "name": "Peninsula High School",
        "entity_type": "school",
        "address": "27118 Silver Spur Rd, Rolling Hills Estates, CA 90274",
        "neighborhood": "rolling_hills_estates",
        "city": "Rolling Hills Estates",
        "category": "public high school",
        "description": (
            "Grades 9-12, PVPUSD. Alternative feeder high school for some Miraleste-area "
            "students depending on attendance boundaries. Strong academics and athletics."
        ),
        "website": "https://penhs.pvpusd.net/",
        "tags": ["PVPUSD", "high school", "feeder"],
    },

    # --- Miraleste Plaza Businesses ---
    {
        "name": "Miraleste Liquor & Deli",
        "entity_type": "restaurant",
        "address": "29 Miraleste Plz, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "deli / market",
        "description": (
            "Longtime neighborhood deli and liquor store at Miraleste Plaza. "
            "Sandwiches, coffee, market goods. An icon on the east side of the Hill. "
            "Mon-Fri 7:30am-8pm."
        ),
        "website": None,
        "tags": ["deli", "sandwiches", "market", "takeout", "miraleste plaza"],
    },
    {
        "name": "Miraleste Hairstylists",
        "entity_type": "business",
        "address": "29A Miraleste Plz, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "hair salon",
        "description": (
            "Family hair and nail salon established in 1993. Haircuts, coloring, "
            "styling, gel nails. A Miraleste Plaza fixture for over 30 years."
        ),
        "website": None,
        "tags": ["salon", "haircut", "nails", "miraleste plaza"],
    },
    {
        "name": "Miraleste Automotive",
        "entity_type": "business",
        "address": "Miraleste Plz, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "auto repair",
        "description": (
            "Local auto repair shop serving Miraleste and east RPV. "
            "Full-service maintenance and repair."
        ),
        "website": "https://ranchopalosverdesautorepair.org/",
        "tags": ["auto repair", "mechanic", "miraleste plaza"],
    },
    {
        "name": "Miraleste Recreation and Parks District",
        "entity_type": "business",
        "address": "19 Miraleste Plz, Rancho Palos Verdes, CA 90275",
        "neighborhood": "miraleste",
        "city": "Rancho Palos Verdes",
        "category": "parks & recreation",
        "description": (
            "Independent special district formed in 1940 when the Palos Verdes Homes "
            "Association deeded 60 acres for parks and recreation. Manages Frog Pond Park, "
            "Harter Park, Miltenberger Park, Canada Park, and the Miraleste trail system. "
            "Trail maps available at the office."
        ),
        "website": None,
        "tags": ["parks", "recreation", "trails", "community"],
    },

    # --- Golden Cove Shopping Center (nearby, ~10 min west) ---
    {
        "name": "Trader Joe's (Golden Cove)",
        "entity_type": "business",
        "address": "31176 Hawthorne Blvd, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "grocery",
        "description": (
            "Anchor tenant of Golden Cove Shopping Center. Full Trader Joe's "
            "grocery with the usual curated selection. The closest major grocery "
            "store for Miraleste residents heading west on the Hill."
        ),
        "website": "https://www.traderjoes.com/",
        "tags": ["grocery", "golden cove", "anchor"],
    },
    {
        "name": "Avenue Italy",
        "entity_type": "restaurant",
        "address": "31230 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "italian",
        "description": (
            "Lively Italian restaurant at Golden Cove Center. Family-friendly, "
            "excellent pasta, outdoor seating. A solid weeknight option for "
            "Miraleste families willing to cross the Hill."
        ),
        "website": None,
        "tags": ["italian", "pasta", "family-friendly", "golden cove"],
    },
    {
        "name": "Swan Thai RPV",
        "entity_type": "restaurant",
        "address": "31224 Palos Verdes Dr W, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "thai",
        "description": (
            "Refined authentic Thai cuisine at Golden Cove. Sophisticated setting, "
            "friendly service. Well-regarded on the peninsula."
        ),
        "website": None,
        "tags": ["thai", "golden cove", "date night"],
    },
    {
        "name": "Yellow Vase (Golden Cove)",
        "entity_type": "restaurant",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "french-california cafe",
        "description": (
            "French-California cafe, florist, and bakery. Brioche French toast, "
            "crepes, pastries. The RPV location of the PVE original. "
            "Where I take every new client."
        ),
        "website": None,
        "tags": ["brunch", "french", "bakery", "florist", "golden cove"],
    },
    {
        "name": "Poke Me",
        "entity_type": "restaurant",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "poke / hawaiian",
        "description": "Build-your-own poke bowls at Golden Cove. Quick, fresh, casual.",
        "website": None,
        "tags": ["poke", "hawaiian", "quick service", "golden cove"],
    },
    {
        "name": "Tomatillo Mexican Grill",
        "entity_type": "restaurant",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "mexican",
        "description": "Casual Mexican grill at Golden Cove Shopping Center.",
        "website": None,
        "tags": ["mexican", "casual", "golden cove"],
    },
    {
        "name": "Golden Scoop Gelato",
        "entity_type": "restaurant",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "gelato / dessert",
        "description": "Artisan gelato at Golden Cove. Family treat spot.",
        "website": None,
        "tags": ["gelato", "dessert", "family", "golden cove"],
    },
    {
        "name": "Starbucks (Golden Cove)",
        "entity_type": "business",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "coffee",
        "description": "Starbucks location at Golden Cove Shopping Center.",
        "website": "https://www.starbucks.com/",
        "tags": ["coffee", "golden cove"],
    },
    {
        "name": "Great American International Seafood Market",
        "entity_type": "business",
        "address": "Golden Cove Center, Rancho Palos Verdes, CA 90275",
        "neighborhood": "golden_cove",
        "city": "Rancho Palos Verdes",
        "category": "seafood market",
        "description": (
            "Specialty seafood market at Golden Cove. Fresh fish, prepared items. "
            "A real find for home cooks on the peninsula."
        ),
        "website": None,
        "tags": ["seafood", "market", "specialty", "golden cove"],
    },

    # --- Terranea Resort (nearby, ~10 min) ---
    {
        "name": "Nelson's at Terranea",
        "entity_type": "restaurant",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "terranea",
        "city": "Rancho Palos Verdes",
        "category": "coastal american",
        "description": (
            "Cliff-top casual dining at Terranea Resort. Fire pits, sunset views, "
            "Baja fish tacos, ahi tuna burger. Chef Juan Nunez. "
            "Mon-Thu 11am-8pm, Fri 11am-9pm, Sat 9am-9pm, Sun 9am-8pm. "
            "This is where I take clients when I want them to fall in love with the area."
        ),
        "website": "https://www.terranea.com/dining/nelsons",
        "tags": ["terranea", "sunset", "casual", "ocean view", "fire pits"],
    },
    {
        "name": "mar'sel at Terranea",
        "entity_type": "restaurant",
        "address": "100 Terranea Way, Rancho Palos Verdes, CA 90275",
        "neighborhood": "terranea",
        "city": "Rancho Palos Verdes",
        "category": "fine dining",
        "description": (
            "Forbes Four-Star fine dining at Terranea Resort. Chef Fabio Ugoletti's "
            "seasonally rotating tasting menus with locally sourced ingredients. "
            "Pacific Ocean views. Sunday brunch is worth the drive from anywhere in "
            "the South Bay."
        ),
        "website": "https://www.terranea.com/dining/marsel",
        "tags": ["terranea", "fine dining", "tasting menu", "ocean view", "forbes"],
    },

    # --- San Pedro Nearby Landmarks ---
    {
        "name": "Korean Bell of Friendship",
        "entity_type": "business",
        "address": "3601 S Gaffey St, San Pedro, CA 90731",
        "neighborhood": "san_pedro",
        "city": "Los Angeles",
        "category": "landmark / park",
        "description": (
            "A 17-ton bronze bell gifted by South Korea for the 1976 bicentennial, "
            "housed in a pagoda-style pavilion at Angels Gate Park. Overlooks Los Angeles "
            "Harbor and Catalina Channel. Rung on July 4th, Korean Liberation Day (Aug 15), "
            "Korean-American Day (Jan 13), and New Year's Eve. "
            "Five minutes from Miraleste's eastern border."
        ),
        "website": "https://koreanfriendshipbellpreservationfoundation.org/",
        "tags": ["landmark", "san pedro", "park", "views", "harbor"],
    },
    {
        "name": "Point Fermin Park & Lighthouse",
        "entity_type": "business",
        "address": "807 W Paseo Del Mar, San Pedro, CA 90731",
        "neighborhood": "san_pedro",
        "city": "Los Angeles",
        "category": "park / historic site",
        "description": (
            "37-acre bluff-top park with the 19th-century Point Fermin Lighthouse "
            "at its center. Big green lawns, ocean views, whale watching in winter. "
            "Free entry. A short drive downhill from Miraleste."
        ),
        "website": None,
        "tags": ["park", "lighthouse", "san pedro", "ocean view", "historic"],
    },
    {
        "name": "White Point Nature Preserve",
        "entity_type": "business",
        "address": "1600 W Paseo Del Mar, San Pedro, CA 90731",
        "neighborhood": "san_pedro",
        "city": "Los Angeles",
        "category": "nature preserve",
        "description": (
            "102 acres of restored coastal sage scrub habitat with hiking trails "
            "and ocean views. Managed by PVPLC. Regular volunteer days, nature walks, "
            "and family programs. One of the closest nature experiences to Miraleste."
        ),
        "website": "https://pvplc.org/",
        "tags": ["nature", "hiking", "san pedro", "PVPLC", "coastal sage"],
    },
]


# ===========================================================================
# 2. EVENTS — recurring and upcoming
# ===========================================================================

EVENTS = [
    {
        "title": "41st Annual Whale of a Day Festival",
        "event_date": "2026-04-11",
        "event_time": "10:00 AM - 4:00 PM",
        "location_name": "Point Vicente Interpretive Center",
        "neighborhood": "rancho_palos_verdes",
        "category": "festival",
        "description": (
            "Gray whale migration celebration with food trucks, kids activities, "
            "beer and wine garden, silent auction, and tours inside the Point Vicente "
            "Lighthouse (celebrating its 100th anniversary in 2026). Free admission. "
            "Free parking and shuttle from Ken Dyda Civic Center."
        ),
        "is_recurring": True,
        "recurrence": "annually, typically April",
    },
    {
        "title": "PV Farmers Market",
        "event_date": None,
        "event_time": "8:00 AM - 1:00 PM",
        "location_name": "Peninsula High School (Hawthorne & Silver Spur)",
        "neighborhood": "rolling_hills_estates",
        "category": "farmers market",
        "description": (
            "Year-round Sunday farmers market. Produce, artisan goods, prepared food. "
            "The social hub for the Hill — get there before 9am for the best selection."
        ),
        "is_recurring": True,
        "recurrence": "every Sunday, year-round",
    },
    {
        "title": "PVPLC Earth Day at White Point",
        "event_date": "2026-04-18",
        "event_time": "9:00 AM - 12:00 PM",
        "location_name": "White Point Nature Preserve",
        "neighborhood": "san_pedro",
        "category": "volunteer / nature",
        "description": (
            "Annual Earth Day event hosted by PV Peninsula Land Conservancy. "
            "Planting, weeding, kids activities, and raffle prizes. Family-friendly."
        ),
        "is_recurring": True,
        "recurrence": "annually, April (Earth Day weekend)",
    },
    {
        "title": "Trolls: A Field Study Exhibition",
        "event_date": None,
        "event_time": "Garden hours",
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rolling_hills_estates",
        "category": "arts / culture",
        "description": (
            "Large-scale troll sculptures scattered throughout the garden. "
            "Running through October 4, 2026. Popular with families."
        ),
        "is_recurring": False,
        "recurrence": None,
    },
    {
        "title": "SOAR: Tropical Butterflies",
        "event_date": "2026-05-01",
        "event_time": "Garden hours",
        "location_name": "South Coast Botanic Garden",
        "neighborhood": "rolling_hills_estates",
        "category": "arts / nature",
        "description": (
            "Sixth year of the immersive butterfly experience. Opens May 2026. "
            "Sells out — book early."
        ),
        "is_recurring": True,
        "recurrence": "annually, May through summer",
    },
    {
        "title": "Korean Bell Ringing — Independence Day",
        "event_date": "2026-07-04",
        "event_time": "Morning",
        "location_name": "Korean Bell of Friendship, Angels Gate Park",
        "neighborhood": "san_pedro",
        "category": "cultural / civic",
        "description": (
            "Annual ringing of the Korean Friendship Bell at Angels Gate Park "
            "for Independence Day. One of four annual bell ringings."
        ),
        "is_recurring": True,
        "recurrence": "annually, July 4th",
    },
    {
        "title": "PVPLC Guided Nature Walks",
        "event_date": None,
        "event_time": "Varies, typically 9:00 AM",
        "location_name": "Various preserves (White Point, George F Canyon, Linden Chandler)",
        "neighborhood": "rancho_palos_verdes",
        "category": "nature / outdoor",
        "description": (
            "Weekly guided walks through PVPLC preserves. Birdlife walks, "
            "canyon discovery, native plant tours. Free or minimal cost. "
            "Best way to explore the preserves if you are new to the area."
        ),
        "is_recurring": True,
        "recurrence": "weekly, year-round (schedule varies by season)",
    },
    {
        "title": "Miraleste Trails Hiking",
        "event_date": None,
        "event_time": "Daylight hours",
        "location_name": "Miraleste Trail System",
        "neighborhood": "miraleste",
        "category": "outdoor / recreation",
        "description": (
            "5.5-mile moderate trail network through wooded canyons. 800-foot elevation "
            "gain, about 2.5 hours. Includes Colinita Trail, Frascati Trail, Siena Loop, "
            "La Canada trails. Mostly shaded. A hidden gem with a bridge at the canyon floor."
        ),
        "is_recurring": True,
        "recurrence": "daily, self-guided (Sierra Club leads group hikes periodically)",
    },
    {
        "title": "Coffee with the Mayor",
        "event_date": "2026-04-22",
        "event_time": "10:00 AM - 11:00 AM",
        "location_name": "Ladera Linda Park",
        "neighborhood": "rancho_palos_verdes",
        "category": "civic",
        "description": "Informal meet with the RPV Mayor. Open to all residents.",
        "is_recurring": True,
        "recurrence": "periodic, check RPV calendar",
    },
    {
        "title": "Arts Open San Pedro",
        "event_date": "2026-04-25",
        "event_time": "All day (Fri-Sat)",
        "location_name": "Various studios, San Pedro",
        "neighborhood": "san_pedro",
        "category": "arts / culture",
        "description": (
            "City-wide open studio event in San Pedro. Free. Artists open their "
            "workspaces to the public. A short drive downhill from Miraleste."
        ),
        "is_recurring": True,
        "recurrence": "annually, April",
    },
]


# ===========================================================================
# 3. NEIGHBORHOOD METADATA
# ===========================================================================

NEIGHBORHOOD_META = {
    "slug": "miraleste",
    "display_name": "Miraleste",
    "city": "Rancho Palos Verdes",
    "zip_code": "90275",
    "geography": (
        "Eastern slopes of the Palos Verdes Peninsula. Borders Rolling Hills to the "
        "west, San Pedro to the east, and the harbor/city views open to the north and east."
    ),
    "population": 5273,  # residences per NeighborhoodScout
    "median_home_price": 1_560_000,  # Redfin March 2026
    "median_price_per_sqft": 742,
    "avg_home_sqft": 2013,
    "home_sqft_range": "147 - 10,496",
    "yoy_price_change": "+9.6%",
    "avg_days_on_market": 81,
    "housing_character": (
        "Medium to large single-family homes, some mobile homes. Mix of 1950s-70s "
        "ranch and split-level construction with scattered modern rebuilds. "
        "Generous lots by LA standards, many with harbor, city, or ocean views."
    ),
    "key_roads": ["Palos Verdes Dr E", "Miraleste Dr", "Crest Rd"],
    "nearby_commercial": ["Miraleste Plaza", "Golden Cove Shopping Center", "Western Ave (San Pedro)"],
    "school_district": "PVPUSD",
    "feeder_schools": [
        "Mira Catalina Elementary -> Miraleste Intermediate -> Palos Verdes HS / Peninsula HS"
    ],
}


# ===========================================================================
# 4. VOICE OVERLAY — Angelique's voice, section by section
# ===========================================================================

VOICE_OVERLAY = {
    "intro": (
        "Miraleste is the east side of the Hill, and it has a personality all its own. "
        "Where the western neighborhoods look out over open ocean, Miraleste faces the "
        "harbor, the city lights, and on clear mornings, the San Gabriel Mountains rising "
        "behind downtown. It is quieter over here, a little more tucked away, and the "
        "prices reflect a genuine entry point into Palos Verdes that the west side "
        "stopped offering years ago.\n\n"
        "I work with a lot of families who discover Miraleste after looking at Lunada Bay "
        "or Malaga Cove and realizing the math does not work. They drive over the ridge, "
        "see the harbor views, find a four-bedroom on a real lot for under two million, "
        "and the conversation changes. This is still PVPUSD schools, still the Hill, "
        "still that same sense of living above everything — the vantage point is just "
        "different."
    ),

    "real_estate": (
        "The median sale price in Miraleste hit $1.56 million in early 2026, up almost "
        "10% year over year. The average home runs about 2,000 square feet, but lot sizes "
        "vary wildly — I have seen everything from compact pads near the plaza to half-acre "
        "hillside parcels with 270-degree views. Most of the housing stock dates from the "
        "'50s through the '70s: ranch homes, split-levels, a handful of mid-century moderns. "
        "The teardown-and-rebuild trend is starting to reach Miraleste now, and when someone "
        "puts a modern build on one of those view lots, it sells fast.\n\n"
        "Compared to the west side of the peninsula, your dollar goes further here. "
        "The median in Lunada Bay is $2.38 million, in Malaga Cove it is higher still. "
        "Miraleste gives you the same school district, the same community, and a different "
        "but equally dramatic set of views — harbor lights at night, Catalina on the "
        "horizon, container ships gliding past. Homes sit on the market about 81 days, "
        "which is longer than the west side, so buyers actually have time to think."
    ),

    "local_scene": (
        "Miraleste Plaza is the neighborhood hub — a small strip center with a deli, "
        "a hair salon that has been here since '93, an auto shop, and the parks district "
        "office. It is not Lunada Bay Plaza with its fountain courtyard and boutiques, "
        "and it does not pretend to be. It is functional, familiar, and the kind of place "
        "where the person behind the counter knows your order.\n\n"
        "For a real grocery run or a wider selection of restaurants, most Miraleste "
        "residents head to Golden Cove Shopping Center on the west side — Trader Joe's, "
        "Avenue Italy, Swan Thai, Yellow Vase, a seafood market — or drop down to "
        "Western Avenue in San Pedro for Korean barbecue, Filipino food, and everything "
        "else the port city has to offer. San Pedro is five minutes downhill, and that "
        "proximity is one of Miraleste's underrated advantages: you get the peninsula "
        "schools and the peninsula air, but you are also close to a real working waterfront "
        "with museums, breweries, and some of the best casual dining in the South Bay."
    ),

    "dining": (
        "The closest sit-down dining to Miraleste itself is Miraleste Liquor & Deli at "
        "the plaza — sandwiches, coffee, the essentials. For anything more, you are driving "
        "ten minutes in one direction or another, and the options are excellent.\n\n"
        "Nelson's at Terranea is my go-to for sunset dining — cliff-top, casual, fire pits, "
        "and Baja fish tacos with a view that makes people decide to move here. mar'sel, "
        "also at Terranea, is the serious fine dining option — Chef Ugoletti's seasonal "
        "tasting menus are worth every dollar. Avenue Italy at Golden Cove handles the "
        "family Italian night. Swan Thai at Golden Cove does refined Thai that keeps "
        "regulars coming back weekly.\n\n"
        "And honestly, do not overlook San Pedro. Point Fermin is five minutes away, "
        "and the Cabrillo district has restaurants, craft breweries, and a growing food "
        "scene that benefits from being under the radar."
    ),

    "community": (
        "The outdoor access here is the real story. The Miraleste trail system is a hidden "
        "gem — 5.5 miles of shaded canyon trails managed by the Miraleste Recreation and "
        "Parks District, which has been taking care of these 60 acres since 1940. There is "
        "a bridge at the canyon floor that feels like you are in the mountains, not ten "
        "minutes from the harbor. Frog Pond Park, Harter Park, Canada Park — these are "
        "quiet neighborhood spaces, not marquee destinations, and that is the point.\n\n"
        "Then there is everything downhill in San Pedro: the Korean Bell of Friendship "
        "at Angels Gate Park, with its panoramic harbor views and ceremonial bell ringings "
        "throughout the year. Point Fermin Park and its 19th-century lighthouse. White Point "
        "Nature Preserve — 102 acres of restored coastal sage with trails and ocean views, "
        "and the PVPLC runs regular volunteer days and nature walks there.\n\n"
        "The Whale of a Day festival happens every April at Point Vicente — the 41st year "
        "was in 2026, with lighthouse tours, food trucks, and a wine garden. The PV Farmers "
        "Market runs every Sunday at Peninsula High School, year-round. And the South Coast "
        "Botanic Garden, a short drive west, keeps a rotating calendar of exhibitions and "
        "family events — the Trolls sculpture exhibit ran through October 2026, and the "
        "annual butterfly experience sells out every summer."
    ),

    "further_reading": (
        "- [Miraleste Housing Market on Redfin](https://www.redfin.com/neighborhood/14717/CA/Rancho-Palos-Verdes/Miraleste/housing-market) — Current pricing and sales trends\n"
        "- [Miraleste Intermediate School on GreatSchools](https://www.greatschools.org/california/rancho-palos-verdes/2846-Miraleste-Intermediate-School/) — Ratings, test scores, parent reviews\n"
        "- [Golden Cove Shopping Center](https://www.shopgoldencove.com/shops--restaurants.html) — Full directory of shops and restaurants\n"
        "- [PVPLC Events Calendar](https://pvplc.org/events) — Guided hikes, volunteer days, nature programs\n"
        "- [RPV City Calendar](https://www.rpvca.gov/Calendar.aspx) — City events and community meetings\n"
        "- [Miraleste Trails Guide](https://gunysguide.com/trails) — Trail maps and route descriptions\n"
        "- [South Coast Botanic Garden](https://southcoastbotanicgarden.org/events) — Exhibitions and family programs\n"
        "- [PVPUSD School Finder](http://schools.pvpusd.net/) — Verify your school boundaries\n"
        "- [Korean Bell of Friendship](https://koreanfriendshipbellpreservationfoundation.org/) — History and bell ringing schedule"
    ),

    "closing": (
        "Miraleste is not the first neighborhood people think of when they say Palos Verdes, "
        "and that is actually its advantage. The views face a different direction — harbor "
        "lights instead of open ocean — the prices are lower, the lots are often bigger, "
        "and you are closer to San Pedro's waterfront than any other neighborhood on the Hill. "
        "I have watched families move here planning to trade up to the west side in a few "
        "years, and they never leave. The canyon trails, the quiet streets, the schools, the "
        "fact that you can watch the harbor light up at sunset from your living room — it "
        "adds up.\n\n"
        "If you are considering Miraleste, call me. I can show you the lots with the views "
        "the internet does not capture and the streets where the next wave of rebuilds "
        "is happening."
    ),
}


# ===========================================================================
# 5. CONTENT SOURCES — for attribution footer
# ===========================================================================

CONTENT_SOURCES = [
    "Redfin", "NeighborhoodScout", "GreatSchools", "Niche", "U.S. News Education",
    "Yelp", "TripAdvisor", "RPV City Calendar", "PVPLC", "shopgoldencove.com",
    "PV Pulse", "PV Source", "rubyhome.com", "AllTrails", "Terranea Resort",
    "SeeCalifornia.com", "Korean Friendship Bell Foundation", "Miraleste Rec & Parks",
    "PVPUSD", "Gunys Guide Trails",
]
