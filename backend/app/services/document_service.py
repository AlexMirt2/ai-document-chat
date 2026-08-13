from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document


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
    def get_all_documents(
        db: Session,
    ):

        return (
            db.query(Document)
            .order_by(
                Document.upload_date.desc()
            )
            .all()
        )

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
    ):

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if not document:
            return False

        upload_path = (
            Path(settings.upload_dir)
            / document.stored_filename
        )

        if upload_path.exists():
            upload_path.unlink()

        # Load vector storage only when needed.
        from app.services.ai.vector_store import VectorStore

        VectorStore.delete_document(
            document.id
        )

        db.delete(document)
        db.commit()

        return True