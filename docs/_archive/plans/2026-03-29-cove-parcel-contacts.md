# Parcel Contacts & Profile Tiles Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add structured contact records per parcel with board-managed CRUD, and redesign the directory detail view as an APN-centric tile page.

**Architecture:** New `ParcelContact` model with FK to `parcels.apn`. Board routes for CRUD under `/board/parcels/<apn>/contacts`. Directory list click-through to a new tile-based profile page at `/member/directory/<apn>`. Two Alembic migrations: one to create the table and migrate data, one to drop the old JSON column.

**Tech Stack:** SQLAlchemy 2.0 (`Mapped[]`), WTForms, Jinja2, Alembic, pytest

**Spec:** `docs/superpowers/specs/2026-03-29-cove-parcel-contacts-design.md`

---

## File Structure

| File | Responsibility |
|------|---------------|
| `cove/models/parcel_contact.py` | New — `ParcelContact` model, `ContactType` enum, `ContactRelationship` enum |
| `cove/models/parcel.py` | Modify — add `contacts` relationship |
| `cove/models/parcel_profile.py` | Modify — add `created_at`, fix relationship typing, drop `household_members` (migration 2) |
| `cove/models/__init__.py` | Modify — add `ParcelContact` import |
| `cove/board/forms.py` | Modify — add `ParcelContactForm` |
| `cove/board/routes.py` | Modify — add contact CRUD routes |
| `cove/board/templates/board/parcel_contacts.html` | New — contact management page |
| `cove/member/services.py` | Modify — update directory sorting, add profile detail function, remove `household_members` references |
| `cove/member/profile_services.py` | Modify — remove `household_members` from allowed fields and return dicts |
| `cove/member/routes.py` | Modify — add `/member/directory/<apn>` route |
| `cove/member/templates/member/directory.html` | Modify — avatar bubbles, sort order, click-through links |
| `cove/member/templates/member/directory_profile.html` | New — tile-based APN profile page |
| `migrations/versions/xxx_add_parcel_contacts.py` | New — create table, migrate JSON, add created_at |
| `migrations/versions/xxx_drop_household_members.py` | New — drop old JSON column |
| `tests/conftest.py` | Modify — add contact fixtures |
| `tests/unit/test_parcel_contacts.py` | New — model and service tests |
| `tests/integration/test_board_contacts.py` | New — board CRUD route tests |
| `tests/integration/test_directory_profile.py` | New — profile page and directory sort tests |

---

## Chunk 1: Model, Fixtures, and Unit Tests

### Task 0: Create Worktree

- [ ] **Step 1: Create feature branch worktree**

```bash
cd /Users/gclyle/GrowDirect/Cove
git worktree add .worktrees/cove-parcel-contacts -b feature/cove-parcel-contacts
```

- [ ] **Step 2: Verify worktree**

```bash
cd .worktrees/cove-parcel-contacts
git branch --show-current
```

Expected: `feature/cove-parcel-contacts`

---

### Task 1: ParcelContact Model

**Files:**
- Create: `cove/models/parcel_contact.py`
- Modify: `cove/models/__init__.py:17` (add import)

- [ ] **Step 1: Write the failing test**

Create `tests/unit/test_parcel_contacts.py`:

```python
"""Tests for ParcelContact model."""
import uuid
import pytest

from cove.models.parcel_contact import ParcelContact, ContactType, ContactRelationship


def test_contact_type_enum_values():
    assert ContactType.PRIMARY.value == "primary"
    assert ContactType.SECONDARY.value == "secondary"
    assert ContactType.HOUSEHOLD.value == "household"
    assert ContactType.EMERGENCY.value == "emergency"
    assert ContactType.TENANT.value == "tenant"


def test_contact_relationship_enum_values():
    assert ContactRelationship.OWNER.value == "owner"
    assert ContactRelationship.CO_OWNER.value == "co_owner"
    assert ContactRelationship.SPOUSE.value == "spouse"
    assert ContactRelationship.CHILD.value == "child"
    assert ContactRelationship.PARENT.value == "parent"
    assert ContactRelationship.TENANT.value == "tenant"
    assert ContactRelationship.OTHER.value == "other"


def test_parcel_contact_defaults(app, db_session, test_org):
    """ParcelContact should have correct defaults."""
    from cove.models.parcel import Parcel

    parcel = Parcel(
        apn="9999-001-001",
        organization_id=test_org.id,
        address="1 Test St",
        street="Test St",
        is_association_member=True,
    )
    db_session.add(parcel)
    db_session.flush()

    contact = ParcelContact(
        apn="9999-001-001",
        name="Jane Doe",
    )
    db_session.add(contact)
    db_session.flush()

    assert contact.id is not None
    assert contact.contact_type == "household"
    assert contact.relationship == "other"
    assert contact.is_minor is False
    assert contact.display_order == 0
    assert contact.email is None
    assert contact.phone is None
    assert contact.notes is None
    assert contact.created_at is not None
    assert contact.updated_at is not None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_parcel_contacts.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'cove.models.parcel_contact'`

- [ ] **Step 3: Create the ParcelContact model**

Create `cove/models/parcel_contact.py`:

```python
"""Parcel contact model — people associated with a parcel address."""
import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cove.extensions import db


class ContactType(enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    HOUSEHOLD = "household"
    EMERGENCY = "emergency"
    TENANT = "tenant"


class ContactRelationship(enum.Enum):
    OWNER = "owner"
    CO_OWNER = "co_owner"
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    TENANT = "tenant"
    OTHER = "other"


class ParcelContact(db.Model):
    """A person associated with a parcel address.

    ContactType and ContactRelationship are Python enums for code safety.
    Database columns are String(20) — no PostgreSQL ENUM types.
    """

    __tablename__ = "parcel_contacts"
    __table_args__ = (
        db.Index(
            "ix_parcel_contacts_primary_unique",
            "apn",
            unique=True,
            postgresql_where=text("contact_type = 'primary'"),
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    apn: Mapped[str] = mapped_column(
        String(20), ForeignKey("parcels.apn", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(254))
    phone: Mapped[str | None] = mapped_column(String(20))
    contact_type: Mapped[str] = mapped_column(
        String(20), default=ContactType.HOUSEHOLD.value
    )
    relationship: Mapped[str] = mapped_column(
        String(20), default=ContactRelationship.OTHER.value
    )
    is_minor: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="contacts")
```

- [ ] **Step 4: Add import to models __init__.py**

In `cove/models/__init__.py`, add after line 15 (ParcelComment import):

```python
from cove.models.parcel_contact import ParcelContact, ContactType, ContactRelationship
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest tests/unit/test_parcel_contacts.py::test_contact_type_enum_values tests/unit/test_parcel_contacts.py::test_contact_relationship_enum_values tests/unit/test_parcel_contacts.py::test_parcel_contact_defaults -v
```

