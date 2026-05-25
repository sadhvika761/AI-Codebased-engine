import chromadb
from chromadb.config import Settings
from typing import List, Dict
from pathlib import Path
import hashlib

class EmbeddingEngine:
    """Manages code embeddings and vector search."""
    
    def __init__(self, persist_directory: str = "data/embeddings"):
        self.client = chromadb.PersistentClient(path=persist_directory)
    
    def create_collection(self, repo_id: str) -> chromadb.Collection:
        """Create or get collection for repository."""
        collection_name = f"repo_{repo_id}"
        
        # Delete if exists
        try:
            self.client.delete_collection(collection_name)
        except:
            pass
        
        return self.client.create_collection(
            name=collection_name,
            metadata={"repo_id": repo_id}
        )
    
    def embed_repository(self, repo_id: str, entities: List[Dict]):
        """Embed all code entities from repository."""
        collection = self.create_collection(repo_id)
        
        documents = []
        metadatas = []
        ids = []
        
        for entity in entities:
            # Create searchable document
            doc = self._entity_to_document(entity)
            documents.append(doc)
            
            # Metadata for filtering
            metadatas.append({
                "type": entity.get("type", "unknown"),
                "file_path": entity.get("file_path", ""),
                "name": entity.get("name", "")
            })
            
            # Unique ID
            ids.append(self._generate_id(entity))
        
        # Batch add to ChromaDB
        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
    
    def search(self, repo_id: str, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant code entities."""
        collection_name = f"repo_{repo_id}"
        
        try:
            collection = self.client.get_collection(collection_name)
        except:
            return []
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return self._format_results(results)
    
    def _entity_to_document(self, entity: Dict) -> str:
        """Convert code entity to searchable text."""
        parts = [
            f"Name: {entity.get('name', '')}",
            f"Type: {entity.get('type', '')}",
            f"File: {entity.get('file_path', '')}",
        ]
        
        if entity.get('docstring'):
            parts.append(f"Documentation: {entity['docstring']}")
        
        if entity.get('parameters'):
            parts.append(f"Parameters: {', '.join(entity['parameters'])}")
        
        if entity.get('dependencies'):
            parts.append(f"Uses: {', '.join(entity['dependencies'])}")
        
        return "\n".join(parts)
    
    def _generate_id(self, entity: Dict) -> str:
        """Generate unique ID for entity."""
        unique_str = f"{entity.get('file_path', '')}:{entity.get('name', '')}:{entity.get('line_start', 0)}"
        return hashlib.md5(unique_str.encode()).hexdigest()
    
    def _format_results(self, results: Dict) -> List[Dict]:
        """Format ChromaDB results."""
        formatted = []
        
        if not results['documents']:
            return formatted
        
        for i, doc in enumerate(results['documents'][0]):
            formatted.append({
                "document": doc,
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted