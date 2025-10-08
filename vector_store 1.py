import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pickle

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = None
        self.chunks = []
    
    def add_documents(self, chunks: List[Dict]):
        texts = [chunk["text"] for chunk in chunks]
        self.chunks.extend(chunks)
        
        # Generate embeddings for all texts
        all_texts = [chunk["text"] for chunk in self.chunks]
        self.embeddings = self.model.encode(all_texts)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings).flatten()
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Higher threshold for semantic similarity
                results.append((self.chunks[idx], float(similarities[idx])))
        
        return results
    
    def save(self, path: str):
        with open(f"{path}_chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        if self.embeddings is not None:
            np.save(f"{path}_embeddings.npy", self.embeddings)
    
    def load(self, path: str):
        try:
            with open(f"{path}_chunks.pkl", "rb") as f:
                self.chunks = pickle.load(f)
            self.embeddings = np.load(f"{path}_embeddings.npy")
        except FileNotFoundError:
            pass