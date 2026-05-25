from .base_agent import BaseAgent
from backend.core.graph_builder import GraphBuilder
from typing import Dict, Any
import networkx as nx


class ArchitectureAgent(BaseAgent):
    """Agent that understands and explains system architecture."""

    def __init__(self):
        super().__init__("ArchitectureAgent")

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        entities = task.get("entities", [])
        graph = task.get("graph")  # pre-built nx.DiGraph (optional)

        if not entities and graph is None:
            return {"error": "entities or graph is required"}

        gb = GraphBuilder()
        if graph is None:
            graph = gb.build_graph(entities)
        else:
            gb.graph = graph

        graph_data = gb.export_to_json()
        circular_deps = gb.find_circular_dependencies()
        hotspots = gb.get_most_complex_functions(top_n=5)

        # LLM explanation
        analysis = self.llm_client.explain_architecture(graph_data)

        return {
            "analysis": analysis,
            "circular_dependencies": circular_deps,
            "hotspots": hotspots,
            "graph_summary": {
                "total_nodes": graph.number_of_nodes(),
                "total_edges": graph.number_of_edges(),
                "is_dag": nx.is_directed_acyclic_graph(graph),
                "components": nx.number_weakly_connected_components(graph),
            },
        }

    def get_file_dependencies(self, entities: list, file_path: str) -> Dict:
        """Return what a specific file depends on and what depends on it."""
        gb = GraphBuilder()
        graph = gb.build_graph(entities)

        file_nodes = [n for n in graph.nodes() if file_path in n]
        dependents = set()
        dependencies = set()

        for node in file_nodes:
            dependents.update(graph.predecessors(node))
            dependencies.update(graph.successors(node))

        return {
            "file": file_path,
            "depends_on": list(dependencies),
            "depended_on_by": list(dependents),
        }