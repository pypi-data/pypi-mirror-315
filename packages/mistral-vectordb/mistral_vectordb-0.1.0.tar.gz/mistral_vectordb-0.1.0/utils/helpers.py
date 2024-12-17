# vectordb/utils/helpers.py
import numpy as np
from typing import List

def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """Normalize vectors to unit length"""
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))