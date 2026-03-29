# Cove Parcel Contacts & Profile Tiles

**Date:** 2026-03-29
**Status:** Draft
**Author:** SYD (dev agent) + Jeffe (product)

---

## Problem

Cove's member directory stores minimal contact info — one name, one email, one phone per parcel. There's no structured way to record who actually lives at each address, designate primary and secondary contacts for HOA business, track household members (including children), or provide emergency contact information.

The board needs to go door-to-door and collect this data. The directory needs a parcel-centric profile page that displays contacts, household members, and pets as visual tiles.

## Requirements

1. Structured contact records per parcel — proper rows, not JSON blobs
2. Contact types: primary, secondary, household, emergency, tenant
3. Relationship tracking: owner, co-owner, spouse, child, parent, tenant, other
4. Minor flag for children (neighborhood watch, not directly contactable)
5. Board/admin manages all contact data
6. Directory detail view becomes a tile-based APN profile page
7. Existing privacy/share toggles control visibility
8. Migrate `ParcelProfile.household_members` JSON into the new table
9. Keep `ParcelProfile.pets` as JSON (no contact info needed)
10. One primary contact per APN (enforced by unique partial index)
11. Directory list sorts by street name, then street number (numeric sort)
12. Directory list avatar bubbles show street number, not first initial

## Non-Goals

- Non-parcel member accounts (future ARC expansion)
- 501(c)(5) membership model (future, same app, different org config)
- Self-service contact editing by members
- External sharing API for city/neighborhood watch programs
- Changes to voting, authentication, or lot email identity

## Design Decisions

### Member ≠ Person

Under Davis-Stirling (Civil Code §4160), HOA membership is automatic and inseparable from property ownership. `Member` represents the parcel's governance identity — its login, vote, assessment status, and lot email. `ParcelContact` represents the actual humans at that address.

This separation holds across all HOA scenarios: single owners, married couples, absentee owners with property managers, trusts, rentals, and ownership transfers. The APN stays; the people change.

### ParcelContact is HOA-Scoped

`ParcelContact` is tied to an APN and only makes sense for organizations with `membership_model = "unit"`. Future person-based organizations (501(c)(5) under ARC expansion) would use `Member` directly for contact info since there are no parcels. This design does not block that future.

### Board Manages Contacts

All contact CRUD is board/admin only. The intended workflow is the board president going door-to-door to meet households and enter their information. Members see their own and neighbors' data (subject to privacy toggles) but cannot edit.

---

## Data Model

### New Table: `parcel_contacts`

```
parcel_contacts
├── id              UUID, primary key, default uuid4
├── apn             String(20), FK → parcels.apn, NOT NULL
├── name            String(200), NOT NULL
├── email           String(254), nullable
├── phone           String(20), nullable
├── contact_type    String(20), NOT NULL
│                   enum: primary, secondary, household, emergency, tenant
├── relationship    String(20), NOT NULL
│                   enum: owner, co_owner, spouse, child, parent, tenant, other
├── is_minor        Boolean, default False
├── notes           Text, nullable
├── display_order   Integer, default 0
├── created_at      DateTime, NOT NULL
└── updated_at      DateTime, NOT NULL
```

**Constraints:**
- Unique partial index: one `primary` contact_type per APN
- Foreign key: `apn` → `parcels.apn` with cascade delete
- Index on `apn` for efficient lookups

### SQLAlchemy Model

```python
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
    __tablename__ = "parcel_contacts"
    __table_args__ = (
        db.Index(
            "ix_parcel_contacts_primary_unique",
            "apn",
            unique=True,
            postgresql_where=text("contact_type = 'primary'"),
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    apn: Mapped[str] = mapped_column(String(20), ForeignKey("parcels.apn", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(254))
    phone: Mapped[str | None] = mapped_column(String(20))
    contact_type: Mapped[str] = mapped_column(String(20), default=ContactType.HOUSEHOLD.value)
    relationship: Mapped[str] = mapped_column(String(20), default=ContactRelationship.OTHER.value)
    is_minor: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="contacts")
```

### Model Changes

**Parcel** — add relationship:
```python
contacts: Mapped[list["ParcelContact"]] = relationship(
    "ParcelContact", back_populates="parcel", order_by="ParcelContact.display_order"
)
```

**ParcelProfile** — drop `household_members` JSON column. Keep `pets` JSON, `share_household` toggle (repurposed to control contact tile visibility), and all other fields.

### Migration

Single Alembic migration:
1. Create `parcel_contacts` table with all columns and indexes
2. Migrate `parcel_profiles.household_members` JSON data into `parcel_contacts` rows
3. Drop `household_members` column from `parcel_profiles`

---

## Routes

### Board Contact Management

Blueprint: `board_bp` (existing), new routes under `/board/parcels/<apn>/contacts`

| Method | Path | Action |
|--------|------|--------|
| GET | `/board/parcels/<apn>/contacts` | List contacts for parcel, show add form |
| POST | `/board/parcels/<apn>/contacts/add` | Create new contact |
| GET | `/board/parcels/<apn>/contacts/<contact_id>/edit` | Edit form |
| POST | `/board/parcels/<apn>/contacts/<contact_id>/edit` | Update contact |
| POST | `/board/parcels/<apn>/contacts/<contact_id>/delete` | Delete contact |

