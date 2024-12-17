# mistral_vectordb/embeddings/mistral.py
from typing import List, Optional, Union
import numpy as np
from datetime import datetime, timedelta
import threading
import json
from pathlib import Path
import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

logger = logging.getLogger(__name__)

class MistralEmbeddings:
    """
    Client for generating embeddings using official Mistral AI client
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "mistral-embed",
        cache_dir: Optional[str] = None,
        cache_duration: int = 24  # hours
    ):
        self.model = model
        self.client = MistralClient(api_key=api_key)
        self.dimension = 1024  # Mistral embeddings dimension
        
        # Cache setup
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".vectordb" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(hours=cache_duration)
        self.cache_lock = threading.Lock()
    
    def _get_cache_path(self, text: str) -> Path:
        """Generate cache file path for text"""
        # Use first 100 chars of text for filename
        safe_text = "".join(c if c.isalnum() else "_" for c in text[:100])
        return self.cache_dir / f"{safe_text}_{hash(text)}.json"
    
    def _load_from_cache(self, text: str) -> Optional[List[float]]:
        """Try to load embeddings from cache"""
        cache_path = self._get_cache_path(text)
        if not cache_path.exists():
            return None
            
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
                
            # Check if cache is expired
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > self.cache_duration:
                return None
                
            return cache_data['embedding']
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            return None
    
    def _save_to_cache(self, text: str, embedding: List[float]):
        """Save embeddings to cache"""
        cache_path = self._get_cache_path(text)
        cache_data = {
            'embedding': embedding,
            'timestamp': datetime.now().isoformat()
        }
        
        with self.cache_lock:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding using official Mistral client"""
        try:
            response = self.client.embeddings(
                model=self.model,
                input=[text]
            )
            return response.data[0].embedding
            
        except Exception as e:
            raise RuntimeError(f"Mistral AI API error: {str(e)}")
    
    def embed(self, text: Union[str, List[str]], use_cache: bool = True) -> np.ndarray:
        """
        Generate embeddings for text or list of texts
        
        Args:
            text: Single text string or list of texts
            use_cache: Whether to use cache for embeddings
            
        Returns:
            numpy array of embeddings with shape (n_texts, dimension)
        """
        if isinstance(text, str):
            texts = [text]
        else:
            texts = text
            
        embeddings = []
        for t in texts:
            if use_cache:
                cached_embedding = self._load_from_cache(t)
                if cached_embedding is not None:
                    embeddings.append(cached_embedding)
                    continue
                    
            embedding = self._get_embedding(t)
            if use_cache:
                self._save_to_cache(t, embedding)
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def bulk_embed(
        self,
        texts: List[str],
        batch_size: int = 32,
        use_cache: bool = True,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for large lists of texts in batches
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            use_cache: Whether to use cache for embeddings
            show_progress: Whether to show progress bar
            
        Returns:
            numpy array of embeddings with shape (n_texts, dimension)
        """
        from tqdm import tqdm
        
        all_embeddings = []
        iterator = tqdm(range(0, len(texts), batch_size)) if show_progress else range(0, len(texts), batch_size)
        
        for i in iterator:
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = []
            
            # Check cache first
            uncached_texts = []
            uncached_indices = []
            
            if use_cache:
                for j, text in enumerate(batch_texts):
                    cached_embedding = self._load_from_cache(text)
                    if cached_embedding is not None:
                        batch_embeddings.append(cached_embedding)
                    else:
                        uncached_texts.append(text)
                        uncached_indices.append(j)
            else:
                uncached_texts = batch_texts
                uncached_indices = list(range(len(batch_texts)))
            
            # Get embeddings for uncached texts
            if uncached_texts:
                response = self.client.embeddings(
                    model=self.model,
                    input=uncached_texts
                )
                
                for idx, emb_data in zip(uncached_indices, response.data):
                    embedding = emb_data.embedding
                    if use_cache:
                        self._save_to_cache(batch_texts[idx], embedding)
                    batch_embeddings.append(embedding)
            
            all_embeddings.append(np.array(batch_embeddings))
            
        return np.vstack(all_embeddings)

# Example usage in test file
def test_mistral_embeddings():
    """Test the MistralEmbeddings class with the official client"""
    api_key = "your-api-key"  # Replace with your API key
    embeddings = MistralEmbeddings(api_key=api_key)
    
    # Test single text
    text = "Test document"
    result = embeddings.embed(text)
    assert isinstance(result, np.ndarray)
    assert result.shape == (1, embeddings.dimension)
    
    # Test multiple texts
    texts = ["Document 1", "Document 2"]
    result = embeddings.embed(texts)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2, embeddings.dimension)
    
    # Test bulk embedding
    texts = ["Doc " + str(i) for i in range(5)]
    result = embeddings.bulk_embed(texts, batch_size=2)
    assert isinstance(result, np.ndarray)
    assert result.shape == (5, embeddings.dimension)