from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentService:

    @staticmethod
    def create_document(
        db: Session,
        filename: str,
        stored_filename: str,
        content_type: str
    ) -> Document:

        document = Document(
            filename=filename,
            stored_filename=stored_filename,
            content_type=content_type
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document