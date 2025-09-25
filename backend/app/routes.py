from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends
from .models import (
    Feature, Entitlements,
    ActivationRequest, ActivationResponse,
    ValidationRequest, ValidationResponse, LeaseToken,
    OfflineRequest, Ticket, TicketApplyRequest
)
from .storage import load_json, save_json
from .security import require_api_key
from .crypto import sign_offline_request, verify_ticket

import logging, os
logging.info("Loaded routes.py from: %s", __file__)


router = APIRouter()

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()

LEASE_HOURS = 72
GRACE_HOURS = 24

@router.get("/health")
def health():
    return {"ok": True}

@router.get("/features/{product}", response_model=list[Feature])
def get_features(product: str):
    data = load_json("features")
    if product not in data:
        raise HTTPException(status_code=404, detail="Unknown product")
    return data[product]

@router.get("/entitlements/{customer_id}", response_model=Entitlements)
def get_entitlements(customer_id: str):
    data = load_json("entitlements")
    info = data.get(customer_id)
    if not info:
        raise HTTPException(status_code=404, detail="Unknown customer_id")
    return info

# ---------- Online activate/validate (protected) ----------
@router.post("/licenses/activate", response_model=ActivationResponse, dependencies=[Depends(require_api_key)])
def activate(req: ActivationRequest):
    entitlements = load_json("entitlements")
    customer = entitlements.get(req.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Unknown customer_id")
    if req.product not in customer.get("products", {}):
        raise HTTPException(status_code=403, detail="Product not entitled for this customer")

    token = str(uuid4())
    issued = now_utc()
    lease_until = issued + timedelta(hours=LEASE_HOURS)

    leases = load_json("leases")
    leases[token] = LeaseToken(
        token=token,
        customer_id=req.customer_id,
        product=req.product,
        machine_fingerprint=req.machine_fingerprint,
        issued_at=iso(issued),
        lease_until=iso(lease_until),
    ).model_dump()
    save_json("leases", leases)

    return ActivationResponse(
        status="issued",
        message=f"Lease token valid for {LEASE_HOURS} hours",
        token=token,
        lease_until=iso(lease_until),
    )

@router.post("/licenses/validate", response_model=ValidationResponse, dependencies=[Depends(require_api_key)])
def validate(req: ValidationRequest):
    leases = load_json("leases")
    info = leases.get(req.token)
    if not info:
        raise HTTPException(status_code=404, detail="Unknown or expired token")

    if info["customer_id"] != req.customer_id or info["product"] != req.product:
        raise HTTPException(status_code=403, detail="Token does not match customer/product")
    if info["machine_fingerprint"] != req.machine_fingerprint:
        raise HTTPException(status_code=403, detail="Token bound to different machine")

    lease_until = datetime.fromisoformat(info["lease_until"])
    now = now_utc()

    if now <= lease_until:
        return ValidationResponse(
            status="ok",
            message="Valid lease",
            valid=True,
            lease_until=iso(lease_until),
            grace_remaining_hours=GRACE_HOURS,
        )

    grace_deadline = lease_until + timedelta(hours=GRACE_HOURS)
    if now <= grace_deadline:
        remaining = int((grace_deadline - now).total_seconds() // 3600)
        return ValidationResponse(
            status="grace",
            message="Lease expired; within grace period",
            valid=True,
            lease_until=iso(lease_until),
            grace_remaining_hours=remaining,
        )

    return ValidationResponse(
        status="expired",
        message="Lease and grace exceeded",
        valid=False,
        lease_until=iso(lease_until),
        grace_remaining_hours=0,
    )

# ---------- Offline helper: generate a request (optional) ----------
@router.post("/offline/request", response_model=OfflineRequest)
def offline_request(req: ActivationRequest):
    """
    Helper to generate a well-formed offline request object.
    In real life this is generated on the client machine.
    """
    return OfflineRequest(
        customer_id=req.customer_id,
        product=req.product,
        machine_fingerprint=req.machine_fingerprint,
        nonce=str(uuid4()),
        requested_at=iso(now_utc()),
    )

# ---------- Server: issue a signed ticket (protected) ----------
@router.post("/tickets/issue", response_model=Ticket, dependencies=[Depends(require_api_key)])
def issue_ticket(off_req: OfflineRequest, lease_hours: int = LEASE_HOURS):
    entitlements = load_json("entitlements")
    customer = entitlements.get(off_req.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Unknown customer_id")
    if off_req.product not in customer.get("products", {}):
        raise HTTPException(status_code=403, detail="Product not entitled for this customer")

    sig = sign_offline_request(off_req, lease_hours)
    return Ticket(request=off_req, lease_hours=lease_hours, signature=sig)

# ---------- Client: apply a ticket (no API key) ----------
@router.post("/tickets/apply", response_model=ActivationResponse)
def apply_ticket(payload: TicketApplyRequest):
    ticket = payload.ticket
    if not verify_ticket(ticket):
        raise HTTPException(status_code=400, detail="Invalid ticket signature")

    token = str(uuid4())
    issued = now_utc()
    lease_until = issued + timedelta(hours=ticket.lease_hours)

    leases = load_json("leases")
    leases[token] = LeaseToken(
        token=token,
        customer_id=ticket.request.customer_id,
        product=ticket.request.product,
        machine_fingerprint=ticket.request.machine_fingerprint,
        issued_at=iso(issued),
        lease_until=iso(lease_until),
    ).model_dump()
    save_json("leases", leases)

    return ActivationResponse(
        status="issued",
        message=f"Offline lease token valid for {ticket.lease_hours} hours",
        token=token,
        lease_until=iso(lease_until),
    )
