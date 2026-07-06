from fastapi import FastAPI

from app.core.config import settings
from app.routers import health
from app.routers import documents
from app.database.database import engine
from app.database.base import Base

from app.models.document import Document

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}!"
    }

Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(documents.router)