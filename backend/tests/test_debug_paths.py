from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test__debug_list_paths():
    paths = client.get("/openapi.json").json()["paths"].keys()
    print("OPENAPI PATHS:", list(paths))
    assert "/offline/request" in paths, "offline/request route missing in OpenAPI"
