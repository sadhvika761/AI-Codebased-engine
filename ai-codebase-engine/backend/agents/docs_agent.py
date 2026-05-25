from .base_agent import BaseAgent
from typing import Dict, Any, List
import ast
from pathlib import Path


class DocsAgent(BaseAgent):
    """Agent that generates documentation for code entities."""

    def __init__(self):
        super().__init__("DocsAgent")

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        entities = task.get("entities", [])
        mode = task.get("mode", "docstrings")  # 'docstrings' | 'readme' | 'all'

        if not entities:
            return {"error": "No entities provided"}

        results = {}

        if mode in ("docstrings", "all"):
            results["docstrings"] = self._generate_docstrings(entities)

        if mode in ("readme", "all"):
            results["readme"] = self._generate_readme(entities, task.get("repo_name", "Project"))

        return {"status": "success", **results}

    # ── Docstring generation ──────────────────────────────────────────────────

    def _generate_docstrings(self, entities: List[Dict]) -> List[Dict]:
        documented = []
        for entity in entities:
            if entity.get("type") in ("function", "class"):
                try:
                    if not self.llm_client:
                        doc = f"Auto-generated doc for {entity['name']}"
                    else:
                        doc = self.llm_client.generate_documentation(entity)
                    documented.append({
                        "name": entity["name"],
                        "type": entity["type"],
                        "file": entity["file_path"],
                        "generated_doc": doc,
                    })
                except Exception as e:
                    print(f"Error generating doc for {entity['name']}: {e}")
        return documented

    # ── README generation ─────────────────────────────────────────────────────

    def _generate_readme(self, entities: List[Dict], repo_name: str) -> str:
        files = list({e["file_path"] for e in entities})
        functions = [e["name"] for e in entities if e.get("type") == "function"]
        classes = [e["name"] for e in entities if e.get("type") == "class"]

        summary_prompt = f"""Generate a professional README.md for a project called '{repo_name}'.

Project contains:
- {len(files)} source files
- {len(functions)} functions: {', '.join(functions[:10])}{'...' if len(functions) > 10 else ''}
- {len(classes)} classes: {', '.join(classes[:10])}{'...' if len(classes) > 10 else ''}

Include: overview, features, installation, usage, project structure, and contributing sections."""

        return self.llm_client.analyze_code(summary_prompt, "")

    # ── Inline docstring injection ────────────────────────────────────────────

    def inject_docstrings_into_file(self, file_path: str, entities: List[Dict]) -> str:
        """
        Read a Python file and insert generated docstrings where they are missing.
        Returns the modified source code as a string.
        """
        path = Path(file_path)
        if not path.exists() or path.suffix != ".py":
            return ""

        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)

        # Map entity name → generated doc
        doc_map = {e["name"]: e.get("generated_doc", "") for e in entities}

        inserts: List[tuple] = []  # (line_number_0indexed, text_to_insert)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node) and node.name in doc_map:
                    indent = " " * (node.col_offset + 4)
                    docstring_lines = f'{indent}"""\n'
                    for dl in doc_map[node.name].splitlines():
                        docstring_lines += f"{indent}{dl}\n"
                    docstring_lines += f'{indent}"""\n'
                    # Insert after the def/class line
                    inserts.append((node.body[0].lineno - 1, docstring_lines))

        # Apply inserts from bottom to top so line numbers stay valid
        for lineno, text in sorted(inserts, reverse=True):
            lines.insert(lineno, text)

        return "".join(lines)