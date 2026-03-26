# main.py

from fastapi import FastAPI
from routers import chatbot

app = FastAPI(
    title="AI Tools Dashboard",
    description="FastAPI backend for PDF + LLM chatbot",
    version="1.0.0"
)

# Include your chatbot routes
app.include_router(chatbot.router)

# ---------------- Root endpoint -----------------
@app.get("/")
def root():
    return {"message": "AI Tools Dashboard API is running. Use /docs for API docs."}