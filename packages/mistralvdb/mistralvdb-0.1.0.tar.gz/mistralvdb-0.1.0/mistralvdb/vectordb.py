"""Main VectorDB implementation."""

from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import json
import pickle
from pathlib import Path
from threading import Lock
from .embeddings import EmbeddingManager
from .index import HNSWIndex
from .storage import StorageManager

class MistralVDB:
    """Vector database optimized for Mistral AI embeddings."""

    def __init__(
        self,
        api_key: str,
        collection_name: str = "default",
        storage_dir: Optional[str] = None,
        dimension: int = 1024,
        M: int = 16,
        ef_construction: int = 200,
        ef: int = 50,
    ):
        """Initialize MistralVDB.
        
        Args:
            api_key: Mistral AI API key
            collection_name: Name of the collection (default: "default")
            storage_dir: Optional custom storage directory. If None, uses .mistralvdb
                        in the current working directory
            dimension: Embedding dimension (default: 1024 for Mistral embeddings)
            M: Number of connections per element in HNSW graph
            ef_construction: Size of dynamic candidate list for construction
            ef: Size of dynamic candidate list for search
        """
        self.embedding_manager = EmbeddingManager(api_key)
        self.index = HNSWIndex(dimension, M, ef_construction, ef)
        self.metadata: Dict[int, Dict] = {}
        self.texts: Dict[int, str] = {}
        self.next_id = 0
        self.lock = Lock()
        self.collection_name = collection_name
        
        # Initialize storage
        self.storage = StorageManager(storage_dir)
        
        # Load existing data if available
        self._load_collection()

    def _load_collection(self):
        """Load collection data from storage if it exists."""
        embedding_path = self.storage.get_embedding_path(self.collection_name)
        index_path = self.storage.get_index_path(self.collection_name)
        
        if embedding_path.exists() and index_path.exists():
            # Load embeddings and metadata
            with open(embedding_path, 'rb') as f:
                data = pickle.load(f)
                self.texts = data["texts"]
                self.metadata = data["metadata"]
                self.next_id = data["next_id"]
            
            # Load index
            self.index.load(str(index_path))

    def _save_collection(self):
        """Save collection data to storage."""
        # Save embeddings and metadata
        data = {
            "next_id": self.next_id,
            "texts": self.texts,
            "metadata": self.metadata
        }
        
        with open(self.storage.get_embedding_path(self.collection_name), 'wb') as f:
            pickle.dump(data, f)
        
        # Save index
        self.index.save(str(self.storage.get_index_path(self.collection_name)))
        
        # Update collection metadata
        self.storage.update_collection_metadata(
            self.collection_name,
            {
                "document_count": len(self.texts),
                "last_modified": str(Path(self.storage.get_embedding_path(self.collection_name)).stat().st_mtime)
            }
        )

    def add_texts(
        self,
        texts: List[str],
        metadata: Optional[List[Dict]] = None
    ) -> List[int]:
        """Add texts to the database.
        
        Args:
            texts: List of texts to add
            metadata: Optional metadata for each text
        
        Returns:
            List of assigned IDs
        """
        embeddings = self.embedding_manager.get_batch_embeddings(texts)
        valid_embeddings = []
        valid_texts = []
        valid_metadata = []
        ids = []

        with self.lock:
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                if embedding is not None:
                    doc_id = self.next_id
                    self.next_id += 1
                    
                    valid_embeddings.append(embedding)
                    valid_texts.append(text)
                    if metadata:
                        valid_metadata.append(metadata[i])
                    ids.append(doc_id)

            if valid_embeddings:
                self.index.add_items(valid_embeddings, ids)
                
                for i, doc_id in enumerate(ids):
                    self.texts[doc_id] = valid_texts[i]
                    if metadata:
                        self.metadata[doc_id] = valid_metadata[i]

            # Save to storage
            self._save_collection()

        return ids

    def search(
        self,
        query: str,
        k: int = 4,
        filter_fn: Optional[callable] = None
    ) -> List[Tuple[int, float]]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_fn: Optional function to filter results based on metadata
        
        Returns:
            List of (doc_id, similarity_score) tuples
        """
        query_embedding = self.embedding_manager.get_embedding(query)
        if query_embedding is None:
            return []

        with self.lock:
            results = self.index.search(query_embedding, k=k)
            
            if filter_fn:
                filtered_results = []
                for doc_id, score in results:
                    if doc_id in self.metadata and filter_fn(self.metadata[doc_id]):
                        filtered_results.append((doc_id, score))
                return filtered_results[:k]
            
            return results

    def get_text(self, doc_id: int) -> Optional[str]:
        """Get the text for a document ID."""
        return self.texts.get(doc_id)

    def get_metadata(self, doc_id: int) -> Optional[Dict]:
        """Get the metadata for a document ID."""
        return self.metadata.get(doc_id)

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the current collection."""
        return self.storage.get_collection_metadata(self.collection_name)

    def list_collections(self) -> Dict[str, Dict[str, Any]]:
        """List all collections in storage."""
        return self.storage.list_collections()

    def delete_collection(self):
        """Delete the current collection."""
        with self.lock:
            self.storage.delete_collection(self.collection_name)
            self.__init__(
                self.embedding_manager.api_key,
                self.collection_name,
                str(self.storage.base_dir)
            )

    def __len__(self) -> int:
        """Get the number of documents in the database."""
        return len(self.texts)
