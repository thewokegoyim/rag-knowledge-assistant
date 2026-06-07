# ============================================================
# pdf_processor.py — Document Parser + Text Chunker
# PDF, DOCX, TXT, CSV, XLSX, HTML sab support karta hai
# ============================================================

import os
import re
import pandas as pd


class DocumentProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        # chunk_size: har chunk mein kitne words
        # chunk_overlap: consecutive chunks mein shared words
        self.chunk_size    = chunk_size
        self.chunk_overlap = chunk_overlap

    def process(self, file_path: str, source_name: str) -> list:
        """File ko read karo, text nikalo, chunks banao"""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File nahi mili: {file_path}")

        ext  = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".pdf":
            text = self._read_pdf(file_path)
        elif ext == ".docx":
            text = self._read_docx(file_path)
        elif ext in (".txt", ".md"):
            text = self._read_text(file_path)
        elif ext == ".csv":
            text = self._read_csv(file_path)
        elif ext == ".xlsx":
            text = self._read_xlsx(file_path)
        elif ext in (".html", ".htm"):
            text = self._read_html(file_path)
        else:
            raise ValueError(f"Yeh format support nahi karta: '{ext}'")

        # Extra whitespace clean karo
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        if not text:
            raise ValueError("File se koi text nahi nikla. File empty ya sirf images wali ho sakti hai.")

        print(f"'{source_name}' se {len(text)} characters nikale")

        chunks = self._split_into_chunks(text)
        print(f"Total chunks bane: {len(chunks)}")

        return [{"text": chunk, "source": source_name} for chunk in chunks]

    # ── Readers ──────────────────────────────────────────────

    def _read_pdf(self, file_path: str) -> str:
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"[Page {i+1}]\n{page_text.strip()}\n\n"
                        print(f"  Page {i+1}: {len(page_text)} chars")
                    else:
                        print(f"  Page {i+1}: text nahi mila (image-only page?)")
            return text
        except ImportError:
            raise ImportError("pdfplumber install karo: pip install pdfplumber")

    def _read_docx(self, file_path: str) -> str:
        try:
            from docx import Document as DocxDocument
            doc   = DocxDocument(file_path)
            paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paras)
        except ImportError:
            raise ImportError("python-docx install karo: pip install python-docx")

    def _read_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def _read_csv(self, file_path: str) -> str:
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
        return df.to_string(index=False)

    def _read_xlsx(self, file_path: str) -> str:
        xl     = pd.ExcelFile(file_path)
        sheets = []
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            sheets.append(f"[Sheet: {sheet_name}]\n{df.to_string(index=False)}")
        return "\n\n".join(sheets)

    def _read_html(self, file_path: str) -> str:
        try:
            from bs4 import BeautifulSoup
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                soup = BeautifulSoup(f.read(), "lxml")
            for tag in soup(["script", "style", "head", "meta"]):
                tag.decompose()
            return soup.get_text(separator="\n")
        except ImportError:
            raise ImportError("beautifulsoup4 aur lxml install karo: pip install beautifulsoup4 lxml")

    # ── Chunker ──────────────────────────────────────────────

    def _split_into_chunks(self, text: str) -> list:
        """Text ko overlapping chunks mein todo"""
        words  = text.split()
        chunks = []
        i      = 0

        while i < len(words):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            i += self.chunk_size - self.chunk_overlap

        return chunks
