# backend/app/main.py
import logging
from fastapi import FastAPI, Request
from time import perf_counter
from dotenv import load_dotenv
import os
from .routes import router

load_dotenv()  # loads .env if present

def create_app() -> FastAPI:
    app = FastAPI(title="LicenseHub v1.0", version="1.0.0")

    # --- simple access log middleware (method, path, status, ms) ---
    @app.middleware("http")
    async def access_log(request: Request, call_next):
        t0 = perf_counter()
        response = await call_next(request)
        dt_ms = int((perf_counter() - t0) * 1000)
        logging.info(
            "access method=%s path=%s status=%s ms=%s",
            request.method, request.url.path, response.status_code, dt_ms
        )
        return response

    app.include_router(router)
    return app

app = create_app()

# Optional: set log level via env (LOG_LEVEL=INFO/DEBUG/WARNING)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
