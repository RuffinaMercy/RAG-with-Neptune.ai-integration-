from sentence_transformers import SentenceTransformer
import os

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print(f"🔹 Loading embedding model (FAST MODE): {model_name}")
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
        os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

        self.model = SentenceTransformer(
            model_name,
            device="cuda"  # use GPU
        )

    def embed(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

    def embed_chunks(self, texts):
        return self.embed(texts)
