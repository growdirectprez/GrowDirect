# DISPATCH: GRO-493 — Lot 106 Full Boundary Layer Build

**Created:** 2026-04-11 (Cowork session — Phase 0 + Phase 1 complete)
**Linear:** [GRO-493](https://linear.app/growdirect/issue/GRO-493/lot-106-full-boundary-layer-build-metes-and-bounds-to-geojson)
**Playbook:** `Cove/docs/archive/wiki/PLAYBOOK-DEED-TO-LAYER.md`
**Branch:** `gclyle/gro-493-lot-106-full-boundary-layer-build-metes-and-bounds-to`

---

## What's Done (Cowork)

Phase 0 (intake/validation) and Phase 1 (transcription) are complete for three transactions.
All human gates cleared — operator verified names, dates, recording references, and LACA numbers.

### Corrected Misreads

These were wrong in the archive and are now fixed in the inventory file:

| Old | Corrected | File affected |
|-----|-----------|---------------|
| Kenneth E. **Word** | Kenneth R. **Wong** | Inventory + all CQD references |
| Patricia **Niblock** | Patricia Mitchell **Brown**, Trustee for the Brown Family Trust | Inventory + grant deed refs |
| LACA **55 / 41 / 31** | LACA **51** (all the same lot, different assessor map editions) | Inventory + legal desc filenames |
| DOT date **1987** | **1980** (same-day as Garrett→Coates grant deed) | Inventory |
| Garrett trust **#99602 / #99603** | **P9602 / P9603** (leading P, not 9) | Inventory + transcription |
| Oreneth QCD date **1993** | **1980** | Inventory |

### Transcriptions Created

| File | Transaction | Layer work? |
|------|------------|-------------|
| `transcriptions/1981-coates-to-brown-family-trust-grant-deed-inst-81-683006.md` | Coates → Brown Family Trust (sub-parcel) | **YES — fully walkable now** |
| `transcriptions/1980-garrett-corp-trust-to-coates-corp-grant-deed.md` | Garrett Corp Trust → F.L. Coates | No (uses same legal desc as Wing Mar CQD) |
| `transcriptions/1979-wing-mar-to-wong-corp-quitclaim-deeds.md` | Wing Mar → Kenneth R. Wong (3 instruments) | Yes — contains full Lot 106 boundary |

### Key Discovery: Two Different Legal Descriptions

The inbox images contain two distinct parcels, not copies of one:

**Description A — Full Lot 106 boundary** (instruments 79-196958 and 90-180342)
- POB: NW corner Lot 74, Tract 14649
- 16+ legs tracing full perimeter
- Quality: DEGRADED — many calls still illegible, needs certified copies
- This is the GRO-493 target

**Description B — Coates→Brown sub-parcel** (instrument 81-683006)
- POB: Point along PVD South curve (R=1046.45, from Tract 14649 map)
- 4 legs, small triangle between PVD South and county parcel (Book 49767 Pg 44)
- Quality: **VERIFIED — all values legible, fully walkable**
- Quick-win layer build

### Upgraded Confidence Values (Playbook Appendix)

Side-by-side comparison of inbox images resolved 4 calls from MEDIUM to HIGH:

| Leg | Value | Old | New |
|-----|-------|-----|-----|
| 02 | R=965 ft, arc=75.71 ft | MEDIUM | **HIGH** |
| 03 | R=25 ft, arc=40.86 ft | MEDIUM | **HIGH** |
| 06 | S 8°09'45" W 41.18 ft | MEDIUM | **HIGH** |
| 09 | S 85°41'13" E 44.01 ft | MEDIUM | **HIGH** |

---

## What Needs Doing (Claude Code)

### Task 1: Rename Misnamed Archive Files

These files in `Cove/docs/archive/originals/property/county-recorder-deeds/` need renaming:

```bash
# Wrong grantee (Word → Wong)
mv corp-quitclaim-deed-wing-mar-to-word-a.jpeg    1980-01-corp-quitclaim-deed-wing-mar-to-wong-correction.jpeg
mv 1979-02-16-corp-quitclaim-deed-wing-mar-to-word-b.jpeg  1979-02-16-corp-quitclaim-deed-wing-mar-to-wong-b.jpeg
mv 1978-12-corp-quitclaim-deed-wing-mar-to-word-c.jpeg     1978-12-19-corp-quitclaim-deed-wing-mar-to-wong-c.jpeg
mv 1979-02-16-corp-quitclaim-deed-wing-mar-to-word-d.jpeg  1979-02-16-corp-quitclaim-deed-wing-mar-to-wong-d.jpeg

# Wrong grantee (Niblock → Brown)
mv 1981-07-09-grant-deed-coates-to-niblock-cover.jpeg  1981-07-09-grant-deed-coates-to-brown-family-trust.jpeg

# Wrong date (1987 → 1980)
mv 1987-12-15-deed-of-trust-coates-first-american-title.jpeg  1980-12-15-deed-of-trust-coates-first-american-title.jpeg

# Wrong LACA numbers
mv legal-desc-lot106-laca55-doc-900096.jpeg         legal-desc-lot106-laca51-doc-900096.jpeg
mv attachment-a-lot106-laca-map41-doc-90-100542.jpeg attachment-a-lot106-laca51-inst-90-180342.jpeg
mv legal-desc-lot106-laca-map31-doc-096962.jpeg      legal-desc-lot106-laca51-doc-096962.jpeg

# Wrong grantor attribution
mv 1981-07-09-quitclaim-deed-coates.jpeg  1981-07-09-quitclaim-deed-oreneth-coates-to-fl-coates.jpeg

# Missing date/grantee
mv corp-grant-deed-garrett-corp-trust.jpeg  1980-12-15-corp-grant-deed-garrett-corp-to-coates.jpeg
```

### Task 2: Quick-Win Layer Build — Coates→Brown Sub-Parcel

This sub-parcel is fully walkable NOW. All values HIGH confidence. No certified copies needed.

**Source:** `transcriptions/1981-coates-to-brown-family-trust-grant-deed-inst-81-683006.md`

**Calls to walk:**

```
COMMENCEMENT: Easterly terminus of PVD South curve (R=1046.45, arc=194.85)
              Radial at commencement: N 13°34'05" E
TPB: 125.00 ft westerly along curve from commencement

LEG 1: curve  R=1046.45  arc=69.85 ft  (westerly along PVD South)
       → NE corner of county parcel (Book 49767, Pg 44)
LEG 2: S 8°09'45" W  95.92 ft  (along E line of county parcel)
LEG 3: direct line SE to point S 30°33'18" W 95.49 ft from TPB
LEG 4: N 30°33'18" E  95.49 ft  → back to TPB
```

**Anchoring:** The commencement point is defined by reference to a specific curve in Tract 14649 (MB 345, pp. 23-26) along the southerly line of PVD South. Anchor against `wpbca-parcels.geojson` Lot 74 NW corner and PVD South curve geometry.

**Phase 2 (ingest):**
- Create SurveyDocument (grant_deed, Coates → Brown, 81-683006, Jul 9 1981)
- Create SurveyDescription (metes_and_bounds, 4 calls + commencement)
- Create SurveyReference records for each call

**Phase 3 (walk):**
- Walk in local coordinates — this is a simple 4-leg polygon
- Compute closure error (should be near zero — it's a closed description)
- Georeference using PVD South curve from Tract 14649 as tie

**Phase 4 (hierarchy):**
- Create LandDivision node: "Coates / Brown Family Trust parcel"
- Parent: Lot 106 (LACA 51) node
- Type: `deed_carveout`
- Link SurveyDocument via SurveyDocumentDivision

**Phase 5 (output):**
- Write `cove/map/data/layers/lot-106-coates-brown-subparcel.geojson`
- Visual verify against PVD South centerline and existing Lot 106 layers

### Task 3: Full Lot 106 Boundary — Partial Walk (GRO-493 Main Target)

Seven legs are now HIGH confidence (legs 01, 02, 03, 04 bearing, 06, 09, 16). Walk those and leave gaps for the legs that still need certified copies.

**Still blocked on certified copies:**

| Document | Reference | Legs affected |
|----------|-----------|---------------|
| County deed | Book 49767, Page 44 | 04-05 distances, 07-08 |
| P.S.L. Land Corp deed | Book 32541, Page 25 | 08, 10 |
| Hugh Brown deed | Book 74063, Page 10 | 11-12 |

### Task 4: Chain of Title Gap

Kenneth R. Wong → Garrett Corporation Trust — no connecting instrument in archive.
Not blocking the layer build, but needs a grantor index search at the Recorder.

---

## Corrected Chain of Title

```
Wing Mar (Calif.), Inc.
  ↓ Corp QCD (Dec 19, 1978 / recorded Feb 16, 1979, inst. 79-196958)
  ↓ Corp QCD correction (~Jan 1980, corrects inst. 79-191962)
Kenneth R. Wong, a married man
  ↓ [GAP — instrument not in archive]
Garrett Corporation Trust (Chase Manhattan Bank, N.A., Trustee, P9602 / P9603)
  ↓ Corp Grant Deed (Dec 15, 1980) — tax $150.12
F.L. Coates, a married man, sole and separate property
  ← DOT (Dec 15, 1980) — First American Title / Chase Manhattan (purchase financing)
  ← Interspousal QCD (Dec 15, 1980, recorded Jul 9, 1981) — Oreneth M. Coates
  ↓ Grant Deed (Jul 9, 1981, inst. 81-683006) — tax $82.50 — SUB-PARCEL ONLY
Patricia Mitchell Brown, Trustee for the Brown Family Trust
  (2803 Via de la Guerra, PVE 90274)
```

---

## Files to Read First

1. This dispatch
2. `Cove/docs/archive/wiki/PLAYBOOK-DEED-TO-LAYER.md` (full pipeline + appendices A and B)
3. `Cove/docs/archive/transcriptions/1981-coates-to-brown-family-trust-grant-deed-inst-81-683006.md` (quick-win transcription)
4. `Cove/docs/archive/property/2026-04-02-county-recorder-deeds-lot106-laca.md` (corrected inventory)
