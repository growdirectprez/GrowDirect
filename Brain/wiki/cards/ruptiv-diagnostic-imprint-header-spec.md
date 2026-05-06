---
classification: internal
type: wiki
sub-type: specification
status: draft
date: 2026-05-04
last-compiled: 2026-05-04
needs-review: 2026-05-18
engines: [store-ops, platform]
companion: Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md
owner: ALX
---

# Diagnostic Imprint Header Specification

## Required header

```json
{
  "type": "object",
  "required": [
    "imprint_id",
    "version",
    "name",
    "description",
    "agent_role",
    "phase",
    "scope",
    "escalation",
    "authority",
    "inputs",
    "outputs",
    "tools",
    "success_criteria",
    "exit_conditions"
  ],
  "properties": {
    "imprint_id": { "type": "string", "pattern": "^imprint-[a-z0-9-]+$" },
    "version": { "type": "string", "pattern": "^v\\d+(\\.\\d+)*$" },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "agent_role": {
      "type": "string",
      "enum": [
        "connector",
        "interviewer",
        "synthesizer",
        "scope-discoverer",
        "tribal-knowledge-extractor",
        "kpi-extractor",
        "system-mapper",
        "process-mapper"
      ]
    },
    "phase": {
      "type": "string",
      "enum": [
        "phase-1-customer-market",
        "phase-2-operating-reality",
        "cross-phase-capture"
      ]
    },
    "domain_specialization": { "type": "string" },
    "scope": {
      "type": "object",
      "required": ["in_scope", "out_of_scope"],
      "properties": {
        "in_scope": { "type": "array", "items": { "type": "string" } },
        "out_of_scope": { "type": "array", "items": { "type": "string" } }
      }
    },
    "escalation": {
      "type": "object",
      "required": ["escalate_to", "triggers"],
      "properties": {
        "escalate_to": { "type": "string", "enum": ["astronaut", "mission-control"] },
        "triggers": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["condition", "severity"],
            "properties": {
              "condition": { "type": "string" },
              "severity": { "type": "string", "enum": ["info", "warn", "halt"] },
              "default_action": { "type": "string" }
            }
          }
        }
      }
    },
    "authority": {
      "type": "object",
      "required": ["read", "write"],
      "properties": {
        "read": { "type": "array", "items": { "type": "string" } },
        "write": { "type": "array", "items": { "type": "string" } }
      }
    },
    "inputs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "shape"],
        "properties": {
          "source": { "type": "string" },
          "shape": { "type": "string" },
          "required": { "type": "boolean" }
        }
      }
    },
    "outputs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["artifact_type", "writes_to_facets", "shape"],
        "properties": {
          "artifact_type": { "type": "string" },
          "writes_to_facets": { "type": "array", "items": { "type": "string" } },
          "shape": { "type": "string" }
        }
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["mcp_server", "operations"],
        "properties": {
          "mcp_server": { "type": "string" },
          "operations": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "success_criteria": { "type": "array", "items": { "type": "string" } },
    "exit_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["condition", "outcome"],
        "properties": {
          "condition": { "type": "string" },
          "outcome": {
            "type": "string",
            "enum": ["complete", "blocked", "escalated", "failed"]
          }
        }
      }
    },
    "model_requirements": {
      "type": "object",
      "properties": {
        "minimum_model": { "type": "string" },
        "harness": { "type": "string", "enum": ["managed-agents", "agent-engine", "either"] },
        "context_budget": { "type": "integer" }
      }
    },
    "audit_requirements": {
      "type": "object",
      "properties": {
        "log_tool_calls": { "type": "boolean", "default": true },
        "log_decisions": { "type": "boolean", "default": true },
        "redaction_rules": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## Authority defaults

- Agents write only `finding` and `audit-event` by default
- `schema-fragment` writes restricted to synthesizer and scope-discoverer roles
- `decision` reserved to astronaut and mission-control
- `handoff` reserved to mission-control under signature
- Tool access is per-mcp-server, per-operation; no blanket access

## Validation rules

At registration:

- Header matches the schema above
- `agent_role` from enum
- `outputs.writes_to_facets` references facets present in current diagnostic schema
- `tools.mcp_server` resolves to a registered server
- `escalation.triggers` includes at least one `halt`
- `exit_conditions` includes `complete` plus at least one failure outcome

At runtime load:

- Engagement binding succeeds (engagement_id + tool credentials)
- Required inputs present in engagement record
- Authority claims enforceable by capsule

Failures emit `audit-event` of type `imprint-validation-failure` and the imprint does not load.

## Worked example

```json
{
  "imprint_id": "imprint-phase1-customer-base",
  "version": "v1",
  "name": "customer-base catalog",
  "description": "Classify every customer by segment, install_type, customization_depth, sizing, and primary integrations from CRM and billing.",
  "agent_role": "connector",
  "phase": "phase-1-customer-market",
  "scope": {
    "in_scope": [
      "Read customer records from CRM and billing via authorized mcp-servers",
      "Classify each customer by segment, install_type, sizing_tier, customization_depth",
      "Flag concentration above 25% from a single customer"
    ],
    "out_of_scope": [
      "Reading financials beyond billing line totals",
      "Modifying customer records",
      "Reading PII beyond billing-name and primary-contact"
    ]
  },
  "escalation": {
    "escalate_to": "astronaut",
    "triggers": [
      { "condition": "PII beyond billing scope appears in records", "severity": "halt", "default_action": "stop reading" },
      { "condition": "Customer record count exceeds 5000", "severity": "warn", "default_action": "switch to sampled mode" },
      { "condition": "CRM connector returns auth error", "severity": "halt", "default_action": "wait for credential refresh" }
    ]
  },
  "authority": {
    "read": ["charter", "capture:crm", "capture:billing"],
    "write": ["finding", "audit-event"]
  },
  "inputs": [
    { "source": "charter", "shape": "charter.v1", "required": true },
    { "source": "capture:crm", "shape": "capture.crm.v1", "required": true },
    { "source": "capture:billing", "shape": "capture.billing.v1", "required": true }
  ],
  "outputs": [
    { "artifact_type": "finding", "writes_to_facets": ["customer-base"], "shape": "finding.customer-base.v1" }
  ],
  "tools": [
    { "mcp_server": "crm", "operations": ["search_companies", "get_company", "list_deals"] },
    { "mcp_server": "billing", "operations": ["list_customers", "list_subscriptions"] }
  ],
  "success_criteria": [
    "At least 95% of customers in source CRM present in finding",
    "Each classified customer has segment, install_type, sizing_tier populated",
    "Top-10-by-revenue list produced",
    "Concentration flag set if top customer revenue exceeds 25%"
  ],
  "exit_conditions": [
    { "condition": "All success_criteria met", "outcome": "complete" },
    { "condition": "PII halt trigger fires", "outcome": "escalated" },
    { "condition": "Auth halt with no refresh in 30 minutes", "outcome": "blocked" },
    { "condition": "MCP non-recoverable error", "outcome": "failed" }
  ],
  "model_requirements": {
    "minimum_model": "<model-id>",
    "harness": "agent-engine",
    "context_budget": 200000
  },
  "audit_requirements": {
    "log_tool_calls": true,
    "log_decisions": true,
    "redaction_rules": ["customer-pii", "billing-card-numbers"]
  }
}
```

## Open

- First imprint set: customer-base, segment-heatmap, market-position, value-prop, brand-promise, stakeholder-map, kpi-extraction, system-map, sop-synthesis, staff-interview
- MCP server catalog for engagement-default tools
- Schema versioning and compatibility policy
