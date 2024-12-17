"""Enhanced HNSW Index implementation with optimizations."""

import numpy as np
from typing import List, Tuple, Set, Optional, Dict
import heapq
from threading import Lock
import pickle
from .utils.validation import validate_vector
from .utils.compression import compress_vector, decompress_vector

class HNSWNode:
    """Node in the HNSW graph with vector compression support."""
    def __init__(self, id: int, vector: np.ndarray, level: int, compress: bool = True):
        self.id = id
        self._vector = compress_vector(vector) if compress else vector
        self.level = level
        self.neighbors: Dict[int, Set[int]] = {}  # level -> set of neighbor ids
        self.is_compressed = compress

    @property
    def vector(self) -> np.ndarray:
        """Get the vector, decompressing if necessary."""
        if self.is_compressed:
            return decompress_vector(self._vector)
        return self._vector

    def add_neighbor(self, level: int, neighbor_id: int):
        """Add a neighbor at the specified level."""
        if level not in self.neighbors:
            self.neighbors[level] = set()
        self.neighbors[level].add(neighbor_id)

    def get_neighbors(self, level: int) -> Set[int]:
        """Get all neighbors at the specified level."""
        return self.neighbors.get(level, set())

class HNSWIndex:
    """Enhanced HNSW index with vector compression and optimizations."""
    
    def __init__(
        self,
        dim: int,
        M: int = 16,
        ef_construction: int = 200,
        ef: int = 50,
        ml: Optional[int] = None,
        compress_vectors: bool = True
    ):
        """Initialize HNSW index.
        
        Args:
            dim: Dimensionality of vectors
            M: Max number of connections per element (M > 0)
            ef_construction: Size of dynamic candidate list for construction
            ef: Size of dynamic candidate list for search
            ml: Max level, if None will be calculated automatically
            compress_vectors: Whether to use vector compression
        """
        self.dim = dim
        self.M = M
        self.M0 = 2 * M  # Extended number of connections for ground layer
        self.ef_construction = ef_construction
        self.ef = ef
        self.ml = ml or int(np.log2(1_000_000))  # Auto-calculate max level
        self.level_mult = 1/np.log(M)  # Level generation factor
        
        self.nodes: Dict[int, HNSWNode] = {}
        self.entry_point = None
        self.max_level = -1
        self.lock = Lock()
        self.compress_vectors = compress_vectors

    def _distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine distance between vectors."""
        return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _get_random_level(self) -> int:
        """Generate random level using exponential distribution."""
        return int(-np.log(np.random.random()) * self.level_mult)

    def _get_neighbors(
        self,
        q: np.ndarray,
        entry: int,
        ef: int,
        level: int,
        visited: Optional[Set[int]] = None
    ) -> List[Tuple[float, int]]:
        """Find nearest neighbors for a query vector.
        
        Args:
            q: Query vector
            entry: Entry point node ID
            ef: Size of dynamic candidate list
            level: Current level
            visited: Set of visited nodes
        
        Returns:
            List of (distance, node_id) tuples
        """
        if visited is None:
            visited = set()

        # Initialize candidate and result sets
        dist_entry = self._distance(q, self.nodes[entry].vector)
        candidates = [(dist_entry, entry)]
        results = [(dist_entry, entry)]
        visited.add(entry)

        while candidates:
            dist_c, current = heapq.heappop(candidates)
            dist_furthest = results[-1][0] if results else float('inf')

            if dist_c > dist_furthest:
                break

            # Examine neighbors
            for neighbor_id in self.nodes[current].get_neighbors(level):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    dist_neighbor = self._distance(q, self.nodes[neighbor_id].vector)

                    if len(results) < ef or dist_neighbor < results[-1][0]:
                        heapq.heappush(candidates, (dist_neighbor, neighbor_id))
                        heapq.heappush(results, (dist_neighbor, neighbor_id))

                        if len(results) > ef:
                            heapq.heappop(results)

        return sorted(results)  # Sort by distance

    def _select_neighbors(
        self,
        q: np.ndarray,
        candidates: List[Tuple[float, int]],
        M: int,
        level: int,
        extend_candidates: bool = False
    ) -> List[int]:
        """Select best neighbors for a node.
        
        Args:
            q: Query vector
            candidates: List of candidate nodes (distance, id)
            M: Max number of neighbors to return
            level: Current level
            extend_candidates: Whether to extend candidates using their neighbors
        
        Returns:
            List of selected neighbor IDs
        """
        if extend_candidates:
            # Collect neighbors of candidates
            extended = set()
            for _, cand_id in candidates:
                extended.update(self.nodes[cand_id].get_neighbors(level))
            
            # Add to candidates if better
            for e in extended:
                if e not in {c[1] for c in candidates}:
                    dist = self._distance(q, self.nodes[e].vector)
                    candidates.append((dist, e))

        # Sort candidates by distance
        candidates.sort()
        
        # Select best neighbors using heuristic selection
        selected = []
        for _, cand_id in candidates[:M]:
            # Check if adding this candidate improves overall connectivity
            if not selected or all(
                self._distance(
                    self.nodes[cand_id].vector,
                    self.nodes[s].vector
                ) > self._distance(q, self.nodes[cand_id].vector)
                for s in selected
            ):
                selected.append(cand_id)
                if len(selected) >= M:
                    break

        return selected

    def add_items(self, vectors: List[np.ndarray], ids: Optional[List[int]] = None) -> List[int]:
        """Add multiple items to the index.
        
        Args:
            vectors: List of vectors to add
            ids: Optional list of IDs for the vectors
        
        Returns:
            List of assigned IDs
        """
        if ids is None:
            ids = list(range(len(self.nodes), len(self.nodes) + len(vectors)))
        
        with self.lock:
            for vector, id_ in zip(vectors, ids):
                self.add_item(vector, id_)
        
        return ids

    def add_item(self, vector: np.ndarray, id_: Optional[int] = None) -> int:
        """Add a single item to the index.
        
        Args:
            vector: Vector to add
            id_: Optional ID for the vector
        
        Returns:
            Assigned ID
        """
        validate_vector(vector, self.dim)
        
        with self.lock:
            if id_ is None:
                id_ = len(self.nodes)
            elif id_ in self.nodes:
                raise ValueError(f"ID {id_} already exists in the index")

            # Generate random level
            level = min(self._get_random_level(), self.ml)
            
            # Create new node
            node = HNSWNode(id_, vector, level, compress=self.compress_vectors)
            self.nodes[id_] = node
            
            if self.entry_point is None:
                # First node becomes entry point
                self.entry_point = id_
                self.max_level = level
                return id_

            # Find entry point
            curr_obj = self.entry_point
            curr_dist = self._distance(vector, self.nodes[curr_obj].vector)

            # Search through levels
            for lc in range(self.max_level, level, -1):
                changed = True
                while changed:
                    changed = False
                    neighbors = self.nodes[curr_obj].get_neighbors(lc)
                    
                    for neighbor_id in neighbors:
                        dist = self._distance(vector, self.nodes[neighbor_id].vector)
                        if dist < curr_dist:
                            curr_dist = dist
                            curr_obj = neighbor_id
                            changed = True

            # For each level, find neighbors
            for lc in range(min(level, self.max_level), -1, -1):
                # Find nearest neighbors
                candidates = self._get_neighbors(
                    vector,
                    curr_obj,
                    self.ef_construction,
                    lc
                )
                
                # Select neighbors
                neighbors = self._select_neighbors(
                    vector,
                    candidates,
                    self.M if lc > 0 else self.M0,
                    lc,
                    extend_candidates=True
                )
                
                # Add bidirectional connections
                for neighbor_id in neighbors:
                    self.nodes[id_].add_neighbor(lc, neighbor_id)
                    self.nodes[neighbor_id].add_neighbor(lc, id_)

            # Update entry point if needed
            if level > self.max_level:
                self.entry_point = id_
                self.max_level = level

            return id_

    def search(self, vector: np.ndarray, k: int = 4) -> List[Tuple[int, float]]:
        """Search for k nearest neighbors.
        
        Args:
            vector: Query vector
            k: Number of neighbors to return
        
        Returns:
            List of (id, distance) tuples
        """
        validate_vector(vector, self.dim)
        
        with self.lock:
            if not self.nodes:
                return []

            # Find entry point
            curr_obj = self.entry_point
            curr_dist = self._distance(vector, self.nodes[curr_obj].vector)

            # Search through levels
            for level in range(self.max_level, 0, -1):
                changed = True
                while changed:
                    changed = False
                    neighbors = self.nodes[curr_obj].get_neighbors(level)
                    
                    for neighbor_id in neighbors:
                        dist = self._distance(vector, self.nodes[neighbor_id].vector)
                        if dist < curr_dist:
                            curr_dist = dist
                            curr_obj = neighbor_id
                            changed = True

            # Search last level more thoroughly
            candidates = self._get_neighbors(vector, curr_obj, self.ef, 0)
            
            # Return k nearest neighbors
            return [(node_id, dist) for dist, node_id in candidates[:k]]

    def save(self, path: str):
        """Save index to disk."""
        with self.lock:
            with open(path, 'wb') as f:
                pickle.dump({
                    'dim': self.dim,
                    'M': self.M,
                    'ef_construction': self.ef_construction,
                    'ef': self.ef,
                    'ml': self.ml,
                    'nodes': self.nodes,
                    'entry_point': self.entry_point,
                    'max_level': self.max_level,
                    'compress_vectors': self.compress_vectors
                }, f)

    def load(self, path: str):
        """Load index from disk."""
        with self.lock:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.dim = data['dim']
                self.M = data['M']
                self.ef_construction = data['ef_construction']
                self.ef = data['ef']
                self.ml = data['ml']
                self.nodes = data['nodes']
                self.entry_point = data['entry_point']
                self.max_level = data['max_level']
                self.compress_vectors = data['compress_vectors']
                self.M0 = 2 * self.M
                self.level_mult = 1/np.log(self.M)

    def __len__(self) -> int:
        """Get number of items in index."""
        return len(self.nodes)
