---
type: adr
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Architecture Decision Record: Presentation Layer Architecture
## ADR-PLA-001 — Swappable Theme, Locale, and Vocabulary Packs

**Status:** APPROVED (Jeffe directive, February 25, 2026)
**Author:** ALX
**Decision Maker:** Jeffe
**Affects:** Tom (architecture), Jeremy (implementation), Art (design system), Condor (blueprint refactor), PhD (investor narrative)

---

## Context

The Triangulation work order produced a Generic Frontend Blueprint (v1.0) that successfully combines functional specs with visual design tokens in a single Markdown file. While this works for the March 3 demo, it creates a coupling problem: changing the look of the app requires editing the same file that defines what the app *does*.

Jeffe directive: the presentation layer must be fully swappable. A merchant should be able to customize their visual theme, rename fields to match their business vocabulary, and select their language — all without touching the functional core. Agencies should be able to apply their own brand to Canary's functionality. And vibe coding tools (Bolt.diy) should accept these as separate inputs.

Additionally, locale and merchant metadata labeling must be architected from day one — not retrofitted later.

---

## Decision

The presentation stack is a four-layer architecture:

```
LAYER 1: HARD CORE (Jeremy's build — never changes fast, never should)
  CRDM + Immutability Triggers + Hash Chain + Detection Engine + REST APIs
  
LAYER 2: FUNCTIONAL BLUEPRINT (Condor — brand-agnostic, locale-agnostic)
  Screen inventory, wizard flows, API contracts, navigation map,
  role visibility, seed data structure, error behaviors.
  Contains NO display strings — only token keys (e.g., {{chirp.hero.title}})
  Contains NO visual specifications — only structural layout semantics.

LAYER 3a: THEME PACK (Art / agency / merchant — swappable)
  Color tokens, typography, spacing, border radius, shadows,
  icon set, layout preferences (nav position, card style),
  mascot/avatar, animation preferences.

LAYER 3b: LOCALE PACK (i18n — swappable per language)
  All user-facing strings keyed by token.
  en-US.json is the default. Additional languages added as JSON files.
  Covers: screen labels, button text, wizard prompts, error messages,
  time-of-day greetings, completion messages, severity labels.
  Also covers: date format, number format, currency symbol, decimal separator.

LAYER 3c: VOCABULARY PACK (per-tenant merchant customization)
  Merchant-specific overrides for business terminology.
  "Employee" → "Barista", "Location" → "Café", "Cash Drawer" → "Register",
  "Chirp" → "Alert", etc.
  Stored as a JSON overlay that takes precedence over the Locale Pack.
```

### Resolution Order

When the frontend renders a display string:

```
1. Vocabulary Pack (merchant-specific terms — most specific)
2. Locale Pack (language — country/language setting)  
3. Default en-US (fallback — always works, never crashes)
```

### API Contract

Every API response that includes a display string returns both the token key and the resolved string:

```json
{
  "label_key": "chirp.hero.title",
  "label_display": "Alerta Urgente",
  "severity_key": "severity.high",
  "severity_display": "Urgente"
}
```

The backend performs resolution (it knows the merchant's language and vocabulary preferences). The frontend renders what it's told. If a merchant changes their vocabulary, the next API call returns updated labels — no frontend rebuild.

### File Structure (Post-Demo Refactor)

```
Triangulation/
  Canary_Functional_Blueprint_v2.0.md        ← Layer 2 (no display strings, no visual specs)
  ThemePacks/
    canary_default_v1.0.json                 ← Art's dark theme, animal icons
    canary_light_v1.0.json                   ← Light mode variant (future)
    white_label_template_v1.0.json           ← Blank for agencies
  LocalePacks/
    en-US.json                               ← Default
    es-MX.json                               ← Spanish (future)
    locale_template.json                     ← Blank for new languages
  VocabularyPacks/
    default.json                             ← Canary standard terms
    vocabulary_template.json                 ← Blank for new merchants
```

### Vibe Coding Input Model

Bolt.diy (or any vibe coding tool) receives three separate inputs:

```
Input 1: Functional Blueprint (what the app does)
Input 2: Theme Pack (how it looks)
Input 3: Locale Pack + Vocabulary Pack (what it says)
```

Swap any input independently. Same functionality, different presentation.

---

## Merchant Settings (Future — Sprint 7+)

```
Settings → Appearance
  └── Theme: [Canary Dark ▼] / [Canary Light ▼] / [Custom ▼]
  └── Custom: upload logo, pick primary + accent colors

Settings → Language & Labels
  └── App Language: [English ▼] / [Español ▼]
  └── Custom Labels:
        "Employee" → [__________]
        "Location" → [__________]
        "Cash Drawer" → [__________]
        "Chirp" → [__________]
  └── Preview: [See how your labels look →]

Settings → Currency & Formatting
  └── Currency: [USD $ ▼] / [MXN $ ▼] / [EUR € ▼] / [JPY ¥ ▼]
  └── Date Format: [MM/DD/YYYY ▼] / [DD/MM/YYYY ▼] / [YYYY/MM/DD ▼]
```

---

## Revenue Implications

- **Default theme:** Included in all tiers
- **Custom theming (merchant colors + logo):** Premium tier feature
- **White-label (full agency rebrand):** Enterprise tier or agency service offering
- **Locale packs beyond en-US:** Included when available (community contributions welcome)
- **Vocabulary customization:** Included in all tiers (low cost, high perceived value)

---

## Roadmap

| Item | Sprint | Owner |
|---|---|---|
| March 3 demo uses v1.0 blueprint as-is (no refactor needed) | Sprint 5 | Jeremy |
| Token-key all display strings in Functional Blueprint v2.0 | Sprint 6 | Condor |
| Default `en-US.json` locale file | Sprint 6 | Condor + Jess |
| Default `vocabulary.json` with Canary standard terms | Sprint 6 | Condor + Tom |
| Extract Theme Pack from blueprint into separate file | Sprint 6 | Condor + Art |
| Bolt.diy accepts 3 separate inputs (blueprint + theme + locale) | Sprint 7 | Jeremy |
| Vocabulary Pack editor in merchant settings UI | Sprint 7+ | Jeremy + Art |
| Second locale (`es-MX`) | Sprint 8+ | Jess + external translator |
| Agency white-label workflow documentation | Sprint 8+ | Condor + Syd |

---

## Principles

1. **No hardcoded display strings.** Every user-facing string comes from a locale/vocabulary file, never from code or blueprint.
2. **Backend resolves, frontend renders.** The API returns resolved strings. The frontend does not maintain translation files.
3. **Theme, locale, and vocabulary are independent.** Changing one never requires changing another.
4. **Default always works.** If a locale pack is missing a key, fall back to en-US. If a vocabulary pack is missing a key, fall back to the locale pack. The app never shows a raw token key to a user.
5. **Config, not code.** All three Layer 3 packs are JSON config files, not compiled code. Swapping them does not require a rebuild or redeploy.
6. **Day-one architecture, incremental delivery.** The framework supports locale and vocabulary from Sprint 6. Actual translations and merchant UI come later. But the architecture never has to be retrofitted.

---

*ADR approved by Jeffe — February 25, 2026*
*Routes to: Tom (architecture), Jeremy (implementation), Art (theming system), Condor (blueprint refactor), PhD (investor narrative)*
