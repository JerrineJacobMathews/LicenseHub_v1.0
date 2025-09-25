# backend/app/crypto.py
import os, base64
from .models import OfflineRequest, Ticket

from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

# Keys are 32-byte values in Base64 (not PEM). In prod, set both env vars.
# If missing, we generate an ephemeral dev keypair (OK for tests/dev only).
_ED25519_PRIV_B64 = os.getenv("ED25519_PRIVATE_KEY")
_ED25519_PUB_B64  = os.getenv("ED25519_PUBLIC_KEY")

_signing_key: SigningKey | None = None
_verify_key:  VerifyKey  | None = None

def _load_or_generate_keys():
    global _signing_key, _verify_key
    if _signing_key and _verify_key:
        return
    if _ED25519_PRIV_B64 and _ED25519_PUB_B64:
        sk_bytes = base64.b64decode(_ED25519_PRIV_B64)
        pk_bytes = base64.b64decode(_ED25519_PUB_B64)
        _signing_key = SigningKey(sk_bytes)
        _verify_key  = VerifyKey(pk_bytes)
    else:
        # Dev fallback: generate ephemeral keys (NOT for production)
        _signing_key = SigningKey.generate()
        _verify_key  = _signing_key.verify_key

def _canonical_message(req: OfflineRequest, lease_hours: int) -> bytes:
    # Stable, deterministic concatenation. Changing this breaks signature compatibility.
    parts = [
        req.customer_id,
        req.product,
        req.machine_fingerprint,
        req.nonce,
        req.requested_at,
        str(lease_hours),
    ]
    return ("|".join(parts)).encode("utf-8")

def sign_offline_request(req: OfflineRequest, lease_hours: int) -> str:
    _load_or_generate_keys()
    msg = _canonical_message(req, lease_hours)
    sig = _signing_key.sign(msg).signature  # 64 bytes
    return base64.b64encode(sig).decode("ascii")  # return as Base64 string

def verify_ticket(ticket: Ticket) -> bool:
    _load_or_generate_keys()
    msg = _canonical_message(ticket.request, ticket.lease_hours)
    try:
        _verify_key.verify(msg, base64.b64decode(ticket.signature))
        return True
    except (BadSignatureError, ValueError, TypeError):
        return False
