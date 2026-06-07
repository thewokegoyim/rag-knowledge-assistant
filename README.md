---
title: RAG Knowledge Assistant
emoji: 🧠
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---
# rag-knowledge-assistant
RAG-powered Knowledge Assistant — Upload documents, ask questions, get AI answers grounded in your data. Built with FastAPI, Pinecone, Groq &amp; LLaMA 3.3 70B.
# 🧠 RAG Knowledge Assistant

> Upload documents. Ask questions. Get AI answers grounded in **your** data — no hallucinations.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 What is this?

A fully local-ready **Retrieval-Augmented Generation (RAG)** system. You upload any document, it gets embedded into a vector database (Pinecone), and when you ask a question, the most relevant chunks are retrieved and passed to LLaMA 3.3 70B (via Groq) to generate a precise, sourced answer.

No made-up facts. Only answers from what you give it.

---

## ✨ Features

- 📄 **Multi-format support** — PDF, DOCX, TXT, MD, CSV, XLSX, HTML
- 🔍 **Semantic search** via Pinecone vector database
- ⚡ **Blazing fast LLM** via Groq (LLaMA 3.3 70B)
- 🌍 **Multilingual embeddings** — works in Urdu, English & more (multilingual-e5-large)
- 🔗 **REST API** with FastAPI — easy to integrate anywhere
- 🗂️ **Source attribution** — every answer tells you which document it came from
- 📦 **Chunking with overlap** — smart text splitting for better retrieval

---

## 🏗️ Architecture

```
User Question
     │
     ▼
[Embed Question] ──► multilingual-e5-large
     │
     ▼
[Vector Search] ──► Pinecone (top-k relevant chunks)
     │
     ▼
[LLM Generation] ──► Groq / LLaMA 3.3 70B
     │
     ▼
Answer + Sources
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Vector DB | Pinecone (Serverless) |
| LLM | LLaMA 3.3 70B via Groq |
| Embeddings | multilingual-e5-large (Pinecone Inference) |
| Document Parsing | pdfplumber, python-docx, pandas, BeautifulSoup |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/thewokegoyim/rag-knowledge-assistant.git
cd rag-knowledge-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-chatbot
GROQ_API_KEY=your_groq_api_key
```

