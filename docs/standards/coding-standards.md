# Coding Standards

These patterns apply to every GrowDirect app. Consistency over cleverness.

## Import Order

stdlib → third-party → local. One blank line between groups.

```python
import uuid
from datetime import datetime

from flask import flash, redirect, url_for
from sqlalchemy.orm import Mapped, mapped_column

from myapp.models import Farm
from myapp.services import farm_service
```

## Model Pattern

UUID primary key, `created_at`/`updated_at` on every table. Use `Mapped[]` — never `Column()`.

```python
class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orgs.id"), nullable=False)  # tenant mixin
```

Audit mixin (`AuditMixin`) tracks `created_by` and `updated_by` on tables that need change history. Add it when a table's writes have business accountability requirements.

## Service Pattern

Stateless functions. The caller (route) opens and owns the db session. Services return domain objects or raise exceptions — they never flash or redirect.

```python
# myapp/services/farm_service.py

def get_farm(db: Session, farm_id: uuid.UUID) -> Farm:
    farm = db.get(Farm, farm_id)
    if farm is None:
        raise ValueError(f"Farm {farm_id} not found")
    return farm

def create_farm(db: Session, name: str, org_id: uuid.UUID) -> Farm:
    farm = Farm(name=name, org_id=org_id)
    db.add(farm)
    db.flush()
    return farm
```

Never import `db` directly in a service. Accept it as a parameter.

## Route Pattern

Thin handlers. Validate form, call service, flash result, redirect. No business logic in routes.

```python
@bp.route("/farms/create", methods=["GET", "POST"])
@login_required
def create():
    form = FarmForm()
    if form.validate_on_submit():
        try:
            farm = farm_service.create_farm(db.session, name=form.name.data, org_id=current_user.org_id)
            db.session.commit()
            flash("Farm created.", "success")
            return redirect(url_for("farms.detail", farm_id=farm.id))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("farms/create.html", form=form)
```

## Error Handling

Services raise — routes catch and flash. Never let a ValueError bubble to a 500.

- Service raises `ValueError` for domain errors (not found, invalid state)
- Service raises `PermissionError` for authorization failures
- Route catches, flashes the message, re-renders or redirects
- Unexpected exceptions propagate to the Flask error handler (log and 500)

```python
try:
    result = some_service.do_thing(db.session, ...)
    db.session.commit()
    flash("Done.", "success")
    return redirect(...)
except ValueError as e:
    flash(str(e), "error")
    return render_template("...", form=form)
```

## Test Pattern

Three layers: unit, integration, smoke. All fixtures in `conftest.py`.

```python
# conftest.py — shared fixtures
@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client, db_session):
    # log in a test user, return authenticated client
    ...
```

Unit test — call service directly with a real db session:

```python
def test_create_farm(db_session):
    farm = farm_service.create_farm(db_session, name="Test Farm", org_id=ORG_UUID)
    assert farm.id is not None
    assert farm.name == "Test Farm"
```

Integration test — hit the route via test client:

```python
def test_create_farm_route(auth_client):
    resp = auth_client.post("/farms/create", data={"name": "Test Farm"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Farm created" in resp.data
```

Smoke test — verify the app is alive:

```python
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
```
