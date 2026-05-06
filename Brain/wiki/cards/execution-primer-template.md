---
classification: internal
type: wiki
sub-type: template-spec
status: active
date: 2026-05-04
last-compiled: 2026-05-04
needs-review: 2026-06-04
engines: [platform]
companion: Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md
companion: Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md
owner: ALX
---

# Execution Primer Template

Single-file dark-theme HTML primer with inline SVG diagrams. One per consulting skill or method. Same chassis (chain of command, artifact taxonomy, run-loop, three-layer integration, validation, bidirectional plumbing) with method-specific phases, imprints, facets, overlay, and handoff.

## Generator

`Brain/templates/execution-primer-generator.py`

Self-contained Python. No external dependencies. Authors HTML to a target directory. SVG diagrams hand-authored via helper functions; no JS, no CDN.

Run:

```
python3 Brain/templates/execution-primer-generator.py
```

## Section order (lean — companion primer)

A companion primer covers only how the pattern changes for the method and what data points it produces. Substrate (chain of command, artifact taxonomy, run-loop, three-layer, validation, bidirectional plumbing) lives once in the diagnostic primer and spec cards — never repeated.

1. Title + lead
2. Substrate cross-reference note
3. What it produces (table)
4. Phase structure (method-specific diagram)
5. Imprints per phase (grouped lists)
6. Method overlay (method-specific diagram + description)
7. Data points produced (table — name, what it captures, decision it enables)
8. Handoff package (method-specific table)
9. Companion specs (cross-references)

## Method data schema

Each method is one entry in the `METHODS` dict in the generator. Fields:

```python
{
    "title": str,                    # primer title
    "lead": str,                     # one-paragraph what + why
    "outputs": [(label, form), ...], # what the engagement produces
    "phases": [
        (name, sublabel, [imprint_id, ...]),
        ...                          # exactly 3 phases
    ],
    "overlay": {
        "title": str,                # method-specific dispatch pattern
        "description": str,
        "actors": [(name,), ...],    # 5-7 actors
        "messages": [
            (src_idx, dst_idx, label, "sync" | "dashed"),
            ...                      # 5-10 messages
        ]
    },
    "data_points": [
        (name, what_it_captures, decision_it_enables),
        ...                          # the evidence the transformation team picks up
    ],
    "handoff_items": [(item, form), ...]
}
```

## Substrate (defined once, never repeated)

These elements are defined in `diagnostic-execution-primer.html` and the spec cards. Companion primers reference them; they do not repeat them.

- Chain of command diagram (5-layer command structure)
- Artifact types table (10 canonical types)
- Run-loop per imprint dispatch (sequence + steps)
- Three-layer integration (issues / wiki / bus)
- Validation discipline at every step
- Bidirectional plumbing (capture as-is, push to-be)

## Aesthetic tokens

```
--bg: #0d1117
--fg: #e6edf3
--muted: #8b949e
--accent: #58a6ff
--border: #30363d
--code-bg: #161b22
--mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace
```

Boxes: rounded 6px corners, code-bg fill, border stroke, monospace label + muted sublabel.
Solid arrows: muted color, marker-end arrowhead.
Dotted arrows: accent color, dashed stroke, marker-end accented arrowhead.
Sequence diagrams: actor boxes at top, dashed lifelines, message lines with label pills over background.

## Existing primers

| Method | File |
|---|---|
| Ruptiv diagnostic (2-phase) | `Brain/wiki/diagnostic-execution-primer.html` |
| Strategic positioning | `Brain/wiki/strategic-positioning-execution-primer.html` |
| SISP | `Brain/wiki/sisp-execution-primer.html` |
| SaaS | `Brain/wiki/saas-execution-primer.html` |

## To add a new method

1. Add an entry to `METHODS` in the generator with the schema above.
2. Run the generator.
3. New `<slug>-execution-primer.html` lands in `Brain/wiki/`.

## Open

- 2-phase variant of `phase_structure()` for diagnostic-primer-style methods (currently authored separately)
- Externalize `METHODS` to YAML/JSON so non-Python edits work
- CLI flag for output directory
- Per-method theme overrides (color accents) if needed
