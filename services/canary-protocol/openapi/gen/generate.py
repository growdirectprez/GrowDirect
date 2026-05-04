#!/usr/bin/env python3
"""
Canary Protocol — OpenAPI 3.0 spec generator.

Reads:
  docs/sdds/go-handoff/canonical-data-model.md  (entity definitions)
  docs/sdds/go-handoff/mcp-service-junctions.md (junction inventory)

Emits:
  services/canary-protocol/openapi/openapi.yaml

The spec rebuilds from canonical SDD source rather than being hand-edited.
Run: python3 services/canary-protocol/openapi/gen/generate.py

Patent context: Application 63/991,596 (Universal Event Notarization).
This dispatch (GRO-740) is the developer-facing surface — parallel to
the patent architecture, not part of the patent claims themselves.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[4]
SDD_CANONICAL = REPO_ROOT / "docs/sdds/go-handoff/canonical-data-model.md"
SDD_JUNCTIONS = REPO_ROOT / "docs/sdds/go-handoff/mcp-service-junctions.md"
OUTPUT = REPO_ROOT / "services/canary-protocol/openapi/openapi.yaml"


# ---------------------------------------------------------------------------
# Supplemental definitions
#
# The canonical SDD declares some app.* entities as "preserve as-is from
# current Canary spec" without explicit DDL (e.g., app.users,
# app.external_identities). To produce a complete OpenAPI surface, we synthesize
# minimal canonical-style DDL here, derived from the live Canary models. The
# generator parses this through the same pipeline as the SDD.
# ---------------------------------------------------------------------------

SUPPLEMENTAL_DDL = """
# §10S Supplemental — preserve-as-is entities (synthesized DDL)

### app.users

```sql
CREATE TABLE app.users (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  username        text NOT NULL,
  email           text NOT NULL,
  display_name    text,
  is_active       boolean NOT NULL DEFAULT true,
  last_login_at   timestamptz,
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, email)
);
```

### app.external_identities

