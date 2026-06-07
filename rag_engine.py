# ============================================================
# rag_engine.py — RAG ka Core Engine
# Pinecone (vector DB) + Groq (LLM) ko connect karta hai
# ============================================================

from pinecone import Pinecone, ServerlessSpec
from groq import Groq
import os
import time
import uuid
from dotenv import load_dotenv

load_dotenv()


class RAGEngine:
    def __init__(self):
        # Pinecone se connect karo
        print("Pinecone se connect ho raha hai...")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        index_name = os.getenv("PINECONE_INDEX_NAME", "rag-chatbot")
        dimension  = 1024  # multilingual-e5-large ka output size

        # Index nahi hai to banao, hai to connect karo
        existing = [idx.name for idx in self.pc.list_indexes()]
        if index_name not in existing:
            print(f"Naya index bana raha hai: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            # Index ready hone ka intezaar karo
            waited = 0
            while waited < 60:
                status = self.pc.describe_index(index_name).status
                if status.get("ready", False):
                    break
                time.sleep(3)
                waited += 3
                print(f"Index ready hone ka wait kar raha hai... ({waited}s)")
        else:
            print(f"Existing index se connect: {index_name}")

        self.index = self.pc.Index(index_name)

        # Groq se connect karo
        print("Groq LLM se connect ho raha hai...")
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("RAG Engine ready hai!")

    def get_embedding(self, text: str, input_type: str = "query"):
        """Text ko vector mein convert karo"""
        response = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[text],
            parameters={"input_type": input_type}
        )
        return response.data[0].values

    def answer(self, question: str) -> dict:
        """Sawaal ka jawab do — Pinecone se context lo, Groq se jawab banao"""

        # Step 1: Sawaal ko vector banao
        query_vector = self.get_embedding(question, input_type="query")

        # Step 2: Pinecone mein similar chunks dhundo
        results = self.index.query(
            vector=query_vector,
            top_k=4,
            include_metadata=True
        )

        chunks  = []
        sources = []

        for match in results["matches"]:
            print(f"Score: {match['score']:.3f} | Source: {match['metadata'].get('source')}")
            # Sirf relevant chunks lo (0.5 se upar)
            if match["score"] > 0.5:
                chunks.append(match["metadata"].get("text", ""))
                sources.append(match["metadata"].get("source", "Unknown"))

        # Koi relevant chunk nahi mila
        if not chunks:
            return {
                "answer": "Uploaded documents mein is sawaal ka jawab nahi mila. Pehle relevant document upload karo.",
                "sources": []
            }

        # Step 3: Context bana kar Groq ko bhejo
        context = "\n\n".join(chunks)

        prompt = f"""You are a helpful AI assistant. Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information in the uploaded documents."

Context:
{context}

Question: {question}

Answer:"""

        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )

        return {
            "answer": response.choices[0].message.content.strip(),
            "sources": list(set(sources))
        }

    def add_document(self, file_path: str, source_name: str) -> int:
        """Document ko parse karo, chunks banao, Pinecone mein store karo"""
        from pdf_processor import DocumentProcessor

        processor = DocumentProcessor()
        chunks    = processor.process(file_path, source_name)

        if not chunks:
            raise ValueError("File se koi text nahi nikla.")

        # Har chunk ko embed karo
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk["text"], input_type="passage")
            vectors.append({
                "id": f"{source_name}_{i}_{uuid.uuid4().hex[:8]}",
                "values": embedding,
                "metadata": {
                    "text": chunk["text"],
                    "source": chunk["source"]
                }
            })

        # 100 ke batch mein Pinecone mein daalo
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            self.index.upsert(vectors=vectors[i:i + batch_size])

        print(f"'{source_name}' se {len(vectors)} chunks index ho gaye!")
        return len(vectors)
