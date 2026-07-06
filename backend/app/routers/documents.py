from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from uuid import uuid4

from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    unique_name = f"{uuid4()}.pdf"

    destination = UPLOAD_DIR / unique_name

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = DocumentService.create_document(
    db=db,
    filename=file.filename,
    stored_filename=unique_name,
    content_type=file.content_type
)

    return {
    "id": document.id,
    "filename": document.filename,
    "stored_filename": document.stored_filename,
    "message": "Upload successful"
}