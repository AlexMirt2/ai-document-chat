import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

print("=== STARTING APPLICATION ===", flush=True)

from app.database.base import Base
print("=== BASE IMPORTED ===", flush=True)

from app.database.database import engine
print("=== DATABASE IMPORTED ===", flush=True)

from app.models.document import Document
print("=== MODEL IMPORTED ===", flush=True)

from app.routers import health
print("=== HEALTH ROUTER IMPORTED ===", flush=True)

from app.routers import documents
print("=== DOCUMENTS ROUTER IMPORTED ===", flush=True)

from app.routers.chat import router as chat_router
print("=== CHAT ROUTER IMPORTED ===", flush=True)


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


print("=== CREATING DATABASE TABLES ===", flush=True)

Base.metadata.create_all(
    bind=engine
)

print("=== DATABASE READY ===", flush=True)


app.include_router(health.router)

app.include_router(documents.router)

app.include_router(chat_router)

print("=== APPLICATION READY ===", flush=True)


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