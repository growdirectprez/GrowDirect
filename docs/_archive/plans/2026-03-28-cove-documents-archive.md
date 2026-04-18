# Cove Documents & Archive Redesign Implementation Plan

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three-tier document access (member/arc/board) to the Vault, gate the Archive to ARC/board/admin, and add a promote-from-archive flow.

**Architecture:** Existing Vault blueprint gains an `access_tier` enum replacing `is_public`. Archive routes split into member-accessible (landing pages) and ARC-gated (research docs). New promote action copies files from Archive filesystem into Vault database storage.

**Tech Stack:** Flask, SQLAlchemy 2.0, PostgreSQL 17, Alembic, WTForms, Jinja2, Tailwind CSS, pytest

**Spec:** `docs/superpowers/specs/2026-03-28-cove-documents-archive-design.md`

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `cove/models/vault.py` | Add `AccessTier` enum, replace `is_public` with `access_tier` on Document |
| Modify | `cove/models/member.py` | Add `can_access_arc` to Role, add `is_arc` property to Member |
| Create | `migrations/versions/xxxx_add_access_tier.py` | Alembic migration for all schema changes |
| Modify | `cove/vault/services.py` | Replace `CATEGORIES` archive→historical, replace `public_only` with tier filtering, add upload tier validation |
| Modify | `cove/vault/forms.py` | Replace `is_public` checkbox with `access_tier` dropdown |
| Modify | `cove/vault/routes.py` | Pass user role context to services, enforce tier access on detail/download |
| Modify | `cove/vault/templates/vault/index.html` | Tier filter tabs, tier badges |
| Modify | `cove/vault/templates/vault/upload.html` | Replace is_public checkbox with access_tier dropdown |
| Modify | `cove/vault/templates/vault/document.html` | Tier badge display |
| Modify | `cove/archive/routes.py` | Add ARC/board/admin gate on research routes, add promote routes |
| Modify | `cove/archive/forms.py` | Add `PromoteDocumentForm` |
| Create | `cove/archive/templates/archive/promote.html` | Promote form template |
| Modify | `cove/archive/templates/archive/catalog.html` | Tier-filtered vault docs in merged catalog |
| Create | `tests/unit/test_vault_services.py` | Unit tests for tier filtering, upload validation, category rename |
| Create | `tests/unit/test_access_tiers.py` | Unit tests for is_arc property, tier access logic |
| Create | `tests/integration/test_vault_routes.py` | Integration tests for tier-gated routes |
| Create | `tests/integration/test_archive_routes.py` | Integration tests for archive access gate + promote flow |

---

## Chunk 1: Data Model & Migration

### Task 0: Create shared test fixtures for tier testing

**Files:**
- Modify: `tests/conftest.py`

All subsequent tasks depend on these fixtures. They must exist before any test can run.

- [ ] **Step 1: Add tier-related fixtures to conftest.py**

Add fixtures for:
- `test_org` — Organization record (needed as FK target for all models)
- `arc_role` — Role with `can_access_arc=True`
- `board_role` — Role with name "board"
- `basic_member` — Member with no special roles (FK to test_org)
- `member_with_arc_role` — Member with active ARC MemberRole
- `board_member` — Member with active board MemberRole
- `authenticated_client` — test client logged in as basic_member
- `arc_client` — test client logged in as member_with_arc_role
- `board_client` — test client logged in as board_member
- `member_document` — Document with `access_tier="member"` (FK to test_org and basic_member)
- `board_document` — Document with `access_tier="board"`
- `sample_tiered_docs` — 3 documents, one per tier

All model instances must use valid UUIDs and proper FK relationships (organization_id, uploaded_by, etc.) to avoid FK constraint violations. Follow existing fixture patterns in `tests/conftest.py` for the app factory and db_session setup.

- [ ] **Step 2: Verify fixtures load**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/conftest.py --collect-only
```
Expected: No import errors.

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py
git commit -m "test: add tier-related fixtures for vault and archive tests"
```

### Task 1: Add AccessTier enum and update Document model

**Files:**
- Modify: `cove/models/vault.py:9-24`
- Test: `tests/unit/test_access_tiers.py`

- [ ] **Step 1: Write failing test for AccessTier enum**

```python
# tests/unit/test_access_tiers.py
import pytest
from cove.models.vault import AccessTier, Document


def test_access_tier_enum_values():
    assert AccessTier.MEMBER.value == "member"
    assert AccessTier.ARC.value == "arc"
    assert AccessTier.BOARD.value == "board"


def test_document_has_access_tier(app, db_session, test_org, basic_member):
    """Document should have access_tier field defaulting to member."""
    import uuid
    from cove.models.vault import Document
    doc = Document(
        id=str(uuid.uuid4()),
        organization_id=test_org.id,
        title="Test Doc",
        category="notices",
        uploaded_by=basic_member.id,
    )
    db_session.add(doc)
    db_session.commit()
    assert doc.access_tier == AccessTier.MEMBER.value
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_access_tiers.py -v`
Expected: FAIL — `ImportError: cannot import name 'AccessTier'`

