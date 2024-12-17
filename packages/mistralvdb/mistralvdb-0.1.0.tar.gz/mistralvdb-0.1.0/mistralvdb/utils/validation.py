"""Validation utilities for vector operations."""

import numpy as np
from typing import Any, Dict, List

def validate_vector(vector: np.ndarray, expected_dim: int):
    """Validate a vector's format and dimensions.
    
    Args:
        vector: Vector to validate
        expected_dim: Expected dimensionality
    
    Raises:
        ValueError: If vector is invalid
    """
    if not isinstance(vector, np.ndarray):
        raise ValueError(f"Vector must be a numpy array, got {type(vector)}")
    
    if vector.ndim != 1:
        raise ValueError(f"Vector must be 1-dimensional, got {vector.ndim} dimensions")
    
    if vector.shape[0] != expected_dim:
        raise ValueError(f"Vector must have dimension {expected_dim}, got {vector.shape[0]}")
    
    if not np.isfinite(vector).all():
        raise ValueError("Vector contains non-finite values")

def validate_batch_vectors(vectors: List[np.ndarray], expected_dim: int):
    """Validate a batch of vectors.
    
    Args:
        vectors: List of vectors to validate
        expected_dim: Expected dimensionality
    
    Raises:
        ValueError: If any vector is invalid
    """
    if not vectors:
        raise ValueError("Vector list cannot be empty")
    
    for i, vector in enumerate(vectors):
        try:
            validate_vector(vector, expected_dim)
        except ValueError as e:
            raise ValueError(f"Invalid vector at index {i}: {str(e)}")

def validate_metadata(metadata: Dict[str, Any]):
    """Validate metadata format.
    
    Args:
        metadata: Metadata dictionary to validate
    
    Raises:
        ValueError: If metadata is invalid
    """
    if not isinstance(metadata, dict):
        raise ValueError(f"Metadata must be a dictionary, got {type(metadata)}")
    
    # Validate that all keys are strings
    for key in metadata:
        if not isinstance(key, str):
            raise ValueError(f"Metadata keys must be strings, got {type(key)}")
        
        # Check for nested dictionaries
        if isinstance(metadata[key], dict):
            validate_metadata(metadata[key])

def validate_search_params(k: int, ef: int):
    """Validate search parameters.
    
    Args:
        k: Number of results to return
        ef: Size of dynamic candidate list
    
    Raises:
        ValueError: If parameters are invalid
    """
    if not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be a positive integer, got {k}")
    
    if not isinstance(ef, int) or ef < k:
        raise ValueError(f"ef must be an integer >= k, got {ef}")

def validate_index_params(M: int, ef_construction: int):
    """Validate HNSW index parameters.
    
    Args:
        M: Max number of connections
        ef_construction: Size of dynamic candidate list for construction
    
    Raises:
        ValueError: If parameters are invalid
    """
    if not isinstance(M, int) or M < 2:
        raise ValueError(f"M must be an integer >= 2, got {M}")
    
    if not isinstance(ef_construction, int) or ef_construction < M:
        raise ValueError(f"ef_construction must be an integer >= M, got {ef_construction}")
