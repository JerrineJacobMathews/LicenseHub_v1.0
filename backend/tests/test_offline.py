from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_offline_issue_and_apply():
    paths = client.get("/openapi.json").json()["paths"].keys()
    assert "/offline/request" in paths, f"/offline/request missing. Paths present: {list(paths)}"

    # 1) create an offline request (client-side helper)
    r = client.post("/offline/request", json={
        "customer_id": "demo-customer",
        "product": "SERVEO",
        "machine_fingerprint": "WIN10-ABC-TEST",
        "license_key": None
    })
    assert r.status_code == 200, r.text
    off_req = r.json()

    # 2) server issues ticket (protected)
    r = client.post("/tickets/issue?lease_hours=2", json=off_req, headers={"X-API-Key": "dev-key"})
    assert r.status_code == 200, r.text
    ticket = r.json()
    assert "signature" in ticket

    # 3) client applies ticket (no API key)
    r = client.post("/tickets/apply", json={"ticket": ticket})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "issued"
    assert "token" in data
