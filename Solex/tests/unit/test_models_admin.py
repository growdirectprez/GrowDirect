from solex.models.admin import AdminUser


def test_admin_user_fields():
    a = AdminUser(email="admin@example.com")
    assert a.email == "admin@example.com"
    assert a.password_hash is None
    assert a.last_login_at is None
