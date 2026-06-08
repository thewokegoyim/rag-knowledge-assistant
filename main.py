# ============================================================
# main.py — FastAPI Backend
# RAG Knowledge Assistant
# ============================================================
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGEngine
import os

app = FastAPI(title="RAG Knowledge Assistant API")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
def serve_ui():
    return FileResponse("static/index.html")
# CORS — frontend ko allow karo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# RAG engine ek baar initialize karo
rag = RAGEngine()


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def root():
    return {"message": "RAG Knowledge Assistant is running!"}


@app.get("/health")
def health():
    """Frontend is check karta hai ke backend online hai ya nahi"""
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question empty nahi hona chahiye")
    try:
        result = rag.answer(request.question)
        return AnswerResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    # Sirf yeh formats allow hain
    allowed_types = [".pdf", ".txt", ".md", ".docx", ".csv", ".xlsx", ".html", ".htm"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Yeh format support nahi: {ext}")

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    # Max 20MB check
    contents = file.file.read()
    if len(contents) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File bohat bari hai. Max 20MB allowed hai.")

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        count = rag.add_document(file_path, file.filename)
        return {"message": f"{file.filename} se {count} chunks index ho gaye!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
