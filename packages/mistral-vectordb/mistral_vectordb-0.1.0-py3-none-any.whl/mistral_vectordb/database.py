# vectordb/core/database.py
from typing import List, Dict, Optional
import numpy as np
from .storage import VectorStorage
from .index import QuantizedIndex

class VectorDatabase:
    def __init__(self, path: str, dimension: int):
        self.storage = VectorStorage(path, dimension)
        self.index = QuantizedIndex(dimension)
        self.dimension = dimension
    
    def add_document(self, content: str, embedding: np.ndarray, metadata: Dict) -> int:
        # Generate document ID (you might want to use a more sophisticated method)
        doc_id = len(self.index.id_mapping)
        
        # Add to storage
        self.storage.add_vector(doc_id, embedding, {
            'content': content,
            **metadata
        })
        
        # Add to index
        self.index.add([doc_id], embedding.reshape(1, -1))
        
        return doc_id
    
    def search(self, query_embedding: np.ndarray, k: int = 10, 
              threshold: float = 0.7, metadata_filters: Optional[Dict] = None) -> List[Dict]:
        # Search in index
        results = self.index.search(query_embedding, k)
        
        # Process results
        processed_results = []
        for doc_id, score in results:
            if score < threshold:
                continue
                
            # Get document from storage
            vector, metadata = self.storage.get_vector(doc_id)
            
            # Apply metadata filters
            if metadata_filters and not all(
                metadata.get(k) == v for k, v in metadata_filters.items()
            ):
                continue
            
            processed_results.append({
                'id': doc_id,
                'content': metadata.pop('content'),
                'metadata': metadata,
                'similarity_score': score
            })
        
        return processed_results