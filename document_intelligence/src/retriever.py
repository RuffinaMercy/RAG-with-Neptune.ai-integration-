import numpy as np
from typing import List, Tuple


class Retriever:
    def __init__(self, embedder):
        self.embedder = embedder
        self.chunks = []
        self.embeddings = None

    def build_index(self, chunks, embeddings):
        self.chunks = chunks
        self.embeddings = np.array(embeddings)
        print(f"✅ Index built with {len(chunks)} chunks")

    def get_relevant_chunks(self, query: str, top_k: int = 3) -> Tuple[List[str], List[float]]:
        if self.embeddings is None or len(self.chunks) == 0:
            return [], []

        query_vec = self.embedder.embed([query])[0]

        scores = np.dot(self.embeddings, query_vec) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec) + 1e-10
        )

        top_indices = np.argsort(scores)[-top_k:][::-1]

        chunks = [self.chunks[i] for i in top_indices]
        top_scores = [float(scores[i]) for i in top_indices]

        return chunks, top_scores
