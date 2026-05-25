from .base_agent import BaseAgent
from backend.core.embeddings import EmbeddingEngine
from backend.core.llm_client import LLMClient
from typing import Dict, Any, List


class RAGAgent(BaseAgent):
    """Agent that retrieves relevant code context and answers questions."""

    def __init__(self):
        super().__init__("RAGAgent")
        self.embedding_engine = EmbeddingEngine()

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        repo_id = task.get("repo_id")
        question = task.get("question")
        n_results = task.get("n_results", 5)

        if not repo_id or not question:
            return {"error": "repo_id and question are required"}

        try:
            # Retrieve relevant chunks
            results = self.embedding_engine.search(repo_id, question, n_results=n_results)

            if not results:
                return {
                    "answer": "No relevant code found for your question.",
                    "sources": [],
                    "context_used": [],
                }

            # Build answer using LLM
            if self.llm_client:
                answer = self.llm_client.answer_question(question, results)
            else:
                # Fallback if no LLM client
                answer = self._build_basic_answer(question, results)

            return {
                "answer": answer,
                "sources": [r["metadata"] for r in results],
                "context_used": [r["document"] for r in results],
            }
        except Exception as e:
            return {"error": f"RAG execution failed: {str(e)}", "answer": "", "sources": []}
    
    def _build_basic_answer(self, question: str, results: List[Dict]) -> str:
        """Fallback answer builder without LLM."""
        if not results:
            return "No relevant information found."
        context = "\n".join([r["document"] for r in results[:3]])
        return f"Based on the codebase:\n\n{context}\n\nThis is relevant to: {question}"

    def retrieve_context(self, repo_id: str, query: str, n: int = 5) -> List[Dict]:
        """Pure retrieval without LLM — useful for pipelines."""
        return self.embedding_engine.search(repo_id, query, n_results=n)