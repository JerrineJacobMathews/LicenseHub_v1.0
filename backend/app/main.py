from fastapi import FastAPI
from .routes import router

def create_app() -> FastAPI:
    app = FastAPI(title="LicenseHub v1.0", version="1.0.0")
    app.include_router(router)
    return app

app = create_app()
