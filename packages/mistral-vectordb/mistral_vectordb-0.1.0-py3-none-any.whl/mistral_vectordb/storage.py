# vectordb/core/storage.py
import os
import mmap
import numpy as np
from pathlib import Path
import json
import zlib
from typing import Dict, Optional, Tuple
from datetime import datetime

class VectorStorage:
    def __init__(self, path: str, vector_dim: int):
        self.path = Path(path)
        self.vector_dim = vector_dim
        self.segment_size = 10000
        self.segments = {}
        
        self.path.mkdir(parents=True, exist_ok=True)
        self._load_segments()
    
    def _load_segments(self):
        metadata_path = self.path / "segments.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.segments = json.load(f)
    
    def _save_segments(self):
        with open(self.path / "segments.json", 'w') as f:
            json.dump(self.segments, f)
    
    def add_vector(self, id: int, vector: np.ndarray, metadata: Dict) -> None:
        segment_id = id // self.segment_size
        segment_path = self.path / f"segment_{segment_id}.bin"
        
        # Compress vector
        compressed_data = zlib.compress(vector.tobytes())
        
        # Write to segment file
        with open(segment_path, 'ab') as f:
            # Write header: id, vector size
            f.write(struct.pack('QI', id, len(compressed_data)))
            # Write data
            f.write(compressed_data)
            f.write(json.dumps(metadata).encode())
        
        # Update segments metadata
        if segment_id not in self.segments:
            self.segments[segment_id] = {
                'start_id': id,
                'count': 0,
                'last_modified': datetime.now().isoformat()
            }
        self.segments[segment_id]['count'] += 1
        self._save_segments()
    
    def get_vector(self, id: int) -> Tuple[np.ndarray, Dict]:
        segment_id = id // self.segment_size
        segment_path = self.path / f"segment_{segment_id}.bin"
        
        if not segment_path.exists():
            raise KeyError(f"Vector {id} not found")
        
        with open(segment_path, 'rb') as f:
            # Read and decompress vector
            header = struct.unpack('QI', f.read(12))
            compressed_data = f.read(header[1])
            vector_data = zlib.decompress(compressed_data)
            vector = np.frombuffer(vector_data, dtype=np.float32)
            
            # Read metadata
            metadata = json.loads(f.read().decode())
            
            return vector, metadata