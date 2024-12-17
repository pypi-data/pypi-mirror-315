# vectordb/core/index.py
import faiss
import numpy as np
from typing import List, Tuple, Optional

class QuantizedIndex:
    def __init__(self, dimension: int, n_lists: int = 100):
        self.dimension = dimension
        self.n_lists = n_lists
        
        # Create two-level index
        self.quantizer = faiss.IndexHNSWFlat(dimension, 32)
        self.index = faiss.IndexIVFPQ(
            self.quantizer,
            dimension,
            n_lists,
            8,  # num sub-vectors
            8   # bits per code
        )
        self.index.nprobe = 10
        
        self.is_trained = False
        self.id_mapping = {}
    
    def train(self, vectors: np.ndarray):
        if not self.is_trained and vectors.shape[0] > 0:
            self.index.train(vectors)
            self.is_trained = True
    
    def add(self, ids: List[int], vectors: np.ndarray):
        if not self.is_trained:
            self.train(vectors)
        self.index.add_with_ids(vectors, np.array(ids))
        
        for i, vid in enumerate(ids):
            self.id_mapping[vid] = i
    
    def search(self, query: np.ndarray, k: int) -> List[Tuple[int, float]]:
        D, I = self.index.search(query.reshape(1, -1), k)
        
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx >= 0:
                original_id = self.id_mapping.get(int(idx))
                if original_id is not None:
                    results.append((original_id, float(dist)))
        
        return results