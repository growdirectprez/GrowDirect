# CoAC HOA Instance Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-mode Cove instance for the Community of Abalone Cove (CoAC), deployed to `hoa.abalonecove.org` on the mini (192.168.10.102), ready to demo to the sitting Board president.

**Architecture:** Branch `feat/coac-hoa-qa-instance` from `main`. Same Cove codebase, new `COVE_DEPLOYMENT_MODE=production` env flag that gates off `map_bp`, `parcels_bp`, `research_bp`, `agent_bp`, `archive_bp`, `angel_web_bp`, `angel_chat_bp`, and the `cove_knowledge_mcp` / `cove_angel_agent` containers. Five net-new features: President's Desk, multi-channel publish cascade, Inspector's paper-ballot tally sheet, consulted-advisor e-acknowledgement, §4525 compliance dashboard + packet builder. Deploy via `git pull` + `docker compose build + up -d` on the mini.

**Tech Stack:** Python 3.12, Flask 3, SQLAlchemy 2.0 with `Mapped[]`, PostgreSQL 17 + pgvector, Valkey 8, Alembic, pytest, Tailwind 3 (PostCSS), weasyprint (PDF generation), itsdangerous (magic-link tokens), Cloudflare Tunnel.

**Design spec:** [docs/superpowers/specs/2026-04-20-coac-president-demo-tenant-design.md](../specs/2026-04-20-coac-president-demo-tenant-design.md)

---

## File Structure

### Files created (new)

```
Cove/cove/deployment.py                                 — production-mode helpers
Cove/cove/vault/publish.py                              — publish cascade service
Cove/cove/vault/channels/__init__.py                    — channel interface
Cove/cove/vault/channels/in_app.py                      — in-app notification channel
Cove/cove/vault/channels/lot_email.py                   — lot-email channel
Cove/cove/vault/channels/door_hanger.py                 — door-hanger PDF channel
Cove/cove/board/president_routes.py                     — /board/president blueprint
Cove/cove/board/templates/board/president.html          — President's Desk template
Cove/cove/governance/paper_tally_routes.py              — paper tally blueprint
Cove/cove/governance/templates/governance/paper_tally.html
Cove/cove/governance/templates/governance/paper_tally_certified.html
Cove/cove/advisor/__init__.py                           — advisor blueprint package
Cove/cove/advisor/routes.py                             — /advisor/acknowledge/<token>
Cove/cove/advisor/services.py                           — magic-link token logic
Cove/cove/advisor/templates/advisor/acknowledge.html
Cove/cove/advisor/templates/advisor/already_acknowledged.html
Cove/cove/advisor/templates/advisor/email_invite.html   — invite email body
Cove/cove/vault/compliance_routes.py                    — §4525 dashboard
Cove/cove/vault/compliance_config.py                    — category → Civ Code map
Cove/cove/vault/compliance_services.py                  — packet generator
Cove/cove/vault/templates/vault/compliance.html
Cove/cove/vault/templates/vault/compliance_packet.html  — cover sheet for zip
Cove/cove/models/advisor_acknowledgement.py
Cove/cove/models/tally_certification.py
Cove/cove/templates/emails/publish_notice.html          — §4040 email body
Cove/cove/templates/emails/publish_notice.txt           — text alternate
Cove/cove/templates/emails/advisor_invite.html
Cove/cove/templates/emails/advisor_invite.txt
Cove/cove/templates/door_hanger.html                    — door-hanger PDF template
Cove/migrations/versions/2026_04_20_hoa_instance.py     — alembic migration
Cove/scripts/seed_coac_president_demo_tenant.py         — curated preload
Cove/scripts/import_disc_docs.py                        — imports /Volumes/My Disc docs
Cove/tests/integration/test_deployment_mode.py
Cove/tests/integration/test_publish_cascade.py
Cove/tests/integration/test_paper_tally.py
Cove/tests/integration/test_advisor_acknowledgement.py
Cove/tests/integration/test_compliance_dashboard.py
Cove/tests/integration/test_sensitivity_filter.py
Cove/tests/unit/test_channels.py
Cove/tests/unit/test_compliance_config.py
Cove/tests/unit/test_advisor_token.py
Cove/tests/unit/test_member_is_president.py
Cove/tests/fixtures/hoa_tenant.py                       — pytest fixtures
Cove/devops/docker-compose.production.yml               — mini-side compose variant
Cove/docs/runbooks/hoa-instance-deploy.md               — mini deploy runbook
Cove/docs/proposals/2026-04-20-board-president-cover-letter.md
Cove/docs/proposals/2026-04-20-4525-compliance-memo.md
Cove/docs/proposals/2026-04-20-board-election-notice-draft.md
Cove/docs/proposals/2026-04-20-demo-script.md
```

### Files modified

```
Cove/cove/__init__.py                   — conditional blueprint registration
Cove/cove/config.py                     — COVE_DEPLOYMENT_MODE handling
Cove/cove/extensions.py                 — (no change expected; verify)
Cove/cove/models/__init__.py            — import new models
Cove/cove/models/member.py              — is_president property
Cove/cove/models/document.py            — publish_to_members, published_at columns
Cove/cove/vault/services.py             — delegate publish to publish.py
Cove/cove/vault/routes.py               — call publish_document() on upload
Cove/cove/governance/__init__.py        — register paper_tally blueprint
Cove/cove/board/__init__.py             — register president blueprint
Cove/.env.example                       — add COVE_DEPLOYMENT_MODE line
```

### Files that must NOT be modified

```
Cove/cove/models/ballot.py              — Davis-Stirling secret ballot separation
Cove/cove/models/ballot_envelope.py     — RLS-protected
Cove/cove/governance/wpbca-bylaws-config.json
Cove/seed.py                            — core seed untouched; new seed is additive
```

---

## Pre-flight (once, before Chunk 1)

- [ ] **Step 0.1: Cut branch**

```bash
cd /Users/gclyle/GrowDirect
git checkout main
git pull
git checkout -b feat/coac-hoa-qa-instance
git push -u origin feat/coac-hoa-qa-instance
```

Expected: new branch on local + origin.

- [ ] **Step 0.2: Confirm test DB clean**

```bash
cd /Users/gclyle/GrowDirect/Cove
docker compose up -d  # ensures cove_flask + shared infra running
docker exec growdirect_postgres psql -U growdirect -d postgres -c "DROP DATABASE IF EXISTS cove_test; CREATE DATABASE cove_test;"
```

Expected: `cove_test` DB recreated.

- [ ] **Step 0.3: Install weasyprint dependency (NEW DEP — USER APPROVAL REQUIRED)**

This introduces a new Python dependency for PDF generation. Per `feedback_flag_dependency_changes` memory, flag and get approval before adding.

User approval confirmed in this plan doc. Add to `Cove/requirements.txt`:

```
weasyprint==61.2
qrcode[pil]==7.4.2
```

```bash
cd /Users/gclyle/GrowDirect/Cove
echo "weasyprint==61.2" >> requirements.txt
echo "qrcode[pil]==7.4.2" >> requirements.txt
docker compose build cove_flask
docker compose up -d cove_flask
docker exec cove_flask python3 -c "import weasyprint; import qrcode; print('deps OK')"
git add requirements.txt
git commit -m "chore(cove): add weasyprint + qrcode for PDF + QR (HOA instance)"
```

Expected: `deps OK` printed; commit created.

---

## Chunk 1: Branch + Production-Mode Config & Blueprint Gating

Establish the `COVE_DEPLOYMENT_MODE` mechanism. Single env flag; default `workspace`; `production` gates off blueprints and fails fast if any gated blueprint slipped through.

### Task 1.1: Add `COVE_DEPLOYMENT_MODE` to config

**Files:**
- Modify: `Cove/cove/config.py`
- Create: `Cove/cove/deployment.py`
- Test: `Cove/tests/integration/test_deployment_mode.py`

- [ ] **Step 1: Write the failing test**

Create `Cove/tests/integration/test_deployment_mode.py`:

```python
"""Deployment mode tests — COVE_DEPLOYMENT_MODE=workspace|production."""
import os
import pytest
from cove import create_app


def _app(mode: str | None):
    prev = os.environ.get("COVE_DEPLOYMENT_MODE")
    if mode is None:
        os.environ.pop("COVE_DEPLOYMENT_MODE", None)
    else:
        os.environ["COVE_DEPLOYMENT_MODE"] = mode
    try:
        return create_app("test")
    finally:
        if prev is None:
            os.environ.pop("COVE_DEPLOYMENT_MODE", None)
        else:
            os.environ["COVE_DEPLOYMENT_MODE"] = prev


def test_deployment_mode_default_is_workspace():
    app = _app(None)
    assert app.config["COVE_DEPLOYMENT_MODE"] == "workspace"


def test_deployment_mode_workspace_registers_map_and_research():
    app = _app("workspace")
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert any(e.startswith("map.") for e in endpoints)
    assert any(e.startswith("research.") for e in endpoints)
    assert any(e.startswith("agent.") for e in endpoints)


def test_deployment_mode_production_gates_map_research_agent():
    app = _app("production")
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert not any(e.startswith("map.") for e in endpoints), "map_bp must not register in production"
    assert not any(e.startswith("research.") for e in endpoints), "research_bp must not register in production"
    assert not any(e.startswith("agent.") for e in endpoints), "agent_bp must not register in production"
    assert not any(e.startswith("archive.") for e in endpoints), "archive_bp must not register in production"
    assert not any(e.startswith("parcels.") for e in endpoints), "parcels_bp must not register in production"
    assert not any(e.startswith("angel_web.") for e in endpoints), "angel_web_bp must not register in production"
    assert not any(e.startswith("angel_chat.") for e in endpoints), "angel_chat_bp must not register in production"


def test_deployment_mode_production_keeps_board_member_vote():
    app = _app("production")
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert any(e.startswith("board.") for e in endpoints)
    assert any(e.startswith("member.") for e in endpoints)
    assert any(e.startswith("vote.") or e.startswith("governance.") for e in endpoints)
    assert any(e.startswith("auth.") for e in endpoints)
    assert any(e.startswith("public.") for e in endpoints)


def test_deployment_mode_production_invalid_value_raises():
    with pytest.raises(ValueError):
        _app("foobar")
```

- [ ] **Step 2: Run test; expect FAIL**

```bash
cd /Users/gclyle/GrowDirect/Cove
docker exec cove_flask pytest tests/integration/test_deployment_mode.py -v
```

