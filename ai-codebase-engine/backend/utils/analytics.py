import time
from functools import wraps
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor system performance."""
    
    def __init__(self):
        self.metrics = {
            'total_repos_analyzed': 0,
            'total_queries': 0,
            'avg_parse_time': 0,
            'avg_query_time': 0
        }
    
    def record_repo_analysis(self, duration: float):
        self.metrics['total_repos_analyzed'] += 1
        self.metrics['avg_parse_time'] = (
            (self.metrics['avg_parse_time'] * (self.metrics['total_repos_analyzed'] - 1) + duration)
            / self.metrics['total_repos_analyzed']
        )
    
    def record_query(self, duration: float):
        self.metrics['total_queries'] += 1
        self.metrics['avg_query_time'] = (
            (self.metrics['avg_query_time'] * (self.metrics['total_queries'] - 1) + duration)
            / self.metrics['total_queries']
        )
    
    def get_metrics(self) -> Dict:
        return self.metrics

monitor = PerformanceMonitor()

def track_performance(operation: str):
    """Decorator to track operation performance."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                logger.info(f"{operation} completed in {duration:.2f}s")
                
                if operation == 'parse_repository':
                    monitor.record_repo_analysis(duration)
                elif operation == 'query':
                    monitor.record_query(duration)
        
        return wrapper
    return decorator