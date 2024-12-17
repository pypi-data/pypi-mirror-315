"""Tests for HNSW index implementation."""

import pytest
import numpy as np
from mistralvdb.index import HNSWIndex

@pytest.fixture
def sample_vectors():
    """Generate sample vectors for testing."""
    np.random.seed(42)
    return np.random.randn(100, 128)

def test_index_initialization():
    """Test index initialization with various parameters."""
    index = HNSWIndex(dim=128)
    assert index.dim == 128
    assert index.M == 16  # default value
    assert index.entry_point is None
    assert len(index.nodes) == 0

def test_add_single_item(sample_vectors):
    """Test adding a single item to the index."""
    index = HNSWIndex(dim=128)
    vector = sample_vectors[0]
    id_ = index.add_item(vector)
    
    assert id_ == 0
    assert len(index.nodes) == 1
    assert index.entry_point == 0

def test_add_multiple_items(sample_vectors):
    """Test adding multiple items to the index."""
    index = HNSWIndex(dim=128)
    ids = index.add_items(sample_vectors[:10])
    
    assert len(ids) == 10
    assert len(index.nodes) == 10
    assert index.entry_point is not None

def test_search(sample_vectors):
    """Test nearest neighbor search."""
    index = HNSWIndex(dim=128)
    index.add_items(sample_vectors)
    
    # Search with a query vector
    query = sample_vectors[0]
    results = index.search(query, k=5)
    
    assert len(results) == 5
    # First result should be the query vector itself
    assert results[0][0] == 0
    assert results[0][1] < 1e-10  # Distance should be very small

def test_invalid_vector():
    """Test handling of invalid vectors."""
    index = HNSWIndex(dim=128)
    
    with pytest.raises(ValueError):
        # Wrong dimension
        index.add_item(np.random.randn(64))
    
    with pytest.raises(ValueError):
        # Wrong shape
        index.add_item(np.random.randn(128, 1))

def test_duplicate_id():
    """Test handling of duplicate IDs."""
    index = HNSWIndex(dim=128)
    vector = np.random.randn(128)
    
    # Add first vector
    id_ = index.add_item(vector, id_=42)
    assert id_ == 42
    
    # Try to add second vector with same ID
    with pytest.raises(ValueError):
        index.add_item(vector, id_=42)

def test_save_load(tmp_path, sample_vectors):
    """Test saving and loading the index."""
    index = HNSWIndex(dim=128)
    index.add_items(sample_vectors[:10])
    
    # Save index
    save_path = tmp_path / "index.pkl"
    index.save(str(save_path))
    
    # Load into new index
    new_index = HNSWIndex(dim=128)
    new_index.load(str(save_path))
    
    # Check if indices are equivalent
    assert len(new_index.nodes) == len(index.nodes)
    assert new_index.entry_point == index.entry_point
    
    # Check if search results are the same
    query = sample_vectors[0]
    results1 = index.search(query, k=5)
    results2 = new_index.search(query, k=5)
    
    assert len(results1) == len(results2)
    for (id1, dist1), (id2, dist2) in zip(results1, results2):
        assert id1 == id2
        assert abs(dist1 - dist2) < 1e-10

def test_vector_compression(sample_vectors):
    """Test index with vector compression enabled."""
    # Create index with compression
    compressed_index = HNSWIndex(dim=128, compress_vectors=True)
    compressed_index.add_items(sample_vectors[:10])
    
    # Create index without compression
    uncompressed_index = HNSWIndex(dim=128, compress_vectors=False)
    uncompressed_index.add_items(sample_vectors[:10])
    
    # Compare search results
    query = sample_vectors[0]
    results1 = compressed_index.search(query, k=5)
    results2 = uncompressed_index.search(query, k=5)
    
    # Results should be similar but not identical due to compression
    for (id1, dist1), (id2, dist2) in zip(results1, results2):
        assert abs(dist1 - dist2) < 0.1  # Allow some difference due to compression

def test_concurrent_access(sample_vectors):
    """Test concurrent access to the index."""
    import threading
    import queue
    
    index = HNSWIndex(dim=128)
    errors = queue.Queue()
    
    def add_vectors(start_idx):
        try:
            index.add_items(sample_vectors[start_idx:start_idx+10])
        except Exception as e:
            errors.put(e)
    
    # Create threads
    threads = []
    for i in range(0, 50, 10):
        thread = threading.Thread(target=add_vectors, args=(i,))
        threads.append(thread)
    
    # Start threads
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    # Check for errors
    assert errors.empty()
    assert len(index.nodes) == 50

def test_large_batch_search(sample_vectors):
    """Test search performance with larger batches."""
    index = HNSWIndex(dim=128, ef=100)  # Increase ef for better recall
    index.add_items(sample_vectors)
    
    # Perform multiple searches
    queries = sample_vectors[:10]
    for query in queries:
        results = index.search(query, k=10)
        assert len(results) == 10
        
        # Check distances are monotonically increasing
        distances = [dist for _, dist in results]
        assert all(distances[i] <= distances[i+1] for i in range(len(distances)-1))
