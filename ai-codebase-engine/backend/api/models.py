from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Literal


# ── Request models ────────────────────────────────────────────────────────────

class GithubUploadRequest(BaseModel):
    github_url: str
    branch: Optional[str] = "main"


class ChatRequest(BaseModel):
    repo_id: str
    question: str
    n_results: Optional[int] = 5


class DocGenRequest(BaseModel):
    repo_id: str
    mode: Literal["docstrings", "readme", "all"] = "all"


class SecurityScanRequest(BaseModel):
    repo_id: str


class FileDepsRequest(BaseModel):
    repo_id: str
    file_path: str


# ── Response models ───────────────────────────────────────────────────────────

class RepoStats(BaseModel):
    total_files: int
    total_functions: int
    total_classes: int
    total_imports: int
    security_issues: int


class UploadResponse(BaseModel):
    repo_id: str
    status: str
    stats: RepoStats


class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]


class SecurityIssue(BaseModel):
    type: str
    file: str
    line: int
    code: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]


class SecurityResponse(BaseModel):
    issues: List[SecurityIssue]
    total: int
    critical: int
    high: int


class ArchitectureResponse(BaseModel):
    analysis: str
    circular_dependencies: List[List[str]]
    hotspots: List[dict]
    graph_summary: dict


class DocGenResponse(BaseModel):
    status: str
    readme: Optional[str] = None
    docstrings: Optional[List[dict]] = None