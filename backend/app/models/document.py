from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    filename: Mapped[str] = mapped_column(String)

    stored_filename: Mapped[str] = mapped_column(String)

    content_type: Mapped[str] = mapped_column(String)

    upload_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )