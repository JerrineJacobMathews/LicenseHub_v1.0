# LicenseHub v1.0 (Scaffold)

Production-ready scaffold to start the **LicenseHub** backend, docs, and ops in minutes.

## What you get
- **FastAPI backend** with health & starter endpoints
- **Data stubs** (`features.json`, `entitlements.json`)
- **Docs**: BRD, SRS, Architecture, Versions (templates)
- **Tests**: pytest smoke test
- **Docker**: lightweight `Dockerfile` + `docker-compose.yml` for dev
- **Tools**: placeholder Migration Wizard GUI (Tkinter)

## Quickstart (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Quickstart (Ubuntu/macOS)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

OpenAPI docs: http://localhost:8000/docs

### Smoke test
```bash
curl http://localhost:8000/health
curl http://localhost:8000/features/SERVEO
curl http://localhost:8000/entitlements/demo-customer
```
