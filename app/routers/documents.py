import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File

from app.ai.ingestion import ingest_pdf

router = APIRouter()

@router.post("/documents/ingest")
def ingest_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    chunk_count = ingest_pdf(tmp_path)

    return {"filename": file.filename, "Chunks created": chunk_count}