import os
from fastapi import Header, HTTPException, status

API_KEY_ENV = os.getenv("API_KEY", "dev-key")

async def require_api_key(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY_ENV:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
