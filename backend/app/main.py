import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

print("=== STARTING APPLICATION ===", flush=True)

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


print("=== BASIC APPLICATION READY ===", flush=True)


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