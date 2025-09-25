# backend/app/db.py
import os
import json
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Default: SQLite file in backend/data (works locally & in CI)
DEFAULT_SQLITE = "sqlite:///./data/licensehub.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

# SQLite needs this flag for threaded test client; Postgres does not.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

class Base(DeclarativeBase):
    pass

@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def _ensure_db_schema_and_seed():
    """
    Dev/CI convenience: create tables if missing and seed entitlements from JSON
    the first time the app imports this module. In prod, you can still run
    Alembic migrations (no conflict: create_all() is no-op if tables exist).
    """
    # Import here to avoid circular imports at module import time.
    from . import models_orm  # registers ORM models with Base metadata
    from .models_orm import EntitlementORM
    from .crud import upsert_entitlements_blob

    # 1) Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # 2) Seed entitlements from JSON if table appears empty
    from sqlalchemy.orm import Session
    with Session(bind=engine, future=True) as db:
        has_any = db.execute(select(EntitlementORM.customer_id).limit(1)).first()
        if has_any:
            return  # already seeded or populated

        data_path = Path(__file__).resolve().parent.parent / "data" / "entitlements.json"
        if data_path.exists():
            try:
                content = json.loads(data_path.read_text(encoding="utf-8"))
                with session_scope() as s:
                    for customer_id, blob in content.items():
                        upsert_entitlements_blob(s, customer_id, blob)
            except Exception:
                # Silent fail in case of invalid JSON; tests will still run, but
                # your endpoints will return 404 for unknown customer_id.
                pass

# Run once on import (safe in tests/dev; no-op if already created/seeded)
_ensure_db_schema_and_seed()
