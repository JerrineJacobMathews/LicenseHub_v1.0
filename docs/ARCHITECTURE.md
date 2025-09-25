# LicenseHub v1.0 — Architecture

## Runtime
- FastAPI app → stateless services.
- Data for v1 demo: JSON files; later → Postgres/Redis.

## Modules
- `app.main` – app creation, routers
- `app.routes` – API endpoints
- `app.models` – Pydantic models
- `app.storage` – simple JSON-backed storage for demo

## Operations
- Containerized with Dockerfile (`python:3.11-slim`).
- Dev compose exposes port 8000.
