from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.vectorstore.chroma_store import add_chunks
from pydantic import BaseModel
from app.vectorstore.chroma_store import search_chunks

app = FastAPI(
    title="Document Grounded AI Assistant",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Seuls les fichiers PDF sont acceptés")
    
    file_path = UPLOAD_DIR / file.filename
    
    if file_path.exists():
        base, ext = file_path.stem, file_path.suffix
        counter = 1
        while file_path.exists():
            file_path = UPLOAD_DIR / f"{base}_{counter}{ext}"
            counter += 1
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        extracted_text = extract_text_from_pdf(str(file_path))
        if not extracted_text.strip():
            raise HTTPException(400, "Le PDF ne contient pas de texte extractible")
        
        chunks = chunk_text(extracted_text)
        add_chunks(chunks, file.filename)
        
        return {
            "filename": file.filename,
            "characters": len(extracted_text),
            "chunks": len(chunks),
            "stored_chunks": len(chunks)
        }
    except HTTPException:
        
        file_path.unlink(missing_ok=True)
        raise
    except Exception as e:
        
        file_path.unlink(missing_ok=True)
        raise HTTPException(500, f"Erreur lors du traitement: {str(e)}")


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(400, "La question ne peut pas être vide")
    
    documents = search_chunks(request.question)

    if not documents:
        return {
            "question": request.question,
            "documents": [],
            "message": "Aucun résultat trouvé"
        }
    
    return {
        "question": request.question,
        "documents": documents
    }


@app.get("/uploads")
async def list_uploads():
    return {
        "files": [f.name for f in UPLOAD_DIR.iterdir() if f.is_file()]
    }
