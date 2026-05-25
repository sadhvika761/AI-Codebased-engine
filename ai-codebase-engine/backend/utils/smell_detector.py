"""
Code smell detector — uses radon for cyclomatic complexity and raw metrics,
plus custom heuristics for long functions, too-many-parameters, etc.
"""
import ast
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, asdict

try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False


@dataclass
class CodeSmell:
    smell_type: str
    severity: str          # INFO | WARNING | ERROR
    file: str
    line: int
    name: str
    detail: str


class CodeSmellDetector:

    # Thresholds
    MAX_FUNCTION_LINES  = 50
    MAX_PARAMS          = 5
    MAX_COMPLEXITY      = 10   # cyclomatic
    MIN_MAINTAINABILITY = 20   # radon MI score (0–100)
    MAX_NESTING         = 4

    def scan_repository(self, repo_path: Path) -> List[Dict]:
        smells = []
        for py_file in repo_path.rglob("*.py"):
            if any(p in py_file.parts for p in ("venv", "__pycache__", ".git", "node_modules")):
                continue
            smells.extend(self.scan_file(py_file))
        return [asdict(s) for s in smells]

    def scan_file(self, file_path: Path) -> List[CodeSmell]:
        smells: List[CodeSmell] = []
        try:
            source = file_path.read_text(encoding="utf-8")
        except Exception:
            return smells

        smells += self._ast_smells(source, str(file_path))

        if RADON_AVAILABLE:
            smells += self._radon_complexity(source, str(file_path))
            smells += self._radon_maintainability(source, str(file_path))

        return smells

    # ── AST-based checks ──────────────────────────────────────────────────────

    def _ast_smells(self, source: str, path: str) -> List[CodeSmell]:
        smells = []
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return smells

        lines = source.splitlines()

        for node in ast.walk(tree):
            # Long functions
            if isinstance(node, ast.FunctionDef):
                length = (node.end_lineno or node.lineno) - node.lineno
                if length > self.MAX_FUNCTION_LINES:
                    smells.append(CodeSmell(
                        smell_type="long_function",
                        severity="WARNING",
                        file=path,
                        line=node.lineno,
                        name=node.name,
                        detail=f"{length} lines (max {self.MAX_FUNCTION_LINES})",
                    ))

                # Too many parameters
                params = len(node.args.args)
                if params > self.MAX_PARAMS:
                    smells.append(CodeSmell(
                        smell_type="too_many_parameters",
                        severity="WARNING",
                        file=path,
                        line=node.lineno,
                        name=node.name,
                        detail=f"{params} parameters (max {self.MAX_PARAMS})",
                    ))

                # Missing docstring
                if not ast.get_docstring(node):
                    smells.append(CodeSmell(
                        smell_type="missing_docstring",
                        severity="INFO",
                        file=path,
                        line=node.lineno,
                        name=node.name,
                        detail="Function has no docstring",
                    ))

                # Deep nesting
                max_depth = self._max_nesting_depth(node)
                if max_depth > self.MAX_NESTING:
                    smells.append(CodeSmell(
                        smell_type="deep_nesting",
                        severity="WARNING",
                        file=path,
                        line=node.lineno,
                        name=node.name,
                        detail=f"Nesting depth {max_depth} (max {self.MAX_NESTING})",
                    ))

            # Large class
            if isinstance(node, ast.ClassDef):
                methods = [n for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
                if len(methods) > 20:
                    smells.append(CodeSmell(
                        smell_type="god_class",
                        severity="ERROR",
                        file=path,
                        line=node.lineno,
                        name=node.name,
                        detail=f"{len(methods)} methods — consider splitting",
                    ))

            # Bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                smells.append(CodeSmell(
                    smell_type="bare_except",
                    severity="WARNING",
                    file=path,
                    line=node.lineno,
                    name="except",
                    detail="Bare except catches everything including KeyboardInterrupt",
                ))

            # TODO/FIXME/HACK comments
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                text = str(node.value.value)
                for tag in ("TODO", "FIXME", "HACK", "XXX"):
                    if tag in text:
                        smells.append(CodeSmell(
                            smell_type="todo_comment",
                            severity="INFO",
                            file=path,
                            line=node.lineno,
                            name=tag,
                            detail=text[:80],
                        ))

        # Inline TODO comments
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                for tag in ("TODO", "FIXME", "HACK"):
                    if tag in stripped:
                        smells.append(CodeSmell(
                            smell_type="todo_comment",
                            severity="INFO",
                            file=path,
                            line=i,
                            name=tag,
                            detail=stripped[:80],
                        ))

        return smells

    # ── Radon checks ─────────────────────────────────────────────────────────

    def _radon_complexity(self, source: str, path: str) -> List[CodeSmell]:
        smells = []
        try:
            results = cc_visit(source)
            for block in results:
                if block.complexity > self.MAX_COMPLEXITY:
                    smells.append(CodeSmell(
                        smell_type="high_complexity",
                        severity="ERROR" if block.complexity > 20 else "WARNING",
                        file=path,
                        line=block.lineno,
                        name=block.name,
                        detail=f"Cyclomatic complexity {block.complexity} (max {self.MAX_COMPLEXITY})",
                    ))
        except Exception:
            pass
        return smells

    def _radon_maintainability(self, source: str, path: str) -> List[CodeSmell]:
        smells = []
        try:
            mi = mi_visit(source, multi=True)
            if mi < self.MIN_MAINTAINABILITY:
                smells.append(CodeSmell(
                    smell_type="low_maintainability",
                    severity="ERROR",
                    file=path,
                    line=1,
                    name=path.split("/")[-1],
                    detail=f"Maintainability index {mi:.1f} (min {self.MIN_MAINTAINABILITY})",
                ))
        except Exception:
            pass
        return smells

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _max_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        NESTING_NODES = (ast.If, ast.For, ast.While, ast.With, ast.Try,
                         ast.ExceptHandler, ast.AsyncFor, ast.AsyncWith)
        max_d = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, NESTING_NODES):
                max_d = max(max_d, self._max_nesting_depth(child, depth + 1))
            else:
                max_d = max(max_d, self._max_nesting_depth(child, depth))
        return max_d

    def summarize(self, smells: List[Dict]) -> Dict:
        return {
            "total": len(smells),
            "by_severity": {
                "ERROR":   sum(1 for s in smells if s["severity"] == "ERROR"),
                "WARNING": sum(1 for s in smells if s["severity"] == "WARNING"),
                "INFO":    sum(1 for s in smells if s["severity"] == "INFO"),
            },
            "by_type": {t: sum(1 for s in smells if s["smell_type"] == t)
                        for t in {s["smell_type"] for s in smells}},
        }