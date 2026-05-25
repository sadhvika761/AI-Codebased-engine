from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.llm_client = None
    
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task."""
        pass
    
    def set_llm_client(self, llm_client):
        """Inject LLM client dependency."""
        self.llm_client = llm_client