"""Tests for vector compression utilities."""

import pytest
import numpy as np
from mistralvdb.utils.compression import (
    ProductQuantizer,
    init_compression,
    compress_vector,
    decompress_vector
)

@pytest.fixture
def sample_vectors():
    """Generate sample vectors for testing."""
    np.random.seed(42)
    return np.random.randn(100, 128)

def test_product_quantizer_initialization():
    """Test Product Quantizer initialization."""
    pq = ProductQuantizer(dim=128, n_subvectors=8)
    assert pq.dim == 128
    assert pq.n_subvectors == 8
    assert pq.subvector_dim == 16
    assert not pq.is_trained

def test_invalid_dimensions():
    """Test handling of invalid dimensions."""
    with pytest.raises(ValueError):
        # Dimension not divisible by n_subvectors
        ProductQuantizer(dim=100, n_subvectors=8)

def test_quantizer_training(sample_vectors):
    """Test quantizer training."""
    pq = ProductQuantizer(dim=128)
    pq.train(sample_vectors)
    
    assert pq.is_trained
    assert pq.codebooks is not None
    assert pq.codebooks.shape == (8, 256, 16)  # (n_subvectors, n_clusters, subvector_dim)

def test_vector_encoding_decoding(sample_vectors):
    """Test vector encoding and decoding."""
    pq = ProductQuantizer(dim=128)
    pq.train(sample_vectors)
    
    # Test single vector
    vector = sample_vectors[0]
    codes = pq.encode(vector)
    reconstructed = pq.decode(codes)
    
    assert codes.shape == (8,)  # n_subvectors
    assert reconstructed.shape == (128,)  # original dimension
    
    # Reconstruction error should be reasonable
    error = np.mean((vector - reconstructed) ** 2)
    assert error < 0.1

def test_compression_pipeline(sample_vectors):
    """Test the complete compression pipeline."""
    # Initialize compression
    init_compression(sample_vectors)
    
    # Test compression and decompression
    vector = sample_vectors[0]
    compressed = compress_vector(vector)
    reconstructed = decompress_vector(compressed)
    
    assert isinstance(compressed, tuple)
    assert len(compressed) == 2
    assert isinstance(compressed[0], np.ndarray)  # codes
    assert isinstance(compressed[1], float)  # norm
    
    # Check reconstruction quality
    cosine_sim = np.dot(vector, reconstructed) / (
        np.linalg.norm(vector) * np.linalg.norm(reconstructed)
    )
    assert cosine_sim > 0.9  # High cosine similarity

def test_compression_without_initialization():
    """Test compression without initialization."""
    vector = np.random.randn(128)
    
    with pytest.raises(RuntimeError):
        compress_vector(vector)
    
    with pytest.raises(RuntimeError):
        decompress_vector((np.zeros(8), 1.0))

def test_save_load_quantizer(tmp_path, sample_vectors):
    """Test saving and loading the quantizer."""
    pq = ProductQuantizer(dim=128)
    pq.train(sample_vectors)
    
    # Save quantizer
    save_path = tmp_path / "quantizer.pkl"
    pq.save(str(save_path))
    
    # Load into new quantizer
    new_pq = ProductQuantizer(dim=128)
    new_pq.load(str(save_path))
    
    assert new_pq.is_trained
    assert np.array_equal(new_pq.codebooks, pq.codebooks)
    
    # Test encoding/decoding with loaded quantizer
    vector = sample_vectors[0]
    codes1 = pq.encode(vector)
    codes2 = new_pq.encode(vector)
    assert np.array_equal(codes1, codes2)

def test_compression_batch(sample_vectors):
    """Test compression with batch of vectors."""
    init_compression(sample_vectors)
    
    # Compress multiple vectors
    compressed_vectors = []
    for vector in sample_vectors[:10]:
        compressed = compress_vector(vector)
        compressed_vectors.append(compressed)
    
    # Decompress and check quality
    for original, compressed in zip(sample_vectors[:10], compressed_vectors):
        reconstructed = decompress_vector(compressed)
        
        # Check shape
        assert reconstructed.shape == original.shape
        
        # Check norm preservation
        assert abs(np.linalg.norm(original) - np.linalg.norm(reconstructed)) < 1e-5
        
        # Check cosine similarity
        cosine_sim = np.dot(original, reconstructed) / (
            np.linalg.norm(original) * np.linalg.norm(reconstructed)
        )
        assert cosine_sim > 0.9

def test_compression_memory_efficiency(sample_vectors):
    """Test memory efficiency of compression."""
    vector = sample_vectors[0]
    
    # Initialize compression
    init_compression(sample_vectors)
    
    # Get original size
    original_size = vector.nbytes
    
    # Get compressed size
    compressed = compress_vector(vector)
    compressed_size = compressed[0].nbytes + 8  # codes + float for norm
    
    # Compression should reduce size significantly
    assert compressed_size < original_size / 4  # At least 75% reduction

def test_compression_edge_cases():
    """Test compression with edge cases."""
    # Initialize with small vectors
    small_vectors = np.random.randn(10, 32)
    init_compression(small_vectors)
    
    # Test zero vector
    zero_vector = np.zeros(32)
    compressed = compress_vector(zero_vector)
    reconstructed = decompress_vector(compressed)
    assert np.allclose(reconstructed, zero_vector)
    
    # Test unit vector
    unit_vector = np.ones(32) / np.sqrt(32)
    compressed = compress_vector(unit_vector)
    reconstructed = decompress_vector(compressed)
    assert abs(np.linalg.norm(reconstructed) - 1.0) < 1e-5
