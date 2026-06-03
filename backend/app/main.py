from pathlib import Path

from fastapi import FastAPI, File, UploadFile

from app.services.pdf_service import extract_text_from_pdf

app = FastAPI(
    title="Document Grounded AI Assistant",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    extracted_text = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "characters": len(extracted_text),
        "preview": extracted_text[:500]
    }
