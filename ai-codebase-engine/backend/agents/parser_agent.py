from .base_agent import BaseAgent
from backend.core.code_parser import CodeParser
from typing import Dict, Any

class ParserAgent(BaseAgent):
    """Agent responsible for parsing code repositories."""
    
    def __init__(self):
        super().__init__("ParserAgent")
        self.parser = CodeParser()
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Parse repository and extract code entities."""
        repo_path = task.get('repo_path')
        
        if not repo_path:
            return {"error": "No repository path provided"}
        
        from pathlib import Path
        path = Path(repo_path)
        if not path.exists():
            return {"error": f"Repository path does not exist: {repo_path}"}
        
        try:
            entities = self.parser.parse_repository(path)
            return {
                "status": "success",
                "entities": [self._entity_to_dict(e) for e in entities],
                "total_entities": len(entities)
            }
        except Exception as e:
            return {"error": f"Parsing failed: {str(e)}", "entities": []}
    
    
    def _entity_to_dict(self, entity) -> Dict:
        """Convert CodeEntity to dictionary."""
        return {
            "name": entity.name,
            "type": entity.type,
            "file_path": entity.file_path,
            "line_start": entity.line_start,
            "line_end": entity.line_end,
            "docstring": entity.docstring,
            "parameters": entity.parameters or [],
            "dependencies": entity.dependencies or []
        }