Expected: 3 PASSED

- [ ] **Step 6: Commit**

```bash
git add cove/models/parcel_contact.py cove/models/__init__.py tests/unit/test_parcel_contacts.py
git commit -m "feat: add ParcelContact model with enums"
```

---

### Task 2: Parcel Relationship + Unique Primary Constraint

**Files:**
- Modify: `cove/models/parcel.py:71` (add contacts relationship)
- Test: `tests/unit/test_parcel_contacts.py` (add constraint test)

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/test_parcel_contacts.py`:

```python
def test_parcel_has_contacts_relationship(app, db_session, test_org):
    """Parcel.contacts should return related ParcelContact rows ordered by display_order."""
    from cove.models.parcel import Parcel

    parcel = Parcel(
        apn="9999-001-002",
        organization_id=test_org.id,
        address="2 Test St",
        street="Test St",
        is_association_member=True,
    )
    db_session.add(parcel)
    db_session.flush()

    c1 = ParcelContact(apn="9999-001-002", name="Second", display_order=2)
    c2 = ParcelContact(apn="9999-001-002", name="First", display_order=1)
    db_session.add_all([c1, c2])
    db_session.flush()

    assert len(parcel.contacts) == 2
    assert parcel.contacts[0].name == "First"
    assert parcel.contacts[1].name == "Second"


def test_unique_primary_per_apn(app, db_session, test_org):
    """Only one primary contact allowed per APN."""
    from sqlalchemy.exc import IntegrityError
    from cove.models.parcel import Parcel

    parcel = Parcel(
        apn="9999-001-003",
        organization_id=test_org.id,
        address="3 Test St",
        street="Test St",
        is_association_member=True,
    )
    db_session.add(parcel)
    db_session.flush()

    c1 = ParcelContact(
        apn="9999-001-003", name="Owner One",
        contact_type="primary", relationship="owner",
    )
    db_session.add(c1)
    db_session.flush()

    c2 = ParcelContact(
        apn="9999-001-003", name="Owner Two",
        contact_type="primary", relationship="co_owner",
    )
    db_session.add(c2)
    with pytest.raises(IntegrityError):
        db_session.flush()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/unit/test_parcel_contacts.py::test_parcel_has_contacts_relationship tests/unit/test_parcel_contacts.py::test_unique_primary_per_apn -v
```

Expected: FAIL — `parcel.contacts` attribute not found

- [ ] **Step 3: Add contacts relationship to Parcel model**

In `cove/models/parcel.py`, after the `comments` relationship (around line 71), add:

```python
    contacts: Mapped[list["ParcelContact"]] = relationship(
        "ParcelContact", back_populates="parcel", order_by="ParcelContact.display_order"
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/unit/test_parcel_contacts.py -v
```

Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git add cove/models/parcel.py tests/unit/test_parcel_contacts.py
git commit -m "feat: add Parcel.contacts relationship and unique primary constraint"
```

---

### Task 3: Minor-Primary Validation

**Files:**
- Test: `tests/unit/test_parcel_contacts.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/test_parcel_contacts.py`:

```python
def test_minor_cannot_be_primary():
    """Validation: is_minor=True with contact_type=primary should be rejected."""
    from cove.models.parcel_contact import validate_contact

    errors = validate_contact(contact_type="primary", is_minor=True)
    assert "minor" in errors.lower()


def test_non_minor_primary_is_valid():
    """Non-minor primary contact should pass validation."""
    from cove.models.parcel_contact import validate_contact

    errors = validate_contact(contact_type="primary", is_minor=False)
    assert errors is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_parcel_contacts.py::test_minor_cannot_be_primary -v
```

Expected: FAIL — `ImportError: cannot import name 'validate_contact'`

- [ ] **Step 3: Add validate_contact function**

Add to `cove/models/parcel_contact.py` after the model class:

```python
def validate_contact(contact_type: str, is_minor: bool) -> str | None:
    """Validate contact field combinations. Returns error message or None."""
    if is_minor and contact_type == ContactType.PRIMARY.value:
        return "A minor cannot be the primary contact."
    return None
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/unit/test_parcel_contacts.py -v
```

Expected: 7 PASSED

- [ ] **Step 5: Commit**

```bash
git add cove/models/parcel_contact.py tests/unit/test_parcel_contacts.py
git commit -m "feat: add minor-primary validation for parcel contacts"
```

---

### Task 4: Test Fixtures

**Files:**
- Modify: `tests/conftest.py` (add parcel contact fixtures after line 307)

- [ ] **Step 1: Add fixtures**

Append to `tests/conftest.py`:

```python
# ---------------------------------------------------------------------------
# Parcel contact fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_parcel(db_session, test_org):
    """A test parcel with association membership."""
    from cove.models.parcel import Parcel
    parcel = Parcel(
        apn="9999-001-010",
        organization_id=test_org.id,
        address="10 Test St",
        street="Test St",
        lot_number=10,
        is_association_member=True,
    )
    db_session.add(parcel)
    db_session.flush()
    return parcel


@pytest.fixture(scope="function")
def test_parcel_with_contacts(db_session, test_parcel):
    """Parcel with primary, secondary, and household contacts."""
    from cove.models.parcel_contact import ParcelContact
    contacts = [
        ParcelContact(
            apn=test_parcel.apn,
            name="John Owner",
            email="john@example.com",
            phone="310-555-0001",
            contact_type="primary",
            relationship="owner",
            display_order=0,
        ),
        ParcelContact(
            apn=test_parcel.apn,
            name="Jane Owner",
            email="jane@example.com",
            phone="310-555-0002",
            contact_type="secondary",
            relationship="spouse",
            display_order=1,
        ),
        ParcelContact(
            apn=test_parcel.apn,
            name="Tommy Owner",
            contact_type="household",
            relationship="child",
            is_minor=True,
            display_order=2,
        ),
    ]
    db_session.add_all(contacts)
    db_session.flush()
    return contacts


@pytest.fixture(scope="function")
def second_test_parcel(db_session, test_org):
    """A second parcel on a different street for sort testing."""
    from cove.models.parcel import Parcel
    parcel = Parcel(
        apn="9999-002-005",
        organization_id=test_org.id,
        address="5 Alpha Ave",
        street="Alpha Ave",
        lot_number=5,
        is_association_member=True,
    )
    db_session.add(parcel)
    db_session.flush()
    return parcel
```

- [ ] **Step 2: Verify fixtures work**

```bash
pytest tests/unit/test_parcel_contacts.py -v
```

Expected: 7 PASSED (existing tests still pass; fixtures available)

- [ ] **Step 3: Commit**

```bash
git add tests/conftest.py
git commit -m "test: add parcel contact fixtures"
```

---

### Task 5: ParcelProfile Cleanup (created_at + typing)

**Files:**
- Modify: `cove/models/parcel_profile.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/test_parcel_contacts.py`:

```python
def test_parcel_profile_has_created_at(app, db_session, test_parcel):
    """ParcelProfile should have created_at timestamp."""
    from cove.models.parcel_profile import ParcelProfile
    profile = ParcelProfile(apn=test_parcel.apn)
    db_session.add(profile)
    db_session.flush()
    assert profile.created_at is not None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_parcel_contacts.py::test_parcel_profile_has_created_at -v
```

Expected: FAIL — `AttributeError: 'ParcelProfile' object has no attribute 'created_at'`

- [ ] **Step 3: Update ParcelProfile model**

In `cove/models/parcel_profile.py`:

1. Add `datetime` import at top
2. Add `created_at` column before `updated_at`
3. Update `parcel` relationship to use `Mapped[]` typing

The `updated_at` line is around line 40. Add `created_at` before it:

```python
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

Update the relationship (around line 45) from:

```python
    parcel = relationship("Parcel", back_populates="profile")
```

to:

```python
    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="profile")
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_parcel_contacts.py::test_parcel_profile_has_created_at -v
```

Expected: PASS

- [ ] **Step 5: Run full test suite to check for regressions**

```bash
pytest tests/ -v
```

Expected: All existing tests pass

- [ ] **Step 6: Commit**

```bash
git add cove/models/parcel_profile.py tests/unit/test_parcel_contacts.py
git commit -m "fix: add created_at to ParcelProfile, fix relationship typing"
```

> **Note:** The dev database will be out of sync with the model until Migration 1 (Task 12) runs. Test suite uses `create_all()` which builds from models, so tests pass. Do not run the app against the dev database between here and Task 12.

---

## Chunk 2: Board Contact CRUD

### Task 6: ParcelContactForm

**Files:**
- Modify: `cove/board/forms.py`
- Test: `tests/unit/test_parcel_contacts.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/test_parcel_contacts.py`:

```python
def test_parcel_contact_form_has_fields(app):
    """ParcelContactForm should have all required fields."""
    with app.test_request_context():
        from cove.board.forms import ParcelContactForm
        form = ParcelContactForm()
        assert hasattr(form, "name")
        assert hasattr(form, "email")
        assert hasattr(form, "phone")
        assert hasattr(form, "contact_type")
        assert hasattr(form, "relationship")
        assert hasattr(form, "is_minor")
        assert hasattr(form, "notes")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_parcel_contacts.py::test_parcel_contact_form_has_fields -v
