from fastapi import FastAPI
from routers import chatbot
from fastapi.middleware.cors import CORSMiddleware

# ✅ Step 1: Create app FIRST
app = FastAPI(
    title="AI Tools Dashboard",
    description="FastAPI backend for PDF + LLM chatbot",
    version="1.0.0"
)

# ✅ Step 2: Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ correct
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your chatbot routes
app.include_router(chatbot.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI Tools Dashboard API is running. Use /docs for API docs."}