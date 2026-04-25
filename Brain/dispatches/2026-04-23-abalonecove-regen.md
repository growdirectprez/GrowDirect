---
date: 2026-04-23
type: dispatch
project: abalonecove.org
mode: permissionless
status: ready-to-run
---

# Dispatch — abalonecove.org full regen

Autonomous coding agent, end-to-end. Run from a terminal with filesystem
and git push access to `~/GrowDirect` (read) and `~/abalonecove` (write).

---

```
=== DISPATCH: abalonecove-site-regen ===
Mode:           permissionless, end-to-end, no human gates
Working roots:  ~/GrowDirect (read), ~/abalonecove (read + write + commit + push)
Out of scope:   ~/GrowDirect/Canary, ~/GrowDirect/Cove code, ~/GrowDirect/private,
                ~/GrowDirect/Angel, anything under .venv, node_modules, .git
Deliverable:    abalonecove.org rebuilt and live: full PV Land Corp story,
                era-by-era box scores, position paper with working hypothesis,
                stubbed anonymous contribute form, image gallery regenerated
                from ~/abalonecove/images/, every document link resolved,
                committed, pushed, deployed.

----- STEP 1: Inventory -----
Read the following Brain cards and treat them as the source of truth. Do not
invent facts; every claim in the published site must trace to one of these or
to a file under ~/GrowDirect/Cove/docs/archive/.

  Brain/wiki/abalonecove-org.md
  Brain/wiki/cove-community-history.md
  Brain/wiki/cove-pv-declaration-scheme.md
  Brain/wiki/cove-legal-framework.md
  Brain/wiki/cove-declaration-100.md
  Brain/wiki/cove-declaration-100-scope-open.md
  Brain/wiki/coac-declaration-100-article-ii-section-5.md
  Brain/wiki/cove-art-jury-vs-wpbca-arc.md
  Brain/wiki/cove-baughey-1947.md
  Brain/wiki/cove-1976-pvp-development-pressure.md
  Brain/wiki/cove-rpv-redevelopment-conveyance.md
  Brain/wiki/cove-rpv-planning-framework-2026.md
  Brain/wiki/cove-rpv-safety-element-2018.md
  Brain/wiki/cove-zone2-geotech-2011.md
  Brain/wiki/cove-property-geology.md
  Brain/wiki/cove-endangered-species-constraints.md
  Brain/wiki/cove-coastal-specific-plan-s4.md
  Brain/wiki/cove-lrpmp.md
  Brain/wiki/cove-lrpmp-shoreline-park-parcel.md
  Brain/wiki/cove-case-law-lessons.md
  Brain/wiki/claim-lot-h-scope-correction.md
  Brain/wiki/coac-negative-space-lot-h-boundary.md
  Brain/wiki/cove-0-clipper.md
  Brain/wiki/cove-colyear-2024.md
  Brain/wiki/coac-rm-22-incompatibility.md
  Brain/wiki/coac-rpv-housing-elements.md
  Brain/wiki/coac-yimby-opposition-landscape.md
  Brain/wiki/coac-aclad-partnership.md
  Brain/wiki/foundation-founders-narrative.md
  Brain/wiki/wpbca-ocean-path-easement.md

Then scan ~/GrowDirect/Brain/raw/inbox/position-paper/ for any recently dropped
report. If present, intake it via content-engine (engine.py extract + ingest),
write a new Brain card, and add it to the source list above.

If ~/GrowDirect/Cove/docs/archive/property/ does not contain a transcription
of Book 6059 p.178 (PV Coast Road 50-ft ROW), add a CPRA-request template
for it to ~/GrowDirect/Cove/docs/archive/originals/templates/ and flag in
the dispatch report. Do the same for an LA County Sanitation District
inquiry on the 24" line maintenance status. These are public records the
Foundation should have on file.

----- STEP 2: Site structure -----
Rebuild ~/abalonecove/ to the following IA. Preserve existing /evidence/,
/map/, /timeline/, /sign/, /about/, /gallery/, /vendor/, images/ as starting
assets; replace /index.html and add new sections.

  /                           landing: 3-paragraph pitch, 10 story cards,
                              consolidated box score, link to position paper,
                              link to /contribute/
  /the-story/                 braided history, one page per era:
    1-the-land/               Tongva ~5100 BCE, Rancho 1846, Bixby 1882
    2-vanderlip/              1913 peninsula purchase, Jekyll Island context,
                              Japanese American farming 1906-1942
    3-pv-corp/                1925 PV Corp Delaware, Olmsted Brothers master
                              plan, Red Tile District, Art Jury, PVCA
    4-the-covenants/          Declaration 1 (1949), 1-A, Lot H (1950),
                              Declarations 100 / 101, Filiorum grant deed,
                              2009 restated, Lot H scope correction
    5-cityhoods/              PVE 1939, Rolling Hills, RPV 1973, Coastal Plan
                              1978, Monks v. RPV 2008, permanent moratorium 2025
    6-portuguese-bend-slides/ 1956 slide start, 1967 clay mineralogy,
                              1979 Stone & Associates, 2011 Zone 2 EIR,
                              ACLAD, 22 dewatering wells, 2.14"/wk (Mar 2026),
                              FEMA buyout
    7-shore-club-fight/       1972 Karshner proposal, Karl Rodi, board vote,
                              park outcome
    8-sister-plots/           Parcel 106 strip, Lot H boundary, APN 7573-007-900
                              LRPMP, 24-inch pipe corridor, Filiorum east parcels
    9-the-development-tries/  every attempted build on the cove, chronological:
                              Baughey 1947, 1976 PVP pressure, 1980 Wong Tract
                              32977, 1986 reversion, 2014 redevelopment
                              conveyance, 2024 Colyear, 2024 rezoning ordinances
                              678U/680U/681, SB9 Feb 2025, SB330 Dec 2024,
                              24TRCP00352 litigation, 0 Clipper drainage corridor
    10-the-conclusion/        plain-language narration of the orphaned-sewer
                              working hypothesis, what it means, what we need
                              the city to do, how to contribute
  /position/                  position paper on the 24" drainage corridor
    index.html                HTML version
    position-paper.pdf        PDF via Pandoc
    contribute/               submission form (see STEP 5)
  /contribute/                plain-URL redirect to /position/contribute/
  /gallery/                   auto-generated image index (see STEP 4)
  /evidence/                  primary source room, existing — refresh links
  /map/                       existing Leaflet map
  /timeline/                  existing
  /sign/                      existing
  /about/                     refresh to reflect the new site identity

Voice: factual, 1491-esque. Report what happened, cite the record, no
adjectives on contested facts. First-person only in /about/ and the
contribute-policy page — narrative sections are third-person.

----- STEP 2.5: Conclusion + Hypothesis panel -----
The position paper at /position/ concludes with a clearly-labeled
"Working Hypothesis" section — not a "Finding" — stating the orphaned-
sewer thesis in the exact language:

  Hypothesis: the 24-inch line on APNs 7573-006-024 and 7573-007-900 is
  a remnant of the pre-1956 Palos Verdes Coast Road right-of-way
  (Book 6059 p.178), may be disconnected from the modern sanitary sewer
  system, and may be exfiltrating water into the lower Filiorum canyon
  along Parcel 106 boundaries altered in the 1956 reparceling. In a
  landslide zone where groundwater is the controlling factor (2011
  Zone 2 EIR) and residential plumbing is named as the likely 1956
  catalyst, an unmaintained water-bearing line in this location is a
  mechanism-of-action explanation consistent with the onset and
  persistence of slide movement.

Follow the hypothesis with a "What would confirm or refute this" box
listing the five investigative steps verbatim:

  1. Title search on the PV Coast Road 50-foot ROW (Book 6059 p.178) —
     date and manner of abandonment; infrastructure disposition.
  2. 1956 reparceling map overlay — did Parcel 106's boundary move
     across the line?
  3. LA County Sanitation District + RPV Public Works inventory —
     is the line maintained? Last inspection?
  4. Dye trace or CCTV inspection of the line.
  5. ACLAD dewatering well hydrology — signature consistent with an
     anthropogenic water source on the corridor?

Every paragraph in the Hypothesis section that is not directly sourced
to a Brain card or archive file must carry the word "appears," "may,"
"suggests," or "consistent with" — never "is," "does," or "causes."

/the-story/10-the-conclusion/ narrates the same finding in plain
language for the public, links to the position paper, and points to
/contribute/.

----- STEP 3: Box scores -----
At the top of every era page under /the-story/<n>-<slug>/, render a
"Box Score" section — a single HTML table with this schema:

  | Year / Range | Actor | Event / Attempt | Parcel / APN | Outcome | Source |

Every row must link to a Brain wiki card or an archive file. Missing
citation = row drops out. Then below the table, the prose narrative
for the era.

The landing page renders a consolidated "Every Development Attempt at
Abalone Cove" box score pulling from eras 7, 8, 9 only. Append this
final row at the bottom:

  | 2026 | Abalone Cove Foundation | Identified orphaned 24" line
  hypothesis | 7573-006-024 + 7573-007-900 | Under investigation |
  [/position/] |

----- STEP 4: Image gallery sync -----
Scan ~/abalonecove/images/ recursively. For every file
(png/jpg/jpeg/webp/gif/svg):

  1. Extract EXIF + filename metadata, write to
     ~/abalonecove/gallery/manifest.json with fields: path, filename,
     caption (from sibling .txt if present, else cleaned filename),
     date (EXIF DateTimeOriginal or filename-parsed), tags (filename
     tokens + parent-folder token).
  2. Generate ~/abalonecove/gallery/index.html — paginated grid,
     lightbox (use existing vendor/ lightbox lib; if none, add
     photoswipe via CDN or bundle), filter by tag, sort by date.
  3. For every story section, auto-embed images whose tags or dates
     match the section. Use captions as alt text. Link each embedded
     image to its gallery entry.
  4. Generate thumbnails at 400px and 1200px into
     ~/abalonecove/images/.thumbs/. Do not commit full-size originals
     if >2 MB; instead keep thumbnails in the repo and point originals
     at a Cloudflare R2 bucket if one is configured in
     ~/abalonecove/.env (if not configured, commit originals, note in
     log).
  5. If any image appears to be a scan of a document already in
     /evidence/, surface it on the evidence page too.

----- STEP 5: Anonymous contribute form — STUB -----
Build /position/contribute/ as a static stub. Not wired to a live
backend on this run.

Form with four submission types as radio-selectable categories:
  - Eyewitness observation (textarea)
  - Document pointer (URL + description)
  - Media upload (file input, accept=image/*,video/*,application/pdf)
  - Historical knowledge (textarea, long)

Optional one-way contact field (Signal handle or burner email — text
input, label says "optional, only if you want us to follow up").

Form action is a placeholder: data-action="https://contribute.abalonecove.org"
with a stub JS handler that currently:
  - collects form into JSON
  - shows "Submission received — form backend not yet deployed"
  - writes the JSON to window.console for debugging
  - does NOT transmit anywhere

No cookies, no analytics, no third-party scripts on any page under
/contribute/ or /position/contribute/. Leave a <noscript> fallback
that explains the form requires JS and gives a mailto to a placeholder
Foundation email.

Include a /position/contribute/how-it-works/ page with the plain-
language policy block: no IP logs, payload will be encrypted with age
public key (when backend deploys), two-editor review, unverified
submissions not published, rebuttal mechanism, named-editor decryption
only.

Generate an age keypair during the run. Write the PUBLIC key into the
form page as a data attribute (for the future backend to use). Write
the PRIVATE key to ~/abalonecove/.secrets/contribute-private.key with
chmod 600 and ensure .secrets/ is in .gitignore. Never commit the
private key.

Scaffold the Cloudflare Worker at ~/abalonecove/workers/contribute/
with wrangler.toml, index.ts, and a DEPLOY.md that contains the exact
commands to deploy when ready. DO NOT deploy. The form is a stub on
this run.

----- STEP 6: Link integrity -----
Before publish, run a full link check across the whole built site:
  - every <a href> resolves (internal file or reachable external)
  - every <img src> resolves
  - every link to a Brain wiki card has been transformed to a local
    archive link or excerpt on the abalonecove side (the live site
    cannot deep-link into ~/GrowDirect)
  - every /evidence/ link resolves and the target file exists

Any broken link blocks publish to main. Write the link report to
~/abalonecove/build/link-report.txt.

----- STEP 7: Build + publish -----
Build the site in place (static GitHub Pages repo). Then:

  cd ~/abalonecove
  git add -A
  git commit -m "regen: PV Land Corp story + gallery + contribute stub

  - 10-era braided history with box scores
  - position paper on 24-inch drainage corridor
    (APN 7573-006-024 ↔ 7573-007-900)
  - conclusion: working hypothesis that the 24\" line is a remnant
    of the pre-1956 Palos Verdes Coast Road ROW (Book 6059 p.178),
    may be disconnected from the modern sewer, and may be exfiltrating
    into the lower Filiorum canyon along the 1956-reparceled
    Parcel 106 boundary
  - /contribute/ anonymous submission form STUBBED
    (worker scaffolded, not deployed)
  - gallery regenerated from images/ with EXIF + tag index
  - all document links verified"
  git push origin main

If link-check fails, push to branch regen/<timestamp> instead of main
and note in the dispatch report.

Verify the GitHub Pages build succeeds (poll the GitHub API or curl
the deployed URL and confirm it serves the new
/the-story/1-the-land/index.html).

----- STEP 8: Report -----
Write ~/abalonecove/build/dispatch-report.md with:
  - files created / modified / deleted
  - box score row counts per era
  - gallery image count, tagged vs untagged
  - link report summary
  - worker scaffold path + next-step commands
  - any Brain gaps you hit and wrote stub cards for
  - CPRA templates generated (Book 6059 p.178, LASD inquiry)
  - live URL confirmation

Also cat the report at the end so it shows in the terminal.

----- Non-negotiables -----
  - No fabricated facts. No unsourced claims in any published page.
  - No file written outside ~/abalonecove (except Brain stub cards
    under ~/GrowDirect/Brain/wiki/ if a gap is found — tag them
    needs-review).
  - No secrets committed. Ever.
  - If a step fails, write the failure to dispatch-report.md and keep
    going on the rest. Do not roll back. Do not stop on first error.
  - If the site cannot pass link-check, commit + push the built state
    to a branch named regen/<timestamp> instead of main and note this
    in the report.
  - The orphaned-sewer conclusion is a hypothesis, not a finding.
    Never publish it as an asserted fact. Always paired with the five
    investigative steps. This rule is absolute.
  - The contribute form is a stub. No live backend. No submissions
    leave the user's browser on this run.

Begin.
=== END DISPATCH ===
```
