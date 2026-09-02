import math
import json
from typing import List

class EmbeddingService:
    def __init__(self):
        self.model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Loaded sentence-transformers model all-MiniLM-L6-v2 successfully.")
        except Exception as e:
            print(f"sentence-transformers not available or loading: {e}. Using feature vector fallback.")
            self.model = None

    def generate_embedding(self, text: str) -> List[float]:
        """Generates a normalized 384-dimensional vector embedding for text."""
        if not text:
            return [0.0] * 384

        if self.model:
            try:
                embedding = self.model.encode(text).tolist()
                return embedding
            except Exception as e:
                print(f"Error encoding with sentence-transformers: {e}")

        # Deterministic feature-hashing fallback producing 384-d normalized vector
        vector = [0.0] * 384
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = hash(word)
            vector[abs(h) % 384] += 1.0 + (idx * 0.01)

        # Normalize L2 norm
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]
        return vector

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Calculates cosine similarity between two vector lists."""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)
