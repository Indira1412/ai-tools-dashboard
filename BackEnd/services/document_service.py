# services/document_service.py

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import ollama
# ---------------- Chat Memory -----------------
chat_history = []


from services.vector_store import search_documents

# ---------------- Initialize embedding model -----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PDF Utilities -----------------
def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# ---------------- Embeddings -----------------
def create_embeddings(chunks: list):
    return model.encode(chunks).tolist()


# ---------------- Retrieve chunks -----------------
def retrieve_chunks(question: str, k: int = 3):

    query_embedding = model.encode([question]).tolist()[0]

    return search_documents(query_embedding, k)

# ---------------- Generate AI answer using Ollama -----------------
def get_ai_answer(question: str, k: int = 3):

    # 1. Retrieve chunks from DB
    chunks = retrieve_chunks(question, k)

    if not chunks:
        return "No relevant information found in the document."

    context = "\n".join(chunks)

    # 2. Convert chat history into text
    history_text = ""
    for item in chat_history:
        history_text += f"User: {item['question']}\n"
        history_text += f"Assistant: {item['answer']}\n"

    # 3. Build prompt with history + context
    prompt = f"""
You are an AI assistant.

Conversation so far:
{history_text}

Context from document:
{context}

Current Question:
{question}

Answer clearly:
"""

    # 4. Call Ollama
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response["message"]["content"]

    # 5. Save to memory
    chat_history.append({
        "question": question,
        "answer": answer
    })

    return answer