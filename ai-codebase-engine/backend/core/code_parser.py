import ast
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class CodeEntity:
    """Represents a code entity (function, class, variable)."""
    name: str
    type: str  # 'function', 'class', 'variable', 'import'
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    complexity: int = 0

class CodeParser:
    """Parse code in multiple languages using AST."""
    
    SUPPORTED_LANGUAGES = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.go': 'go',
    }
    
    def __init__(self):
        self.parsers = {}
        self._init_parsers()
    
    def _init_parsers(self):
        """Initialize language-specific parsers."""
        # For Python, we'll use ast (built-in)
        # For others, you'd use tree-sitter
        pass
    
    def parse_repository(self, repo_path: Path) -> List[CodeEntity]:
        """Parse entire repository."""
        entities = []
        
        for file_path in self._get_code_files(repo_path):
            try:
                file_entities = self.parse_file(file_path)
                entities.extend(file_entities)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
        
        return entities
    
    def parse_file(self, file_path: Path) -> List[CodeEntity]:
        """Parse single file based on extension."""
        ext = file_path.suffix
        
        if ext == '.py':
            return self._parse_python(file_path)
        elif ext in ['.js', '.ts']:
            return self._parse_javascript(file_path)
        # Add more languages as needed
        
        return []
    
    def _parse_python(self, file_path: Path) -> List[CodeEntity]:
        """Parse Python file using AST."""
        entities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    entities.append(CodeEntity(
                        name=node.name,
                        type='function',
                        file_path=str(file_path),
                        line_start=node.lineno,
                        line_end=getattr(node, 'end_lineno', None) or node.lineno,
                        docstring=ast.get_docstring(node),
                        parameters=[arg.arg for arg in node.args.args],
                        return_type=self._annotation_to_string(node.returns),
                        dependencies=self._extract_dependencies(node)
                    ))
                
                elif isinstance(node, ast.ClassDef):
                    entities.append(CodeEntity(
                        name=node.name,
                        type='class',
                        file_path=str(file_path),
                        line_start=node.lineno,
                        line_end=getattr(node, 'end_lineno', None) or node.lineno,
                        docstring=ast.get_docstring(node),
                        dependencies=self._extract_dependencies(node)
                    ))
                
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        entities.append(CodeEntity(
                            name=alias.name,
                            type='import',
                            file_path=str(file_path),
                            line_start=node.lineno,
                            line_end=node.lineno,
                            dependencies=[alias.name]
                        ))
        
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
        
        return entities

    def _annotation_to_string(self, annotation) -> Optional[str]:
        """Return a readable representation of a Python type annotation."""
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except Exception:
            return None
    
    def _extract_dependencies(self, node) -> List[str]:
        """Extract function/class dependencies from AST node."""
        dependencies = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)
        
        return list(set(dependencies))
    
    def _parse_javascript(self, file_path: Path) -> List[CodeEntity]:
        """Parse JavaScript/TypeScript file."""
        entities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex-based parsing for JS/TS
            import re
            
            # Find function declarations
            func_pattern = r'(?:async\s+)?function\s+(\w+)\s*\((.*?)\)'
            for match in re.finditer(func_pattern, content, re.MULTILINE):
                name, params = match.groups()
                line_num = content[:match.start()].count('\n') + 1
                entities.append(CodeEntity(
                    name=name,
                    type='function',
                    file_path=str(file_path),
                    line_start=line_num,
                    line_end=line_num,
                    parameters=[p.strip().split('=')[0].strip() for p in params.split(',') if p.strip()],
                    dependencies=[]
                ))
            
            # Find arrow functions
            arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>'
            for match in re.finditer(arrow_pattern, content, re.MULTILINE):
                name, params = match.groups()
                line_num = content[:match.start()].count('\n') + 1
                entities.append(CodeEntity(
                    name=name,
                    type='function',
                    file_path=str(file_path),
                    line_start=line_num,
                    line_end=line_num,
                    parameters=[p.strip().split(':')[0].strip() for p in params.split(',') if p.strip()],
                    dependencies=[]
                ))
            
            # Find class declarations
            class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
            for match in re.finditer(class_pattern, content, re.MULTILINE):
                name, extends = match.groups()
                line_num = content[:match.start()].count('\n') + 1
                deps = [extends] if extends else []
                entities.append(CodeEntity(
                    name=name,
                    type='class',
                    file_path=str(file_path),
                    line_start=line_num,
                    line_end=line_num,
                    dependencies=deps
                ))
            
            # Find imports
            import_pattern = r'(?:import|require)\s+(?:.*?\s+from\s+)?[\'"]([^\'"]+)[\'"]'
            for match in re.finditer(import_pattern, content, re.MULTILINE):
                module = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                entities.append(CodeEntity(
                    name=module,
                    type='import',
                    file_path=str(file_path),
                    line_start=line_num,
                    line_end=line_num,
                    dependencies=[module]
                ))
        
        except Exception as e:
            print(f"Error parsing JavaScript {file_path}: {e}")
        
        return entities
    
    def _get_code_files(self, repo_path: Path) -> List[Path]:
        """Get all code files from repository."""
        code_files = []
        
        for ext in self.SUPPORTED_LANGUAGES.keys():
            code_files.extend(repo_path.rglob(f"*{ext}"))
        
        # Filter out ignored directories
        ignored = {'node_modules', '__pycache__', 'venv', '.git', 'build', 'dist'}
        
        return [f for f in code_files if not any(ig in f.parts for ig in ignored)]
