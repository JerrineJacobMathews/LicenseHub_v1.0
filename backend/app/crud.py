# backend/app/crud.py
import json
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from .models_orm import EntitlementORM, LeaseORM, AuditLogORM

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
        db.add(EntitlementORM(customer_id=customer_id, blob_json=blob))

# -------- Leases --------
def save_lease(db: Session, lease: dict) -> None:
    db.add(LeaseORM(**lease))

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

def list_leases_for_customer(db: Session, customer_id: str) -> List[Dict]:
    q = db.execute(
        select(
            LeaseORM.token, LeaseORM.product, LeaseORM.machine_fingerprint,
            LeaseORM.issued_at, LeaseORM.lease_until
        ).where(LeaseORM.customer_id == customer_id)
    )
    rows = q.all()
    return [
        {
            "token": r.token,
            "product": r.product,
            "machine_fingerprint": r.machine_fingerprint,
            "issued_at": r.issued_at,
            "lease_until": r.lease_until,
        }
        for r in rows
    ]

def delete_lease(db: Session, token: str) -> int:
    result = db.execute(delete(LeaseORM).where(LeaseORM.token == token))
    # result.rowcount is deprecated in some DBs; SQLAlchemy returns rowcount in execution result
    return result.rowcount or 0

# -------- Audit --------
def log_event(db: Session, event: str, actor: str, details: dict) -> None:
    db.add(AuditLogORM(
        ts_iso=details.get("ts_iso"),
        event=event,
        actor=actor,
        details_json=json.dumps(details, ensure_ascii=False),
    ))
