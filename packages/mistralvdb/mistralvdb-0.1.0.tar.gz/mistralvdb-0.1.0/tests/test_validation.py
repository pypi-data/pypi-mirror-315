"""Tests for validation utilities."""

import pytest
import numpy as np
from mistralvdb.utils.validation import (
    validate_vector,
    validate_batch_vectors,
    validate_metadata,
    validate_search_params,
    validate_index_params
)

def test_validate_vector():
    """Test vector validation."""
    # Valid vector
    valid_vector = np.random.randn(128)
    validate_vector(valid_vector, 128)
    
    # Wrong type
    with pytest.raises(ValueError):
        validate_vector([1, 2, 3], 128)
    
    # Wrong dimensions
    with pytest.raises(ValueError):
        validate_vector(np.random.randn(128, 1), 128)
    
    # Wrong size
    with pytest.raises(ValueError):
        validate_vector(np.random.randn(64), 128)
    
    # Non-finite values
    invalid_vector = np.array([np.inf, 1.0, 2.0])
    with pytest.raises(ValueError):
        validate_vector(invalid_vector, 3)

def test_validate_batch_vectors():
    """Test batch vector validation."""
    # Valid batch
    valid_batch = [np.random.randn(128) for _ in range(5)]
    validate_batch_vectors(valid_batch, 128)
    
    # Empty batch
    with pytest.raises(ValueError):
        validate_batch_vectors([], 128)
    
    # Invalid vector in batch
    invalid_batch = [np.random.randn(128) for _ in range(3)]
    invalid_batch.append(np.random.randn(64))  # Wrong dimension
    with pytest.raises(ValueError):
        validate_batch_vectors(invalid_batch, 128)

def test_validate_metadata():
    """Test metadata validation."""
    # Valid metadata
    valid_metadata = {
        "title": "Document 1",
        "tags": ["tag1", "tag2"],
        "nested": {
            "field1": "value1",
            "field2": 42
        }
    }
    validate_metadata(valid_metadata)
    
    # Invalid type
    with pytest.raises(ValueError):
        validate_metadata([1, 2, 3])
    
    # Invalid key type
    invalid_metadata = {
        "title": "Document 1",
        42: "Invalid key"
    }
    with pytest.raises(ValueError):
        validate_metadata(invalid_metadata)
    
    # Invalid nested metadata
    invalid_nested = {
        "title": "Document 1",
        "nested": {
            42: "Invalid key"
        }
    }
    with pytest.raises(ValueError):
        validate_metadata(invalid_nested)

def test_validate_search_params():
    """Test search parameter validation."""
    # Valid parameters
    validate_search_params(k=5, ef=10)
    
    # Invalid k
    with pytest.raises(ValueError):
        validate_search_params(k=0, ef=10)
    
    with pytest.raises(ValueError):
        validate_search_params(k=-1, ef=10)
    
    # Invalid ef
    with pytest.raises(ValueError):
        validate_search_params(k=5, ef=4)  # ef must be >= k
    
    with pytest.raises(ValueError):
        validate_search_params(k=5, ef=-1)

def test_validate_index_params():
    """Test index parameter validation."""
    # Valid parameters
    validate_index_params(M=16, ef_construction=200)
    
    # Invalid M
    with pytest.raises(ValueError):
        validate_index_params(M=1, ef_construction=200)
    
    with pytest.raises(ValueError):
        validate_index_params(M=-1, ef_construction=200)
    
    # Invalid ef_construction
    with pytest.raises(ValueError):
        validate_index_params(M=16, ef_construction=15)  # Must be >= M
    
    with pytest.raises(ValueError):
        validate_index_params(M=16, ef_construction=-1)
