def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["db"] is True
    assert data["valkey"] is True
    assert data["version"] == "0.1.0"
