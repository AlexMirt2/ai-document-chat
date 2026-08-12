from pathlib import Path

from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.ai.vector_store import VectorStore


class DocumentService:

    @staticmethod
    def create_document(
        db: Session,
        filename: str,
        stored_filename: str,
        content_type: str,
    ) -> Document:

        document = Document(
            filename=filename,
            stored_filename=stored_filename,
            content_type=content_type,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def update_ai_metadata(
        db: Session,
        document_id: int,
        summary: str,
        keywords: str,
    ):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return

        document.summary = summary
        document.keywords = keywords

        db.commit()

    @staticmethod
    def get_document(
        db: Session,
        document_id: int,
    ):

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    @staticmethod
    def get_all_documents(db: Session):

        return (
            db.query(Document)
            .order_by(Document.upload_date.desc())
            .all()
        )

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
    ):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return False

        file_path = (
            Path("uploads")
            / document.stored_filename
        )

        if file_path.exists():
            file_path.unlink()

        VectorStore.delete_document(
            document.id
        )

        db.delete(document)
        db.commit()

        return True