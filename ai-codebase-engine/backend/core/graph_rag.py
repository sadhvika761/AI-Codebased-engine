import networkx as nx
from typing import List, Dict
from collections import defaultdict

class GraphRAG:
    """Advanced Graph-based Retrieval Augmented Generation."""
    
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.pagerank = None
        self.communities = None
        self._compute_metrics()
    
    def _compute_metrics(self):
        """Pre-compute important graph metrics."""
        try:
            self.pagerank = nx.pagerank(self.graph)
            # Community detection
            undirected = self.graph.to_undirected()
            self.communities = nx.community.greedy_modularity_communities(undirected)
        except:
            self.pagerank = {}
            self.communities = []
    
    def get_context_for_entity(self, entity_name: str, depth: int = 2) -> Dict:
        """Get rich context for an entity using graph traversal."""
        
        # Find the node
        matching_nodes = [n for n in self.graph.nodes() 
                         if entity_name in n]
        
        if not matching_nodes:
            return {"error": "Entity not found"}
        
        node = matching_nodes[0]
        
        # Get neighborhood
        context = {
            "entity": node,
            "metadata": self.graph.nodes[node],
            "direct_dependencies": [],
            "indirect_dependencies": [],
            "dependent_on_this": [],
            "related_entities": [],
            "importance_score": self.pagerank.get(node, 0),
            "community": self._get_community(node)
        }
        
        # Direct dependencies (what this calls)
        for successor in self.graph.successors(node):
            context["direct_dependencies"].append({
                "name": successor,
                "metadata": self.graph.nodes[successor]
            })
        
        # Things that depend on this
        for predecessor in self.graph.predecessors(node):
            context["dependent_on_this"].append({
                "name": predecessor,
                "metadata": self.graph.nodes[predecessor]
            })
        
        # Indirect dependencies (depth 2+)
        try:
            descendants = nx.descendants(self.graph, node)
            for desc in list(descendants)[:10]:  # Limit to top 10
                if desc not in [d["name"] for d in context["direct_dependencies"]]:
                    context["indirect_dependencies"].append({
                        "name": desc,
                        "metadata": self.graph.nodes[desc]
                    })
        except:
            pass
        
        # Related entities in same community
        community_members = self._get_community_members(node)
        context["related_entities"] = [
            {"name": m, "metadata": self.graph.nodes[m]} 
            for m in community_members[:5]
            if m != node
        ]
        
        return context
    
    def get_execution_path(self, start_entity: str, end_entity: str) -> List[str]:
        """Find execution path between two entities."""
        
        start_nodes = [n for n in self.graph.nodes() if start_entity in n]
        end_nodes = [n for n in self.graph.nodes() if end_entity in n]
        
        if not start_nodes or not end_nodes:
            return []
        
        try:
            path = nx.shortest_path(self.graph, start_nodes[0], end_nodes[0])
            return path
        except nx.NetworkXNoPath:
            return []
    
    def get_critical_paths(self, top_n: int = 5) -> List[Dict]:
        """Find most critical execution paths using centrality."""
        
        try:
            betweenness = nx.betweenness_centrality(self.graph)
            sorted_nodes = sorted(betweenness.items(), 
                                key=lambda x: x[1], 
                                reverse=True)[:top_n]
            
            critical = []
            for node, score in sorted_nodes:
                critical.append({
                    "entity": node,
                    "criticality_score": score,
                    "metadata": self.graph.nodes[node],
                    "influences": list(self.graph.successors(node))[:5]
                })
            
            return critical
        except:
            return []
    
    def get_workflow_for_feature(self, feature_keyword: str) -> List[Dict]:
        """Extract workflow for a specific feature."""
        
        relevant_nodes = [
            n for n in self.graph.nodes() 
            if feature_keyword.lower() in n.lower() or 
               feature_keyword.lower() in str(self.graph.nodes[n]).lower()
        ]
        
        if not relevant_nodes:
            return []
        
        # Build subgraph
        subgraph = self.graph.subgraph(relevant_nodes)
        
        workflow = []
        try:
            # Topological sort for execution order
            for node in nx.topological_sort(subgraph):
                workflow.append({
                    "step": len(workflow) + 1,
                    "entity": node,
                    "metadata": self.graph.nodes[node],
                    "calls": list(subgraph.successors(node))
                })
        except:
            # If cyclic, just return nodes
            for node in relevant_nodes:
                workflow.append({
                    "entity": node,
                    "metadata": self.graph.nodes[node]
                })
        
        return workflow
    
    def _get_community(self, node: str) -> int:
        """Get community ID for a node."""
        for idx, community in enumerate(self.communities):
            if node in community:
                return idx
        return -1
    
    def _get_community_members(self, node: str) -> List[str]:
        """Get all members of node's community."""
        community_id = self._get_community(node)
        if community_id >= 0:
            return list(self.communities[community_id])
        return []
    
    def get_subsystem_analysis(self) -> Dict:
        """Analyze codebase as interconnected subsystems."""
        
        subsystems = {}
        
        for idx, community in enumerate(self.communities):
            nodes = list(community)
            
            # Analyze this subsystem
            subgraph = self.graph.subgraph(nodes)
            
            subsystems[f"subsystem_{idx}"] = {
                "size": len(nodes),
                "entities": nodes[:10],  # Top 10
                "internal_connections": subgraph.number_of_edges(),
                "external_connections": self._count_external_edges(nodes),
                "key_entities": self._get_key_entities(nodes)[:3]
            }
        
        return subsystems
    
    def _count_external_edges(self, nodes: List[str]) -> int:
        """Count edges going outside this set of nodes."""
        count = 0
        for node in nodes:
            for successor in self.graph.successors(node):
                if successor not in nodes:
                    count += 1
        return count
    
    def _get_key_entities(self, nodes: List[str]) -> List[str]:
        """Get most important entities in a node set."""
        node_scores = {n: self.pagerank.get(n, 0) for n in nodes}
        return sorted(node_scores.keys(), 
                     key=lambda x: node_scores[x], 
                     reverse=True)