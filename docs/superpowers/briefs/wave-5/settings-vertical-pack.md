---
screen: /settings/vertical-pack
title: Vertical Pack Settings
role: ADM
wave: W5
origin: N
cp_equivalent: "None — CP has no vertical-specific configuration pack; configuration is per-field manual"
---

# Vertical Pack Settings

**URL:** `/settings/vertical-pack`  
**Primary role:** ADM  
**Entry points:** Settings → Vertical Pack section; tenant onboarding wizard → vertical selection step

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Vertical Pack", current vertical badge | |
| Main content | Active vertical + applied settings summary | |
| Action bar | Change Vertical (wizard), Reset to Defaults | |

## Key Elements

### Active Vertical Display
Shows the currently active vertical pack: name, applied-on date, configuration summary. A vertical pack is a curated set of defaults that maps to a retail industry segment.

**Current supported verticals:**
- **Garden + Nursery (default):** Pre-configured for plant retail — default departments (Tropicals, Succulents, Hardscape, Annuals, Seeds, etc.), detection rule thresholds tuned for garden retail transaction patterns, report labels using garden/nursery terminology, loyalty point currency default ("Seeds").
- **General Specialty Retail:** Neutral defaults; no domain-specific terminology or department pre-configuration.
- **Nursery + Landscape Supply:** Extends Garden + Nursery with B2B account defaults, contractor price level, heavier landscape materials departments (Aggregates, Bulk Soil, Decorative Stone).

### Applied Settings Summary
What the active vertical pack has configured:
- **Departments pre-loaded:** List of default departments
- **Detection rule thresholds:** Which thresholds were set by the vertical pack vs manually customized
- **Report labels:** Any terminology customizations ("Shrink" vs "Shrinkage", department names in reports)
- **LP substrate defaults:** Which LP substrate fields were pre-populated by the pack

**Manual overrides:** Settings changed after the vertical pack was applied are marked "Overridden." This tells ADM which defaults are still from the pack and which have been customized. An override can be reset to the pack default.

### Change Vertical
Opens a step-by-step wizard:
1. Select new vertical
2. Preview what will change (settings that differ from current configuration)
3. Confirm (settings that were manually overridden are preserved unless explicitly reset)

**Changing a vertical does not reset manual overrides by default.** The new pack's defaults apply where no manual override exists.

### Reset to Defaults
Resets all settings to the current vertical pack's defaults. Manual overrides are cleared. **Destructive action — confirmation required.** Used when a tenant's configuration has drifted and they want a clean restart from the pack.

**Empty state:** Not applicable — a vertical pack is always applied (Garden + Nursery is the default at tenant creation).

## Interaction Flows

1. **New tenant onboarding:** ADM provisions a new nursery tenant → vertical pack selection step → selects Garden + Nursery → departments, rule thresholds, and LP substrate pre-populated → ADM reviews applied settings → customizes 2 fields (adds a custom department) → onboarding complete
2. **Vertical change — expansion:** An existing Garden + Nursery tenant acquires a landscape supply operation → ADM opens Vertical Pack → changes to Nursery + Landscape Supply → preview shows: 6 new departments added, contractor price level added, 2 detection rule thresholds adjusted → confirms → tenant configuration updated
3. **Configuration drift reset:** After 18 months, ADM notices many "Overridden" labels in the Applied Settings summary → decides to clean up → reviews each override to determine which are intentional vs accidental → resets accidental overrides individually to pack defaults

## UX Callout

The vertical pack is the mechanism that makes onboarding fast for a defined industry segment and positions Canary as a domain-specific platform rather than a generic retail tool. A garden center going through onboarding shouldn't need to configure 40+ department names from scratch — the Garden + Nursery pack does it for them. The LP thresholds in the pack are tuned for garden retail transaction patterns: the void rate, average ticket, and discount structure of a nursery are different from those of an electronics retailer. Pack-tuned thresholds reduce false positive alert volume for new tenants vs the out-of-the-box defaults. The "Overridden" labels are the operational intelligence layer: ADM always knows which configuration is intentional and which is the pack, without needing documentation.

## Navigation Exits

- `/admin/tenants/:id` — for per-tenant configuration management
- `/settings/store/locations` — neighboring settings section

## Open Questions

None.
