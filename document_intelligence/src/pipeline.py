# import os
# import re
# from typing import List

# from src.document_loader import DocumentLoader
# from src.adaptive_chunker import AdaptiveChunker
# from src.embeddings import EmbeddingModel
# from src.retriever import Retriever
# from src.qa_model import QAModel
# from src.pdf_highlighter import PDFHighlighter
# from config import MODEL_NAME, LOCAL_MODEL_PATH


# class DocumentPipeline:
#     def __init__(self):
#         print("🚀 Initializing Hybrid RAG Pipeline...")
#         self.loader = DocumentLoader()
#         self.chunker = AdaptiveChunker()
#         self.embedder = EmbeddingModel()
#         self.retriever = Retriever(self.embedder)
#         self.qa = QAModel(MODEL_NAME, LOCAL_MODEL_PATH)
#         self.highlighter = PDFHighlighter()

#         self.current_doc = None
#         self.current_text = ""
#         self.chunks: List[str] = []
#         self.index_built = False

#     # ================= DOCUMENT UPLOAD ================= #
#     def upload_document(self, file_path: str):
#         print(f"📂 Loading document: {file_path}")
#         self.current_doc = file_path

#         text, metadata = self.loader.load_document(file_path)
#         self.current_text = text

#         file_size = os.path.getsize(file_path) if os.path.exists(file_path) else None
#         chunk_size = self.chunker.calculate_chunk_size(text, file_size)

#         self.chunks = self.chunker.chunk_text(text, chunk_size)

#         if self.chunks:
#             embeddings = self.embedder.embed_chunks(self.chunks)
#             self.retriever.build_index(self.chunks, embeddings)
#             self.index_built = True

#         return {
#             "chunks": len(self.chunks),
#             "chunk_size": chunk_size,
#             "metadata": metadata,
#         }

#     # ================= HYBRID CHAT ================= #
#     def chat(self, question: str):
#         if not self.index_built:
#             return "❌ Please upload a document first.", [], {}

#         # 1️⃣ Retrieve relevant chunks
#         relevant_chunks, scores = self.retriever.get_relevant_chunks(question, top_k=5)

#         if not relevant_chunks:
#             return "⚠️ Answer not found in the document.", [], {}

#         # 2️⃣ Filter chunks by keyword overlap
#         question_words = set(question.lower().split())
#         filtered_chunks = []

#         for chunk in relevant_chunks:
#             chunk_words = set(chunk.lower().split())
#             if question_words.intersection(chunk_words):
#                 filtered_chunks.append(chunk)

#         if not filtered_chunks:
#             filtered_chunks = relevant_chunks[:2]

#         # 3️⃣ Build context
#         context = "\n\n".join(filtered_chunks[:2])[:2000]

#         q = question.lower()

#         # ================= FACTUAL QUESTIONS → EXTRACTIVE MODEL ================= #
#         factual_keywords = ["phone", "number", "email", "name", "date", "contact"]

#         if any(k in q for k in factual_keywords):
#             answer = self.qa.extract_answer(context, question)

#             # Regex fallback for phone/email
#             phone_pattern = r"\+?\d[\d\s\-]{7,}\d"
#             email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

#             if "phone" in q or "number" in q:
#                 match = re.search(phone_pattern, context)
#                 if match:
#                     return match.group(), filtered_chunks, {"model": "regex"}

#             if "email" in q:
#                 match = re.search(email_pattern, context)
#                 if match:
#                     return match.group(), filtered_chunks, {"model": "regex"}

#             if answer.strip():
#                 return answer, filtered_chunks, {"model": "extractive"}

#         # ================= CONCEPTUAL QUESTIONS → GENERATIVE MODEL ================= #
#         answer = self.qa.generate_answer(context, question)

#         if len(answer.strip()) > 3:
#             return answer, filtered_chunks, {"model": "generative"}

#         return "⚠️ The document does not contain this information.", filtered_chunks, {}

#     # ================= PDF HIGHLIGHT ================= #
#     def highlight_keywords(self, keywords: str):
#         if not self.current_doc or not self.current_doc.endswith(".pdf"):
#             return None, [], [], ["Only PDF files supported"]

#         return self.highlighter.highlight_pdf(self.current_doc, keywords)












import os
import re
from typing import List

from src.document_loader import DocumentLoader
from src.adaptive_chunker import AdaptiveChunker
from src.embeddings import EmbeddingModel
from src.retriever import Retriever
from src.qa_model import QAModel


class DocumentPipeline:
    def __init__(self):
        print("🚀 Initializing RAG Pipeline (Hybrid mode)...")

        self.loader = DocumentLoader()
        self.chunker = AdaptiveChunker()
        self.embedder = EmbeddingModel()
        self.retriever = Retriever(self.embedder)
        self.qa = QAModel()

        self.chunks: List[str] = []
        self.index_built = False

    # ---------------- Document Upload ----------------
    def upload_document(self, file_path: str):
        print(f"📂 Loading document: {file_path}")

        text, _ = self.loader.load_document(file_path)
        chunk_size = self.chunker.calculate_chunk_size(text, None)
        self.chunks = self.chunker.chunk_text(text, chunk_size)

        embeddings = self.embedder.embed_chunks(self.chunks)
        self.retriever.build_index(self.chunks, embeddings)

        self.index_built = True
        print(f"✅ Document indexed with {len(self.chunks)} chunks")

    # ---------------- Chat ----------------
    def chat(self, question: str):
        if not self.index_built:
            return "Upload a document first", [], {}

        relevant_chunks, _ = self.retriever.get_relevant_chunks(question, top_k=5)
        context = "\n\n".join(relevant_chunks[:2])[:2000]

        q = question.lower()

        # 🔹 FACTUAL → Extractive
        factual_keywords = [
            "name", "email", "phone", "number",
            "date", "degree", "college", "skill"
        ]

        if any(k in q for k in factual_keywords):
            answer = self.qa.extract_answer(context, question)
            return answer, relevant_chunks, {"model": "extractive"}

        # 🔹 CONCEPTUAL → Generative
        answer = self.qa.generate_answer(context, question)
        return answer, relevant_chunks, {"model": "generative"}
