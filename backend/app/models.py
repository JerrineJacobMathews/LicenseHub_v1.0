from pydantic import BaseModel
from typing import List, Optional, Dict

class Feature(BaseModel):
    code: str
    name: str
    tier: Optional[str] = None

class Entitlements(BaseModel):
    products: Dict[str, List[str]]
    expires: Optional[str] = None

class ActivationRequest(BaseModel):
    customer_id: str
    product: str
    machine_fingerprint: str
    license_key: Optional[str] = None  # placeholder

class ActivationResponse(BaseModel):
    status: str
    message: str
    token: str
    lease_until: str  # ISO 8601

class ValidationRequest(BaseModel):
    customer_id: str
    product: str
    machine_fingerprint: str
    token: str

class ValidationResponse(BaseModel):
    status: str
    message: str
    valid: bool
    lease_until: Optional[str] = None
    grace_remaining_hours: Optional[int] = None

class LeaseToken(BaseModel):
    token: str
    customer_id: str
    product: str
    machine_fingerprint: str
    issued_at: str
    lease_until: str
