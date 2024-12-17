"""Vector compression utilities using Product Quantization."""

import numpy as np
from typing import Tuple
import pickle

class ProductQuantizer:
    """Product Quantizer for vector compression."""
    
    def __init__(self, dim: int, n_subvectors: int = 8, n_clusters: int = 256):
        """Initialize Product Quantizer.
        
        Args:
            dim: Vector dimensionality
            n_subvectors: Number of subvectors to split vectors into
            n_clusters: Number of clusters for each subvector (usually 256 for uint8)
        """
        if dim % n_subvectors != 0:
            raise ValueError(f"Dimension {dim} must be divisible by n_subvectors {n_subvectors}")
        
        self.dim = dim
        self.n_subvectors = n_subvectors
        self.n_clusters = n_clusters
        self.subvector_dim = dim // n_subvectors
        self.codebooks = None
        self.is_trained = False

    def train(self, vectors: np.ndarray):
        """Train the quantizer on a set of vectors.
        
        Args:
            vectors: Training vectors of shape (n_vectors, dim)
        """
        from sklearn.cluster import KMeans
        
        # Reshape into subvectors
        subvectors = vectors.reshape(-1, self.n_subvectors, self.subvector_dim)
        
        # Initialize codebooks
        self.codebooks = []
        
        # Train each subquantizer
        for i in range(self.n_subvectors):
            kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
            kmeans.fit(subvectors[:, i, :])
            self.codebooks.append(kmeans.cluster_centers_)
        
        self.codebooks = np.array(self.codebooks)
        self.is_trained = True

    def encode(self, vector: np.ndarray) -> np.ndarray:
        """Encode a vector into its compressed form.
        
        Args:
            vector: Vector to compress
        
        Returns:
            Compressed vector as uint8 codes
        """
        if not self.is_trained:
            raise RuntimeError("Quantizer must be trained before encoding")
        
        # Reshape into subvectors
        subvectors = vector.reshape(self.n_subvectors, self.subvector_dim)
        
        # Encode each subvector
        codes = np.zeros(self.n_subvectors, dtype=np.uint8)
        for i in range(self.n_subvectors):
            distances = np.linalg.norm(
                subvectors[i] - self.codebooks[i],
                axis=1
            )
            codes[i] = np.argmin(distances)
        
        return codes

    def decode(self, codes: np.ndarray) -> np.ndarray:
        """Decode compressed codes back into a vector.
        
        Args:
            codes: Compressed vector codes
        
        Returns:
            Reconstructed vector
        """
        if not self.is_trained:
            raise RuntimeError("Quantizer must be trained before decoding")
        
        # Reconstruct vector from codes
        vector = np.zeros(self.dim)
        for i in range(self.n_subvectors):
            start = i * self.subvector_dim
            end = start + self.subvector_dim
            vector[start:end] = self.codebooks[i][codes[i]]
        
        return vector

    def save(self, path: str):
        """Save quantizer to disk."""
        with open(path, 'wb') as f:
            pickle.dump({
                'dim': self.dim,
                'n_subvectors': self.n_subvectors,
                'n_clusters': self.n_clusters,
                'codebooks': self.codebooks,
                'is_trained': self.is_trained
            }, f)

    def load(self, path: str):
        """Load quantizer from disk."""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.dim = data['dim']
            self.n_subvectors = data['n_subvectors']
            self.n_clusters = data['n_clusters']
            self.subvector_dim = self.dim // self.n_subvectors
            self.codebooks = data['codebooks']
            self.is_trained = data['is_trained']

# Global quantizer instance
_quantizer = None

def init_compression(vectors: np.ndarray):
    """Initialize vector compression with training data.
    
    Args:
        vectors: Training vectors for the quantizer
    """
    global _quantizer
    _quantizer = ProductQuantizer(vectors.shape[1])
    _quantizer.train(vectors)

def compress_vector(vector: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compress a vector using product quantization.
    
    Args:
        vector: Vector to compress
    
    Returns:
        Tuple of (compressed_codes, original_norm)
    """
    if _quantizer is None:
        raise RuntimeError("Must call init_compression before compressing vectors")
    
    # Store original norm for cosine similarity
    original_norm = np.linalg.norm(vector)
    
    # Normalize vector before compression
    normalized = vector / original_norm
    
    # Compress normalized vector
    codes = _quantizer.encode(normalized)
    
    return codes, original_norm

def decompress_vector(compressed: Tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    """Decompress a vector from its compressed form.
    
    Args:
        compressed: Tuple of (compressed_codes, original_norm)
    
    Returns:
        Reconstructed vector
    """
    if _quantizer is None:
        raise RuntimeError("Must call init_compression before decompressing vectors")
    
    codes, original_norm = compressed
    
    # Decode normalized vector
    normalized = _quantizer.decode(codes)
    
    # Restore original magnitude
    return normalized * original_norm
