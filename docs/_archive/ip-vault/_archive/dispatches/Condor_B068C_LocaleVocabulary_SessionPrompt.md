---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor — B-068-C: Locale and Vocabulary JSON Files
## Session Prompt

**Work Order:** B-068, Lane C
**Date:** February 28, 2026
**From:** ALX
**Priority:** 🟡 HIGH — Gates the vocabulary resolution system. Runs after Lane B token registry.

---

## Gate: Read This Before Starting

This lane depends on the token registry from Lane B:

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/
  B068_TokenRegistry_v1.0.md
```

**Do not start Lane C until the registry exists.** The JSON files are generated from
the registry. If the registry is incomplete, the JSON files will be wrong, and
Tom's resolution function will miss keys.

Also read:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/PhD/
  GrowDirect_UnifiedArchitectureThesis_v1.0.md
```
Section 3.3 — specifically the resolution order and the vocabulary-overridable token
table. This gives you the design intent behind what you're building.

---

## What You Are Building

Three JSON files that power the vocabulary resolution system.

The resolution chain (from white paper Section 3.3):
```
merchant_vocabulary DB  (per-merchant overrides — most specific)
        ↓ miss
Locale Pack JSON        (this is what you're building — language defaults)
        ↓ miss
en-US.json              (hardcoded fallback — you're building this too)
```

The API resolution service loads these JSON files at startup. They are the
in-memory source of truth for every string resolution that doesn't have a
merchant-specific override in the DB.

---

## Deliverable 1: `en-US.json`

Every token key in the registry, resolved to English.

This file is the guaranteed fallback. It must be complete — every key, no gaps.
If the resolution chain reaches this file and the key isn't here, the API throws.

Format:
```json
{
  "locale": "en-US",
  "version": "1.0.0",
  "generated": "2026-02-28",
  "tokens": {
    "employee": {
      "label": {
        "singular": "Employee",
        "plural": "Employees"
      }
    },
    "location": {
      "label": {
        "singular": "Location",
        "plural": "Locations"
      }
    },
    "chirp": {
      "label": {
        "singular": "Alert",
        "plural": "Alerts"
      },
      "card": {
        "title": null,
        "severity": {
          "label": {
            "critical": "Critical",
            "high": "High",
            "medium": "Medium",
            "low": "Low"
          }
        }
      }
    }
  }
}
```

Notes:
- Nested structure mirrors the token key path: `chirp.card.title` → `tokens.chirp.card.title`
- `null` values are valid for tokens whose display value is computed at runtime
  (e.g., a Chirp title that comes from the rule name, not a static string)
- Every key in the registry that has a static default gets a value here
- "Chirp" resolves to "Alert" in all end-user-facing contexts. Internal codename
  "Chirp" never appears in any merchant-facing string.

## Deliverable 2: `default_vocabulary.json`

The standard Canary vocabulary for a generic retail merchant. This is the default
locale pack for merchants who haven't configured any overrides and whose locale
is `en-US`.

This file contains only the **vocabulary-overridable tokens** — the business terms
that define the merchant's conceptual model of their business. It does not contain
UI strings.

```json
{
  "merchant_id": "__default__",
  "locale": "en-US",
  "version": "1.0.0",
  "description": "Canary default vocabulary — generic retail",
  "tokens": {
    "employee": {
      "label": { "singular": "Employee", "plural": "Employees" }
    },
    "location": {
      "label": { "singular": "Location", "plural": "Locations" }
    },
    "cash_drawer": {
      "label": { "singular": "Cash Drawer", "plural": "Cash Drawers" }
    },
    "transaction": {
      "label": { "singular": "Transaction", "plural": "Transactions" }
    },
    "void": {
      "label": { "singular": "Void", "plural": "Voids" }
    },
    "refund": {
      "label": { "singular": "Refund", "plural": "Refunds" }
    },
    "case": {
      "label": { "singular": "Case", "plural": "Cases" }
    },
    "chirp": {
      "label": { "singular": "Alert", "plural": "Alerts" }
    }
  }
}
```

## Deliverable 3: `vocabulary_template.json`

A blank template for merchant-specific overrides. Every vocabulary-overridable token
key present, every value set to `null`. A merchant's Settings → Language & Labels
page reads this template to know what fields to display, and writes the merchant's
choices back to the DB (`merchant_vocabulary` table, Tom's Lane D).

```json
{
  "merchant_id": null,
  "locale": "en-US",
  "version": "1.0.0",
  "instructions": "Set values for any terms you want to customize. Leave null to use defaults.",
  "tokens": {
    "employee": {
      "label": { "singular": null, "plural": null }
    }
  }
}
```

---

## Vertical Reference Examples

**Document these in a separate section of each file — do not include as defaults.**

These are reference implementations showing how the vocabulary pack enables vertical
market deployment without code changes. Include them as comments or in a
`_vertical_examples` key that the application ignores:

```
Restaurant:
  employee → Server / Servers
  location → Restaurant / Restaurants
  cash_drawer → Register / Registers
  transaction → Check / Checks
  void → Void / Voids

Specialty Coffee:
  employee → Barista / Baristas
  location → Café / Cafés
  cash_drawer → Register / Registers
  transaction → Order / Orders

Cannabis Dispensary:
  employee → Budtender / Budtenders
  location → Dispensary / Dispensaries
  transaction → Receipt / Receipts
  void → Cancellation / Cancellations

Franchise Retail:
  employee → Associate / Associates
  location → Store / Stores
  cash_drawer → Till / Tills
  transaction → Sale / Sales
```

These examples are the "any app" proof in JSON form. One vocabulary pack. Any vertical.
Zero code changes.

---

## Naming and Format Rules

- All keys lowercase, dot-path structure (mirrors token key format)
- UTF-8 encoding throughout
- BCP 47 locale codes (`en-US`, `es-MX` — never `en_US`)
- `version` field follows semver (`1.0.0`)
- No trailing commas (valid JSON, not JSON5)
- Pretty-printed with 2-space indentation

---

## Output

```
_ALX/WorkOrders/output/Triangulation/LocalePacks/en-US.json
_ALX/WorkOrders/output/Triangulation/VocabularyPacks/default_vocabulary.json
_ALX/WorkOrders/output/Triangulation/VocabularyPacks/vocabulary_template.json
```

---

## Coordination

**Depends on:** Lane B token registry. Do not start without it.

**Feeds Tom (Lane D):** Your locale field naming (`en-US`, `es-MX`) must match what
Tom defines in `merchants.locale`. Confirm the BCP 47 convention is consistent.

**Feeds Art (Sprint 7):** The vocabulary editor UI reads `vocabulary_template.json`
to know which fields to show merchants. The field set you define here IS the
product feature set for the Language & Labels settings page.

---

*ALX | B-068-C | February 28, 2026*
*"Four JSON files. Any vertical. Zero code changes. That's what they look like."*
