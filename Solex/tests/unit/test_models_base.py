import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel


class ThingForTest(BaseModel):
    __tablename__ = "things_for_test"
    name: Mapped[str] = mapped_column(String(32))


def test_base_has_uuid_pk_and_timestamps():
    assert hasattr(ThingForTest, "id")
    assert hasattr(ThingForTest, "created_at")
    assert hasattr(ThingForTest, "updated_at")
    t = ThingForTest(name="x")
    assert t.id is None or isinstance(t.id, uuid.UUID)
