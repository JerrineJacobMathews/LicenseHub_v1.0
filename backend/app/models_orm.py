# backend/app/models_orm.py
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class EntitlementORM(Base):
    __tablename__ = "entitlements"
    # store per-customer entitlement blob as JSON string (portable across SQLite/Postgres)
    customer_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    blob_json: Mapped[str] = mapped_column(Text)  # {"products": {...}, "expires": null}

class LeaseORM(Base):
    __tablename__ = "leases"
    token: Mapped[str] = mapped_column(String(64), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(128), index=True)
    product: Mapped[str] = mapped_column(String(64), index=True)
    machine_fingerprint: Mapped[str] = mapped_column(String(256), index=True)
    issued_at: Mapped[str] = mapped_column(String(64))   # ISO 8601
    lease_until: Mapped[str] = mapped_column(String(64)) # ISO 8601