> Get your keys:
> - Pinecone → [app.pinecone.io](https://app.pinecone.io)
> - Groq → [console.groq.com](https://console.groq.com)

### 4. Run the server

```bash
python main.py
```

Server starts at `http://localhost:8080`

---

## 📡 API Endpoints

### `GET /health`
Check if the server is running.

```json
{ "status": "ok" }
```

---

### `POST /upload`
Upload a document to be indexed.

```bash
curl -X POST http://localhost:8080/upload \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{ "message": "your_document.pdf se 42 chunks index ho gaye!" }
```

---

### `POST /ask`
Ask a question against your uploaded documents.

```bash
curl -X POST http://localhost:8080/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}'
```

**Response:**
```json
{
  "answer": "The refund policy states that...",
  "sources": ["your_document.pdf"]
}
```

---

## 📁 Project Structure

```
rag-knowledge-assistant/
├── main.py            # FastAPI server & API routes
├── rag_engine.py      # Core RAG logic (Pinecone + Groq)
├── pdf_processor.py   # Document parser & text chunker
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── README.md
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_INDEX_NAME` | `rag-chatbot` | Name of your Pinecone index |
| `chunk_size` | `500` | Words per chunk |
| `chunk_overlap` | `100` | Overlapping words between chunks |
| `top_k` | `4` | Number of chunks retrieved per query |
| `score_threshold` | `0.5` | Minimum similarity score to include a chunk |
| `max_tokens` | `500` | Max LLM response length |

---

## 🔒 Security Notes

- Never commit your `.env` file — it's in `.gitignore`
- Use `.env.example` to share variable names without values
- File uploads are capped at **20MB**

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**@thewokegoyim** — [github.com/thewokegoyim](https://github.com/thewokegoyim)

---

*Built with FastAPI · Pinecone · Groq · LLaMA 3.3 70B*# 🧠 RAG Knowledge Assistant

> Upload documents. Ask questions. Get AI answers grounded in **your** data — no hallucinations.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 What is this?

A fully local-ready **Retrieval-Augmented Generation (RAG)** system. You upload any document, it gets embedded into a vector database (Pinecone), and when you ask a question, the most relevant chunks are retrieved and passed to LLaMA 3.3 70B (via Groq) to generate a precise, sourced answer.

No made-up facts. Only answers from what you give it.

---

## ✨ Features

- 📄 **Multi-format support** — PDF, DOCX, TXT, MD, CSV, XLSX, HTML
- 🔍 **Semantic search** via Pinecone vector database
- ⚡ **Blazing fast LLM** via Groq (LLaMA 3.3 70B)
- 🌍 **Multilingual embeddings** — works in Urdu, English & more (multilingual-e5-large)
- 🔗 **REST API** with FastAPI — easy to integrate anywhere
- 🗂️ **Source attribution** — every answer tells you which document it came from
- 📦 **Chunking with overlap** — smart text splitting for better retrieval

---

## 🏗️ Architecture

```
User Question
     │
     ▼
[Embed Question] ──► multilingual-e5-large
     │
     ▼
[Vector Search] ──► Pinecone (top-k relevant chunks)
     │
     ▼
[LLM Generation] ──► Groq / LLaMA 3.3 70B
     │
     ▼
Answer + Sources
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Vector DB | Pinecone (Serverless) |
| LLM | LLaMA 3.3 70B via Groq |
| Embeddings | multilingual-e5-large (Pinecone Inference) |
| Document Parsing | pdfplumber, python-docx, pandas, BeautifulSoup |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/thewokegoyim/rag-knowledge-assistant.git
cd rag-knowledge-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-chatbot
GROQ_API_KEY=your_groq_api_key
```

> Get your keys:
> - Pinecone → [app.pinecone.io](https://app.pinecone.io)
> - Groq → [console.groq.com](https://console.groq.com)

### 4. Run the server

```bash
python main.py
```

Server starts at `http://localhost:8080`

---

## 📡 API Endpoints

### `GET /health`
Check if the server is running.

```json
{ "status": "ok" }
```

---

### `POST /upload`
Upload a document to be indexed.

```bash
curl -X POST http://localhost:8080/upload \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{ "message": "your_document.pdf se 42 chunks index ho gaye!" }
```

---

### `POST /ask`
Ask a question against your uploaded documents.

```bash
curl -X POST http://localhost:8080/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}'
```

**Response:**
```json
{
  "answer": "The refund policy states that...",
  "sources": ["your_document.pdf"]
}
```

---

## 📁 Project Structure

```
rag-knowledge-assistant/
├── main.py            # FastAPI server & API routes
├── rag_engine.py      # Core RAG logic (Pinecone + Groq)
├── pdf_processor.py   # Document parser & text chunker
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── README.md
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PINECONE_INDEX_NAME` | `rag-chatbot` | Name of your Pinecone index |
| `chunk_size` | `500` | Words per chunk |
| `chunk_overlap` | `100` | Overlapping words between chunks |
| `top_k` | `4` | Number of chunks retrieved per query |
| `score_threshold` | `0.5` | Minimum similarity score to include a chunk |
| `max_tokens` | `500` | Max LLM response length |

---

## 🔒 Security Notes

- Never commit your `.env` file — it's in `.gitignore`
- Use `.env.example` to share variable names without values
- File uploads are capped at **20MB**

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**@thewokegoyim** — [github.com/thewokegoyim](https://github.com/thewokegoyim)

---

*Built with FastAPI · Pinecone · Groq · LLaMA 3.3 70B*
