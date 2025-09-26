# backend/app/models_orm.py
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class EntitlementORM(Base):
    __tablename__ = "entitlements"
    customer_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    blob_json: Mapped[str] = mapped_column(Text)

class LeaseORM(Base):
    __tablename__ = "leases"
    token: Mapped[str] = mapped_column(String(64), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(128), index=True)
    product: Mapped[str] = mapped_column(String(64), index=True)
    machine_fingerprint: Mapped[str] = mapped_column(String(256), index=True)
    issued_at: Mapped[str] = mapped_column(String(64))   # ISO 8601
    lease_until: Mapped[str] = mapped_column(String(64)) # ISO 8601

# NEW: very simple audit log (dev-friendly)
class AuditLogORM(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts_iso: Mapped[str] = mapped_column(String(64))      # ISO 8601 timestamp
    event: Mapped[str] = mapped_column(String(64))       # e.g., "activate", "apply_ticket", "revoke"
    actor: Mapped[str] = mapped_column(String(64))       # e.g., "api"
    details_json: Mapped[str] = mapped_column(Text)      # free-form JSON string
