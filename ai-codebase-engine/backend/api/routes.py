from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import PlainTextResponse
import uuid
import os
import tempfile

from backend.api.models import (
    GithubUploadRequest, ChatRequest, DocGenRequest,
    FileDepsRequest, UploadResponse, ChatResponse,
    SecurityResponse, ArchitectureResponse, DocGenResponse,
)
from backend.utils.repo_loader import RepoLoader
from backend.agents.parser_agent import ParserAgent
from backend.agents.security_agent import SecurityAgent
from backend.agents.rag_agent import RAGAgent
from backend.agents.architecture_agent import ArchitectureAgent
from backend.agents.docs_agent import DocsAgent
from backend.core.embeddings import EmbeddingEngine
from backend.core.graph_builder import GraphBuilder
from backend.core.llm_client import LLMClient

router = APIRouter()

# ── Shared singletons ─────────────────────────────────────────────────────────

repo_loader = RepoLoader()
llm_client  = LLMClient()

parser_agent   = ParserAgent()
security_agent = SecurityAgent()
rag_agent      = RAGAgent()
arch_agent     = ArchitectureAgent()
docs_agent     = DocsAgent()

# Inject LLM into agents that need it
for agent in (rag_agent, arch_agent, docs_agent):
    agent.set_llm_client(llm_client)

embedding_engine = EmbeddingEngine()

# In-memory session store with persistence
import json
from pathlib import Path

SESSIONS_FILE = Path("data/.sessions.json")
sessions: dict = {}

def _load_sessions():
    """Load sessions from persistent storage."""
    global sessions
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, 'r') as f:
                data = json.load(f)
                # Deserialize graph objects
                for repo_id, session in data.items():
                    if 'graph' in session:
                        import networkx as nx
                        session['graph'] = nx.node_link_graph(session['graph'], directed=True)
                sessions = data
        except Exception as e:
            print(f"Error loading sessions: {e}")
            sessions = {}

def _save_sessions():
    """Save sessions to persistent storage."""
    try:
        SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        data_to_save = {}
        for repo_id, session in sessions.items():
            session_copy = session.copy()
            # Serialize graph to JSON-compatible format
            if 'graph' in session_copy:
                import networkx as nx
                session_copy['graph'] = nx.node_link_data(session_copy['graph'])
            data_to_save[repo_id] = session_copy
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    except Exception as e:
        print(f"Error saving sessions: {e}")

# Load on startup
_load_sessions()


# ── Helper ────────────────────────────────────────────────────────────────────

def _require_session(repo_id: str) -> dict:
    if repo_id not in sessions:
        raise HTTPException(status_code=404, detail="Repository session not found. Upload it first.")
    return sessions[repo_id]


def _ingest(repo_id: str, repo_path) -> dict:
    """Parse, embed, graph-build, and security-scan a repo. Returns session dict."""
    try:
        parse_result   = parser_agent.execute({"repo_path": repo_path})
        if "error" in parse_result:
            raise Exception(f"Parser error: {parse_result['error']}")
        
        entities       = parse_result["entities"]

        embedding_engine.embed_repository(repo_id, entities)

        graph_builder = GraphBuilder()
        graph          = graph_builder.build_graph(entities)
        security_result = security_agent.execute({"entities": entities})

        session = {
            "repo_path":       str(repo_path),
            "entities":        entities,
            "graph":           graph,
            "security_issues": security_result["issues"],
        }
        sessions[repo_id] = session
        _save_sessions()  # Save to disk
        return session
    except Exception as e:
        print(f"Ingestion error for {repo_id}: {e}")
        raise


# ── Upload endpoints ──────────────────────────────────────────────────────────