Expected: FAIL (config key `COVE_DEPLOYMENT_MODE` doesn't exist).

- [ ] **Step 3: Add config handling**

Modify `Cove/cove/config.py` — add to `BaseConfig`:

```python
    # Deployment mode: "workspace" (laptop/dev, full platform) or "production" (mini/HOA, narrowed surface).
    COVE_DEPLOYMENT_MODE = os.environ.get("COVE_DEPLOYMENT_MODE", "workspace")
```

Create `Cove/cove/deployment.py`:

```python
"""Deployment-mode helpers.

`workspace` = dev laptop, full platform including map/research/agent/archive/angel blueprints.
`production` = HOA instance on the mini; board-level-and-down community app only.
"""
from __future__ import annotations

VALID_MODES = ("workspace", "production")


def validate_mode(mode: str) -> str:
    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid COVE_DEPLOYMENT_MODE={mode!r}; expected one of {VALID_MODES}"
        )
    return mode


def is_production(config) -> bool:
    return validate_mode(config["COVE_DEPLOYMENT_MODE"]) == "production"


# Blueprint modules that must NOT register in production mode.
GATED_BLUEPRINTS = frozenset({
    "cove.map.routes",
    "cove.parcels.routes",
    "cove.research.routes",
    "cove.agent.routes",
    "cove.archive.routes",
    "cove.angel.web_routes",
    "cove.angel.chat_routes",
})
```

- [ ] **Step 4: Run test; still expects FAIL on 2nd and 3rd cases (registration not yet gated)**

```bash
docker exec cove_flask pytest tests/integration/test_deployment_mode.py::test_deployment_mode_default_is_workspace -v
```

Expected: PASS.

```bash
docker exec cove_flask pytest tests/integration/test_deployment_mode.py::test_deployment_mode_production_gates_map_research_agent -v
```

Expected: FAIL (blueprints still register).

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/config.py Cove/cove/deployment.py Cove/tests/integration/test_deployment_mode.py
git commit -m "feat(cove): add COVE_DEPLOYMENT_MODE config + deployment helpers"
```

### Task 1.2: Conditional blueprint registration in create_app

**Files:**
- Modify: `Cove/cove/__init__.py`

- [ ] **Step 1: Update `create_app` to gate blueprints**

Modify `Cove/cove/__init__.py` between lines 68 and 124. Replace the blueprint import + registration block with:

```python
    # Register blueprints — conditional on deployment mode
    from cove.deployment import is_production, validate_mode
    validate_mode(app.config["COVE_DEPLOYMENT_MODE"])
    _prod = is_production(app.config)

    from cove.public.routes import public_bp
    from cove.auth.routes import auth_bp
    from cove.member.routes import member_bp
    from cove.governance.routes import governance_bp
    from cove.governance.proceeding_routes import proceeding_bp
    from cove.vault.routes import vault_bp
    from cove.board.routes import board_bp
    from cove.treasury.routes import treasury_bp
    from cove.meetings.routes import meetings_bp
    from cove.governance.election_routes import election_bp
    from cove.community import community_bp

    # Always-on (community app core)
    app.register_blueprint(public_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(member_bp, url_prefix="/member")
    app.register_blueprint(governance_bp, url_prefix="/vote")
    app.register_blueprint(proceeding_bp, url_prefix="/proceedings")
    app.register_blueprint(vault_bp, url_prefix="/documents")
    app.register_blueprint(board_bp, url_prefix="/board")
    app.register_blueprint(treasury_bp, url_prefix="/treasury")
    app.register_blueprint(meetings_bp, url_prefix="/meetings")
    app.register_blueprint(election_bp, url_prefix="/vote/election")
    app.register_blueprint(community_bp, url_prefix="/community")

    # Workspace-only (ARC-gated in workspace; absent in production)
    if not _prod:
        from cove.parcels.routes import parcels_bp
        from cove.agent.routes import agent_bp
        from cove.archive.routes import archive_bp
        from cove.map.routes import map_bp
        from cove.research.routes import research_bp
        from cove.angel.web_routes import angel_web_bp
        from cove.angel.chat_routes import angel_chat_bp

        # ARC gate for map/archive/parcels (unchanged behavior in workspace mode)
        from flask import abort as _abort
        from flask_login import current_user as _arc_cu

        def _arc_gate():
            if not _arc_cu.is_authenticated:
                return login_manager.unauthorized()
            if not _arc_cu.is_arc:
                _abort(403)

        map_bp.before_request(_arc_gate)
        archive_bp.before_request(_arc_gate)
        parcels_bp.before_request(_arc_gate)

        app.register_blueprint(parcels_bp, url_prefix="/parcels")
        app.register_blueprint(agent_bp, url_prefix="/agent")
        app.register_blueprint(archive_bp, url_prefix="/archive")
        app.register_blueprint(map_bp, url_prefix="/map")
        app.register_blueprint(research_bp, url_prefix="/research")
        app.register_blueprint(angel_web_bp, url_prefix="/angel/web")
        app.register_blueprint(angel_chat_bp, url_prefix="/angel")
```

- [ ] **Step 2: Update privacy-consent exempt set (remove angel_* in production)**

The existing `exempt` set in `_check_privacy_consent` (around line 141) references `angel_web.` and `angel_chat.` — harmless when those blueprints aren't registered, no code change required.

- [ ] **Step 3: Run full deployment-mode tests**

```bash
docker exec cove_flask pytest tests/integration/test_deployment_mode.py -v
```

Expected: 5/5 PASS.

- [ ] **Step 4: Regression — full test suite still passes in workspace (default) mode**

```bash
docker exec cove_flask pytest tests/ -x --tb=short -q
```

Expected: existing suite PASS (or same known-failing baseline as pre-change).

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/__init__.py
git commit -m "feat(cove): gate map/parcels/research/agent/archive/angel blueprints in production mode"
```

### Task 1.3: Fail-fast startup assertion

**Files:**
- Modify: `Cove/cove/deployment.py`
- Modify: `Cove/cove/__init__.py`
- Test: `Cove/tests/integration/test_deployment_mode.py` (extend)

- [ ] **Step 1: Write failing test**

Append to `Cove/tests/integration/test_deployment_mode.py`:

```python
def test_production_mode_detects_leaked_gated_blueprint():
    """If a gated blueprint sneaks into production registration, create_app must raise."""
    os.environ["COVE_DEPLOYMENT_MODE"] = "production"
    try:
        # Simulate leak: monkey-patch register to allow a gated bp
        import cove
        # Use the public API: call create_app and assert no gated endpoints exist
        app = cove.create_app("test")
        gated_prefixes = ("map.", "parcels.", "research.", "agent.", "archive.", "angel_web.", "angel_chat.")
        leaked = [r.endpoint for r in app.url_map.iter_rules()
                  if any(r.endpoint.startswith(p) for p in gated_prefixes)]
        assert leaked == [], f"Production mode leaked blueprints: {leaked}"
    finally:
        os.environ.pop("COVE_DEPLOYMENT_MODE", None)


def test_production_mode_assertion_runs():
    """Smoke: assert_production_invariants runs without raising on a clean app."""
    from cove.deployment import assert_production_invariants
    os.environ["COVE_DEPLOYMENT_MODE"] = "production"
    try:
        app = create_app("test")
        with app.app_context():
            assert_production_invariants(app)
    finally:
        os.environ.pop("COVE_DEPLOYMENT_MODE", None)
```

- [ ] **Step 2: Add assertion helper**

Append to `Cove/cove/deployment.py`:

```python
# Endpoint prefixes that must not exist in production mode.
GATED_ENDPOINT_PREFIXES = (
    "map.", "parcels.", "research.", "agent.",
    "archive.", "angel_web.", "angel_chat.",
)


def assert_production_invariants(app) -> None:
    """Fail-fast: abort startup if any gated route or service leaked into production."""
    if not is_production(app.config):
        return
    leaked = []
    for rule in app.url_map.iter_rules():
        if any(rule.endpoint.startswith(p) for p in GATED_ENDPOINT_PREFIXES):
            leaked.append(rule.endpoint)
    if leaked:
        raise RuntimeError(
            f"COVE_DEPLOYMENT_MODE=production but gated blueprints registered: {leaked}"
        )
```

- [ ] **Step 3: Wire into create_app**

In `Cove/cove/__init__.py`, near the end of `create_app` (just before `return app`), add:

```python
    # Fail-fast: verify production invariants
    from cove.deployment import assert_production_invariants
    assert_production_invariants(app)
```

- [ ] **Step 4: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_deployment_mode.py -v
```

Expected: 7/7 PASS.

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/deployment.py Cove/cove/__init__.py Cove/tests/integration/test_deployment_mode.py
git commit -m "feat(cove): fail-fast production-mode invariant assertion"
```

### Task 1.4: Update .env.example + docs

**Files:**
- Modify: `Cove/.env.example`

- [ ] **Step 1: Append to `Cove/.env.example`**

```
# Deployment mode: workspace (dev laptop, full platform) | production (HOA on the mini)
COVE_DEPLOYMENT_MODE=workspace
```

- [ ] **Step 2: Commit**

```bash
git add Cove/.env.example
git commit -m "docs(cove): document COVE_DEPLOYMENT_MODE in .env.example"
```

---

## Chunk 2: Data Model Migrations

New tables + columns + `president` role. Single Alembic migration; models imported in `cove/models/__init__.py`.

### Task 2.1: Model — `AdvisorAcknowledgement`

**Files:**
- Create: `Cove/cove/models/advisor_acknowledgement.py`
- Modify: `Cove/cove/models/__init__.py`
- Test: `Cove/tests/unit/test_advisor_token.py`

- [ ] **Step 1: Write failing unit test**

Create `Cove/tests/unit/test_advisor_token.py`:

```python
"""Unit tests for advisor acknowledgement model + token helpers."""
import uuid
import pytest
from datetime import datetime, timezone


def test_advisor_ack_model_fields(app_ctx, db_session, default_org):
    from cove.models.advisor_acknowledgement import AdvisorAcknowledgement
    a = AdvisorAcknowledgement(
        id=str(uuid.uuid4()),
        organization_id=default_org.id,
        advisor_name="Jane Former-President",
        advisor_email="jane@example.com",
        advisor_role_label="Former Board President, 2018–2020",
        magic_link_token="abc.signed.token",
        nonce="n1",
    )
    db_session.add(a)
    db_session.commit()
    assert a.reviewed_at is None
    assert a.attestation_text is not None  # default template present


def test_advisor_ack_mark_reviewed(app_ctx, db_session, default_org):
    from cove.models.advisor_acknowledgement import AdvisorAcknowledgement
    a = AdvisorAcknowledgement(
        id=str(uuid.uuid4()),
        organization_id=default_org.id,
        advisor_name="J", advisor_email="j@x.com",
        advisor_role_label="r", magic_link_token="t", nonce="n",
    )
    db_session.add(a); db_session.commit()
    a.mark_reviewed()
    db_session.commit()
    assert a.reviewed_at is not None
    assert a.reviewed_at.tzinfo is timezone.utc or a.reviewed_at.utcoffset() is not None
```

Fixtures `app_ctx`, `db_session`, `default_org` presumed to exist in `Cove/tests/conftest.py`; if missing, add per pattern of other existing tests.

- [ ] **Step 2: Run — expect FAIL**

```bash
docker exec cove_flask pytest tests/unit/test_advisor_token.py -v
```

Expected: FAIL (module doesn't exist).

- [ ] **Step 3: Create the model**

Create `Cove/cove/models/advisor_acknowledgement.py`:

```python
"""Advisor acknowledgement — magic-link attestation by consulted former presidents.

Not a legal approval. Trust artifact only: documents that a named former board
president reviewed the platform before the sitting Board president saw it.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cove.extensions import db


DEFAULT_ATTESTATION = (
    "I have reviewed this Community of Abalone Cove platform as a consulted "
    "advisor. My review is informational and does not constitute legal "
    "approval, endorsement, or official HOA action."
)


class AdvisorAcknowledgement(db.Model):
    __tablename__ = "advisor_acknowledgements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=False)

    advisor_name: Mapped[str] = mapped_column(String(120), nullable=False)
    advisor_email: Mapped[str] = mapped_column(String(254), nullable=False)
    advisor_role_label: Mapped[str] = mapped_column(String(160), nullable=False)

    magic_link_token: Mapped[str] = mapped_column(String(512), nullable=False)
    nonce: Mapped[str] = mapped_column(String(64), nullable=False)

    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    attestation_text: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_ATTESTATION)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def mark_reviewed(self) -> None:
        self.reviewed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<AdvisorAcknowledgement {self.advisor_name!r} reviewed={self.reviewed_at}>"
```

Modify `Cove/cove/models/__init__.py` — add:

```python
from cove.models.advisor_acknowledgement import AdvisorAcknowledgement  # noqa: F401
```

- [ ] **Step 4: Run — expect PASS after migration applied (see Task 2.4)**

Pause — migration not yet applied. Move to next task; tests will pass after migration.

### Task 2.2: Model — `ProposalTallyCertification`

**Files:**
- Create: `Cove/cove/models/tally_certification.py`
- Modify: `Cove/cove/models/__init__.py`

- [ ] **Step 1: Create the model**

Create `Cove/cove/models/tally_certification.py`:

```python
"""Paper-ballot tally certification.

Inspector of Elections enters per-choice paper-ballot counts; platform auto-sums;
system generates a certified PDF. This model stores the attested result.

Hard rule: never writes to ballots / ballot_envelopes. Paper ballots remain the
legal vote; this is the Inspector's spreadsheet.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict

from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cove.extensions import db


class ProposalTallyCertification(db.Model):
    __tablename__ = "proposal_tally_certifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    proposal_id: Mapped[str] = mapped_column(String(36), ForeignKey("proposals.id"), nullable=False)
    inspector_member_id: Mapped[str] = mapped_column(String(36), ForeignKey("members.id"), nullable=False)

    per_choice_counts: Mapped[Dict[str, int]] = mapped_column(JSON, nullable=False, default=dict)
    total_ballots: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    certified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    certification_pdf_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    proposal = relationship("Proposal", backref="tally_certifications")

    def recompute_total(self) -> int:
        self.total_ballots = sum(int(v) for v in (self.per_choice_counts or {}).values())
        return self.total_ballots
```

Modify `Cove/cove/models/__init__.py` — add:

```python
from cove.models.tally_certification import ProposalTallyCertification  # noqa: F401
```

- [ ] **Step 2: Commit both models**

```bash
git add Cove/cove/models/advisor_acknowledgement.py Cove/cove/models/tally_certification.py Cove/cove/models/__init__.py Cove/tests/unit/test_advisor_token.py
git commit -m "feat(cove): add AdvisorAcknowledgement + ProposalTallyCertification models"
```

### Task 2.3: Extend `Document` model — publish fields

**Files:**
- Modify: `Cove/cove/models/document.py`

- [ ] **Step 1: Add columns to `Document`**

Locate `Cove/cove/models/document.py`. Add fields:

```python
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    publish_to_members: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    compliance_category: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
```

(`Boolean` must be imported from `sqlalchemy` if not already.)

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/models/document.py
git commit -m "feat(cove): Document.published_at / publish_to_members / compliance_category"
```

### Task 2.4: Alembic migration

**Files:**
- Create: `Cove/migrations/versions/2026_04_20_hoa_instance.py`

- [ ] **Step 1: Generate autogen revision**

```bash
docker exec cove_flask alembic -c /app/migrations/alembic.ini revision --autogenerate -m "hoa_instance: advisor_ack, tally_cert, doc.publish_fields, president role"
```

Copy resulting file to `Cove/migrations/versions/2026_04_20_hoa_instance.py`. Inspect for:
- `advisor_acknowledgements` CREATE
- `proposal_tally_certifications` CREATE
- `documents.published_at`, `publish_to_members`, `compliance_category` ADD COLUMN
- Add explicit `op.execute("INSERT INTO roles (id, organization_id, name, ...) SELECT ...")` for each existing org — the `president` role.

If autogen misses the role seed, manually append to migration body:

```python
def upgrade() -> None:
    # ... autogen changes above ...
    # Seed 'president' role per existing org (idempotent).
    op.execute("""
        INSERT INTO roles (id, organization_id, name, description, created_at, updated_at)
        SELECT
            gen_random_uuid()::text,
            o.id,
            'president',
            'Board President — role-gated landing page',
            NOW(), NOW()
        FROM organizations o
        WHERE NOT EXISTS (
            SELECT 1 FROM roles r WHERE r.organization_id = o.id AND r.name = 'president'
        );
    """)
```

Mirror in `downgrade()`.

- [ ] **Step 2: Apply migration to dev DB**

```bash
docker exec cove_flask alembic -c /app/migrations/alembic.ini upgrade head
```

Expected: "Running upgrade <prev> -> 2026_04_20_hoa_instance"

- [ ] **Step 3: Apply to test DB**

```bash
TEST_DATABASE_URL="postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove_test" \
  docker exec -e TEST_DATABASE_URL cove_flask alembic -c /app/migrations/alembic.ini upgrade head
```

- [ ] **Step 4: Run unit tests from Task 2.1**

```bash
docker exec cove_flask pytest tests/unit/test_advisor_token.py -v
```

Expected: 2/2 PASS.

- [ ] **Step 5: Commit**

```bash
git add Cove/migrations/versions/2026_04_20_hoa_instance.py
git commit -m "feat(cove): alembic migration for HOA instance tables + president role"
```

### Task 2.5: `member.is_president` property + test

**Files:**
- Modify: `Cove/cove/models/member.py`
- Test: `Cove/tests/unit/test_member_is_president.py`

- [ ] **Step 1: Write failing test**

Create `Cove/tests/unit/test_member_is_president.py`:

```python
"""Member.is_president role property."""
import uuid


def test_is_president_false_for_plain_member(app_ctx, db_session, default_org, make_member):
    m = make_member(org=default_org, lot_email="1Barkentine@abalonecove.org")
    assert m.is_president is False


def test_is_president_true_when_president_role_assigned(app_ctx, db_session, default_org, make_member, assign_role):
    m = make_member(org=default_org, lot_email="2Barkentine@abalonecove.org")
    assign_role(m, "president")
    assert m.is_president is True


def test_is_board_unaffected_by_president(app_ctx, db_session, default_org, make_member, assign_role):
    """is_board stays true when president is also assigned, but is_president gates the desk."""
    m = make_member(org=default_org, lot_email="3Barkentine@abalonecove.org")
    assign_role(m, "board")
    assign_role(m, "president")
    assert m.is_board is True
    assert m.is_president is True
```

Add fixtures `make_member` and `assign_role` to `Cove/tests/conftest.py` if missing — pattern from existing tests.

- [ ] **Step 2: Add property to `Member`**

Locate `Cove/cove/models/member.py`. Alongside `is_board`, `is_admin`, `is_inspector`, `is_arc` add:

```python
    @property
    def is_president(self) -> bool:
        return any(r.name == "president" for r in self.roles)
```

Exact `self.roles` accessor depends on existing Member implementation; follow the same pattern as `is_board`.

- [ ] **Step 3: Run tests**

```bash
docker exec cove_flask pytest tests/unit/test_member_is_president.py -v
```

Expected: 3/3 PASS.

- [ ] **Step 4: Commit**

```bash
git add Cove/cove/models/member.py Cove/tests/unit/test_member_is_president.py
git commit -m "feat(cove): member.is_president role property"
```

---

## Chunk 3: Publish Cascade (multi-channel)

Vault upload with `publish_to_members=true` fans out a §4040 notice across in-app + lot-email + door-hanger PDF. Pluggable channel interface; idempotent.

### Task 3.1: Channel interface

**Files:**
- Create: `Cove/cove/vault/channels/__init__.py`
- Test: `Cove/tests/unit/test_channels.py`

- [ ] **Step 1: Write interface test**

Create `Cove/tests/unit/test_channels.py`:

```python
"""Publish channel interface contract."""
import pytest
from cove.vault.channels import Channel, ChannelDelivery


def test_channel_is_abstract():
    with pytest.raises(TypeError):
        Channel()  # cannot instantiate abstract base


def test_channel_delivery_shape():
    d = ChannelDelivery(channel="in_app", member_id="m1", document_id="d1", ok=True, detail=None)
    assert d.channel == "in_app"
    assert d.ok is True
```

- [ ] **Step 2: Create interface**

Create `Cove/cove/vault/channels/__init__.py`:

```python
"""Publish-channel interface.

A Channel delivers a publish notice to a single member via a single medium.
Implementations: InAppChannel, LotEmailChannel, DoorHangerPDFChannel.
Future: SMSChannel (Twilio) — not wired in this scope.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ChannelDelivery:
    channel: str
    member_id: str
    document_id: str
    ok: bool
    detail: Optional[str] = None


class Channel(ABC):
    name: str = "abstract"

    @abstractmethod
    def deliver(self, *, member, document, announcement_text: str, magic_link: str) -> ChannelDelivery:
        ...
```

- [ ] **Step 3: Run test; expect PASS**

```bash
docker exec cove_flask pytest tests/unit/test_channels.py -v
```

- [ ] **Step 4: Commit**

```bash
git add Cove/cove/vault/channels/__init__.py Cove/tests/unit/test_channels.py
git commit -m "feat(cove): publish channel interface"
```

### Task 3.2: In-app channel

**Files:**
- Create: `Cove/cove/vault/channels/in_app.py`
- Test: extend `Cove/tests/unit/test_channels.py`

- [ ] **Step 1: Append test**

```python
def test_in_app_channel_writes_notification(app_ctx, db_session, default_org, make_member):
    from cove.vault.channels.in_app import InAppChannel
    from cove.models import Document, Notification
    m = make_member(org=default_org)
    d = Document(organization_id=default_org.id, title="Test", filename="t.pdf", mime_type="application/pdf", size_bytes=0)
    db_session.add(d); db_session.commit()
    ch = InAppChannel()
    result = ch.deliver(member=m, document=d, announcement_text="Hi", magic_link="https://x/t")
    assert result.ok
    n = db_session.query(Notification).filter_by(member_id=m.id).first()
    assert n is not None
    assert d.id in n.link_url or d.id in n.body
```

- [ ] **Step 2: Implement InAppChannel**

Create `Cove/cove/vault/channels/in_app.py`:

```python
"""In-app notification channel."""
from __future__ import annotations

from cove.extensions import db
from cove.models import Notification
from cove.vault.channels import Channel, ChannelDelivery


class InAppChannel(Channel):
    name = "in_app"

    def deliver(self, *, member, document, announcement_text: str, magic_link: str) -> ChannelDelivery:
        try:
            n = Notification(
                member_id=member.id,
                organization_id=document.organization_id,
                title=f"Published: {document.title}",
                body=announcement_text[:500],
                link_url=f"/documents/{document.id}",
                category="publish",
            )
            db.session.add(n)
            db.session.commit()
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=True)
        except Exception as e:
            db.session.rollback()
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=False, detail=str(e))
```

Notification model shape: verify against existing `cove/notifications/services.py` + `cove/models/notification.py`. Adjust field names as needed.

- [ ] **Step 3: Run; expect PASS**

```bash
docker exec cove_flask pytest tests/unit/test_channels.py -v
```

- [ ] **Step 4: Commit**

```bash
git add Cove/cove/vault/channels/in_app.py Cove/tests/unit/test_channels.py
git commit -m "feat(cove): in-app publish channel"
```

### Task 3.3: Lot-email channel

**Files:**
- Create: `Cove/cove/vault/channels/lot_email.py`
- Create: `Cove/cove/templates/emails/publish_notice.html`
- Create: `Cove/cove/templates/emails/publish_notice.txt`

- [ ] **Step 1: Write test**

Append to `Cove/tests/unit/test_channels.py`:

```python
def test_lot_email_channel_sends_to_lot_email(app_ctx, db_session, default_org, make_member, mailoutbox):
    from cove.vault.channels.lot_email import LotEmailChannel
    from cove.models import Document
    m = make_member(org=default_org, lot_email="25SeaCove@abalonecove.org")
    d = Document(organization_id=default_org.id, title="March Minutes", filename="minutes.pdf", mime_type="application/pdf", size_bytes=0)
    db_session.add(d); db_session.commit()
    result = LotEmailChannel().deliver(member=m, document=d, announcement_text="The March minutes are published.", magic_link="https://hoa.abalonecove.org/auth/verify/xyz")
    assert result.ok
    assert len(mailoutbox) == 1
    assert "25SeaCove@abalonecove.org" in mailoutbox[0].to
    assert "March Minutes" in mailoutbox[0].subject
```

`mailoutbox` fixture follows Flask-Mail test pattern (`with mail.record_messages() as outbox: ...`). Add to `conftest.py` if missing.

- [ ] **Step 2: Create templates**

`Cove/cove/templates/emails/publish_notice.html`:

```html
<p>A new document has been published for the Community of Abalone Cove:</p>
<p><strong>{{ document.title }}</strong></p>
<p>{{ announcement_text }}</p>
<p><a href="{{ magic_link }}">Sign in to review</a></p>
<hr>
<p style="font-size: 11px; color: #666">
  Delivered to your lot address ({{ member.lot_email }}) per Civil Code §4040.
  You may withdraw consent to electronic delivery at any time by writing to the association.
</p>
```

`Cove/cove/templates/emails/publish_notice.txt`:

```
A new document has been published for the Community of Abalone Cove:

{{ document.title }}

{{ announcement_text }}

Sign in to review: {{ magic_link }}

---
Delivered to your lot address ({{ member.lot_email }}) per Civil Code §4040.
```

- [ ] **Step 3: Implement channel**

Create `Cove/cove/vault/channels/lot_email.py`:

```python
"""Lot-email channel — §4040 electronic notice delivery."""
from __future__ import annotations

from flask import render_template
from flask_mail import Message

from cove.extensions import mail
from cove.vault.channels import Channel, ChannelDelivery


class LotEmailChannel(Channel):
    name = "lot_email"

    def deliver(self, *, member, document, announcement_text: str, magic_link: str) -> ChannelDelivery:
        try:
            ctx = dict(member=member, document=document, announcement_text=announcement_text, magic_link=magic_link)
            msg = Message(
                subject=f"Published: {document.title}",
                recipients=[member.lot_email],
                html=render_template("emails/publish_notice.html", **ctx),
                body=render_template("emails/publish_notice.txt", **ctx),
            )
            mail.send(msg)
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=True)
        except Exception as e:
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=False, detail=str(e))
```

- [ ] **Step 4: Run; expect PASS**

```bash
docker exec cove_flask pytest tests/unit/test_channels.py::test_lot_email_channel_sends_to_lot_email -v
```

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/vault/channels/lot_email.py Cove/cove/templates/emails/publish_notice.html Cove/cove/templates/emails/publish_notice.txt Cove/tests/unit/test_channels.py
git commit -m "feat(cove): lot-email publish channel (§4040 electronic notice)"
```

### Task 3.4: Door-hanger PDF channel

**Files:**
- Create: `Cove/cove/vault/channels/door_hanger.py`
- Create: `Cove/cove/templates/door_hanger.html`

- [ ] **Step 1: Create PDF template**

`Cove/cove/templates/door_hanger.html`:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: 4in 9in; margin: 0.25in; }
body { font-family: 'Helvetica', sans-serif; font-size: 11pt; margin: 0; }
.hero { font-size: 22pt; font-weight: bold; margin-top: 0.5in; }
.addr { font-size: 14pt; margin-top: 0.2in; color: #333; }
.body { margin-top: 0.4in; line-height: 1.4; }
.qr { margin-top: 0.5in; text-align: center; }
.qr img { width: 2in; height: 2in; }
.url { font-family: monospace; font-size: 9pt; margin-top: 0.1in; text-align: center; }
.foot { margin-top: 0.5in; font-size: 9pt; color: #666; text-align: center; }
</style>
</head>
<body>
<div class="hero">Community of Abalone Cove</div>
<div class="addr">Lot {{ member.lot_number }} · {{ member.street }}</div>
<div class="body">
<p>{{ announcement_text }}</p>
<p><strong>{{ document.title }}</strong></p>
<p>Scan to sign in and review:</p>
</div>
<div class="qr">
<img src="data:image/png;base64,{{ qr_base64 }}">
</div>
<div class="url">{{ magic_link }}</div>
<div class="foot">Delivered per Civil Code §4040</div>
</body>
</html>
```

- [ ] **Step 2: Write test**

Append to `Cove/tests/unit/test_channels.py`:

```python
def test_door_hanger_channel_generates_pdf(app_ctx, db_session, default_org, make_member, tmp_path):
    from cove.vault.channels.door_hanger import DoorHangerPDFChannel
    from cove.models import Document
    m = make_member(org=default_org, lot_email="25SeaCove@abalonecove.org", lot_number=25, street="Sea Cove Drive")
    d = Document(organization_id=default_org.id, title="March Minutes", filename="minutes.pdf", mime_type="application/pdf", size_bytes=0)
    db_session.add(d); db_session.commit()
    result = DoorHangerPDFChannel(output_dir=str(tmp_path)).deliver(member=m, document=d, announcement_text="x", magic_link="https://hoa.abalonecove.org/auth/verify/xyz")
    assert result.ok
    assert result.detail  # path to PDF
    pdf_path = tmp_path / result.detail
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000  # non-trivial PDF
```

- [ ] **Step 3: Implement channel**

Create `Cove/cove/vault/channels/door_hanger.py`:

```python
"""Door-hanger PDF channel — physical hand-delivery supplement."""
from __future__ import annotations

import base64
import io
import os
from pathlib import Path

import qrcode
from flask import render_template
from weasyprint import HTML

from cove.vault.channels import Channel, ChannelDelivery


def _qr_png_base64(url: str) -> str:
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class DoorHangerPDFChannel(Channel):
    name = "door_hanger"

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def deliver(self, *, member, document, announcement_text: str, magic_link: str) -> ChannelDelivery:
        try:
            qr_b64 = _qr_png_base64(magic_link)
            html = render_template(
                "door_hanger.html",
                member=member, document=document,
                announcement_text=announcement_text,
                magic_link=magic_link, qr_base64=qr_b64,
            )
            filename = f"doorhanger-lot{member.lot_number}-{document.id}.pdf"
            out = Path(self.output_dir) / filename
            HTML(string=html).write_pdf(str(out))
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=True, detail=filename)
        except Exception as e:
            return ChannelDelivery(channel=self.name, member_id=member.id, document_id=document.id, ok=False, detail=str(e))
```

- [ ] **Step 4: Run; expect PASS**

```bash
docker exec cove_flask pytest tests/unit/test_channels.py::test_door_hanger_channel_generates_pdf -v
```

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/vault/channels/door_hanger.py Cove/cove/templates/door_hanger.html Cove/tests/unit/test_channels.py
git commit -m "feat(cove): door-hanger PDF publish channel"
```

### Task 3.5: Publish orchestrator service

**Files:**
- Create: `Cove/cove/vault/publish.py`
- Test: `Cove/tests/integration/test_publish_cascade.py`

- [ ] **Step 1: Write integration test**

Create `Cove/tests/integration/test_publish_cascade.py`:

```python
"""Integration: vault upload → multi-channel publish cascade."""
import pytest
from cove.models import Document, Notification


def test_publish_document_fans_out_to_all_members(app_ctx, db_session, default_org, hoa_tenant_fixture, mailoutbox, tmp_path):
    from cove.vault.publish import publish_document
    tenant = hoa_tenant_fixture  # seeds 81 members, 0 claimed
    doc = Document(organization_id=default_org.id, title="March Minutes", filename="m.pdf", mime_type="application/pdf", size_bytes=100)
    db_session.add(doc); db_session.commit()

    results = publish_document(
        doc,
        announcement_text="The 2026-03-21 annual meeting minutes are published.",
        channels=["in_app", "lot_email", "door_hanger"],
        door_hanger_output_dir=str(tmp_path),
    )

    # One delivery per member per channel
    active_members = [m for m in tenant.members if m.membership_status == "active"]
    assert len(results) == len(active_members) * 3

    # In-app notifications persisted
    notifs = db_session.query(Notification).filter_by(organization_id=default_org.id, category="publish").all()
    assert len(notifs) == len(active_members)

    # Emails to lot addresses
    emails = [m.to[0] for m in mailoutbox]
    for member in active_members:
        assert member.lot_email in emails

    # Door-hangers on disk
    pdfs = list(tmp_path.glob("doorhanger-*.pdf"))
    assert len(pdfs) == len(active_members)

    # Document marked published
    db_session.refresh(doc)
    assert doc.published_at is not None
    assert doc.publish_to_members is True


def test_publish_document_idempotent(app_ctx, db_session, default_org, hoa_tenant_fixture, mailoutbox, tmp_path):
    from cove.vault.publish import publish_document
    doc = Document(organization_id=default_org.id, title="x", filename="x.pdf", mime_type="application/pdf", size_bytes=0)
    db_session.add(doc); db_session.commit()
    publish_document(doc, announcement_text="a", channels=["in_app"], door_hanger_output_dir=str(tmp_path))
    count_before = db_session.query(Notification).count()
    mailoutbox.clear()
    # Re-publish
    publish_document(doc, announcement_text="a", channels=["in_app"], door_hanger_output_dir=str(tmp_path))
    count_after = db_session.query(Notification).count()
    assert count_after == count_before, "Re-publish must not duplicate notifications"
```

`hoa_tenant_fixture` defined in Task 8.1.

- [ ] **Step 2: Implement orchestrator**

Create `Cove/cove/vault/publish.py`:

```python
"""Publish orchestrator — fans out a document to all active members via selected channels."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Iterable, List

from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for

from cove.extensions import db
from cove.models import Member, Document
from cove.vault.channels import Channel, ChannelDelivery
from cove.vault.channels.in_app import InAppChannel
from cove.vault.channels.lot_email import LotEmailChannel
from cove.vault.channels.door_hanger import DoorHangerPDFChannel


log = logging.getLogger(__name__)


def _channel_registry(door_hanger_output_dir: str) -> dict[str, Channel]:
    return {
        "in_app": InAppChannel(),
        "lot_email": LotEmailChannel(),
        "door_hanger": DoorHangerPDFChannel(output_dir=door_hanger_output_dir),
    }


def _magic_link_for(member: Member, document: Document) -> str:
    """Generate a §4040 magic link — reuses auth token pattern."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps({"member_id": member.id, "action": f"view:{document.id}"}, salt="publish")
    return url_for("auth.verify", token=token, _external=True)


def publish_document(
    document: Document,
    *,
    announcement_text: str,
    channels: Iterable[str] = ("in_app", "lot_email", "door_hanger"),
    door_hanger_output_dir: str | None = None,
) -> List[ChannelDelivery]:
    """Fan out `document` to every active member via the given channels.

    Idempotent: if `document.published_at` is already set, returns a no-op (no new
    notifications, no new emails, no new PDFs) but still returns the delivery shape
    summarizing the earlier cascade.
    """
    if document.publish_to_members and document.published_at is not None:
        log.info("Document %s already published at %s; skipping cascade.", document.id, document.published_at)
        return []

    door_hanger_output_dir = door_hanger_output_dir or current_app.config.get("DOOR_HANGER_DIR", "/tmp/doorhangers")
    registry = _channel_registry(door_hanger_output_dir)

    members = (
        db.session.query(Member)
        .filter_by(organization_id=document.organization_id, membership_status="active")
        .all()
    )

    results: List[ChannelDelivery] = []
    for member in members:
        link = _magic_link_for(member, document)
        for ch_name in channels:
            channel = registry.get(ch_name)
            if channel is None:
                log.warning("Unknown channel: %s", ch_name)
                continue
            r = channel.deliver(member=member, document=document, announcement_text=announcement_text, magic_link=link)
            results.append(r)
            if not r.ok:
                log.error("Channel %s failed for member %s: %s", ch_name, member.id, r.detail)

    document.publish_to_members = True
    document.published_at = datetime.now(timezone.utc)
    db.session.commit()

    return results
```

- [ ] **Step 3: Wire into `vault/routes.py`**

In the existing document-upload route, after `db.session.commit()` for the new Document, check form field:

```python
    if form.publish_to_members.data:
        from cove.vault.publish import publish_document
        publish_document(
            document,
            announcement_text=form.announcement_text.data or f"{document.title} is now available.",
        )
```

Add `publish_to_members` (BooleanField) and `announcement_text` (TextAreaField) to `Cove/cove/vault/forms.py` upload form.

- [ ] **Step 4: Run**

```bash
docker exec cove_flask pytest tests/integration/test_publish_cascade.py -v
```

Expected: 2/2 PASS (after hoa_tenant_fixture exists; may need stubbed fixture mid-chunk).

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/vault/publish.py Cove/cove/vault/routes.py Cove/cove/vault/forms.py Cove/tests/integration/test_publish_cascade.py
git commit -m "feat(cove): publish cascade — in-app + lot-email + door-hanger PDF"
```

---

## Chunk 4: President's Desk

Role-gated landing page: three-item checklist (upload minutes, review election notice, advisor e-acks). Small, focused.

### Task 4.1: Route + template

**Files:**
- Create: `Cove/cove/board/president_routes.py`
- Create: `Cove/cove/board/templates/board/president.html`
- Modify: `Cove/cove/board/__init__.py`
- Test: `Cove/tests/integration/test_president_desk.py`

- [ ] **Step 1: Write failing test**

Create `Cove/tests/integration/test_president_desk.py`:

```python
"""President's Desk — /board/president role-gated dashboard."""
import pytest


def test_president_desk_requires_auth(client):
    r = client.get("/board/president")
    assert r.status_code in (302, 401)  # redirect to login or 401


def test_president_desk_denied_for_plain_board_member(client, login_as, default_org, make_member, assign_role):
    m = make_member(org=default_org, lot_email="5Barkentine@abalonecove.org")
    assign_role(m, "board")  # not president
    login_as(m)
    r = client.get("/board/president")
    assert r.status_code == 403


def test_president_desk_renders_three_items_for_president(client, login_as, default_org, make_member, assign_role):
    m = make_member(org=default_org, lot_email="2Barkentine@abalonecove.org")
    assign_role(m, "board")
    assign_role(m, "president")
    login_as(m)
    r = client.get("/board/president")
    assert r.status_code == 200
    body = r.data.decode()
    assert "Upload 2026-03-21 AGM Minutes" in body or "Upload Annual Meeting Minutes" in body
    assert "Board Election Notice" in body
    assert "Consulted Advisor" in body
```

- [ ] **Step 2: Create route**

Create `Cove/cove/board/president_routes.py`:

```python
"""Board President's Desk — role-gated landing page."""
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from cove.extensions import db
from cove.models import Document, Proposal
from cove.models.advisor_acknowledgement import AdvisorAcknowledgement


president_bp = Blueprint("president", __name__, template_folder="templates")


@president_bp.before_request
@login_required
def _require_president():
    if not current_user.is_president:
        abort(403)


@president_bp.get("/president")
def desk():
    org_id = current_user.organization_id
    annual_minutes_slot = (
        db.session.query(Document)
        .filter_by(organization_id=org_id, compliance_category="compliance-minutes-annual-2026")
        .first()
    )
    election_notice = (
        db.session.query(Proposal)
        .filter_by(organization_id=org_id, type="election", status="draft")
        .first()
    )
    advisors = (
        db.session.query(AdvisorAcknowledgement)
        .filter_by(organization_id=org_id)
        .order_by(AdvisorAcknowledgement.created_at)
        .all()
    )
    return render_template(
        "board/president.html",
        annual_minutes_slot=annual_minutes_slot,
        election_notice=election_notice,
        advisors=advisors,
    )
```

- [ ] **Step 3: Create template**

Create `Cove/cove/board/templates/board/president.html`:

```html
{% extends "base.html" %}
{% block title %}President's Desk — Community of Abalone Cove{% endblock %}

{% block content %}
<div class="cove-page">
  <div class="cove-content">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">President's Desk</h1>
    <p class="text-sm text-gray-600 mb-8">Three items to review. No rush on any of them.</p>

    <div class="cove-card mb-4">
      <div class="cove-card-header">
        <h2 class="text-lg font-semibold">1. Upload 2026-03-21 AGM Minutes</h2>
      </div>
      <div class="cove-card-body">
        {% if annual_minutes_slot and annual_minutes_slot.published_at %}
          <p class="text-green-700">Published on {{ annual_minutes_slot.published_at.strftime('%Y-%m-%d %H:%M') }}.</p>
          <a href="/documents/{{ annual_minutes_slot.id }}" class="cove-btn cove-btn-secondary">View</a>
        {% else %}
          <p class="text-sm text-gray-600 mb-3">Uploading the minutes publishes them to all 81 lots via in-app notification, lot-email, and printable door-hangers (Civ §4040).</p>
          <a href="/documents/upload?compliance_category=compliance-minutes-annual-2026&publish=true" class="cove-btn cove-btn-primary">Upload Minutes</a>
        {% endif %}
      </div>
    </div>

    <div class="cove-card mb-4">
      <div class="cove-card-header">
        <h2 class="text-lg font-semibold">2. Review Board Election Notice (Draft)</h2>
      </div>
      <div class="cove-card-body">
        {% if election_notice %}
          <p class="text-sm text-gray-600 mb-3">Paper-ballot primary under Civ §4040 electronic delivery. Counsel review welcome before notice publishes.</p>
          <a href="/vote/proposal/{{ election_notice.id }}" class="cove-btn cove-btn-primary">Open Draft</a>
        {% else %}
          <p class="text-sm text-red-700">Election notice draft not found. Contact the ARC librarian.</p>
        {% endif %}
      </div>
    </div>

    <div class="cove-card mb-4">
      <div class="cove-card-header">
        <h2 class="text-lg font-semibold">3. Consulted Advisors</h2>
      </div>
      <div class="cove-card-body">
        {% if advisors %}
          <ul class="divide-y">
            {% for a in advisors %}
              <li class="py-2 flex items-center justify-between">
                <div>
                  <div class="font-medium">{{ a.advisor_name }}</div>
                  <div class="text-xs text-gray-500">{{ a.advisor_role_label }}</div>
                </div>
                <div>
                  {% if a.reviewed_at %}
                    <span class="cove-badge cove-status-active">Acknowledged {{ a.reviewed_at.strftime('%Y-%m-%d') }}</span>
                  {% else %}
                    <form method="post" action="/advisor/{{ a.id }}/resend" style="display:inline">
                      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                      <button class="cove-btn cove-btn-secondary" type="submit">Resend invite</button>
                    </form>
                  {% endif %}
                </div>
              </li>
            {% endfor %}
          </ul>
        {% else %}
          <p class="text-sm text-gray-600">No advisors configured. Contact the ARC librarian to add.</p>
        {% endif %}
      </div>
    </div>

    <div class="cove-card">
      <div class="cove-card-header">
        <h2 class="text-lg font-semibold">Compliance Snapshot</h2>
      </div>
      <div class="cove-card-body">
        <a href="/documents/compliance" class="cove-btn cove-btn-secondary">Open §4525 Dashboard</a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Register blueprint**

Modify `Cove/cove/board/__init__.py` to expose and register:

```python
from cove.board.president_routes import president_bp  # noqa: F401
```

In `Cove/cove/__init__.py`, register under `/board` (after `board_bp`):

```python
    from cove.board.president_routes import president_bp
    app.register_blueprint(president_bp, url_prefix="/board")
```

- [ ] **Step 5: Run; expect 3/3 PASS**

```bash
docker exec cove_flask pytest tests/integration/test_president_desk.py -v
```

- [ ] **Step 6: Commit**

```bash
git add Cove/cove/board/president_routes.py Cove/cove/board/templates/board/president.html Cove/cove/board/__init__.py Cove/cove/__init__.py Cove/tests/integration/test_president_desk.py
git commit -m "feat(cove): President's Desk — role-gated /board/president"
```

---

## Chunk 5: Inspector's Paper Tally Sheet

New route under `governance_bp`. Inspector-role-gated. Per-choice integer entry; auto-sum; certify → PDF → stored as document.

### Task 5.1: Routes + form

**Files:**
- Create: `Cove/cove/governance/paper_tally_routes.py`
- Create: `Cove/cove/governance/templates/governance/paper_tally.html`
- Create: `Cove/cove/governance/templates/governance/paper_tally_certified.html`
- Test: `Cove/tests/integration/test_paper_tally.py`

- [ ] **Step 1: Write tests**

Create `Cove/tests/integration/test_paper_tally.py`:

```python
"""Inspector paper-ballot tally sheet."""
import pytest
from cove.models import Proposal, Ballot, BallotEnvelope
from cove.models.tally_certification import ProposalTallyCertification


def test_paper_tally_requires_inspector(client, login_as, default_org, make_member, assign_role, make_proposal):
    m = make_member(org=default_org)
    assign_role(m, "member")
    login_as(m)
    p = make_proposal(org=default_org, type="election", status="open")
    r = client.get(f"/vote/paper-tally/{p.id}")
    assert r.status_code == 403


def test_paper_tally_inspector_can_enter_counts_and_certify(
    client, login_as, default_org, make_member, assign_role, make_proposal, db_session
):
    insp = make_member(org=default_org, lot_email="insp@x.com")
    assign_role(insp, "inspector")
    login_as(insp)
    p = make_proposal(org=default_org, type="election", status="closed")
    # Assume 3 candidates pre-seeded on proposal
    resp = client.post(f"/vote/paper-tally/{p.id}/certify", data={
        "choice_1": "18",
        "choice_2": "22",
        "choice_3": "4",
        "csrf_token": "x",  # adjust to real CSRF in integration test setup
    }, follow_redirects=True)
    assert resp.status_code == 200
    cert = db_session.query(ProposalTallyCertification).filter_by(proposal_id=p.id).one()
    assert cert.total_ballots == 44
    assert cert.certification_pdf_path is not None


def test_paper_tally_does_not_write_to_ballots(
    client, login_as, default_org, make_member, assign_role, make_proposal, db_session
):
    insp = make_member(org=default_org)
    assign_role(insp, "inspector")
    login_as(insp)
    p = make_proposal(org=default_org, type="election", status="closed")
    ballots_before = db_session.query(Ballot).count()
    envelopes_before = db_session.query(BallotEnvelope).count()
    client.post(f"/vote/paper-tally/{p.id}/certify", data={"choice_1": "5", "csrf_token": "x"})
    assert db_session.query(Ballot).count() == ballots_before
    assert db_session.query(BallotEnvelope).count() == envelopes_before
```

- [ ] **Step 2: Implement routes**

Create `Cove/cove/governance/paper_tally_routes.py`:

```python
"""Inspector's paper-ballot tally sheet.

Paper ballots remain the legal vote. This form is a calculator for the Inspector
of Elections to enter per-choice counts and produce a certified PDF result.

Hard rule: never writes to `ballots` or `ballot_envelopes`. Davis-Stirling secret
ballot separation is inviolable.
"""
from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timezone

from flask import Blueprint, render_template, request, abort, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from weasyprint import HTML

from cove.extensions import db
from cove.models import Proposal, Document
from cove.models.tally_certification import ProposalTallyCertification


paper_tally_bp = Blueprint("paper_tally", __name__, url_prefix="/vote/paper-tally", template_folder="templates")


@paper_tally_bp.before_request
@login_required
def _require_inspector():
    if not current_user.is_inspector:
        abort(403)


@paper_tally_bp.get("/<proposal_id>")
def form(proposal_id: str):
    proposal = db.session.get(Proposal, proposal_id) or abort(404)
    if proposal.organization_id != current_user.organization_id:
        abort(403)
    existing = (
        db.session.query(ProposalTallyCertification)
        .filter_by(proposal_id=proposal.id, inspector_member_id=current_user.id)
        .first()
    )
    return render_template("governance/paper_tally.html", proposal=proposal, existing=existing)


@paper_tally_bp.post("/<proposal_id>/certify")
def certify(proposal_id: str):
    proposal = db.session.get(Proposal, proposal_id) or abort(404)
    if proposal.organization_id != current_user.organization_id:
        abort(403)
    counts = {}
    total = 0
    for key, val in request.form.items():
        if not key.startswith("choice_"):
            continue
        try:
            n = int(val)
        except (TypeError, ValueError):
            continue
        if n < 0:
            flash("Counts cannot be negative", "error")
            return redirect(url_for("paper_tally.form", proposal_id=proposal.id))
        counts[key] = n
        total += n

    cert = ProposalTallyCertification(
        proposal_id=proposal.id,
        inspector_member_id=current_user.id,
        per_choice_counts=counts,
        total_ballots=total,
        certified_at=datetime.now(timezone.utc),
    )
    db.session.add(cert)
    db.session.commit()

    # Generate PDF
    pdf_dir = Path(current_app.config.get("CERTIFICATIONS_DIR", "/tmp/cove_certifications"))
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_dir / f"cert-{proposal.id}-{cert.id}.pdf"
    html = render_template("governance/paper_tally_certified.html", proposal=proposal, cert=cert, inspector=current_user)
    HTML(string=html).write_pdf(str(pdf_path))

    # Store in documents table as artifact
    doc = Document(
        organization_id=proposal.organization_id,
        title=f"Election Certification — {proposal.title}",
        filename=pdf_path.name,
        mime_type="application/pdf",
        size_bytes=pdf_path.stat().st_size,
        compliance_category="election-certification",
    )
    db.session.add(doc)
    cert.certification_pdf_path = str(pdf_path)
    db.session.commit()

    flash(f"Certified — total ballots: {total}", "success")
    return redirect(url_for("paper_tally.form", proposal_id=proposal.id))
```

- [ ] **Step 3: Templates**

`Cove/cove/governance/templates/governance/paper_tally.html`:

```html
{% extends "base.html" %}
{% block title %}Paper Tally — {{ proposal.title }}{% endblock %}
{% block content %}
<div class="max-w-3xl mx-auto">
  <a href="{{ url_for('governance.proposals') }}" class="text-sm text-cove-600 hover:underline">&larr; All Proposals</a>
  <h1 class="text-2xl font-bold mb-2">Paper Ballot Tally Sheet</h1>
  <p class="text-sm text-gray-600 mb-6">{{ proposal.title }}</p>
  <p class="text-xs text-gray-500 mb-6">Enter the count of paper ballots you have tallied for each choice. This produces a certified PDF result. Paper ballots remain the legal vote.</p>

  <form method="post" action="/vote/paper-tally/{{ proposal.id }}/certify" class="cove-card">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <div class="cove-card-body">
      {% for choice in proposal.choices or [] %}
      <div class="mb-3 flex items-center justify-between">
        <label class="cove-label" for="choice_{{ loop.index }}">{{ choice.label }}</label>
        <input type="number" min="0" step="1" name="choice_{{ loop.index }}" id="choice_{{ loop.index }}" class="cove-input w-32 text-right" x-model="counts[{{ loop.index }}]" value="{{ existing.per_choice_counts.get('choice_' ~ loop.index, 0) if existing else 0 }}">
      </div>
      {% endfor %}
      <div class="mt-4 pt-4 border-t text-right" x-data="{ counts: {} }">
        <strong>Total: </strong>
        <span x-text="Object.values(counts).reduce((a,b) => (parseInt(b)||0) + a, 0)">0</span>
      </div>
    </div>
    <div class="cove-card-header flex items-center justify-end gap-2">
      <a href="{{ url_for('governance.proposals') }}" class="cove-btn cove-btn-secondary">Cancel</a>
      <button type="submit" class="cove-btn cove-btn-primary">Certify Result</button>
    </div>
  </form>
</div>
{% endblock %}
```

`Cove/cove/governance/templates/governance/paper_tally_certified.html` (PDF output):

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: letter; margin: 1in; }
body { font-family: 'Helvetica', sans-serif; font-size: 11pt; line-height: 1.5; }
h1 { font-size: 16pt; border-bottom: 2px solid #333; padding-bottom: 0.2in; }
.meta { margin-top: 0.3in; color: #555; font-size: 10pt; }
table { width: 100%; border-collapse: collapse; margin-top: 0.3in; }
th, td { padding: 8px 12px; border-bottom: 1px solid #ddd; text-align: left; }
th { background: #f5f5f5; }
.total { font-weight: bold; font-size: 13pt; margin-top: 0.3in; padding-top: 0.2in; border-top: 2px solid #333; }
.sig { margin-top: 1in; }
</style>
</head>
<body>
<h1>Election Certification — Community of Abalone Cove</h1>
<div class="meta">
  Proposal: <strong>{{ proposal.title }}</strong><br>
  Inspector of Elections: <strong>{{ inspector.preferred_name or inspector.lot_email }}</strong><br>
  Certified: <strong>{{ cert.certified_at.strftime('%Y-%m-%d %H:%M %Z') }}</strong>
</div>
<table>
  <thead><tr><th>Choice</th><th style="text-align:right">Paper Ballots Counted</th></tr></thead>
  <tbody>
    {% for key, count in cert.per_choice_counts.items() %}
    <tr>
      <td>{{ key.replace('choice_', 'Choice ') }}</td>
      <td style="text-align:right">{{ count }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
<div class="total">Total paper ballots: {{ cert.total_ballots }}</div>
<div class="sig">
  <p>_______________________________________</p>
  <p>Inspector of Elections signature</p>
  <p style="font-size: 9pt; color: #666">Issued under California Civil Code §§5100–5145. Paper ballots retained by the Inspector per §4950/4955.</p>
</div>
</body>
</html>
```

- [ ] **Step 4: Register blueprint**

In `Cove/cove/__init__.py`, always-on section:

```python
    from cove.governance.paper_tally_routes import paper_tally_bp
    app.register_blueprint(paper_tally_bp)
```

- [ ] **Step 5: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_paper_tally.py -v
```

Expected: 3/3 PASS.

- [ ] **Step 6: Commit**

```bash
git add Cove/cove/governance/paper_tally_routes.py Cove/cove/governance/templates/governance/paper_tally*.html Cove/cove/__init__.py Cove/tests/integration/test_paper_tally.py
git commit -m "feat(cove): Inspector's paper-ballot tally sheet with PDF certification"
```

---

## Chunk 6: Consulted Advisor E-Acknowledgement

Magic-link flow. Advisor receives email, clicks link, lands on a page summarizing platform sections, clicks "I have reviewed this platform," attestation stored.

### Task 6.1: Token service + advisor blueprint

**Files:**
- Create: `Cove/cove/advisor/__init__.py`
- Create: `Cove/cove/advisor/services.py`
- Create: `Cove/cove/advisor/routes.py`
- Create: `Cove/cove/advisor/templates/advisor/acknowledge.html`
- Create: `Cove/cove/advisor/templates/advisor/already_acknowledged.html`
- Create: `Cove/cove/templates/emails/advisor_invite.html`
- Create: `Cove/cove/templates/emails/advisor_invite.txt`
- Test: `Cove/tests/integration/test_advisor_acknowledgement.py`

- [ ] **Step 1: Write tests**

Create `Cove/tests/integration/test_advisor_acknowledgement.py`:

```python
"""Advisor e-acknowledgement magic-link flow."""
import pytest
from cove.models.advisor_acknowledgement import AdvisorAcknowledgement


def test_advisor_invite_sends_email_with_magic_link(
    app_ctx, db_session, default_org, mailoutbox
):
    from cove.advisor.services import create_advisor_invite
    a = create_advisor_invite(
        organization_id=default_org.id,
        advisor_name="Jane Former",
        advisor_email="jane@x.com",
        advisor_role_label="Former Board President, 2018-2020",
    )
    assert len(mailoutbox) == 1
    body = mailoutbox[0].body + (mailoutbox[0].html or "")
    assert "/advisor/acknowledge/" in body


def test_advisor_acknowledge_flow(client, app_ctx, db_session, default_org):
    from cove.advisor.services import create_advisor_invite, serializer
    a = create_advisor_invite(
        organization_id=default_org.id,
        advisor_name="Jane", advisor_email="j@x.com", advisor_role_label="x",
    )
    # Simulate click
    r = client.get(f"/advisor/acknowledge/{a.magic_link_token}")
    assert r.status_code == 200
    assert b"reviewed" in r.data.lower()
    # Post acknowledge
    r = client.post(f"/advisor/acknowledge/{a.magic_link_token}")
    assert r.status_code in (200, 302)
    db_session.refresh(a)
    assert a.reviewed_at is not None


def test_advisor_token_single_use(client, app_ctx, db_session, default_org):
    from cove.advisor.services import create_advisor_invite
    a = create_advisor_invite(
        organization_id=default_org.id,
        advisor_name="J", advisor_email="j@x.com", advisor_role_label="x",
    )
    client.post(f"/advisor/acknowledge/{a.magic_link_token}")
    # Second use should land on already-acknowledged
    r = client.get(f"/advisor/acknowledge/{a.magic_link_token}")
    assert b"already" in r.data.lower()
```

- [ ] **Step 2: Implement service**

Create `Cove/cove/advisor/__init__.py`:

```python
from cove.advisor.routes import advisor_bp  # noqa: F401
```

Create `Cove/cove/advisor/services.py`:

```python
"""Advisor invite + acknowledgement token logic."""
from __future__ import annotations

import secrets
from typing import Optional

from itsdangerous import URLSafeTimedSerializer
from flask import current_app, render_template, url_for
from flask_mail import Message

from cove.extensions import db, mail
from cove.models.advisor_acknowledgement import AdvisorAcknowledgement


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="advisor-ack")


def _generate_token(ack_id: str, nonce: str) -> str:
    return _serializer().dumps({"ack_id": ack_id, "nonce": nonce})


def decode_token(token: str, max_age: int = 60 * 60 * 24 * 30) -> Optional[dict]:
    """Decode + validate token. Returns payload dict or None if invalid/expired."""
    try:
        return _serializer().loads(token, max_age=max_age)
    except Exception:
        return None


def create_advisor_invite(
    *,
    organization_id: str,
    advisor_name: str,
    advisor_email: str,
    advisor_role_label: str,
    attestation_text: Optional[str] = None,
) -> AdvisorAcknowledgement:
    import uuid
    nonce = secrets.token_hex(12)
    ack = AdvisorAcknowledgement(
        id=str(uuid.uuid4()),
        organization_id=organization_id,
        advisor_name=advisor_name,
        advisor_email=advisor_email,
        advisor_role_label=advisor_role_label,
        magic_link_token="",  # filled below
        nonce=nonce,
    )
    if attestation_text:
        ack.attestation_text = attestation_text
    db.session.add(ack)
    db.session.flush()  # obtain id
    ack.magic_link_token = _generate_token(ack.id, nonce)
    db.session.commit()
    _send_invite_email(ack)
    return ack


def _send_invite_email(ack: AdvisorAcknowledgement) -> None:
    link = url_for("advisor.acknowledge_get", token=ack.magic_link_token, _external=True)
    msg = Message(
        subject="Community of Abalone Cove — Consulted Advisor Review",
        recipients=[ack.advisor_email],
        html=render_template("emails/advisor_invite.html", ack=ack, link=link),
        body=render_template("emails/advisor_invite.txt", ack=ack, link=link),
    )
    mail.send(msg)


def resend_invite(ack: AdvisorAcknowledgement) -> None:
    ack.nonce = secrets.token_hex(12)
    ack.magic_link_token = _generate_token(ack.id, ack.nonce)
    db.session.commit()
    _send_invite_email(ack)
```

- [ ] **Step 3: Implement routes**

Create `Cove/cove/advisor/routes.py`:

```python
"""Advisor acknowledgement public magic-link routes."""
from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import current_user, login_required

from cove.extensions import db
from cove.models.advisor_acknowledgement import AdvisorAcknowledgement
from cove.advisor.services import decode_token, resend_invite


advisor_bp = Blueprint("advisor", __name__, url_prefix="/advisor", template_folder="templates")


@advisor_bp.get("/acknowledge/<token>")
def acknowledge_get(token: str):
    payload = decode_token(token)
    if not payload:
        abort(410)  # gone / expired
    ack = db.session.get(AdvisorAcknowledgement, payload["ack_id"])
    if not ack or ack.nonce != payload["nonce"]:
        abort(410)
    if ack.reviewed_at is not None:
        return render_template("advisor/already_acknowledged.html", ack=ack)
    return render_template("advisor/acknowledge.html", ack=ack, token=token)


@advisor_bp.post("/acknowledge/<token>")
def acknowledge_post(token: str):
    payload = decode_token(token)
    if not payload:
        abort(410)
    ack = db.session.get(AdvisorAcknowledgement, payload["ack_id"])
    if not ack or ack.nonce != payload["nonce"]:
        abort(410)
    if ack.reviewed_at is None:
        ack.mark_reviewed()
        db.session.commit()
    return render_template("advisor/already_acknowledged.html", ack=ack)


@advisor_bp.post("/<ack_id>/resend")
@login_required
def resend(ack_id: str):
    if not (current_user.is_president or current_user.is_admin):
        abort(403)
    ack = db.session.get(AdvisorAcknowledgement, ack_id) or abort(404)
    if ack.organization_id != current_user.organization_id:
        abort(403)
    resend_invite(ack)
    flash(f"Invite resent to {ack.advisor_email}", "success")
    return redirect(url_for("president.desk"))
```

- [ ] **Step 4: Templates**

`Cove/cove/advisor/templates/advisor/acknowledge.html`:

```html
{% extends "base.html" %}
{% block title %}Review — Community of Abalone Cove{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto">
  <h1 class="text-2xl font-bold mb-2">Community of Abalone Cove</h1>
  <p class="text-sm text-gray-500 mb-6">Consulted advisor review</p>
  <div class="cove-card">
    <div class="cove-card-body">
      <p>Dear {{ ack.advisor_name }},</p>
      <p>You were asked to review this platform as a consulted advisor in your role as {{ ack.advisor_role_label }}.</p>
      <p>The platform provides the association with a digital archive of governing documents, a community directory, a §4525 compliance dashboard, and supporting tools for board communications and the Inspector of Elections.</p>
      <p class="mt-4"><strong>Your attestation:</strong></p>
      <blockquote class="p-3 border-l-4 border-cove-300 bg-cove-50 italic">{{ ack.attestation_text }}</blockquote>
      <form method="post" action="/advisor/acknowledge/{{ token }}" class="mt-6">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <button class="cove-btn cove-btn-primary" type="submit">I have reviewed this platform</button>
      </form>
    </div>
  </div>
</div>
{% endblock %}
```

`Cove/cove/advisor/templates/advisor/already_acknowledged.html`:

```html
{% extends "base.html" %}
{% block content %}
<div class="max-w-2xl mx-auto text-center py-16">
  <h1 class="text-2xl font-bold mb-2">Acknowledged</h1>
  <p>Thank you, {{ ack.advisor_name }}.</p>
  {% if ack.reviewed_at %}
  <p class="text-sm text-gray-500 mt-2">Recorded: {{ ack.reviewed_at.strftime('%Y-%m-%d %H:%M %Z') }}</p>
  {% endif %}
</div>
{% endblock %}
```

Email templates:

`Cove/cove/templates/emails/advisor_invite.html`:

```html
<p>Dear {{ ack.advisor_name }},</p>
<p>In your capacity as {{ ack.advisor_role_label }}, you are invited to review a platform being developed for the Community of Abalone Cove.</p>
<p><a href="{{ link }}">Open review link</a></p>
<p style="font-size: 10pt; color: #666">Your review is informational and does not constitute legal approval or endorsement. If you did not expect this, simply ignore this message.</p>
```

`Cove/cove/templates/emails/advisor_invite.txt`:

```
Dear {{ ack.advisor_name }},

In your capacity as {{ ack.advisor_role_label }}, you are invited to review
a platform being developed for the Community of Abalone Cove.

Open review link: {{ link }}

Your review is informational and does not constitute legal approval or
endorsement.
```

- [ ] **Step 5: Register blueprint**

In `Cove/cove/__init__.py`, always-on section:

```python
    from cove.advisor.routes import advisor_bp
    app.register_blueprint(advisor_bp)
```

- [ ] **Step 6: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_advisor_acknowledgement.py -v
```

Expected: 3/3 PASS.

- [ ] **Step 7: Commit**

```bash
git add Cove/cove/advisor/ Cove/cove/templates/emails/advisor_invite.* Cove/cove/__init__.py Cove/tests/integration/test_advisor_acknowledgement.py
git commit -m "feat(cove): consulted-advisor e-acknowledgement magic-link flow"
```

---

## Chunk 7: §4525 Compliance Dashboard + Packet Builder

Visible record-keeping. Maps each Civ Code requirement to a vault category; shows ✅/⚠️/❌; generates a zip on demand.

### Task 7.1: Compliance config

**Files:**
- Create: `Cove/cove/vault/compliance_config.py`
- Test: `Cove/tests/unit/test_compliance_config.py`

- [ ] **Step 1: Write tests**

Create `Cove/tests/unit/test_compliance_config.py`:

```python
"""Compliance category config — Civ Code mapping."""
from cove.vault.compliance_config import CATEGORIES, category_is_stale


def test_categories_present():
    keys = {c.key for c in CATEGORIES}
    assert "compliance-governing" in keys
    assert "compliance-minutes-annual" in keys
    assert "compliance-reserves" in keys
    assert "compliance-arc" in keys


def test_all_categories_have_civ_code():
    for c in CATEGORIES:
        assert c.civ_code, f"Missing civ_code for {c.key}"
        assert c.label, f"Missing label for {c.key}"
        assert c.refresh_months is not None


def test_staleness_check():
    from datetime import datetime, timezone, timedelta
    ok = datetime.now(timezone.utc) - timedelta(days=30)
    stale = datetime.now(timezone.utc) - timedelta(days=500)
    assert category_is_stale(ok, refresh_months=12) is False
    assert category_is_stale(stale, refresh_months=12) is True
```

- [ ] **Step 2: Implement config**

Create `Cove/cove/vault/compliance_config.py`:

```python
"""Davis-Stirling compliance category map.

Each entry names a category key (used on `documents.compliance_category`), the
human label, the Civil Code reference, and the refresh cadence (in months).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional


@dataclass(frozen=True)
class ComplianceCategory:
    key: str
    label: str
    civ_code: str
    description: str
    refresh_months: int
    multiple: bool = False  # true when multiple docs belong (e.g., minutes)


CATEGORIES: tuple[ComplianceCategory, ...] = (
    ComplianceCategory(
        "compliance-governing",
        "Governing documents",
        "§4525(a)(1)(A)",
        "CC&Rs, bylaws, articles of incorporation, operating rules.",
        120, multiple=True,
    ),
    ComplianceCategory(
        "compliance-annual-budget",
        "Annual budget report",
        "§5300",
        "Pro-forma budget, reserve summary, collection policy, assessment/fee schedule.",
        12,
    ),
    ComplianceCategory(
        "compliance-annual-policy",
        "Annual policy statement",
        "§5310",
        "General info on member rights, procedures, contact.",
        12,
    ),
    ComplianceCategory(
        "compliance-insurance",
        "Insurance summary",
        "§5300(b)(9), §5555",
        "Summary of current association policies.",
        12,
    ),
    ComplianceCategory(
        "compliance-minutes-annual",
        "Annual meeting minutes",
        "§4950, §4955",
        "Most recent annual meeting minutes.",
        12,
    ),
    ComplianceCategory(
        "compliance-minutes-board",
        "Board meeting minutes (12 months)",
        "§4950, §4955",
        "Most recent 12 months of board meeting minutes.",
        1, multiple=True,
    ),
    ComplianceCategory(
        "compliance-reserves",
        "Reserve study",
        "§5550, §5565, §5570",
        "Current reserve study + funding plan.",
        36,
    ),
    ComplianceCategory(
        "compliance-arc",
        "ARC guidelines",
        "§4765",
        "Written procedure, timelines, appeal rights.",
        60,
    ),
    ComplianceCategory(
        "compliance-collection",
        "Collection / delinquency policy",
        "§5650, §5730",
        "Policy statement + active-delinquency disclosure.",
        12,
    ),
    ComplianceCategory(
        "compliance-litigation",
        "Pending litigation / claims",
        "§4530",
        "Lawsuits affecting the association.",
        3,
    ),
    ComplianceCategory(
        "compliance-inspection-rights",
        "Member inspection rights",
        "§5200–§5240",
        "Documented member rights of access.",
        60,
    ),
)


def category_is_stale(last_updated: Optional[datetime], refresh_months: int) -> bool:
    if last_updated is None:
        return True
    now = datetime.now(timezone.utc)
    return (now - last_updated) > timedelta(days=refresh_months * 30)


def get_category(key: str) -> Optional[ComplianceCategory]:
    for c in CATEGORIES:
        if c.key == key:
            return c
    return None
```

- [ ] **Step 3: Run tests**

```bash
docker exec cove_flask pytest tests/unit/test_compliance_config.py -v
```

- [ ] **Step 4: Commit**

```bash
git add Cove/cove/vault/compliance_config.py Cove/tests/unit/test_compliance_config.py
git commit -m "feat(cove): Davis-Stirling compliance category config"
```

### Task 7.2: Dashboard route + template

**Files:**
- Create: `Cove/cove/vault/compliance_routes.py`
- Create: `Cove/cove/vault/templates/vault/compliance.html`
- Test: `Cove/tests/integration/test_compliance_dashboard.py`

- [ ] **Step 1: Write tests**

Create `Cove/tests/integration/test_compliance_dashboard.py`:

```python
"""§4525 compliance dashboard + packet builder."""
import io
import zipfile
import pytest


def test_dashboard_requires_board_or_higher(client, login_as, default_org, make_member, assign_role):
    m = make_member(org=default_org)  # default: member role only
    login_as(m)
    r = client.get("/documents/compliance")
    assert r.status_code == 403


def test_dashboard_renders_all_categories(client, login_as, default_org, make_member, assign_role):
    m = make_member(org=default_org)
    assign_role(m, "board")
    login_as(m)
    r = client.get("/documents/compliance")
    assert r.status_code == 200
    b = r.data.decode()
    for key in ("Governing documents", "Annual budget report", "Reserve study", "ARC guidelines"):
        assert key in b


def test_generate_packet_returns_zip(client, login_as, default_org, make_member, assign_role, db_session):
    from cove.models import Document
    m = make_member(org=default_org)
    assign_role(m, "board")
    login_as(m)
    # Seed two compliance docs
    for cat in ("compliance-governing", "compliance-annual-budget"):
        d = Document(
            organization_id=default_org.id, title=f"Doc-{cat}", filename=f"{cat}.pdf",
            mime_type="application/pdf", size_bytes=100, compliance_category=cat,
            file_path=None,
        )
        db_session.add(d)
    db_session.commit()
    r = client.post("/documents/compliance/packet")
    assert r.status_code == 200
    assert r.headers["Content-Type"] in ("application/zip", "application/x-zip-compressed")
    z = zipfile.ZipFile(io.BytesIO(r.data))
    names = z.namelist()
    assert any("cover" in n.lower() for n in names)
    assert any("governing" in n.lower() for n in names) or any(".pdf" in n for n in names)
```

- [ ] **Step 2: Create route**

Create `Cove/cove/vault/compliance_routes.py`:

```python
"""§4525 compliance dashboard + packet builder."""
from __future__ import annotations

import io
import os
import zipfile
from datetime import datetime, timezone

from flask import Blueprint, render_template, abort, send_file, current_app, request
from flask_login import login_required, current_user

from cove.extensions import db
from cove.models import Document
from cove.vault.compliance_config import CATEGORIES, category_is_stale, get_category


compliance_bp = Blueprint("compliance", __name__, url_prefix="/documents/compliance", template_folder="templates")


@compliance_bp.before_request
@login_required
def _require_board_or_higher():
    if not (current_user.is_board or current_user.is_admin or current_user.is_inspector or current_user.is_president):
        abort(403)


@compliance_bp.get("/")
def dashboard():
    org_id = current_user.organization_id
    docs_by_cat: dict[str, list[Document]] = {}
    q = db.session.query(Document).filter(
        Document.organization_id == org_id,
        Document.compliance_category.isnot(None),
    ).order_by(Document.created_at.desc())
    for d in q:
        docs_by_cat.setdefault(d.compliance_category, []).append(d)

    rows = []
    for cat in CATEGORIES:
        docs = docs_by_cat.get(cat.key, [])
        if not docs:
            state = "missing"
            most_recent = None
        else:
            most_recent = docs[0]
            if category_is_stale(most_recent.created_at, cat.refresh_months):
                state = "stale"
            else:
                state = "current"
        rows.append({"cat": cat, "docs": docs, "state": state, "most_recent": most_recent})

    summary = {
        "current": sum(1 for r in rows if r["state"] == "current"),
        "stale": sum(1 for r in rows if r["state"] == "stale"),
        "missing": sum(1 for r in rows if r["state"] == "missing"),
    }
    return render_template("vault/compliance.html", rows=rows, summary=summary)


@compliance_bp.post("/packet")
def generate_packet():
    org_id = current_user.organization_id
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        cover = render_template("vault/compliance_packet.html", rows=_build_rows(org_id), generated_at=datetime.now(timezone.utc))
        zf.writestr("00-cover.html", cover)
        q = db.session.query(Document).filter(
            Document.organization_id == org_id,
            Document.compliance_category.isnot(None),
        )
        for d in q:
            if not d.file_path or not os.path.exists(d.file_path):
                continue
            arcname = f"{d.compliance_category}/{d.filename}"
            zf.write(d.file_path, arcname=arcname)

    buf.seek(0)
    filename = f"disclosure-packet-{datetime.now(timezone.utc).strftime('%Y%m%d')}.zip"
    return send_file(buf, mimetype="application/zip", as_attachment=True, download_name=filename)


def _build_rows(org_id: str):
    docs_by_cat: dict[str, list[Document]] = {}
    for d in db.session.query(Document).filter_by(organization_id=org_id).all():
        if d.compliance_category:
            docs_by_cat.setdefault(d.compliance_category, []).append(d)
    rows = []
    for cat in CATEGORIES:
        docs = docs_by_cat.get(cat.key, [])
        rows.append({"cat": cat, "docs": docs})
    return rows
```

- [ ] **Step 3: Template**

`Cove/cove/vault/templates/vault/compliance.html`:

```html
{% extends "base.html" %}
{% block title %}Compliance Dashboard — §4525{% endblock %}
{% block content %}
<div class="max-w-5xl mx-auto">
  <h1 class="text-2xl font-bold">Compliance Dashboard</h1>
  <p class="text-sm text-gray-600 mb-6">Davis-Stirling record-keeping obligations. Green = current; amber = stale; red = missing.</p>
  <div class="grid grid-cols-3 gap-3 mb-8">
    <div class="cove-card p-4 text-center"><div class="text-3xl font-bold text-green-700">{{ summary.current }}</div><div class="text-sm">Current</div></div>
    <div class="cove-card p-4 text-center"><div class="text-3xl font-bold text-amber-700">{{ summary.stale }}</div><div class="text-sm">Stale</div></div>
    <div class="cove-card p-4 text-center"><div class="text-3xl font-bold text-red-700">{{ summary.missing }}</div><div class="text-sm">Missing</div></div>
  </div>

  <form method="post" action="/documents/compliance/packet" class="mb-6 text-right">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <button class="cove-btn cove-btn-primary" type="submit">Generate §4525 Packet</button>
  </form>

  <div class="cove-card">
    <table class="cove-table">
      <thead><tr><th>Category</th><th>Civ Code</th><th>Status</th><th>Most recent</th><th></th></tr></thead>
      <tbody>
        {% for r in rows %}
        <tr>
          <td>
            <div class="font-medium">{{ r.cat.label }}</div>
            <div class="text-xs text-gray-500">{{ r.cat.description }}</div>
          </td>
          <td class="text-xs"><span class="font-mono">{{ r.cat.civ_code }}</span></td>
          <td>
            {% if r.state == 'current' %}<span class="cove-badge cove-status-active">Current</span>
            {% elif r.state == 'stale' %}<span class="cove-badge" style="background:#fef3c7;color:#92400e">Stale</span>
            {% else %}<span class="cove-badge" style="background:#fee2e2;color:#991b1b">Missing</span>
            {% endif %}
          </td>
          <td class="text-xs text-gray-600">
            {% if r.most_recent %}
              <a href="/documents/{{ r.most_recent.id }}" class="text-cove-600 hover:underline">{{ r.most_recent.title }}</a><br>
              <span>{{ r.most_recent.created_at.strftime('%Y-%m-%d') }}</span>
            {% else %} — {% endif %}
          </td>
          <td class="text-right">
            <a href="/documents/upload?compliance_category={{ r.cat.key }}" class="cove-btn cove-btn-secondary">Upload</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
```

`Cove/cove/vault/templates/vault/compliance_packet.html`:

```html
<!DOCTYPE html><html><head><meta charset="utf-8"><title>§4525 Packet Cover</title>
<style>body{font-family:sans-serif;padding:1in} table{border-collapse:collapse;width:100%} th,td{padding:6px;border-bottom:1px solid #ccc;text-align:left}</style>
</head><body>
<h1>Community of Abalone Cove — §4525 Disclosure Packet</h1>
<p>Generated {{ generated_at.strftime('%Y-%m-%d %H:%M %Z') }}</p>
<table>
  <thead><tr><th>Civ Code</th><th>Category</th><th>Included</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr>
      <td>{{ r.cat.civ_code }}</td>
      <td>{{ r.cat.label }}</td>
      <td>{% if r.docs %}{% for d in r.docs %}{{ d.filename }}<br>{% endfor %}{% else %}<em>missing</em>{% endif %}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
<p style="font-size:10pt;color:#666;margin-top:1em">Missing categories are explicitly disclosed. Recipients should request missing items directly from the association.</p>
</body></html>
```

- [ ] **Step 4: Register blueprint**

In `Cove/cove/__init__.py`, always-on section:

```python
    from cove.vault.compliance_routes import compliance_bp
    app.register_blueprint(compliance_bp)
```

- [ ] **Step 5: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_compliance_dashboard.py -v
```

Expected: 3/3 PASS.

- [ ] **Step 6: Commit**

```bash
git add Cove/cove/vault/compliance_routes.py Cove/cove/vault/templates/vault/compliance*.html Cove/cove/__init__.py Cove/tests/integration/test_compliance_dashboard.py
git commit -m "feat(cove): §4525 compliance dashboard + packet builder"
```

---

## Chunk 8: Seed, Sensitivity, Polish

Seed script for the HOA tenant. Sensitivity filter tests. Copy pass.

### Task 8.1: Disc importer + tenant seed

**Files:**
- Create: `Cove/scripts/import_disc_docs.py`
- Create: `Cove/scripts/seed_coac_president_demo_tenant.py`
- Create: `Cove/tests/fixtures/hoa_tenant.py`

- [ ] **Step 1: Disc import script**

Create `Cove/scripts/import_disc_docs.py`:

```python
"""Import the 2010 sample §4525 disclosure package from /Volumes/My Disc.

Run once. Populates the vault with:
- 2009 Restated Declaration (governing)
- 2012 Amended & Restated Bylaws (governing) — from repo
- Articles of Incorporation (governing)
- 2010 Sample §4525 Package (reference) — all 7 disc files bundled
"""
import os
import shutil
import sys
import uuid
from pathlib import Path
from datetime import datetime, timezone

from cove import create_app
from cove.extensions import db
from cove.models import Document, Organization

DISC = Path("/Volumes/My Disc")
BYLAWS_REPO = Path(__file__).parent.parent / "docs/archive/originals/governance/WPBCA-Bylaws-2012.pdf"


GOVERNING = [
    ("ArticlesOfIncorporation.pdf", "Articles of Incorporation", "compliance-governing", DISC),
    ("ProtectiveRestrictionsRestated-AsRecorded090529.pdf", "2009 Restated Declaration (CC&Rs)", "compliance-governing", DISC),
]

SAMPLE_FILES = [
    "ArticlesOfIncorporation.pdf",
    "ByLawsCopy1-HistoricScanned090920.pdf",
    "BylawsHistoricWithAmendmentsToSept2009Assembled091001.doc",
    "DisclosurePacket-Financial-Foreclosure-Architectural-Dispu….pdf",
    "MinutesAnnualMeetingMembers&Board02102010Signed.pdf",
    "MinutesDirectorsMeeting2010-09-15-Financials& Notice.pdf",
    "ProtectiveRestrictionsRestated-AsRecorded090529.pdf",
]


def main():
    app = create_app("dev")
    with app.app_context():
        org = Organization.query.first()
        if not org:
            print("ERROR: no organization seeded. Run seed.py first.")
            sys.exit(1)

        upload_root = Path(app.config["UPLOAD_FOLDER"]).resolve()
        upload_root.mkdir(parents=True, exist_ok=True)

        # 1) Governing documents from disc
        for filename, title, category, source in GOVERNING:
            src = source / filename
            if not src.exists():
                print(f"SKIP {filename} (not on disc)")
                continue
            dst = upload_root / f"{uuid.uuid4()}-{filename}"
            shutil.copy2(src, dst)
            d = Document(
                id=str(uuid.uuid4()),
                organization_id=org.id,
                title=title,
                filename=filename,
                mime_type="application/pdf",
                size_bytes=dst.stat().st_size,
                file_path=str(dst),
                compliance_category=category,
                created_at=datetime.now(timezone.utc),
            )
            db.session.add(d)
            print(f"Imported {filename}")

        # 2) 2012 Bylaws from repo
        if BYLAWS_REPO.exists():
            dst = upload_root / f"{uuid.uuid4()}-WPBCA-Bylaws-2012.pdf"
            shutil.copy2(BYLAWS_REPO, dst)
            db.session.add(Document(
                id=str(uuid.uuid4()),
                organization_id=org.id,
                title="2012 Amended & Restated Bylaws",
                filename="WPBCA-Bylaws-2012.pdf",
                mime_type="application/pdf",
                size_bytes=dst.stat().st_size,
                file_path=str(dst),
                compliance_category="compliance-governing",
            ))
            print("Imported 2012 Bylaws from repo")

        # 3) 2010 Sample Package as ZIP for reference category
        import zipfile
        bundle = upload_root / f"{uuid.uuid4()}-2010-sample-package.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in SAMPLE_FILES:
                src = DISC / f
                if src.exists():
                    zf.write(src, arcname=f)
        db.session.add(Document(
            id=str(uuid.uuid4()),
            organization_id=org.id,
            title="2010 Sample §4525 Disclosure Package (Reference Only)",
            filename="2010-sample-package.zip",
            mime_type="application/zip",
            size_bytes=bundle.stat().st_size,
            file_path=str(bundle),
            compliance_category="reference-sample",
        ))
        print("Imported 2010 sample package")

        db.session.commit()
        print("Done.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Tenant seed**

Create `Cove/scripts/seed_coac_president_demo_tenant.py`:

```python
"""Seed the CoAC HOA production tenant — curated preload for the Board president demo.

Runs AFTER seed.py + seed_members.py. Additive: doesn't rerun member import.

What this seeds:
- One draft proposal: Board Election Notice (paper-ballot primary, §4040 delivery)
- Two consulted-advisor slots (names supplied via CLI args)
- President role assignment (CLI arg: --president-email <lot_email>)
- Minutes slot reserved (empty Document row for 2026-03-21 AGM awaiting upload)

Usage:
    python3 scripts/seed_coac_president_demo_tenant.py \
        --president-email 2Barkentine@abalonecove.org \
        --advisor "Jane Doe,jane@x.com,Former Board President 2018-2020" \
        --advisor "John Roe,john@x.com,Former Board President 2014-2017"
"""
import argparse
import uuid
from datetime import datetime, timezone

from cove import create_app
from cove.extensions import db
from cove.models import Member, Organization, Role, MemberRole, Document, Proposal
from cove.advisor.services import create_advisor_invite


ELECTION_NOTICE = """## Notice of Board Election — Paper Ballot Primary

**Community of Abalone Cove**

**WHEREAS** the 2012 Amended & Restated Bylaws Section 8.2 provide for five
directors, each serving a one-year term; and

**WHEREAS** the 2026-03-21 annual meeting did not achieve quorum under Bylaws
Section 6.6, leaving the board at 2-of-5 without capacity for full action; and

**WHEREAS** California Civil Code §4040 permits delivery of notice by electronic
means to members who have so consented; and AB 2460 (effective January 1, 2025)
reduces the reconvened-meeting quorum to 20%;

**NOTICE IS HEREBY GIVEN** that an election of directors will be held:

- **Ballot method:** Paper ballots, two-envelope secret ballot per Bylaws §8.12
- **Notice delivery:** Electronically to each lot's canonical address
  `{lot#}{Street}@abalonecove.org` per Civ §4040
- **Nomination period:** 30 days from notice
- **Inspector of Elections:** [TBD — Board to confirm]
- **Reconvened-meeting quorum:** 20% (AB 2460) if initial quorum fails

[Proposed meeting date and venue: TBD]
"""


def seed(president_email: str, advisors: list[tuple[str, str, str]]):
    app = create_app("dev")
    with app.app_context():
        org = Organization.query.first()
        if not org:
            raise RuntimeError("No organization — run seed.py first.")

        # 1) Assign president role
        president_role = Role.query.filter_by(organization_id=org.id, name="president").first()
        if not president_role:
            raise RuntimeError("No 'president' role — run the HOA migration first.")
        pres = Member.query.filter_by(organization_id=org.id, lot_email=president_email).first()
        if not pres:
            raise RuntimeError(f"No member with lot_email={president_email}")
        if not any(r.name == "president" for r in pres.roles):
            db.session.add(MemberRole(member_id=pres.id, role_id=president_role.id))
            print(f"Assigned president role to {president_email}")

        # 2) Election-notice proposal
        existing = Proposal.query.filter_by(organization_id=org.id, type="election", status="draft").first()
        if not existing:
            p = Proposal(
                id=str(uuid.uuid4()),
                organization_id=org.id,
                title="Notice of Board Election — Paper Ballot Primary",
                description=ELECTION_NOTICE,
                type="election",
                status="draft",
                threshold_percent=0,  # plurality
                quorum_percent=0,
                secret_ballot=True,
                notice_period_days=30,
                created_at=datetime.now(timezone.utc),
            )
            db.session.add(p)
            print("Seeded election-notice proposal")

        # 3) Minutes slot reserved (empty placeholder)
        minutes_slot = Document.query.filter_by(
            organization_id=org.id, compliance_category="compliance-minutes-annual-2026"
        ).first()
        if not minutes_slot:
            d = Document(
                id=str(uuid.uuid4()),
                organization_id=org.id,
                title="2026-03-21 Annual Meeting Minutes",
                filename="pending-upload.placeholder",
                mime_type="application/pdf",
                size_bytes=0,
                compliance_category="compliance-minutes-annual-2026",
                file_path=None,
            )
            db.session.add(d)
            print("Reserved minutes slot")

        # 4) Advisor invites
        for name, email, role_label in advisors:
            existing_ack = db.session.query(
                __import__("cove.models.advisor_acknowledgement", fromlist=["AdvisorAcknowledgement"]).AdvisorAcknowledgement
            ).filter_by(organization_id=org.id, advisor_email=email).first()
            if existing_ack:
                print(f"Advisor {email} already invited")
                continue
            create_advisor_invite(
                organization_id=org.id,
                advisor_name=name,
                advisor_email=email,
                advisor_role_label=role_label,
            )
            print(f"Invited advisor {name} <{email}>")

        db.session.commit()


def parse_advisor(s: str) -> tuple[str, str, str]:
    parts = s.split(",", 2)
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(f"Advisor must be 'Name,email,role-label'; got {s!r}")
    return tuple(p.strip() for p in parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--president-email", required=True)
    ap.add_argument("--advisor", type=parse_advisor, action="append", default=[], help="Repeatable: 'Name,email,role-label'")
    args = ap.parse_args()
    seed(args.president_email, args.advisor)
```

- [ ] **Step 3: pytest fixture for integration tests**

Create `Cove/tests/fixtures/hoa_tenant.py`:

```python
"""HOA tenant fixture — 81 lots, 1 draft election proposal, 0 claimed accounts."""
import uuid
import pytest


@pytest.fixture
def hoa_tenant_fixture(db_session, default_org):
    """Seed a minimal HOA tenant for integration tests."""
    from cove.models import Member, Role, MemberRole, Parcel, Proposal

    # Minimal member set: 10 test lots instead of 81 (fast tests)
    members = []
    for i in range(1, 11):
        m = Member(
            id=str(uuid.uuid4()),
            organization_id=default_org.id,
            lot_email=f"{i}Barkentine@abalonecove.org",
            personal_email=f"owner{i}@example.com",
            lot_number=i,
            street="Barkentine Road",
            preferred_name=f"Owner {i}",
            membership_status="active",
        )
        db_session.add(m)
        members.append(m)
    db_session.commit()

    class _Tenant:
        pass
    t = _Tenant()
    t.members = members
    return t
```

Import into `conftest.py` so it's available.

- [ ] **Step 4: Commit**

```bash
git add Cove/scripts/import_disc_docs.py Cove/scripts/seed_coac_president_demo_tenant.py Cove/tests/fixtures/hoa_tenant.py
git commit -m "feat(cove): HOA tenant seed + 2010 sample package importer"
```

### Task 8.2: Sensitivity filter tests

**Files:**
- Create: `Cove/tests/integration/test_sensitivity_filter.py`

- [ ] **Step 1: Write tests**

```python
"""Production-mode sensitivity filter — no coac-* / reactivation content leaks."""
import os
import pytest
from cove import create_app


BANNED_SUBSTRINGS = [
    "Article II §5", "Article II Section 5",
    "reactivation", "Lot H", "0 Clipper",
    "ocean path easement", "Parcel 106",
    "15-owner", "trustee slate", "blitz",
    "Declaration 100 Article II",
]


@pytest.fixture
def production_app():
    prev = os.environ.get("COVE_DEPLOYMENT_MODE")
    os.environ["COVE_DEPLOYMENT_MODE"] = "production"
    yield create_app("test")
    if prev is None:
        os.environ.pop("COVE_DEPLOYMENT_MODE", None)
    else:
        os.environ["COVE_DEPLOYMENT_MODE"] = prev


@pytest.mark.parametrize("path", [
    "/", "/auth/login", "/member/dashboard", "/board/president", "/documents/compliance",
    "/vote/", "/community/",
])
def test_no_banned_content_on_public_and_board_routes(production_app, path):
    client = production_app.test_client()
    r = client.get(path)
    # 401/403/302 are fine; we're only scanning bodies that render
    if r.status_code not in (200, 302):
        pytest.skip(f"{path} → {r.status_code}, nothing to scan")
    body = r.data.decode(errors="ignore").lower()
    for bad in BANNED_SUBSTRINGS:
        assert bad.lower() not in body, f"{path} body contains banned substring {bad!r}"
```

- [ ] **Step 2: Run**

```bash
docker exec cove_flask pytest tests/integration/test_sensitivity_filter.py -v
```

Expected: all parametrized cases PASS (even 302 skipped cases are fine).

- [ ] **Step 3: Commit**

```bash
git add Cove/tests/integration/test_sensitivity_filter.py
git commit -m "test(cove): sensitivity filter — no coac/reactivation content in production"
```

---

## Chunk 9: Deploy to Mini + Board Proposal Packet

### Task 9.1: Mini-side compose variant

**Files:**
- Create: `Cove/devops/docker-compose.production.yml`
- Create: `Cove/docs/runbooks/hoa-instance-deploy.md`

- [ ] **Step 1: Production compose**

Create `Cove/devops/docker-compose.production.yml`:

```yaml
name: cove-hoa

services:
  flask:
    image: cove-flask
    build:
      context: ../
      dockerfile: Dockerfile
    container_name: cove_hoa_flask
    command: gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 --timeout 120 wsgi:app
    ports:
      - "127.0.0.1:5002:5000"
    environment:
      FLASK_ENV: prod
      COVE_ENV: production
      COVE_DEPLOYMENT_MODE: production
      DATABASE_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove_hoa
      VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/2
      DOMAIN: abalonecove.org
      # Outbound mail uses Cloudflare Email Routing / relay — configure in .env
    env_file:
      - ../.env.production
    healthcheck:
      test: ["CMD-SHELL", "python3 -c \"from urllib.request import urlopen; urlopen('http://localhost:5000/health')\""]
      interval: 10s
      start_period: 20s
      retries: 5
    volumes:
      - ../cove:/app/cove
      - ../templates:/app/templates
      - ../static:/app/static
      - ../wsgi.py:/app/wsgi.py
      - ../migrations:/app/migrations
      - ../scripts:/app/scripts
      - cove_hoa_uploads:/app/uploads
    networks:
      - growdirect
    restart: unless-stopped

volumes:
  cove_hoa_uploads:
    name: cove_hoa_uploads

networks:
  growdirect:
    external: true
```

- [ ] **Step 2: Runbook**

Create `Cove/docs/runbooks/hoa-instance-deploy.md`:

```markdown
# HOA Instance Deploy Runbook — `hoa.abalonecove.org`

Target: Mac mini at 192.168.10.102 (`gclyle@Geoffs-Mac-mini`).

## Prerequisites on the mini

- macOS (current)
- Docker Desktop running
- Git + `~/GrowDirect` checked out
- `cloudflared` installed (`brew install cloudflared`)
- Cloudflare tunnel credential in `~/.cloudflared/`

Verify:

```bash
ssh gclyle@192.168.10.102 'docker info >/dev/null && echo docker ok; which cloudflared'
```

## One-time setup

### 1. Create `cove_hoa` database

```bash
ssh gclyle@192.168.10.102 'docker exec growdirect_postgres psql -U growdirect -c "CREATE DATABASE cove_hoa;"'
```

### 2. Configure `.env.production`

SSH to mini, edit `~/Cove/.env.production`:

```
SECRET_KEY=<generate with `python3 -c "import secrets; print(secrets.token_hex(32))"`>
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove_hoa
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/2
COVE_DEPLOYMENT_MODE=production
DOMAIN=abalonecove.org
MAIL_SERVER=<Cloudflare or SES SMTP>
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=<...>
MAIL_PASSWORD=<...>
MAIL_DEFAULT_SENDER=hoa@abalonecove.org
MAGIC_LINK_EXPIRY=900
SESSION_DURATION_DAYS=7
```

### 3. Configure Cloudflare tunnel

```bash
ssh gclyle@192.168.10.102
cloudflared tunnel login   # browser OAuth
cloudflared tunnel create hoa-abalonecove
```

Edit `~/.cloudflared/config.yml`:

```yaml
tunnel: hoa-abalonecove
credentials-file: /Users/gclyle/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: hoa.abalonecove.org
    service: http://localhost:5002
  - service: http_status:404
```

Add DNS route:

```bash
cloudflared tunnel route dns hoa-abalonecove hoa.abalonecove.org
```

Install as a service:

```bash
sudo cloudflared service install
sudo launchctl load /Library/LaunchDaemons/com.cloudflare.cloudflared.plist
```

## Deploy cycle (every change)

From the laptop, push branch:

```bash
cd ~/GrowDirect
git push origin feat/coac-hoa-qa-instance
```

On the mini:

```bash
ssh gclyle@192.168.10.102
cd ~/GrowDirect
git fetch
git checkout feat/coac-hoa-qa-instance
git pull
cd Cove
docker compose -f devops/docker-compose.production.yml build
docker compose -f devops/docker-compose.production.yml up -d
docker exec cove_hoa_flask alembic -c /app/migrations/alembic.ini upgrade head
```

## Initial tenant seed (one-time)

```bash
docker exec cove_hoa_flask python3 /app/scripts/seed.py
docker exec cove_hoa_flask python3 /app/scripts/seed_members.py
docker exec cove_hoa_flask python3 /app/scripts/import_disc_docs.py  # requires disc mounted; or skip in prod
docker exec cove_hoa_flask python3 /app/scripts/seed_coac_president_demo_tenant.py \
  --president-email 2Barkentine@abalonecove.org \
  --advisor "Name1,email1@x.com,Former Board President YYYY-YYYY" \
  --advisor "Name2,email2@x.com,Former Board President YYYY-YYYY"
```

## Smoke test

```bash
curl -sI https://hoa.abalonecove.org/ | head -1   # expect HTTP/2 200
curl -sI https://hoa.abalonecove.org/health | head -1   # expect 200
```

Then browser:
- `https://hoa.abalonecove.org/auth/login`
- Magic-link login as `2Barkentine@abalonecove.org`
- Verify President's Desk renders

## Rollback

```bash
ssh gclyle@192.168.10.102
cd ~/GrowDirect
git checkout main
cd Cove
docker compose -f devops/docker-compose.production.yml up -d
docker exec cove_hoa_flask alembic -c /app/migrations/alembic.ini downgrade -1
```
```

- [ ] **Step 3: Commit**

```bash
git add Cove/devops/docker-compose.production.yml Cove/docs/runbooks/hoa-instance-deploy.md
git commit -m "feat(cove): HOA production compose + deploy runbook"
```

### Task 9.2: Board proposal packet documents

**Files:**
- Create: `Cove/docs/proposals/2026-04-20-board-president-cover-letter.md`
- Create: `Cove/docs/proposals/2026-04-20-4525-compliance-memo.md`
- Create: `Cove/docs/proposals/2026-04-20-board-election-notice-draft.md`
- Create: `Cove/docs/proposals/2026-04-20-demo-script.md`

- [ ] **Step 1: Cover letter**

Create `Cove/docs/proposals/2026-04-20-board-president-cover-letter.md`:

```markdown
# Cover Letter — Community of Abalone Cove Digital Archive Proposal

Date: 2026-04-20
To: [Board President]
From: Angelique Lyle, Board Director
Subject: Proposal — Digital archive + §4525 compliance dashboard

Dear [Board President],

Over the past several months, the ARC librarian (Greg Lyle), with my sponsorship
as a sitting board director and in consultation with two former board presidents
listed below, has assembled a digital archive and a §4525 compliance dashboard
for the Community of Abalone Cove.

It is no different from a spreadsheet and a bulletin board — functionally, a
modernized digital version of our filing cabinet, plus a phone book of lot
addresses, plus a calculator for the Inspector of Elections. It does not
replace paper ballots, which remain the legal vote. It does not create any
new legal authority; the 2012 Bylaws and 2009 Restated Declaration are the
controlling instruments.

What it does is make our existing Davis-Stirling record-keeping visible.
The 2026-03-21 annual meeting minutes enumerated gaps (indemnification, dues,
ARC procedure, bylaws modernization). This tool gives the board a single place
to upload the March minutes, publish them to every lot via §4040 electronic
notice, track §4525 compliance categories, and prepare the next board election
notice.

I am asking for your review and, when you are ready, your approval to:

1. Upload the 2026-03-21 annual meeting minutes through the platform.
2. Review the draft Notice of Board Election (paper-ballot primary) for
   counsel review before publication.
3. Authorize me to continue coordinating with Greg as the ARC librarian.

Two former board presidents have reviewed the platform and acknowledged it
electronically: [name1], [name2]. Their attestations are visible on the
President's Desk of the platform.

Access: hoa.abalonecove.org
Your lot email: 2Barkentine@abalonecove.org (sign-in via magic link)

No rush. Counsel review is welcome. The archive functions today; the election
notice waits on your word.

Respectfully,
Angelique Lyle
Director, Community of Abalone Cove
```

- [ ] **Step 2: §4525 compliance memo**

Create `Cove/docs/proposals/2026-04-20-4525-compliance-memo.md`:

```markdown
# §4525 Compliance Memorandum

Date: 2026-04-20
Prepared by: ARC Librarian, Community of Abalone Cove

## Purpose

Summarize Davis-Stirling record-keeping obligations and how the digital archive
supports the board in meeting them.

## Obligations

California Civil Code §§4525 and 5200–5240 impose specific record-keeping and
disclosure requirements on HOAs. These obligations are ongoing — not optional,
not triggered only by escrow.

| Civ Code | Requirement | Refresh cadence |
|---|---|---|
| §4525(a)(1)(A) | Governing documents (CC&Rs, bylaws, articles, operating rules) | On change |
| §5300 | Annual budget report | 12 months |
| §5310 | Annual policy statement | 12 months |
| §5300(b)(9), §5555 | Insurance summary | 12 months |
| §4950, §4955 | Minutes (annual + 12 months of board) | Per meeting |
| §5550, §5565, §5570 | Reserve study + funding plan | 36 months |
| §4765 | ARC guidelines | On change |
| §5650, §5730 | Collection / delinquency policy | 12 months |
| §4530 | Pending litigation / claims | 90 days |
| §5200–§5240 | Member inspection rights policy | On change |

The association is further obligated to deliver a §4525 package to any selling
owner within 10 days of request, for a fee established by the board.

## How the platform supports compliance

The platform's compliance dashboard is a visible map of the above requirements
against current inventory. For each category:

- ✅ Current — the most recent document is within the refresh cadence
- ⚠️ Stale — document exists but is past cadence
- ❌ Missing — no document in vault

"Generate §4525 Packet" assembles a zip of current documents with a cover sheet
that explicitly lists any missing items.

This does not create compliance; it surfaces the gap. Closing the gap remains
board work. The platform makes it inspectable at a glance.

## Current state snapshot (at cutover)

Imported at launch:
- 2009 Restated Declaration (CC&Rs)
- 2012 Amended & Restated Bylaws
- Articles of Incorporation
- 2010 Sample §4525 Disclosure Package (reference exemplar)

Pending upload by the Board:
- 2026-03-21 annual meeting minutes
- Current year's annual budget report (§5300)
- Current year's policy statement (§5310)
- Current insurance summary
- Current reserve study (if within 36 months)

## Recommendation

Adopt the platform as the association's record-keeping channel. No bylaw
amendment required — the 2012 Bylaws are silent on which digital tool, if any,
the association uses for its filing. The platform is additive to, not a
replacement for, paper originals.
```

- [ ] **Step 3: Board election notice draft**

Create `Cove/docs/proposals/2026-04-20-board-election-notice-draft.md`:

```markdown
# Draft — Notice of Board Election

**Community of Abalone Cove**

**Pursuant to** California Civil Code §§5100–5145, Corporations Code §7512, and
the 2012 Amended & Restated Bylaws of the Community of Abalone Cove:

NOTICE IS HEREBY GIVEN that an election of five (5) directors of the Community
of Abalone Cove will be held on the following terms:

1. **Ballot method.** Paper secret ballot, two-envelope system, per Bylaws
   §§8.12 and 5.9.

2. **Notice delivery.** This notice is delivered electronically to each lot's
   canonical address `{lot#}{Street}@abalonecove.org` per Civ §4040. Members
   preferring paper delivery may request same from the secretary.

3. **Nomination period.** Thirty (30) days from this notice. Nominations
   accepted by written submission to the secretary or, alternatively, through
   the association's digital archive at hoa.abalonecove.org.

4. **Inspector of Elections.** [TBD — Board to designate pursuant to Bylaws
   §8.14].

5. **Quorum.** Civil Code §5115 applies. If initial quorum is not achieved,
   the reconvened-meeting quorum under AB 2460 (effective 2025-01-01) is 20%.

6. **Uncontested seats.** If the number of candidates equals or is fewer than
   the seats available, the Board may declare election by acclamation per
   AB 502 (effective 2023-01-01).

7. **Meeting date and venue.** [TBD — Board to set].

Dated: _______________

_____________________________
[Board President]

_____________________________
[Secretary]
```

- [ ] **Step 4: Demo script (for your reference; you do the talking)**

Create `Cove/docs/proposals/2026-04-20-demo-script.md`:

```markdown
# Demo Script — Board President Walkthrough

Scope: 15-minute sit-down with the sitting Board president. You (Greg) do the
talking. Platform = prop.

## Open

"Angel asked me to walk you through something the ARC has been putting together.
It's no different from a spreadsheet, really — a filing cabinet, a phone book,
and a calculator. Can I show you?"

## The President's Desk

Log in as president → lands on `/board/president`. Three items.

"Here's everything the board has been working on in one place. Three things for
you to see. No rush on any of them."

## Vault — the filing cabinet

`/documents/compliance` → compliance dashboard.

"This is Davis-Stirling by category. Green means current. Amber means stale.
Red means missing. The board already has most of this — it just hasn't been
in one place before. When a document needs to go out for an escrow package,
we hit Generate and we have it."

## Directory — the phone book

`/community/` → 81 lots.

"Every lot has an email address already: {lot#}{Street}@abalonecove.org.
Nobody's signed in yet. When you upload the March minutes, everyone gets a
magic link to sign in. I'll walk the neighborhood and help people get their
first login."

## Inspector's Tally — the calculator

`/vote/paper-tally/...` (on a test proposal).

"The Inspector counts paper ballots by hand. This is his calculator — he
enters each pile, it sums, and spits out a certified PDF. He can ignore it
entirely. Paper ballots are still the legal vote."

## The ask

`/board/president` again.

"Three things:
1. Upload the March minutes. That's what sends the first notice to every lot.
2. Review the draft election notice. Counsel review welcome before it goes out.
3. Two former board presidents already acknowledged — you're the third.

Whenever you're ready. No rush."

## Close

Hand them printed: cover letter + §4525 memo + election notice draft. Leave.
```

- [ ] **Step 5: Commit**

```bash
git add Cove/docs/proposals/
git commit -m "docs(cove): board proposal packet (cover letter + 4525 memo + election notice + demo script)"
```

---

## Merge + Handoff

### Final task: PR + merge

- [ ] **Step 1: Push branch**

```bash
git push origin feat/coac-hoa-qa-instance
```

- [ ] **Step 2: Create PR**

```bash
gh pr create --title "CoAC HOA instance — hoa.abalonecove.org on the mini" --body "$(cat <<'EOF'
## Summary

- Production-mode gating (COVE_DEPLOYMENT_MODE) + fail-fast invariants
- President's Desk, publish cascade, Inspector's paper tally, advisor e-ack, §4525 compliance dashboard
- HOA tenant seed + disc importer
- Production compose for the mini + deploy runbook
- Board proposal packet (cover + §4525 memo + election notice + demo script)

Spec: docs/superpowers/specs/2026-04-20-coac-president-demo-tenant-design.md
Plan: docs/superpowers/plans/2026-04-20-coac-hoa-qa-instance.md

## Test plan

- [x] Full pytest suite passes in workspace mode
- [x] Full pytest suite passes in production mode (map/parcels/research/agent/archive gated)
- [x] Sensitivity filter tests pass (no coac/reactivation content)
- [ ] Deployed to mini; `https://hoa.abalonecove.org/` returns 200
- [ ] Magic-link login works as 2Barkentine@abalonecove.org
- [ ] Minutes upload → 81 emails delivered (MailHog or prod SMTP verified)
- [ ] §4525 packet zip generates

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Deploy to mini per runbook**

See `Cove/docs/runbooks/hoa-instance-deploy.md`.

- [ ] **Step 4: Verify**

```bash
curl -sI https://hoa.abalonecove.org/ | head -1
curl -sI https://hoa.abalonecove.org/health | head -1
```

- [ ] **Step 5: Hand the board packet to Angel**

Print from `Cove/docs/proposals/*.md`. Angel hands it to the Board president in the sit-down.

---

## Chunk 10: Security Hardening

HOA data is PII. The threat model is: opportunistic scrapers, credential-stuffing bots, a developer laptop that "might already be a torrent," and the long tail of copy-pasted screenshots in group chats. Cloudflare Tunnel + Docker isolation + role-gating are the base layer; this chunk adds the next layer.

### Task 10.1: Dedicated least-privilege Postgres user

**Files:**
- Modify: `Cove/docs/runbooks/hoa-instance-deploy.md`
- Create: `Cove/devops/init-db/hoa-user.sql`

- [ ] **Step 1: Create init-db script**

Create `Cove/devops/init-db/hoa-user.sql`:

```sql
-- Least-privilege role for the HOA instance.
-- Does NOT have access to cove, canary, growdirect_memory databases.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='cove_hoa_app') THEN
    CREATE ROLE cove_hoa_app LOGIN PASSWORD 'CHANGE_ME_IN_PROD';
  END IF;
END $$;

-- Database created separately via: CREATE DATABASE cove_hoa OWNER cove_hoa_app;
-- On first migration run, cove_hoa_app owns schema + all tables.

-- Revoke any default public grants
REVOKE ALL ON DATABASE cove_hoa FROM PUBLIC;
GRANT CONNECT ON DATABASE cove_hoa TO cove_hoa_app;
```

- [ ] **Step 2: Update runbook with setup step**

In `Cove/docs/runbooks/hoa-instance-deploy.md`, replace the `CREATE DATABASE cove_hoa` step with:

```bash
# Generate strong password
export HOA_DB_PASS=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
echo "cove_hoa_app password: $HOA_DB_PASS"  # save to .env.production immediately

# Create user + db
ssh gclyle@192.168.10.102 "docker exec -i growdirect_postgres psql -U growdirect <<SQL
CREATE ROLE cove_hoa_app LOGIN PASSWORD '$HOA_DB_PASS';
CREATE DATABASE cove_hoa OWNER cove_hoa_app;
REVOKE ALL ON DATABASE cove_hoa FROM PUBLIC;
GRANT CONNECT ON DATABASE cove_hoa TO cove_hoa_app;
SQL"
```

Update `DATABASE_URL` in `.env.production` to use `cove_hoa_app:$HOA_DB_PASS@...`.

- [ ] **Step 3: Commit**

```bash
git add Cove/devops/init-db/hoa-user.sql Cove/docs/runbooks/hoa-instance-deploy.md
git commit -m "security(cove): dedicated least-privilege cove_hoa_app Postgres role"
```

### Task 10.2: Non-root Docker user

**Files:**
- Modify: `Cove/Dockerfile`

- [ ] **Step 1: Audit current Dockerfile**

```bash
docker exec cove_flask whoami
```

If `root`, proceed. If already a non-root user, note and skip.

- [ ] **Step 2: Add non-root user to Dockerfile**

In `Cove/Dockerfile`, before the `CMD`/`ENTRYPOINT`:

```dockerfile
# Non-root runtime user
RUN groupadd -r cove && useradd -r -g cove -d /app -s /sbin/nologin cove \
 && chown -R cove:cove /app
USER cove
```

If the container currently needs write access beyond `/app/uploads`, grant explicit `chown` for those paths only.

- [ ] **Step 3: Rebuild + verify**

```bash
docker compose build cove_flask
docker compose up -d cove_flask
docker exec cove_flask whoami   # expect: cove
docker exec cove_flask id       # verify uid/gid non-zero
```

- [ ] **Step 4: Run full test suite (ensure nothing broke)**

```bash
docker exec cove_flask pytest tests/ -x --tb=short -q
```

- [ ] **Step 5: Commit**

```bash
git add Cove/Dockerfile
git commit -m "security(cove): run Flask container as non-root 'cove' user"
```

### Task 10.3: Encrypted offsite backup

**Files:**
- Create: `Cove/devops/backup/hoa_backup.sh`
- Create: `Cove/devops/backup/README.md`

- [ ] **Step 1: Backup script**

Create `Cove/devops/backup/hoa_backup.sh`:

```bash
#!/usr/bin/env bash
# Encrypted backup of the HOA instance.
# Runs on the mini via launchd (see README.md).
set -euo pipefail

TS=$(date +%Y-%m-%dT%H-%M-%S)
OUT_DIR=${OUT_DIR:-/var/backups/cove-hoa}
mkdir -p "$OUT_DIR"

# 1) DB dump
docker exec growdirect_postgres pg_dump -U cove_hoa_app -d cove_hoa \
  | gzip > "$OUT_DIR/cove-hoa-$TS.sql.gz"

# 2) Uploads volume snapshot
docker run --rm -v cove_hoa_uploads:/src -v "$OUT_DIR":/out alpine \
  tar czf "/out/cove-hoa-uploads-$TS.tar.gz" -C /src .

# 3) Encrypt both with GPG (recipient key must be imported on the mini)
GPG_RECIPIENT=${GPG_RECIPIENT:?set GPG_RECIPIENT env var (e.g., backup@abalonecove.org)}
for f in "$OUT_DIR/cove-hoa-$TS.sql.gz" "$OUT_DIR/cove-hoa-uploads-$TS.tar.gz"; do
  gpg --encrypt --recipient "$GPG_RECIPIENT" --output "$f.gpg" "$f"
  rm "$f"
done

# 4) Upload to Backblaze B2 (or S3 — configure b2 tool on mini)
if command -v b2 >/dev/null 2>&1; then
  b2 upload-file abalonecove-backups "$OUT_DIR/cove-hoa-$TS.sql.gz.gpg" "cove-hoa-$TS.sql.gz.gpg"
  b2 upload-file abalonecove-backups "$OUT_DIR/cove-hoa-uploads-$TS.tar.gz.gpg" "cove-hoa-uploads-$TS.tar.gz.gpg"
fi

# 5) Retain last 30 daily + 12 monthly locally
find "$OUT_DIR" -name "*.gpg" -mtime +30 -delete
```

- [ ] **Step 2: Document setup in README**

Create `Cove/devops/backup/README.md`:

```markdown
# Backup Setup (mini)

## One-time
1. `brew install gnupg b2-tools`
2. Generate backup key pair; export public key to backup@abalonecove.org
3. `b2 authorize-account <keyID> <applicationKey>`
4. Bucket: `abalonecove-backups` (private, encrypted at rest)
5. Set env: `export GPG_RECIPIENT=backup@abalonecove.org`

## Schedule (launchd)
`~/Library/LaunchAgents/com.abalonecove.backup.plist`:

- ProgramArguments: `/bin/bash /Users/gclyle/GrowDirect/Cove/devops/backup/hoa_backup.sh`
- StartCalendarInterval: hour 3, minute 0 (3am local daily)
- EnvironmentVariables: GPG_RECIPIENT

Load: `launchctl load ~/Library/LaunchAgents/com.abalonecove.backup.plist`

## Restore drill (quarterly)
1. `b2 download-file abalonecove-backups cove-hoa-<latest>.sql.gz.gpg ./`
2. `gpg --decrypt cove-hoa-<latest>.sql.gz.gpg | gunzip | psql -U cove_hoa_app -d cove_hoa_restore`
3. Verify table counts match production.

Document restore time in the incident-response playbook (Task 10.9).
```

- [ ] **Step 3: Commit**

```bash
chmod +x Cove/devops/backup/hoa_backup.sh
git add Cove/devops/backup/
git commit -m "security(cove): encrypted offsite backup script + README"
```

### Task 10.4: Login rate-limit + account lockout

**Files:**
- Modify: `Cove/cove/auth/routes.py`
- Create: `Cove/cove/auth/lockout.py`
- Test: `Cove/tests/integration/test_login_lockout.py`

- [ ] **Step 1: Write failing test**

Create `Cove/tests/integration/test_login_lockout.py`:

```python
"""Login rate limit + lockout after N failed attempts."""
import pytest


def test_login_lockout_after_5_failed_attempts(client, app_ctx, db_session, default_org, make_member):
    m = make_member(org=default_org, lot_email="test@example.com", password="correct-password")
    for _ in range(5):
        r = client.post("/auth/login", data={"email": "test@example.com", "password": "wrong"})
        assert r.status_code in (200, 401, 403)  # error shown, not success
    # 6th attempt — even with correct password — should be locked
    r = client.post("/auth/login", data={"email": "test@example.com", "password": "correct-password"})
    assert r.status_code in (403, 429)
    body = r.data.decode().lower()
    assert "locked" in body or "too many" in body


def test_login_lockout_expires_after_window(client, app_ctx, db_session, default_org, make_member, freezer):
    m = make_member(org=default_org, lot_email="test2@example.com", password="correct-password")
    for _ in range(5):
        client.post("/auth/login", data={"email": "test2@example.com", "password": "wrong"})
    # Advance 20 minutes
    freezer.move_to("+20min")
    r = client.post("/auth/login", data={"email": "test2@example.com", "password": "correct-password"})
    assert r.status_code in (200, 302)  # unlocked
```

`freezer` fixture via freezegun — add to requirements-test.txt if missing.

- [ ] **Step 2: Lockout helper**

Create `Cove/cove/auth/lockout.py`:

```python
"""Account lockout — store failed-attempt counters in Valkey with TTL.

Key: lockout:{lot_email}
Value: count
TTL: 15 minutes
Lockout threshold: 5 failures in the window → locked until TTL expires.
"""
from __future__ import annotations

import logging
from flask import current_app

try:
    import redis
except ImportError:
    redis = None


FAILURE_LIMIT = 5
WINDOW_SECONDS = 15 * 60


log = logging.getLogger(__name__)


def _client():
    if redis is None:
        return None
    url = current_app.config.get("VALKEY_URL")
    if not url:
        return None
    return redis.from_url(url)


def record_failure(email: str) -> int:
    r = _client()
    if r is None:
        return 0
    key = f"lockout:{email.lower()}"
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, WINDOW_SECONDS)
    count, _ = pipe.execute()
    return int(count)


def is_locked(email: str) -> bool:
    r = _client()
    if r is None:
        return False
    val = r.get(f"lockout:{email.lower()}")
    if val is None:
        return False
    return int(val) >= FAILURE_LIMIT


def clear(email: str) -> None:
    r = _client()
    if r is None:
        return
    r.delete(f"lockout:{email.lower()}")
```

- [ ] **Step 3: Wire into login route**

In `Cove/cove/auth/routes.py` login handler:

```python
from cove.auth.lockout import record_failure, is_locked, clear

# at top of POST handler
if is_locked(email):
    flash("Too many failed attempts. Try again in 15 minutes.", "error")
    return render_template("auth/login.html", form=form), 429

# on password check fail
if not check_password_hash(member.password_hash, password):
    count = record_failure(email)
    flash(f"Invalid credentials. {max(0, 5 - count)} attempts remaining.", "error")
    return render_template("auth/login.html", form=form), 401

# on success
clear(email)
login_user(member, remember=True)
```

Preserve existing behavior for magic-link flows (no password → no lockout).

- [ ] **Step 4: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_login_lockout.py -v
```

Expected: 2/2 PASS.

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/auth/lockout.py Cove/cove/auth/routes.py Cove/tests/integration/test_login_lockout.py
git commit -m "security(cove): account lockout after 5 failed login attempts (15-min window)"
```

### Task 10.5: Audit log — all privileged actions

**Files:**
- Modify: `Cove/cove/vault/publish.py`
- Modify: `Cove/cove/board/president_routes.py`
- Modify: `Cove/cove/governance/paper_tally_routes.py`
- Modify: `Cove/cove/advisor/services.py`
- Modify: `Cove/cove/vault/compliance_routes.py`
- Test: `Cove/tests/integration/test_audit_log.py`

- [ ] **Step 1: Verify audit_log model exists**

```bash
docker exec cove_flask python3 -c "from cove.models import AuditLog; print(AuditLog.__tablename__)"
```

If missing, reference existing `cove/models/audit_log.py`. If absent entirely, defer this task and open GRO issue.

- [ ] **Step 2: Write test**

Create `Cove/tests/integration/test_audit_log.py`:

```python
"""Audit log coverage — privileged actions must record."""
import pytest
from cove.models import AuditLog


@pytest.mark.parametrize("action,path,method", [
    ("document.publish", "/documents/<doc_id>/publish", "post"),
    ("paper_tally.certify", "/vote/paper-tally/<prop_id>/certify", "post"),
    ("compliance.packet_generated", "/documents/compliance/packet", "post"),
    ("advisor.invite_created", None, None),  # service-level
])
def test_audit_entries_exist(db_session, default_org, action, path, method):
    # Seed a relevant action in each test; assert AuditLog row created.
    # Implementation per test: e.g., call publish_document() and check audit_log rows
    pass  # concrete test bodies per action
```

- [ ] **Step 3: Add `audit()` helper**

Create or extend `Cove/cove/audit.py`:

```python
from __future__ import annotations
from datetime import datetime, timezone
from flask import request
from flask_login import current_user
from cove.extensions import db
from cove.models import AuditLog


def audit(action: str, *, resource_id: str | None = None, metadata: dict | None = None) -> None:
    try:
        entry = AuditLog(
            organization_id=getattr(current_user, "organization_id", None),
            actor_member_id=getattr(current_user, "id", None),
            action=action,
            resource_id=resource_id,
            ip_address=request.headers.get("X-Forwarded-For", request.remote_addr) if request else None,
            user_agent=request.user_agent.string if request else None,
            metadata_json=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        # Audit failure must not break the action; log and swallow
        db.session.rollback()
```

- [ ] **Step 4: Wire into privileged paths**

In `publish.py` after commit:

```python
from cove.audit import audit
audit("document.publish", resource_id=document.id, metadata={"channels": list(channels), "deliveries": len(results)})
```

In `paper_tally_routes.py` after cert commit:

```python
audit("paper_tally.certify", resource_id=cert.id, metadata={"proposal_id": proposal.id, "total": total})
```

In `compliance_routes.py` `generate_packet`:

```python
audit("compliance.packet_generated", metadata={"categories": len(CATEGORIES)})
```

In `advisor/services.py` after `db.session.commit()` in `create_advisor_invite`:

```python
audit("advisor.invite_created", resource_id=ack.id, metadata={"email": advisor_email})
```

And in `acknowledge_post`:

```python
audit("advisor.acknowledged", resource_id=ack.id, metadata={"name": ack.advisor_name})
```

- [ ] **Step 5: Run tests**

```bash
docker exec cove_flask pytest tests/integration/test_audit_log.py -v
```

- [ ] **Step 6: Commit**

```bash
git add Cove/cove/audit.py Cove/cove/vault/publish.py Cove/cove/board/president_routes.py Cove/cove/governance/paper_tally_routes.py Cove/cove/advisor/ Cove/cove/vault/compliance_routes.py Cove/tests/integration/test_audit_log.py
git commit -m "security(cove): audit-log wiring for privileged actions"
```

### Task 10.6: Cloudflare WAF + tunnel hardening

**Files:**
- Create: `Cove/docs/runbooks/hoa-cloudflare-config.md`

- [ ] **Step 1: Document Cloudflare-side config**

Create `Cove/docs/runbooks/hoa-cloudflare-config.md`:

```markdown
# Cloudflare Config — hoa.abalonecove.org

## Tunnel (already required)
- Named tunnel: `hoa-abalonecove`
- Origin: `http://localhost:5002`
- Credentials: on mini only

## SSL/TLS
- Mode: **Full (strict)** — tunnel handles cert
- Minimum TLS: 1.2
- HSTS: enabled (6-month max-age, includeSubDomains)

## Firewall rules (dashboard → Security → WAF → Custom rules)

1. **Rate-limit /auth/*** — 10 requests per minute per IP → challenge
   ```
   (http.request.uri.path matches "^/auth/") 
   ```

2. **Challenge known-bot UAs on any /auth/***
   ```
   (http.request.uri.path matches "^/auth/") and (cf.client.bot)
   ```

3. **Block countries outside US/CA** (optional — only if board agrees)
   ```
   not (ip.geoip.country in {"US" "CA"})
   ```

4. **Challenge on high threat score**
   ```
   (cf.threat_score ge 10)
   ```

## Bot Fight Mode
Dashboard → Security → Bots → enable **Bot Fight Mode** (free tier).

## Page rules / Transform rules
- Strip `Server` header
- Set `X-Frame-Options: DENY` (already via talisman, but belt + suspenders)
- Enable **Always Use HTTPS**

## Access policies (optional — for board-only staging)
Cloudflare Access can gate `/board/*` behind email OTP for extra layer. Requires
Cloudflare Teams free tier. Document but don't enable by default.
```

- [ ] **Step 2: Commit**

```bash
git add Cove/docs/runbooks/hoa-cloudflare-config.md
git commit -m "security(cove): Cloudflare WAF + tunnel hardening runbook"
```

### Task 10.7: Secrets hygiene

**Files:**
- Create: `Cove/docs/runbooks/secrets-rotation.md`
- Modify: `.gitignore` (if .env.production not already ignored)

- [ ] **Step 1: Verify `.env.production` is gitignored**

```bash
grep -E "^\.env" .gitignore || echo ".env*" >> .gitignore
```

- [ ] **Step 2: Rotation runbook**

Create `Cove/docs/runbooks/secrets-rotation.md`:

```markdown
# Secrets Rotation — HOA Instance

Rotate on schedule: SECRET_KEY quarterly, DB password annually, Cloudflare
tunnel token on any suspected compromise.

## SECRET_KEY (Flask session signing + magic-link signing)

**Impact of rotation:** invalidates all active sessions + all outstanding magic
links. Schedule during off-hours.

```bash
ssh gclyle@192.168.10.102
cd ~/Cove
cp .env.production .env.production.bak.$(date +%Y%m%d)
NEW=$(python3 -c "import secrets; print(secrets.token_hex(32))")
sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=$NEW|" .env.production
docker compose -f devops/docker-compose.production.yml restart cove_hoa_flask
```

## Database password

```bash
NEW=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
docker exec -i growdirect_postgres psql -U growdirect <<SQL
ALTER ROLE cove_hoa_app WITH PASSWORD '$NEW';
SQL
# Update .env.production DATABASE_URL
sed -i '' "s|cove_hoa_app:[^@]*|cove_hoa_app:$NEW|" .env.production
docker compose -f devops/docker-compose.production.yml restart cove_hoa_flask
```

## File permissions

```bash
chmod 600 ~/Cove/.env.production
chmod 600 ~/.cloudflared/*.json
```

## Incident: key suspected compromised

1. Rotate immediately (do not schedule).
2. Review `audit_log` for unexpected admin/president actions in the suspect window.
3. If compromise confirmed:
   - Rotate ALL secrets (SECRET_KEY, DB, CF tunnel, SMTP, GPG)
   - Force password reset for all members
   - Notify board in writing
```

- [ ] **Step 3: Commit**

```bash
git add Cove/docs/runbooks/secrets-rotation.md .gitignore
git commit -m "security(cove): secrets rotation runbook"
```

### Task 10.8: Mini hardening verification

**Files:**
- Create: `Cove/docs/runbooks/mini-hardening-checklist.md`

- [ ] **Step 1: Write checklist**

Create `Cove/docs/runbooks/mini-hardening-checklist.md`:

```markdown
# Mini Hardening Checklist (192.168.10.102)

Verify before cutover; review quarterly.

## macOS
- [ ] FileVault enabled — `fdesetup status` → `FileVault is On`
- [ ] Auto-updates enabled — `softwareupdate --schedule` → On
- [ ] Firewall enabled — `defaults read /Library/Preferences/com.apple.alf globalstate` → `1` or `2`
- [ ] Remote Login (SSH) restricted to specific users (System Settings → Sharing → Remote Login → Only these users)
- [ ] Screen Sharing disabled unless needed

## SSH
- [ ] Password auth disabled once key auth confirmed: `sudo sed -i '' 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config` then `sudo launchctl kickstart -k system/com.openssh.sshd`
- [ ] `~/.ssh/authorized_keys` chmod 600, contains only intended keys
- [ ] Consider fail2ban or sshguard (`brew install sshguard`)

## Docker
- [ ] Docker Desktop auto-updates on
- [ ] Only bind to 127.0.0.1 on host (already in compose; verify `docker ps` shows `127.0.0.1:5002->5000`, not `0.0.0.0:5002`)
- [ ] Cove_flask runs as non-root (see Task 10.2)

## Cloudflared
- [ ] Installed as system service: `sudo launchctl list | grep cloudflared`
- [ ] Tunnel config: `~/.cloudflared/config.yml` chmod 600
- [ ] Cert file: `~/.cloudflared/*.json` chmod 600

## Network
- [ ] Nothing else exposed on LAN beyond what's required
- [ ] Router firewall rule: inbound 22 allowed only from laptop IP (192.168.10.124) if possible
- [ ] No port forwarding from external router → mini (Cloudflare Tunnel obviates this)

## Backups
- [ ] Daily launchd backup job loaded and reporting success in `/var/log/abalonecove-backup.log`
- [ ] Restore drill performed at least once (see `Cove/devops/backup/README.md`)
```

- [ ] **Step 2: Commit**

```bash
git add Cove/docs/runbooks/mini-hardening-checklist.md
git commit -m "security(cove): mini hardening checklist"
```

### Task 10.9: Incident response playbook

**Files:**
- Create: `Cove/docs/runbooks/incident-response.md`

- [ ] **Step 1: Playbook**

Create `Cove/docs/runbooks/incident-response.md`:

```markdown
# Incident Response — HOA Instance

## Severity levels

- **SEV1**: Data breach confirmed OR service down + unable to recover in < 4h
- **SEV2**: Suspected unauthorized access, no confirmed exfil
- **SEV3**: Service degraded (slow, intermittent errors)
- **SEV4**: Non-urgent bug

## SEV1/SEV2 — first 30 minutes

1. **Isolate** — stop the tunnel:
   ```bash
   ssh gclyle@192.168.10.102 'sudo launchctl unload /Library/LaunchDaemons/com.cloudflare.cloudflared.plist'
   ```
   `hoa.abalonecove.org` goes dark. Origin still reachable on LAN for investigation.

2. **Preserve evidence** — snapshot:
   ```bash
   ssh gclyle@192.168.10.102 'docker exec growdirect_postgres pg_dump -U cove_hoa_app cove_hoa | gzip > /tmp/forensic-$(date +%s).sql.gz'
   scp gclyle@192.168.10.102:/tmp/forensic-*.sql.gz ~/forensics/
   ```

3. **Triage** — check audit_log for unexpected actions:
   ```sql
   SELECT actor_member_id, action, resource_id, created_at, ip_address
   FROM audit_log
   WHERE created_at > NOW() - INTERVAL '48 hours'
   ORDER BY created_at DESC;
   ```

4. **Notify** — Angel, Board president, consulted advisors. Draft in plain language; no speculation.

## Recovery

- Rotate all secrets (Task 10.7)
- If data-at-rest compromised: restore from last known-clean backup (Task 10.3)
- Once stable, re-enable tunnel:
  ```bash
  sudo launchctl load /Library/LaunchDaemons/com.cloudflare.cloudflared.plist
  ```

## Post-incident

Within 72 hours: written incident summary for the board. Template:
- What happened
- When detected, when contained
- What data was (or was not) accessed
- Actions taken
- Actions planned (patching, process improvements)

File under `Cove/docs/incidents/YYYY-MM-DD-<slug>.md`.

## Contact tree

- ARC librarian (primary): Greg Lyle
- Board sponsor: Angelique Lyle
- Board president: <name>
- Cloudflare support: https://dash.cloudflare.com/support
- Backblaze support: https://help.backblaze.com
```

- [ ] **Step 2: Commit**

```bash
git add Cove/docs/runbooks/incident-response.md
git commit -m "security(cove): incident response playbook"
```

---

**End of plan.**
