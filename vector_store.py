import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pickle

class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.embeddings = None
        self.chunks = []
        self.is_fitted = False
    
    def add_documents(self, chunks: List[Dict]):
        texts = [chunk["text"] for chunk in chunks]
        self.chunks.extend(chunks)
        
        # Fit vectorizer on all texts
        all_texts = [chunk["text"] for chunk in self.chunks]
        self.embeddings = self.vectorizer.fit_transform(all_texts)
        self.is_fitted = True
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        if not self.is_fitted or len(self.chunks) == 0:
            return []
        
        # Transform query
        query_embedding = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings).flatten()
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append((self.chunks[idx], float(similarities[idx])))
        
        return results
    
    def save(self, path: str):
        with open(f"{path}_chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        with open(f"{path}_vectorizer.pkl", "wb") as f:
            pickle.dump(self.vectorizer, f)
        if self.embeddings is not None:
            np.save(f"{path}_embeddings.npy", self.embeddings.toarray())
    
    def load(self, path: str):
        try:
            with open(f"{path}_chunks.pkl", "rb") as f:
                self.chunks = pickle.load(f)
            with open(f"{path}_vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            self.embeddings = np.load(f"{path}_embeddings.npy")
            self.is_fitted = True
        except FileNotFoundError:
            pass