- [ ] **Step 3: Implement AccessTier enum and update Document model**

In `cove/models/vault.py`, add the enum and replace `is_public`:

```python
import enum

class AccessTier(enum.Enum):
    MEMBER = "member"
    ARC = "arc"
    BOARD = "board"
```

On the Document model, replace:
```python
is_public: Mapped[bool] = mapped_column(default=False)
```
with:
```python
access_tier: Mapped[str] = mapped_column(
    String(10), default=AccessTier.MEMBER.value
)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_access_tiers.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/models/vault.py tests/unit/test_access_tiers.py
git commit -m "feat: add AccessTier enum, replace is_public with access_tier on Document"
```

### Task 2: Add can_access_arc to Role and is_arc to Member

**Files:**
- Modify: `cove/models/member.py:16-20` (Role permissions) and `cove/models/member.py:53-63` (Member properties)
- Test: `tests/unit/test_access_tiers.py`

- [ ] **Step 1: Write failing tests for Role.can_access_arc and Member.is_arc**

Append to `tests/unit/test_access_tiers.py`:

```python
def test_role_has_can_access_arc(app, db_session, test_org):
    """Role should have can_access_arc permission flag."""
    import uuid
    from cove.models.member import Role
    role = Role(
        id=str(uuid.uuid4()),
        organization_id=test_org.id,
        name="arc_committee",
        can_access_arc=True,
    )
    db_session.add(role)
    db_session.commit()
    assert role.can_access_arc is True


def test_role_can_access_arc_defaults_false(app, db_session, test_org):
    import uuid
    from cove.models.member import Role
    role = Role(
        id=str(uuid.uuid4()),
        organization_id=test_org.id,
        name="member",
    )
    db_session.add(role)
    db_session.commit()
    assert role.can_access_arc is False


def test_member_is_arc_property(app, db_session, member_with_arc_role):
    """Member with active ARC role should return is_arc=True."""
    assert member_with_arc_role.is_arc is True


def test_member_is_arc_false_without_role(app, db_session, basic_member):
    """Member without ARC role should return is_arc=False."""
    assert basic_member.is_arc is False
```

Note: `member_with_arc_role` and `basic_member` fixtures will need to be created in `conftest.py` or a local conftest. Use existing fixture patterns from `tests/conftest.py`.

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_access_tiers.py -v`
Expected: FAIL — `TypeError: can_access_arc is an invalid keyword argument`

- [ ] **Step 3: Add can_access_arc to Role model**

In `cove/models/member.py`, after line 20 (`can_access_envelopes`), add:

```python
can_access_arc: Mapped[bool] = mapped_column(default=False)
```

- [ ] **Step 4: Add is_arc property to Member model**

In `cove/models/member.py`, after the `is_inspector` property (around line 63), add:

```python
@property
def is_arc(self) -> bool:
    return any(
        mr.is_current and mr.role.can_access_arc
        for mr in self.member_roles
    )
```

This matches the existing style of `is_board` and `is_inspector` which access `mr.role.name` without a None guard (relying on `lazy="joined"` on the relationship).

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_access_tiers.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add cove/models/member.py tests/unit/test_access_tiers.py
git commit -m "feat: add can_access_arc to Role, is_arc property to Member"
```

### Task 3: Write Alembic migration

**Files:**
- Create: `migrations/versions/xxxx_add_access_tier.py`

- [ ] **Step 1: Generate migration**

```bash
cd ~/GrowDirect/Cove && python3 -m alembic revision -m "add access tier and can_access_arc"
```

- [ ] **Step 2: Write migration upgrade/downgrade**

