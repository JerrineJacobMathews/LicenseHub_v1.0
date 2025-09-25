# backend/app/crud.py
import json
from typing import Optional
from sqlalchemy.orm import Session
from .models_orm import EntitlementORM, LeaseORM

# -------- Entitlements --------
def get_entitlements_blob(db: Session, customer_id: str) -> Optional[dict]:
    row = db.get(EntitlementORM, customer_id)
    if not row:
        return None
    try:
        return json.loads(row.blob_json)
    except json.JSONDecodeError:
        return None

def upsert_entitlements_blob(db: Session, customer_id: str, data: dict) -> None:
    blob = json.dumps(data, ensure_ascii=False)
    row = db.get(EntitlementORM, customer_id)
    if row:
        row.blob_json = blob
    else:
        row = EntitlementORM(customer_id=customer_id, blob_json=blob)
        db.add(row)

# -------- Leases --------
def save_lease(db: Session, lease: dict) -> None:
    row = LeaseORM(**lease)
    db.add(row)

def get_lease(db: Session, token: str) -> Optional[dict]:
    row = db.get(LeaseORM, token)
    if not row:
        return None
    return {
        "token": row.token,
        "customer_id": row.customer_id,
        "product": row.product,
        "machine_fingerprint": row.machine_fingerprint,
        "issued_at": row.issued_at,
        "lease_until": row.lease_until,
    }
