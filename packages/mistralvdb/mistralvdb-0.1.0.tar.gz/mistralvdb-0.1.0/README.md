# MistralVDB

A vector database optimized for Mistral AI embeddings with HNSW indexing. Features include:
- Efficient similarity search using HNSW indexing
- Vector compression for reduced memory usage
- Built-in REST API server
- Secure authentication
- Multiple collection support
- Automatic persistence

## Installation

```bash
pip install mistralvdb
```

## Quick Start

### As a Python Library

```python
from mistralvdb import MistralVDB

# Initialize database
db = MistralVDB(
    api_key="your-mistral-api-key",
    collection_name="my_collection"
)

# Add documents
texts = [
    "The quick brown fox jumps over the lazy dog",
    "Python is a versatile programming language"
]
metadata = [
    {"type": "example"},
    {"type": "programming"}
]
ids = db.add_texts(texts, metadata=metadata)

# Search
results = db.search("programming language", k=4)
for doc_id, score in results:
    print(f"Score: {score}")
    print(f"Text: {db.get_text(doc_id)}")
    print(f"Metadata: {db.get_metadata(doc_id)}\n")
```

### As an API Server

1. Start the server:
```bash
# Set your API key
export MISTRAL_API_KEY=your-mistral-api-key

# Start server
mistralvdb-server --host 127.0.0.1 --port 8000
```

2. Use the client:
```python
from mistralvdb.client import MistralVDBClient

# Create client
client = MistralVDBClient()

# Login (default credentials)
client.login(username="admin", password="admin-password")

# Add documents
docs = ["Document 1", "Document 2"]
client.add_documents(docs, collection_name="my_collection")

# Search
results = client.search("my query", collection_name="my_collection")
```

## Features

### HNSW Indexing
- Efficient approximate nearest neighbor search
- Configurable index parameters (M, ef_construction, ef)
- Thread-safe operations

### Vector Compression
- Product Quantization for reduced memory usage
- Configurable compression parameters
- Minimal accuracy loss

### API Server
- RESTful API with FastAPI
- JWT authentication
- Collection management
- Swagger UI documentation

### Storage Management
- Automatic persistence
- Multiple collections
- Custom storage location
- Collection metadata

## Configuration

### Environment Variables
- `MISTRAL_API_KEY`: Your Mistral AI API key (required)

### Server Options
```bash
mistralvdb-server --help
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mistralvdb.git
cd mistralvdb
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