Edit the generated file:

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # 1. Add access_tier column with default
    op.add_column('documents', sa.Column('access_tier', sa.String(10), nullable=False, server_default='member'))

    # 2. Migrate is_public data
    op.execute("UPDATE documents SET access_tier = 'member' WHERE is_public = true")
    op.execute("UPDATE documents SET access_tier = 'board' WHERE is_public = false")

    # 3. Drop is_public
    op.drop_column('documents', 'is_public')

    # 4. Rename archive category to historical
    op.execute("UPDATE documents SET category = 'historical' WHERE category = 'archive'")

    # 5. Add can_access_arc to roles
    op.add_column('roles', sa.Column('can_access_arc', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    # Reverse: add is_public back, map tiers, drop access_tier, rename category, drop permission
    op.add_column('documents', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))
    op.execute("UPDATE documents SET is_public = true WHERE access_tier = 'member'")
    op.execute("UPDATE documents SET is_public = false WHERE access_tier IN ('arc', 'board')")
    op.drop_column('documents', 'access_tier')
    op.execute("UPDATE documents SET category = 'archive' WHERE category = 'historical'")
    op.drop_column('roles', 'can_access_arc')
```

- [ ] **Step 3: Run migration against dev database**

```bash
cd ~/GrowDirect/Cove && python3 -m alembic upgrade head
```
Expected: Migration applies without errors.

- [ ] **Step 4: Verify migration applied**

```bash
cd ~/GrowDirect/Cove && python3 -c "
from cove import create_app
from cove.extensions import db
app = create_app()
with app.app_context():
    result = db.session.execute(db.text(\"SELECT column_name FROM information_schema.columns WHERE table_name='documents'\"))
    cols = [r[0] for r in result]
    assert 'access_tier' in cols, f'access_tier not found in {cols}'
    assert 'is_public' not in cols, f'is_public still exists in {cols}'
    print('Migration verified: access_tier present, is_public removed')
"
```

- [ ] **Step 5: Commit**

```bash
git add migrations/
git commit -m "migrate: add access_tier, drop is_public, rename archive category, add can_access_arc"
```

---

## Chunk 2: Vault Service & Form Changes

### Task 4: Update CATEGORIES constant and list_documents service

**Files:**
- Modify: `cove/vault/services.py:23-31` (CATEGORIES) and `cove/vault/services.py:211-242` (list_documents)
- Test: `tests/unit/test_vault_services.py`

- [ ] **Step 1: Write failing test for updated CATEGORIES**

```python
# tests/unit/test_vault_services.py
from cove.vault.services import CATEGORIES


def test_categories_has_historical_not_archive():
    assert "historical" in CATEGORIES
    assert "archive" not in CATEGORIES
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_categories_has_historical_not_archive -v`
Expected: FAIL — `assert 'historical' in [... 'archive']`

- [ ] **Step 3: Update CATEGORIES in services.py**

In `cove/vault/services.py`, replace `"archive"` with `"historical"` in the `CATEGORIES` list (around line 31).

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_categories_has_historical_not_archive -v`
Expected: PASS

- [ ] **Step 5: Write failing test for tier-filtered list_documents**

Append to `tests/unit/test_vault_services.py`:

```python
from cove.models.vault import AccessTier


def test_list_documents_member_sees_member_only(app, db_session, sample_tiered_docs):
    """Member-level user should only see member-tier documents."""
    from cove.vault.services import list_documents
    docs = list_documents(org_id="test-org", user_max_tier=AccessTier.MEMBER)
    tiers = {d.access_tier for d in docs}
    assert tiers == {AccessTier.MEMBER.value}


def test_list_documents_arc_sees_member_and_arc(app, db_session, sample_tiered_docs):
    """ARC-level user should see member + arc documents."""
    from cove.vault.services import list_documents
    docs = list_documents(org_id="test-org", user_max_tier=AccessTier.ARC)
    tiers = {d.access_tier for d in docs}
    assert tiers == {AccessTier.MEMBER.value, AccessTier.ARC.value}


def test_list_documents_board_sees_all(app, db_session, sample_tiered_docs):
    """Board-level user should see all documents."""
    from cove.vault.services import list_documents
    docs = list_documents(org_id="test-org", user_max_tier=AccessTier.BOARD)
    tiers = {d.access_tier for d in docs}
    assert tiers == {AccessTier.MEMBER.value, AccessTier.ARC.value, AccessTier.BOARD.value}
```

Note: `sample_tiered_docs` fixture creates 3 docs, one per tier.

- [ ] **Step 6: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py -v`
Expected: FAIL — `TypeError: list_documents() got an unexpected keyword argument 'user_max_tier'`

- [ ] **Step 7: Update list_documents to filter by tier**

In `cove/vault/services.py`, modify `list_documents()` (around line 211):
- Replace `public_only: bool = False` parameter with `user_max_tier: AccessTier = AccessTier.MEMBER`
- Replace the `if public_only` filter with tier-based filtering:

```python
# Define tier hierarchy
TIER_HIERARCHY = {
    AccessTier.MEMBER: [AccessTier.MEMBER.value],
    AccessTier.ARC: [AccessTier.MEMBER.value, AccessTier.ARC.value],
    AccessTier.BOARD: [AccessTier.MEMBER.value, AccessTier.ARC.value, AccessTier.BOARD.value],
}

# In the query:
allowed_tiers = TIER_HIERARCHY[user_max_tier]
query = query.where(Document.access_tier.in_(allowed_tiers))
```

- [ ] **Step 8: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py -v`
Expected: PASS

- [ ] **Step 9: Commit**

```bash
git add cove/vault/services.py tests/unit/test_vault_services.py
git commit -m "feat: update CATEGORIES, add tier-filtered list_documents"
```

### Task 5: Add upload tier validation to upload_document

**Files:**
- Modify: `cove/vault/services.py:48-125` (upload_document)
- Test: `tests/unit/test_vault_services.py`

- [ ] **Step 1: Write failing test for upload tier validation**

Append to `tests/unit/test_vault_services.py`:

```python
def test_member_cannot_upload_board_tier(app, db_session, test_org, basic_member):
    """Member-level user cannot upload board-tier documents."""
    from cove.vault.services import upload_document
    result = upload_document(
        org_id=test_org.id,
        uploaded_by=basic_member.id,
        filename="test.pdf",
        file_data=b"fake pdf content",
        title="Board Secret",
        category="notices",
        access_tier="board",
        user_max_tier=AccessTier.MEMBER,
        upload_folder="/tmp/test_uploads",
    )
    assert result is None  # Rejected due to insufficient tier


def test_member_cannot_upload_arc_tier(app, db_session, test_org, basic_member):
    """Member-level user cannot upload arc-tier documents."""
    from cove.vault.services import upload_document
    result = upload_document(
        org_id=test_org.id,
        uploaded_by=basic_member.id,
        filename="test.pdf",
        file_data=b"fake pdf content",
        title="ARC Doc",
        category="notices",
        access_tier="arc",
        user_max_tier=AccessTier.MEMBER,
        upload_folder="/tmp/test_uploads",
    )
    assert result is None


def test_arc_cannot_upload_board_tier(app, db_session, test_org, member_with_arc_role):
    """ARC-level user cannot upload board-tier documents."""
    from cove.vault.services import upload_document
    result = upload_document(
        org_id=test_org.id,
        uploaded_by=member_with_arc_role.id,
        filename="test.pdf",
        file_data=b"fake pdf content",
        title="Board Secret",
        category="notices",
        access_tier="board",
        user_max_tier=AccessTier.ARC,
        upload_folder="/tmp/test_uploads",
    )
    assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_upload_document_validates_tier_permission -v`
Expected: FAIL — `TypeError: upload_document() got unexpected keyword arguments`

- [ ] **Step 3: Update upload_document signature and add validation**

In `cove/vault/services.py`, modify `upload_document()`:
- Replace `is_public` parameter with `access_tier: str = "member"` and `user_max_tier: AccessTier = AccessTier.MEMBER`
- Add validation at top of function:

```python
allowed_tiers = TIER_HIERARCHY[user_max_tier]
if access_tier not in allowed_tiers:
    return None
```

- Set `doc.access_tier = access_tier` instead of `doc.is_public = is_public`

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/vault/services.py tests/unit/test_vault_services.py
git commit -m "feat: add tier validation to upload_document"
```

### Task 6: Update DocumentUploadForm

**Files:**
- Modify: `cove/vault/forms.py:39-42` (replace is_public with access_tier)
- Test: `tests/unit/test_vault_services.py`

- [ ] **Step 1: Write failing test for form field**

Append to `tests/unit/test_vault_services.py`:

```python
def test_upload_form_has_access_tier_field(app):
    """Upload form should have access_tier SelectField, not is_public."""
    with app.test_request_context():
        from cove.vault.forms import DocumentUploadForm
        form = DocumentUploadForm()
        assert hasattr(form, 'access_tier'), "Form missing access_tier field"
        assert not hasattr(form, 'is_public'), "Form still has is_public field"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_upload_form_has_access_tier_field -v`
Expected: FAIL — `AssertionError: Form missing access_tier field`

- [ ] **Step 3: Replace is_public with access_tier in form**

In `cove/vault/forms.py`, replace the `is_public` BooleanField (lines 39-42) with:

```python
access_tier = SelectField(
    "Access Level",
    choices=[
        ("member", "All Members"),
        ("arc", "ARC Committee"),
        ("board", "Board Only"),
    ],
    default="member",
)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_upload_form_has_access_tier_field -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/vault/forms.py tests/unit/test_vault_services.py
git commit -m "feat: replace is_public with access_tier SelectField in upload form"
```

---

## Chunk 3: Vault Route & Template Updates

### Task 7: Update vault routes to use access tiers

**Files:**
- Modify: `cove/vault/routes.py:28-161`
- Test: `tests/integration/test_vault_routes.py`

- [ ] **Step 1: Write failing integration tests for tier-gated access**

```python
# tests/integration/test_vault_routes.py
import pytest


def test_member_cannot_see_board_document(authenticated_client, board_document):
    """Regular member should get 403 on board-tier document."""
    response = authenticated_client.get(f"/vault/{board_document.id}")
    assert response.status_code == 403


def test_member_can_see_member_document(authenticated_client, member_document):
    """Regular member should see member-tier document."""
    response = authenticated_client.get(f"/vault/{member_document.id}")
    assert response.status_code == 200


def test_board_member_can_see_board_document(board_client, board_document):
    """Board member should see board-tier document."""
    response = board_client.get(f"/vault/{board_document.id}")
    assert response.status_code == 200


def test_index_filters_by_tier(authenticated_client, sample_tiered_docs):
    """Index should only show member-tier docs for regular members."""
    response = authenticated_client.get("/vault/")
    assert response.status_code == 200
    assert b"Member Doc" in response.data
    assert b"Board Doc" not in response.data


def test_upload_passes_access_tier(board_client):
    """Upload form should accept access_tier instead of is_public."""
    response = board_client.get("/vault/upload")
    assert response.status_code == 200
    assert b"Access Level" in response.data or b"access_tier" in response.data
```

Note: Fixtures `authenticated_client`, `board_client`, `board_document`, `member_document`, `sample_tiered_docs` need to be defined in `tests/integration/conftest.py` or `tests/conftest.py`. Follow existing patterns from `tests/integration/test_auth_routes.py`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_vault_routes.py -v`
Expected: FAIL

- [ ] **Step 3: Update vault index route**

In `cove/vault/routes.py`, modify the `index()` function (around line 28):
- Add a shared helper `get_user_max_tier(user)` in `cove/vault/services.py`:

```python
def get_user_max_tier(user) -> AccessTier:
    if user.is_board or user.is_admin:
        return AccessTier.BOARD
    elif user.is_arc:
        return AccessTier.ARC
    return AccessTier.MEMBER
```

- Import and use it in the index route: `user_max_tier=get_user_max_tier(current_user)`
- Pass `user_max_tier` to `list_documents()` and to template context
- Pass `user_max_tier` to template context for tab rendering

- [ ] **Step 4: Update vault upload route**

In `cove/vault/routes.py`, modify the `upload()` function (around line 54):
- Read `form.access_tier.data` instead of `form.is_public.data`
- Pass `access_tier=form.access_tier.data` and `user_max_tier=_user_max_tier(current_user)` to `upload_document()`
- Filter form choices based on user tier (set `form.access_tier.choices` dynamically)

- [ ] **Step 5: Update vault document detail route**

In `cove/vault/routes.py`, modify the `document()` function (around line 86):
- After fetching the document, check tier access:

```python
from cove.vault.services import TIER_HIERARCHY

allowed = TIER_HIERARCHY[_user_max_tier(current_user)]
if doc.access_tier not in allowed:
    abort(403)
```

- [ ] **Step 6: Update vault download routes**

In `cove/vault/routes.py`, add the same tier check to `download_latest()` (line 107) and `download_version()` (line 136).

- [ ] **Step 7: Run tests to verify they pass**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_vault_routes.py -v`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add cove/vault/routes.py tests/integration/test_vault_routes.py
git commit -m "feat: add tier-based access control to vault routes"
```

### Task 8: Update vault templates

**Files:**
- Modify: `cove/vault/templates/vault/index.html`
- Modify: `cove/vault/templates/vault/upload.html`
- Modify: `cove/vault/templates/vault/document.html`

- [ ] **Step 1: Update index.html — add tier filter tabs and tier badges**

Replace the category pills section with tier tabs above category pills:

```html
<!-- Tier filter tabs (visible based on user role) -->
<div class="flex gap-2 mb-4">
    <a href="{{ url_for('vault_bp.index', tier='all') }}"
       class="cove-badge {{ 'cove-badge-active' if not request.args.get('tier') }}">All</a>
    {% if user_max_tier.value in ('arc', 'board') %}
    <a href="{{ url_for('vault_bp.index', tier='arc') }}"
       class="cove-badge {{ 'cove-badge-active' if request.args.get('tier') == 'arc' }}">ARC</a>
    {% endif %}
    {% if user_max_tier.value == 'board' %}
    <a href="{{ url_for('vault_bp.index', tier='board') }}"
       class="cove-badge {{ 'cove-badge-active' if request.args.get('tier') == 'board' }}">Board</a>
    {% endif %}
</div>
```

On each document card, replace the `is_public` badge with a tier badge:

```html
<span class="cove-badge cove-badge-{{ doc.access_tier }}">{{ doc.access_tier }}</span>
```

- [ ] **Step 2: Update upload.html — replace is_public checkbox with access_tier dropdown**

Replace the `is_public` checkbox block with:

```html
<div class="mb-4">
    {{ form.access_tier.label(class="cove-label") }}
    {{ form.access_tier(class="cove-input") }}
</div>
```

- [ ] **Step 3: Update document.html — add tier badge**

In the document header section, replace the public badge with:

```html
<span class="cove-badge cove-badge-{{ document.access_tier }}">{{ document.access_tier }}</span>
```

- [ ] **Step 4: Verify templates render**

Start the dev server and visually verify:
```bash
cd ~/GrowDirect/Cove/devops && docker compose up -d
```
Navigate to `/vault/` and `/vault/upload` — confirm tier tabs and dropdown render.

- [ ] **Step 5: Commit**

```bash
git add cove/vault/templates/
git commit -m "feat: update vault templates for tier-based access display"
```

---

## Chunk 4: Archive Access Gate

### Task 9: Add ARC/board/admin gate to archive research routes

**Files:**
- Modify: `cove/archive/routes.py:141-218`
- Test: `tests/integration/test_archive_routes.py`

- [ ] **Step 1: Write failing integration tests for archive access gate**

```python
# tests/integration/test_archive_routes.py
import pytest


def test_member_can_access_archive_landing(authenticated_client):
    """Regular member should access archive landing page."""
    response = authenticated_client.get("/archive/")
    assert response.status_code == 200


def test_member_can_access_timeline(authenticated_client):
    """Regular member should access timeline."""
    response = authenticated_client.get("/archive/timeline")
    assert response.status_code == 200


def test_member_can_access_catalog(authenticated_client):
    """Regular member should access catalog."""
    response = authenticated_client.get("/archive/catalog")
    assert response.status_code == 200


def test_member_can_access_chain(authenticated_client):
    """Regular member should access chain of title."""
    response = authenticated_client.get("/archive/chain")
    assert response.status_code == 200


def test_member_cannot_access_archive_doc(authenticated_client):
    """Regular member should get 403 on archive research documents."""
    response = authenticated_client.get("/archive/doc/governance/some-doc")
    # 403 (forbidden) or 404 (not found) — either is acceptable
    assert response.status_code in (403, 404)


def test_member_cannot_access_originals(authenticated_client):
    """Regular member should get 403 on archive originals."""
    response = authenticated_client.get("/archive/originals/test.pdf")
    assert response.status_code in (403, 404)


def test_arc_member_can_access_archive_doc(arc_client):
    """ARC member should access archive research documents."""
    response = arc_client.get("/archive/doc/governance/some-doc")
    # 200 or 404 (file may not exist) — but not 403
    assert response.status_code != 403


def test_board_member_can_access_archive_doc(board_client):
    """Board member should access archive research documents."""
    response = board_client.get("/archive/doc/governance/some-doc")
    assert response.status_code != 403
```

Note: `arc_client` fixture needed — authenticated client with ARC role.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_archive_routes.py -v`
Expected: FAIL — member gets 200 on research routes (no gate yet)

- [ ] **Step 3: Add access gate helper to archive routes**

In `cove/archive/routes.py`, add a decorator or inline check:

```python
from flask_login import current_user
from functools import wraps
from flask import abort

def arc_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not (current_user.is_arc or current_user.is_board or current_user.is_admin):
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

Apply `@arc_required` to these routes:
- `document()` (line 141)
- `data_file()` (line 167)
- `originals()` (line 188)
- `request_original()` (line 218)

Leave these routes member-accessible (no change):
- `index()` (line 29)
- `timeline()` (line 39)
- `chain()` (line 58)
- `bylaws()` (line 77)
- `catalog()` (line 96)

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_archive_routes.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/archive/routes.py tests/integration/test_archive_routes.py
git commit -m "feat: gate archive research routes to ARC/board/admin"
```

### Task 10: Update archive catalog to filter vault docs by tier

**Files:**
- Modify: `cove/archive/routes.py:96` (catalog route)
- Test: `tests/integration/test_archive_routes.py`

- [ ] **Step 1: Read the catalog route to understand how vault docs are merged**

Read `cove/archive/routes.py` catalog route (line 96) and trace how `parse_catalog_entries()` merges vault documents. Determine where the vault query happens.

- [ ] **Step 2: Write failing test**

Append to `tests/integration/test_archive_routes.py`:

```python
def test_catalog_does_not_leak_board_docs_to_member(authenticated_client, sample_tiered_docs):
    """Catalog should not show board-tier vault documents to regular members."""
    response = authenticated_client.get("/archive/catalog")
    assert response.status_code == 200
    assert b"Board Doc" not in response.data
```

- [ ] **Step 3: Add tier filtering to catalog route**

In the catalog route, compute `user_max_tier` using the shared `get_user_max_tier()` helper. Pass it to whatever query fetches vault documents for the merged catalog view. Filter vault docs by `TIER_HIERARCHY[user_max_tier]`.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_archive_routes.py::test_catalog_does_not_leak_board_docs_to_member -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/archive/routes.py tests/integration/test_archive_routes.py
git commit -m "feat: filter vault documents by tier in archive catalog"
```

---

## Chunk 5: Promote Action

### Task 11: Create PromoteDocumentForm

**Files:**
- Modify: `cove/archive/forms.py`
- Test: `tests/unit/test_vault_services.py`

- [ ] **Step 1: Write failing test for form**

Append to `tests/unit/test_vault_services.py`:

```python
def test_promote_form_has_required_fields(app):
    """Promote form should have title, category, access_tier, description."""
    with app.test_request_context():
        from cove.archive.forms import PromoteDocumentForm
        form = PromoteDocumentForm()
        assert hasattr(form, 'title')
        assert hasattr(form, 'category')
        assert hasattr(form, 'access_tier')
        assert hasattr(form, 'description')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_promote_form_has_required_fields -v`
Expected: FAIL — `ImportError: cannot import name 'PromoteDocumentForm'`

- [ ] **Step 3: Create PromoteDocumentForm**

In `cove/archive/forms.py`, add:

```python
from cove.vault.services import CATEGORIES

class PromoteDocumentForm(CoveForm):
    title = StringField(
        "Document Title",
        validators=[DataRequired(), Length(min=2, max=500)],
    )
    category = SelectField(
        "Category",
        choices=[(c, c.replace("_", " ").title()) for c in CATEGORIES],
        validators=[DataRequired()],
    )
    access_tier = SelectField(
        "Access Level",
        choices=[
            ("member", "All Members"),
            ("arc", "ARC Committee"),
            ("board", "Board Only"),
        ],
        default="member",
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=2000)],
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/unit/test_vault_services.py::test_promote_form_has_required_fields -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/archive/forms.py tests/unit/test_vault_services.py
git commit -m "feat: add PromoteDocumentForm for archive-to-vault promotion"
```

### Task 12: Add promote routes to archive blueprint

**Files:**
- Modify: `cove/archive/routes.py`
- Create: `cove/archive/templates/archive/promote.html`
- Test: `tests/integration/test_archive_routes.py`

- [ ] **Step 1: Write failing integration tests for promote flow**

Append to `tests/integration/test_archive_routes.py`:

```python
def test_member_cannot_access_promote(authenticated_client):
    """Regular member should get 403 on promote route."""
    response = authenticated_client.get("/archive/promote/test.pdf")
    assert response.status_code == 403


def test_arc_can_access_promote_form(arc_client):
    """ARC member should see promote form."""
    # This will 404 if the file doesn't exist, which is fine
    response = arc_client.get("/archive/promote/test.pdf")
    assert response.status_code in (200, 404)


def test_promote_creates_vault_document(arc_client, app, db_session):
    """Promoting an archive file should create a Document in the vault."""
    import os
    # Create a test file in archive originals
    archive_dir = os.path.join(app.root_path, "..", "docs", "archive", "originals")
    os.makedirs(archive_dir, exist_ok=True)
    test_file = os.path.join(archive_dir, "test_promote.pdf")
    with open(test_file, "wb") as f:
        f.write(b"%PDF-1.4 fake content")

    response = arc_client.post(
        "/archive/promote/test_promote.pdf",
        data={
            "title": "Promoted Test Doc",
            "category": "notices",
            "access_tier": "member",
            "description": "Test promotion",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    from sqlalchemy import select
    from cove.models.vault import Document
    doc = db_session.execute(select(Document).where(Document.title == "Promoted Test Doc")).scalar_one_or_none()
    assert doc is not None
    assert doc.access_tier == "member"
    assert doc.category == "notices"

    # Cleanup
    os.remove(test_file)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_archive_routes.py -v`
Expected: FAIL — 404 on promote routes (don't exist yet)

- [ ] **Step 3: Add promote GET route**

In `cove/archive/routes.py`, add:

```python
from cove.archive.forms import PromoteDocumentForm
from cove.archive.services import sanitize_path

@archive_bp.route("/promote/<path:filepath>", methods=["GET"])
@login_required
@arc_required
def promote_form(filepath):
    archive_root = _archive_root()
    originals_dir = os.path.join(archive_root, "originals")
    safe_path = sanitize_path(filepath, originals_dir)
    if not safe_path or not os.path.isfile(safe_path):
        abort(404)

    form = PromoteDocumentForm()
    # Pre-fill title from filename
    form.title.data = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ")

    # Filter access_tier choices by user role
    if current_user.is_board or current_user.is_admin:
        pass  # All choices available
    elif current_user.is_arc:
        form.access_tier.choices = [("member", "All Members"), ("arc", "ARC Committee")]
    else:
        form.access_tier.choices = [("member", "All Members")]

    return render_template("archive/promote.html", form=form, filepath=filepath, filename=os.path.basename(filepath))
```

- [ ] **Step 4: Add promote POST route**

```python
@archive_bp.route("/promote/<path:filepath>", methods=["POST"])
@login_required
@arc_required
def promote_submit(filepath):
    archive_root = _archive_root()
    originals_dir = os.path.join(archive_root, "originals")
    safe_path = sanitize_path(filepath, originals_dir)
    if not safe_path or not os.path.isfile(safe_path):
        abort(404)

    form = PromoteDocumentForm()
    if not form.validate_on_submit():
        return render_template("archive/promote.html", form=form, filepath=filepath, filename=os.path.basename(filepath))

    # Read file from archive
    with open(safe_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(filepath)

    from cove.vault.services import upload_document, get_user_max_tier, TIER_HIERARCHY
    from cove.models.vault import AccessTier

    user_max_tier = get_user_max_tier(current_user)

    doc = upload_document(
        org_id=current_user.organization_id,
        uploaded_by=current_user.id,
        filename=filename,
        file_data=file_data,
        title=form.title.data,
        category=form.category.data,
        description=form.description.data,
        access_tier=form.access_tier.data,
        user_max_tier=user_max_tier,
        upload_folder=current_app.config.get("UPLOAD_FOLDER", "uploads"),
    )

    if doc:
        flash(f"'{form.title.data}' promoted to Community Documents.", "success")
        return redirect(url_for("vault_bp.document", doc_id=doc.id))
    else:
        flash("You don't have permission to upload at that access level.", "error")
        return render_template("archive/promote.html", form=form, filepath=filepath, filename=os.path.basename(filepath))
```

- [ ] **Step 5: Create promote.html template**

Create `cove/archive/templates/archive/promote.html`:

```html
{% extends "base.html" %}

{% block title %}Promote to Community Documents{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <nav class="mb-6 text-sm text-gray-500">
        <a href="{{ url_for('archive_bp.index') }}" class="hover:text-cove-600">Archive</a>
        <span class="mx-2">/</span>
        <span>Promote Document</span>
    </nav>

    <div class="cove-card">
        <div class="cove-card-header">
            <h1 class="text-xl font-semibold">Promote to Community Documents</h1>
            <p class="text-sm text-gray-500 mt-1">Source: {{ filename }}</p>
        </div>
        <div class="cove-card-body">
            <form method="POST" action="{{ url_for('archive_bp.promote_submit', filepath=filepath) }}">
                {{ form.hidden_tag() }}

                <div class="mb-4">
                    {{ form.title.label(class="cove-label") }}
                    {{ form.title(class="cove-input") }}
                    {% for error in form.title.errors %}
                    <p class="text-red-500 text-sm mt-1">{{ error }}</p>
                    {% endfor %}
                </div>

                <div class="mb-4">
                    {{ form.category.label(class="cove-label") }}
                    {{ form.category(class="cove-input") }}
                </div>

                <div class="mb-4">
                    {{ form.access_tier.label(class="cove-label") }}
                    {{ form.access_tier(class="cove-input") }}
                </div>

                <div class="mb-6">
                    {{ form.description.label(class="cove-label") }}
                    {{ form.description(class="cove-input", rows="3") }}
                </div>

                <div class="flex gap-3">
                    <button type="submit" class="cove-btn cove-btn-primary">Promote</button>
                    <a href="{{ url_for('archive_bp.originals', filepath=filepath) }}" class="cove-btn cove-btn-secondary">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd ~/GrowDirect/Cove && python3 -m pytest tests/integration/test_archive_routes.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add cove/archive/routes.py cove/archive/forms.py cove/archive/templates/archive/promote.html tests/integration/test_archive_routes.py
git commit -m "feat: add promote-from-archive flow with form, routes, and template"
```

---

## Chunk 6: Final Verification

### Task 13: Run full regression and verify

- [ ] **Step 1: Run complete test suite**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/ -v --tb=short
```
Expected: All tests pass.

- [ ] **Step 2: Run migration on test database**

```bash
cd ~/GrowDirect/Cove && DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove_test python3 -m alembic upgrade head
```
Expected: No errors.

- [ ] **Step 3: Manual smoke test**

Start the app and verify:
1. `/vault/` shows tier tabs based on logged-in user role
2. Upload form has access_tier dropdown
3. Document detail shows tier badge
4. Regular member cannot access board-tier documents
5. `/archive/` landing accessible to all members
6. `/archive/doc/...` returns 403 for regular members
7. ARC/board members can access archive research docs
8. Promote button appears on archive originals for ARC/board users

- [ ] **Step 4: Final commit (if any uncommitted changes remain)**

```bash
git status
# Stage only relevant files — do not use git add -A
git commit -m "chore: final cleanup for documents archive redesign"
```
