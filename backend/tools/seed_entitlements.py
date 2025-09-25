import json, pathlib
from app.db import session_scope
from app.crud import upsert_entitlements_blob

DATA = pathlib.Path(__file__).resolve().parents[1] / "data" / "entitlements.json"

def main():
    content = json.loads(DATA.read_text(encoding="utf-8"))
    with session_scope() as db:
        for customer_id, blob in content.items():
            upsert_entitlements_blob(db, customer_id, blob)
    print("Seeded entitlements:", ", ".join(content.keys()))

if __name__ == "__main__":
    main()
