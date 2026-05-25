from .base_agent import BaseAgent
from typing import Dict, Any, List
import re

class SecurityAgent(BaseAgent):
    """Agent for detecting security vulnerabilities."""
    
    SECURITY_PATTERNS = {
        'hardcoded_secret': [
            r'password\s*=\s*["\'].*["\']',
            r'api_key\s*=\s*["\'].*["\']',
            r'secret\s*=\s*["\'].*["\']',
            r'token\s*=\s*["\'].*["\']'
        ],
        'sql_injection': [
            r'execute\s*\(\s*["\'].*\+.*["\']',
            r'query\s*\(\s*f["\'].*{.*}.*["\']'
        ],
        'command_injection': [
            r'os\.system\s*\(',
            r'subprocess\.call\s*\(',
            r'eval\s*\('
        ]
    }
    
    def __init__(self):
        super().__init__("SecurityAgent")
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Scan code for security issues."""
        entities = task.get('entities', [])
        issues = []
        
        for entity in entities:
            file_path = entity.get('file_path')
            
            if file_path:
                file_issues = self._scan_file(file_path)
                issues.extend(file_issues)
        
        return {
            "status": "success",
            "issues": issues,
            "total_issues": len(issues)
        }
    
    def _scan_file(self, file_path: str) -> List[Dict]:
        """Scan single file for security issues."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            for issue_type, patterns in self.SECURITY_PATTERNS.items():
                for pattern in patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            issues.append({
                                "type": issue_type,
                                "file": file_path,
                                "line": line_num,
                                "code": line.strip(),
                                "severity": self._get_severity(issue_type)
                            })
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return issues
    
    def _get_severity(self, issue_type: str) -> str:
        """Determine severity level."""
        if issue_type in ['sql_injection', 'command_injection']:
            return "CRITICAL"
        elif issue_type == 'hardcoded_secret':
            return "HIGH"
        return "MEDIUM"