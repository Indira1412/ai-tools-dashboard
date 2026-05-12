# routers/chatbot.py

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
from services.document_service import chat_history
from services.vector_store import reset_collection

# ---------------- Import from services -----------------
from services.document_service import (
    extract_text_from_pdf,
    split_text,
    create_embeddings,
    get_ai_answer
)
from services.vector_store import store_embeddings  # Chroma storage

# ---------------- Setup -----------------
router = APIRouter()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- Request Model -----------------
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3  # number of chunks to retrieve

# ---------------- /ask endpoint -----------------
@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Receives a user question, retrieves top chunks from Chroma,
    generates AI answer using Ollama (Llama3), and returns it.
    """
    try:
        answer = get_ai_answer(request.question, k=request.top_k)
        return {
    "question": request.question,
    "answer": answer,
    "chat_history": chat_history
}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-chat")
def reset_chat():

    # Clear chat history
    chat_history.clear()

    # Clear vector database
    reset_collection()

    return {
        "message": "Chat reset successful"
    }
# ---------------- /upload-document endpoint -----------------
@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document, extract text, split into chunks,
    create embeddings, and store them in Chroma.
    """
    # ---------------- File validation -----------------
    from utils.file_validator import validate_file
    is_valid, message = validate_file(file)
    if not is_valid:
        return {"error": message}

    # ---------------- Save file -----------------
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------------- Process PDF -----------------
    text = extract_text_from_pdf(file_path)
    chunks = split_text(text)
    embeddings = create_embeddings(chunks)

    # ---------------- Store embeddings in Chroma -----------------
    store_embeddings(chunks, embeddings)

    return {
        "message": "Document processed and stored successfully",
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0])
    }