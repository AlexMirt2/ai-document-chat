from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    Response,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.dependencies import get_db
from app.models.document import Document
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path(settings.upload_dir)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    unique_name = f"{uuid4()}.pdf"

    destination = (
        UPLOAD_DIR / unique_name
    )

    try:

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        document = (
            DocumentService.create_document(
                db=db,
                filename=file.filename,
                stored_filename=unique_name,
                content_type=file.content_type,
            )
        )

        print(
            "\n========== DOCUMENT PROCESSING ==========",
            flush=True,
        )

        # Import heavy/processing services only
        # when an actual PDF is uploaded.
        from app.services.ai.document_loader import (
            DocumentLoader,
        )

        from app.services.ai.text_splitter import (
            TextSplitter,
        )

        from app.services.ai.vector_store import (
            VectorStore,
        )

        pages = DocumentLoader.load(
            str(destination)
        )

        print(
            f"Pages extracted: {len(pages)}",
            flush=True,
        )

        chunks = TextSplitter.split(
            pages
        )

        print(
            f"Chunks created: {len(chunks)}",
            flush=True,
        )

        VectorStore.add_document(
            document.id,
            chunks,
        )

        print(
            "Embeddings/vector processing complete",
            flush=True,
        )

        print(
            "========== PROCESS COMPLETE ==========\n",
            flush=True,
        )

        return {
            "id": document.id,
            "filename": document.filename,
            "stored_filename": document.stored_filename,
            "pages": len(pages),
            "chunks": len(chunks),
            "message": "Upload successful",
        }

    except Exception as exc:

        print(
            "UPLOAD ERROR:",
            repr(exc),
            flush=True,
        )

        # Remove uploaded PDF if processing failed.
        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF.",
        )


@router.get("")
async def get_documents(
    db: Session = Depends(get_db),
):

    documents = (
        DocumentService.get_all_documents(
            db
        )
    )

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "stored_filename": document.stored_filename,
            "upload_date": document.upload_date,
        }
        for document in documents
    ]


@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    file_path = (
        Path(settings.upload_dir)
        / document.stored_filename
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return FileResponse(
        path=file_path,
        filename=document.filename,
        media_type=document.content_type,
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):

    success = (
        DocumentService.delete_document(
            db,
            document_id,
        )
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return Response(
        status_code=204
    )