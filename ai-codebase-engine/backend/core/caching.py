from functools import lru_cache
import hashlib
import json
from typing import Any

class QueryCache:
    """Cache for expensive operations."""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Any:
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        self.cache[key] = value
    
    @staticmethod
    def make_key(*args, **kwargs) -> str:
        """Generate cache key from arguments."""
        data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(data.encode()).hexdigest()

# Global cache instance
query_cache = QueryCache()

def cached_graph_query(func):
    """Decorator for caching graph queries."""
    def wrapper(*args, **kwargs):
        cache_key = QueryCache.make_key(*args, **kwargs)
        
        result = query_cache.get(cache_key)
        if result is not None:
            return result
        
        result = func(*args, **kwargs)
        query_cache.set(cache_key, result)
        return result
    
    return wrapper