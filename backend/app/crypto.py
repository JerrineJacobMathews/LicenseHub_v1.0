import hmac, hashlib, os
from .models import OfflineRequest, Ticket

TICKET_SECRET = os.getenv("TICKET_SECRET", "dev-secret")

def sign_offline_request(req: OfflineRequest, lease_hours: int) -> str:
    msg = "|".join([
        req.customer_id,
        req.product,
        req.machine_fingerprint,
        req.nonce,
        req.requested_at,
        str(lease_hours),
    ]).encode("utf-8")
    return hmac.new(TICKET_SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest()

def verify_ticket(ticket: Ticket) -> bool:
    expected = sign_offline_request(ticket.request, ticket.lease_hours)
    # constant-time compare
    return hmac.compare_digest(expected, ticket.signature)
