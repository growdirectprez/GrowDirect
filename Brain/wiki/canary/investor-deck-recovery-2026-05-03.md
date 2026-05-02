---
title: Investor Deck Recovery — Original Multi-Vertical Thesis Language
type: recovery-summary
domain: canary
status: draft
date: 2026-05-03
last-compiled: 2026-05-03
needs-review: true
session: substrate-captures-2026-05-03
unit-of-analysis: Pre-retail GrowDirect investor decks; identification of original identity-layer / multi-vertical language for harvest into next pitch material
tags: [investor, deck, recovery, identity-layer, multi-vertical, harvest, pitch-spine, manifesto]
---

# Investor Deck Recovery — 2026-05-03

> One-page summary of the GrowDirect deck and manifesto material that exists in the repo, what each artifact says about the multi-vertical / identity-layer thesis, and the most-quotable original language. Produced as Task 5 of the substrate captures session.

---

## What was searched

| Search | Scope | Result |
|---|---|---|
| `memory_recall("original GrowDirect investor pitch identity layer all verticals")` | Memory bus, top-5 | Returned PITCH_SPINE v0.4 wiki, growdirect.io portfolio site spec, canary.growdirect.io design spec |
| `memory_recall("health voting consumer spend identity triad pre-retail vertical")` | Memory bus, top-5 | Returned retail vendor cards (false positive on "vendor identity") and the Voyix/Counterpoint engagement context |
| `memory_recall("GrowDirect investor deck identity protocol multi-vertical pitch")` | Memory bus, top-5 | Returned PITCH_SPINE v0.4 (highest similarity), portfolio site spec, agent topology |
| `find … *.pptx, *.pdf, *.key … -path "*investor*"` | Repo + worktrees | No filename match for "investor" — but `docs/_archive/ip-vault/sales/` contains the load-bearing decks |
| `find … *.pptx, *.pdf, *.key …` cross-cutting | `docs/_archive/`, `Brain/raw/`, `Angel/`, `Cove/` | Identified two original GrowDirect / Canary decks plus the Manifesto v1.1 and Pitch Spine v0.4 |
| `grep -rln "(identity layer\|health.*voting\|voting.*spend)" docs/_archive/ip-vault` | IP vault tree | Hit on `Canary_Bitcoin_Architecture_Research_Paper_v1.0.md` and `GrowDirect_Manifesto_v1.1.md` |

## What was found — the canonical artifacts

| Artifact | Path | Date | Role |
|---|---|---|---|
| **GrowDirect Thesis v1.0 deck** | `docs/_archive/ip-vault/sales/GrowDirect_Thesis_v1.0.pptx` | Feb 2026 | The "platform is universal" investor deck. 12 slides. Patent-anchored opening; multi-vertical "Vision" slide is the load-bearing artifact for the identity-layer thesis. |
| **Canary Square Opportunity deck** | `docs/_archive/ip-vault/sales/Canary_Square_Opportunity.pptx` | Feb 2026 | The Square SMB beachhead deck. 17 slides. Goes deep on the retail proof case; closes with conference roadshow + franchise channel strategy. |
| **GrowDirect Manifesto v1.1** | `docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md` | early 2026 | The long-form thesis. §V.9 introduces the **.jeffe namespace as identity layer** — the original architectural articulation of identity-as-substrate. §VII.4 names the Phase 3 multi-vertical expansion explicitly. |
| **Pitch Spine v0.4 (locked)** | `Brain/wiki/growdirect-pitch-spine.md` (sources `docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4.md`) | Feb 27, 2026 | The 8-act narrative arc. Act 4G ("The Vision — The TAM isn't retail. The TAM is everything") is the explicit multi-vertical sell. |
| **Canary Bitcoin Architecture Research Paper v1.0** | `docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md` | early 2026 | Long-form architecture; cross-references identity-layer language. Not the primary recovery target but a useful corroborator. |
| **Warchest source folder** | `docs/_archive/ip-vault/warchest/sources/` | Feb 2026 | 50+ short slide-source markdown files (00-the-demo, 04-the-crdm, 06-the-glog, 13-the-scale, 30-first-mover, etc.) — the raw building blocks of the spine and the Thesis deck. |

The original investor decks **do exist** in the repo. They were not lost; they live in `docs/_archive/ip-vault/`. The recovery answer is *yes, the language is recoverable, and here it is.*

## What the original thesis says about the identity-layer triad

The current substrate captures session articulated the triad as **health · voting · consumer spend** ([[concept-identity-layer-triad]]). The original thesis didn't use those exact three words — it used a six-vertical TAM list. Mapping the original list onto the triad:

| Original (Thesis deck Slide 11 + Manifesto §VII.4) | Triad leg |
|---|---|
| Retail | Spend |
| Healthcare ("patient records notarization") | Health |
| Supply chain ("audit trail anchoring") | Spend (industrial) |
| Legal ("legal document timestamping") | Voting / governance |
| Insurance | Spend (risk side) |
| Government | Voting / governance |
| Real estate ("closing document timestamping") | Spend + voting (HOA-adjacent) |

