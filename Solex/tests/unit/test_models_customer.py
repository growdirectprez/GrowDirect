from solex.models.customer import Customer, Address


def test_customer_fields():
    c = Customer(email="test@example.com", first_name="Jane", last_name="Doe")
    assert c.email == "test@example.com"
    assert c.first_name == "Jane"


def test_address_fields():
    a = Address(
        first_name="Jane",
        last_name="Doe",
        line1="123 Main St",
        city="Rancho Palos Verdes",
        region="CA",
        postal_code="90275",
        country="US",
    )
    assert a.line1 == "123 Main St"
    assert a.country == "US"
