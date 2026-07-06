from fastapi import FastAPI

from app.core.config import settings
from app.routers import health

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}!"
    }


app.include_router(health.router)