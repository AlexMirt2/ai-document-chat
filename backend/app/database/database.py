from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


database_path = Path(settings.database_path)

database_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)


DATABASE_URL = f"sqlite:///{settings.database_path}"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)