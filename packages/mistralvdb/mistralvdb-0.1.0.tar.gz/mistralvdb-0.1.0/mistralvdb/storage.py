"""Storage management for MistralVDB."""

import os
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

class StorageManager:
    """Manages storage locations and persistence for MistralVDB."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize storage manager.
        
        Args:
            base_dir: Optional base directory for storage. If None, uses .mistralvdb
                     in the current working directory.
        """
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), '.mistralvdb')
        
        self.base_dir = Path(base_dir)
        self.embeddings_dir = self.base_dir / 'embeddings'
        self.indices_dir = self.base_dir / 'indices'
        self.metadata_file = self.base_dir / 'metadata.json'
        
        # Create directories if they don't exist
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        self.indices_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load metadata
        if not self.metadata_file.exists():
            self._save_metadata({})
    
    def get_embedding_path(self, collection_name: str) -> Path:
        """Get path for storing embeddings of a collection."""
        return self.embeddings_dir / f"{collection_name}_embeddings.pkl"
    
    def get_index_path(self, collection_name: str) -> Path:
        """Get path for storing HNSW index of a collection."""
        return self.indices_dir / f"{collection_name}_index.pkl"
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """Save metadata to disk."""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from disk."""
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
    
    def update_collection_metadata(self, collection_name: str, metadata: Dict[str, Any]):
        """Update metadata for a collection."""
        all_metadata = self._load_metadata()
        all_metadata[collection_name] = metadata
        self._save_metadata(all_metadata)
    
    def get_collection_metadata(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a collection."""
        all_metadata = self._load_metadata()
        return all_metadata.get(collection_name)
    
    def list_collections(self) -> Dict[str, Dict[str, Any]]:
        """List all collections and their metadata."""
        return self._load_metadata()
    
    def delete_collection(self, collection_name: str):
        """Delete a collection and its associated files."""
        # Remove files
        embedding_path = self.get_embedding_path(collection_name)
        index_path = self.get_index_path(collection_name)
        
        if embedding_path.exists():
            embedding_path.unlink()
        if index_path.exists():
            index_path.unlink()
        
        # Remove from metadata
        metadata = self._load_metadata()
        if collection_name in metadata:
            del metadata[collection_name]
            self._save_metadata(metadata)
    
    def clear_storage(self):
        """Clear all storage (use with caution)."""
        shutil.rmtree(self.base_dir)
        self.__init__(str(self.base_dir))  # Reinitialize storage
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Get information about storage usage."""
        def get_dir_size(path: Path) -> int:
            return sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
        
        return {
            'total_collections': len(self._load_metadata()),
            'embeddings_size': get_dir_size(self.embeddings_dir),
            'indices_size': get_dir_size(self.indices_dir),
            'base_directory': str(self.base_dir)
        }