```sql
CREATE TABLE app.external_identities (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  entity_type     text NOT NULL,
  entity_id       uuid NOT NULL,
  source_code     text NOT NULL,
  external_id     text NOT NULL,
  is_primary      boolean NOT NULL DEFAULT true,
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, source_code, entity_type, external_id),
  UNIQUE (tenant_id, entity_type, entity_id, source_code)
);
```
"""


# ---------------------------------------------------------------------------
# SQL → OpenAPI type mapping
# ---------------------------------------------------------------------------

# (regex pattern → OpenAPI schema fragment producer)
TYPE_MAP: list[tuple[re.Pattern, callable]] = [
    (re.compile(r"^uuid$", re.I), lambda _: {"type": "string", "format": "uuid"}),
    (re.compile(r"^text$", re.I), lambda _: {"type": "string"}),
    (
        re.compile(r"^varchar\s*\(\s*(\d+)\s*\)$", re.I),
        lambda m: {"type": "string", "maxLength": int(m.group(1))},
    ),
    (re.compile(r"^char\s*\(\s*(\d+)\s*\)$", re.I),
     lambda m: {"type": "string", "maxLength": int(m.group(1))}),
    (re.compile(r"^bigint$", re.I), lambda _: {"type": "integer", "format": "int64"}),
    (re.compile(r"^smallint$", re.I), lambda _: {"type": "integer", "format": "int32"}),
    (re.compile(r"^int(eger)?$", re.I), lambda _: {"type": "integer", "format": "int32"}),
    (
        re.compile(r"^numeric\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)$", re.I),
        lambda m: {
            "type": "string",
            "format": "decimal",
            "description": (
                f"decimal({m.group(1)},{m.group(2)}) — string-encoded for "
                "precision; clients should not coerce to float"
            ),
        },
    ),
    (re.compile(r"^numeric$", re.I),
     lambda _: {"type": "string", "format": "decimal"}),
    (re.compile(r"^bool(ean)?$", re.I), lambda _: {"type": "boolean"}),
    (
        re.compile(r"^timestamp(\s+with\s+time\s+zone)?$|^timestamptz$", re.I),
        lambda _: {"type": "string", "format": "date-time"},
    ),
    (re.compile(r"^date$", re.I), lambda _: {"type": "string", "format": "date"}),
    (re.compile(r"^time(stamptz)?$", re.I),
     lambda _: {"type": "string", "format": "date-time"}),
    (
        re.compile(r"^jsonb?$", re.I),
        lambda _: {"type": "object", "additionalProperties": True},
    ),
    (re.compile(r"^ltree$", re.I),
     lambda _: {"type": "string", "description": "Postgres ltree path"}),
    (re.compile(r"^bytea$", re.I),
     lambda _: {"type": "string", "format": "byte"}),
]


def map_sql_type(sql_type: str) -> dict:
    """Map a SQL type string to an OpenAPI schema fragment."""
    sql_type = sql_type.strip()
    for pat, builder in TYPE_MAP:
        m = pat.match(sql_type)
        if m:
            return builder(m)
    # Fallback: unknown type → string with description
    return {
        "type": "string",
        "description": f"Unmapped SQL type: {sql_type}",
    }


# ---------------------------------------------------------------------------
# SDD parsing
# ---------------------------------------------------------------------------

ENTITY_HEADING = re.compile(r"^(##|###)\s+([a-z_][a-z_0-9]*)\.([a-z_][a-z_0-9]*)\s*$")
SQL_FENCE_OPEN = re.compile(r"^```sql\s*$", re.I)
SQL_FENCE_CLOSE = re.compile(r"^```\s*$")
CREATE_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"([a-z_][a-z_0-9]*)\.([a-z_][a-z_0-9]*)\s*\(",
    re.I,
)
COLUMN_LINE = re.compile(
    r"""^
    \s*
    ([a-z_][a-z_0-9]*)              # column name
    \s+
    ([a-z][a-z0-9_]*               # type (with optional precision)
       (?:\s+with\s+time\s+zone)?
       (?:\s*\([^)]*\))?
    )
    (.*)$                          # remaining: NOT NULL, DEFAULT, REFERENCES, etc.
    """,
    re.I | re.X,
)


@dataclass
class Field:
    name: str
    sql_type: str
    not_null: bool = False
    default: Optional[str] = None
    references: Optional[str] = None  # "schema.entity(column)"
    description: Optional[str] = None


@dataclass
class Entity:
    schema: str
    name: str
    fields: list[Field] = field(default_factory=list)
    raw_sql: str = ""
    section: str = ""  # narrative section title


SKIPPED_LINE_KEYWORDS = (
    "PRIMARY KEY",
    "FOREIGN KEY",
    "UNIQUE ",
    "UNIQUE(",
    "CHECK ",
    "CHECK(",
    "CONSTRAINT ",
    "EXCLUDE ",
)


def parse_create_table(sql: str) -> list[Field]:
    """Extract field definitions from a CREATE TABLE block.

    Line-based: each physical line is treated as a column candidate. Trailing
    SQL comments (`-- ...`) are stripped per line, then a trailing comma is
    removed, then the COLUMN_LINE regex matches column declarations. This
    correctly handles comments that span the rest of a line — earlier
    char-based comma splitting bled comment text into the next column line and
    swallowed real fields.
    """
    fields: list[Field] = []

    # Find the body between the opening "(" and the matching closing ");"
    open_paren = sql.find("(")
    if open_paren == -1:
        return fields

    depth = 0
    body_end = None
    for i in range(open_paren, len(sql)):
        c = sql[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                body_end = i
                break
    if body_end is None:
        return fields

    body = sql[open_paren + 1:body_end]

    for raw_line in body.split("\n"):
        # Strip trailing line-comment
        comment: Optional[str] = None
        line = raw_line
        comment_idx = line.find("--")
        if comment_idx >= 0:
            comment = line[comment_idx + 2:].strip() or None
            line = line[:comment_idx]
        line = line.rstrip()
        # Strip a trailing comma (column separator)
        if line.endswith(","):
            line = line[:-1].rstrip()
        line = line.strip()
        if not line:
            continue

        upper = line.upper()
        if any(upper.startswith(k) for k in SKIPPED_LINE_KEYWORDS):
            continue

        m = COLUMN_LINE.match(line)
        if not m:
            continue

        col_name = m.group(1)
        col_type = m.group(2).strip()
        rest = m.group(3) or ""

        upper_rest = rest.upper()
        not_null = "NOT NULL" in upper_rest
        is_pk_inline = "PRIMARY KEY" in upper_rest

        # DEFAULT extraction — capture the next token (literal, function call,
        # or simple identifier). Function calls like gen_random_uuid() include
        # parens; quoted strings like 'individual' should also work.
        default = None
        m_def = re.search(
            r"\bDEFAULT\s+("
            r"'[^']*'"                    # quoted literal
            r"|[a-zA-Z_][\w]*\s*\([^)]*\)" # function call
            r"|[\-+]?\d+(?:\.\d+)?"        # numeric
            r"|[a-zA-Z_][\w]*"             # bare identifier (true, false, null, ...)
            r")",
            rest, re.I,
        )
        if m_def:
            default = m_def.group(1).strip()

        # REFERENCES extraction
        references = None
        m_ref = re.search(
            r"\bREFERENCES\s+([a-z_][a-z_0-9]*\.[a-z_][a-z_0-9]*"
            r"(?:\s*\([a-z_][a-z_0-9]*\))?)",
            rest, re.I,
        )
        if m_ref:
            references = m_ref.group(1).strip()

        fields.append(
            Field(
                name=col_name,
                sql_type=col_type,
                not_null=not_null or is_pk_inline,
                default=default,
                references=references,
                description=comment,
            )
        )

    return fields


def parse_canonical_sdd(text: str) -> list[Entity]:
    """Walk the SDD line-by-line, extracting entity headings and their CREATE TABLE blocks."""
    entities: list[Entity] = []
    lines = text.splitlines()
    i = 0
    current_section = ""

    while i < len(lines):
        line = lines[i]

        # Track top-level section context for nicer descriptions
        if line.startswith("# §"):
            current_section = line.lstrip("# ").strip()

        m = ENTITY_HEADING.match(line)
        if not m:
            i += 1
            continue

        schema = m.group(2)
        entity_name = m.group(3)

        # Find the next sql code fence (or the next entity heading first, meaning
        # this entity has no DDL — "preserve as-is" pattern).
        j = i + 1
        sql_block: list[str] = []
        in_sql = False
        hit_next_entity = False
        while j < len(lines):
            ln = lines[j]
            if not in_sql:
                if SQL_FENCE_OPEN.match(ln):
                    in_sql = True
                    j += 1
                    continue
                if ENTITY_HEADING.match(ln):
                    hit_next_entity = True
                    break
            else:
                if SQL_FENCE_CLOSE.match(ln):
                    # Past the closing fence — advance one and stop
                    j += 1
                    break
                sql_block.append(ln)
            j += 1

        sql = "\n".join(sql_block)
        ct = CREATE_TABLE.search(sql)
        if ct and ct.group(1) == schema and ct.group(2) == entity_name:
            fields = parse_create_table(sql[ct.start():])
            entities.append(
                Entity(
                    schema=schema,
                    name=entity_name,
                    fields=fields,
                    raw_sql=sql,
                    section=current_section,
                )
            )
        # else: heading without matching DDL — handled by SUPPLEMENTAL_ENTITIES

        # If we stopped at the next entity heading, leave i pointing at that
        # line so the outer loop re-matches it. Otherwise advance past where
        # we ended.
        i = j if hit_next_entity else max(j, i + 1)

    return entities


# ---------------------------------------------------------------------------
# OpenAPI emission
# ---------------------------------------------------------------------------

# Schema-name → human-readable tag mapping
SCHEMA_TAGS = {
    "m": ("M-Merchandising", "Master merchandising data: items, vendors, categories"),
    "l": ("A-Location", "Stores, warehouses, location hierarchy"),
    "s": ("S-Space", "Planograms, shelf positions"),
    "c": ("C-Customer", "Customer master, addresses, loyalty"),
    "e": ("L-Labor", "Employees, roles, location assignments"),
    "i": ("D-Inventory", "Inventory positions, movements, documents, lots"),
    "o": ("O-Orders", "Purchase orders, sales orders, fulfillment, allocations"),
    "p": ("P-Pricing", "Item prices, promotions, taxes"),
    "f": ("F-Finance", "Tender types, GL accounts, supplier invoices, payments"),
    "t": ("T-Transactions", "POSLog transactions, line items, tenders, drawer events"),
    "q": ("Q-Loss-Prevention", "Detection rules, detections, cases, evidence, subjects"),
    "ledger": ("Ledger-Cost-to-Serve", "Stock ledger, ILDWAC positions, RIB batches, blockchain anchors"),
    "app": ("Cross-Cutting-Platform", "Tenants, users, audit log, external identities"),
    "memory": ("Memory-Agent", "Agent memory and sessions"),
}

# Standard fields present on (almost) every canonical entity.
STANDARD_FIELDS = {"id", "tenant_id", "created_at", "updated_at"}


def schema_for_field(f: Field) -> dict:
    """Build the OpenAPI schema fragment for a single field."""
    base = map_sql_type(f.sql_type)

    # Add description if available
    desc_parts = []
    if f.description:
        desc_parts.append(f.description)
    if f.references:
        desc_parts.append(f"FK → {f.references}")
    if f.default and f.default not in {"now()", "gen_random_uuid()"}:
        # Only surface meaningful defaults; opaque function calls are noise
        desc_parts.append(f"default: {f.default}")
    if desc_parts:
        existing = base.get("description", "")
        joined = " · ".join(desc_parts)
        base["description"] = f"{existing} · {joined}".strip(" ·") if existing else joined

    # readOnly for system-managed fields
    if f.name in {"id", "created_at", "updated_at"}:
        base["readOnly"] = True

    # Make sure x-references is present for FKs (machine-readable)
    if f.references:
        base["x-references"] = f.references

    return base


def emit_entity_schemas(entity: Entity) -> dict[str, dict]:
    """Emit the four component schemas for an entity: full, create, update, list-page."""
    full_props = {}
    required = []
    for f in entity.fields:
        full_props[f.name] = schema_for_field(f)
        # required iff NOT NULL AND no default value (clients must supply it)
        if f.not_null and not f.default and f.name not in {"id", "created_at", "updated_at"}:
            required.append(f.name)

    full = {
        "type": "object",
        "description": (
            f"{entity.schema}.{entity.name} — canonical retail entity. "
            f"Section: {entity.section or 'unspecified'}."
        ),
        "properties": full_props,
    }
    if required:
        full["required"] = required

    # Create payload: omit readOnly fields (id/created_at/updated_at)
    create_props = {k: v for k, v in full_props.items() if k not in {"id", "created_at", "updated_at"}}
    create_required = [r for r in required if r not in {"id", "created_at", "updated_at"}]
    create = {
        "type": "object",
        "description": f"Create payload for {entity.schema}.{entity.name}.",
        "properties": create_props,
    }
    if create_required:
        create["required"] = create_required

    # Update payload: all fields optional, only updatable ones
    update_props = {k: v for k, v in full_props.items() if k not in {"id", "tenant_id", "created_at", "updated_at"}}
    update = {
        "type": "object",
        "description": f"Update payload for {entity.schema}.{entity.name}. All fields optional.",
        "properties": update_props,
    }

    # Page response
    page_ref = {"$ref": f"#/components/schemas/{entity.schema}_{entity.name}"}
    page = {
        "type": "object",
        "description": f"Paginated list of {entity.schema}.{entity.name}.",
        "properties": {
            "items": {"type": "array", "items": page_ref},
            "next_cursor": {
                "type": "string",
                "nullable": True,
                "description": "Opaque cursor for the next page; null when exhausted.",
            },
            "total_estimate": {
                "type": "integer",
                "description": "Approximate total matching the query.",
            },
        },
        "required": ["items"],
    }

    base = f"{entity.schema}_{entity.name}"
    return {
        base: full,
        f"{base}_Create": create,
        f"{base}_Update": update,
        f"{base}_Page": page,
    }


def emit_entity_paths(entity: Entity) -> dict[str, dict]:
    """Emit the CRUD + list paths for an entity."""
    base = f"{entity.schema}_{entity.name}"
    tag = SCHEMA_TAGS.get(entity.schema, (entity.schema.upper(), ""))[0]
    collection = f"/v1/{entity.schema}/{entity.name}"
    item = f"{collection}/{{id}}"

    paths: dict[str, dict] = {}

    paths[collection] = {
        "get": {
            "tags": [tag],
            "summary": f"List {entity.schema}.{entity.name}",
            "operationId": f"list_{base}",
            "parameters": [
                {"$ref": "#/components/parameters/Cursor"},
                {"$ref": "#/components/parameters/Limit"},
                {"$ref": "#/components/parameters/TenantId"},
            ],
            "responses": {
                "200": {
                    "description": "Paginated list",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{base}_Page"}
                        }
                    },
                },
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "402": {"$ref": "#/components/responses/PaymentRequired"},
                "429": {"$ref": "#/components/responses/RateLimited"},
            },
        },
        "post": {
            "tags": [tag],
            "summary": f"Create {entity.schema}.{entity.name}",
            "operationId": f"create_{base}",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{base}_Create"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Created",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{base}"}
                        }
                    },
                },
                "400": {"$ref": "#/components/responses/BadRequest"},
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "402": {"$ref": "#/components/responses/PaymentRequired"},
                "409": {"$ref": "#/components/responses/Conflict"},
            },
        },
    }

    paths[item] = {
        "parameters": [{"$ref": "#/components/parameters/PathId"}],
        "get": {
            "tags": [tag],
            "summary": f"Get {entity.schema}.{entity.name} by id",
            "operationId": f"get_{base}",
            "responses": {
                "200": {
                    "description": "Found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{base}"}
                        }
                    },
                },
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
        },
        "patch": {
            "tags": [tag],
            "summary": f"Update {entity.schema}.{entity.name}",
            "operationId": f"update_{base}",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{base}_Update"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Updated",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{base}"}
                        }
                    },
                },
                "400": {"$ref": "#/components/responses/BadRequest"},
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
        },
        "delete": {
            "tags": [tag],
            "summary": f"Delete (or soft-delete) {entity.schema}.{entity.name}",
            "operationId": f"delete_{base}",
            "responses": {
                "204": {"description": "Deleted"},
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
        },
    }

    return paths


# ---------------------------------------------------------------------------
# Patent-architecture endpoints (reserved — built in dedicated dispatches)
# ---------------------------------------------------------------------------

PATENT_PATHS = {
    "/v1/protocol/webhook/{source}": {
        "post": {
            "tags": ["Protocol-Patent"],
            "summary": "Universal webhook ingest (Node 2 — API Gateway)",
            "description": (
                "Per Patent Application 63/991,596, Node 2. HMAC-SHA256 verify, "
                "payload hash, queue publish, 200 OK <5ms. **Built in GRO-746.**"
            ),
            "operationId": "protocol_webhook_ingest",
            "parameters": [
                {
                    "name": "source",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": "Source network identifier (square, shopify, counterpoint, etc.)",
                }
            ],
            "responses": {
                "200": {"description": "Accepted, event hash assigned"},
                "401": {"$ref": "#/components/responses/Unauthorized"},
                "400": {"$ref": "#/components/responses/BadRequest"},
                "429": {"$ref": "#/components/responses/RateLimited"},
            },
        }
    },
    "/v1/protocol/namespace": {
        "post": {
            "tags": ["Protocol-Patent"],
            "summary": ".jeffe namespace registration (FIG. 5)",
            "description": (
                "Per Patent Application 63/991,596, FIG. 5. Inscribe namespace "
                "ordinal on Bitcoin; indexer caches with `.jeffe` suffix. "
                "**Built in GRO-751.**"
            ),
            "operationId": "protocol_namespace_register",
            "responses": {
                "202": {"description": "Inscription submitted"},
            },
        }
    },
    "/v1/protocol/evidence/{event_hash}": {
        "get": {
            "tags": ["Protocol-Patent"],
            "summary": "Bilateral verification surface (Sub 1 / L1)",
            "description": (
                "Per Patent Application 63/991,596, Sub 1 / Node 3. "
                "Returns L1 evidence record matching the event_hash. "
                "**Built in GRO-748.**"
            ),
            "operationId": "protocol_evidence_get",
            "parameters": [
                {
                    "name": "event_hash",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                }
            ],
            "responses": {
                "200": {"description": "Evidence record"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
        }
    },
    "/v1/protocol/anchor/{event_hash}": {
        "get": {
            "tags": ["Protocol-Patent"],
            "summary": "Anchor receipt (inscription_id + Merkle proof)",
            "description": (
                "Per Patent Application 63/991,596, Sub 3 / Node 5/6. Returns "
                "the Bitcoin inscription_id and Merkle proof path for an event. "
                "**Built in GRO-750.**"
            ),
            "operationId": "protocol_anchor_get",
            "parameters": [
                {
                    "name": "event_hash",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                }
            ],
            "responses": {
                "200": {"description": "Anchor receipt"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
        }
    },
    "/v1/protocol/verify/{event_hash}": {
        "get": {
            "tags": ["Protocol-Patent"],
            "summary": "L402 sat-gated verification",
            "description": (
                "Per Patent Application 63/991,596. HTTP 402 → Lightning invoice "
                "→ sat payment → cryptographic proof. **Built in GRO-752.**"
            ),
            "operationId": "protocol_verify",
            "parameters": [
                {
                    "name": "event_hash",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                }
            ],
            "responses": {
                "402": {"description": "Payment required (Lightning invoice)"},
                "200": {"description": "Verification proof"},
                "404": {"$ref": "#/components/responses/NotFound"},
            },
            "security": [{"L402SatGated": []}],
        }
    },
}


# ---------------------------------------------------------------------------
# Top-level OpenAPI document
# ---------------------------------------------------------------------------

def build_spec(entities: list[Entity]) -> dict:
    """Compose the full OpenAPI 3.0 document."""
    schemas: dict[str, dict] = {}
    paths: dict[str, dict] = {}

    # Standard reusable parameters
    parameters = {
        "PathId": {
            "name": "id",
            "in": "path",
            "required": True,
            "schema": {"type": "string", "format": "uuid"},
            "description": "Canonical entity UUID (the row's `id` column).",
        },
        "Cursor": {
            "name": "cursor",
            "in": "query",
            "required": False,
            "schema": {"type": "string"},
            "description": "Opaque cursor returned from a prior page.",
        },
        "Limit": {
            "name": "limit",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 50, "minimum": 1, "maximum": 500},
        },
        "TenantId": {
            "name": "tenant_id",
            "in": "query",
            "required": False,
            "schema": {"type": "string", "format": "uuid"},
            "description": "Restrict to a single tenant (admin contexts only).",
        },
    }

    # Standard reusable responses
    responses = {
        "BadRequest": {
            "description": "Malformed request",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
        "Unauthorized": {
            "description": "Authentication required (LNURL-auth or L402)",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
        "PaymentRequired": {
            "description": (
                "L402 payment required — server returns a Lightning invoice; "
                "client pays and retries with the macaroon + preimage."
            ),
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
        "NotFound": {
            "description": "Resource not found",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
        "Conflict": {
            "description": "Conflict (duplicate key, idempotency violation)",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
        "RateLimited": {
            "description": "Rate limit exceeded",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
        },
    }

    # Standard error schema
    schemas["Error"] = {
        "type": "object",
        "required": ["code", "message"],
        "properties": {
            "code": {"type": "string", "description": "Machine-readable error code"},
            "message": {"type": "string", "description": "Human-readable error message"},
            "details": {
                "type": "object",
                "additionalProperties": True,
                "description": "Optional structured error context",
            },
        },
    }

    # Per-entity schemas + paths
    for ent in entities:
        schemas.update(emit_entity_schemas(ent))
        paths.update(emit_entity_paths(ent))

    # Patent-architecture reserved paths
    paths.update(PATENT_PATHS)

    # Tags — domain groups + the patent reservation
    tags_seen = []
    for schema_key, (tag, desc) in SCHEMA_TAGS.items():
        if any(e.schema == schema_key for e in entities):
            tags_seen.append({"name": tag, "description": desc})
    tags_seen.append({
        "name": "Protocol-Patent",
        "description": (
            "Patent-architecture endpoints (Application 63/991,596). "
            "Reserved here; built in dedicated dispatches GRO-746 / 748 / 750 / 751 / 752."
        ),
    })

    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Canary Protocol — Canonical Retail Substrate",
            "version": "0.1.0",
            "description": (
                "Developer-facing OpenAPI 3.0 contract for the Canary Protocol "
                "canonical retail data model. Auto-generated from "
                "`docs/sdds/go-handoff/canonical-data-model.md` — do not hand-edit. "
                "Patent context: Application 63/991,596 (Universal Event Notarization). "
                "This OpenAPI surface is the developer-facing layer. The MCP-native "
                "agent surface lives at the `mcp__canary-protocol__*` tools (see "
                "GRO-741). The patent-architecture endpoints under `Protocol-Patent` "
                "are reserved here and built in their own dispatches."
            ),
            "contact": {"name": "GrowDirect, LLC"},
            "license": {
                "name": "Proprietary — Patent Pending",
                "url": "https://growdirect.io",
            },
        },
        "servers": [
            {
                "url": "https://api.canary.growdirect.io",
                "description": "Production",
            },
            {
                "url": "https://api.canary-staging.growdirect.io",
                "description": "Staging",
            },
        ],
        "tags": tags_seen,
        "paths": paths,
        "components": {
            "parameters": parameters,
            "responses": responses,
            "schemas": schemas,
            "securitySchemes": {
                "LNURLAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": (
                        "LNURL-auth wallet-derived identity. "
                        "Authorization: LNURL <linkingKey>:<signature>. "
                        "See GRO-753."
                    ),
                },
                "L402SatGated": {
                    "type": "http",
                    "scheme": "L402",
                    "description": (
                        "L402 sat-gated. Server returns 402 + Lightning invoice; "
                        "client retries with Authorization: L402 <macaroon>:<preimage>. "
                        "See GRO-752."
                    ),
                },
            },
        },
        "security": [{"LNURLAuth": []}],
    }

    return spec


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if not SDD_CANONICAL.exists():
        print(f"ERROR: SDD not found at {SDD_CANONICAL}", file=sys.stderr)
        return 1

    text = SDD_CANONICAL.read_text()
    # Append supplemental DDL for "preserve as-is" entities not defined in the SDD
    text = text + "\n\n" + SUPPLEMENTAL_DDL
    entities = parse_canonical_sdd(text)

    if not entities:
        print("ERROR: no entities parsed from SDD", file=sys.stderr)
        return 2

    spec = build_spec(entities)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(yaml.dump(spec, sort_keys=False, default_flow_style=False, width=120))

    # Summary
    by_schema: dict[str, int] = {}
    total_fields = 0
    for e in entities:
        by_schema[e.schema] = by_schema.get(e.schema, 0) + 1
        total_fields += len(e.fields)

    print(f"Parsed {len(entities)} entities ({total_fields} fields total) from {SDD_CANONICAL.name}")
    for schema, count in sorted(by_schema.items()):
        print(f"  {schema:8} {count:3} entities")
    print(f"\nWrote {OUTPUT.relative_to(REPO_ROOT)}")
    print(f"  paths:   {len(spec['paths'])}")
    print(f"  schemas: {len(spec['components']['schemas'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