All routes gated by `@login_required` + board/admin role check.

### Parcel Profile Page

New route on `member_bp`: `GET /member/directory/<apn>`

Replaces the current directory detail behavior. When a user clicks a row in the directory list, they navigate to this APN-centric profile page.

**Access:** Any logged-in member can view. Privacy toggles control what's shown.

---

## Templates

### Directory List Changes (`member/templates/member/directory.html`)

**Sort order:** Primary sort by street name (alphabetical), secondary sort by street number (numeric, not lexicographic — so 5, 10, 25 not 10, 25, 5). Applied in the service layer query, not client-side.

**Avatar bubbles:** Currently show first initial of member name. Change to show the **street number** from the parcel address (e.g., "25", "101"). This identifies the property, which is the real identity in an HOA directory.

### Parcel Profile Page (`member/templates/member/directory_profile.html`)

Top-to-bottom tile layout:

**Header tile** (always visible):
- APN, full address, lot email
- Membership status badge (active/suspended/inactive)
- Assessment status badge (current/delinquent)
- Voting weight
- Member roles (if any: board, ARC, etc.)

**Contacts tile** (visible if `share_household` is true, or viewer is board):
- Primary and secondary contacts displayed as cards
- Each card: name, relationship badge, email (if set), phone (if set)
- Primary contact highlighted with distinct styling

**Household tile** (visible if `share_household` is true, or viewer is board):
- Non-primary contacts: household members, tenants
- Minor indicator (name only, no contact details displayed)
- Emergency contacts shown with distinct styling

**Pets tile** (visible if `share_pets` is true, or viewer is board):
- From `ParcelProfile.pets` JSON
- Each pet: name, type, breed

### Board Contact Management (`board/templates/board/parcel_contacts.html`)

- Table view of all contacts for the APN
- Add/edit forms inline or in modal
- Delete with confirmation
- Drag-to-reorder or manual display_order field

---

## Forms

### `ParcelContactForm` (new, in `cove/board/forms.py`)

```python
class ParcelContactForm(CoveForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=200)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=254)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    contact_type = SelectField("Contact Type", choices=[
        ("primary", "Primary"),
        ("secondary", "Secondary"),
        ("household", "Household Member"),
        ("emergency", "Emergency Contact"),
        ("tenant", "Tenant"),
    ])
    relationship = SelectField("Relationship", choices=[
        ("owner", "Owner"),
        ("co_owner", "Co-Owner"),
        ("spouse", "Spouse"),
        ("child", "Child"),
        ("parent", "Parent"),
        ("tenant", "Tenant"),
        ("other", "Other"),
    ])
    is_minor = BooleanField("Minor (under 18)")
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
```

---

## Privacy Model

Existing toggles are reused:

| Toggle | Controls | Default |
|--------|----------|---------|
| `ParcelProfile.share_household` | Contacts and household tiles | False (opt-in) |
| `ParcelProfile.share_pets` | Pets tile | True |
| `DirectoryPreference.show_name` | Member name in directory list | False |
| `DirectoryPreference.show_email` | Member email in directory list | False |
| `DirectoryPreference.show_phone` | Member phone in directory list | False |

Board members see all tiles regardless of toggle state.

---

## File Changes Summary

| File | Change |
|------|--------|
| `cove/models/parcel_contact.py` | New — `ParcelContact` model, `ContactType` enum, `ContactRelationship` enum |
| `cove/models/parcel.py` | Add `contacts` relationship |
| `cove/models/parcel_profile.py` | Drop `household_members` column |
| `cove/models/__init__.py` | Import `ParcelContact` |
| `cove/board/routes.py` | Add contact CRUD routes |
| `cove/board/forms.py` | Add `ParcelContactForm` |
| `cove/board/templates/board/parcel_contacts.html` | New — contact management page |
| `cove/member/routes.py` | Add `/member/directory/<apn>` profile route |
| `cove/member/services.py` | Update directory detail to include contacts |
| `cove/member/templates/member/directory_profile.html` | New — tile-based APN profile page |
| `cove/member/templates/member/directory.html` | Update sort order, avatar bubbles show street number |
| `migrations/versions/xxx_add_parcel_contacts.py` | New — create table, migrate data, drop column |

---

## Test Plan

### Unit Tests
- `ParcelContact` model: create, defaults, enum values
- Unique primary constraint: second primary for same APN raises IntegrityError
- Contact CRUD service functions
- Privacy toggle enforcement: contacts hidden when `share_household` is false

### Integration Tests
- Board can add/edit/delete contacts via routes
- Non-board member gets 403 on contact management routes
- Directory profile page renders correct tiles
- Board sees all tiles; regular member respects privacy toggles
- Migration: JSON household data correctly converted to rows

---

## Future Considerations (Not In Scope)

- **Non-parcel member accounts** — ARC expansion for 501(c)(5) supporters. `Member.apn` is already nullable.
- **Self-service editing** — Members manage their own household contacts. Would need auth changes.
- **External sharing** — Exportable contact rosters for city programs, neighborhood watch. Separate opt-in layer.
- **Contact-to-Member linking** — Primary contact shares UUID with Member record. Deferred pending further design.
