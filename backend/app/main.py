from pathlib import Path

from fastapi import FastAPI, File, UploadFile

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

    return {
        "filename": file.filename,
        "status": "uploaded"
    }
