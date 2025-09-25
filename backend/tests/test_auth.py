from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_activate_requires_api_key():
    # missing key → 401
    r = client.post("/licenses/activate", json={
        "customer_id": "demo-customer",
        "product": "SERVEO",
        "machine_fingerprint": "X",
        "license_key": None
    })
    assert r.status_code == 401

def test_activate_with_api_key():
    r = client.post("/licenses/activate",
        headers={"X-API-Key": "dev-key"},
        json={
            "customer_id": "demo-customer",
            "product": "SERVEO",
            "machine_fingerprint": "X",
            "license_key": None
        }
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "issued"
    assert "token" in data
