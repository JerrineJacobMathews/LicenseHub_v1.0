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
    license_key: Optional[str] = None

class ActivationResponse(BaseModel):
    status: str
    message: str
    lease_until: Optional[str] = None

class ValidationRequest(BaseModel):
    customer_id: str
    product: str
    machine_fingerprint: str
    token: Optional[str] = None

class ValidationResponse(BaseModel):
    status: str
    message: str
    valid: bool
    grace_remaining_hours: Optional[int] = None
