---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor — B-068-B: Blueprint v2.0 Tokenization
## Session Prompt

**Work Order:** B-068, Lane B
**Date:** February 28, 2026
**From:** ALX
**Priority:** 🔴 HIGH — Gates Lane C (JSON files). Gates B-067-A capability map user-facing strings.

---

## Read This First

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/PhD/
  GrowDirect_UnifiedArchitectureThesis_v1.0.md
```

Section **3.3 (The Presentation Layer)** specifically. Then Section **4 (The Unified Statement)**.

The vocabulary pack is not a localization feature. It is the presentation-layer expression
of merchant-first isolation — the same principle that produced the per-merchant hash chain
and the per-merchant Postgres partition. Every display string that a merchant can rename
represents one merchant's bounded, independent interface to the system. That is the reason
this refactor matters. The architecture requires it.

---

## Source Document

Blueprint v1.0 is here:

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Triangulation/
  Canary_Generic_Frontend_Blueprint_v1.0.md
```

Read it completely before writing a single token key. Understand the structure before
stripping the strings.

---

## What You Are Doing

Blueprint v1.0 contains hardcoded display strings throughout. Merchant-facing labels,
module titles, action text, status words — all written in English, all embedded directly
in the Blueprint spec.

You are stripping every display string and replacing it with a structured token key in
`{{module.screen.element.variant}}` format.

The Blueprint v2.0 output describes structure, layout, and behavior. It does not contain
a single English label that a merchant would ever see on screen. Those strings live in
the JSON packs that Condor produces in Lane C.

---

## Token Key Format

```
{{module.screen.element.variant}}
```

Examples:
```
{{chirp.card.title}}
{{chirp.card.severity.label}}
{{companion.today.greeting.morning}}
{{employee.label.singular}}
{{employee.label.plural}}
{{cash_drawer.label.singular}}
{{fox.case.status.open}}
{{nav.primary.dashboard.label}}
{{action.button.resolve.label}}
{{shared.status.loading}}
```

Rules:
- All lowercase
- Dot-separated namespacing
- Module first: `chirp`, `companion`, `fox`, `goose`, `owl`, `nav`, `action`, `shared`
- For business-term labels (the vocabulary-overridable tokens): use `{entity}.label.{singular|plural}`
- For UI strings (not overridable by merchants): use descriptive paths
- No abbreviations unless the abbreviation is the canonical CRDM field name

---

## Two Deliverables

### Deliverable 1: `Canary_Generic_Frontend_Blueprint_v2.0.md`

The tokenized Blueprint. Structure, layout, components, behavior specs — all intact.
Every display string replaced with `{{token.key}}`.

What stays in the Blueprint:
- Layout descriptions
- Component structure
- Behavior specs (tap targets, loading states, error states)
- API contract references
- Conditional rendering logic
- Accessibility requirements

What leaves the Blueprint:
- Every English word a merchant would see
- Every label, button text, status string, placeholder text
- Every section title, card header, nav item label

**No hex colors in v2.0.** Colors belong in the Theme Pack JSON. If v1.0 has hex codes
embedded in component specs, replace with `{{theme.color.token}}` references.

**No font names.** Typography belongs in the Theme Pack. Replace with semantic tokens:
`{{theme.font.heading}}`, `{{theme.font.body}}`.

### Deliverable 2: `B068_TokenRegistry_v1.0.md`

A flat registry of every token key in the Blueprint. One row per token key.

Columns:
| Token Key | Category | Vocabulary-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `employee.label.singular` | business-term | YES | Singular form of employee | Employee |
| `chirp.card.title` | chirp-ui | NO | Title of a Chirp alert card | (derived from rule) |
| `companion.today.greeting.morning` | companion-ui | NO | Morning greeting on Today's View | Good morning |

**Vocabulary-overridable = YES** for any token that represents a business term the
merchant might rename. These are the tokens the Settings → Language & Labels page
will expose. The list starts with these — extend it as you find more in the Blueprint:

```
employee.label.singular / plural
location.label.singular / plural
cash_drawer.label.singular / plural
transaction.label.singular / plural
void.label.singular / plural
refund.label.singular / plural
case.label.singular / plural
chirp.label.singular / plural     ← default resolves to "Alert" (not "Chirp")
shift.label.singular / plural
tender.label.singular / plural
```

The registry is Lane C's input. Condor uses it in their next session to build the JSON
files. It is also Tom's reference for the `merchant_vocabulary` DB schema (Lane D).
Make it complete and exact.

---

## IP Discipline

You are the IP sanitization agent. Apply that discipline here.

The Blueprint must describe what the system looks like and how it behaves.
It must not expose:
- Chirp rule logic or detection algorithms
- CRDM field names beyond what's needed for display token naming
- Any internal codename that isn't merchant-facing
- PhD research framing or patent claim language

The token key naming convention uses CRDM-aligned field names where they apply
(`employee`, `transaction`, `refund`, `cash_drawer`, `location`). That is correct —
it ensures the token layer and the data layer are consistent. It does not require
exposing the CRDM schema.

PhD supervises this deliverable. Flag anything that feels like it's crossing the hood
before you include it.

---

## B-067 Connection

B-067-A (the Square Capability Dashboard) requires token keys for:
- LP Signals section header
- Capability phase labels
- Coverage status labels

Before Condor writes B-067-A, read the registry from this lane and use it.
No hardcoded English in the capability map user-facing strings.

If you're running B-067-A in the same session as B-068-B: complete the registry
first, then use it in the capability map. The registry is a 20-minute document.
Do not skip it.

---

## Output

```
_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v2.0.md
_ALX/WorkOrders/output/Condor/B068_TokenRegistry_v1.0.md
```

Also create the output directory if it doesn't exist:
```
_ALX/WorkOrders/output/Triangulation/LocalePacks/
_ALX/WorkOrders/output/Triangulation/VocabularyPacks/
```

Lane C needs these directories ready.

---

## Coordination

**Runs parallel with Tom's Lanes A and D.** No dependency on Tom's output.

**Gates Lane C.** Condor cannot build the JSON files until the token registry exists.

**Gates B-067-A** for any user-facing strings. Write the registry. Use it in B-067-A.

---

*ALX | B-068-B | February 28, 2026*
*"The Blueprint describes structure. The JSON describes language. Never mix them."*
