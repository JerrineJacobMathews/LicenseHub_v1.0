from fastapi import APIRouter, HTTPException
from .models import Feature, Entitlements, ActivationRequest, ActivationResponse, ValidationRequest, ValidationResponse
from .storage import load_json

router = APIRouter()

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

@router.post("/licenses/activate", response_model=ActivationResponse)
def activate(req: ActivationRequest):
    # Stub logic: accept any known customer for demo
    data = load_json("entitlements")
    if req.customer_id not in data:
        raise HTTPException(status_code=404, detail="Unknown customer_id")
    # Pretend we issue a short lease
    return ActivationResponse(status="issued", message="Demo lease granted", lease_until=None)

@router.post("/licenses/validate", response_model=ValidationResponse)
def validate(req: ValidationRequest):
    # Stub logic: always valid for demo
    return ValidationResponse(status="ok", message="Valid (demo)", valid=True, grace_remaining_hours=72)
