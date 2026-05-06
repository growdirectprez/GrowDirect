---
classification: internal
type: wiki
sub-type: specification
status: draft
date: 2026-05-04
last-compiled: 2026-05-04
needs-review: 2026-05-18
engines: [store-ops, platform]
companion: Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md
owner: ALX
---

# Diagnostic Artifact Taxonomy

## Canonical types

| Type | Producer | Storage |
|---|---|---|
| `charter` | mission-control | engagement repo + bus |
| `imprint` | imprint library (versioned) | imprint library + bus |
| `finding` | propagation agent | bus, indexed by imprint + run |
| `schema-fragment` | synthesizer | bus, queryable by facet |
| `transcript` | interviewer | bus + object storage |
| `capture` | connector | object storage + bus index |
| `synthesis` | synthesizer | engagement repo + bus |
| `decision` | mission-control / astronaut | audit log + bus |
| `handoff` | mission-control (signed) | engagement repo + bus snapshot |
| `audit-event` | all layers (auto) | append-only audit log |

## Universal envelope

```json
{
  "type": "object",
  "required": [
    "artifact_id",
    "artifact_type",
    "namespace",
    "schema_version",
    "engagement_id",
    "producer",
    "produced_at",
    "audit_hash"
  ],
  "properties": {
    "artifact_id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
    "artifact_type": {
      "type": "string",
      "enum": [
        "charter",
        "imprint",
        "finding",
        "schema-fragment",
        "transcript",
        "capture",
        "synthesis",
        "decision",
        "handoff",
        "audit-event"
      ]
    },
    "namespace": { "type": "string" },
    "schema_version": { "type": "string", "pattern": "^v\\d+(\\.\\d+)*$" },
    "engagement_id": { "type": "string", "pattern": "^eng-[a-z0-9-]+$" },
    "producer": {
      "type": "object",
      "required": ["layer", "identity"],
      "properties": {
        "layer": {
          "type": "string",
          "enum": ["mission-control", "astronaut", "capsule", "agent", "tool"]
        },
        "identity": { "type": "string" },
        "imprint_id": { "type": "string" },
        "imprint_version": { "type": "string" }
      }
    },
    "produced_at": { "type": "string", "format": "date-time" },
    "audit_hash": { "type": "string" },
    "supersedes": { "type": "string" },
    "links": { "type": "array", "items": { "type": "string" } }
  }
}
```

## Per-type body schemas

### `charter`

```json
{
  "type": "object",
  "required": ["customer", "mission_control", "scope", "timeline", "success_criteria"],
  "properties": {
    "customer": {
      "type": "object",
      "required": ["name", "vertical", "primary_contact"],
      "properties": {
        "name": { "type": "string" },
        "vertical": { "type": "string" },
        "primary_contact": { "type": "object" },
        "stack": { "type": "object" }
      }
    },
    "mission_control": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "org", "role"]
      }
    },
    "scope": {
      "type": "object",
      "required": ["in_scope", "out_of_scope"],
      "properties": {
        "in_scope": { "type": "array", "items": { "type": "string" } },
        "out_of_scope": { "type": "array", "items": { "type": "string" } }
      }
    },
    "timeline": {
      "type": "object",
      "required": ["start", "handoff_target"],
      "properties": {
        "start": { "type": "string", "format": "date" },
        "handoff_target": { "type": "string", "format": "date" },
        "milestones": { "type": "array" }
      }
    },
    "success_criteria": { "type": "array", "items": { "type": "string" } }
  }
}
```

### `finding`

```json
{
  "type": "object",
  "required": ["imprint_id", "run_id", "scope_evidence", "content", "confidence"],
  "properties": {
    "imprint_id": { "type": "string" },
    "run_id": { "type": "string" },
    "scope_evidence": {
      "type": "object",
      "required": ["sources_consulted", "completeness"],
      "properties": {
        "sources_consulted": { "type": "array", "items": { "type": "string" } },
        "completeness": {
          "type": "string",
          "enum": ["full", "partial", "blocked"]
        },
        "blockers": { "type": "array", "items": { "type": "string" } }
      }
    },
    "content": { "type": "object" },
    "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
    "writes_to_facets": { "type": "array", "items": { "type": "string" } }
  }
}
```

### `schema-fragment`

```json
{
  "type": "object",
  "required": ["facet", "data", "source_findings"],
  "properties": {
    "facet": {
      "type": "string",
      "enum": [
        "mission-value-prop",
        "customer-base",
        "stakeholder-map",
        "operating-process",
        "kpi",
        "org-structure",
        "system-map",
        "data-flows",
        "sop",
        "compliance-posture",
        "cultural-reality"
      ]
    },
    "data": { "type": "object" },
    "source_findings": { "type": "array", "items": { "type": "string" } },
    "review_status": {
      "type": "string",
      "enum": ["draft", "astronaut-reviewed", "mission-control-approved"]
    }
  }
}
```

### `decision`

```json
{
  "type": "object",
  "required": ["question", "options_considered", "decision", "authority", "rationale"],
  "properties": {
    "question": { "type": "string" },
    "options_considered": { "type": "array", "items": { "type": "string" } },
    "decision": { "type": "string" },
    "authority": { "type": "string", "enum": ["mission-control", "astronaut"] },
    "rationale": { "type": "string" },
    "raised_by": { "type": "string" },
    "escalation_path": { "type": "array", "items": { "type": "string" } }
  }
}
```

Body schemas for `imprint`, `transcript`, `capture`, `synthesis`, `handoff`, `audit-event` land in companion JSON Schema files.

## Naming

- Engagement ID: `eng-<customer-slug>-<yymm>`
- Artifact ID: `<artifact_type>-<short-ULID>`
- Imprint ID: `imprint-<phase>-<role>-v<version>`
- Facet names: lowercase-hyphenated, from the enum

## Storage layout

```
eng-<customer-slug>-<yymm>/
├── charter.json
├── imprints/
│   └── <imprint_id>.json
├── findings/
│   └── <run_id>/
│       └── <artifact_id>.json
├── captures/
│   └── <source>/<artifact_id>/
├── transcripts/
│   └── <artifact_id>.json
├── schema/
│   └── <facet>.json
├── synthesis/
│   └── <facet>.md
├── decisions/
│   └── <artifact_id>.json
├── audit/
│   └── audit-events.ndjson
└── handoff/
    └── workspace/
```

Bus mirrors structure as a queryable index.

## Validation rules

At write:

- Envelope schema validates
- Body schema for `artifact_type` validates
- `audit_hash` computed and recorded to audit log
- Failures emit `audit-event` of type `validation-rejection` and reject the write

## Open

- Body schemas for `imprint`, `transcript`, `capture`, `synthesis`, `handoff`, `audit-event`
- Per-facet `data` shapes for `schema-fragment`
- Schema versioning policy (deprecation, migration)