Six original verticals → three triad legs. The triad is a sharpening, not a contradiction, of the original multi-vertical TAM. The recovered language proves the multi-vertical claim was structural from day one; the triad makes it architecturally portable.

The architectural articulation of identity-as-substrate is in **Manifesto §V.9 — The .jeffe Namespace**. Quote (single, in quotation marks, capability-language preserved):

> "Names are mutable but human-readable. The namespace bridges them."

That sentence is the protein. The .jeffe namespace was the original identity layer; the triad generalizes the same architectural shape across health, voting, and spend.

## The most-quotable original language (one paragraph for harvest)

The Pitch Spine v0.4 closes Act 4 with the line that does the most work for the multi-vertical investor pitch: *"The TAM isn't retail. The TAM is everything."* The Thesis deck Slide 11 lists the verticals — Retail, Healthcare, Supply Chain, Legal, Insurance, Government — over the line *"Canary LP is the beachhead. The platform is universal."* The Manifesto §V.9 gives the architectural reason: identity is a substrate-layer concern (the .jeffe namespace bridges immutable Ordinal ranges with mutable human-readable names), and once identity is in the substrate, every vertical that needs identity-anchored evidence is a projection of the same protocol. Combine the three: the platform was multi-vertical-by-architecture from the founding documents; retail is the proof case, not the product; the substrate was always meant to scale across health, voting, and consumer spend; the .jeffe namespace was the original identity-layer articulation. **All of this language is reusable — and the capability-language invariant ([[platform-gateway-thesis]] invariant #6) requires that any harvest replace satoshi / Bitcoin / Ordinal / L402 surface with verifiable cost-to-serve, transparent settlement, cryptographic evidence, immutable audit, and hash-chained provenance terminology before it ships externally.**

## Recommendation

The recovery is complete; nothing material is missing from the repo. The next pitch material should:

1. **Open with the Pitch Spine Act 4G line, retranslated to capability language.** *"The TAM isn't retail. The TAM is everything"* survives capability translation cleanly — it makes no Bitcoin-specific claim. Use it.
2. **Re-anchor the multi-vertical slide on the triad, not the six-vertical list.** The triad ([[concept-identity-layer-triad]]) is the architectural through-line; the six verticals are projections of the triad. Sharper pitch.
3. **Bring the .jeffe namespace into the substrate-discipline frame.** Manifesto §V.9 is the architectural origin of identity-as-substrate; reference it in the gateway thesis Layer 2 (open protocol) brand-stack copy.
4. **Lift the Thesis deck Slide 11 vertical icons into the next deck.** The visual language (six vertical icons over a "platform is universal" claim) lands. Replace the icon set's emoji grid with vertical names that ladder onto the triad explicitly.
5. **Founder upload not required.** The decks are present. The Manifesto is present. The Spine is present. The harvest can proceed against what's on disk.

## Open question for the founder

Is there an even earlier deck — pre-Canary, pre-retail-beachhead — that articulated the identity-layer triad in its current health/voting/spend shape, that lives outside the `docs/_archive/ip-vault/` tree (e.g., on iCloud, in an old Notion, in a personal Google Drive)? The recovery found the Bitcoin-anchored multi-vertical thesis but not a pre-Bitcoin, pre-Canary articulation of the triad as such. If one exists, harvest it; if not, the triad is a 2026-05-03 sharpening, and that's a valid origin story.

## Sources

| Source | Path |
|---|---|
| GrowDirect Thesis v1.0 deck | [docs/_archive/ip-vault/sales/GrowDirect_Thesis_v1.0.pptx](../../../docs/_archive/ip-vault/sales/GrowDirect_Thesis_v1.0.pptx) |
| Canary Square Opportunity deck | [docs/_archive/ip-vault/sales/Canary_Square_Opportunity.pptx](../../../docs/_archive/ip-vault/sales/Canary_Square_Opportunity.pptx) |
| GrowDirect Manifesto v1.1 | [docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md](../../../docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md) |
| Pitch Spine v0.4 (locked) | [Brain/wiki/growdirect-pitch-spine.md](../growdirect-pitch-spine.md) |
| Pitch Spine v0.4 (source) | [docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4.md](../../../docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4.md) |
| Canary Bitcoin Architecture Research Paper v1.0 | [docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md](../../../docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md) |
| Warchest sources folder | [docs/_archive/ip-vault/warchest/sources/](../../../docs/_archive/ip-vault/warchest/sources/) |

## Related

- [[Brain/wiki/cards/concept-identity-layer-triad|Identity Layer Triad]] — the 2026-05-03 sharpening of the multi-vertical thesis
- [[Brain/wiki/cards/vertical-smb-health-hypothesis|SMB Health Hypothesis]] — the next vertical to validate
- [[Brain/wiki/cards/platform-gateway-thesis|Platform Gateway Thesis]] — current substrate articulation; Layer 5 of the brand stack hosts the multi-vertical pitch
- [[Brain/wiki/cards/mission-main-street|Mission · Main Street]] — civic frame that animates the multi-vertical thesis
- [[Brain/wiki/growdirect-pitch-spine|GrowDirect Pitch Spine v0.4]] — the upstream investor narrative