@router.post("/upload/github", response_model=UploadResponse)
def upload_github(request: GithubUploadRequest):
    """Clone a GitHub repository and analyse it."""
    repo_id  = str(uuid.uuid4())
    try:
        repo_path = repo_loader.load_from_github(request.github_url, repo_id)
        session   = _ingest(repo_id, repo_path)
        entities  = session["entities"]
        return UploadResponse(
            repo_id=repo_id,
            status="success",
            stats={
                "total_files":     len({e["file_path"] for e in entities}),
                "total_functions": sum(1 for e in entities if e["type"] == "function"),
                "total_classes":   sum(1 for e in entities if e["type"] == "class"),
                "total_imports":   sum(1 for e in entities if e["type"] == "import"),
                "security_issues": len(session["security_issues"]),
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/upload/zip", response_model=UploadResponse)
def upload_zip(file: UploadFile = File(...)):
    """Upload a ZIP archive of a repository."""
    repo_id = str(uuid.uuid4())
    try:
        suffix  = os.path.splitext(file.filename or "repo.zip")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        repo_path = repo_loader.load_from_zip(tmp_path, repo_id)
        os.unlink(tmp_path)

        session  = _ingest(repo_id, repo_path)
        entities = session["entities"]
        return UploadResponse(
            repo_id=repo_id,
            status="success",
            stats={
                "total_files":     len({e["file_path"] for e in entities}),
                "total_functions": sum(1 for e in entities if e["type"] == "function"),
                "total_classes":   sum(1 for e in entities if e["type"] == "class"),
                "total_imports":   sum(1 for e in entities if e["type"] == "import"),
                "security_issues": len(session["security_issues"]),
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Analysis endpoints ────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Ask a natural-language question about the codebase."""
    _require_session(request.repo_id)
    try:
        result = rag_agent.execute({
            "repo_id":  request.repo_id,
            "question": request.question,
            "n_results": request.n_results,
        })
        return ChatResponse(answer=result["answer"], sources=result["sources"])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/repo/{repo_id}/security", response_model=SecurityResponse)
def security_scan(repo_id: str):
    """Return security vulnerabilities found during ingestion."""
    session = _require_session(repo_id)
    issues  = session["security_issues"]
    return SecurityResponse(
        issues=issues,
        total=len(issues),
        critical=sum(1 for i in issues if i["severity"] == "CRITICAL"),
        high=sum(1 for i in issues if i["severity"] == "HIGH"),
    )


@router.get("/repo/{repo_id}/architecture", response_model=ArchitectureResponse)
def architecture(repo_id: str):
    """Return AI-generated architecture analysis + graph metrics."""
    session = _require_session(repo_id)
    result  = arch_agent.execute({
        "entities": session["entities"],
        "graph":    session["graph"],
    })
    return ArchitectureResponse(**result)


@router.get("/repo/{repo_id}/graph")
def dependency_graph(repo_id: str):
    """Return the full dependency graph as JSON (nodes + edges)."""
    session = _require_session(repo_id)
    gb = GraphBuilder()
    gb.graph = session["graph"]
    return gb.export_to_json()


@router.post("/repo/docs", response_model=DocGenResponse)
def generate_docs(request: DocGenRequest):
    """Generate documentation (README and/or docstrings)."""
    session = _require_session(request.repo_id)
    result  = docs_agent.execute({
        "entities":  session["entities"],
        "mode":      request.mode,
        "repo_name": session["repo_path"].split("/")[-1],
    })
    return DocGenResponse(**result)


@router.get("/repo/{repo_id}/file-deps")
def file_dependencies(repo_id: str, file_path: str):
    """Return what a specific file depends on and what depends on it."""
    session = _require_session(repo_id)
    return arch_agent.get_file_dependencies(session["entities"], file_path)


@router.get("/repo/{repo_id}/stats")
def repo_stats(repo_id: str):
    """Return overview metrics on the repository."""
    session = _require_session(repo_id)
    entities = session["entities"]
    return {
        "total_files":     len({e["file_path"] for e in entities}),
        "total_functions": sum(1 for e in entities if e["type"] == "function"),
        "total_classes":   sum(1 for e in entities if e["type"] == "class"),
        "total_imports":   sum(1 for e in entities if e["type"] == "import"),
        "security_issues": len(session["security_issues"]),
    }


@router.get("/repo/{repo_id}/structure")
def file_structure(repo_id: str):
    """Return the file tree of the repository."""
    session   = _require_session(repo_id)
    from pathlib import Path
    return repo_loader.get_file_structure(Path(session["repo_path"]))


@router.get("/repo/{repo_id}/smells")
def code_smells(repo_id: str):
    """Detect code smells (complexity, long functions, bare excepts, etc.)."""
    session = _require_session(repo_id)
    from backend.utils.smell_detector import CodeSmellDetector
    from pathlib import Path
    detector = CodeSmellDetector()
    smells   = detector.scan_repository(Path(session["repo_path"]))
    return {"smells": smells, "summary": detector.summarize(smells)}


@router.delete("/repo/{repo_id}")
def delete_repo(repo_id: str):
    """Remove a session and its embeddings from memory."""
    _require_session(repo_id)
    sessions.pop(repo_id, None)
    _save_sessions()  # Save to disk
    return {"status": "deleted", "repo_id": repo_id}