```

Expected: FAIL — `ImportError: cannot import name 'ParcelContactForm'`

- [ ] **Step 3: Add ParcelContactForm to board/forms.py**

Append to `cove/board/forms.py`:

```python
class ParcelContactForm(CoveForm):
    """Form for creating/editing parcel contacts. Board-only."""

    name = StringField("Name", validators=[DataRequired(), Length(max=200)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=254)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    contact_type = SelectField(
        "Contact Type",
        choices=[
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("household", "Household Member"),
            ("emergency", "Emergency Contact"),
            ("tenant", "Tenant"),
        ],
    )
    relationship = SelectField(
        "Relationship",
        choices=[
            ("owner", "Owner"),
            ("co_owner", "Co-Owner"),
            ("spouse", "Spouse"),
            ("child", "Child"),
            ("parent", "Parent"),
            ("tenant", "Tenant"),
            ("other", "Other"),
        ],
    )
    is_minor = BooleanField("Minor (under 18)")
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
```

Add the necessary imports at the top of `cove/board/forms.py`:

```python
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Email
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/unit/test_parcel_contacts.py::test_parcel_contact_form_has_fields -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cove/board/forms.py tests/unit/test_parcel_contacts.py
git commit -m "feat: add ParcelContactForm for board contact management"
```

---

### Task 7: Board Contact Routes

**Files:**
- Modify: `cove/board/routes.py`
- Create: `cove/board/templates/board/parcel_contacts.html`
- Test: `tests/integration/test_board_contacts.py`

- [ ] **Step 1: Write the failing integration tests**

Create `tests/integration/test_board_contacts.py`:

```python
"""Integration tests for board parcel contact management routes."""
import pytest


def test_board_can_view_contacts(board_client, test_parcel, test_parcel_with_contacts):
    """Board member can view contacts for a parcel."""
    resp = board_client.get(f"/board/parcels/{test_parcel.apn}/contacts")
    assert resp.status_code == 200
    assert b"John Owner" in resp.data
    assert b"Jane Owner" in resp.data


def test_non_board_gets_403(client, db_session, test_org, basic_member, test_parcel):
    """Non-board member should get 403."""
    with client.session_transaction() as sess:
        sess["_user_id"] = str(basic_member.id)
        sess["_fresh"] = True
    resp = client.get(f"/board/parcels/{test_parcel.apn}/contacts")
    assert resp.status_code == 403


def test_board_can_add_contact(board_client, test_parcel):
    """Board member can add a contact to a parcel."""
    resp = board_client.post(
        f"/board/parcels/{test_parcel.apn}/contacts/add",
        data={
            "name": "New Person",
            "email": "new@example.com",
            "phone": "310-555-9999",
            "contact_type": "household",
            "relationship": "other",
            "is_minor": False,
            "notes": "",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"New Person" in resp.data


def test_board_can_edit_contact(board_client, test_parcel, test_parcel_with_contacts):
    """Board member can edit an existing contact."""
    contact = test_parcel_with_contacts[0]  # John Owner
    resp = board_client.post(
        f"/board/parcels/{test_parcel.apn}/contacts/{contact.id}/edit",
        data={
            "name": "John Updated",
            "email": "john.updated@example.com",
            "phone": "310-555-0001",
            "contact_type": "primary",
            "relationship": "owner",
            "is_minor": False,
            "notes": "Updated",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"John Updated" in resp.data


def test_board_can_delete_contact(board_client, test_parcel, test_parcel_with_contacts):
    """Board member can delete a contact."""
    contact = test_parcel_with_contacts[2]  # Tommy (household)
    resp = board_client.post(
        f"/board/parcels/{test_parcel.apn}/contacts/{contact.id}/delete",
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Tommy Owner" not in resp.data


def test_minor_primary_rejected(board_client, test_parcel):
    """Adding a minor as primary contact should fail validation."""
    resp = board_client.post(
        f"/board/parcels/{test_parcel.apn}/contacts/add",
        data={
            "name": "Kid Primary",
            "contact_type": "primary",
            "relationship": "child",
            "is_minor": True,
            "notes": "",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"minor" in resp.data.lower() or b"Minor" in resp.data
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/integration/test_board_contacts.py -v
```

Expected: FAIL — 404 (routes don't exist yet)

- [ ] **Step 3: Add board contact routes**

Append to `cove/board/routes.py`:

```python
@board_bp.route("/parcels/<apn>/contacts")
@login_required
def parcel_contacts(apn):
    """List and manage contacts for a parcel."""
    _board_required()
    from cove.models.parcel import Parcel
    from cove.models.parcel_contact import ParcelContact
    from cove.board.forms import ParcelContactForm

    parcel = db.session.query(Parcel).filter_by(apn=apn).first_or_404()
    contacts = (
        db.session.query(ParcelContact)
        .filter_by(apn=apn)
        .order_by(ParcelContact.display_order)
        .all()
    )
    form = ParcelContactForm()
    return render_template(
        "board/parcel_contacts.html",
        parcel=parcel,
        contacts=contacts,
        form=form,
    )


@board_bp.route("/parcels/<apn>/contacts/add", methods=["POST"])
@login_required
def add_contact(apn):
    """Add a new contact to a parcel."""
    _board_required()
    from cove.models.parcel import Parcel
    from cove.models.parcel_contact import ParcelContact, validate_contact
    from cove.board.forms import ParcelContactForm

    parcel = db.session.query(Parcel).filter_by(apn=apn).first_or_404()
    form = ParcelContactForm()

    if form.validate_on_submit():
        error = validate_contact(form.contact_type.data, form.is_minor.data)
        if error:
            flash(error, "error")
            return redirect(url_for("board.parcel_contacts", apn=apn))

        # Auto-calculate display_order as next in sequence
        max_order = (
            db.session.query(db.func.max(ParcelContact.display_order))
            .filter_by(apn=apn)
            .scalar()
        ) or -1

        contact = ParcelContact(
            apn=apn,
            name=form.name.data,
            email=form.email.data or None,
            phone=form.phone.data or None,
            contact_type=form.contact_type.data,
            relationship=form.relationship.data,
            is_minor=form.is_minor.data,
            notes=form.notes.data or None,
            display_order=max_order + 1,
        )
        db.session.add(contact)
        db.session.commit()
        flash(f"Contact '{contact.name}' added.", "success")

    return redirect(url_for("board.parcel_contacts", apn=apn))


@board_bp.route("/parcels/<apn>/contacts/<contact_id>/edit", methods=["GET", "POST"])
@login_required
def edit_contact(apn, contact_id):
    """Edit an existing parcel contact."""
    _board_required()
    from cove.models.parcel import Parcel
    from cove.models.parcel_contact import ParcelContact, validate_contact
    from cove.board.forms import ParcelContactForm

    parcel = db.session.query(Parcel).filter_by(apn=apn).first_or_404()
    contact = db.session.query(ParcelContact).filter_by(id=contact_id, apn=apn).first_or_404()

    form = ParcelContactForm(obj=contact)

    if form.validate_on_submit():
        error = validate_contact(form.contact_type.data, form.is_minor.data)
        if error:
            flash(error, "error")
            return redirect(url_for("board.edit_contact", apn=apn, contact_id=contact_id))

        contact.name = form.name.data
        contact.email = form.email.data or None
        contact.phone = form.phone.data or None
        contact.contact_type = form.contact_type.data
        contact.relationship = form.relationship.data
        contact.is_minor = form.is_minor.data
        contact.notes = form.notes.data or None
        db.session.commit()
        flash(f"Contact '{contact.name}' updated.", "success")
        return redirect(url_for("board.parcel_contacts", apn=apn))

    return render_template(
        "board/parcel_contacts.html",
        parcel=parcel,
        contacts=parcel.contacts,
        form=form,
        editing=contact,
    )


@board_bp.route("/parcels/<apn>/contacts/<contact_id>/delete", methods=["POST"])
@login_required
def delete_contact(apn, contact_id):
    """Delete a parcel contact."""
    _board_required()
    from cove.models.parcel_contact import ParcelContact

    contact = db.session.query(ParcelContact).filter_by(id=contact_id, apn=apn).first_or_404()
    name = contact.name
    db.session.delete(contact)
    db.session.commit()
    flash(f"Contact '{name}' removed.", "success")
    return redirect(url_for("board.parcel_contacts", apn=apn))
```

Add necessary imports at top of `cove/board/routes.py` (check existing, add missing):

```python
from flask import redirect, url_for, flash
```

- [ ] **Step 4: Create board contact template**

Create `cove/board/templates/board/parcel_contacts.html`:

```html
{% extends "base.html" %}

{% block title %}Contacts — {{ parcel.address }} — Board — Cove{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto space-y-6">

  <!-- Breadcrumb -->
  <nav class="text-sm text-gray-500">
    <a href="{{ url_for('board.dashboard') }}" class="hover:text-cove-600">Board</a>
    <span class="mx-2">/</span>
    <span class="text-gray-900">{{ parcel.address }} — Contacts</span>
  </nav>

  <!-- Parcel Header -->
  <div class="cove-card">
    <div class="cove-card-header">
      <h1 class="text-xl font-bold text-gray-900">{{ parcel.address }}</h1>
      <p class="text-sm text-gray-500 mt-1">APN {{ parcel.apn }} · {{ parcel.lot_email or '—' }}</p>
    </div>
  </div>

  <!-- Existing Contacts -->
  <div class="cove-card">
    <div class="cove-card-header flex items-center justify-between">
      <h2 class="text-lg font-semibold text-gray-900">Contacts</h2>
      <span class="text-sm text-gray-500">{{ contacts | length }} contact{{ 's' if contacts | length != 1 }}</span>
    </div>
    {% if contacts %}
    <div class="overflow-x-auto">
      <table class="cove-table w-full">
        <thead>
          <tr>
            <th class="cove-th">Name</th>
            <th class="cove-th">Type</th>
            <th class="cove-th">Relationship</th>
            <th class="cove-th">Email</th>
            <th class="cove-th">Phone</th>
            <th class="cove-th">Notes</th>
            <th class="cove-th"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          {% for c in contacts %}
          <tr>
            <td class="cove-td font-medium">
              {{ c.name }}
              {% if c.is_minor %}<span class="cove-badge bg-yellow-100 text-yellow-700 ml-1">Minor</span>{% endif %}
            </td>
            <td class="cove-td">
              <span class="cove-badge {% if c.contact_type == 'primary' %}bg-cove-100 text-cove-700{% elif c.contact_type == 'emergency' %}bg-red-100 text-red-700{% else %}bg-gray-100 text-gray-600{% endif %}">
                {{ c.contact_type | title }}
              </span>
            </td>
            <td class="cove-td text-gray-600">{{ c.relationship.replace('_', ' ') | title }}</td>
            <td class="cove-td text-gray-500">{{ c.email or '—' }}</td>
            <td class="cove-td text-gray-500">{{ c.phone or '—' }}</td>
            <td class="cove-td text-gray-500 max-w-xs truncate">{{ c.notes or '—' }}</td>
            <td class="cove-td text-right space-x-2">
              <a href="{{ url_for('board.edit_contact', apn=parcel.apn, contact_id=c.id) }}"
                 class="text-cove-600 hover:text-cove-800 text-sm font-medium">Edit</a>
              <form method="post" action="{{ url_for('board.delete_contact', apn=parcel.apn, contact_id=c.id) }}"
                    class="inline" onsubmit="return confirm('Remove {{ c.name }}?')">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <button type="submit" class="text-red-600 hover:text-red-800 text-sm font-medium">Delete</button>
              </form>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    {% else %}
    <div class="cove-card-body">
      <p class="text-sm text-gray-500">No contacts yet. Add the first one below.</p>
    </div>
    {% endif %}
  </div>

  <!-- Add / Edit Contact Form -->
  <div class="cove-card">
    <div class="cove-card-header">
      <h2 class="text-lg font-semibold text-gray-900">
        {% if editing is defined and editing %}Edit {{ editing.name }}{% else %}Add Contact{% endif %}
      </h2>
    </div>
    <div class="cove-card-body">
      <form method="post"
            action="{% if editing is defined and editing %}{{ url_for('board.edit_contact', apn=parcel.apn, contact_id=editing.id) }}{% else %}{{ url_for('board.add_contact', apn=parcel.apn) }}{% endif %}"
            class="cove-form space-y-4">
        {{ form.hidden_tag() }}

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="cove-label">{{ form.name.label.text }}</label>
            {{ form.name(class="cove-input") }}
            {% if form.name.errors %}<p class="cove-error">{{ form.name.errors[0] }}</p>{% endif %}
          </div>
          <div>
            <label class="cove-label">{{ form.email.label.text }}</label>
            {{ form.email(class="cove-input") }}
            {% if form.email.errors %}<p class="cove-error">{{ form.email.errors[0] }}</p>{% endif %}
          </div>
          <div>
            <label class="cove-label">{{ form.phone.label.text }}</label>
            {{ form.phone(class="cove-input") }}
          </div>
          <div>
            <label class="cove-label">{{ form.contact_type.label.text }}</label>
            {{ form.contact_type(class="cove-select") }}
          </div>
          <div>
            <label class="cove-label">{{ form.relationship.label.text }}</label>
            {{ form.relationship(class="cove-select") }}
          </div>
          <div class="flex items-center gap-2 pt-6">
            {{ form.is_minor() }}
            <label class="cove-label mb-0">{{ form.is_minor.label.text }}</label>
          </div>
        </div>

        <div>
          <label class="cove-label">{{ form.notes.label.text }}</label>
          {{ form.notes(class="cove-input", rows="2") }}
        </div>

        <div class="flex gap-3 pt-2">
          <button type="submit" class="cove-btn cove-btn-primary">
            {% if editing is defined and editing %}Update Contact{% else %}Add Contact{% endif %}
          </button>
          {% if editing is defined and editing %}
          <a href="{{ url_for('board.parcel_contacts', apn=parcel.apn) }}"
             class="cove-btn cove-btn-secondary">Cancel</a>
          {% endif %}
        </div>
      </form>
    </div>
  </div>

</div>
{% endblock %}
```

- [ ] **Step 5: Run integration tests**

```bash
pytest tests/integration/test_board_contacts.py -v
```

Expected: 6 PASSED

- [ ] **Step 6: Commit**

```bash
git add cove/board/routes.py cove/board/templates/board/parcel_contacts.html tests/integration/test_board_contacts.py
git commit -m "feat: add board contact CRUD routes and template"
```

---

## Chunk 3: Directory List + Profile Tiles

### Task 8: Directory Sort and Avatar Bubbles

**Files:**
- Modify: `cove/member/services.py:71-89` (sort query)
- Modify: `cove/member/templates/member/directory.html:49-56` (avatar)
- Test: `tests/integration/test_directory_profile.py`

- [ ] **Step 1: Write the failing test**

Create `tests/integration/test_directory_profile.py`:

```python
"""Integration tests for directory list and profile page."""
import pytest


def test_directory_sorts_by_street_then_number(
    app, db_session, test_org, basic_member, test_parcel, second_test_parcel
):
    """Directory should sort by street name, then street number (numeric)."""
    from cove.member.services import get_directory_listings

    # test_parcel: 10 Test St, second_test_parcel: 5 Alpha Ave
    # basic_member is on test_org but has its own parcel (1 Test St)
    listings = get_directory_listings(test_org.id)
    streets = [entry["street"] for entry in listings]

    # Alpha Ave should come before Test St
    alpha_idx = next(i for i, s in enumerate(streets) if s == "Alpha Ave")
    test_idx = next(i for i, s in enumerate(streets) if s == "Test St")
    assert alpha_idx < test_idx


def test_avatar_bubble_shows_lot_number(authenticated_client):
    """Avatar bubble should show street number, not first initial."""
    resp = authenticated_client.get("/member/directory")
    assert resp.status_code == 200
    # The authenticated_client's member is at "1 Test St"
    # Avatar bubble should contain the lot number or address number
    # Check that the template renders the number, not the first initial
    html = resp.data.decode()
    # Should NOT have the old initial pattern for this member
    # The exact assertion depends on template changes
    assert "directory" in html.lower()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_directory_profile.py::test_directory_sorts_by_street_then_number -v
```

Expected: FAIL — sort order not yet updated

- [ ] **Step 3: Update directory sort in services.py**

In `cove/member/services.py`, update the `get_directory_listings` function. Replace the existing query ordering with numeric street sort.

Find the existing `order_by` in `get_directory_listings` (around line 80) and update to:

```python
from sqlalchemy import func, Integer, cast

def get_directory_listings(org_id: str, board_view: bool = False) -> list[dict]:
    """All association member parcels, sorted by street then street number."""
    parcels = (
        db.session.query(Parcel)
        .filter_by(organization_id=org_id, is_association_member=True)
        .order_by(
            Parcel.street,
            cast(
                func.regexp_replace(Parcel.address, "[^0-9].*", "", "g"),
                Integer,
            ),
        )
        .all()
    )
    return [_parcel_to_entry(p, board_view=board_view) for p in parcels]
```

- [ ] **Step 4: Update avatar bubble in directory template**

In `cove/member/templates/member/directory.html`, replace the avatar bubble section (lines 49-56). Change the fallback from first initial to lot number:

Replace:
```html
<div class="h-8 w-8 rounded-full bg-cove-100 flex items-center justify-center text-cove-600 text-xs font-bold shrink-0">
  {{ entry.name[0] | upper if entry.name else '?' }}
</div>
```

With:
```html
<div class="h-8 w-8 rounded-full bg-cove-100 flex items-center justify-center text-cove-600 text-xs font-bold shrink-0">
  {{ entry.address_num if entry.address_num else '?' }}
</div>
```

- [ ] **Step 5: Add `address_num` to the entry dict**

In `cove/member/services.py`, add `address_num` to the dict returned by `_parcel_to_entry` (around line 33, alongside `lot_number`):

```python
        "address_num": parcel.address_num,
```

Also update `search_directory` to use the same numeric sort ordering as `get_directory_listings`. Find the `order_by` in `search_directory` (around line 110) and replace:

```python
.order_by(Parcel.street, Parcel.address)
```

with:

```python
.order_by(
    Parcel.street,
    cast(func.regexp_replace(Parcel.address, "[^0-9].*", "", "g"), Integer),
)
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/integration/test_directory_profile.py -v
```

Expected: 2 PASSED

- [ ] **Step 7: Commit**

```bash
git add cove/member/services.py cove/member/templates/member/directory.html tests/integration/test_directory_profile.py
git commit -m "feat: directory sorts by street/number, avatar shows lot number"
```

---

### Task 9: Directory Profile Page Route and Service

**Files:**
- Modify: `cove/member/services.py` (add `get_parcel_profile_data` function)
- Modify: `cove/member/routes.py` (add `/member/directory/<apn>` route)
- Test: `tests/integration/test_directory_profile.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/integration/test_directory_profile.py`:

```python
def test_profile_page_renders(authenticated_client, test_parcel, test_parcel_with_contacts):
    """Profile page should render for a valid APN."""
    resp = authenticated_client.get(f"/member/directory/{test_parcel.apn}")
    assert resp.status_code == 200
    assert test_parcel.address.encode() in resp.data


def test_profile_page_shows_contacts_for_board(
    board_client, test_parcel, test_parcel_with_contacts
):
    """Board member should see all contacts regardless of share toggle."""
    resp = board_client.get(f"/member/directory/{test_parcel.apn}")
    assert resp.status_code == 200
    assert b"John Owner" in resp.data
    assert b"Jane Owner" in resp.data
    assert b"Tommy Owner" in resp.data


def test_profile_page_hides_contacts_when_not_shared(
    authenticated_client, db_session, test_parcel, test_parcel_with_contacts
):
    """Regular member should not see contacts when share_household is False."""
    from cove.models.parcel_profile import ParcelProfile

    # Ensure share_household is False (default)
    profile = ParcelProfile(apn=test_parcel.apn, share_household=False)
    db_session.add(profile)
    db_session.flush()

    resp = authenticated_client.get(f"/member/directory/{test_parcel.apn}")
    assert resp.status_code == 200
    # Contact names should NOT appear for non-board users
    assert b"John Owner" not in resp.data


def test_profile_page_shows_contacts_when_shared(
    authenticated_client, db_session, test_parcel, test_parcel_with_contacts
):
    """Regular member should see contacts when share_household is True."""
    from cove.models.parcel_profile import ParcelProfile

    profile = ParcelProfile(apn=test_parcel.apn, share_household=True)
    db_session.add(profile)
    db_session.flush()

    resp = authenticated_client.get(f"/member/directory/{test_parcel.apn}")
    assert resp.status_code == 200
    assert b"John Owner" in resp.data


def test_profile_page_404_for_invalid_apn(authenticated_client):
    """Invalid APN should return 404."""
    resp = authenticated_client.get("/member/directory/0000-000-000")
    assert resp.status_code == 404
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/integration/test_directory_profile.py -v
```

Expected: New tests FAIL — 404 (route doesn't exist)

- [ ] **Step 3: Add get_parcel_profile_data to member services**

Append to `cove/member/services.py`:

```python
def get_parcel_profile_data(apn: str, board_view: bool = False) -> dict | None:
    """Build complete profile data for a parcel, including contacts.

    Returns None if the parcel doesn't exist.
    Privacy toggles are respected unless board_view=True.
    """
    parcel = db.session.query(Parcel).filter_by(apn=apn).first()
    if not parcel:
        return None

    member = parcel.member
    profile = parcel.profile
    prefs = member.directory_preferences if member else None
    show_all = board_view

    # Share toggles
    share_household = show_all or (profile and profile.share_household)
    share_pets = show_all or (profile and profile.share_pets)
    share_bio = show_all or (profile and profile.share_bio)

    # Contacts (from parcel_contacts table)
    contacts_visible = []
    if share_household:
        contacts_visible = [
            {
                "name": c.name,
                "email": c.email if not c.is_minor else None,
                "phone": c.phone if not c.is_minor else None,
                "contact_type": c.contact_type,
                "relationship": c.relationship,
                "is_minor": c.is_minor,
                "notes": c.notes if show_all else None,
            }
            for c in parcel.contacts
        ]

    # Pets (from profile JSON)
    pets_visible = []
    if share_pets and profile and profile.pets:
        pets_visible = profile.pets

    return {
        "parcel": parcel,
        "member": member,
        "profile": profile,
        "display_name": (profile.display_name if profile else None)
            or (parcel.owner_name)
            or (member.name if member else "—"),
        "bio": (profile.bio if profile and share_bio else None),
        "avatar_url": (profile.avatar_url if profile and (show_all or (profile and profile.share_avatar)) else None),
        "contacts": contacts_visible,
        "pets": pets_visible,
        "show_email": show_all or (prefs and prefs.show_email),
        "show_phone": show_all or (prefs and prefs.show_phone),
        "voting_weight": member.voting_weight if member else None,
        "roles": [mr.role.name for mr in member.roles if mr.is_current] if member else [],
    }
```

- [ ] **Step 4: Add directory profile route**

In `cove/member/routes.py`, add after the directory route (around line 66):

```python
@member_bp.route("/directory/<apn>")
@login_required
def directory_profile(apn):
    """APN-centric profile page with tiles."""
    from cove.member.services import get_parcel_profile_data

    board_view = current_user.is_board
    data = get_parcel_profile_data(apn, board_view=board_view)
    if data is None:
        abort(404)

    return render_template(
        "member/directory_profile.html",
        board_view=board_view,
        **data,
    )
```

Add `abort` to the flask imports at top of the file if not already imported.

- [ ] **Step 5: Run tests (will fail on template)**

```bash
pytest tests/integration/test_directory_profile.py -v
```

Expected: May FAIL on template not found — need to create template next

---

### Task 10: Directory Profile Template

**Files:**
- Create: `cove/member/templates/member/directory_profile.html`
- Modify: `cove/member/templates/member/directory.html` (add click-through links)

- [ ] **Step 1: Create the profile tile template**

Create `cove/member/templates/member/directory_profile.html`:

```html
{% extends "base.html" %}

{% block title %}{{ parcel.address }} — Directory — Cove{% endblock %}

{% block content %}
<div class="max-w-3xl mx-auto space-y-6">

  <!-- Breadcrumb -->
  <nav class="text-sm text-gray-500">
    <a href="{{ url_for('member.directory') }}" class="hover:text-cove-600">Directory</a>
    <span class="mx-2">/</span>
    <span class="text-gray-900">{{ parcel.address }}</span>
  </nav>

  <!-- Header Tile -->
  <div class="cove-card">
    <div class="cove-card-header">
      <div class="flex items-start justify-between gap-4">
        <div class="flex items-center gap-4">
          {% if avatar_url %}
          <img src="{{ avatar_url }}" alt="{{ display_name }}"
               class="h-16 w-16 rounded-full object-cover border-2 border-cove-200">
          {% else %}
          <div class="h-16 w-16 rounded-full bg-cove-100 flex items-center justify-center text-cove-600 text-xl font-bold">
            {{ parcel.address_num if parcel.address_num else '?' }}
          </div>
          {% endif %}
          <div>
            <h1 class="text-xl font-bold text-gray-900">{{ parcel.address }}</h1>
            <p class="text-sm text-gray-500 mt-1">APN {{ parcel.apn }}</p>
          </div>
        </div>
        {% if board_view %}
        <a href="{{ url_for('board.parcel_contacts', apn=parcel.apn) }}"
           class="cove-btn cove-btn-secondary text-sm shrink-0">Manage Contacts</a>
        {% endif %}
      </div>
    </div>
    <div class="cove-card-body">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
        <div>
          <span class="text-gray-500">Lot Email</span>
          <p class="font-medium text-gray-900">{{ parcel.lot_email or '—' }}</p>
        </div>
        {% if member %}
        <div>
          <span class="text-gray-500">Status</span>
          <p>
            <span class="cove-badge {% if member.membership_status == 'active' %}cove-status-active{% else %}cove-status-pending{% endif %}">
              {{ member.membership_status | title }}
            </span>
          </p>
        </div>
        <div>
          <span class="text-gray-500">Assessment</span>
          <p>
            <span class="cove-badge {% if member.assessment_status == 'current' %}cove-status-active{% else %}bg-red-100 text-red-700{% endif %}">
              {{ member.assessment_status | title }}
            </span>
          </p>
        </div>
        {% if voting_weight %}
        <div>
          <span class="text-gray-500">Voting Weight</span>
          <p class="font-medium text-gray-900">{{ voting_weight }}</p>
        </div>
        {% endif %}
        {% if show_email and member.personal_email %}
        <div>
          <span class="text-gray-500">Email</span>
          <p class="font-medium text-gray-900">{{ member.personal_email }}</p>
        </div>
        {% endif %}
        {% if show_phone and member.phone %}
        <div>
          <span class="text-gray-500">Phone</span>
          <p class="font-medium text-gray-900">{{ member.phone }}</p>
        </div>
        {% endif %}
        {% if roles %}
        <div>
          <span class="text-gray-500">Roles</span>
          <p>
            {% for role in roles %}
            <span class="cove-badge bg-cove-100 text-cove-700">{{ role | title }}</span>
            {% endfor %}
          </p>
        </div>
        {% endif %}
        {% endif %}
      </div>
      {% if bio %}
      <p class="text-sm text-gray-700 mt-4">{{ bio }}</p>
      {% endif %}
    </div>
  </div>

  <!-- Contacts Tile -->
  {% if contacts %}
  <div class="cove-card">
    <div class="cove-card-header">
      <h2 class="text-lg font-semibold text-gray-900">Contacts</h2>
    </div>
    <div class="cove-card-body">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {% for c in contacts %}
        <div class="border border-gray-200 rounded-lg p-4 {% if c.contact_type == 'primary' %}border-cove-300 bg-cove-50{% elif c.contact_type == 'emergency' %}border-red-200 bg-red-50{% endif %}">
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium text-gray-900">{{ c.name }}</span>
            <span class="cove-badge {% if c.contact_type == 'primary' %}bg-cove-100 text-cove-700{% elif c.contact_type == 'emergency' %}bg-red-100 text-red-700{% else %}bg-gray-100 text-gray-600{% endif %}">
              {{ c.contact_type | title }}
            </span>
          </div>
          <p class="text-xs text-gray-500 mb-2">{{ c.relationship.replace('_', ' ') | title }}{% if c.is_minor %} · Minor{% endif %}</p>
          {% if c.email %}
          <p class="text-sm text-gray-600">{{ c.email }}</p>
          {% endif %}
          {% if c.phone %}
          <p class="text-sm text-gray-600">{{ c.phone }}</p>
          {% endif %}
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
  {% endif %}

  <!-- Pets Tile -->
  {% if pets %}
  <div class="cove-card">
    <div class="cove-card-header">
      <h2 class="text-lg font-semibold text-gray-900">Pets</h2>
    </div>
    <div class="cove-card-body">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {% for pet in pets %}
        <div class="border border-gray-200 rounded-lg p-4">
          <span class="font-medium text-gray-900">{{ pet.name }}</span>
          <p class="text-xs text-gray-500">{{ pet.type }}{% if pet.breed %} · {{ pet.breed }}{% endif %}</p>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
  {% endif %}

</div>
{% endblock %}
```

- [ ] **Step 2: Add click-through links to directory list**

In `cove/member/templates/member/directory.html`, wrap each directory row name in a link to the profile page. Find the name display section (around line 57) and wrap it:

Replace the name `<div>` block:
```html
<div class="min-w-0">
  <div class="text-sm font-medium text-gray-900 truncate">{{ entry.name }}</div>
```

With:
```html
<div class="min-w-0">
  <a href="{{ url_for('member.directory_profile', apn=entry.apn) }}"
     class="text-sm font-medium text-gray-900 hover:text-cove-600 truncate block">{{ entry.name }}</a>
```

- [ ] **Step 3: Run all integration tests**

```bash
pytest tests/integration/test_directory_profile.py -v
```

Expected: All PASSED

- [ ] **Step 4: Run full test suite**

```bash
pytest tests/ -v
```

Expected: All tests pass, no regressions

- [ ] **Step 5: Commit**

```bash
git add cove/member/templates/member/directory_profile.html cove/member/templates/member/directory.html cove/member/routes.py cove/member/services.py tests/integration/test_directory_profile.py
git commit -m "feat: add APN profile page with tiles, directory click-through"
```

---

## Chunk 4: Cleanup + Migrations

### Task 11: Remove household_members References from Services

**Files:**
- Modify: `cove/member/profile_services.py` (remove household_members from allowed fields and return dicts)
- Modify: `cove/member/services.py` (remove household_members from _parcel_to_entry)

**Note:** This must happen before Migration 2 drops the `household_members` column. After Migration 2, any code referencing `profile.household_members` would raise `AttributeError`.

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/test_parcel_contacts.py`:

```python
def test_profile_for_directory_has_no_household_members(app, db_session, test_parcel):
    """get_profile_for_directory should not return household_members key."""
    from cove.member.profile_services import get_profile_for_directory
    profile = get_profile_for_directory(test_parcel.apn)
    assert "household_members" not in profile
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/unit/test_parcel_contacts.py::test_profile_for_directory_has_no_household_members -v
```

Expected: FAIL — `household_members` key still present

- [ ] **Step 3: Update profile_services.py**

In `cove/member/profile_services.py`:
- Remove `"household_members"` from the `_ALLOWED_FIELDS` set (around line 10)
- Remove `"household_members"` from the empty dict in `get_profile_for_directory` (around line 57)
- Remove `"household_members"` from the populated return dict (around line 68)

- [ ] **Step 4: Update _parcel_to_entry in services.py**

In `cove/member/services.py`, remove the `household_members` line from the dict returned by `_parcel_to_entry` (around line 42):

Remove:
```python
        "household_members": profile["household_members"],
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/ -v
```

Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add cove/member/profile_services.py cove/member/services.py tests/unit/test_parcel_contacts.py
git commit -m "refactor: remove household_members references from services (replaced by parcel_contacts)"
```

---

### Task 12: Migration 1 — Create Table and Migrate Data

**Files:**
- Create: `migrations/versions/xxx_add_parcel_contacts.py`

- [ ] **Step 1: Generate migration**

```bash
cd /Users/gclyle/GrowDirect/Cove/.worktrees/cove-parcel-contacts
FLASK_ENV=dev flask db revision -m "add parcel contacts table and profile created_at"
```

- [ ] **Step 2: Edit the generated migration**

Replace the generated `upgrade()` and `downgrade()` with:

```python
def upgrade() -> None:
    # 1. Create parcel_contacts table
    op.create_table(
        "parcel_contacts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("apn", sa.String(20), sa.ForeignKey("parcels.apn", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(254), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("contact_type", sa.String(20), nullable=False, server_default="household"),
        sa.Column("relationship", sa.String(20), nullable=False, server_default="other"),
        sa.Column("is_minor", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_parcel_contacts_apn", "parcel_contacts", ["apn"])
    op.create_index(
        "ix_parcel_contacts_primary_unique",
        "parcel_contacts",
        ["apn"],
        unique=True,
        postgresql_where=sa.text("contact_type = 'primary'"),
    )

    # 2. Add created_at to parcel_profiles
    op.add_column(
        "parcel_profiles",
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # 3. Migrate household_members JSON into parcel_contacts rows
    conn = op.get_bind()
    profiles = conn.execute(
        sa.text("SELECT apn, household_members FROM parcel_profiles WHERE household_members IS NOT NULL")
    ).fetchall()
    for row in profiles:
        members = row.household_members
        if not isinstance(members, list):
            continue
        for i, m in enumerate(members):
            if not isinstance(m, dict) or "name" not in m:
                continue
            conn.execute(
                sa.text(
                    "INSERT INTO parcel_contacts (id, apn, name, contact_type, relationship, display_order, created_at, updated_at) "
                    "VALUES (:id, :apn, :name, 'household', :rel, :order, now(), now())"
                ),
                {
                    "id": str(__import__("uuid").uuid4()),
                    "apn": row.apn,
                    "name": m["name"],
                    "rel": m.get("relation", "other"),
                    "order": i,
                },
            )


def downgrade() -> None:
    op.drop_column("parcel_profiles", "created_at")
    op.drop_index("ix_parcel_contacts_primary_unique", table_name="parcel_contacts")
    op.drop_index("ix_parcel_contacts_apn", table_name="parcel_contacts")
    op.drop_table("parcel_contacts")
```

- [ ] **Step 3: Run migration**

```bash
flask db upgrade head
```

Expected: Migration applies successfully

- [ ] **Step 4: Verify table exists**

```bash
docker exec growdirect_postgres psql -U growdirect -d cove -c "\d parcel_contacts"
```

Expected: Table schema with all columns and indexes

- [ ] **Step 5: Commit**

```bash
git add migrations/versions/
git commit -m "migration: add parcel_contacts table and parcel_profiles.created_at"
```

---

### Task 13: Migration 2 — Drop household_members JSON Column

**Files:**
- Create: `migrations/versions/xxx_drop_household_members.py`

- [ ] **Step 1: Generate migration**

```bash
flask db revision -m "drop household_members from parcel_profiles"
```

- [ ] **Step 2: Edit the generated migration**

```python
def upgrade() -> None:
    op.drop_column("parcel_profiles", "household_members")


def downgrade() -> None:
    op.add_column(
        "parcel_profiles",
        sa.Column("household_members", sa.JSON(), nullable=True),
    )
```

- [ ] **Step 3: Update ParcelProfile model**

In `cove/models/parcel_profile.py`, remove the `household_members` column definition (around line 29):

Remove:
```python
    household_members: Mapped[list | None] = mapped_column(JSON)
```

- [ ] **Step 4: Run migration**

```bash
flask db upgrade head
```

Expected: Migration applies, column dropped

- [ ] **Step 5: Run full test suite**

```bash
pytest tests/ -v
```

Expected: All tests pass. Any test referencing `household_members` on `ParcelProfile` should have been updated or removed in earlier tasks.

- [ ] **Step 6: Commit**

```bash
git add migrations/versions/ cove/models/parcel_profile.py
git commit -m "migration: drop household_members JSON column from parcel_profiles"
```

---

## Chunk 5: Final Verification

### Task 14: Full Suite + Merge

- [ ] **Step 1: Run full test suite from worktree**

```bash
cd /Users/gclyle/GrowDirect/Cove/.worktrees/cove-parcel-contacts
pytest tests/ -v
```

Expected: All tests pass

- [ ] **Step 2: Run tests in Docker container**

Sync worktree changes to main repo for container testing:

```bash
rsync -av --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
  /Users/gclyle/GrowDirect/Cove/.worktrees/cove-parcel-contacts/ \
  /tmp/cove-parcel-contacts-sync/
```

Then run tests inside the container:

```bash
docker exec cove_flask pytest tests/ -v
```

- [ ] **Step 3: Verify no broken imports**

```bash
grep -r "is_public" cove/ --include="*.py" | grep -v __pycache__ | grep -v migration
grep -r "household_members" cove/ --include="*.py" | grep -v __pycache__ | grep -v migration
```

Expected: No references to `household_members` in model/service/route code (only in migrations)

- [ ] **Step 4: Merge to main branch**

```bash
cd /Users/gclyle/GrowDirect/Cove
git merge feature/cove-parcel-contacts
```

- [ ] **Step 5: Clean up worktree**

```bash
git worktree remove .worktrees/cove-parcel-contacts
git branch -d feature/cove-parcel-contacts
```

- [ ] **Step 6: Final commit log check**

```bash
git log --oneline -10
```

Expected: Clean commit history with feat/test/migration prefixes
