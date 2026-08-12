import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.base import Base
from app.database.database import engine

from app.models.document import Document

from app.routers import health
from app.routers import documents
from app.routers.chat import router as chat_router


print(
    "=== STARTING APPLICATION ===",
    flush=True,
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


print(
    "=== CREATING DATABASE TABLES ===",
    flush=True,
)

Base.metadata.create_all(
    bind=engine
)

print(
    "=== DATABASE READY ===",
    flush=True,
)


app.include_router(
    health.router
)

app.include_router(
    documents.router
)

app.include_router(
    chat_router
)


print(
    "=== APPLICATION READY ===",
    flush=True,
)


if __name__ == "__main__":

    import uvicorn

    port = int(
        os.environ.get(
            "PORT",
            "10000",
        )
    )

    print(
        f"=== STARTING UVICORN ON 0.0.0.0:{port} ===",
        flush=True,
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )